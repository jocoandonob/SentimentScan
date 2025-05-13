import os
import logging
from flask import Flask, render_template, request, jsonify
from ai_sentiment_analyzer import analyze_sentiment
from models import db, UserUsage
from utils import generate_device_fingerprint, get_client_ip, check_usage_limit

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure the PostgreSQL database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the database
db.init_app(app)

# Usage limit configuration
MAX_USAGE = 7

# Create database tables
with app.app_context():
    db.create_all()
    logger.info("Database tables created")

@app.route("/")
def index():
    """Render the main page"""
    # Get client information
    ip_address = get_client_ip(request)
    device_fingerprint = generate_device_fingerprint(request)
    
    # Check usage status
    user_usage = UserUsage.get_or_create(ip_address, device_fingerprint)
    usage_status = check_usage_limit(user_usage, MAX_USAGE)
    
    # Pass usage data to template
    return render_template(
        "index.html",
        usage_remaining=usage_status["remaining"],
        usage_allowed=usage_status["allowed"],
        usage_total=usage_status["max"]
    )

@app.route("/usage")
def usage_status():
    """Return the current usage status"""
    # Get client information
    ip_address = get_client_ip(request)
    device_fingerprint = generate_device_fingerprint(request)
    
    # Check usage status
    user_usage = UserUsage.get_or_create(ip_address, device_fingerprint)
    usage_status = check_usage_limit(user_usage, MAX_USAGE)
    
    return jsonify(usage_status)

@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze the sentiment of the provided review text"""
    # Get client information
    ip_address = get_client_ip(request)
    device_fingerprint = generate_device_fingerprint(request)
    
    # Check usage status
    user_usage = UserUsage.get_or_create(ip_address, device_fingerprint)
    usage_status = check_usage_limit(user_usage, MAX_USAGE)
    
    # Check if user has reached usage limit
    if not usage_status["allowed"]:
        return jsonify({
            "error": "You have reached your analysis limit. Maximum 7 analyses per device/IP address.",
            "usage_status": usage_status
        }), 403
    
    # Get the review text from the request
    review = request.form.get("review", "")
    
    # Check if the review is empty
    if not review.strip():
        return jsonify({"error": "Please enter a movie review to analyze"}), 400
    
    try:
        # Analyze the sentiment using AI-powered analyzer
        result = analyze_sentiment(review)
        
        # Add debug logging
        logger.debug(f"Sentiment analysis result: {result}")
        
        # Increment usage count
        user_usage.increment_usage()
        
        # Update usage status after increment
        usage_status = check_usage_limit(user_usage, MAX_USAGE)
        
        # Return the analysis results with updated usage info
        return jsonify({
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "analysis": result["analysis"],
            "usage_status": usage_status
        })
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {str(e)}")
        return jsonify({
            "error": "An error occurred during analysis. Please try again.",
            "usage_status": usage_status
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
