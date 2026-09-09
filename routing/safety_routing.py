from geofence import get_zone
from emergency_route import find_emergency_route


def check_emergency_safety(
    vehicle_lat,
    vehicle_lon,
    incident_lat,
    incident_lon,
    red_radius,
    orange_radius
):
    """
    Check the emergency vehicle's zone
    and decide whether emergency routing is needed.
    """

    zone = get_zone(
        vehicle_lat,
        vehicle_lon,
        incident_lat,
        incident_lon,
        red_radius,
        orange_radius
    )

    print("\nEmergency Vehicle Zone:", zone)

    if zone == "RED":

        print("⚠️ Vehicle is inside RED Zone.")
        print("Finding safe emergency route...")

    elif zone == "ORANGE":

        print("⚠️ Vehicle is near the restricted area.")
        print("Proceed with caution.")

    else:

        print("✅ Vehicle is in GREEN Zone.")
        print("Normal movement allowed.")

    return zone


# ==================================================
# TESTING
# ==================================================

if __name__ == "__main__":

    # Incident location
    incident_lat = 30.3165
    incident_lon = 78.0322

    # Emergency vehicle location
    vehicle_lat = 30.3160
    vehicle_lon = 78.0320

    # Zone radius in metres
    red_radius = 500
    orange_radius = 1000

    check_emergency_safety(
        vehicle_lat,
        vehicle_lon,
        incident_lat,
        incident_lon,
        red_radius,
        orange_radius
    )