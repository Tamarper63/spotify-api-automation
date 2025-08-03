from tools.nlp_to_api.query_engine import query_api_with_nlp

def main():
    question = "תראה לי את האומנים הכי מושמעים שלי"
    result = query_api_with_nlp(question, doc_path="docs/spotify_api_snippet.md")

    print("--- NLP → API Result ---")
    print(f"Method: {result['method']}")
    print(f"URL: {result['url']}")
    print(f"Headers: {result['headers']}")
    print(f"Body: {result['body']}")

if __name__ == "__main__":
    main()
