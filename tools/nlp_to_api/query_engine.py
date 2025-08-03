from openai import OpenAI
from dotenv import load_dotenv
from tools.nlp_to_api.prompt_template import TEMPLATE
from tools.nlp_to_api.openapi_loader import load_api_doc

load_dotenv()  # טוען את OPENAI_API_KEY מתוך .env

client = OpenAI()  # קורא את המפתח מהסביבה

def query_api_with_nlp(user_input: str, doc_path="docs/spotify_api_snippet.md", model="gpt-4o") -> dict:
    api_docs = load_api_doc(doc_path)

    messages = [
        {"role": "system", "content": TEMPLATE.format(api_docs=api_docs)},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return extract_json(response.choices[0].message.content)

def extract_json(text: str) -> dict:
    import json, re
    match = re.search(r"\{[\s\S]+\}", text)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No valid JSON found in model output.")
