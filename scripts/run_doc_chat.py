from tools.rag.search import retrieve
from tools.local_llm.ollama_client import chat

SYSTEM = (
    "אתה עוזר טכני. ענה רק מתוך הקונטקסט שסופק.\n"
    "אם המידע לא נמצא בקונטקסט – ענה 'לא מצאתי במקור הנתונים'.\n"
    "ענה בעברית אם נשאלת בעברית, אחרת באנגלית."
)

def build_messages(question: str, contexts: list[dict]) -> list[dict]:
    ctx = "\n\n---\n\n".join(
        [f"[{i+1}] {c['path']}\n{c['text']}" for i, c in enumerate(contexts)]
    )
    system = SYSTEM + "\n\n====\nקונטקסט:\n" + ctx + "\n====\n"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ]

def main():
    print(">> Doc Chat (Ollama). Ctrl+C to exit.")
    while True:
        try:
            q = input("\nשאלה: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            continue
        ctx = retrieve(q, k=6)
        msgs = build_messages(q, ctx)
        ans = chat(msgs, stream=False, options={"temperature": 0.1})
        print("\nתשובה:\n" + ans)

if __name__ == "__main__":
    main()
