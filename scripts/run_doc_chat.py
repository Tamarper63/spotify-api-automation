#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doc Chat (Ollama) — RAG-assisted console tool
- Retrieves context with the local RAG layer.
- Chats with a local LLM (Ollama) constrained to the retrieved context.
- English-only, technical tone.

Usage:
  python doc_chat.py
  python doc_chat.py -k 8 --temperature 0.0
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Sequence

from tools.rag.search import retrieve
from tools.local_llm.ollama_client import chat

DEFAULT_SYSTEM = (
    "You are a technical assistant. Answer ONLY using the provided context.\n"
    "If the information is not present in the context, reply exactly: 'Not found in the data source.'\n"
    "Respond in English only."
)


def build_messages(question: str, contexts: Sequence[Dict[str, str]], system_prompt: str) -> List[Dict[str, str]]:
    """
    Construct chat messages for the LLM with a system prompt and a stitched context section.
    Each context item is rendered with its path and text, separated by a visible delimiter.
    """
    stitched = "\n\n---\n\n".join(
        f"[{i + 1}] {c.get('path', '<unknown>')}\n{c.get('text', '')}"
        for i, c in enumerate(contexts)
    )
    system = f"{system_prompt}\n\n====\nContext:\n{stitched}\n====\n"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ]


def run_console(k: int, temperature: float, stream: bool, system_prompt: str) -> None:
    """
    Interactive console loop. Fetches context via RAG and queries the local LLM.
    Ctrl+C / Ctrl+D to exit.
    """
    print(">> Doc Chat (Ollama). Press Ctrl+C to exit.")
    while True:
        try:
            q = input("\nQuestion: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()  # newline for clean exit
            break

        if not q:
            continue

        try:
            ctx = retrieve(q, k=k)
        except Exception as e:
            print(f"[ERROR] retrieve() failed: {e}", file=sys.stderr)
            continue

        msgs = build_messages(q, ctx, system_prompt=system_prompt)

        try:
            ans = chat(
                msgs,
                stream=stream,
                options={"temperature": float(temperature)},
            )
        except Exception as e:
            print(f"[ERROR] chat() failed: {e}", file=sys.stderr)
            continue

        print("\nAnswer:\n" + (ans if isinstance(ans, str) else str(ans)))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="RAG-constrained local LLM console (English-only)."
    )
    p.add_argument("-k", type=int, default=6, help="Number of context chunks to retrieve.")
    p.add_argument("--temperature", type=float, default=0.1, help="LLM sampling temperature.")
    p.add_argument("--stream", action="store_true", help="Enable streamed responses if supported.")
    p.add_argument(
        "--system",
        type=str,
        default=DEFAULT_SYSTEM,
        help="Override system prompt (English-only).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    # Basic validation
    if args.k <= 0:
        print("[ERROR] -k must be > 0", file=sys.stderr)
        sys.exit(2)
    if not (0.0 <= args.temperature <= 2.0):
        print("[ERROR] --temperature must be in [0.0, 2.0]", file=sys.stderr)
        sys.exit(2)

    run_console(k=args.k, temperature=args.temperature, stream=args.stream, system_prompt=args.system)


if __name__ == "__main__":
    main()
