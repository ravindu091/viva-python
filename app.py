import math

def euclidean_distance(loc1, loc2):
    """
    Calculates the Euclidean distance between two points (x, y).
    """
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def plan_waste_collection_route(full_bins, truck_capacity, depot_location):
    """
    Plans a waste collection route using a greedy approach.
    It prioritizes visiting the nearest unvisited bin that fits within capacity.
    Args:
        full_bins (list): A list of dictionaries, each representing a full bin.
            Example: [{'id': 'B1', 'amount': 30, 'location': (x, y)}]
        truck_capacity (int): The maximum waste the truck can carry.
        depot_location (tuple): The (x, y) coordinates of the depot.
    Returns:
        tuple: A tuple containing:
            - route (list): A list of bin IDs representing the collection order.
            - total_distance (float): The total distance traveled.
            - uncollected_bins (list): Bins that couldn't be collected due to capacity.
    """
    current_location = depot_location
    current_load = 0
    total_distance = 0.0
    route = []
    uncollected_bins = []
    visited_bins = set()
    # Create a mutable list of bins, sorted by ID for consistent processing
    bins_to_visit = sorted(full_bins, key=lambda b: b['id'])

    # Continue as long as there are bins left to consider
    while len(visited_bins) < len(full_bins):
        # Find the nearest unvisited bin that the truck can collect
        nearest_bin = None
        min_distance = float('inf')
        for bin_data in bins_to_visit:
            bin_id = bin_data['id']
            bin_location = bin_data['location']
            bin_amount = bin_data['amount']
            if bin_id not in visited_bins:
                # Check if adding this bin would exceed capacity
                if current_load + bin_amount <= truck_capacity:
                    distance = euclidean_distance(current_location, bin_location)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_bin = bin_data
                else:
                    # If this bin cannot be added due to capacity, we note it for potential future trips
                    # For this simple greedy approach, if it doesn't fit, it's considered uncollected in this round.
                    pass
        if nearest_bin:
            # Add the nearest bin to the route
            route.append(nearest_bin['id'])
            total_distance += min_distance
            current_load += nearest_bin['amount']
            current_location = nearest_bin['location']
            visited_bins.add(nearest_bin['id'])
        else:
            # If no suitable bin can be found (e.g., all remaining bins exceed capacity)
            # break out of the loop.
            # Mark remaining bins as uncollected for this trip.
            for bin_data in bins_to_visit:
                if bin_data['id'] not in visited_bins:
                    uncollected_bins.append(bin_data['id'])
            break # Exit the loop if no more bins can be added to the current trip
    # Return to the depot from the last visited bin
    if route: # If any bins were collected
        total_distance += euclidean_distance(current_location, depot_location)
        route.append('Depot') # Indicate return to depot for clarity

    return route, total_distance, uncollected_bins

# --- Example Usage ---
if __name__ == "__main__":
    # Define your full bins data
    sample_bins = [
        {'id': 'B1', 'amount': 20, 'location': (10, 5)},
        {'id': 'B2', 'amount': 40, 'location': (5, 15)},
        {'id': 'B3', 'amount': 30, 'location': (20, 10)},
        {'id': 'B4', 'amount': 10, 'location': (15, 2)},
        {'id': 'B5', 'amount': 50, 'location': (8, 20)} # A larger bin
    ]
    truck_cap = 100
    depot = (0, 0)
    print("--- Planning Route 1 ---")
    print(f"Depot Location: {depot}")
    print(f"Truck Capacity: {truck_cap}")
    print("Full Bins:")
    for b in sample_bins:
        print(f" - ID: {b['id']}, Amount: {b['amount']}, Location: {b['location']}")
    route, distance, uncollected = plan_waste_collection_route(sample_bins, truck_cap, depot)
    print("\n--- Route Plan ---")
    if route:
        print(f"Optimized Route: Depot -> {' -> '.join(route)}")
        print(f"Total Travel Distance: {distance:.2f} units")
    else:
        print("No bins could be collected in this trip.")
    if uncollected:
        print(f"Uncollected Bins (due to capacity/no fit in current trip): {', '.join(uncollected)}")
    else:
        print("All specified bins collected in this trip.")

    print("\n--- Planning Route 2 (with lower capacity to show uncollected bins) ---")
    truck_cap_lower = 70 # Lower capacity
    print(f"Depot Location: {depot}")
    print(f"Truck Capacity: {truck_cap_lower}")
    print("Full Bins:")
    for b in sample_bins:
        print(f" - ID: {b['id']}, Amount: {b['amount']}, Location: {b['location']}")
    route2, distance2, uncollected2 = plan_waste_collection_route(sample_bins, truck_cap_lower, depot)
    print("\n--- Route Plan 2 ---")
    if route2:
        print(f"Optimized Route: Depot -> {' -> '.join(route2)}")
        print(f"Total Travel Distance: {distance2:.2f} units")
    else:
        print("No bins could be collected in this trip.")
    if uncollected2:
        print(f"Uncollected Bins (due to capacity/no fit in current trip): {', '.join(uncollected2)}")
    else:
        print("All specified bins collected in this trip.")