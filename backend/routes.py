from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mock_platforms.platform_manager import send_restriction_to_platforms

from backend.database import get_db
from backend.models import (
    User,
    Incident,
    SafetyZone,
    Restriction,
    RestrictionService,
    Alert,
    EmergencyUnit,
    WorkerLocation,
    CitizenReport,
    AuditLog
)

from backend.schemas import (
    IncidentCreate,
    IncidentWorkflowResponse,
    SafetyZoneCreate,
    RestrictionCreate,
    RestrictionServiceCreate,
    AlertCreate,
    EmergencyUnitCreate,
    WorkerLocationCreate,
    CitizenReportCreate,
    AuditLogCreate
)

from backend.decision_engine import (
    calculate_risk,
    find_nearest_units,
    recommend_deployment,
    check_worker_in_zone
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


# ---------------- INCIDENTS ----------------

@router.get("/")
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()
    return incidents


@router.post("/", response_model=IncidentWorkflowResponse)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):
    # Calculate risk and recommended response
    risk = calculate_risk(incident.severity)

    # Create incident
    new_incident = Incident(
        type=incident.type,
        description=incident.description,
        latitude=incident.latitude,
        longitude=incident.longitude,
        severity=incident.severity,
        status=incident.status,
        created_by=incident.created_by
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    # Automatically create safety zone
    new_zone = SafetyZone(
        name=incident.type + " Safety Zone",
        latitude=incident.latitude,
        longitude=incident.longitude,
        radius=risk["zone_radius"],
        zone_type=risk["zone_type"],
        severity=risk["risk_level"],
        status="ACTIVE",
        incident_id=new_incident.id
    )

    db.add(new_zone)
    db.commit()
    db.refresh(new_zone)

    # Automatically create restriction
    new_restriction = Restriction(
        zone_id=new_zone.id,
        action=risk["recommended_action"],
        start_time="00:00:00",
        end_time="23:59:59",
        status="ACTIVE",
        created_by=incident.created_by
    )

    db.add(new_restriction)
    db.commit()
    db.refresh(new_restriction)

    # Send restriction to mock platforms
    restriction_data = {
        "zone_id": new_restriction.zone_id,
        "action": new_restriction.action,
        "start_time": str(new_restriction.start_time),
        "end_time": str(new_restriction.end_time)
    }

    platform_results = send_restriction_to_platforms(
        restriction_data
    )

    # Automatically add affected services
    for service_name in risk.get("affected_services", []):
        new_service = RestrictionService(
            restriction_id=new_restriction.id,
            service=service_name
        )
        db.add(new_service)

    db.commit()

    # Automatically create alerts for users
    users = db.query(User).all()

    for user in users:
        new_alert = Alert(
            user_id=user.id,
            zone_id=new_zone.id,
            message=(
                f"Safety alert: {incident.type} detected. "
                f"A {risk['zone_radius']}m {risk['zone_type']} zone "
                f"has been created. Please avoid the affected area."
            ),
            alert_type="SAFETY_ZONE",
            status="UNREAD"
        )

        db.add(new_alert)

    db.commit()

    # Find nearest available emergency units
    emergency_units = db.query(EmergencyUnit).all()

    nearest_units = find_nearest_units(
        incident.latitude,
        incident.longitude,
        emergency_units
    )

    # Generate deployment recommendation
    deployment_recommendation = recommend_deployment(
        nearest_units,
        risk["risk_level"]
    )

    # Update deployed emergency units
    for recommendation in deployment_recommendation:
        if recommendation["recommendation"] == "DEPLOY":
            unit = db.query(EmergencyUnit).filter(
                EmergencyUnit.id == recommendation["unit_id"]
            ).first()

            if unit:
                unit.status = "DEPLOYED"

    db.commit()

    return {
        "incident": new_incident,
        "decision": risk,
        "safety_zone": new_zone,
        "restriction": new_restriction,
        "nearest_emergency_units": nearest_units,
        "deployment_recommendation": deployment_recommendation,
        "deployment_status": "UNITS_DEPLOYED"
    }


# ---------------- SAFETY ZONES ----------------

@router.post("/zones")
def create_safety_zone(
    zone: SafetyZoneCreate,
    db: Session = Depends(get_db)
):
    new_zone = SafetyZone(
        name=zone.name,
        latitude=zone.latitude,
        longitude=zone.longitude,
        radius=zone.radius,
        zone_type=zone.zone_type,
        severity=zone.severity,
        status=zone.status,
        incident_id=zone.incident_id
    )

    db.add(new_zone)
    db.commit()
    db.refresh(new_zone)

    return new_zone


@router.get("/zones")
def get_safety_zones(db: Session = Depends(get_db)):
    zones = db.query(SafetyZone).all()
    return zones


# ---------------- RESTRICTIONS ----------------

@router.post("/restrictions")
def create_restriction(
    restriction: RestrictionCreate,
    db: Session = Depends(get_db)
):
    new_restriction = Restriction(
        zone_id=restriction.zone_id,
        action=restriction.action,
        start_time=restriction.start_time,
        end_time=restriction.end_time,
        status=restriction.status,
        created_by=restriction.created_by
    )

    db.add(new_restriction)
    db.commit()
    db.refresh(new_restriction)

    # Send government restriction to all mock platforms
    restriction_data = {
        "zone_id": new_restriction.zone_id,
        "action": new_restriction.action,
        "start_time": str(new_restriction.start_time),
        "end_time": str(new_restriction.end_time)
    }

    platform_results = send_restriction_to_platforms(
        restriction_data
    )

    return {
        "restriction": new_restriction,
        "platform_results": platform_results
    }


@router.get("/restrictions")
def get_restrictions(db: Session = Depends(get_db)):
    restrictions = db.query(Restriction).all()
    return restrictions


# ---------------- RESTRICTION SERVICES ----------------

@router.post("/restriction-services")
def create_restriction_service(
    service: RestrictionServiceCreate,
    db: Session = Depends(get_db)
):
    new_service = RestrictionService(
        restriction_id=service.restriction_id,
        service=service.service
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.get("/restriction-services")
def get_restriction_services(db: Session = Depends(get_db)):
    return db.query(RestrictionService).all()


# ---------------- ALERTS ----------------

@router.post("/alerts")
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db)
):
    new_alert = Alert(
        user_id=alert.user_id,
        zone_id=alert.zone_id,
        message=alert.message,
        alert_type=alert.alert_type,
        status=alert.status
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).all()


# ---------------- EMERGENCY UNITS ----------------

@router.post("/emergency-units")
def create_emergency_unit(
    unit: EmergencyUnitCreate,
    db: Session = Depends(get_db)
):
    new_unit = EmergencyUnit(
        type=unit.type,
        unit_name=unit.unit_name,
        latitude=unit.latitude,
        longitude=unit.longitude,
        status=unit.status
    )

    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)

    return new_unit


@router.get("/emergency-units")
def get_emergency_units(db: Session = Depends(get_db)):
    return db.query(EmergencyUnit).all()


# ---------------- WORKER LOCATIONS ----------------

@router.post("/worker-locations")
def create_worker_location(
    location: WorkerLocationCreate,
    db: Session = Depends(get_db)
):
    new_location = WorkerLocation(
        worker_id=location.worker_id,
        latitude=location.latitude,
        longitude=location.longitude,
        recorded_at=datetime.utcnow()
    )

    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location


@router.get("/worker-locations")
def get_worker_locations(db: Session = Depends(get_db)):
    return db.query(WorkerLocation).all()


# ---------------- CITIZEN REPORTS ----------------

@router.post("/citizen-reports")
def create_citizen_report(
    report: CitizenReportCreate,
    db: Session = Depends(get_db)
):
    new_report = CitizenReport(
        user_id=report.user_id,
        description=report.description,
        latitude=report.latitude,
        longitude=report.longitude,
        image_url=report.image_url,
        status=report.status
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report


@router.get("/citizen-reports")
def get_citizen_reports(db: Session = Depends(get_db)):
    return db.query(CitizenReport).all()


# ---------------- AUDIT LOGS ----------------

@router.post("/audit-logs")
def create_audit_log(
    log: AuditLogCreate,
    db: Session = Depends(get_db)
):
    new_log = AuditLog(
        user_id=log.user_id,
        action=log.action,
        entity_type=log.entity_type,
        entity_id=log.entity_id,
        created_at=datetime.utcnow()
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


@router.get("/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).all()


# ---------------- WORKER SAFETY CHECK ----------------

@router.post("/worker-check")
def worker_check(
    worker: WorkerLocationCreate,
    db: Session = Depends(get_db)
):
    zone = db.query(SafetyZone).filter(
        SafetyZone.status == "ACTIVE"
    ).order_by(SafetyZone.id.desc()).first()

    if not zone:
        return {
            "error": "No active safety zone found"
        }

    result = check_worker_in_zone(
        worker.latitude,
        worker.longitude,
        zone.latitude,
        zone.longitude,
        zone.radius
    )

    # Create alert if worker is inside restricted zone
    if result["inside_zone"]:
        new_alert = Alert(
            user_id=worker.worker_id,
            zone_id=zone.id,
            message=(
                f"WARNING: You are inside the restricted safety zone. "
                f"Distance from incident: "
                f"{result['distance_meters']} meters."
            ),
            alert_type="WORKER_ZONE_ALERT",
            status="UNREAD"
        )

        db.add(new_alert)
        db.commit()

    return {
        "worker_id": worker.worker_id,
        "zone_id": zone.id,
        "zone_name": zone.name,
        "zone_radius": zone.radius,
        **result
    }

# ---------------- GET INCIDENT BY ID ----------------

@router.get("/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        return {"error": "Incident not found"}

    return incident


# ---------------- UPDATE INCIDENT ----------------

@router.put("/{incident_id}")
def update_incident(
    incident_id: int,
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not existing:
        return {"error": "Incident not found"}

    existing.type = incident.type
    existing.description = incident.description
    existing.latitude = incident.latitude
    existing.longitude = incident.longitude
    existing.severity = incident.severity
    existing.status = incident.status

    db.commit()
    db.refresh(existing)

    return existing


# ---------------- UPDATE SAFETY ZONE ----------------

@router.put("/zones/{zone_id}")
def update_safety_zone(
    zone_id: int,
    zone: SafetyZoneCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(SafetyZone).filter(
        SafetyZone.id == zone_id
    ).first()

    if not existing:
        return {"error": "Safety zone not found"}

    existing.name = zone.name
    existing.latitude = zone.latitude
    existing.longitude = zone.longitude
    existing.radius = zone.radius
    existing.zone_type = zone.zone_type
    existing.severity = zone.severity
    existing.status = zone.status
    existing.incident_id = zone.incident_id

    db.commit()
    db.refresh(existing)

    return existing


# ---------------- UPDATE RESTRICTION ----------------

@router.put("/restrictions/{restriction_id}")
def update_restriction(
    restriction_id: int,
    restriction: RestrictionCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Restriction).filter(
        Restriction.id == restriction_id
    ).first()

    if not existing:
        return {"error": "Restriction not found"}

    existing.zone_id = restriction.zone_id
    existing.action = restriction.action
    existing.start_time = restriction.start_time
    existing.end_time = restriction.end_time
    existing.status = restriction.status
    existing.created_by = restriction.created_by

    db.commit()
    db.refresh(existing)

    return existing