import numpy as np
from sklearn.cluster import KMeans

def create_data_model(dustbins, num_vehicles=6):
    """Stores the data for the problem."""
    data = {}
    data['locations'] = [(float(d[0]), float(d[1])) for d in dustbins]
    data['num_vehicles'] = num_vehicles
    data['depot'] = 0  # Assuming the first point is the depot
    return data

def compute_euclidean_distance_matrix(locations):
    """Creates a distance matrix using Euclidean distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distances[from_counter][to_counter] = (
                    (from_node[0] - to_node[0])**2 +
                    (from_node[1] - to_node[1])**2
                )**0.5
    return distances

def divide_points_by_clustering(locations, num_vehicles):
    """Clusters the points for each vehicle using K-Means clustering."""
    # Exclude the depot from clustering
    points = np.array(locations[1:])  # Exclude depot (index 0)
    
    # Use K-Means clustering to create clusters of points
    kmeans = KMeans(n_clusters=num_vehicles, random_state=0).fit(points)
    
    # Initialize routes for each vehicle
    vehicle_routes = [[] for _ in range(num_vehicles)]
    
    # Assign each point to the route corresponding to its cluster
    for point_index, cluster_id in enumerate(kmeans.labels_):
        vehicle_routes[cluster_id].append(point_index + 1)  # +1 to adjust for depot index
    
    return vehicle_routes

def plan_optimized_route(dustbins, num_vehicles=6):
    """Plan routes by clustering points for each vehicle."""
    try:
        data = create_data_model(dustbins, num_vehicles)
        routes = divide_points_by_clustering(data['locations'], num_vehicles)

        # Add depot (0) at the start and end of each route
        for route in routes:
            route.insert(0, 0)  # Start at depot
            route.append(0)     # End at depot

        return routes
    except Exception as e:
        print("Error in plan_optimized_route:", str(e))
        raise



# import numpy as np
# from sklearn.cluster import KMeans

# def create_data_model(dustbins, bin_capacities, truck_capacity, num_vehicles=6):
#     """Stores the data for the problem with capacities."""
#     data = {
#         'locations': [(float(d[0]), float(d[1])) for d in dustbins],
#         'bin_capacities': bin_capacities,
#         'truck_capacity': truck_capacity,
#         'num_vehicles': num_vehicles,
#         'depot': 0  # Assuming the first point is the depot
#     }
#     return data

# def compute_euclidean_distance_matrix(locations):
#     """Creates a distance matrix using Euclidean distance between points."""
#     distances = {}
#     for from_counter, from_node in enumerate(locations):
#         distances[from_counter] = {}
#         for to_counter, to_node in enumerate(locations):
#             if from_counter == to_counter:
#                 distances[from_counter][to_counter] = 0
#             else:
#                 distances[from_counter][to_counter] = (
#                     (from_node[0] - to_node[0])**2 +
#                     (from_node[1] - to_node[1])**2
#                 )**0.5
#     return distances

# def divide_points_by_clustering(data):
#     """Clusters the points for each vehicle using K-Means clustering and respects truck capacity."""
#     points = np.array(data['locations'][1:])  # Exclude depot (index 0)
#     num_vehicles = data['num_vehicles']
#     truck_capacity = data['truck_capacity']
#     bin_capacities = data['bin_capacities']

#     # Use K-Means clustering
#     kmeans = KMeans(n_clusters=num_vehicles, random_state=0).fit(points)
    
#     # Initialize routes and capacities for each vehicle
#     vehicle_routes = [[] for _ in range(num_vehicles)]
#     vehicle_capacities = [0] * num_vehicles
    
#     # First, attempt to assign each point based on clustering, with capacity check
#     for point_index, cluster_id in enumerate(kmeans.labels_):
#         actual_index = point_index + 1  # Adjust for depot index
#         bin_capacity = bin_capacities[actual_index]

#         # Try to fit the bin into its cluster's assigned vehicle
#         if vehicle_capacities[cluster_id] + bin_capacity <= truck_capacity:
#             vehicle_routes[cluster_id].append(actual_index)
#             vehicle_capacities[cluster_id] += bin_capacity
#         else:
#             # If not possible, attempt to find another vehicle with capacity
#             assigned = False
#             for alt_cluster_id in range(num_vehicles):
#                 if vehicle_capacities[alt_cluster_id] + bin_capacity <= truck_capacity:
#                     vehicle_routes[alt_cluster_id].append(actual_index)
#                     vehicle_capacities[alt_cluster_id] += bin_capacity
#                     assigned = True
#                     break
#             if not assigned:
#                 # If no vehicle can take this bin, split it into its own cluster or redistribute
#                 print(f"Warning: Bin {actual_index} could not be assigned to any vehicle within capacity. Reassigning...")
#                 min_vehicle = np.argmin(vehicle_capacities)  # Assign to vehicle with most available capacity
#                 vehicle_routes[min_vehicle].append(actual_index)
#                 vehicle_capacities[min_vehicle] += bin_capacity

#     return vehicle_routes

# def plan_optimized_route(dustbins, bin_capacities, truck_capacity, num_vehicles=6):
#     """Plan routes by clustering points for each vehicle and respecting capacities."""
#     try:
#         data = create_data_model(dustbins, bin_capacities, truck_capacity, num_vehicles)
#         routes = divide_points_by_clustering(data)

#         # Add depot (0) at the start and end of each route
#         for route in routes:
#             route.insert(0, 0)  # Start at depot
#             route.append(0)     # End at depot

#         return routes
#     except Exception as e:
#         print("Error in plan_optimized_route:", str(e))
#         raise

# # Example usage:
# dustbins = [(0, 0), (1, 2), (2, 3), (3, 1), (4, 5), (5, 2)]
# bin_capacities = [0, 100, 150, 120, 130, 140]  # Capacity of each bin including depot
# truck_capacity = 250
# num_vehicles = 2
# print(plan_optimized_route(dustbins, bin_capacities, truck_capacity, num_vehicles))