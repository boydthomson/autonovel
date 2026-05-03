#!/usr/bin/env python3
"""
Complete an in-progress outline.md.

Reads whatever gen_outline.py produced, detects where it stopped,
and asks the writer model to finish remaining chapters plus the
Foreshadowing Ledger — with no story-specific assumptions.
"""
import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv
from utils import extract_text_from_response, get_max_tokens_with_thinking

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
API_BASE = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.anthropic.com")


def call_writer(prompt, max_tokens=16000):
    max_tokens = get_max_tokens_with_thinking(max_tokens)
    import httpx
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": WRITER_MODEL,
        "max_tokens": max_tokens,
        "temperature": 0.5,
        "system": (
            "You are a novel architect completing an in-progress chapter outline. "
            "Continue in exactly the same format as the existing chapters. "
            "Every chapter needs: POV, Location, Save the Cat beat, % mark, "
            "Emotional arc, Try-fail cycle, Beats, Plants, Payoffs, Character movement, "
            "The lie, Word count target."
        ),
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = httpx.post(f"{API_BASE}/v1/messages", headers=headers, json=payload, timeout=600)
    resp.raise_for_status()
    return extract_text_from_response(resp.json())


def detect_outline_state(text: str) -> dict:
    """Return info about what's already in the outline."""
    chapter_headers = re.findall(r"^###\s+Ch\s+(\d+)\s*:", text, re.MULTILINE | re.IGNORECASE)
    chapter_numbers = [int(n) for n in chapter_headers]
    has_ledger = bool(re.search(r"foreshadowing\s+ledger", text, re.IGNORECASE))
    # Detect target chapter count from Act Structure if present
    target_match = re.search(r"(\d+)[\s-]+chapter", text, re.IGNORECASE)
    target = int(target_match.group(1)) if target_match else 24
    target = max(target, 22)
    return {
        "chapters_found": sorted(set(chapter_numbers)),
        "last_chapter": max(chapter_numbers) if chapter_numbers else 0,
        "has_ledger": has_ledger,
        "target_chapters": target,
    }


outline_path = BASE_DIR / "outline.md"
existing = outline_path.read_text()
state = detect_outline_state(existing)

last = state["last_chapter"]
target = state["target_chapters"]
has_ledger = state["has_ledger"]

if last >= target and has_ledger:
    print("Outline already complete — nothing to do.", file=sys.stderr)
    sys.exit(0)

needs = []
if last < target:
    needs.append(
        f"Complete chapters {last + 1} through {target} in the same format as the existing chapters."
    )
if not has_ledger:
    needs.append(
        "Add a Foreshadowing Ledger at the end:\n\n"
        "## Foreshadowing Ledger\n\n"
        "| # | Thread | Planted (Ch) | Reinforced (Ch) | Payoff (Ch) | Type |\n"
        "|---|--------|-------------|-----------------|-------------|------|\n\n"
        "Include at least 15 threads. Types: object, dialogue, action, symbolic, structural. "
        "Plant-to-payoff distance must be at least 3 chapters."
    )

tasks = "\n\n".join(needs)

# Read companion files for story context
mystery_text = (BASE_DIR / "MYSTERY.md").read_text()
characters_text = (BASE_DIR / "characters.md").read_text()

prompt = f"""Here is an in-progress novel outline. {
    f"It currently covers chapters 1–{last} of a planned {target}-chapter novel." if last > 0
    else "It appears to be empty or very early."
}

YOUR TASKS:
{tasks}

CONSTRAINTS:
- Match the format of existing chapters exactly
- Vary Try-fail types: aim for 60%+ yes-but or no-and
- At least one quiet chapter in the back half (character-focused, low action)
- The lie established early must be fully shattered by the climax
- Stability Trap: not everything resolves cleanly
- Final Image should mirror the Opening Image but show transformation

THE OUTLINE SO FAR:
{existing}

CHARACTER REFERENCE (for consistency):
{characters_text}

THE CENTRAL MYSTERY (author's eyes only):
{mystery_text}
"""

print(f"Outline has {last}/{target} chapters, ledger={'yes' if has_ledger else 'no'}. Completing...", file=sys.stderr)
result = call_writer(prompt)
outline_path.write_text(existing.rstrip() + "\n\n" + result)
print(result)
