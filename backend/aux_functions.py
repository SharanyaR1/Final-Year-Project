import numpy as np

def create_data_model(dustbins, num_vehicles=6):
    """Stores the data for the problem."""
    data = {}
    data['locations'] = [(float(d[0]), float(d[1])) for d in dustbins]
    data['num_vehicles'] = num_vehicles
    data['depot'] = 0
    return data

def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distances[from_counter][to_counter] = (
                    (from_node[0] - to_node[0])**2 +
                    (from_node[1] - to_node[1])**2)**0.5
    return distances

def divide_points_equally(locations, num_vehicles):
    """Divide the points into equal groups for each vehicle."""
    num_points = len(locations) - 1  # Exclude depot
    points_per_vehicle = num_points // num_vehicles
    remainder = num_points % num_vehicles

    # Create empty routes for each vehicle
    vehicle_routes = [[] for _ in range(num_vehicles)]

    # Distribute points evenly
    point_index = 1  # Start from 1 (skip depot which is 0)
    for i in range(num_vehicles):
        num_points_to_assign = points_per_vehicle + (1 if i < remainder else 0)
        vehicle_routes[i] = list(range(point_index, point_index + num_points_to_assign))
        point_index += num_points_to_assign

    return vehicle_routes

def plan_optimized_route(dustbins, num_vehicles=6):
    """Solve the VRP problem by forcing equal point distribution among vehicles."""
    try:
        data = create_data_model(dustbins, num_vehicles)
        routes = divide_points_equally(data['locations'], num_vehicles)

        # Add depot (0) at start and end of each route
        for route in routes:
            route.insert(0, 0)  # Start at depot
            route.append(0)     # End at depot

        return routes
    except Exception as e:
        print("Error in plan_optimized_route:", str(e))
        raise