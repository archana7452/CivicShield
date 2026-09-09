from math import radians, sin, cos, sqrt, atan2
def calculate_risk(severity):
    severity = severity.upper()

    if severity == "HIGH":
        return {
            "risk_level": "HIGH",
            "zone_radius": 500,
            "zone_type": "RESTRICTED",
            "recommended_action": "RESTRICT",
            "affected_services": [
            "FOOD_DELIVERY",
            "RIDE_HAILING",
            "PUBLIC_TRANSPORT",
            "LOGISTICS"
            ]
        }

    elif severity == "MEDIUM":
        return {
            "risk_level": "MEDIUM",
            "zone_radius": 300,
            "zone_type": "CAUTION",
            "recommended_action": "MONITOR"
        }

    else:
        return {
            "risk_level": "LOW",
            "zone_radius": 100,
            "zone_type": "MONITORING",
            "recommended_action": "MONITOR"
        }

    


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates in meters.
    Uses the Haversine formula.
    """

    R = 6371000  # Earth radius in meters

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def find_nearest_units(
    incident_latitude,
    incident_longitude,
    emergency_units
):
    available_units = []

    for unit in emergency_units:

        if unit.status != "AVAILABLE":
            continue

        distance = calculate_distance(
            incident_latitude,
            incident_longitude,
            unit.latitude,
            unit.longitude
        )

        available_units.append({
            "unit_id": unit.id,
            "unit_name": unit.unit_name,
            "type": unit.type,
            "distance_meters": round(distance, 2)
        })

    available_units.sort(
        key=lambda unit: unit["distance_meters"]
    )

    return available_units

def recommend_deployment(nearest_units, risk_level):
    recommendations = []

    if risk_level == "HIGH":
        required_types = ["POLICE", "AMBULANCE", "FIRE"]

        for unit_type in required_types:
            for unit in nearest_units:
                if unit["type"] == unit_type:
                    recommendations.append({
                        "unit_id": unit["unit_id"],
                        "unit_name": unit["unit_name"],
                        "type": unit["type"],
                        "distance_meters": unit["distance_meters"],
                        "recommendation": "DEPLOY"
                    })
                    break

    elif risk_level == "MEDIUM":
        for unit in nearest_units[:2]:
            recommendations.append({
                "unit_id": unit["unit_id"],
                "unit_name": unit["unit_name"],
                "type": unit["type"],
                "distance_meters": unit["distance_meters"],
                "recommendation": "STANDBY"
            })

    else:
        for unit in nearest_units[:1]:
            recommendations.append({
                "unit_id": unit["unit_id"],
                "unit_name": unit["unit_name"],
                "type": unit["type"],
                "distance_meters": unit["distance_meters"],
                "recommendation": "MONITOR"
            })

    return recommendations
def check_worker_in_zone(
    worker_latitude,
    worker_longitude,
    zone_latitude,
    zone_longitude,
    zone_radius
):
    distance = calculate_distance(
        worker_latitude,
        worker_longitude,
        zone_latitude,
        zone_longitude
    )

    if distance <= zone_radius:
        return {
            "inside_zone": True,
            "distance_meters": round(distance, 2),
            "status": "WORKER INSIDE RESTRICTED ZONE"
        }

    return {
        "inside_zone": False,
        "distance_meters": round(distance, 2),
        "status": "WORKER SAFE"
    }

