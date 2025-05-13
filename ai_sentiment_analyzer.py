import os
import json
import logging
from openai import OpenAI
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def analyze_sentiment_with_openai(text):
    """
    Analyze sentiment using OpenAI's GPT-4o model.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Analysis result containing sentiment, confidence and analysis
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
                        "You are an expert at analyzing movie review sentiment. "
                        "Analyze the sentiment of the following movie review and classify it as "
                        "'positive', 'negative', or 'neutral'. "
                        "Return a JSON object with the following fields: "
                        "- sentiment: 'positive', 'negative', or 'neutral' "
                        "- confidence: a number between 0 and 100 indicating your confidence "
                        "- analysis: a brief explanation of your reasoning"
                    )
                },
                {"role": "user", "content": text}
            ],
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("Empty response from OpenAI API")
            
        result = json.loads(content)
        logger.info(f"OpenAI sentiment result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error with OpenAI sentiment analysis: {e}")
        # Fall back to alternative method if OpenAI fails
        return analyze_sentiment_fallback(text)

def analyze_sentiment_fallback(text):
    """
    Analyze sentiment using a simple keyword-based approach as fallback.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Analysis result containing sentiment, confidence and analysis
    """
    try:
        # Simple keyword-based sentiment analysis as fallback
        text = text.lower()
        
        # Positive keywords
        positive_words = [
            "good", "great", "excellent", "amazing", "awesome", "wonderful", 
            "fantastic", "superb", "brilliant", "masterpiece", "loved", "best",
            "enjoy", "impressive", "beautiful", "perfect", "recommend", "favorite"
        ]
        
        # Negative keywords
        negative_words = [
            "bad", "terrible", "awful", "horrible", "disappointing", "waste", 
            "boring", "poor", "worst", "hate", "dislike", "mediocre", "dull",
            "stupid", "failure", "disaster", "mess", "weak", "annoying"
        ]
        
        # Count positive and negative words
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        # Determine overall sentiment
        if positive_count > negative_count:
            sentiment = "positive"
            polarity = min(1.0, positive_count / 10)
        elif negative_count > positive_count:
            sentiment = "negative"
            polarity = -min(1.0, negative_count / 10)
        else:
            sentiment = "neutral"
            polarity = 0.0
            
        # Calculate confidence score (0-100)
        if sentiment == "neutral":
            confidence = 30  # Lower confidence for neutral reviews
        else:
            confidence = min(100, (abs(positive_count - negative_count) / (positive_count + negative_count + 1)) * 100)
        
        result = {
            "sentiment": sentiment,
            "confidence": round(confidence, 1),
            "analysis": f"Keyword analysis detected {sentiment} sentiment (polarity: {polarity:.2f})"
        }
        
        logger.info(f"TextBlob sentiment result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error with TextBlob sentiment analysis: {e}")
        # Ultimate fallback
        return {
            "sentiment": "neutral",
            "confidence": 0,
            "analysis": "Analysis failed. Unable to determine sentiment."
        }

def analyze_sentiment(text):
    """
    Main sentiment analysis function that attempts OpenAI first, 
    then falls back to TextBlob if needed.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Analysis result
    """
    if not text or not text.strip():
        return {
            "sentiment": "neutral",
            "confidence": 0,
            "analysis": "No text provided for analysis."
        }
    
    if openai_api_key:
        return analyze_sentiment_with_openai(text)
    else:
        logger.warning("No OpenAI API key available. Using fallback method instead.")
        return analyze_sentiment_fallback(text)