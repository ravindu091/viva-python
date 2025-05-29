import math

# Sample data
bins = [
    {"id": "B1", "amount": 30, "location": (2, 3)},
    {"id": "B2", "amount": 20, "location": (5, 4)},
    {"id": "B3", "amount": 40, "location": (1, 7)},
    {"id": "B4", "amount": 10, "location": (6, 1)},
    {"id": "B5", "amount": 25, "location": (3, 6)},
]

truck_capacity = 40
depot_location = (0, 0)

# Distance function
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Find largest-amount, nearest bin that fits
def find_best_bin(current_location, remaining_capacity, bins, visited):
    # Filter unvisited bins that fit in the truck
    candidates = [
        b for b in bins
        if b["id"] not in visited and b["amount"] <= remaining_capacity
    ]
    if not candidates:
        return None

    # Sort by amount (desc), then distance (asc)
    candidates.sort(key=lambda b: (-b["amount"], euclidean_distance(current_location, b["location"])))
    return candidates[0]

# Plan all trips
def plan_routes(bins, truck_capacity, depot_location):
    visited = set()
    all_routes = []
    total_distance = 0

    while len(visited) < len(bins):
        route = ["Depot"]
        distance = 0
        current_location = depot_location
        remaining_capacity = truck_capacity

        while True:
            next_bin = find_best_bin(current_location, remaining_capacity, bins, visited)
            if not next_bin:
                break
            route.append(next_bin["id"])
            distance += euclidean_distance(current_location, next_bin["location"])
            remaining_capacity -= next_bin["amount"]
            current_location = next_bin["location"]
            visited.add(next_bin["id"])

        # Return to depot
        distance += euclidean_distance(current_location, depot_location)
        route.append("Depot")
        all_routes.append({"route": route, "distance": round(distance, 2)})
        total_distance += distance

    return all_routes, round(total_distance, 2)

# Run
routes, total = plan_routes(bins, truck_capacity, depot_location)

# Output
for i, trip in enumerate(routes, 1):
    print(f"Trip {i}: Route = {trip['route']}, Distance = {trip['distance']}")

print(f"Total Distance Covered: {total}")
