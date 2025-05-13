import os
import json
import logging
from openai import OpenAI
from textblob import TextBlob  # Keep as fallback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_sentiment_with_openai(text):
    """
    Analyze the sentiment of the given text using OpenAI's GPT-4o model.
    
    Args:
        text (str): The movie review text to analyze
        
    Returns:
        dict: {
            'sentiment': str, 
            'confidence': float,
            'analysis': str
        }
    """
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a sentiment analysis expert specialized in movie reviews. "
                        "Analyze the movie review and determine whether the sentiment is positive, "
                        "negative, or neutral. Provide a confidence score between 0 and 100, "
                        "where 100 means absolute certainty. Also include a brief explanation "
                        "for your classification. Return ONLY a JSON object with the following format: "
                        "{'sentiment': 'positive/negative/neutral', 'confidence': number, "
                        "'analysis': 'brief explanation'}"
                    )
                },
                {"role": "user", "content": text}
            ],
            temperature=0,  # Use deterministic output for consistent results
            max_tokens=150
        )
        
        # Parse the response content
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("Empty response from OpenAI API")
            
        result = json.loads(content)
        
        # Ensure we have the expected fields
        if not all(k in result for k in ("sentiment", "confidence", "analysis")):
            raise ValueError("Unexpected response format from OpenAI API")
            
        return result
        
    except Exception as e:
        logger.error(f"Error using OpenAI API: {str(e)}")
        # Use TextBlob as fallback in case of API issues
        return fallback_sentiment_analysis(text)


def fallback_sentiment_analysis(text):
    """
    Fallback to TextBlob if OpenAI API fails.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: {
            'sentiment': str, 
            'confidence': float,
            'analysis': str
        }
    """
    try:
        # Create TextBlob object
        from textblob.blob import Blobber
        from textblob.sentiments import PatternAnalyzer
        
        # Use the Pattern analyzer explicitly
        tb = Blobber(analyzer=PatternAnalyzer())
        blob = tb(text)
        
        # Get polarity score (-1.0 to 1.0, negative to positive)
        polarity = blob.sentiment[0]  # Access first element of sentiment tuple
        
        # Determine sentiment label based on polarity
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Calculate confidence score (0-100)
        confidence = abs(polarity) * 100
        
        # Create simple analysis message
        analysis_text = f"TextBlob detected {sentiment} sentiment with {confidence:.1f}% confidence."
    except Exception as e:
        # Absolute fallback for any TextBlob issues
        logger.error(f"TextBlob fallback failed: {str(e)}")
        sentiment = "neutral"
        confidence = 0
        analysis_text = "Unable to determine sentiment with confidence."
    
    return {
        'sentiment': sentiment,
        'confidence': round(confidence, 2),
        'analysis': analysis_text
    }


def analyze_sentiment(text):
    """
    Main function to analyze sentiment, using OpenAI with TextBlob as fallback.
    
    Args:
        text (str): The review text to analyze
        
    Returns:
        dict: Analysis results including sentiment, confidence, and explanation
    """
    if not OPENAI_API_KEY:
        logger.warning("No OpenAI API key found. Using TextBlob fallback.")
        return fallback_sentiment_analysis(text)
    
    try:
        return analyze_sentiment_with_openai(text)
    except Exception as e:
        logger.error(f"Error in OpenAI sentiment analysis: {str(e)}")
        logger.info("Falling back to TextBlob sentiment analysis")
        return fallback_sentiment_analysis(text)