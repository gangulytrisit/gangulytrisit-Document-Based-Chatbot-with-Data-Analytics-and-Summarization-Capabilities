from gcs_setup import client, bucket
import pdfplumber
import os
import io  
import re  

def extract_text_from_pdf(blob_name, bucket_name):
    """
    Extracts text from a PDF file stored in a GCS bucket.
    """
    blob = bucket.blob(blob_name)
    pdf_bytes = blob.download_as_bytes()

    try:
        with io.BytesIO(pdf_bytes) as pdf_file:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                    else:
                        print(f"Warning: No text found on page {page.page_number} of {blob_name}")
    except Exception as e:
        print(f"Error reading {blob_name}: {e}")
        text = ""

  
    text = re.sub(r'(\w)([A-Z])', r'\1 \2', text)  
    text = re.sub(r'\s+', ' ', text)  
    text = text.strip()  


    return text

def search_documents(query, bucket_name):
    """
    Search for relevant documents in GCS based on a query.
    """
    files = bucket.list_blobs()

    found = False
    for file in files:
        print(f"Checking file: {file.name}")
        text = extract_text_from_pdf(file.name, bucket_name)

  
        query_normalized = query.strip().lower()  
        text_normalized = text.strip().lower() 

       
        if text:
            print(f"Text from {file.name}: {text[:100]}...")  
            if query_normalized in text_normalized: 
                print(f"Found relevant document: {file.name}")
                found = True
                return {"results": text}

    if not found:
        print(f"No relevant documents found for query: {query}")
    return {"results": "No relevant documents found for your question."}





