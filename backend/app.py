from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase_credentials.json')  # Update the path to your Firebase credentials
firebase_admin.initialize_app(cred)


from routes.activities import activities_bp
from routes.users import users_bp

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for the app
CORS(app)

# Initialize Firebase Admin SDK
#cred = credentials.Certificate('../fruitful-ultimateplowers-firebase-adminsdk-6db5u-5e706ee779.json')  # Update the path to your Firebase credentials
#firebase_admin.initialize_app(cred)



# Initialize Firestore
db = firestore.client()

# Register the activities blueprint
app.register_blueprint(activities_bp)
app.register_blueprint(users_bp)


# Optionally, you can set configuration options for Flask, such as:
app.config['DEBUG'] = True  # Enable debug mode
app.config['JSON_SORT_KEYS'] = False  # To keep the order of keys in JSON responses

# Health check endpoint (optional, useful for testing)
@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "OK"}, 200


@app.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return jsonify({"message": "Token is valid", "uid": uid}), 200
    except Exception as e:
        return jsonify({"message": "Invalid token", "error": str(e)}), 403



def add_placeholder_activity():
    # Check if the placeholder already exists
    placeholder_doc_ref = db.collection('activities').document('placeholder_activity')
    
    if placeholder_doc_ref.get().exists:
        print("Placeholder activity already exists in Firestore.")
        return
    
    placeholder_data = {
        "activity_id": "placeholder_activity",
        "user_id": "placeholder_user",
        "activity_description": "No activity data available yet.",
        "timestamp": firestore.SERVER_TIMESTAMP,
        "likes": 0,
        "comments": [
            {
                "user_id": "placeholder_user",
                "comment_text": "Be the first to add an activity!"
            }
        ],
        "images": ["https://your_placeholder_image_url.com/image.png"]
    }
    
    placeholder_doc_ref.set(placeholder_data)
    print("Placeholder activity added to Firestore.")




if __name__ == '__main__':
    add_placeholder_activity()  # Call the function after initializing Firebase
    # Run the application
    app.run(debug=True)  # The app runs in debug mode for easier development
