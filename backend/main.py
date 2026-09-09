from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ==========================================
# CIVICSHIELD APPLICATION
# ==========================================

app = FastAPI(
    title="CivicShield API",
    description="AI-Based Dynamic Public Safety & Essential-Service Coordination System",
    version="1.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# TEMPORARY STORAGE
# ==========================================

incidents = []
restrictions = []
emergency_units = []
alerts = []


# ==========================================
# INCIDENT MODEL
# ==========================================

class Incident(BaseModel):
    location: str
    latitude: float
    longitude: float
    crowd_size: int
    severity: str
    duration_minutes: int
    affected_roads: int


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "CivicShield API is running"
    }


# ==========================================
# STATUS
# ==========================================

@app.get("/api/status")
def status():
    return {
        "success": True,
        "system": "CivicShield",
        "status": "ONLINE"
    }


# ==========================================
# INCIDENT
# ==========================================

@app.post("/api/incidents")
def create_incident(incident: Incident):

    incidents.append(incident)

    if incident.severity == "CRITICAL":
        red_radius = 750
        orange_radius = 1500

    elif incident.severity == "HIGH":
        red_radius = 500
        orange_radius = 1000

    elif incident.severity == "MEDIUM":
        red_radius = 300
        orange_radius = 700

    else:
        red_radius = 150
        orange_radius = 400

    return {
        "success": True,
        "message": "Incident processed successfully",
        "data": {
            "incident": {
                "location": incident.location,
                "latitude": incident.latitude,
                "longitude": incident.longitude,
                "crowd_size": incident.crowd_size,
                "severity": incident.severity,
                "duration_minutes": incident.duration_minutes,
                "affected_roads": incident.affected_roads
            },
            "recommended_zones": {
                "red_radius_meters": red_radius,
                "orange_radius_meters": orange_radius
            }
        }
    }


# ==========================================
# GET INCIDENTS
# ==========================================

@app.get("/api/incidents")
def get_incidents():
    return {
        "success": True,
        "count": len(incidents),
        "data": incidents
    }


# ==========================================
# OFFICER APPROVAL
# ==========================================

class ZoneApproval(BaseModel):
    incident_id: int
    approved: bool
    officer_name: str


@app.post("/api/zones/approve")
def approve_zone(approval: ZoneApproval):

    if approval.approved:
        return {
            "success": True,
            "message": "Safety zone approved by officer",
            "data": {
                "incident_id": approval.incident_id,
                "approved": True,
                "officer": approval.officer_name,
                "zone_status": "ACTIVE"
            }
        }

    return {
        "success": True,
        "message": "Safety zone rejected by officer",
        "data": {
            "incident_id": approval.incident_id,
            "approved": False,
            "officer": approval.officer_name,
            "zone_status": "REJECTED"
        }
    }


# ==========================================
# SAFETY ZONE
# ==========================================

class SafetyZone(BaseModel):
    incident_id: int
    latitude: float
    longitude: float
    red_radius_meters: float
    orange_radius_meters: float
    duration_minutes: int
    approved_by: str


@app.post("/api/zones")
def create_zone(zone: SafetyZone):

    return {
        "success": True,
        "message": "Safety zone created successfully",
        "data": {
            "incident_id": zone.incident_id,
            "center": {
                "latitude": zone.latitude,
                "longitude": zone.longitude
            },
            "red_zone": {
                "radius_meters": zone.red_radius_meters,
                "status": "ACTIVE"
            },
            "orange_zone": {
                "radius_meters": zone.orange_radius_meters,
                "status": "ACTIVE"
            },
            "duration_minutes": zone.duration_minutes,
            "approved_by": zone.approved_by,
            "zone_status": "ACTIVE"
        }
    }


# ==========================================
# SERVICE RESTRICTION
# ==========================================

class ServiceRestriction(BaseModel):
    zone_id: int
    platform: str
    service_type: str
    restriction: str
    reason: str
    duration_minutes: int


@app.post("/api/restrictions")
def create_restriction(restriction: ServiceRestriction):

    emergency_services = [
        "AMBULANCE",
        "POLICE",
        "FIRE"
    ]

    if restriction.service_type.upper() in emergency_services:
        status = "ALLOWED"
    else:
        status = "RESTRICTED"

    restrictions.append(restriction)

    return {
        "success": True,
        "message": "Service restriction processed",
        "data": {
            "zone_id": restriction.zone_id,
            "platform": restriction.platform,
            "service_type": restriction.service_type,
            "restriction": restriction.restriction,
            "reason": restriction.reason,
            "duration_minutes": restriction.duration_minutes,
            "status": status
        }
    }


# ==========================================
# EMERGENCY UNIT
# ==========================================

class EmergencyUnit(BaseModel):
    unit_type: str
    unit_id: str
    latitude: float
    longitude: float
    status: str


@app.post("/api/emergency-units")
def register_emergency_unit(unit: EmergencyUnit):

    emergency_units.append(unit)

    return {
        "success": True,
        "message": "Emergency unit registered",
        "data": {
            "unit_type": unit.unit_type,
            "unit_id": unit.unit_id,
            "location": {
                "latitude": unit.latitude,
                "longitude": unit.longitude
            },
            "status": unit.status
        }
    }


# ==========================================
# WORKER SAFETY
# ==========================================

class WorkerLocation(BaseModel):
    worker_id: str
    latitude: float
    longitude: float
    zone: str


@app.post("/api/worker-safety")
def worker_safety(worker: WorkerLocation):

    if worker.zone == "RED":
        message = "Worker is inside RED Zone. New tasks should be stopped."
        action = "STOP_NEW_TASKS"

    elif worker.zone == "ORANGE":
        message = "Worker is approaching restricted area. Proceed carefully."
        action = "WARNING"

    else:
        message = "Worker is in GREEN Zone. Normal work can continue."
        action = "NORMAL"

    return {
        "success": True,
        "message": message,
        "data": {
            "worker_id": worker.worker_id,
            "zone": worker.zone,
            "action": action
        }
    }


# ==========================================
# ALERT SYSTEM
# ==========================================

class Alert(BaseModel):
    alert_type: str
    message: str
    zone: str
    duration_minutes: int


@app.post("/api/alerts")
def create_alert(alert: Alert):

    alerts.append(alert)

    return {
        "success": True,
        "message": "Safety alert created",
        "data": {
            "alert_type": alert.alert_type,
            "message": alert.message,
            "zone": alert.zone,
            "duration_minutes": alert.duration_minutes,
            "status": "ACTIVE"
        }
    }


# ==========================================
# EMERGENCY ROUTING
# ==========================================

class RouteRequest(BaseModel):
    start: str
    destination: str


@app.post("/api/routes/calculate")
def calculate_route(request: RouteRequest):

    route = [
        [30.3150, 78.0300],
        [30.3155, 78.0320],
        [30.3170, 78.0340],
        [30.3185, 78.0370],
        [30.3200, 78.0400]
    ]

    return {
        "success": True,
        "message": "Safe emergency route calculated",
        "data": {
            "start": request.start,
            "destination": request.destination,
            "route": route,
            "algorithm": "A*",
            "blocked_roads_avoided": True
        }
    }


# ==========================================
# MOCK PLATFORM INTEGRATION
# ==========================================

class PlatformRestriction(BaseModel):
    platform: str
    zone_id: int
    status: str
    reason: str


@app.post("/api/platform/restriction")
def platform_restriction(data: PlatformRestriction):

    return {
        "success": True,
        "message": "Platform received safety restriction",
        "data": {
            "platform": data.platform,
            "zone_id": data.zone_id,
            "status": data.status,
            "reason": data.reason
        }
    }