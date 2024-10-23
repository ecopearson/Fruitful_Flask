from flask import Blueprint, jsonify, request
from firebase_admin import credentials, auth, firestore
from app import app

@app.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    try:
        decoded_token = auth.verify_id_token(token)
        return jsonify({"message": "Token is valid!", "uid": decoded_token['uid']}), 200
    except Exception as e:
        return jsonify({"message": "Invalid token!", "error": str(e)}), 403
