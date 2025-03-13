from fastapi import APIRouter, Query
import requests
from textblob import TextBlob

router = APIRouter()

# Replace with your GNews API Key (Get from https://gnews.io/)
GNEWS_API_KEY = "484af3c7216b19781fcf2bc830e3628e"
GNEWS_BASE_URL = "https://gnews.io/api/v4/search"

@router.get("/events/crypto-news/")
def get_crypto_news(
    query: str = Query("cryptocurrency", description="Search term (e.g., Bitcoin, Ethereum)"),
    from_date: str = Query(None, description="Start date in YYYY-MM-DDThh:mm:ssTZD (e.g., 2025-03-11T23:54:31Z)"),
    to_date: str = Query(None, description="End date in YYYY-MM-DD"),
    max_articles: int = Query(5, description="Number of articles to fetch")
):
    """Fetches crypto-related news and analyzes sentiment."""
    
    params = {
        "q": query,
        "lang": "en",
        "from": from_date,
        "to": to_date,
        "max": max_articles,
        "token": GNEWS_API_KEY
    }
    
    response = requests.get(GNEWS_BASE_URL, params=params)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch news", "status_code": response.status_code}
    
    articles = response.json().get("articles", [])

    # Perform sentiment analysis
    results = []
    for article in articles:
        sentiment_score = TextBlob(article["title"] + " " + article["description"]).sentiment.polarity
        results.append({
            "title": article["title"],
            "url": article["url"],
            "publishedAt": article["publishedAt"],
            "sentiment_score": sentiment_score,
            "sentiment": "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
        })

    return {"query": query, "results": results}