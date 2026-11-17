# The grammar-first pilot

Status on 2026-11-16, 19:22: the first round is counted (section 8): 41 of 54 rules passed on the held-back
texts, and none of them is a finding of ours, since the sources in hand state or partly state every one. A
second round, on the texts outside the epitaphs, is set (section 9); its finders have not been started. Working
scripts (local, not reviewed yet): `data/sources/grammar/`; the rules' tests are frozen on the branch `grammar`.
What the finders are given: [`runs/prompts/GRAMMAR_finders.md`](../../runs/prompts/GRAMMAR_finders.md).

## 1. What was asked

Mike, 2026-11-16: "how can we make more structural strategic moves. I am a bit pissed we've been working on
"assembling some data" for the last week". The move as it was put to him:

> **Grammar first.** Stop chasing word meanings. Find rules of the grammar (word order, endings, agreement), test
> each on held-back texts, then parse the long royal texts with them.

Asked "Should I start a two-day grammar-first pilot?", he answered: "Yes, start it".

| | Requirement | State |
|---|---|---|
| R1 | "Find rules of the grammar (word order, endings, agreement)." | Set: sections 3 and 4. |
| R2 | "Test each on held-back texts." | Set: sections 2 and 5. |
| R3 | "Then parse the long royal texts with them." | Set: section 6. |
| R4 | "A two-day pilot." | Started on 2026-11-16; its verdict is due by the evening of 2026-11-18. |
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
grammar of the epitaph, and it does not carry over. No word without a meaning gets a kind or a role from these
rules that the map did not already give it.

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
