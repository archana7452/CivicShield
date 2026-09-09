from astar import astar


def find_emergency_route(
    graph,
    start,
    destination,
    blocked_roads
):
    """
    Calculate a safe route for an emergency vehicle.
    """

    print("\nCalculating emergency route...")

    route = astar(
        graph,
        start,
        destination,
        blocked_roads
    )

    if route:

        print("Safe emergency route found:")

        print(route)

        return route

    else:

        print("No safe route available.")

        return []


# ==================================================
# TESTING
# ==================================================

if __name__ == "__main__":

    # ------------------------------------
    # CIVICSHIELD ROAD NETWORK
    # ------------------------------------

    graph = {

        (0, 0): [
            ((1, 0), 1),
            ((0, 1), 1)
        ],

        (1, 0): [
            ((0, 0), 1),
            ((2, 0), 1),
            ((1, 1), 1)
        ],

        (0, 1): [
            ((0, 0), 1),
            ((1, 1), 1)
        ],

        (1, 1): [
            ((1, 0), 1),
            ((0, 1), 1),
            ((2, 1), 1)
        ],

        (2, 0): [
            ((1, 0), 1),
            ((2, 1), 1)
        ],

        (2, 1): [
            ((2, 0), 1),
            ((1, 1), 1),
            ((2, 2), 1)
        ],

        (2, 2): [
            ((2, 1), 1)
        ]
    }

    # ------------------------------------
    # AMBULANCE
    # ------------------------------------

    ambulance_location = (0, 0)

    hospital_location = (2, 2)

    # ------------------------------------
    # BLOCKED ROAD
    # ------------------------------------

    blocked_roads = {
        ((1, 0), (2, 0))
    }

    # ------------------------------------
    # CALCULATE ROUTE
    # ------------------------------------

    find_emergency_route(
        graph,
        ambulance_location,
        hospital_location,
        blocked_roads
    )