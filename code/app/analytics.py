# app/analytics.py
import pandas as pd
from datetime import datetime
from textblob import TextBlob  
from collections import Counter


query_logs = pd.DataFrame(columns=["timestamp", "question"])

def log_query(question):
    """Log the user query with the timestamp."""
    global query_logs
    new_row = pd.DataFrame([{"timestamp": datetime.now(), "question": question}])
    query_logs = pd.concat([query_logs, new_row], ignore_index=True)

def get_query_summary():
    """Get a summary of frequent keywords in the query logs."""
    words = " ".join(query_logs["question"]).split()
    keyword_counts = Counter(words)
    return dict(keyword_counts)

def generate_analytics_report(text: str) -> dict:
    """
    Generate analytics for the given text. This includes:
    - Word count
    - Sentiment polarity
    - Sentiment subjectivity
    """
    # Word count
    word_count = len(text.split())
    
    # Sentiment analysis using TextBlob
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)
    sentiment_subjectivity = blob.sentiment.subjectivity  # Range: 0 (objective) to 1 (subjective)
    
  
    analytics = {
        "word_count": word_count,
        "sentiment_polarity": sentiment_polarity,
        "sentiment_subjectivity": sentiment_subjectivity
    }
    
    return analytics

def get_daily_query_trends():
    """Analyze user queries and group by date for daily trends."""
    # Convert timestamp to just the date
    query_logs['date'] = query_logs['timestamp'].dt.date
    
    daily_trends = query_logs.groupby('date').size().reset_index(name='query_count')
    
    return daily_trends

def get_weekly_query_trends():
    """Analyze user queries and group by week for weekly trends."""
    query_logs['week'] = query_logs['timestamp'].dt.isocalendar().week
    
    weekly_trends = query_logs.groupby('week').size().reset_index(name='query_count')
    
    return weekly_trends




