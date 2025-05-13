from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using TextBlob.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        tuple: (sentiment_label, polarity, subjectivity)
    """
    # Create TextBlob object
    analysis = TextBlob(text)
    
    # Get polarity score (-1.0 to 1.0, where -1 is negative, 0 is neutral, 1 is positive)
    polarity = analysis.sentiment.polarity
    
    # Get subjectivity score (0.0 to 1.0, where 0 is objective and 1 is subjective)
    subjectivity = analysis.sentiment.subjectivity
    
    # Determine sentiment label based on polarity
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
        
    return sentiment, polarity, subjectivity
