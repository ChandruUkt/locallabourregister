from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from urllib.parse import quote_plus
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB Atlas connection
username = quote_plus('deltanovaindia')
password = quote_plus('chacha@2025')  # This will encode @ as %40

# Create connection string
connection_string = f"mongodb+srv://{username}:{password}@cluster0.mp4sb12.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(connection_string)
    db = client.LLR  # Your database name
    workers = db.workers  # Define the workers collection
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Connection failed: {e}")

@app.route('/')
def home():
    return "LLR Backend Service"

# Register a new worker
@app.route('/api/register', methods=['POST'])
def register_worker():
    data = request.json

    required_fields = ['name', 'phone', 'location', 'category', 'distance', 'charge', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    # Check if phone already exists
    if workers.find_one({'phone': data['phone']}):
        return jsonify({'error': 'Phone number already registered'}), 400

    # Hash password before storing
    hashed_password = generate_password_hash(data['password'])
    data['password'] = hashed_password
    
    # Add registration date
    data['registration_date'] = ObjectId().generation_time
    
    # Insert new worker
    try:
        worker_id = workers.insert_one(data).inserted_id
        return jsonify({
            'message': 'Registration successful',
            'worker_id': str(worker_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Search workers
@app.route('/api/search', methods=['GET'])
def search_workers():
    location = request.args.get('location')
    category = request.args.get('category')

    if not location or not category:
        return jsonify({'error': 'Location and category are required'}), 400

    try:
        results = list(workers.find({
            'location': location,
            'category': category
        }, {'_id': 1, 'name': 1, 'phone': 1, 'location': 1, 
            'category': 1, 'distance': 1, 'charge': 1, 'experience': 1}))
            
        # Convert ObjectId to string
        for worker in results:
            worker['_id'] = str(worker['_id'])
            
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Worker login
@app.route('/api/login', methods=['POST'])
def worker_login():
    data = request.json

    if 'phone' not in data or 'password' not in data:
        return jsonify({'error': 'Phone and password are required'}), 400

    try:
        worker = workers.find_one({'phone': data['phone']})
        
        if not worker or not check_password_hash(worker['password'], data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Create response without sensitive data
        response = {
            '_id': str(worker['_id']),
            'name': worker['name'],
            'phone': worker['phone'],
            'location': worker['location'],
            'category': worker['category']
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
