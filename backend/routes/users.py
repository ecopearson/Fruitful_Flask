from flask import Blueprint, jsonify, request
from firebase_admin import firestore

users_bp = Blueprint('users', __name__)
db = firestore.client()

@users_bp.route('/users', methods=['GET', 'POST'])
def handle_activities():
    if request.method == 'POST':
        activity_data = request.json
        db.collection('users').add(activity_data)
        return jsonify({"users": "user posted!"}), 201

    elif request.method == 'GET':
        activities = db.collection('users').stream()
        activity_list = [{"id": activity.id, **activity.to_dict()} for activity in activities]
        return jsonify({"users": activity_list}), 200
