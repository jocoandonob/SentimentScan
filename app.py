import os
import logging
from flask import Flask, render_template, request, jsonify
from ai_sentiment_analyzer import analyze_sentiment

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

@app.route("/")
def index():
    """Render the main page"""
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze the sentiment of the provided review text"""
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
        
        # Return the analysis results
        return jsonify({
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "analysis": result["analysis"]
        })
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {str(e)}")
        return jsonify({"error": "An error occurred during analysis. Please try again."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
