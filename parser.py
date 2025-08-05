import cohere
import re

co = cohere.Client("korv6munGd0a3gPtoheXu3uHR6vw8xvhucrKYWae")

def query_to_json(user_query, document_text):
    prompt = f"""
You are a JSON API builder. Based on the document and the user query, respond with a **single valid JSON object** like:

{{
  "intent": "get_waiting_period",
  "entity": {{
    "condition": "maternity",
    "document_section": "waiting period"
  }}
}}

Document:
\"\"\"
{document_text}
\"\"\"

User Query:
\"{user_query}\"

Rules:
- Do NOT return a list.
- Do NOT include ```json or any markdown.
- Only return a JSON object with exactly these keys:
  - intent: must be a short string like 'get_waiting_period'
  - entity: must include ONLY 'condition' and 'document_section'
- Do NOT include extra keys like 'waiting_period' inside entity.
"""

    response = co.chat(
        message=prompt,
        temperature=0.3,
        chat_history=[],
        model="command-r"
    )

    raw = response.text.strip()

    cleaned = re.sub(r"^```json|```$", "", raw, flags=re.MULTILINE).strip()

    return cleaned