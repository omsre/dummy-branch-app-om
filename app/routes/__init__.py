from flask import Blueprint, jsonify

routes = Blueprint("routes", __name__)

@routes.route("/", methods=["GET"])
def root():
    """
    Root endpoint for quick sanity check.
    Returns a simple JSON message instead of 404.
    """
    return jsonify({
        "message": "Welcome to Branch Loans API",
        "available_endpoints": [
            "/health",
            "/users",
            "/loans"
        ]
    }), 200

