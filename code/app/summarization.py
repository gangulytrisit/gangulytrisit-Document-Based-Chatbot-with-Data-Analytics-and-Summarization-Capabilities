from transformers import T5Tokenizer, T5ForConditionalGeneration

def summarize_text(input_text, query=None, min_length=50, max_length=150, num_beams=5):
    if not input_text or len(input_text.strip()) == 0:
        return "No content to summarize."
    
    # Initialize T5 tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained('t5-base')
    model = T5ForConditionalGeneration.from_pretrained('t5-base')

    # Preprocess input with query if provided
    if query:
        input_text = f"Question: {query} Context: {input_text}"

    # Tokenize and encode the input text
    input_ids = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate the summary with specific beam search and length constraints
    summary_ids = model.generate(
        input_ids, 
        num_beams=num_beams, 
        min_length=min_length, 
        max_length=max_length, 
        length_penalty=2.0, 
        early_stopping=True
    )

    # Decode the summary and clean up extra spaces
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()

    # Remove redundant phrases without disrupting the sentence structure
    seen_words = set()
    summary = ' '.join([word for word in summary.split() if not (word in seen_words or seen_words.add(word))])

    # Check for an empty summary output
    if not summary:
        return "Summary could not be generated."
    
    return summary



