# import numpy as np
# from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# def create_data_model(dustbins, num_vehicles=10, vehicle_capacity=100):
#     """Stores the data for the problem."""
#     data = {}
#     data['locations'] = [(float(d[0]), float(d[1])) for d in dustbins]
#     data['num_vehicles'] = num_vehicles
#     data['depot'] = 0  # Assuming the first point is the depot
#     data['demands'] = [0] + [d[2] for d in dustbins]  # First demand is 0 for the depot
#     data['vehicle_capacities'] = [vehicle_capacity] * num_vehicles
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

# def plan_optimized_route(dustbins, num_vehicles=6, vehicle_capacity=100):
#     """Plan routes using CVRP algorithm."""
#     data = create_data_model(dustbins, num_vehicles, vehicle_capacity)
#     distance_matrix = compute_euclidean_distance_matrix(data['locations'])

#     manager = pywrapcp.RoutingIndexManager(len(data['locations']), data['num_vehicles'], data['depot'])
#     routing = pywrapcp.RoutingModel(manager)

#     def distance_callback(from_index, to_index):
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         return int(distance_matrix[from_node][to_node])

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     def demand_callback(from_index):
#         from_node = manager.IndexToNode(from_index)
#         return data['demands'][from_node]

#     demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
#     routing.AddDimensionWithVehicleCapacity(
#         demand_callback_index,
#         0,  # null capacity slack
#         data['vehicle_capacities'],  # vehicle maximum capacities
#         True,  # start cumul to zero
#         'Capacity'
#     )

#     # Add penalty for not visiting certain locations
#     penalty = 1000
#     for node in range(1, len(data['locations'])):
#         routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = (
#         routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
#     search_parameters.local_search_metaheuristic = (
#         routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC)
#     search_parameters.time_limit.seconds = 30

#     solution = routing.SolveWithParameters(search_parameters)

#     if not solution:
#         print("No solution found!")
#         return []

#     routes = []
#     for vehicle_id in range(data['num_vehicles']):
#         index = routing.Start(vehicle_id)
#         route = []
#         while not routing.IsEnd(index):
#             route.append(manager.IndexToNode(index))
#             index = solution.Value(routing.NextVar(index))
#         route.append(manager.IndexToNode(index))
#         routes.append(route)

#     return routes

# aux_functions.py

import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def create_data_model(dustbins, num_vehicles=10, vehicle_capacity=100):
    """Stores the data for the problem."""
    data = {}
    data['locations'] = [(float(d[0]), float(d[1])) for d in dustbins]
    data['num_vehicles'] = num_vehicles
    data['depot'] = 0  # Assuming the first point is the depot
    data['demands'] = [0] + [d[2] for d in dustbins]  # First demand is 0 for the depot
    data['vehicle_capacities'] = [vehicle_capacity] * num_vehicles
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

def plan_optimized_route(dustbins, num_vehicles=6, vehicle_capacity=100):
    """Plan routes using CVRP algorithm."""
    data = create_data_model(dustbins, num_vehicles, vehicle_capacity)
    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    manager = pywrapcp.RoutingIndexManager(len(data['locations']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity'
    )

    # Add penalty for not visiting certain locations
    penalty = 1000
    for node in range(1, len(data['locations'])):
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC)
    search_parameters.time_limit.seconds = 30

    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        print("No solution found!")
        return []

    routes = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append(route)

    return routes
