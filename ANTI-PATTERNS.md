# AI WRITING ANTI-PATTERNS

Patterns discovered through iterative evaluation of AI-generated novel
chapters. These are the specific failure modes that survive prompt
engineering and surface-level slop detection. They are structural, not
lexical -- you won't catch them with word lists.

This document supplements ANTI-SLOP.md (which covers word-level slop).

---

## 1. THE OVER-EXPLAIN

**The #1 problem.** The narrator restates what a scene already showed.

A character's hands shake. The dialogue goes silent. The scene lands.
Then the narrator adds: "He was afraid." Or worse: a full paragraph
analyzing what the shaking hands meant.

**Detection:** After every emotional beat, check: does the next
paragraph explain what just happened? If yes, cut it.

**Rule:** If a scene shows it, the narrator doesn't say it. Trust
the image, the gesture, the silence.

---

## 2. TRIADIC LISTING

AI defaults to groups of three: "X. Y. Z." or "X and Y and Z."

Sensory descriptions: "Linseed oil. Cold bronze. The faint char..."
Options: "He could go left. He could go right. He could stay."
Adjectives: "warm and clean and simple"

**Detection:** Search for three consecutive fragments or three items
joined by "and." More than 2 per chapter is a pattern.

**Fix:** Combine two items. Cut one. Use a different number. Two is
often stronger than three.

---

## 3. NEGATIVE-ASSERTION REPETITION

"He did not look back."
"He did not think about the room."
"He did not say what he meant."

Each one is fine. Five in a chapter is a tic.

**Rule:** Max 1 per chapter. Replace with: active alternatives
("The door stayed closed"), or just cut (let the absence speak).

---

## 4. CATALOGING-BY-THINKING

"He thought about X. He thought about Y. He thought about Z."

AI compresses reflection into a list of topics the character
considers. Real interiority is messier -- one thought bleeds into
another, gets interrupted, loops back.

**Fix:** Replace with: the thought itself as a fragment ("The two
years. The wrong-pitched bells."), a physical action, or dialogue.

---

## 5. THE SIMILE CRUTCH

"the way X did Y" -- used 4-8 times per chapter.

AI reaches for simile when it doesn't trust the image. Most of these
can be cut entirely. The image is already there.

**Rule:** Max 2 "the way" similes per chapter. If you need the
comparison, vary the construction. "Like" is fine. Direct metaphor
("his words were bronze -- heavy, functional") is better.

---

## 6. PARAGRAPH LENGTH UNIFORMITY

AI paragraphs cluster at 4-6 sentences, especially in middle
sections. The variation that appears at chapter openings and closings
flattens in the middle.

**Fix:** Deliberately include 1-2 sentence paragraphs for impact
and 6+ sentence paragraphs for building. Never 3+ consecutive
paragraphs of similar length.

---

## 7. PREDICTABLE EMOTIONAL ARCS

Beats arrive on schedule. If the outline says "curiosity → discovery
→ dread," the chapter delivers exactly that in exactly that order
with no deviation. Real chapters have moments that arrive early,
late, or sideways.

**Fix:** Include one moment per chapter that surprises: a character
saying the wrong thing, an emotion arriving before its trigger, a
beat that interrupts another beat.

---

## 8. REPETITIVE CHAPTER ENDINGS

AI finds a closing pattern and reuses it. In this novel: 4 chapters
ended with "Cass outside, listening to his father work."

**Rule:** No two chapters end with the same structural move. Each
ending belongs to THAT chapter specifically.

---

## 9. BALANCED ANTITHESIS IN DIALOGUE

"I'm not saying X. I'm saying Y."
"Not X, but Y."
"There's a difference."
"Those are different things."

AI loves this rhetorical formula. It sounds clever the first time.
By the third character using it, they all sound like the same person.

**Detection:** Check that no two characters share this sentence
structure. If multiple characters use it, they're not distinct.

---

## 10. DIALOGUE AS WRITTEN PROSE

Characters speak in complete, polished sentences. No one stumbles,
interrupts, trails off, or says something slightly wrong.

A 14-year-old does not speak in epigrams. A 60-year-old merchant
does not deliver thesis statements.

**Fix:** Dialogue should sound like speech. Include: false starts,
interruptions, trailing off, saying the wrong word, not finishing
a thought. At least one imperfect line per scene.

---

## 11. SCENE-SUMMARY IMBALANCE

AI defaults to summary when a scene would be more engaging. "The
morning passed" skips what could be a 200-word interaction that
reveals character.

**Rule:** 70%+ of each chapter should be in-scene (moment by moment,
with dialogue and action). Summary is for time compression only.

---

## 12. ONE EMOTIONAL TEMPERATURE

Not a sentence-level pattern but a chapter- or novel-level one.
Every scene is processed through the same register: ironic distance,
melancholy self-awareness, measured analytical calm. The narrator
never loses composure. The intellectual apparatus never fails.

This is the AI stability trap manifested as tone. The model finds
a working register and stays in it because deviation is risky.
Human writing has ruptures -- moments of genuine anger, fear, joy,
grief that bypass the narrator's usual processing.

**Detection:** Read the first and last paragraphs of every chapter.
If the emotional register is the same in both, the chapter is
monotone. Read the emotional peaks (fights, revelations, losses).
If they're processed through the same ironic/analytical distance as
everything else, the story is flat regardless of content.

**Fix:** At least one scene per 10,000 words where the dominant
register cracks. Short flat sentences. Physical detail only. No
digressions. The prose itself should register the emotional break
through a change in style, not just a change in subject matter.

---

## 13. THESIS-ABSORPTION

Every detail in the story connects to the argument. The bathmat
connects to questions of choice. The fork connects to identity.
The chopsticks connect to performance. Every observation serves
the theme. The pattern-matching is too thorough.

Real life contains details that don't connect. Real fiction contains
moments that resist thematic integration -- observations the story
can't explain, memories that arrive without justification, objects
that sit in the text and refuse to become symbols.

**Detection:** For each significant detail or digression, ask: does
this serve the thesis? If the answer is yes for every single one,
the story has become an essay with characters.

**Fix:** Add details that resist. A sensory detail that doesn't
connect. A memory that arrives without thematic justification. A
moment of comedy unrelated to the premise. A character doing
something the text doesn't interpret. Distribute these unevenly --
not one per chapter, but clustered in some places and absent in
others. See Phase 2.5 (Organic Finishing) in program.md.

---

## 14. THE TYPE-DESCRIPTION FORMULA

The single most common AI character-description tell. The pattern:
"the [expression/posture/confidence/satisfaction] of [someone/a man/
a person] who [lengthy clause describing the type]."

Examples:
  "the expression of a man who had been disappointed by rooms
    full of people before"
  "the confidence of someone who had done all the reading and
    wanted the room to know it"
  "the slightly aggressive cheerfulness of someone who had been
    doing this since before dawn"
  "the quiet satisfaction of a man who had planned this exact
    outcome"

This construction turns characters into instances of types. Instead
of showing a disappointed teacher, it shows "the expression of a
man who had been disappointed." The character is depersonalized
into a sociological category. The reader sees a type, not a person.

**Detection:** Search for "the [noun] of [someone/a man/a woman/
a person] who." More than 2 per chapter is a pattern.

**Fix:** Show the specific physical detail instead. Not "the
expression of a man who had been disappointed" but: the way his
mouth thinned when he looked at the board. Not "the confidence of
someone who had done all the reading" but: she set the stack down
like it was a hand of cards she knew she'd win with. Specifics,
not categories.

---

## 15. SCENE-STRUCTURE REPETITION

The paragraph-template problem (§1) applied at scene scale. Every
scene follows the same beat sequence: arrive at location → observe
the environment → interact with someone → reflect on the
interaction → leave.

**Detection:** Summarize each scene in a chapter as a sequence of
beats (arrive, observe, interact, reflect, leave). If three or
more scenes share the same sequence, the chapter has structural
monotone.

**Fix:** Vary scene structures. Some scenes should start mid-
conversation. Some should end before resolution. Some should skip
the observation phase and open on dialogue. Some should be pure
interiority with no interaction. The shape of a scene should be
unpredictable.

---

## 16. UNIVERSAL COMPETENCE

The three-slider character model (CRAFT.md §2) asks for at least
two sliders high per character. But when EVERY character in the
cast is high-competence, the world becomes a seminar: a room of
smart people being smart at each other. Nobody fumbles. Nobody
misreads a situation. Nobody is bad at their job in a way that
isn't plot-functional (a character who makes one calibrated mistake
to demonstrate the system doesn't count).

**Fix:** At least one character should be incompetent in a way
that is not a plot device. At least one character should say
something genuinely stupid. At least one interaction should
feature someone who has no idea what's happening and doesn't
care. These people exist in every professional milieu, and their
absence is a tell.

---

## 17. MAGIC SYSTEM RE-EXPLANATION

Related to the Over-Explain (§1) but specific to speculative
fiction. The first time a magic/tech/speculative mechanic triggers,
it's described in full. The second time, it's described in full
again. The third time, again.

AI defaults to re-explaining mechanics because it can't assume
the reader remembers. Human writers establish the mechanic once,
then reference it in shorthand.

**Rule:** Full sensory description of a mechanic once. After that,
a brief physical cue (a word, a gesture, a sensation) is sufficient.
If the character's jaw tightens when they detect a lie, the reader
needs the full explanation once. After that, "his jaw tightened"
is enough.

---

## 18. SENTENCE-LEVEL TICS AT CHAPTER DENSITY

Several patterns that are individually valid become anti-patterns at
AI density. These are covered with detection thresholds in
ANTI-SLOP.md (see: paired em-dash parentheticals, "which was"
recontextualization machine, deflationary sentence endings). What
makes them ANTI-PATTERNS rather than just slop is that they compound
across a chapter: a reader won't notice one deflationary ending but
will start skipping final clauses when every paragraph deflates.

The chapter-level check: read only the last sentence of every
paragraph in a chapter. If they share a pattern (deflation, "which
was" reframe, em-dash interruption), the chapter has a structural
tic regardless of whether any individual sentence is problematic.

---

## EVALUATION NOTES

These patterns are invisible to standard slop detection (word lists,
regex). They require either:

1. **Adversarial editing** -- ask a judge to cut 500 words and
   classify what it cuts. OVER-EXPLAIN type dominates every time.

2. **Comparative ranking** -- head-to-head matchups between chapters
   force discrimination the judge can't avoid. Produces a true rank
   order. Swiss-style Elo tournament works well with 4 rounds.

3. **Sentence-level grading** -- flag every sentence as STRONG /
   FINE / WEAK / CUT. The distribution matters more than the average.

Standard 1-10 scoring collapses to a 2-point band regardless of
rubric calibration. Avoid absolute scoring for revision work.
