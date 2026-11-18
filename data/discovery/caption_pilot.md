# Captions read against their pictures: the rules and the bars of a pilot

Status on 2026-11-17, 16:40: **gate 2 missed; the pilot has ended, with no meaning of the project's own.**

| Gate | Bar | Result |
|---|---|---|
| 1. Enough material | at least 20 known items and 10 open spellings | **Met.** 56 of the 87 texts are captions with a picture held: 65 known items and 71 open spellings |
| 2. The picture helps on known words | right picture at least 0.50, and at least 0.20 above the wrong picture, p < 0.05 | **Missed.** Right picture 0.244, wrong picture 0.194: 5 points, p = 0.156 |
| 3. The open words | read only if gate 2 is met | **Not run** |

The rules and bars (sections 1 to 5) were written and pushed in 1f8c80e, before the material was counted and
before any reader saw a picture. They have not changed since. The results are in section 6.

## 1. What was asked

Mike asked, on 2026-11-17, whether there are any other languages we should cross-check against, or other
scientific methods. The answer was that no other language is worth a test.
- The ten related languages show no signal beyond the 20 words the sound rules were built from
  ([cognates_rules.md](cognates_rules.md)).
- Nile Nubian missed with whole dictionaries ([outside_evidence.md](outside_evidence.md)).
- Egyptian, Demotic, Greek, Latin and Coptic are already mined ([lead 4](../leads/04-foreign-renderings.md)).

One method was untried: captions read against the pictures beside them, the way the pictured objects in Linear B
helped Ventris. Asked "Should I run the caption pilot on Lepsius's plates?", he answered: "Yes, run the pilot".

The offer he accepted said what the pilot would do:
1. Take the 87 royal and temple texts of the map's 548 texts (Naga, Meroë, Philae).
2. Pair them with [Lepsius's plates](https://edoc3.bibliothek.uni-halle.de/lepsius/start.html), which draw these
   reliefs with their captions.
3. First count how many open words stand beside a picture.
4. Then test on caption words whose meaning is known, with the bar set beforehand.

The offer also stated that the odds are low, because most captions are names and known formulas, and that the
cost would be about 3 to 6 million tokens plus downloading the plates.

## 2. The question

Does the picture beside a caption tell a reader what a word of the caption means, more often than the caption's
own text and a reader's general knowledge do? If it does, on words whose meaning is known, the same readers are
then asked about the open words of the captions.

## 3. The material

1. **The pictures.**
   - The 75 plates of Lepsius, *Denkmäler*, section V, "Aethiopische Denkmäler", fetched on 2026-11-17 from the
     University and State Library of Halle (public domain; local, `data/sources/lepsius-ld5/`).
   - The plates of Griffith's *Meroitic Inscriptions* I (1911) and II (1912), already held
     (`data/sources/griffith-mi1/`, `griffith-mi2/`, public domain). Griffith checked Lepsius's drawings
     against photographs and the originals, and his second volume draws the figures of the Meroitic chamber at
     Philae with their texts.
   - Garstang's *Meroë* (1911), already held (`data/sources/meroe1911/`), where its photographs show a scene.
2. **A caption** is a text written beside a figure or a scene in a relief or a painting, whose picture is drawn or
   photographed in one of these plates. A stela or a wall text that stands apart from any figure is not a
   caption.
3. **The words.** The map is the map as it stands (`src/themap.py`, with its seven layers), on the 548 texts of
   `data/discovery/map_texts.json`.
   - **A known item** is a word of a caption at the level `meaning`.
   - **An open item** is a word of a caption at any level other than `meaning`, `grammar`, `name`, `number` or
     `lost`.
   - **Excluded:** endings and particles (`grammar`), names, numerals and words with a lost sign.
   - **The cap:** an item is one word in one caption, and a spelling counts at most three times (its first three
     captions by REM number), so that a frequent word cannot carry a gate alone.
4. **An inventory**, made by one agent before any reader starts, gives for each of the 87 texts:
   - whether it is a caption;
   - which plate holds its picture;
   - the box to cut the scene from the plate;
   - what kind of figure the caption stands beside (god, goddess, king, queen, prince, official, priest,
     animal, object, or scene).

   The kind is for drawing the wrong pictures (section 4) and is never shown to a reader.

## 4. The rules and the bars, set before anything ran

### Gate 1: is there enough material?

Counted from the inventory.

**Bar:** at least 20 known items, and at least 10 different open spellings, in captions beside a picture that is
held.

If it is missed, the pilot stops here as too small to decide, and the count is written up.

### Gate 2: does the picture help on words whose meaning is known?

1. **What a reader sees, for each item:**
   - the cut picture of its scene;
   - the caption in transliteration, with the item's own word hidden as `[?]`, so that a reader who knows the
     lexicon cannot look the spelling up;
   - every other word glossed as the map glosses it (names marked as names, open words as "unknown").
2. **What a reader is told:** use only the picture and the caption given, open no other file, and search
   nothing.
3. **What a reader answers, for each item:**
   - one best meaning, in at most five words;
   - the element of the picture it points to, or "none".
4. **The two conditions.** In the right-picture condition, two readers see the item's own scene. In the
   wrong-picture condition, two other readers see the same caption with a scene cut for another caption.
   - The wrong scene is drawn by lot, seed 17, among captions whose figure is of another kind, at the same
     site when one exists and at any site otherwise.
   - No reader sees both conditions of one caption.
   - Every reader is a fresh agent on Opus 5.5.
5. **The judges.** Two fresh judges, who are not told the condition, score each answer against the map's gloss:
   1 for right, 0.5 for partly right, 0 for wrong. An item's score in a condition is the mean of its two
   readers, averaged over the two judges. The judges' agreement is reported.
6. **Bar (all four):**
   1. at least 20 known items are scored;
   2. the right-picture mean is at least 0.50;
   3. the right-picture mean is at least 0.20 above the wrong-picture mean;
   4. the difference beats chance: a one-sided sign-flip test over spellings (the items of one spelling flip
      together), 10,000 draws, seed 17, p < 0.05.

If gate 2 is missed, the open items are not read, and the pilot ends with this page's results.

### Gate 3: the open words (only if gate 2 is met)

1. **The readers.** Each open item is read in the same two conditions by four new readers, with the same packs
   and instructions.
2. **When a proposal stands:**
   - both right-picture readers give the same meaning (the two judges decide "the same");
   - neither wrong-picture reader gives it.
3. **Every standing proposal is then checked:**
   1. against the sources in hand: Rilly's lexicon of 2003 with its listed proposals, Millet 2005, Lipiński
      2011, Rilly 2021, Griffith 1911, 1912 and 1922, and FHN. A proposal a source states is that scholar's,
      and counts as a confirmation of the method;
   2. where the spelling stands in other texts of corpus_v6, by the blind choice of step G6: two checkers pick
      among the proposal and three decoys, and the proposal must be picked by both.
4. **What it takes to count.** A proposal that no source states and that passes the check is a candidate "own
   meaning". It counts on the scoreboard only after an independent check and the review, as the reporting
   skill's row "Our own meanings" requires (`.claude/skills/reporting/SKILL.md`, section 3).

### Cost

The pilot stops and reports if its subagent tokens pass 6 million, the top of the cost quoted to Mike.

## 5. What would not count

1. A meaning a scholar already gives (it confirms the method; it adds nothing).
2. A name, or a word read as part of a name.
3. The kind of a word without its meaning: "a title" is not a meaning, but "a priest who carries the censer"
   would be.
4. A meaning the picture shows but only one right-picture reader gives.

## 6. Results (2026-11-17)

### Gate 1: met

An agent made the inventory before any reader started. It went through the 87 texts, using Griffith's catalogues to
see where each one stands, and cut each caption's scene out of its plate with all writing painted white. Every cut
was checked by eye for leftover signs.

- **Captions:** 56 of the 87 texts.
  - 40 are drawn in Lepsius's section V (Naga, the Meroë chapels, Barkal).
  - 14 are drawn on Griffith's plate of the Meroitic chamber at Philae (*Meroitic Inscriptions* II, pl. XVIII).
  - 2 are photographed in Garstang's *Meroë*.
- **Not captions:** the other 31, each recorded with its reason. Among them are pieces of one stela, statue bases,
  graffiti, bands on columns, the long texts of Kalabsha (REM 0094), Hamadab (REM 1003) and Philae (REM 0101), and
  two texts whose picture we do not hold.
- **The figures beside the captions:** 18 gods, 4 goddesses, 9 kings, 5 queens, 16 officials, 1 priest and 3 whole
  scenes.
- **The count:** 65 known items (42 spellings) and 83 open items (71 spellings), against bars of 20 and 10.

### Gate 2: missed

All 65 known items were read with their own picture and with a wrong one, two readers in each condition: 260
answers in all. The two judges gave the same score to 97.7% of them (Cohen's kappa 0.945).

| | Right picture | Wrong picture | Gain | p |
|---|---|---|---|---|
| All 65 items | 0.244 | 0.194 | 0.050 | 0.156 |
| Lepsius's drawings (27 items) | 0.227 | 0.222 | 0.005 | |
| Griffith's Philae chamber (32 items) | 0.281 | 0.176 | 0.105 | |
| Garstang's photographs (6 items) | 0.125 | 0.167 | −0.042 | |

Only the first row is the gate; the other rows were split out afterwards to see where the gain came from.

- **Most items do not move:** 39 of the 65 score the same with either picture. 29 of those are wrong in both.
- **17 items score higher with the right picture, and 9 lower.** The gains are mostly titles of the officials at
  Philae. For example, `atolis` ("of the water", in "general of the water") was read as "of the water" with its own
  picture and "of the land (army)" with a wrong one.
- **A picture also misled.** In one royal scene, the right picture led both readers to read `qore` ("ruler") as
  "god", while the wrong picture gave "king".

**What it means.** A relief shows who a figure is (a god, a king, a queen, an official), and the names in the
caption already say that. What the caption words that need a meaning do, as titles, epithets and verbs of blessing,
is not something a drawing shows. Even with the true picture, readers got a quarter of the known words right. This
is the result of the six digs of 11 November in another form: the surroundings of a word give its kind, rarely its
meaning. By the rule set in section 4, the 83 open items were not read.

### How the run kept to the rules, and where it differed

1. **The code was reviewed before the gate ran** (full review, 328,434 tokens). The review found three ways the
   first packs would have spoiled gate 2, and fixed them in eb56ebb:
   - a caption with several items came back once per item, so one copy showed the word hidden in another;
   - the pack files named their condition;
   - the picture files were named after their text.

   Since that fix, each pack is read by one fresh agent; no pack holds two items that would give each other away;
   pack files carry only the items; and pictures have names drawn by lot. Readers "A" and "B" (right picture) and
   "C" and "D" (wrong picture) are therefore each 12 packs of 5 or 6 items, read by 48 agents in all. That is what
   section 4 asks ("every reader is a fresh agent"; "no reader sees both conditions of one caption").
2. **One pack was read twice.** One reader of pack 35 gave a six-word meaning, past the five-word limit. Its answers
   were set aside unread, and a fresh agent read the pack again with the same instruction plus "count them: five
   is the limit".
3. **A known limit, left as the rules have it.** In 4 of the 65 items, a variant spelling of the hidden word stands
   in the same caption with the same gloss. Both conditions see it, so it can raise both scores but cannot make a
   gain.
4. **The readers' instruction** said the pictures were cut from "a drawing or photograph of a relief or carved
   object", since two of them are photographs. The judges were told to ignore endings written as "+l" in a gloss.
   Both instructions are kept with the local files (`data/sources/captions/`).

### Cost

4,511,343 subagent tokens in all, under the 6 million set in section 4:

| Step | Tokens |
|---|---|
| The inventory | 548,503 |
| The review of the code | 328,434 |
| 49 readers' packs | 3,459,356 |
| The two judges | 175,050 |

The review of this write-up is extra. The plates came from Halle (29 MB, public domain).

### Files

- **Public:** `src/captions.py`, `tests/test_captions.py`, and the counts in
  [`caption_pilot_figures.json`](caption_pilot_figures.json).
- **Local** (`data/sources/captions/`): the inventory, the cut pictures, the packs and their key, the readers'
  answers, the judges' scores and the item scores. They hold the map's glosses, which are not public.
