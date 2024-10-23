from flask import Blueprint, jsonify, request
from firebase_admin import firestore

activities_bp = Blueprint('activities', __name__)
db = firestore.client()

@activities_bp.route('/activities', methods=['GET', 'POST'])
def handle_activities():
    if request.method == 'POST':
        activity_data = request.json
        db.collection('activities').add(activity_data)
        return jsonify({"message": "Activity posted!"}), 201

    elif request.method == 'GET':
        activities = db.collection('activities').stream()
        activity_list = [{"id": activity.id, **activity.to_dict()} for activity in activities]
        return jsonify({"activities": activity_list}), 200
