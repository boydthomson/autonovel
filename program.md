# autonovel

Autonomous fantasy novel writing pipeline. The agent writes and refines
a novel across 5 co-evolving layers, guided by automated evaluation.

## Required Reading

Before ANY writing or evaluation, the agent must internalize:
  - `voice.md` -- Part 1 (guardrails) is permanent. Part 2 is per-novel.
  - `CRAFT.md` -- Operationalizable frameworks for plot, character,
    worldbuilding, foreshadowing, prose quality. This is the education.
  - `ANTI-SLOP.md` -- Full reference on AI writing tells.

## The Layer Stack

```
  Layer 5:  voice.md          -- HOW we write (style, tone, vocabulary)
  Layer 4:  world.md          -- WHAT exists (lore, magic, geography, history)
  Layer 3:  characters.md     -- WHO acts (registry, arcs, relationships)
  Layer 2:  outline.md        -- WHAT HAPPENS (beats, foreshadowing map)
  Layer 1:  chapters/ch_NN.md -- THE ACTUAL PROSE (one file per chapter)
  Cross-cutting: canon.md     -- WHAT IS TRUE (hard facts, consistency DB)
```

## Setup

1. **Tag the run**: Create branch `autonovel/<tag>` from master.
2. **Read all layer files** for full context.
3. **Verify state.json** shows phase=foundation.
4. **Confirm and go**.

## Phase 1: Foundation (no prose yet)

LOOP until foundation_score > 7.5 AND lore_score > 7.0:
  1. Run `python evaluate.py --phase=foundation`
  2. Identify the weakest layer/dimension from the eval output
  3. Expand or revise that layer's document
  4. When adding facts to world.md or characters.md, ALSO log them
     in canon.md as canonical entries
  5. git commit with description of what changed
  6. Re-evaluate
  7. If score improved -> keep. If worse -> git reset --hard HEAD~1, discard.
  8. Log to results.tsv

Lore priorities (the foundation evaluator weights these at 40%):
  - Magic system: hard rules, costs, limitations, societal implications
  - History: timeline that creates PRESENT-DAY TENSIONS, not decoration
  - Geography/culture: distinct locations, specific customs and taboos
  - Interconnection: magic affects politics, history explains factions,
    geography shapes culture. Pulling one thread should move everything.
  - Iceberg depth: more implied than stated. Hints at deeper systems.

Cross-layer consistency checks on every iteration:
  - Outline references only lore that exists in world.md
  - Character arcs align with outline beats
  - Character abilities match magic system rules
  - Foreshadowing ledger balances (every plant has a payoff)
  - Voice exemplars exist and are non-generic
  - Canon.md is populated with all hard facts from world.md and
    characters.md

Exit: When foundation_score > 7.5 AND lore_score > 7.0, update
state.json phase to "drafting".

## Phase 2: First Draft (sequential chapter writing)

FOR each chapter in outline order:
  LOOP until chapter_score > 6.0 or attempts > 5:
    1. Load context: voice.md + world.md + characters.md
       + this chapter's outline entry
       + previous chapter's last ~1000 words
       + next chapter's outline (for continuity)
    2. Write chapters/ch_NN.md
    3. Run `python evaluate.py --chapter=NN`
    4. Keep/discard based on score
    5. If writing reveals a lore gap or inconsistency, log a debt
       in state.json
    6. After evaluation, check new_canon_entries in the eval output.
       Add any new facts established in the chapter to canon.md.
    7. Log to results.tsv
    8. git commit

Canon grows during drafting. Every chapter establishes facts (a
character reveals something, a place is described, an event occurs).
These get logged in canon.md so future chapters stay consistent.

After all chapters drafted, update state.json phase to "revision".

## Phase 2.5: Organic Finishing

After revision stabilizes (no chapter scores dropping, no major
structural issues), run an organic finishing pass. This is not
revision -- it is the addition of details that resist the story's
own logic. The purpose is to make the story exceed its argument.

The agent rereads the full manuscript and adds, unevenly distributed:

  - **Unexplained sensory details**: A smell, a sound, a physical
    sensation that doesn't connect to the thesis. A character
    discovering what they smell like. The texture of a specific
    fabric. A sound from another room that's never identified.

  - **Sideways memories**: A parent, a childhood moment, an image
    from the past that surfaces without thematic justification.
    Not a memory that echoes the theme -- a memory that arrives
    because consciousness is associative and does not respect
    narrative architecture.

  - **Physical comedy or absurdity**: A moment that's just funny.
    Not wry, not ironic, not thematically resonant. Funny. A man
    getting his head through a sweater's arm hole. A cat choosing
    one person over another for no discernible reason.

  - **Unexplained character behavior**: Something a character does
    that the text doesn't interpret. Push-ups nobody suggested.
    A grocery list with different pen pressure. A melody hummed
    from nowhere that no app can identify. A security guard
    sleeping standing up.

  - **The unresolvable recurring detail**: A detail that appears
    two or three times, changes slightly each time, and never
    explains itself. A melody that acquires direction but never
    resolves. An object that migrates around the apartment.

Rules:
  - Distribute unevenly. Not one per chapter. Cluster some, skip others.
  - Never explain what these details mean. They mean nothing. They are
    there because the world contains more than the story's argument.
  - If a detail starts to feel thematic during revision, cut it and
    replace with something that doesn't connect. The whole point is
    resistance to thematic integration.

## Phase 3: Revision (infinite refinement)

LOOP FOREVER:
  1. Run `python evaluate.py --full`
  2. Identify weakest point:
     - Lowest-scoring chapter
     - Unresolved foreshadowing thread
     - Consistency violation
     - Voice deviation
     - Pacing problem
     - Pending debt from state.json
  3. Decide action:
     a. Revise a weak chapter
     b. Fix a consistency violation (may touch lore + chapters)
     c. Strengthen a foreshadowing thread (plant + payoff chapters)
     d. Refine voice in the most-deviant chapter
     e. Adjust pacing (split/merge chapters)
     f. Update planning docs to reflect reality
  4. Make the change(s)
  5. git commit
  6. Re-evaluate affected scope
  7. Keep/discard
  8. Log to results.tsv

### Propagation Rules

When a layer changes, check downstream:
  - voice.md changes    -> re-evaluate ALL chapters for voice adherence
  - world.md changes    -> check all chapters for lore consistency
  - characters.md changes -> check affected chapters for dialogue/behavior
  - outline.md changes  -> re-evaluate affected chapters for beat coverage
  - chapter changes     -> check foreshadowing ledger, check adjacent chapters

When writing reveals upstream issues, log a debt in state.json:
```json
{"trigger": "ch_07: magic system needs teleportation rules",
 "affected": ["world.md", "ch_03.md"],
 "status": "pending"}
```

## Context Window Strategy

ALWAYS loaded (~8k tokens):
  - voice.md (full)
  - characters.md (full)
  - world.md (key rules summary)
  - outline.md (full)
  - foreshadowing ledger (full)

PER TASK (~20-30k tokens):
  - Target chapter(s)
  - Adjacent chapters (prev + next)
  - Chapters connected by foreshadowing threads

## Evaluation Dimensions

Foundation: world_depth, character_depth, outline_completeness,
  foreshadowing_balance, internal_consistency

Chapter: voice_adherence, beat_coverage, character_voice,
  plants_seeded, prose_quality, continuity

Full novel: all above + arc_completion, pacing_curve,
  theme_coherence, foreshadowing_resolution, overall_engagement

## Prose Critique (supplement to numerical scoring)

Numerical evaluation (foundation_score, chapter_score) is useful for
automated loops but misses the most actionable insights. After Phase 2
and after every major revision cycle, generate a structured prose
critique covering:

  - **Emotional temperature**: Does the register stay at one level
    throughout? Identify the dominant mode. Identify any breaks. If
    there are no breaks, flag this as the #1 revision priority.
  - **Character opacity**: For each supporting character, apply the
    opacity test from CRAFT.md §2. List which characters pass and
    which are functions.
  - **Passivity audit**: Does the protagonist make at least one
    unforced decision? List all decisions and classify: forced by
    circumstance, or genuinely chosen.
  - **Surprise audit**: Does the story contain at least one
    consequence its own framework can't absorb? If every event
    confirms the thesis, the story is predictable.
  - **Register variation**: Does the prose have more than one mode?
    Identify the dominant register and any counter-registers. If
    there's only one, flag it.
  - **Dramatization audit**: List the 3 most consequential dramatic
    events. Are they scenes (with dialogue, action, physical detail)
    or summaries? Any summary should become a scene.

For literary/contemporary fiction, also apply the evaluation rubric
in CRAFT.md §9 (domain insight danger level, thesis-resistance,
structural model identification).

This critique should be a prose document, not a score. The output
is a list of specific, addressable problems, not a number.

## Continuity Protocol

After every structural revision pass, verify:

  - **Character ages and dates**: Birth years, ages mentioned in
    text, and timeline arithmetic must agree. If a character is
    "sixty-one" and "born 1963," the story year is 2024.
  - **Duration arithmetic**: Day counts should add to week/month
    references. "Day fifty-three" and "three months" in the same
    context is a contradiction.
  - **Object consistency**: Colors, brands, locations of recurring
    objects must not drift. The bathmat is blue everywhere or nowhere.
  - **Spatial/layout references**: If a room arrangement changes
    (e.g., a retrospective layout is reorganized), ALL references
    to room order must update. Grep for "first room," "last room,"
    "final room," room numbers.
  - **Biographical details**: Gallery names, school years, artwork
    titles and dates, character relationships mentioned in multiple
    places must not contradict.
  - **Artwork consistency**: If "Correspondence (Two Chairs)" is
    dated 1998 in one passage, it is 1998 everywhere.

Run this as a mechanical check (grep + manual review) after any
revision that touches timeline, layout, or character history.

## The Stability Trap (CRITICAL)

AI favours stability over change. This kills fiction. The full
analysis and concrete countermeasure protocols are in CRAFT.md §7.
Read it. The short version:

- Characters must end TRULY different from how they began.
- Let bad things stay bad. Not everything gets fixed.
- At least one register break per 10,000 words (CRAFT.md §7).
- At least one unforced protagonist decision (CRAFT.md §7).
- At least one scene that breaks the story's own rules (CRAFT.md §7).

## Foundation Phase: Voice Discovery

During foundation, the agent must DISCOVER the voice for this novel:
1. Read the world concept and initial ideas
2. Write 5 trial passages in different registers (mythic, spare,
   warm, cold, whimsical, etc.)
3. Evaluate which register best serves THIS story's world and tone
4. Select the best, refine it, write exemplar and anti-exemplar passages
5. Fill in voice.md Part 2 with the discovered voice

The voice should feel like it BELONGS in the world (Le Guin's insight:
in fantasy, the language creates the world, not just describes it).

## Foundation Phase: Character Framework

Every POV character must have documented before drafting begins:
- Wound/Want/Need/Lie chain (see CRAFT.md)
- Three-slider profile (proactivity, likability, competence)
- Arc type (positive, negative, or flat)
- Speech pattern distinct from every other character
- At least one secret the reader doesn't learn immediately

## Foundation Phase: Plot Framework

For genre fiction, the outline must demonstrate:
- Save the Cat beats at roughly correct percentage marks
- Try-fail cycle types planned for each chapter (yes-but / no-and)
- Foreshadowing ledger with every plant and its planned payoff
- MICE threads identified and planned to close in reverse order
- Escalating stakes through Act 2

For literary fiction or non-beat-sheet structures, identify the
structural model explicitly (see CRAFT.md §9: question structure,
accretion structure, recursive structure). If you can't name the
structure, the story may lack one rather than transcend one.

## Rules

- **NEVER STOP** during a phase. Keep looping until interrupted.
- **Simpler is better**: Don't add complexity for marginal gains.
- **Forward progress over perfection**: In Phase 2, a 6.0 chapter
  is good enough. Phase 3 is for polish.
- **Log everything**: Every experiment goes in results.tsv.
- **Different judge**: Evaluation model should differ from writing model
  when possible to avoid self-congratulation bias.
- **Fight stability**: Actively push toward transformation, cost, and
  genuine consequence. See "The Stability Trap" above.
- **Specificity over abstraction**: "a jay" not "a bird." "lupine" not
  "flowers." "the smell of hot iron" not "a metallic scent."
- **Earn every metaphor**: Metaphors come from character experience.
  A blacksmith thinks in terms of heat and metal. A sailor in tides.
