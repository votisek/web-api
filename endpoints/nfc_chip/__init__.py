from flask import Blueprint, request, jsonify
import json
import os
import hashlib
import random

blueprint = Blueprint("nfc_chip", __name__)

# Constants
USERS_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
DEFAULT_REDIRECT = "divi.votisek.dev/edit-redirect"

def load_users():
    """Safely load users data from JSON file"""
    try:
        if not os.path.exists(USERS_JSON_PATH):
            return {}
        with open(USERS_JSON_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    """Safely save users data to JSON file"""
    with open(USERS_JSON_PATH, "w") as f:
        json.dump(users, f, indent=4)

@blueprint.route("/get-redirect/<redirect_id>", methods=['GET'])
def get_redirect(redirect_id):
    users = load_users()
    
    if redirect_id in users:
        users[redirect_id]["redirect_count"] = users[redirect_id].get("redirect_count", 0) + 1
        save_users(users)
        return jsonify({
            "redirect_id": redirect_id,
            "redirect_url": users[redirect_id]["redirect"]
        }), 200
    return jsonify({"error": "Redirect ID not found"}), 404

@blueprint.route("/edit-redirect", methods=['GET'])
def edit_redirect():
    redirect_pin = request.args.get("redirect-pin")
    url = request.args.get("url")
    
    if not redirect_pin or not url:
        return jsonify({"error": "Missing redirect_id or url parameter"}), 400
    
    users = load_users()
    
    redirect_id = hashlib.sha256(redirect_pin.strip("0").encode()).hexdigest()[:8]

    if redirect_id in users:
        users[redirect_id].update({
            "redirect": url,
            "edit_count": users[redirect_id].get("edit_count", 0) + 1
        })
        save_users(users)
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Redirect ID not found or wrong PIN"}), 404

@blueprint.route("/new-chip", methods=['GET'])
def add_chip():
    color = request.args.get("color", "default")
    redirect_pin = str(random.randrange(0, 99999999)).strip("0")
    redirect_id = hashlib.sha256(redirect_pin.encode()).hexdigest()[:8]

    users = load_users()
    
    if redirect_id not in users:
        users[redirect_id] = {
            "redirect": DEFAULT_REDIRECT,
            "color": color,
            "redirect_count": 0,
            "edit_count": 0
        }
        save_users(users)
        return jsonify({"status": "created", "redirect_id": redirect_id, "redirect_pin": redirect_pin}), 201
    return jsonify({"error": "Chip already exists"}), 409