import gcs_setup
from google.cloud import storage
from .gcs_utils import extract_text_from_pdf
from .summarization import summarize_text
from .analytics import generate_analytics_report, log_query, get_daily_query_trends, get_weekly_query_trends
import re

def search_documents(question: str, bucket_name: str):
    """Search for a keyword in documents stored in GCS, summarize relevant ones, generate analytics, and track user queries."""
    
    
    log_query(question)

   
    daily_trends = get_daily_query_trends()
    weekly_trends = get_weekly_query_trends()
    
    print(f"Daily query trends: {daily_trends}")
    print(f"Weekly query trends: {weekly_trends}")
   
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    summarized_results = []  

    
    question_cleaned = re.sub(r'\b(what|is|how|does|are|the|of|for|about|do|you|know|about)\b', '', question, flags=re.IGNORECASE).strip()

   
    primary_keyword = question_cleaned.lower()

    for blob in blobs:
        print(f"Processing document: {blob.name}")
        text = extract_text_from_pdf(blob.name, bucket_name)

        
        if re.search(rf"\b{primary_keyword}\b", text, re.IGNORECASE):
            print(f"Match found in document: {blob.name}")

           
            start_index = text.lower().find(primary_keyword)
            snippet = text[max(0, start_index - 200): start_index + 800]  # Extended surrounding text length for better context
            summary = summarize_text(snippet, question)
            analytics = generate_analytics_report(summary)

            summarized_results.append({
                "document": blob.name,
                "snippet": summary,
                "analytics": analytics,
                "query_trends": {
                    "daily": daily_trends.to_dict(orient='records'),
                    "weekly": weekly_trends.to_dict(orient='records')
                }
            })
        else:
            print(f"No relevant match in document: {blob.name}")


    if not summarized_results:
        summarized_results = [{"message": "No relevant documents found for your question."}]
    
    return summarized_results




