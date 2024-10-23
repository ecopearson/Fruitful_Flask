from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

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

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)  # The app runs in debug mode for easier development
