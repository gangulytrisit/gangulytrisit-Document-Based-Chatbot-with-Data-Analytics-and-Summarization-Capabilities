import gcs_setup  
from flask import Blueprint, request, jsonify, render_template  
from .search import search_documents
from .summarization import summarize_text  
from .analytics import generate_analytics_report  
from .analytics import log_query, get_daily_query_trends, get_weekly_query_trends

api_bp = Blueprint('api', __name__)

@api_bp.route("/", methods=["GET"])
def home():
    """Render the index.html page."""
    return render_template("index.html") 

@api_bp.route("/ask", methods=["POST"])
def ask_question():
    """Route to handle questions and search documents in GCS."""
    
    question = request.json.get("question")
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    
    log_query(question)

    try:
        bucket_name = "my-document-storage-bucket" 
        print(f"Searching for documents related to the question: {question}")
        
       
        search_results = search_documents(question, bucket_name)
        print("Search Results:", search_results)
        
        if not search_results or "message" in search_results[0]:
            print("No relevant documents found.")
            return jsonify({"error": "No relevant documents found for your question."}), 404
        
   
        summarized_results = []
        
        for result in search_results:
            print("Processing result:", result)
            
            if isinstance(result, dict) and "snippet" in result:
                snippet = result["snippet"]
                             
                summary = summarize_text(snippet, question)              
               
                analytics = generate_analytics_report(snippet)
                
                summarized_results.append({
                    "document": result["document"],
                    "summary": summary,
                    "analytics": analytics  # Add analytics data here
                })
            else:
                print("Unexpected result format:", result)
        
       
        daily_trends = get_daily_query_trends()
        weekly_trends = get_weekly_query_trends()

        return jsonify({
            "results": summarized_results,
            "analytics": {
                "total_word_count": sum([result["analytics"]["word_count"] for result in summarized_results]),
                "avg_sentiment_polarity": sum([result["analytics"]["sentiment_polarity"] for result in summarized_results]) / len(summarized_results),
                "avg_sentiment_subjectivity": sum([result["analytics"]["sentiment_subjectivity"] for result in summarized_results]) / len(summarized_results)
            },
            "query_trends": {
                "daily": daily_trends.to_dict(orient='records'),
                "weekly": weekly_trends.to_dict(orient='records')
            }
        })
    
    except Exception as e:
        print(f"Error occurred during document search: {e}")
        return jsonify({"error": f"An error occurred while processing your request: {str(e)}"}), 500
 