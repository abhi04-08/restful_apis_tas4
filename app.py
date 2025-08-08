from flask import Flask, jsonify, request

app = Flask(__name__)

users = {}

# Home route
@app.route("/")
def home():
    return jsonify("User API's are running.")

# Get all users
@app.route("/users", methods = ["GET"])
def get_users():
    return jsonify(users)

# Get users by id
@app.route("/users/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id : user})
    return jsonify({"error": "User not found"})

# Post users
@app.route("/users", methods = ["POST"])
def post_user():
    data = request.get_json()
    user_id = data.get("id")
    name = data.get("name")

    if user_id in users:
        return jsonify({ "error" : "User already exists"})
    if not name:
        return jsonify({ "error" : "Name is required." })
    
    users[user_id] = {"name" : name}
    return jsonify({"message" : "User added", "user": users[user_id]})

# Update user
@app.route("/users/<int:user_id>", methods = ["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({ "error" : "User not found" })
    
    data = request.get_json()
    name = data.get("name")

    if name:
        users[user_id]["name"] = name
        return jsonify({ "message" : "User updated", "user": users[user_id]})
    return jsonify({ "error" : "Name is required" })

# Delete Users
@app.route("/users/<int:user_id>", methods = ["DELETE"])
def delete_user(user_id):
    if user_id in users:
        delete_user = users.pop(user_id)
        return jsonify({ "message" : "User deleted", "user": delete_user})
    return jsonify({ "error" : "User not found" })

if __name__ == "__main__":
    app.run(debug=True)