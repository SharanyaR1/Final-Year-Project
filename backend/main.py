from flask import request, jsonify,render_template,Flask, send_from_directory
from config import app, db
from models import Dustbin
import aux_functions
import math
import random
#change to your relative system path 
app = Flask(__name__, template_folder='../frontend', static_folder='../static')

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dustbins.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional but recommended

# Initialize your SQLAlchemy instance with the app
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pathplanning',methods=["GET"])
def pathplanning():
    return render_template('pathplanning.html')

@app.route('/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory('../assets', filename)

# New route to return adjacency matrix data
@app.route('/get_adjacency_matrix', methods=["GET"])
def get_adjacency_matrix():
    # Example adjacency matrix (you can replace this with your actual data)
    adjacency_matrix = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    
    return jsonify(adjacency_matrix)


@app.route("/plan_optimized_route", methods=["POST"])
@app.route("/plan_optimized_route", methods=["POST"])
def plan_optimized_route_handler():
    try:
        dustbins_data = request.json.get("dustbins")
        num_vehicles = request.json.get("num_vehicles", 3)  # Default to 3 vehicles if not specified

        if not dustbins_data:
            return jsonify({"error": "No dustbins data provided"}), 400

        # Convert dustbins_data to a list of tuples
        dustbins = [(float(d['latitude']), float(d['longitude']), d['capacity']) for d in dustbins_data]

        print("Dustbins data received:", dustbins)
        print("Number of vehicles:", num_vehicles)

        optimized_routes = aux_functions.plan_optimized_route(dustbins, num_vehicles)
        print("Optimized routes:", optimized_routes)

        return jsonify({"optimized_routes": optimized_routes}), 200
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": f"Failed to plan optimized route: {str(e)}"}), 500
    
# @app.route("/add_random_dustbins", methods=["POST"])
# def add_random_dustbins():
#     num_dustbins = request.json.get("numDustbins")
#     if not num_dustbins:
#         return jsonify({"message": "Number of dustbins is required"}), 400

#     # Define the bounding box for Banashankari area of Bangalore
#     center_lat, center_lon = 12.908214, 77.564112
#     range_km = 2

#     # Calculate the bounding box
#     lat_range = range_km / 111  # 1 degree of latitude is approximately 111 km
#     lon_range = range_km / (111 * math.cos(math.radians(center_lat)))  # Adjust for longitude

#     min_lat, max_lat = center_lat - lat_range, center_lat + lat_range
#     min_lon, max_lon = center_lon - lon_range, center_lon + lon_range
#     dustbins = []

#     for _ in range(int(num_dustbins)):
#         latitude = random.uniform(min_lat, max_lat)
#         longitude = random.uniform(min_lon, max_lon)
#         capacity = random.randint(1, 100) 
#         dustbin = Dustbin(latitude=latitude, longitude=longitude, capacity=capacity)
#         dustbins.append(dustbin)
#         db.session.add(dustbin)  # Add the dustbin to the session
#     db.session.commit()  # Commit the session to save all dustbins
#     return jsonify({"message": f"{num_dustbins} random dustbins added"}), 201





@app.route("/add_random_dustbins", methods=["POST"])
def add_random_dustbins():
    num_dustbins = request.json.get("numDustbins")
    if not num_dustbins:
        return jsonify({"message": "Number of dustbins is required"}), 400

    # Define the bounding box for Banashankari area of Bangalore
    center_lat, center_lon = 12.908214, 77.564112
    range_km = 0.5

    # Calculate the bounding box
    lat_range = range_km / 111  # 1 degree of latitude is approximately 111 km
    lon_range = range_km / (111 * math.cos(math.radians(center_lat)))  # Adjust for longitude

    min_lat, max_lat = center_lat - lat_range, center_lat + lat_range
    min_lon, max_lon = center_lon - lon_range, center_lon + lon_range
    dustbins = []

    # Check if the fixed dustbin already exists
    fixed_lat = 12.9092
    fixed_lon = 77.5666
    fixed_capacity = 10
    fixed_dustbin = Dustbin.query.filter_by(latitude=fixed_lat, longitude=fixed_lon).first()
    if not fixed_dustbin:
        fixed_dustbin = Dustbin(latitude=fixed_lat, longitude=fixed_lon, capacity=fixed_capacity)
        db.session.add(fixed_dustbin)
        db.session.commit()
    dustbins.append(fixed_dustbin)

    # Generate the remaining random dustbins
    for _ in range(int(num_dustbins)):
        latitude = random.uniform(min_lat, max_lat)
        longitude = random.uniform(min_lon, max_lon)
        capacity = random.randint(1, 10) 
        dustbin = Dustbin(latitude=latitude, longitude=longitude, capacity=capacity)
        db.session.add(dustbin)
        dustbins.append(dustbin)
    db.session.commit()

    # Convert dustbins to a serializable format
    dustbins_data = [{"id": dustbin.id, "latitude": dustbin.latitude, "longitude": dustbin.longitude, "capacity": dustbin.capacity} for dustbin in dustbins]

    return jsonify({"message": f"{num_dustbins} random dustbins added", "dustbins": dustbins_data}), 201



@app.route("/dustbins", methods=["GET"])
def get_dustbins():
    dustbins = Dustbin.query.all()
    json_dustbins = list(map(lambda x: x.to_json(), dustbins))
    return jsonify({"dustbins": json_dustbins})

@app.route("/create_dustbin", methods=["POST"])
def create_dustbin():
    latitude = request.json.get("latitude")
    longitude = request.json.get("longitude")
    capacity = request.json.get("capacity")

    if not latitude or not longitude or not capacity:
        return (
            jsonify({"message": "You must include the coordinates and capacity"}),
            400,
        )

    new_dustbin = Dustbin(latitude=latitude, longitude=longitude, capacity=capacity)
    try:
        db.session.add(new_dustbin)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Dustbin created!"}), 201


@app.route("/update_dustbin/<int:user_id>", methods=["PATCH"])
def update_dustbin(user_id):
    dustbin = Dustbin.query.get(user_id)

    if not dustbin:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    dustbin.latitude = data.get("latitude", dustbin.latitude)
    dustbin.longitude = data.get("longitude", dustbin.longitude)
    dustbin.capacity = data.get("capacity", dustbin.capacity)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200


@app.route("/delete_dustbin/<int:user_id>", methods=["DELETE"])
def delete_dustbin(user_id):
    dustbin = Dustbin.query.get(user_id)

    if not dustbin:
        return jsonify({"message": "Dustbin not found"}), 404

    db.session.delete(dustbin)
    db.session.commit()
    return jsonify({"message": "Dustbin deleted!"}), 200

@app.route("/clear_all_dustbins", methods=["DELETE"])
def clear_all_dustbins():
    try:
        num_deleted = db.session.query(Dustbin).delete()
        db.session.commit()
        return jsonify({"message": f"All dustbins cleared! Total deleted: {num_deleted}"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to clear dustbins: {str(e)}"}), 500



# def create_dustbin_from_thingspeak():
#     latitude,longitude,capacity = thingspeak.dustbins()
#     new_dustbin = Dustbin(latitude=latitude, longitude=longitude, capacity=capacity)
#     try:
#         db.session.add(new_dustbin)
#         db.session.commit()
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400

#     return jsonify({"message": "Dustbin created!"}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # create_dustbin_from_thingspeak()
    
    app.run(debug=True)
