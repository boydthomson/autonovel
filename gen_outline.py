#!/usr/bin/env python3
"""Generate outline.md from seed + world + characters + mystery + craft."""
import os
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
        "anthropic-beta": "context-1m-2025-08-07",
        "content-type": "application/json",
    }
    payload = {
        "model": WRITER_MODEL,
        "max_tokens": max_tokens,
        "temperature": 0.5,
        "system": (
            "You are a novel architect with deep knowledge of Save the Cat beats, "
            "Sanderson's plotting principles, Dan Harmon's Story Circle, and MICE Quotient. "
            "You build outlines that an author can draft from without inventing structure "
            "on the fly. Every chapter has beats, emotional arc, and try-fail cycle type. "
            "You never use AI slop words. You write in clean, direct prose."
        ),
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = httpx.post(f"{API_BASE}/v1/messages", headers=headers, json=payload, timeout=600)
    resp.raise_for_status()
    return extract_text_from_response(resp.json())

seed =(BASE_DIR / "seed.txt").read_text()
world = (BASE_DIR / "world.md").read_text()
characters = (BASE_DIR / "characters.md").read_text()
mystery = (BASE_DIR / "MYSTERY.md").read_text()
craft = (BASE_DIR / "CRAFT.md").read_text()

# Voice Part 2 only
voice = (BASE_DIR / "voice.md").read_text()
voice_lines = voice.split('\n')
part2_start = next(i for i, l in enumerate(voice_lines) if 'Part 2' in l)
voice_part2 = '\n'.join(voice_lines[part2_start:])

prompt = f"""Build a complete chapter outline for this novel. Target: 22-26 chapters,
~80,000 words total (~3,000-4,000 words per chapter).

SEED CONCEPT:
{seed}

THE CENTRAL MYSTERY (author's eyes only -- reader discovers gradually):
{mystery}

WORLD BIBLE:
{world}

CHARACTER REGISTRY:
{characters}

VOICE (tone and register):
{voice_part2}

CRAFT REFERENCE (structures to follow):
{craft}

BUILD THE OUTLINE WITH:

## Act Structure
Map out Act I (0-23%), Act II Part 1 (23-50%), Act II Part 2 (50-77%), Act III (77-100%).
State the percentage marks for the key story beats.

## Chapter-by-Chapter Outline

For EACH chapter, provide:
### Ch N: [Title]
- **POV:** (derive from the story -- which character, what perspective mode)
- **Location:** Which locations/settings
- **Save the Cat beat:** Which beat this chapter serves (Opening Image, Setup, Catalyst, etc.)
- **% mark:** Where this falls in the novel
- **Emotional arc:** Starting emotion → ending emotion
- **Try-fail cycle:** Yes-but / No-and / No-but / Yes-and
- **Beats:** 3-5 specific scene beats that must happen
- **Plants:** Foreshadowing elements planted in this chapter
- **Payoffs:** Foreshadowing elements that pay off here
- **Character movement:** What changes for the protagonist (or other characters) by chapter's end
- **The lie:** How the protagonist's central lie is reinforced or challenged in this chapter
- **~Word count target:** for pacing

## Foreshadowing Ledger

A table tracking every planted thread:
| # | Thread | Planted (Ch) | Reinforced (Ch) | Payoff (Ch) | Type |

Include at LEAST 15 threads. Types: object, dialogue, action, symbolic, structural.
Plant-to-payoff distance must be at least 3 chapters.

KEY PLOT ARCHITECTURE (derive specifics from the seed and characters):

Act I (Ch 1-6ish): Establish the protagonist's ordinary world, their wound, their lie.
Plant the central mystery or question early. Catalyst forces the protagonist out of stasis.

Act II Part 1 (Ch 7-12ish): Protagonist pursues their Want using the Lie as a guide.
Investigation, discovery, alliances. Midpoint: partial truth that changes approach
(false victory or false defeat).

Act II Part 2 (Ch 13-18ish): Pressure mounts. The Lie becomes increasingly unsustainable.
All Is Lost: Protagonist confronts the truth they've been avoiding.

Act III (Ch 19-24ish): Protagonist understands what they truly need. Must choose how to answer
the central question. Climax is mechanically resolvable using established story rules.
Resolution shows the aftermath.

CONSTRAINTS:
- The climax must be earned by the story's established rules -- no deus ex machina
- The protagonist's investigation (if any) should feel like a mystery plot overlaid on their arc
- The Stability Trap: bad things must stay bad. Not everything resolves cleanly.
- At least 3 chapters should be "quiet" -- character-focused, low-action, emotionally rich
- Vary the try-fail types: 60%+ should be "yes-but" or "no-and"
- Final Image should mirror Opening Image but show transformation
"""

print("Calling writer model...", file=sys.stderr)
result = call_writer(prompt)
(BASE_DIR / "outline.md").write_text(result)
Path("/tmp/outline_output.md").write_text(result)
print(result)
