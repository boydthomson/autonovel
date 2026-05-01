# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
cp .env.example .env    # Add your API keys
uv sync                  # Install dependencies
```

Required: `ANTHROPIC_API_KEY`. Optional: `FAL_KEY` (cover art), `ELEVENLABS_API_KEY` (audiobook).

Model env vars: `AUTONOVEL_WRITER_MODEL`, `AUTONOVEL_JUDGE_MODEL`, `AUTONOVEL_REVIEW_MODEL`.

## Running the Pipeline

```bash
uv run python seed.py                               # Generate seed concepts → seed.txt
uv run python run_pipeline.py --from-scratch        # Full pipeline from seed.txt
uv run python run_pipeline.py --phase foundation    # One phase only
uv run python run_pipeline.py --phase drafting
uv run python run_pipeline.py --phase revision
uv run python run_pipeline.py --phase export
uv run python run_pipeline.py --max-cycles 4        # Limit revision cycles
```

## Running Individual Tools

```bash
uv run python evaluate.py --phase=foundation   # Score planning docs
uv run python evaluate.py --chapter=5          # Score chapter 5
uv run python evaluate.py --full               # Score entire novel

uv run python draft_chapter.py 3               # Draft chapter 3
uv run python adversarial_edit.py all          # Cut analysis across all chapters
uv run python apply_cuts.py all --types OVER-EXPLAIN REDUNDANT --min-fat 15
uv run python reader_panel.py                  # 4-persona novel evaluation
uv run python review.py --output reviews.md    # Opus dual-persona review
uv run python review.py --parse                # Parse review into actionable items
uv run python gen_brief.py --auto              # Auto-generate revision brief
uv run python gen_revision.py 5 briefs/ch05_auto.md  # Rewrite chapter from brief
```

## Architecture

The pipeline is **branch-per-novel**: `master` holds the reusable framework; each novel lives on its own branch (e.g., `autonovel/bells`).

### Five Co-Evolving Layers (per novel branch)

```
voice.md       — HOW we write (guardrails + discovered voice)
world.md       — WHAT exists (world bible, magic system, geography)
characters.md  — WHO acts (wound/want/need/lie, speech patterns)
outline.md     — WHAT HAPPENS (beats, foreshadowing ledger)
chapters/      — THE ACTUAL PROSE (ch_01.md ... ch_NN.md)
canon.md       — WHAT IS TRUE (cross-cutting hard facts database)
```

Changes propagate both directions: lore change → outline → chapter revision; writing reveals gap → update lore → check downstream. `state.json` tracks propagation debts.

### Pipeline Phases

**Phase 1 — Foundation**: Loop `gen_world.py → gen_characters.py → gen_outline.py → gen_outline_part2.py → gen_canon.py → voice_fingerprint.py → evaluate.py --phase=foundation`. Keep if score improved, `git reset --hard HEAD` if not. Exit at `foundation_score > 7.5`.

**Phase 2 — Drafting**: Sequential per-chapter loop via `draft_chapter.py` + `evaluate.py --chapter=N`. Keep if `score > 6.0`, retry up to 5 times.

**Phase 3a — Automated Revision**: `adversarial_edit.py → apply_cuts.py → reader_panel.py → gen_brief.py → gen_revision.py`. Plateau detection stops at `Δ < 0.3` across 2 cycles (min 3, max 6 cycles).

**Phase 3b — Opus Review Loop**: Full manuscript to `claude-opus-4-*` with dual-persona review (literary critic + professor of fiction). Stop when `≥4★` with no major items, or `>50%` of items are qualified hedges. Max 4 rounds.

**Phase 4 — Export**: `build_arc_summary.py → build_outline.py → manuscript.md → typeset/build_tex.py → tectonic novel.tex`.

### State Tracking

`state.json` tracks current phase, scores, chapter counts. `results.tsv` logs every keep/discard decision with git hash, score, and word count.

### Two Quality Immune Systems

1. **Mechanical** (`evaluate.py`, no LLM): regex for ~50 banned AI-tell words, fiction clichés, show-don't-tell violations, sentence uniformity.
2. **LLM Judge** (separate model from writer): prose quality, voice adherence, character distinctiveness, beat coverage.

The writer model and judge model are intentionally different to avoid self-congratulation.

### Git Strategy

`run_pipeline.py` makes a commit for every keep decision and `git reset --hard HEAD` for every discard. The git log is the experiment record. `results.tsv` mirrors it in tabular form.

### Key Thresholds (in run_pipeline.py)

- `FOUNDATION_THRESHOLD = 7.5` — exit foundation loop
- `CHAPTER_THRESHOLD = 6.0` — accept a drafted chapter
- `PLATEAU_DELTA = 0.3` — stop revision when improvement < this
- `MIN_REVISION_CYCLES = 3`, `MAX_REVISION_CYCLES = 6`

### Typesetting

`typeset/novel.tex` — EB Garamond, trade paperback (6×9"). `typeset/build_tex.py` converts `chapters/*.md` to `chapters_content.tex`. Build with `tectonic typeset/novel.tex`.

### Common Pitfalls

- Over-compressing chapters below 1800 words makes them the new weakest; sweet spot is 2200–3000w
- `gen_revision.py` adds ~30% more words than briefed (a 3200w target → 3800–4200w output)
- OVER-EXPLAIN (~32% of adversarial cuts) and REDUNDANT (~26%) are the dominant AI patterns — cut aggressively
- Pacing score ~7 may be a structural ceiling for LLM-evaluated novels; stop chasing it after 2 rotation cycles
- The beta header `anthropic-beta: context-1m-2025-08-07` is used by all tools for extended context
