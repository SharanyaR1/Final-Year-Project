from flask import request, jsonify,render_template,Flask
from config import app, db
from models import Dustbin
import aux_functions
import thingspeak

#change to your relative system path 
app = Flask(__name__, static_folder="C:\\Users\\shrchand\\Downloads\\Routecraft-A-garbage-truck-route-optimization-system.-main\\Routecraft-A-garbage-truck-route-optimization-system.-main\\frontend", template_folder='C:\\Users\\shrchand\\Downloads\\Routecraft-A-garbage-truck-route-optimization-system.-main\\Routecraft-A-garbage-truck-route-optimization-system.-main\\frontend')

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
def plan_optimized_route_handler():
    dustbins_data = request.json.get("dustbins")
    dustbins = [(d.get('latitude'), d.get('longitude'), d.get('capacity')) for d in dustbins_data]
    optimized_route = aux_functions.plan_optimized_route(dustbins)
    return jsonify({"optimized_route": optimized_route}), 200

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

def create_dustbin_from_thingspeak():
    latitude,longitude,capacity = thingspeak.dustbins()
    new_dustbin = Dustbin(latitude=latitude, longitude=longitude, capacity=capacity)
    try:
        db.session.add(new_dustbin)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Dustbin created!"}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_dustbin_from_thingspeak()
    
    app.run(debug=True)
