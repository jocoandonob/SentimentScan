# SentimentScan

SentimentScan is a web-based application that performs AI-powered sentiment analysis on movie reviews. It provides detailed analysis of the emotional tone and sentiment of text input, helping users understand the underlying sentiment in movie reviews.

## Features

- Real-time sentiment analysis of movie reviews
- AI-powered analysis with confidence scores
- Detailed breakdown of sentiment components
- User-friendly web interface
- RESTful API endpoint for sentiment analysis

## Technologies Used

- Python 3.x
- Flask (Web Framework)
- AI Sentiment Analysis
- HTML/CSS/JavaScript
- RESTful API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SentimentScan.git
cd SentimentScan
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Enter a movie review in the text input field
3. Click "Analyze" to get the sentiment analysis results
4. View the detailed analysis including:
   - Overall sentiment
   - Confidence score
   - Detailed analysis breakdown

## API Usage

You can also use the sentiment analysis API endpoint:

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "review=Your movie review text here"
```

## Project Structure

- `app.py` - Main Flask application
- `ai_sentiment_analyzer.py` - AI sentiment analysis implementation
- `enhanced_sentiment_analyzer.py` - Enhanced sentiment analysis features
- `templates/` - HTML templates
- `static/` - Static assets (CSS, JavaScript, images)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the open-source community for their invaluable tools and libraries 