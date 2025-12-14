"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    member_list = jackson_family.get_all_members()
    return jsonify(member_list), 200

@app.route('/members/<int:member_id>', methods= ['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    return jsonify(member), 200
    
@app.route('/members/<int:member_id>', methods =['DELETE'])
def delete_single_member(member_id):
    deleted= jackson_family.delete_member(member_id)
    return jsonify({"done" : deleted}), 200
   

@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400 
    if "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    
    member= {
                
                "first_name": data["first_name"],
                "age": data["age"],
                "lucky_numbers": data["lucky_numbers"]
            }
    if "id" in data:
        member["id"] = data["id"]
    
    result = jackson_family.add_member(member)
    return jsonify(result), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
