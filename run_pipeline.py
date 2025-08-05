import json
from document_ingestion.ingest import extract_text
from parser import query_to_json
from schema import ParsedQuery
from search_engine import find_most_relevant_chunk

file_path = input("Enter the document file name (PDF, DOCX, or EML): ")
user_query = input("Enter your question about the document: ")

try:
    document_text = extract_text(file_path)
    raw_json = query_to_json(user_query, document_text)
    print("\nOutput:\n", raw_json)
    
    json_dict = json.loads(raw_json)
    parsed = ParsedQuery.model_validate(json_dict)
    print("\nJSON is valid!")
    print(parsed)

    
    search_query = f"Information about {parsed.entity.document_section or ''} for {parsed.entity.condition or ''}"

    lines = [line.strip() for line in document_text.split('\n') if len(line.strip()) > 30]
    chunks = [' '.join(lines[i:i+3]) for i in range(0, len(lines), 3)]
    best_chunks, scores = find_most_relevant_chunk(search_query, chunks)
    best_answer = best_chunks[0]  # top match
    print("\nAnswer from the document:\n")
    print(best_answer)
    from answer_generator import generate_answer
    final_answer = generate_answer(user_query, best_answer)
    print("\n Final Answer (LLM-generated):")
    print(final_answer)
except Exception as e:
    print("\nError processing response:", e)