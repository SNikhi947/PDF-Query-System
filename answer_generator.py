# answer_generator.py
import cohere

co = cohere.Client("korv6munGd0a3gPtoheXu3uHR6vw8xvhucrKYWae")  # Use your actual key

def generate_answer(user_query, relevant_text):
    prompt = f"""
You are an assistant. Based on the document content, answer the user's question clearly and briefly.

Document Section:
\"\"\"
{relevant_text}
\"\"\"

User Question:
{user_query}

Give a clean answer based only on the document.
"""

    response = co.chat(
        message=prompt,
        model="command-r",
        temperature=0.4
    )

    return response.text.strip()

