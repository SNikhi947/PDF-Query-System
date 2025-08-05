import streamlit as st
import json
from document_ingestion.ingest import extract_text
from parser import query_to_json
from schema import ParsedQuery
from search_engine import find_most_relevant_chunk
from answer_generator import generate_answer

st.title(" PDF Query System")

uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "eml"])
user_query = st.text_input("Enter your question")

if uploaded_file and user_query:
    try:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        document_text = extract_text(uploaded_file.name)
        raw_json = query_to_json(user_query, document_text)
        json_dict = json.loads(raw_json)
        parsed = ParsedQuery.model_validate(json_dict)
        search_query = f"{parsed.intent} {parsed.entity.condition or ''} {parsed.entity.document_section or ''}"
        chunks = [chunk.strip() for chunk in document_text.split('\n') if len(chunk.strip()) > 30]
        best_match, score = find_most_relevant_chunk(search_query, chunks)
        final_answer = generate_answer(user_query, best_match )
        st.success(" Answer:")
        st.write(final_answer)
        with open("logs.txt", "a") as log_file:
            log_file.write(f"File: {uploaded_file.name}, Question: {user_query}, Answer: {final_answer}\n\n")
        st.download_button(
            label=" Download Answer",
            data=final_answer,
            file_name="answer.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Error: {e}")