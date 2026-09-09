from geofence import get_zone


def check_worker_safety(
    worker_lat,
    worker_lon,
    incident_lat,
    incident_lon,
    red_radius,
    orange_radius
):
    """
    Check whether a worker is approaching
    or inside a restricted safety zone.
    """

    zone = get_zone(
        worker_lat,
        worker_lon,
        incident_lat,
        incident_lon,
        red_radius,
        orange_radius
    )

    print("\nWorker Safety Status:")

    if zone == "RED":

        print("🔴 RED ZONE")
        print("⚠️ Worker is inside a restricted area.")
        print("❌ New tasks should not be assigned here.")

    elif zone == "ORANGE":

        print("🟠 ORANGE ZONE")
        print("⚠️ Worker is approaching the restricted area.")
        print("Please proceed carefully.")

    else:

        print("🟢 GREEN ZONE")
        print("✅ Normal work can continue.")

    return zone


# ==================================================
# TESTING
# ==================================================

if __name__ == "__main__":

    # Incident location
    incident_lat = 30.3165
    incident_lon = 78.0322

    # Worker location
    worker_lat = 30.3160
    worker_lon = 78.0320

    # Zone radius in metres
    red_radius = 500
    orange_radius = 1000

    check_worker_safety(
        worker_lat,
        worker_lon,
        incident_lat,
        incident_lon,
        red_radius,
        orange_radius
    )