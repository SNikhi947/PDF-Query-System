import streamlit as st
from document_ingestion.ingest import extract_text
from parser import query_to_json
from schema import ParsedQuery
from search_engine import find_most_relevant_chunk
from answer_generator import generate_answer
import json
st.title("LLM-Powered Document Question Answering")
uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, or EML)", type=["pdf", "docx", "eml"])
user_query = st.text_input("Ask your question:")
if uploaded_file and user_query:
    try:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        document_text = extract_text(uploaded_file.name)    
        raw_json = query_to_json(user_query, document_text)
        json_dict = json.loads(raw_json)
        parsed = ParsedQuery.model_validate(json_dict)
        search_query = f"Information about {parsed.entity.document_section or ''} for {parsed.entity.condition or ''}"
        lines = [line.strip() for line in document_text.split('\n') if len(line.strip()) > 30]
        chunks = [' '.join(lines[i:i+3]) for i in range(0, len(lines), 3)]
        best_chunks, scores = find_most_relevant_chunk(search_query, chunks)
        best_answer = best_chunks[0]
        final_answer = generate_answer(user_query, best_answer)
        st.subheader("Final Answer:")
        st.success(final_answer)
        with open("logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"File: {uploaded_file.name}, Question: {user_query}, Answer: {final_answer}\n\n")
        st.download_button(
            label="Download Answer",
            data=final_answer,
            file_name="answer.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Error: {e}")
