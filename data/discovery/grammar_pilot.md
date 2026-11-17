# The grammar-first pilot

Status on 2026-11-16, 19:34: **the pilot is over, and its bar is not met.** Over two rounds 73 rules were
proposed, 53 passed on held-back texts, and 1 is a finding of ours where 3 were needed (sections 8, 10 and 11).
The grammar that can be tested on this corpus is the grammar the sources already describe. The long texts were
cut by the rules that passed after the review asked for it (section 12). The script is
`src/grammar.py` (checks: `tests/test_grammar.py`); the rules' tests stand in `runs/grammar/` as they were frozen
(first committed at 19:15:35 and 19:30:39 on a branch of their own, `grammar`, as 604c379 and 6c974f3; in this
history they are 8b011a7 and 81a043e, copies of the same files made at 19:35 that keep the first commits' author
times). Every count of this page is in
[`grammar_pilot_figures.json`](grammar_pilot_figures.json), where each rule stands with its counts and its two
readers' verdicts. What the agents were given:
[`runs/prompts/GRAMMAR_finders.md`](../../runs/prompts/GRAMMAR_finders.md) and
[`GRAMMAR_round2.md`](../../runs/prompts/GRAMMAR_round2.md).

## 1. What was asked

Mike, 2026-11-16: "how can we make more structural strategic moves. I am a bit pissed we've been working on
"assembling some data" for the last week". The move as it was put to him:

> **Grammar first.** Stop chasing word meanings. Find rules of the grammar (word order, endings, agreement), test
> each on held-back texts, then parse the long royal texts with them.

Asked "Should I start a two-day grammar-first pilot?", he answered: "Yes, start it".

| | Requirement | State |
|---|---|---|
| R1 | "Find rules of the grammar (word order, endings, agreement)." | Done: 73 rules in two rounds (sections 8 and 10). |
| R2 | "Test each on held-back texts." | Done: each rule's frozen test was run once on the held-back texts (sections 8 and 10). |
| R3 | "Then parse the long royal texts with them." | Done on 2026-11-16 at 20:15, after the review asked for it (section 12): the rules that passed cut the 7 long texts 25 times and speak of 54 of their 925 words without a meaning. At first only each rule's reach in those texts had been counted (sections 8 and 10). |
| R4 | "A two-day pilot." | Ended on 2026-11-16, its first evening, by the verdict set beforehand (section 11). |
| R5 | The project's rules for such steps: every bar committed before its agents are started, counts from a figures file, nothing called a finding of ours unless it passes a test set beforehand. | The bars are in this page, committed before any finder is started. |

## 2. The split

The 548 texts were dealt by lot (seed 20261128) into two sets, 40% held back within each kind of text, long
texts (100 words or more) apart from short ones:

| Set | Texts | Words | Long texts |
|---|---|---|---|
| Tuning: the rule finders see these | 329 | 5,614 | 4 |
| Held back: only the frozen tests see these | 219 | 4,676 | 3 |

The words are those of the map with its six reviewed layers ([map_layers.md](map_layers.md)). The split was
drawn once, before anything else of the pilot, and is not drawn again.

## 3. The rule finders

Eight finders, each a fresh agent (Opus), each with the tuning texts only and one angle of its own:

1. the noun phrase: the order of noun, adjective, determiner and genitive;
2. the verb: which prefixes and endings go together, and with what around the verb;
3. the clause: where a clause begins and ends, and the order of its members;
4. the endings of place, source and direction, and what they attach to;
5. counting: numerals, what is counted, and lists;
6. the epitaph: the order and the form of the clauses of filiation and relation, and of titles;
7. the long texts: frames that repeat from sentence to sentence, and the words that link them;
8. writing: how a stem and an ending change where they meet.

A finder writes and runs its own counts on the tuning texts and keeps at most 8 rules.

## 4. What a rule is

- **A rule is a statement about forms and places that a script can check** on the map's columns (text, kind of
  text, place in the text, spelling, level, the parts of the word and their entries), with no judgment in it.
- **It names its cases, its prediction and its comparison:** where it applies, what must be true there, and how
  often that would be true if the rule were not there, counted by the same script on the same texts (for an
  order, the opposite order).
- **It ties things together:** a word to its neighbours or to its place in the text, or a part of a word to
  another part or to the letters beside it.
- **Not a rule:** a statement that only repeats how the map cuts or labels one word (the map's cuts follow the
  lexicon), and a statement about what one word means.

## 5. The bars, set before any finder is started

1. **A frozen test.** Each rule's test is a function over the map's columns, written from the rule's wording and
   the tuning texts alone, and committed before it is run on the held-back texts. A rule whose wording cannot be
   made into such a test is dropped, and counted as dropped.
2. **On the held-back texts** a rule passes when it has at least 20 cases, holds in at least 80% of them, and
   stands at least 30 points above its comparison rate on those texts.
3. **A rule that passes is confirmed.** It is **a finding of ours** only if, besides, two readers, each on their
   own, find it stated in none of the sources in hand (the lexicon of 2003 with its entries for the endings,
   Rilly 2016 and 2021, Fontes Historiae Nubiorum, Millet 2005, Lipiński 2011, Griffith's works).
4. **Every rule proposed is reported with its result,** passed or not. No rule is reworded after its test.
5. **The pilot's verdict, set now:** grammar first is worth going on with if at least 3 rules are findings of
   ours. With fewer, the pilot ends with what it confirmed.

## 6. The long texts

After the test the rules that passed are applied to the 7 long texts: each is cut into clauses and phrases by
the rules, and for each word without a meaning the page says what the rules make of it (its kind, its role in
the clause). This part has no bar: it is a description. A meaning it suggests is a proposal to test, not a
result.

## 7. What the pilot cannot show

- **The map's cuts and labels follow the lexicon,** so a rule may in part restate the grammar already built
  into the map. Rules about whole words and their order depend on it least.
- **"Ours" means "in no source we hold".** The project does not hold Rilly's grammar of 2007, Rilly and de Voogt
  2012 or Hintze 1979, and the finders are a model that may have met published grammar.
- **The finders are told to open the tuning files only.** Nothing but that instruction keeps them from the rest.
- **4,676 held-back words are few:** a rare construction cannot reach 20 cases, however regular it is.

## 8. The first round (counted at 19:21)

**The finders.** Eight finders were started at 19:09, after the commit with the bars (19:09:13), and proposed 54
rules. Each finder then wrote its rules' counts as test functions; all 54 give the finder's own counts on the
tuning texts. The tests were committed at 19:15:35, the table of the held-back texts was written after that
(19:15:45), and the tests were run on it once.

| Result on the held-back texts | Rules |
|---|---|
| Passed (at least 20 cases, 80% holding, 30 points above the comparison) | 41 |
| Fewer than 20 cases | 4 |
| Holding in under 80% | 8 |
| Under 30 points above the comparison | 1 |

**Are they ours?** Four readers (two for each of 2 packs) searched the sources in hand for each of the 41 rules
between 19:16 and 19:20.

| Both readers | Rules |
|---|---|
| Stated by a source | 28 |
| Stated by one reader's source, partly by the other's | 4 |
| Partly stated | 9 |
| Not found | 0 |

**No rule is a finding of ours.** The pilot's bar of 3 is not met by this round.

**What the 41 rules are.** They describe the epitaph: 90% of their cases stand in funerary texts. Many say one
thing from several angles: the invocation of Isis and then Osiris opens the text, the naming comes before the
clauses of filiation, these before the offering formulas, water before bread, each with its own verb, and the
verb last. Griffith described that frame in 1911, and the sources name it most often (Griffith's Karanòg and
Rilly 2021, 17 rules each).

**The nine that are only partly stated** are sharper than what the sources in hand say, and are the round's
yield:

- on a verb with the prefix `ps-`, the prefix's vowel is o almost only before the stem `ẖ`, never before `ḫr`
  (32 of 35 held-back cases);
- the verb `ẖol` takes the bare prefix `p-` or none, not `ps-` (34 of 36);
- before the ending `-te` the stem `ḫr` keeps its k, the stem `ẖ` often does not (29 of 31);
- a word ends in `-owi` only after l, q or t (409 of 410);
- when two vowels are joined by a glide and the second is e or o, the glide is y (124 of 131);
- and four finer points of the same frame (what stands right before the first offering formula and before
  "bread", and where a `ps-` verb carries its ending).

Whether Rilly's grammar of 2007 or Hintze 1979 state them is not known: the project holds neither.

**The long texts (section 6).** The rules that passed say little about them:

| Text | Kind | Words | Open words | Rules with a case, of 41 | Cases | Holding |
|---|---|---|---|---|---|---|
| REM 1044 | funerary (a royal stela) | 708 | 374 | 22 | 101 | 55 |
| REM 1003 | royal or temple | 485 | 204 | 7 | 40 | 27 |
| REM 0094 | royal or temple | 234 | 136 | 12 | 55 | 36 |
| REM 1333 | funerary | 190 | 88 | 10 | 41 | 33 |
| REM 1039 | not known | 131 | 52 | 5 | 16 | 8 |
| REM 1066 | funerary | 113 | 31 | 36 | 168 | 147 |
| REM 1067 | not known | 111 | 40 | 33 | 63 | 58 |

In the two epitaph-like texts (REM 1066, REM 1067) nearly all rules apply and hold. In the three longest
texts few apply, and where they do they hold in about six cases of ten: the grammar that can be tested is the
grammar of the epitaph, and it does not carry over. This counts each rule's reach; the parse that section 6
set out is in section 12.

Cost: 8 finders, 845,046 tokens; 4 readers, 630,212 tokens (typed from the task notifications, local).

## 9. A second round, outside the epitaphs (set before its finders are started)

The first round found what is known because only the epitaph's formulas come often enough to reach 20 cases.
The second round keeps every bar of section 5 and changes what is searched:

- **The texts:** only those that are not funerary: 2,210 words of the tuning set for the finders, 1,776 words
  of the held-back set for the tests (royal and temple texts, documents, graffiti, oracular decrees, and texts
  whose kind is not known).
- **Six finders,** each a fresh agent (Opus) with one angle: the royal and temple texts; the documents (numbers,
  items, lists); the graffiti and the oracular decrees; the order of the endings within a word; names, titles
  and what stands beside them; frames that repeat from sentence to sentence. At most 6 rules each.
- **Not wanted:** a rule about the invocation, the naming, the filiation or the offering formulas of an epitaph.
- **The tests** are frozen in git before they are run, and are run on the held-back texts that are not
  funerary. The same bars, the same check against the sources by two readers, the same verdict: grammar first
  is worth going on with if, over both rounds, at least 3 rules are findings of ours.

With 1,776 held-back words a rule needs a construction that comes about once in 90 words to reach 20 cases:
few will.

## 10. The second round (counted at 19:33)

The six finders were started at 19:23, after the commit that set the round (19:22:34), and proposed 19 rules,
each with its test. All 19 tests give their finder's counts on the tuning texts. They were committed at
19:30:39 and then run once on the 1,776 held-back words that are not funerary.

| Result on the held-back texts | Rules |
|---|---|
| Passed | 12 |
| Holding in under 80% (three of them also under the margin) | 7 |

Two readers searched the sources in hand for each of the 12 between 19:31 and 19:33.

| Both readers | Rules |
|---|---|
| Stated by a source | 4 |
| Stated by one reader's source, partly by the other's | 1 |
| Partly stated | 6 |
| Not found | 1 |

**One rule is a finding of ours:** inside a word the sign `q` is followed by o or e far more often than other
consonant signs are (140 of 169 held-back cases, 82.8%, against 43.3%). It is a fact about spelling and sound.
Rilly reads `q` as a k spoken with rounded lips, and a grammar the project does not hold may well state it.

**What the finders reported, each on its own:** outside the epitaphs the texts are too few and too broken for
rules of word order. No frame in the graffiti, the oracular decrees or the documents reached the bar on the
tuning texts; several candidates stood in one stela alone (REM 1003) and were dropped or failed. What passed is
spelling (a word ends in b after e; in `-owi` after l or t; two vowel signs never meet), and three rules about
names and titles: a name with an ending takes no article, which the sources state for two uses only.

**The long texts.** Applied to the 7 long texts as in section 8, the 12 rules that passed have cases in each of
them (8 to 12 of the 12 rules a text), and their cases hold there 87% to 98% of the time: rules of spelling hold
in any text. As in section 8 their reach is counted; they cut no text into clauses.

Cost: 6 finders, 739,226 tokens; 2 readers, 271,463 tokens.

## 11. The verdict

| Over both rounds | Rules |
|---|---|
| Proposed | 73 |
| Passed on held-back texts | 53 |
| Stated or partly stated in a source in hand | 52 |
| A finding of ours | 1 |

**The bar set beforehand was 3. It is not met, and the pilot ends here,** on its first evening: a third round
would search the same few words again.

**What it shows.**

- **The testable grammar is the known grammar.** A rule needs a construction that comes back at least 20
  times in texts it was not found in. On this corpus only the epitaph's formulas and the habits of the script
  do, and scholars have described both.
- **Outside the epitaphs there are about 4,000 words,** one in eight of them in one stela. That is too little to
  test word order, endings or agreement, however regular they may be.
- **The yield is small and real:** 53 rules that hold out of sample (a check on the map's grammar), 15 points
  where the count is sharper than what the sources in hand say (the 9 of section 8 and 6 of this round), and
  one rule the sources in hand do not state.
- **It closes the second door.** Meanings cannot be read from the contexts (the blind tests), and new grammar
  cannot be tested on this little text. What is left is evidence the project does not hold: more texts, and
  the scholars who hold them.

Cost of the pilot: 20 agents, 2,485,947 tokens.

Review (2026-11-16): an independent reviewer (Opus 5.5, a fresh agent that saw the change and the task, not the
reasoning) checked the script, the checks and this page against the local files, and changed:

1. **The parse of the long texts is said to be not done.** Section 6 set it out (each long text cut into clauses
   by the rules, and for each word without a meaning what the rules make of it), and the request said "then
   parse the long royal texts with them". What was done is a count of each rule's reach in those texts. Section
   8 had said that no word without a meaning gets a kind or a role from the rules; no count stood behind it.
2. **The second round's rules are counted in the long texts too** (section 10), as section 6 set for every rule
   that passed.
3. **The commits that froze the tests are named as git has them:** the figures name the first commits and the
   copies in this history, and the opening says that the copies keep the first commits' author times.

The times were checked against three records: git's own log of the branch `grammar` has 604c379 at 19:15:35
and 6c974f3 at 19:30:39; the session's log has the finders started at 19:09:47 and 19:23:21 and the readers at
19:16:54 and 19:31:10; the files have the held-back table written at 19:15:45, after the first commit. The second
round's tests were committed and then run in one command, at 19:30:39. The tokens of all 20 agents are those of
their task notifications. No rule, test, answer, bar or count changed.

After the review (2026-11-16, 20:15) the parse of section 6 was built: section 12. The R3 row above and the
last lines of section 8 were changed with it; the review's note stands as it was written.


## 12. The long texts, cut by the rules (built on 2026-11-16 at 20:15, after the review)

The review found that section 6 had not been carried out: each rule's reach in the long texts had been counted,
but no text had been cut. This section does it as section 6 set it before any finder ran: a description, with no
bar. It uses the 53 rules that passed and nothing else. The script is `src/grammar.py` (`parse`); the cut
texts stay local, because they hold the spellings.

**The marks of an end.** A text is cut after every word that carries one.

| Mark | Rules | Where it can stand | It rests on |
|---|---|---|---|
| After woSi or wiSi, the word for Osiris in -i closes the address to the two gods | L1-4 (with L3-2, L7-4) | at the epitaph's fixed words | the rule's count |
| A word in -qowi closes the naming of the dead | L7-4, L3-3 (with L6-1) | at any word | the rule's wording |
| A word in -owi carries the ending -wi, which the rule calls the last of a sentence | L7-5 (with L8-4, M3-1, M6-1) | at any word | the rule's wording |
| The word before `ato mXe` closes a sentence | L7-3, L2-6 | at the epitaph's fixed words | the rule's count |
| The word before `at` closes the item of the offering list that comes before it | L5-6 | at the epitaph's fixed words | the rule's count |
| The verb right after mXe closes the phrase of noun, mXe and verb; a ps- verb in two pieces closes with the second | L3-7, L1-3 (with L7-1, L5-4, L4-5) | at the epitaph's fixed words | the rule's count |

Two of the six rest on a rule's wording alone. The rules L7-4 and L7-5 name an end ("the name closed by -qowi",
"the sentence-final ending -wi"), but what their tests counted was the order of the frame's parts and the letter
before -wi. No rule that passed gives a mark that does not hang on the epitaph's own words or on -owi.

**What the rules make of a word without a meaning** (the first that fits):

| The rules say | Rules |
|---|---|
| It stands right before a word of filiation, where a parent's name is due | L1-5, L6-2 |
| It stands right before `yetmde-`, where the noun that word governs is due | L1-6 |
| A verb: by the prefix `ps-` and a verbal ending; by its place right after mXe; in `-kete` with its object within two words before it | L4-5; L3-7, L1-3; L4-3 |
| It carries the copula: in `-owi` after l, q or t; or as a common noun with the article | L8-4, M3-1, M6-1; M5-2 |
| A place in `-te`, closed by the article or the copula | L4-1 |
| It ends in `-eb`, the mark of the plural | M1-2, M3-3, M4-2 |
| It closes a clause or a sentence (it carries a mark of an end) | the marks' rules |
| Nothing: no rule speaks of it | |

**The seven texts.**

| Text | Kind | Words | Cuts | Longest stretch without a cut | Words without a meaning | Of these, a rule speaks of |
|---|---|---|---|---|---|---|
| REM 1044 | funerary | 708 | 3 | 358 | 374 | 13 |
| REM 1003 | royal or temple | 485 | 0 | 485 | 204 | 20 |
| REM 0094 | royal or temple | 234 | 1 | 118 | 136 | 5 |
| REM 1333 | funerary | 190 | 1 | 189 | 88 | 3 |
| REM 1039 | not known | 131 | 0 | 131 | 52 | 1 |
| REM 1066 | funerary | 113 | 16 | 29 | 31 | 11 |
| REM 1067 | not known | 111 | 4 | 90 | 40 | 1 |
| All seven | | 1,972 | 25 | | 925 | 54 |

| What the rules say of the 925 words without a meaning | Words |
|---|---|
| Nothing | 871 |
| It ends in `-eb`, like a plural | 38 |
| It stands where the noun governed by `yetmde-` is due | 7 |
| A verb | 5 |
| A place in `-te` | 2 |
| It carries the copula | 2 |

**A stretch of each sort.** No spelling is shown: a word stands as what the map knows of it, a word without a
meaning as "[open: what the rules say]", and a double bar marks a cut.

- REM 1066, words 1 to 16 (a long text built like an epitaph):
  Isis, addressed · Osiris, addressed ‖ · (name) · (lost) · (translated) · (translated) · (translated) ‖ · (name) · (translated) · (translated) · (translated) ‖ · (name) ‖ · (lost) · (translated) · (translated) ‖ · (name)
- REM 1066, words 90 to 99:
  (translated) · [open: nothing said] · (name) ‖ · water · abundant · [open: verb] · (translated) ‖ · bread · abundant · [open: verb] ‖
- REM 1003, words 1 to 24 (the longest royal text):
  (name) · (translated) · (translated) · (translated) · (translated) · [open: nothing said] · (translated) · (translated) · (name) · (translated) · (translated) · (translated) · (translated) · (translated) · (translated) · (translated) · (translated) · (translated) · [open: nothing said] · (translated) · (translated) · (translated) · (translated) · [open: nothing said]

**What the parse gives, and what it does not.**

- **Where a text is built like an epitaph, the rules find its frame.** REM 1066 is cut 16 times: after the address
  to the gods, after the naming, and around the offering formulas with their verbs.
- **The three longest texts stay uncut.** REM 1044, REM 1003 and REM 0094 hold 1,427 words and are cut
  4 times; REM 1003 not once. A stretch of hundreds of words between two cuts is not a clause.
- **Of the 925 words without a meaning the rules speak of 54,** and of 38 of those they say only that the
  word ends in `-eb`, like a plural. Of 871 they say nothing.
- **So the rules that could be tested do not parse the long royal texts.** The parse gives no word a meaning and
  proposes none; it shows in numbers what section 8 said of the rules' reach.
