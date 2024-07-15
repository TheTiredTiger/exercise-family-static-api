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

john_jackson = {
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
}

jane_jackson = {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

jimmy_jackson = {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def member_id(member_id):
    found = jackson_family.get_member(member_id)
    if not found:
        return jsonify({"Warning": "Member not found"})
    
    return jsonify(found), 200

@app.route('/member/', methods=['POST'])
def add_member():
    new_member = request.json
    print(new_member)

    jackson_family.add_member(new_member)
    return jsonify({'Done': 'Member created'}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if not deleted:
        return jsonify({"Warning": "Family member not found"}), 400
    return jsonify({"Done": "Family member kicked out of all events"}), 200

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_family_member(member_id):
    updated_member = request.json
    updated = jackson_family.update_member(member_id, updated_member)
    if not updated:
        return jsonify({"Warning": "Family member not found"}), 400
    
    return jsonify({"Done": "Member updated"})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)