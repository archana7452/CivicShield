import heapq


def heuristic(a, b):
    """
    Estimate the distance between two points.
    """

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(graph, start, goal, blocked_roads):
    """
    Find the shortest available route using A*.
    Blocked roads are avoided.
    """

    open_list = []

    heapq.heappush(open_list, (0, start))

    came_from = {}

    cost_so_far = {
        start: 0
    }

    while open_list:

        _, current = heapq.heappop(open_list)

        # Destination reached
        if current == goal:
            break

        for neighbour, cost in graph[current]:

            # Check whether the road is blocked
            road = (current, neighbour)

            reverse_road = (neighbour, current)

            if road in blocked_roads or reverse_road in blocked_roads:
                continue

            new_cost = cost_so_far[current] + cost

            if (
                neighbour not in cost_so_far
                or new_cost < cost_so_far[neighbour]
            ):

                cost_so_far[neighbour] = new_cost

                priority = (
                    new_cost
                    + heuristic(neighbour, goal)
                )

                heapq.heappush(
                    open_list,
                    (priority, neighbour)
                )

                came_from[neighbour] = current

    # No route available
    if goal != start and goal not in came_from:
        return []

    # Build route backwards
    route = []

    current = goal

    while current != start:

        route.append(current)

        current = came_from[current]

    route.append(start)

    # Reverse route
    route.reverse()

    return route


# ==================================================
# TESTING ONLY
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
    # EMERGENCY VEHICLE
    # ------------------------------------

    start = (0, 0)

    goal = (2, 2)

    # ------------------------------------
    # BLOCKED ROAD
    # ------------------------------------

    blocked_roads = {
        ((1, 0), (2, 0))
    }

    # ------------------------------------
    # FIND ROUTE
    # ------------------------------------

    route = astar(
        graph,
        start,
        goal,
        blocked_roads
    )

    print("Emergency Vehicle Route:")

    if route:
        print(route)
    else:
        print("No safe route available.")