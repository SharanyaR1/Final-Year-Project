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