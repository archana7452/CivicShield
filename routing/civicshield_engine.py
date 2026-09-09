from geofence import get_zone
from astar import astar


def recommend_zone(crowd_size, severity, affected_roads, duration_minutes):
    if severity == "CRITICAL" or crowd_size >= 5000 or affected_roads >= 5:
        return 750, 1500

    elif severity == "HIGH" or crowd_size >= 2000 or affected_roads >= 3:
        return 500, 1000

    elif severity == "MEDIUM" or crowd_size >= 500:
        return 300, 700

    else:
        return 150, 400


def check_worker(worker_lat, worker_lon,
                 incident_lat, incident_lon,
                 red_radius, orange_radius):

    zone = get_zone(
        worker_lat,
        worker_lon,
        incident_lat,
        incident_lon,
        red_radius,
        orange_radius
    )

    if zone == "RED":
        action = "STOP_NEW_TASKS"
    elif zone == "ORANGE":
        action = "WARNING"
    else:
        action = "NORMAL"

    return zone, action


def find_safe_route(graph, start, destination, blocked_roads):
    return astar(
        graph,
        start,
        destination,
        blocked_roads
    )


if __name__ == "__main__":

    print("================================")
    print("      CIVICSHIELD AI ENGINE")
    print("================================")

    crowd_size = int(input("Crowd size: "))
    severity = input("Severity (LOW/MEDIUM/HIGH/CRITICAL): ").upper()
    affected_roads = int(input("Affected roads: "))
    duration = int(input("Duration (minutes): "))

    red_radius, orange_radius = recommend_zone(
        crowd_size,
        severity,
        affected_roads,
        duration
    )

    print("\nAI Recommendation")
    print("------------------")
    print("RED Zone:", red_radius, "meters")
    print("ORANGE Zone:", orange_radius, "meters")

    approval = input("\nOfficer approves? (yes/no): ").lower()

    if approval != "yes":
        print("\nZone recommendation rejected by officer.")
        exit()

    print("\n✅ Safety zone activated.")

    incident_lat = 30.3165
    incident_lon = 78.0322

    worker_lat = 30.3160
    worker_lon = 78.0320

    zone, action = check_worker(
        worker_lat,
        worker_lon,
        incident_lat,
        incident_lon,
        red_radius,
        orange_radius
    )

    print("\nWorker Safety")
    print("-------------")
    print("Worker Zone:", zone)
    print("Action:", action)

    graph = {
        (0, 0): [((1, 0), 1), ((0, 1), 1)],
        (1, 0): [((0, 0), 1), ((2, 0), 1), ((1, 1), 1)],
        (0, 1): [((0, 0), 1), ((1, 1), 1)],
        (1, 1): [((1, 0), 1), ((0, 1), 1), ((2, 1), 1)],
        (2, 0): [((1, 0), 1), ((2, 1), 1)],
        (2, 1): [((2, 0), 1), ((1, 1), 1), ((2, 2), 1)],
        (2, 2): [((2, 1), 1)]
    }

    blocked_roads = {
        ((1, 0), (2, 0))
    }

    emergency_route = find_safe_route(
        graph,
        (0, 0),
        (2, 2),
        blocked_roads
    )

    print("\nEmergency Safe Route")
    print("--------------------")
    print(emergency_route)