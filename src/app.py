"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})

jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})

jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member', methods=['POST'])
def add_member():
    member = request.get_json()
    if not member:
        return jsonify({"error": "Request body is empty"}), 400
    if "first_name" not in member:
        return jsonify({"error": "First name is required"}), 400
    if "age" not in member:
        return jsonify({"error": "Age is required"}), 400
    if "lucky_numbers" not in member:
        return jsonify({"error": "Lucky numbers are required"}), 400
    
    new_member = jackson_family.add_member({
        "first_name": member["first_name"],
        "id": member.get("id", None),
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    })
    return jsonify(new_member), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify({
            "first_name": member["first_name"],
            "id": member["id"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }), 200
    else:
        return jsonify({"error": "Member not found"}), 404


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    deleted_member = jackson_family.delete_member(id)
    if deleted_member:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 404
    
    # Este solo se ejecuta si `$ python src/app.py` es ejecutado
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)