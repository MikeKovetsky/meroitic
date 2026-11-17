# Evidence from outside the texts: three tracks, their rules and their bars

Status on 2026-11-17, 07:00: **two of the three tracks are counted; no meaning of the project's own.**

| Track | Gate | Result |
|---|---|---|
| A. Nubian dictionaries | A1: related words beat a shuffle | **Not run yet.** All 340 dictionary pages are typed and 34 typed twice; the script is reviewed and its bar chosen |
| B. The Kushite kings' Egyptian texts as frames | B: 80% right, 30 points over decoys | **Missed.** With the frames 7 of 26 hidden words right (26.9%), without them 5 of 38 (13.2%) |
| C. Names cut into parts | C1: parts recur in unseen names | **Met.** 62.6% of held-back names split into parts, 15.8% of shuffled ones |
| | C2: readers tell a part's kind | **Too small to decide.** The readers called 237 of 260 parts unclear |

This page set the rules and the bars of the three paths of [`NEXT_STEPS.md`](../../NEXT_STEPS.md), section H,
before any agent was started; the rules added later each say when, and every one came before its gate ran. The
results stand below each track; section 6 says what is left.

## 1. What was asked

Mike, 2026-11-16, in the evening: "read the latest progress and doc. design the best next steps with subagents we can
launch in parallel". The design put to him was three tracks, each from sources already on disk, each stopping at
a blind gate on known words before it touches an open word. Asked "Should I launch the three tracks now?", he
answered: "Yes, launch all".

The requirements, in the words of the design he answered:

1. Track A: typists and second readers type the Nubian–German dictionaries of Reinisch 1879 and Lepsius 1880.
2. Track A's gate: on the known words that are no loan and were not used to build the sound laws, the Nubian
   word of the same meaning must beat 2,000 shuffles (p < 0.05). Then, blind end to end, 80% of the meanings
   given must be right and at most 10% of trap words may get one.
3. Track B: agents build frames from the Kushite kings' Egyptian texts in *Fontes Historiae Nubiorum* I and II;
   aligners read the royal and temple texts against them; judges score.
4. Track B's gate: with known words hidden, where both aligners agree 80% must be right on at least 10 words,
   and 30 points above frames dealt by lot.
5. Track C: a script splits the personal names into recurring parts; agents check them and compare with
   Egyptian and Nubian naming.
6. Track C's gate: at least 80% of the known parts (`mlo`, `lẖ`, the gods' names) must come out as parts, and as
   what they are.
7. Each gate is committed before the first agent of its track.

**Two requirements are not built as worded,** and both are told to Mike with the launch (sections 3 and 4 say
why): the comparison of requirement 4 is counted with decoys, not with frames dealt by lot, and the first half
of requirement 6 is a count against made-up names, because only about seven known parts stand in five or more of
the held-back names.

**Both are waived by Mike,** in writing, before any gate was run: asked on 2026-11-16 "Do you waive the original
wording of the two changed gates (B and C)?", he answered at 22:27: "Yes, waive both".

What none of the three tracks can do alone: call a meaning the project's own. A proposal that passes a gate
still has to be searched for in the sources in hand (a meaning a source states is the scholar's), to pass an
independent check and the review ([the reporting rules](../../.claude/skills/reporting/SKILL.md), "Our own
meanings").

## 2. Track A: whole dictionaries of Nubian (H1)

**The sources**, both public domain and on disk as page images without a text layer:

| Book | Part typed | Printed pages | PDF page indexes | Pages |
|---|---|---|---|---|
| Reinisch, *Die Nuba-Sprache*, vol. 3, *Wörterbuch* (1879) | Nubian–German | 1 to 188 | 333 to 520 | 188 |
| Lepsius, *Nubische Grammatik* (1880) | *Nubisch-Deutsches Wörterbuch* | 263 to 414 | 410 to 561 | 152 |

The German–Nubian parts of both books are not typed: they index the same words.

**The typing.** 43 typists, eight pages each (the last pack of Reinisch has four), one file a page with one row
an entry: headword with every mark, dialect, loan mark, plural, part of speech, the German meanings as printed,
an English translation of them, cross-references, and a row of its own for each derived word printed with a
meaning. The brief is [`runs/prompts/NUBIAN_typists.md`](../../runs/prompts/NUBIAN_typists.md).

**The second reading.** 34 pages, a tenth, are typed a second time by 5 fresh typists who do not see the first
typing. They were drawn by lot before any typist started (`random.Random(20261116)`: 19 of Reinisch's indexes,
then 15 of Lepsius's):

- Reinisch: 334, 336, 381, 386, 387, 395, 415, 419, 426, 436, 461, 462, 466, 477, 480, 493, 495, 498, 509.
- Lepsius: 419, 441, 457, 462, 467, 475, 501, 513, 521, 527, 529, 543, 552, 553, 556.

**The typing's bar.** On those pages, at least 95% of the first typist's headwords stand in the second reading
with the same letters once length marks and accents are set aside, and at least 90% of those carry the same
German meaning (a likeness of 0.8 or more by Python's `difflib`). The share of headwords equal mark for mark is
reported beside it. If the bar is missed, every page is typed a second time and the differences are settled
against the page before any test below is run.

**Gate A1: do the sound laws carry anything on words they were not built from?** No agent takes part.

- **The words.** The dictionary words in use that have a meaning on the map of 2026-11-16 (160), without the
  15 that both readers of the Egyptian key take for loans into Meroitic and without the 18 that Rilly's
  correspondences were built from: 127. Two reductions follow, by rule: a word built on one of those 18 is left
  out (its headword begins or ends with one of them that has three letters or more), and words built on one stem
  count once (the shortest headword of three letters or more stands for those that begin with it). The script
  writes the list, and the list is committed with the script.
- **The comparison.** The engine of the first test as it stands (`src/cognates_rules.py`, last changed in
  1b4f0ff): its score by Rilly's 82 correspondences, and its shuffle test with 2,000 shuffles and seed 3. A
  Nubian row has the same meaning as a Meroitic word by the engine's own rule, applied to the typists' English
  meanings. The rows are the two typed dictionaries without the entries marked as loans, together with the
  5,442 rows of the short lists; the dictionaries alone are reported beside it.
- **The bar.** p < 0.05, on at least 30 words that have a row of the same meaning. With fewer than 30 such
  words the test is reported as too small to decide.
- **The script** is written by an agent that does not open the typed pages, and is committed before it is run
  on them. It is run once.

**If gate A1 is missed,** no meaning is proposed from these dictionaries. That closes the comparison for Nile
Nubian (Kenzi, Dongola, Mahas, Fadidscha), which is what the two books hold; the other branches of the family
(Old Nubian, Hill Nubian, Nara, Taman, Nyima) are tested the same way if their dictionaries are fetched.

**Gate A2, only if A1 is met: the whole path, blind, on the known words.** Each known word of the list is hidden
behind a code. The engine gives it the best-scoring dictionary entries of its kind of word; their meanings,
with fillers, go to five readers as a choice from the contexts, as in the blind test
([`blind_test_83.md`](blind_test_83.md)). How the candidates and the fillers are drawn is committed before the
readers start. The bars are those of the blind test and stand now:

- where all five readers choose one meaning for a word whose true meaning is among those offered, at least 80%
  of those choices are right, on at least 8 words;
- of the words whose true meaning is not among those offered, at most 10% get a meaning chosen by all five.

Only if both hold are candidates made for the words without a meaning.

**Rules added on 2026-11-16 at about 22:15, after the script was written and before it was committed or run on
a typed page** (its builder had seen no typed page). Its builder named two weaknesses of the rules above:

- **The meanings of the Meroitic words.** A word's meaning is taken, in this order, from the short wording of the
  public tables (`lexicon_statuses.tsv`, `meaning_in_our_words`) where one exists; else from the map's wording,
  for a word a layer of the map gives a meaning; else from the lexicon's English meaning. Words of grammar and of
  cross-reference (articles, prepositions, conjunctions, auxiliaries, pronouns, and "see", "also", "variant",
  "form", "cf", "perhaps", "probably", "kind", "sort", "type") are taken out of that wording, and out of the
  typists' English meanings, before the engine makes its keys; a fixed list in the script, with no word of
  content on it. The engine itself is not changed.
- **A third reduction, by name,** each word with its reason in the public list: forms of a word the
  correspondences were built from that the lexicon ties to it (`qor`, `yeto`, `mse`, `ḫ- (1)`, `ḫlẖl`, `ḫmlol`);
  words built on a loan (`apote-lẖ`, `pesto`, `at (1)`); and of each family of stems under three letters that
  stands more than once (`tk`, `ns`, `qo`, and any other found), the shortest headword alone. A word of the first
  two kinds is dropped only where the lexicon's own entry or the Egyptian key says so.
- **Decided by the builder and kept:** an entry with no dialect mark is one row, scored as Nobiin (the engine
  scores Kenzi, Dongola and Nobiin by the same correspondences); `ṅ` is read as ŋ, `ń` as ɲ, a `g` with a mark as
  the palatal stop, Reinisch's `q` as c, from the sound chapters of the two grammars; the sub-rows of a loan are
  loans; the typing's bar sets aside the marks on vowels and case, and no mark on a consonant. The gate refuses
  to run twice, on a script or a list that is not as committed, on a page that failed the merge's checks, or
  while the typing's bar is not met.

**Found by the review and added on 2026-11-16 at about 23:15, before gate A1 is run.**

- **The engine's shuffle is not a fair 5% test for these words.** The reviewer ran it with no related word in the
  data at all (the kept words against the short lists, each row's forms moved to another row): it gave p < 0.05
  in 13 of 40 draws (median p 0.136). Short Meroitic words carry broad meanings that match many rows, and a shuffle
  across words of every length breaks that pairing. Shuffling the meanings only among words with the same number
  of consonants gave p < 0.05 in 2 of 40 (median 0.488), the size a 5% test should have. The script computes both
  (`by_length` beside the engine's own). Which one is the bar is Mike's to say, and is asked before the gate runs.
  **Decided before the gate ran:** asked "Should gate A1's bar be the length-matched shuffle instead of the
  engine's own?", Mike answered on 2026-11-17 at about 06:50: "do you call". The bar is the length-matched
  shuffle (`by_length`), because the engine's own passes about one time in three with no related word in the data;
  the engine's own is reported beside it.
- Words that name a kind of word or speak of meaning ("noun", "verb", "adjective", "adverb", "particle",
  "suffix", "prefix", "ending", "word", "meaning", "sense") join the words taken out before the keys.
- `pqr` is dropped by name as a form of `qore`: the lexicon's entry `p- (2)` analyses it as p- + `qr`.
- Left as it is: the rule for the families of short stems goes by letters and also drops a few words not built
  on them (`ateqi`, `qetrri`, `qetneyineqeli`). It lowers the number of words; it does not make the test easier.

## 3. Track B: the royal texts beside the Kushite kings' Egyptian texts (H2)

**The Meroitic side.** The inscriptions of `corpus_v6` whose kind is "royal or temple" (87) or "oracular decree"
(7), and every text of 100 words or more (7, five of them of another kind): 99 texts and 2,945 words. On the
map with its layers 1,370 of those words are open, and 102 dictionary words with a meaning stand in them, at
624 places.

**The other side.** The sources of *Fontes Historiae Nubiorum* I and II that are not in Meroitic: the Egyptian
texts of the kings of Kush from the 8th to the 1st century BC, with the Demotic and Greek texts printed beside
them, in the editors' English. Both volumes are on disk with a text layer.

**Step 1: the frames.** Six builders, one angle each, read the two volumes and never see a Meroitic text. The
angles: the king's names, titles and epithets; the gods (epithets, speeches, hymns); dates, enthronement and
journeys; war (the report of a campaign, the lists of booty and of captives); gifts and buildings (donations
and offerings with their numbers, dedications); and the texts of people who are not kings (officials,
graffiti, oracles and decrees). A frame is a run of slots in a fixed order that stands in at least three
sources; each slot has a meaning, the wording of the translation, and the sources with their pages.

**Step 2: the packs.** A script cuts the 99 texts into packs and shows every word either by the map's reading
or by a code. A word without a meaning is a code. The 102 known words are dealt by lot (seed 20261116) into two
halves; in each of two folds one half is shown as codes too, every spelling of a hidden word under one code,
so that a reader cannot tell a hidden word from an open one. Gods' names are shown; the names of people and
places are codes that say which of the two they are. The script is committed before any aligner is started.

**Step 3: the aligners.** For each pack and fold, two aligners get the pack and the frames, and two more get
the pack alone. Each gives every code a meaning in a few English words or "none", and, with the frames, the
frame and slot it rests on.

**Step 4: the judges.** Two judges, who do not know which arm an answer comes from, compare each answer for a
hidden word with the meaning the lexicon gives it: the same, partly, or another. Beside every answer stands a
decoy, the same answer paired with the meaning of another hidden word of its kind, drawn by lot. The judges'
bar: kappa of at least 0.6.

**Gate B.** A hidden word is *given* when both aligners with the frames give it a meaning, and *right* when
both judges call both answers the same as the lexicon's.

- At least 80% of the given words are right, on at least 10 given words.
- That share stands at least 30 points above the share of decoys that both judges call the same.

The design put to Mike said "30 points above frames dealt by lot". An aligner chooses its frames itself, so
frames cannot be dealt to it by lot; the decoys measure the same thing, how often an answer fits a meaning that
is not its own. The arm without frames is counted the same way and reported beside the gate: it says whether
the Egyptian texts carry the result or the reader's own knowledge of such texts does.

**If the gate is met,** the open words to which both aligners with the frames give the same meaning are listed
as favoured by the frames, each with its frame. **What a pass would not show:** the hidden words are commoner
than the open ones, and an aligner may know a published reading of a famous text. So each listed word still
goes through the sources in hand and an independent check, by rules set before that step starts.

**Rules added on 2026-11-16 at about 22:15, after the packs were built and before any aligner was started.**
The packs' builder asked eight questions; the answers:

1. **A hidden word that stands in several packs** (59 of the 102) is *given* when both aligners with the frames
   give it a meaning in one of its packs, and *right* only when it is right in every pack where it is given. The
   count by word and pack is reported beside it.
2. **The meaning to judge against** is taken as in track A: the public tables' short wording where one exists,
   else the meaning the map gives the word, else the lexicon's English.
3. **A meaning that only names another word** ("variant of sr") is replaced by that word's meaning where the map
   gives it one; a word left without a meaning of its own is left out of the count, and its number is reported.
4. **The frames an aligner is given** are a digest of the six files written by the script: each frame's id,
   name, place in a text and monuments, and each slot's number, meaning, wording and whether it may be left out
   or repeated, without the sources' passages and notes (the six files together are about 120,000 tokens, too
   many for one reader).
5. **A text of 708 words** (REM 1044) stays one pack: a text is never split.
6. **In the arm with the frames,** a meaning that names no frame and slot of the digest counts as "none"; the
   number of such answers is reported. The brief does not tell the aligners that some codes are known words.
7. **`l (2)`, "to give"**, stands at 98 of the 624 places of known words, 83 of them as the single letter `l`;
   it is counted as one word like any other.
8. **What the packs cannot hide:** a hidden code stands at three places in the median and an open one at one,
   and hidden codes are more often joined to an ending (39 to 45% against 15 to 16%). A reader who guesses that
   a common code is a known word gains nothing it can use: it does not know which word.
9. **Forms built on a hidden word** (added at about 23:15, after the review): in each fold, a word whose headword
   begins with the headword of a hidden entry of three letters or more (`qorene` when `qore` is hidden) is shown
   as a code and not counted. Its reading would hint at the hidden word's meaning, where an open word has no such
   neighbour.

### Result of track B (2026-11-16)

The script was reviewed at the full tier by a fresh Opus 5.5 reviewer before any aligner started; every line of
track B was met (the review stayed open only on gate A1). The six frame builders gave 150 frames (2,693,594
tokens); 80 Opus aligners answered 4,550 codes in each arm (10,659,683 tokens); two judges read 419 rows, each
answer beside a decoy (kappa 0.94 on the three verdicts, 0.91 on same or not). Local files:
`data/sources/frames/`; the count is `result.json`, made once at 23:52 on the script of 6e383c3.

**Gate B: missed.**

| Arm | Hidden words given by both aligners | Right | Share right | Decoys called the same | Margin |
|---|---|---|---|---|---|
| With the frames | 26 | 7 | 26.9% | 7.7% | 19.2 points |
| Without the frames | 38 | 5 | 13.2% | 7.9% | 5.3 points |

The bars were 80% right on at least 10 given words, and 30 points above the decoys. Counted by word and pack
instead of by word, the frames arm has 12 right of 33 given.

**What it shows.** The Egyptian frames double the share of right meanings over the same readers without them, so
they carry something real. But where two readers with the frames agree to give a hidden word a meaning, it is
wrong about three times in four, so a meaning read off a frame cannot be trusted for an open word. The aligners
named why: no frame fits the oracular decrees or the funerary formulas of the long texts, the Meroitic order
(verb last) does not follow the Egyptian, and the commonest little word, `l`, is read "to give" or "the", which
hides where the clauses end. No open word is listed, and `open-packs` is not run.

## 4. Track C: names as small sentences (H3)

**The names.** Every place the map with its layers marks as a person's name: 705 places, 701 of them without a
lost sign, 624 different spellings. The grammar pilot's split is used again
([`grammar_pilot.md`](grammar_pilot.md), section 2): 350 spellings stand in the 329 tuning texts and 305 in the
219 held-back texts, 31 of them in both.

**Step 1: the cutter.** One builder writes a script that cuts a name into parts that come back, from the tuning
names alone; it takes off what the map already names as an ending. It does not open the held-back names. The
script is committed before it is run on them.

**Gate C1: do the parts carry over?** The share of held-back names that the cutter splits wholly into parts
standing in at least three tuning names must be at least 30 points above the same share for made-up names (the
letters of each held-back name shuffled, 200 draws, seed 20261116).

The design put to Mike said that at least 80% of the known parts (`mlo`, `lẖ`, the gods' names) must come out
as parts. Counted before any agent started, on the gods' names and known words tried: in the held-back names
`mlo` stands in 5, `lẖ` in 6, `mni` in 9, `kdi` in 5, `ms` in 6 and `ar` in 8, the others tried in fewer. A list
of about seven parts cannot carry an 80% bar, so the first half of that gate is the count above; the second half
is gate C2.

**Gate C2: do the parts come out as what they are?** Every part that stands in at least five of the 624 names
gets a code. Two readers, who see no letters, get for each code how often it stands first, in the middle and
last, with which gods' names, in the names of mothers, fathers and the dead, and at which sites; and what is
known of how Egyptian and Nubian names are built. Each says what kind of part it is (a god, a quality, a thing
or person, a deed, a kin word, a title, an ending) and, if they can, what it means. The known parts are those
whose letters are a god's name of the map or a dictionary word with a meaning.

- **Kinds:** where both readers give a known part the same kind, at least 80% are right, on at least 8 parts.
- **Meanings:** where both give it the same meaning, at least 80% are right, on at least 8 parts.

With fewer than 8 parts agreed, a bar is neither met nor missed: the test is too small to decide, and nothing
is laid. If the kinds' bar is met, the parts without a meaning that both readers agree on are listed with
their kind. Only if the meanings' bar is met is a meaning listed, and then only as a proposal, as in track B.

**Rules added on 2026-11-16 at about 22:45, after the script was written on the tuning names and before it was
committed or run on a held-back name.** The builders named eight points; the answers:

1. **Endings.** Where the map cuts a name into parts, what it names as an ending is taken off. Where it does not,
   an end is taken off only where the map reads the word "this is X", and only an end that the map's own parts
   take off at least three tuning names and that the lexicon lists (in practice `qowi` and `qo`). Taking off
   whatever the lexicon lists as an ending would have cut 251 of the 262 one-piece tuning names.
2. **A name, for counting,** is a spelling with its endings off, so that two spellings of one name count once,
   for the cutter and for gate C2. Gate C1 counts the 305 held-back spellings, as above, with the count by names
   beside it.
3. **The parts** that "stand in at least three tuning names" are the cutter's 328: strings of two letters or more
   in at least three tuning names, without a string that a string one letter longer follows into every one of its
   names (358 strings before that cut).
4. **The codes of gate C2** are the frozen cutter's parts, counted over all names; a god stands "in the same name"
   only where its letters are one of those parts.
5. **The kinds in the key** come from the lexicon's kind of the word by a fixed table (a god's name: god;
   adjective or epithet: quality; verb: deed; title: title; noun: thing or person, or kin word where its meaning is
   a kin term; function word: ending). **Title and quality count as one kind for the bar:** in names both describe
   the bearer, and the lexicon files some words as titles that names use as qualities (`lẖ`, "great"). A known
   part without a kind in the lexicon counts for the meanings only.
6. **Two readers who both say "unclear"** have not agreed on a kind.
7. **A meaning that only names another word** is replaced as in track B; no known part among the tuning parts
   needs it.
8. **Reported beside gate C1, with no bar:** the same share for made-up names that keep their syllables and only
   shuffle their order.

**What the bar of C1 may expect, measured before the run on the tuning names alone:** learning from half of them
and cutting the other half, 30.0% are wholly split against 5.9% for shuffled letters (24.1 points); learning from
four fifths and cutting the last fifth, 48.2% against 11.3% (36.9 points); with every other tuning text standing
for the held-back set, 33.7% against 6.4% (27.4 points). The real gate learns from all 342 tuning names. The bar
of 30 points is not changed.

### Result of track C (2026-11-16)

The script was reviewed at the full tier by a fresh Opus 5.5 reviewer, which fixed eight faults before any gate
ran (the gravest: the order of the codes in a pack told the known parts from the others) and marked it clean
(18a3c11). Local files: `data/sources/names/`.

**Gate C1, run once at 23:11:55 on 18a3c11: met.** 191 of the 305 held-back names are split wholly into parts that
stand in three tuning names or more (62.6%); the same names with their letters shuffled, 15.8% (200 draws):
46.8 points, where the bar was 30. Without the 31 spellings that stand in the tuning texts too: 165 of 274, 60.2%
against 15.4% (44.8 points). Beside it, with no bar: names that keep their syllables and shuffle their order split
39.9% of the time, so about 20 of the 46.8 points come from the parts and not from the syllables alone.

What C1 shows: the parts that the cutter learned come back in names it never saw, far more often than chance
letters do. It says nothing of what any part means.

**Gate C2, counted at 23:16:27 on 18a3c11: too small to decide.** 260 parts in six packs, 26 of them known, two
readers a pack, blind to the letters and to which parts are known. The readers answered "unclear" for 237 of the
260 parts, and both did so for 23 of the 26 known ones (kappa on kinds 0.84, most of it agreement on "unclear").
They agreed on the kind of one known part and gave it rightly (a god, Amun), and on its meaning; a bar needed 8.
Where they gave a kind at all it was mostly "ending", for parts that close women's names. One reader called the
part `kdi` "thing or person", "woman, female", which is its meaning; the other called it unclear.

What C2 shows: the counts of where a part stands, with which gods and in whose names, do not tell careful readers
what kind of part it is; they decline to guess, and the test cannot decide. This is a third kind of evidence from
inside the texts that gives the kind of a word sooner than its meaning, and here not even the kind.

## 5. The order, and who writes what

- The three tracks run side by side; none reads another's files. Agents write under `data/sources/nubian/`,
  `data/sources/frames/` and `data/sources/names/` (local), and the builders write `src/nubian.py`,
  `src/frames.py` and `src/names.py` with a test file each.
- No builder runs git. Each script is committed here before its test is run, and the commit is named in the
  track's result.
- Everything is reviewed before it is called done, and nothing is pushed without Mike's word.

## 6. What is left (2026-11-17, 07:00)

Mike, 2026-11-17: "describe the progress in the doc with what is left. and push everything."

1. **Gate A1, run once.** `python3 -I src/nubian.py merge`, then `agree` (the typing's bar: 95% of headwords and
   90% of their meanings the same on the 34 pages typed twice; if it is missed, every page is typed a second time
   before the gate), then `gate`, which counts the bar once: the length-matched shuffle, p < 0.05 on at least 30
   words. The script refuses to run if it is not as committed.
2. **The public figures files** of the three tracks (`public` in each script), checked against this page.
3. **Gate A2,** only if A1 is met: the blind choice with the dictionaries' candidates, by the bars of section 2.
4. **The other dictionaries fetched on 2026-11-16** (`data/INDEX.md`, section 3: Murray 1923, Almkvist 1911, the
   Comparative Nubian Dictionary data, Reinisch's Barea, Meinhof, Czermak, MacMichael, Griffith 1913, Lukas
   1933): typed and tested the same way only if gate A1 shows a signal in the two dictionaries typed so far.
5. **What tracks B and C leave:** the frames double the share of right meanings but are wrong three times in
   four, so they cannot name an open word; the name parts are real but their places do not tell their kind. Both
   are closed as ways to a meaning of the project's own, unless new texts or a bilingual come.

**What it cost:** track B about 14.8 million subagent tokens; track A's typing about 14.0 million; track C about
1.9 million with its review; the reviews of A and B about 1.4 million. Fable's usage limit stopped 11 agents
on 2026-11-16 at about 22:16; everything after ran on Opus 5.5.
