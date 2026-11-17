# The grammar-first pilot

Status on 2026-11-16, 19:09: the split of the texts, what counts as a rule, and the bars are set; no rule finder
has been started. Working script (local): `data/sources/grammar/run.py`. What the finders are given:
[`runs/prompts/GRAMMAR_finders.md`](../../runs/prompts/GRAMMAR_finders.md).

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
