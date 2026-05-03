#!/usr/bin/env python3
"""
One-shot world.md generator for foundation phase.
Reads seed.txt + voice.md, calls the writer model, outputs world.md content.
"""
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
        "content-type": "application/json",
    }
    payload = {
        "model": WRITER_MODEL,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "system": (
            "You are a worldbuilder with deep knowledge of Sanderson's Laws, "
            "Le Guin's prose philosophy, and TTRPG-quality lore design. "
            "You write world bibles that are specific, interconnected, and imply depth "
            "beyond what's stated. You never use AI slop words (delve, tapestry, myriad, etc). "
            "You write in clean, direct prose. Every rule has a cost. Every cultural detail "
            "implies a history. Every location has a sensory signature."
        ),
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = httpx.post(f"{API_BASE}/v1/messages", headers=headers, json=payload, timeout=300)
    resp.raise_for_status()
    return extract_text_from_response(resp.json())

seed =(BASE_DIR / "seed.txt").read_text()
voice = (BASE_DIR / "voice.md").read_text()
craft = (BASE_DIR / "CRAFT.md").read_text()

# Extract voice Part 2 only (the novel-specific voice)
voice_lines = voice.split('\n')
part2_start = next(i for i, l in enumerate(voice_lines) if 'Part 2' in l)
voice_part2 = '\n'.join(voice_lines[part2_start:])

prompt = f"""Build a complete world bible for this novel. This is the WORLD.MD file --
the definitive reference for everything that EXISTS in this world. A writer should be able
to resolve any worldbuilding question from this document alone.

SEED CONCEPT:
{seed}

VOICE IDENTITY (the tone and register of this novel):
{voice_part2}

WORLDBUILDING REQUIREMENTS:
- History must create PRESENT-DAY TENSIONS that drive the plot (not just backdrop)
- Geography/setting must be specific and sensory (not generic)
- If the story has a power or rule system: include HARD RULES with COSTS and LIMITATIONS.
  Limitations must be at least as prominent as powers. Trace implications through society,
  economy, law, religion.
- Iceberg principle: imply more than you state
- Interconnection: pulling one thread should move everything
- Every rule should have a COST or LIMITATION alongside it

DETERMINE THE RIGHT SECTIONS for this story's needs. At minimum include:

## Setting & Geography
The specific locations this story requires. Physical layout. Sensory signatures for each.
Neighboring places. How geography shapes daily life and conflict.

## History & Timeline
Major events. Focus on events that create PRESENT-DAY tensions.
Include founding conditions, key turning points, recent events that matter to the plot.

## Power Systems (if applicable)
Hard rules, costs, limitations. Societal implications. What happens when you break them.

## Factions & Power Structure
Who holds power, who wants it, who's being crushed by it.
At least 3-4 factions or interest groups with opposing stakes.

## Cultural Details
Customs, taboos, festivals, food, clothing, daily rituals.
Things that make life feel SPECIFIC and LIVED-IN.

## Internal Consistency Rules
Hard constraints a writer must not violate. What's possible and what's not.

IMPORTANT:
- Be SPECIFIC. Name places, describe them, give them sensory signatures.
- Every rule should have a COST or LIMITATION stated alongside it.
- Include 2-3 facts per section that are unexplained, hinting at deeper systems.
- Facts should INTERCONNECT: the power structure shapes daily life, the geography
  shapes the culture, the history explains current faction conflicts.
- Write in clean, direct prose. No AI slop. No "rich tapestry." No "delving."
- The world should feel grounded and LIVED-IN. Think: what does breakfast smell like?
  What do children play? How do old people complain?
- Target ~3000-4000 words. Dense, not padded.
"""

print("Calling writer model...", file=sys.stderr)
result = call_writer(prompt)
(BASE_DIR / "world.md").write_text(result)
print(result)
