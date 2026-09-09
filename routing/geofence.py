import math


# ==========================================
# CALCULATE DISTANCE
# ==========================================

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates
    using the Haversine formula.

    Returns distance in meters.
    """

    R = 6371000  # Earth radius in meters

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


# ==========================================
# FIND SAFETY ZONE
# ==========================================

def get_zone(
    user_lat,
    user_lon,
    zone_lat,
    zone_lon,
    red_radius,
    orange_radius
):
    """
    Determine whether a location is inside
    RED, ORANGE or GREEN zone.
    """

    distance = calculate_distance(
        user_lat,
        user_lon,
        zone_lat,
        zone_lon
    )

    if distance <= red_radius:
        return "RED"

    elif distance <= orange_radius:
        return "ORANGE"

    else:
        return "GREEN"


# ==========================================
# TESTING ONLY
# ==========================================

if __name__ == "__main__":

    print("CivicShield Geofencing Test")

    incident_lat = float(
        input("Enter incident latitude: ")
    )

    incident_lon = float(
        input("Enter incident longitude: ")
    )

    red_radius = float(
        input("Enter RED radius in meters: ")
    )

    orange_radius = float(
        input("Enter ORANGE radius in meters: ")
    )

    worker_lat = float(
        input("Enter worker latitude: ")
    )

    worker_lon = float(
        input("Enter worker longitude: ")
    )

    zone = get_zone(
        worker_lat,
        worker_lon,
        incident_lat,
        incident_lon,
        red_radius,
        orange_radius
    )

    print("\nWorker Zone:", zone)

    if zone == "RED":

        print("WARNING: Worker is inside RED Zone.")

    elif zone == "ORANGE":

        print("CAUTION: Worker is approaching RED Zone.")

    else:

        print("NORMAL: Worker is in GREEN Zone.")