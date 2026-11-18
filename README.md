# Meroitic with Opus 5.5

**Did we decipher anything? No.** No new reading of the Meroitic language survived checking. What is new is about
the data and the method: the public corpus turned out to be mostly copies, 396 inscriptions are now machine-readable
under an open licence (327 of them missing from that corpus), the obvious way to blind a test of AI on an
undeciphered script (scramble the letters) turned out not to work, and we built a test that does.

Why the texts alone do not give more is written up in one place: [FINDINGS.md](FINDINGS.md).

## What's new

1. **The public Meroitic corpus is mostly copies.** The only machine-readable corpus
   ([Otten & Anastasopoulos, ALP 2025](https://aclanthology.org/2025.alp-1.11/)) is a file of 18,090 lines that holds
   662 different texts or phrases: each one is repeated, about 27 times on average, with only a person's name
   changed. For example, the short label `tdxe mlEqErebr qEret ___` appears 198 times, once with each of 198 names
   (`…aplXye`, `…pqebete`, `…msxte trEbit`, …). Anyone counting words in the file counts the same text over and over:
   some titles come out about 100 times more frequent than they are. The paper says so itself: it collected 871
   example texts and phrases (those quoted in Millet 1968 and Rilly 2007, Lobban's word list and three royal
   narratives) and swapped names to make 17,257 for training word vectors. What the paper does not say is that the
   file on GitHub, `mero-corpus.txt`, is that padded version (it has the 1,868 word forms the paper reports): the
   repository has no note saying so, and it holds the unpadded examples only in the per-scholar files the corpus was
   built from, with translations and page notes (`Data/MilletExamples.txt` and others), not as one corpus file. Our
   662 is lower than the paper's 871, probably because, with names masked, examples that differ only in a name count
   once; that was not checked. `src/pool.py` recovers the two swap pools (178 private and 11 royal names) from the
   data alone, and `src/dedup.py`, `src/collapse.py`, `src/clean_v2.py` undo it.
2. **396 inscriptions are now machine-readable under an open licence, 327 of them missing from the public corpus.**
   The model reads the Meroitic cursive type printed in Griffith's 1911–12 editions at 95.6% sign accuracy against
   the modern edition (99.6% against what Griffith printed), measured on 12 texts. The test covered cursive type
   only: about a third of the rows (48) are in hieroglyphic type, read with Griffith's sign table and not scored.
   It transcribed 152 inscriptions (29 only in part, as
   Griffith printed them) from *Meroitic Inscriptions* I–II and *Meroë*, public-domain editions, each row with its
   source page, site and object, and 127 with a REM number (`data/expansion/`, CC BY 4.0:
   [`LICENSE-DATA.md`](LICENSE-DATA.md)); 86 are not in the public corpus (+5% words). Griffith's hand copies it
   reads at 89% on their own, which is not enough. But his Karanòg volume prints most words of every inscription
   again in type, and with each reading checked against those pages it reaches 97.7% on the four texts that have a
   modern edition: 151 more inscriptions ([`data/expansion/karanog/`](data/expansion/karanog/README.md)), none of
   them in the public corpus (+15% words). A second reader of eleven of the 53 pages got 97.7% of the same signs.
   It can't read photographs of the stones (almost nothing). The longest text, the Akinidad stela (REM 1003), is
   open too: Griffith printed all 42 lines in 1917 in his transliteration of the time; typed by hand from page
   images and mapped to today's signs, 278 of its 337 words (82.5%) agree with Millet's closed reading
   ([`data/expansion/jea/`](data/expansion/jea/), `src/akinidad.py`). And 46 short texts on potsherds, none of
   them in the public corpus: the ostraca from Faras, Buhen and Dakkah that Griffith printed in 1925, typed from
   page images (item 27). Griffith's 46 funerary texts from Faras of 1922 are hand copies with no type to check
   them by, only his English renderings of the names, titles and formula words: all are typed, 3,865 signs; two
   readers who did not see each other's work agree on 97.6% of the signs of five texts drawn by lot (the bar was
   95%), and the two texts held in a modern edition agree on 90.4% (Faras 43, Millet) and 83.0% (Faras 44, the
   Newsletter) of the letters ([`data/expansion/faras/`](data/expansion/faras/README.md), `src/faras.py`).
3. **Scrambled-script "blind" tests don't work on a frontier model.** Given only a 17-word glossary of Meroitic
   re-spelled with a random letter swap, it broke the cipher and matched all 35 test words to their meanings; given the
   scrambled corpus with neutral labels, it recognised the opening formula "O Isis, O Osiris" and read the script from
   there. A test of AI decipherment on a known-but-undeciphered script has to assume the model has read the
   literature.
4. **A test that does work, and what it measures.** A synthetic twin language (same size and texture, every word
   invented): it recovered 41 and 43 of 52 meanings on two independent runs, where chance is about 2. And a
   recall-then-corpus test on Rilly's lexicon: of the words it could not recall, reading the corpus got it to the
   published meaning for 13 of 35 (20 within three guesses), scored by an independent judge.
5. **Its confidence is a usable filter.** Across every test, all 74 answers it gave at confidence 4 or 5 were right;
   at confidence 1 or 2, about a third were.
6. **It restores lost words better than statistics.** Where a masked word has no parallel anywhere in the texts, it
   restored 48% on the first guess against 26% for an n-gram model.
7. **Negative results worth knowing.**
   - With open word lists, Meroitic words show no resemblance to their Nubian-family equivalents beyond the about 20
     word series Rilly built his sound laws from (held-out p = 0.49): the lexical case for the family rests on those.
   - None of the 14 "new" readings the discovery runs proposed survived an adversarial literature check. Of the two
     partial leads left open, one got weaker and one held when tested on texts typed afterwards
     ([`REPORT.md`](REPORT.md)). Where the key books are print-only, the model can't tell a
     rediscovery from a discovery.
   - The British Museum's Hamadab stela (REM 1003) holds nothing checkable against the Roman war, as Rilly said in 2014.
   - A search by sound alone does not find the Egyptian word behind a Meroitic title or noun. Tested on the known
     loans, each hidden in turn, it puts the true source among the five best candidates for 4 of 14 titles, nouns
     and verbs, though for all 10 names of gods, places and people that have a source among the Demotic names of
     their kind it is among the three best. For the 383 pieces without a meaning it gives nothing above chance, and
     two blind checkers found no new source among its 33 best matches
     ([`data/discovery/egyptian.md`](data/discovery/egyptian.md)). Comparing the written vowels too, on the Coptic
     entries, ranks the true source better (among the five best for 7 of 13 loans, against 4) and leaves both
     answers as they are. Of the step's two other Egyptian parallels, the oracular decrees are not done yet; the
     people the Philae graffiti name in Demotic are (item 13).
8. **About 62% of the corpus's running words can be translated today, word by word.** Every word of the 899 texts
   was glossed from Rilly's 2003 lexicon, by lookup and then by analysts. After four corrections made the same day,
   13,618 of 21,977 words (62.0%) are a name, a number or a word with an accepted meaning or function (61.6% with
   near-copies counted once); 16% have a proposal only, 9% are known by their kind only and 11% are unknown.
   Every legible word is translated in 106 of 605 texts. The 1,304 pieces without an accepted meaning are listed
   with their kind and the texts they block. The map as first built gave 60.5%, 82 texts and 1,336 pieces; the
   difference is words it counted wrongly, not meanings found
   ([`data/discovery/coverage.md`](data/discovery/coverage.md)).
9. **A search by letters ranks the spellings of a known word well, and cannot say by itself which unknown pieces
   are one.** Each of the 242 spelling variants that Rilly's lexicon lists under a word was hidden in turn. The
   search brings 187 (77%) back to their own entry as the single best match and 232 (96%) among the three best.
   The bar set before the run also asked half of them to stand out from made-up words, and only 105 (43%) do:
   a word of three or four letters cannot, since a made-up word that short is too often a word of the lexicon
   letter for letter. So the test missed its bar. Of the 1,140 pieces without a meaning that the lexicon does
   not already link to a word, 82 beat the made-up words where 57 are expected, but known words that are nobody's
   variant beat them as often, so two blind checkers read all 105 matches under the bar, the 23 that the lexicon
   links itself included. Both confirmed 48, and 29 of those are new. 26 are a word with an accepted meaning and
   would move 59 running words of the coverage map, from 60.5% to 60.7% (54 words, still 60.7%, without the two
   whose packs showed a word with the piece's letters and its gloss). The check is careful and misses a lot:
   of 12 listed variants shown as if they were unknown, both checkers named the right entry for 6, and of 12
   shown with the right entry taken out, both accepted a look-alike for 1
   ([`data/discovery/variants.md`](data/discovery/variants.md)).
10. **Two printed editions give the map's meaning for 70% of the words they translate, and for 85% outside two
    words on which scholars differ.** The coverage map takes every meaning from one lexicon. For the 31
    inscriptions that Millet's article on Gebel Adda (2005) or *Fontes Historiae Nubiorum* III (1998) also
    print, independent judges compared our reading of each word with the edition's. Of the 537 words the map
    counts as translated there, the edition gives a meaning to 397 and the map's meaning to 276 (69.5%). Most of
    the gap is two words: `yetmde`, "nephew, niece" in the lexicon and "relative" in both editions, and `qo`,
    "this one" against Millet's "the noble". Outside them it is 259 of 304 (85.2%). On a quarter of the words the
    editions are silent. The check found a numeral typed as a letter in the older corpus and eleven names or
    pieces of words read as words, and almost no meaning that the map lacks: of 167 meanings the editions give,
    the sure ones on words without an accepted meaning in the map are mostly titles left untranslated, phrases
    whose words the map reads the same way, and proposals the lexicon already holds
    ([`data/discovery/experts.md`](data/discovery/experts.md)).
11. **The corpus keyed by inscription: 899 texts held 288 inscriptions.** Otten's padded file can be undone
    exactly from his own per-scholar files: of its 17,995 different lines, 340 are a line of those files and
    17,446 are such a line with one name swapped. Traced that way, 54.4% of the words of `corpus_v5` are copies of
    a reading with a name swapped, and the texts that stand for an inscription hold 29.9% of them. `corpus_v6`
    has one row per inscription, with the real names: 637 inscriptions since 2026-11-17, 288 that were in
    `corpus_v5`, 209 of the Newsletter's texts, kept locally, and 140 of Griffith's texts that `corpus_v5` left out
    (46 of them his ostraca, item 27, and the Faras texts the corpus did not hold). The table of all 652 inscriptions is public, with
    every reading's source and licence and the text of the open ones: 486 have a REM number, 65 readings from two
    editions or more, 396 a reading under an open licence. The map is drawn on the 548 there were before the
    ostraca and the Faras texts. Counted again on the
    inscriptions that were already in the corpus, the coverage map translates 60.0% of the words (62.0% before),
    and the two editions give its meaning for 71.4% of the words they translate (69.5% before). The matching rule
    missed the bar set for it (the right partner for 45 of 54 known pairs, where 90% was asked), so numbers
    decide before letters, and the 17 doubtful matches went to two readers. Both passed their own test (12 of 12 known lines, 12 of 12 decoys); 13 of their matches are taken,
    one line matches nothing and 3 are not settled ([`data/discovery/corpus_v6.md`](data/discovery/corpus_v6.md)).
12. **Analysts on the spellings nobody had read add 1.4 points, half of what was expected.** The clean corpus
    had 930 spellings (1,038 running words) that only the lookup had seen, most of them in the Newsletter's
    texts. Eight analysts read them, 110 of them twice: 125 spellings got a translated level (68 names, 55
    meanings, 2 grammar words), and 550 got nothing. 139 running words more are translated, 5,419 of 10,290
    (52.7%, from 51.3%). The two analysts put 105 of the 110 words read twice on the same side, above the bar of
    85%. The gain expected beforehand was 265 to 385 words: the unread words turned out to be pieces of words
    printed in two parts, and single words of broken or obscure texts
    ([`data/discovery/v6_readers.md`](data/discovery/v6_readers.md)).
13. **The same people in Demotic, Greek and Meroitic: four of them carry titles in two languages, and where the
    two texts give the same office the titles line up with the lexicon.** *Fontes Historiae Nubiorum* III prints
    22 Demotic graffiti and two Greek inscriptions from Philae, Dakka and Maharraqa, among them those of the
    families whose Meroitic epitaphs the corpus holds. Three readers listed the people (99, 21 of them in two
    entries or more) and the 125 places where the editors set a Meroitic word beside a word of another language or
    give it a meaning. `perite` stands where the Demotic has "agent" for two people and `peseto` where it has "the
    king's son" and the Greek `psentes` for one, the words the lexicon derives them from; `kroro` stands where the
    Demotic writes the same title, of unknown meaning, as `3krre` for one. Two judges agree with the map's reading
    on 36 of 58 and 41 of 57 of the lines whose word it translates. No meaning is both new and sure; what the map
    lacks is mostly titles the editors leave as titles too ([`data/discovery/demotic.md`](data/discovery/demotic.md)).
14. **A second scholar for 84 of the 177 entries the map leans on: 4,105 of the 10,290 running words (39.9%) are
    built only on meanings two scholars share.** Rilly's lexicon records what other scholars proposed for most of
    its entries. Two judges set 407 such proposals beside the lexicon's meaning, without the scholar's name and
    with decoys (kappa 0.92 on "same or not"; 2 of 82 decoys accepted), and in a second round read the real
    proposal on the lines where they had seen a decoy (decoys accepted: 1 of 8 in round two, too many for the
    second judge by the letter of the bar); with the editors' readings of item 10, 84 entries are
    agreed by two scholars, 22 disputed (`qo`, `mlo` and `mte` lead), 51 stated by one and 20 only proposed. One
    lexicon translates 5,419 of the running words (52.7%); names and numbers count in both figures, and an ending
    that the lookup cuts off without naming its entry is not checked. A third round (kappa 0.90, 0 of 40 decoys
    accepted) rated the 417 other entries the map uses and the names among the 177: of all 594, 114 are agreed, 26
    disputed, 94 stated by one and 360 only proposed. Held to a stricter rule for the editors' readings, 3,715 words
    (36.1%) are agreed. A sample of the lexicon's citations of Griffith, checked against his own texts, held for all
    15 found. The review corrected the first count (3,873 words), which had called five names "proposed" and the
    verb `l` "to give" disputed on the numeral 1 typed as `l`. The public tables give each entry's meaning in words
    of our own (for the 177), its spellings with the confirmed variants of step 21, and the pages of the statements
    where the sources in hand give them ([`data/discovery/lexicon.md`](data/discovery/lexicon.md)).
15. **Five inscriptions translated whole, and scored against a scholar's renderings: the translation does not
    beat the map read word by word.** A translator agent, blind to N. B. Millet's edition of the Gebel Adda
    inscriptions (2005), translated five of the texts he renders, from the map's reading of each word and the
    statuses of F2 counted again without his proposals. Two judges with decoys marked each of his units of
    meaning given, partly, wrong or missing: of 57 units the translator gets 58.3% (given, and half of partly)
    and the map's glosses in order 60.5%, with 3.5% and 6.1% of the units wrong (judges' kappa 0.97, no decoy
    accepted). The translator adds a text a reader can follow and the status of every word; it leaves open what
    the map knows only vaguely, where a vague gloss earns half credit. Scoring all 18 of Millet's renderings the
    corpus holds would cost about 2.1 million subagent tokens ([`data/discovery/f4_pilot.md`](data/discovery/f4_pilot.md)).
16. **A translator with a handbook beats the map read word by word, also on texts it was not tuned on: 73.9%
    of a scholar's units of meaning against 58.5%, and a panel of three with an editor 74.9%.** After the pilot,
    several ways of translating were compared on its five texts: the map's glosses in order; a writer that only
    turns them into sentences; a translator with rules that keep a vague meaning instead of leaving the word open,
    a handbook of the grammar and of how an epitaph is built (compiled from the sources in hand, each line with its
    page, and checked line by line), and the other places of the corpus where each word stands; and a panel of
    three such translators with an editor.
    The first judging missed its bar (the judges' kappa 0.58: "related to" against "nephew or niece"), so one rule
    was added and the same readings judged again by new judges (kappa 0.94). The panel was carried to the 13 other
    renderings of Millet's that the corpus holds, held back until then: of 218 units the glosses get 58.5%, the
    writer 69.3%, one translator 73.9% and the panel 74.9%, with 9.2%, 4.4%, 2.8% and 2.3% of the units wrong
    (judges' kappa 0.88; each judge accepted 1 of 186 clean decoy units). The panel is not shown to beat one
    translator, and the writer, who sees no lexicon entry and no parallel, gets 10.8 of the 16.4 points: most of
    the gain needs neither. Not built yet: the pages for the 304 open inscriptions, and the scoring against
    Griffith's own translations ([`data/discovery/f4_rounds.md`](data/discovery/f4_rounds.md)).
17. **Of the unread spellings that recur, a quarter of the places take a meaning a scholar stated after 2003 and
    a sixth are pieces of other words; for the words that stay open, a blind test could not tell from the
    contexts, well enough to label any, the meaning a scholar proposed from others of its kind.** 154 spellings
    without an accepted meaning stand in three texts or more and cover 1,108 running words of the clean corpus.
    Readers collected what the sources in hand say of them (792 statements, every quote found in its file by
    script): for 26 items Rilly's later work (2016, 2021) states a meaning that the map, built on his lexicon of
    2003, does not have. Two checkers then decided each of the 1,108 places on their own (kappa 0.91): 273 hold
    the word the later source speaks of (the benediction verbs "eat" and "present, serve", "prince", the emphatic
    particle after the copula), 192 are pieces of a longer word or name that the edition's word division cut, 425
    are words of their own that stay open, and 218 are unclear or not agreed. Laid over the map, that moves the
    running words with a meaning from 3,676 to 3,916, from 50.1% to 53.9% of those that need one; since
    2026-11-16 these places are the map's first layer (item 19). For the open words a blind test asked five readers to pick, from the contexts
    alone, the meaning a scholar proposed among others of the same kind. On words whose meaning is accepted the
    readers' choice was right for 13 of 17 (76.5%, the bar was 80%), and they chose a wrong meaning for 2 of 11
    words whose true meaning was not offered (18.2%, the bar was 10%): so no proposal is labelled. None of these
    meanings is a reading of this project
    ([`data/discovery/recurring_words.md`](data/discovery/recurring_words.md)).
18. **Counted by distinct words, about one word in ten has a meaning: 127 of about 1,307 (9.7%, between 9.2%
    and 12.1%), the same as before the project.** Half of the running words are translated because the common
    words are. Counted once each, the words are far fewer: the map ties its spellings to 377 words of the lexicon,
    127 of them with an established or probable meaning, and leaves 1,107 stems it cannot name; an ending or a
    particle written as a word of its own is a piece of a word, not a word. Two checkers judged a sample of 240 of
    those stems (a first reading missed its bar; with the brief corrected the second agreed, kappa 0.94): about two
    in three are words of their own, the rest pieces, damaged words, names or forms of known words. Each of the
    127 has its meaning in the lexicon of 2003, so the share was the same before the project, which has added no
    meaning; a plain lookup of the lexicon finds 112 of them, and the map recognises the other 15 in spellings the
    lookup does not know. The first count took the endings and particles written as words for words and gave
    11.6%; the review corrected it. This is the project's north star
    ([`data/discovery/distinct_words.md`](data/discovery/distinct_words.md)).
19. **The results of item 17 are laid into the map as its first layer: with it 53.9% of the running words that
    need a meaning are translated, and 136 of about 1,307 distinct words (10.4%, between 9.8% and 13.0%).** The 385 places that item
    17 resolved (273 where Rilly states a meaning in 2016 or 2021, 66 pieces of a word or name the map holds, 46
    places of seven names) are laid over the analysts' map as a layer, each with its source; the analysts' map is
    not changed, and the studies run on it keep their numbers. That makes 240 running words more translated
    (3,676 to 3,916 of those that need a meaning, 50.1% to 53.9%) and gives 9 more words of the lexicon a meaning
    (127 to 136). All of these meanings were published before the project, so the north star's "before us" is
    the same 10.4%, and the project still has no meaning of its own. The step also asked for the three pages that
    count from the map (the coverage of the clean corpus, the lexicon's statuses, the translations' baseline) to be
    rebuilt from the same file: they are not, they keep their dated numbers and point to the new page, and Mike
    waived that part on 2026-11-16 ("Yes, waive it.")
    ([`data/discovery/map_layers.md`](data/discovery/map_layers.md)).
20. **Of the open spellings that stand in one or two texts, 268 more places take a scholar's meaning or turn out to
    be names; the map now translates 57.4% of the running words that need a meaning, and 156 of about 1,307 distinct
    words (11.9%).** 1,096 such spellings hang on an entry of the lexicon. Where the lexicon calls that entry sure,
    two checkers judged whether each place holds its word (366 places, kappa 0.70); where it does not, readers
    collected what the later sources say (1,659 statements, every quote found by script), two readers found a
    meaning stated by Rilly in 2016 or 2021 for 57 of 60 entries, and two checkers judged the 695 places of the
    entries concerned (kappa 0.93; a first reading was not taken, because one place had one checker's answer
    only). A stated place is laid in the map only where the map names every part of the spelling and each stem in
    it has a meaning, a piece only where the map translates or names the whole word: 109 places of the first kind
    and 159 of the second. At 182 more places both checkers recognise the word, but a part of the spelling is
    unnamed (at one, another stem has no meaning), so they stay open. With the three layers 4,149 of the 7,230 running words that need a meaning are translated (57.4%), 814 of 2,917 distinct spellings (27.9%) and 156 of about 1,307 distinct words (11.9%, between 11.3% and 14.9%). 20 entries of the lexicon get a meaning
    that way ("donkey", "horse", "to seize", "talent", the title Candace); by Rilly's own later analysis several
    of them are forms of one another, so the gain in words is smaller than 20. Before the project the north star
    was the same 11.9%: every one of these meanings was published before it
    ([`data/discovery/rare_spellings.md`](data/discovery/rare_spellings.md)).
21. **Of the open spellings the lexicon does not hold, two thirds are words of their own and a tenth are names;
    laying the 111 names leaves fewer words to decipher and gives no word a meaning.** 1,107 spellings that stand in one or two
    texts hang on no entry of the lexicon; they stand at 1,225 open places. Two checkers judged every place from the
    place alone (the word, five words on each side, the map's reading of each), with places of known answer mixed
    in. A first pilot missed two bars and is not taken: its controls asked for what context cannot show (a word
    cut in two in running text) and counted particles written apart as words. A second pilot and the full pass
    met their bars (kappa 0.80 and 0.79; no more than one known word in ten called a name, at least seven known
    names in ten found). Both checkers call 828 places a word of its own, 111 a name and 41 a piece of a word beside
    it; 245 are unclear or not agreed. The 111 names and the 7 pieces whose whole word the map holds are the map's
    fourth layer: 4,154 of the 7,117 running words that need a meaning are translated (58.4%), 815 of 2,813 distinct spellings (29.0%) and 156 of about 1,284 distinct words (12.1%, between 11.5% and 15.2%). The north star's last step is a recount, not a meaning: 39 more of the stems the map cannot
    name became names, and the estimate of the words among them was made again from the sampled stems still
    unnamed. The reporting rules had named a new sample; asked whether to keep the recount, Mike answered "why do
    you need my approval to recount? this is obvious you need to recount to show the up to date result?"
    ([`data/discovery/unnamed_spellings.md`](data/discovery/unnamed_spellings.md)).
22. **Half of the meanings that Rilly states in 2016 and 2021 are also stated by another scholar.** For the 66
    entries of the lexicon that items 17 and 20 gave a later meaning, two judges compared it with 260 statements
    of other scholars (Griffith, Millet, the editors of FHN, Lipiński, and the proposals the lexicon of 2003
    reports), with decoys mixed in (kappa 0.95; each judge took 1 of 26 decoys for the same meaning). 33 of the 66
    meanings are agreed by two scholars, for 15 of them with a third who dissents; 13 are disputed; 20 rest on
    Rilly alone. This is a status for each meaning, not a count of the map
    ([`data/discovery/second_scholar_later.md`](data/discovery/second_scholar_later.md)).
23. **The leftover parts: 49 more places are laid, 31 of them as translated words.** A follow-up to item 20, in two
    parts. Part 1: at 96 places the checkers of item 20 had recognised the word, but the map leaves a part of the
    spelling unnamed. Two checkers said what that part is, with 40 places of known answer mixed in. The first
    reading of the unnamed parts is not taken: one checker explained 3 of the 20 runs of letters drawn by lot,
    one more than the bar allowed, each time as a name, where the letters stood before "born of" or "this one".
    Asked whether to read again with a bar for each verdict, Mike said: "Yes, read again". The second reading,
    by fresh checkers on controls drawn anew, lays only what both call an ending or a known word, and never a
    name. It met its bars (kappa 0.66; 0 and 1 of the 20 runs of lot letters called an ending or a known word;
    20 and 19 of the 20 hidden endings found). The map's sixth layer lays 32 places, 27 of them as translated
    words and 5 as names
    ([`data/discovery/leftover_parts_2.md`](data/discovery/leftover_parts_2.md)). Part 2: for 15 entries that
    Rilly's later work gives no meaning, Millet 2005 or Lipiński 2011 states one. Two readers found 12 stated
    firmly: 7 as names, 3 with a Meroitic word left as it is, 2 as a meaning in full (both from Lipiński). Two
    checkers judged the 56 places (kappa 0.97). The map's fifth layer lays 17 places, 13 of them as names and 4 as
    translated words ([`data/discovery/leftover_parts.md`](data/discovery/leftover_parts.md)). With both layers,
    4,185 of the 7,099 running words that need a meaning are translated (59.0%), 840 of 2,798 distinct spellings (30.0%) and 160 of about 1,284 distinct words (12.5%, between 11.8% and 15.6%); before us the north star is the same.
24. **The blind test again gives no label: when all five readers pick the same meaning it is the right one 16 times
    in 17 if the right one is offered, and they all pick a wrong one 3 times in 13 if it is not.** The choice test of
    item 17 with what it taught: a choice needs all five readers, the fillers are drawn from one pool of accepted
    meanings and proposals, and a filler is never near another option. The plan named 83 accepted words; 43 could be
    used, because only 5 of the 45 further entries have a meaning that can be offered. Shown with their meaning, 17
    accepted words got a meaning from all five readers and 16 of 17 the right one (the bar of 80% is met; one more
    got "none of these" from all five). Shown without it, 3 of 13 got a wrong one from all five readers (the
    bar allowed one). So no label is given: a proposal that all five choose cannot be told from a wrong meaning
    chosen for want of the right one. All five chose the same proposal for 7 of the 33 open words; they carry no
    label ([`data/discovery/blind_test_2.md`](data/discovery/blind_test_2.md)). Mike did not waive the 83 words
    ("No, do not waive"), so the test was run again with all 83, the 40 others with the meaning the lexicon gives
    them, however coarse ("a priestly title"). It came out the same way: 36 of 37 right with the meaning offered,
    6 of 27 wrongly chosen without it, where the bar allowed two. No label is given, and this is the method's
    third miss. All five chose the same proposal for 8 of the 33 open words
    ([`data/discovery/blind_test_83.md`](data/discovery/blind_test_83.md)).
25. **The leftover stems: 23 more places are laid, 22 of them as names; no unnamed stem is a word the lexicon
    knows.** Item 23 named 182 leftover places and gave checkers 96. At the other 86 the checkers of item 20 had
    recognised an ending or a particle, and the unnamed part is the stem itself. The review asked whether a
    checker could still recognise such a stem as a known word, and Mike said: "run it and document everything in
    our doc". Two fresh checkers judged the 86 places among 80 places of known answer, 20 of each of four kinds:
    a hidden stem, hidden endings, a name, and letters drawn by lot in a stem's place. Each verdict stood on its
    own bars: found by each checker at least 14 times in 20, said wrongly at most 2 times in 20. Every bar was
    met (kappa 0.79; hidden stems named with their entry 18 and 15 times, hidden endings found 20 and 20 times,
    names 18 and 18 times; no run of lot letters called a name, an ending or a known word, and no hidden stem
    called a name).
    Both checkers call the stem unknown at 55 places, a name at 22, an ending at 1, and differ at 8; at no place
    do both find a known word. The map's seventh layer lays 23 places, 22 of them as names and 1 as a translated
    word ([`data/discovery/leftover_stems.md`](data/discovery/leftover_stems.md)). The map as it stands:
    4,186 of the 7,077 running words that need a meaning are translated (59.1%), 841 of 2,781 distinct spellings (30.2%) and 160 of about 1,283 distinct words (12.5%, between 11.8% and 15.6%); before us the north star is the same.
26. **Grammar first, a pilot: the grammar that can be tested is the grammar already described.** Mike asked for a
    move of another kind ("how can we make more structural strategic moves. I am a bit pissed we've been working
    on "assembling some data" for the last week") and answered "Yes, start it" to a pilot: find rules of the
    grammar on one part of the texts and test each on the other. The 548 texts were dealt by lot into
    329 for finding and 219 held back. Eight finders, one angle each, proposed 54 rules, each with its
    count written as a function; the functions were committed before the held-back texts were touched. A rule
    passed there with at least 20 cases, holding in 80% of them, 30 points above its comparison. 41 passed,
    and two readers found every one of them stated or partly stated in a source in hand: 90% of their cases
    stand in epitaphs, whose frame Griffith described in 1911. A second round on the texts that are not
    epitaphs (2,210 words for finding, 1,776 held back) gave 19 rules; 12 passed, and one is in no
    source in hand: inside a word the sign `q` is followed by o or e far more often than other consonant signs
    are. Over two rounds 73 rules were proposed, 53 passed on held-back texts and 1 is a finding of ours, where the bar set beforehand was 3:
    the pilot ended on its first evening. Its last part, the parse of the long royal texts, was built after the
    review asked for it: the rules that passed cut the 7 long texts 11 times, 6 of them in one text built like an
    epitaph, and speak of 51 of their 925 words without a meaning; the long royal texts stay uncut. At 15 points the count is sharper than what the
    sources in hand say. The map and its counts do not change
    ([`data/discovery/grammar_pilot.md`](data/discovery/grammar_pilot.md)).
27. **Griffith's 46 ostraca are open texts now, and Sayce's reading of the longest text settles almost nothing.**
    Griffith's "Meroitic Studies V" (*JEA* 11, 1925) prints 46 ostraca from Faras, Buhen and Dakkah in his
    transliteration of the time: 275 words, typed from page images and mapped to today's signs. A tenth of them,
    drawn by lot before the typing, was typed again by an agent that saw only the pages: all 56 signs agree (the
    bar was 97%). They are open readings in `corpus_v6`, none of them in the public corpus: 594 inscriptions with them,
    350 with an open reading (637 and 396 since the Faras texts, item 2). The map stays on the 548 texts it is drawn on until it is counted again with a new
    sample for the north star; of its 1,681 open spellings that stood in one text, 9 now stand in an ostracon too,
    five of them two-letter pieces. Sayce printed all 42 lines of REM 1003 in 1914-15 in his own letters (public
    domain: he died in 1933). Typed and mapped to Griffith's signs, his words agree with Millet's later reading at
    61.8%, where Griffith's agree at 82.5%; at Griffith's 38 doubted words Sayce reads 7 the same and 20
    otherwise and is unsure himself at 11, and Millet sides with Sayce alone at 1
    ([`data/discovery/ostraca_sayce.md`](data/discovery/ostraca_sayce.md)).
28. **The REM's plates cannot be read well enough to grow the corpus.** The *Répertoire d'épigraphie méroïtique*
    (2000, on Persée) gives each inscription as plates of photographs and drawings, with no transliteration. It
    holds 917 inscriptions, not 1,278 as its numbering suggests; 473 are not among the 548 texts the map is drawn
    on, about 4,600 words, and 91 of those 473 are typed but not yet in the map: the 46 ostraca of item 27 and 45
    of Griffith's Faras texts (item 2; the 46th, REM 0544, was held; REM 0543 is Millet's line 286, which the map
    holds under his number). A reader
    that saw only the plates read 4 inscriptions from their drawings: 426 of 555 signs right against Griffith
    (76.8%) and 43 of 103 words (41.7%), under the bar of 85%, at 158,438 subagent tokens an inscription, and
    nothing from the photographs. Reading all 473 so would cost about 28 to 75 million
    tokens and give about 44 of the 2,013 open spellings that stand in one text a second text read right. The pilot
    stopped at 4 of its 20 inscriptions on Mike's word; the route is a printed transliteration
    ([`data/discovery/rem_pilot.md`](data/discovery/rem_pilot.md)).
29. **The pictures beside the temple captions do not show what their words mean.** This is the one method left
    untried, the way the pictured objects in Linear B helped Ventris: 56 of the map's 87 royal and temple texts are
    captions whose relief is drawn in Lepsius's *Denkmäler* (section V), on Griffith's plate of the Philae chamber,
    or in Garstang's photographs. Each scene was cut out with its writing painted white. Each of 65 caption words of
    known meaning was then hidden, and read by two readers with its own picture and by two with a wrong one. With
    the true picture they scored 24.4% (half credit for a meaning partly right), with a wrong one 19.4%: a gain of
    5 points, p = 0.156. The bars, pushed before anything ran, were 50% and a gain of 20 points with p < 0.05. So
    the 71 open spellings of the captions were not read. A relief shows who a
    figure is, which the caption's names already say, not what its titles and epithets mean; 4.5 million tokens
    ([`data/discovery/caption_pilot.md`](data/discovery/caption_pilot.md)).

## The question

Meroitic, the language of the kingdom of Kush (Sudan, about 300 BC to 400 AD), can be read aloud since Griffith
(1909–11), but most of it is not understood: there is no long bilingual text, and its relatives in the Northern East
Sudanic family split from it long before it was written. This repo is a two-day experiment (2026-11-08/09), with
a third day of reading and testing (2026-11-10): can a
frontier language model (Claude Opus 5.5, run as about 60 independent subagents) find real patterns in Meroitic and
make it more understandable?

Results, with every number traced to its run: [`REPORT.md`](REPORT.md). What to do next: [`NEXT_STEPS.md`](NEXT_STEPS.md).
The illustrated summary page: <https://mikekovetsky.github.io/meroitic/> (source: `docs/report.html`). This file
describes the data and the methods.

## Data

Data without an open licence is not in this repo, apart from the readings and glosses the tests are scored against
(the Rilly and FHN rows below): it stays on the author's machine, listed in `.gitignore`, and the scripts rebuild
what can be rebuilt.

| Source | What | In this repo |
|---|---|---|
| Otten & Anastasopoulos, ALP 2025, [Meroitic-Corpus](https://github.com/Joshua-Otten/Meroitic-Corpus) | the only machine-readable corpus (18,090 lines): example texts and phrases quoted in Millet 1968 and Rilly 2007, Lobban's word list and three royal narratives, padded with name-swapped copies | not committed (no licence stated): clone it to `data/otten/`; the cleaned corpora (`data/corpus*.jsonl`) and the task files that embed them (`runs/tasks/`) are rebuilt locally, not committed |
| Griffith, *Meroitic Inscriptions* I–II (1911–12) and Garstang/Sayce/Griffith, *Meroë* (1911), archive.org | printed Meroitic type, public domain | `data/expansion/griffith_*.jsonl`, read by the model |
| Griffith, *Karanòg: The Meroitic Inscriptions of Shablûl and Karanòg* (1911), [archive.org](https://archive.org/details/karangmeroitic00grifuoft) | 151 funerary texts as hand copies, public domain; most of their words printed again in type in the same book | `data/expansion/karanog/`: the texts read by the model and checked against that type (`griffith_karanog.jsonl`), the 48 typed reference pages, and [how it was done and measured](data/expansion/karanog/README.md) |
| Griffith, "Meroitic Studies IV: The Great Stela of Prince Akinizaz", *JEA* 4 (1917), [Zenodo](https://zenodo.org/records/2497984) | the whole text of REM 1003 in his transliteration of 1917, public domain | `data/expansion/jea/`: his sections typed by hand from page images, the row in the corpus spelling and the counts of its comparison with the closed readings ([how](data/expansion/jea/README.md)) |
| *Meroitic Newsletter* 1–30 (1968–2003), scans at meroiticnewsletter.org | printed transliterations with REM numbers: 256 texts typed, 188 of them new to the corpus; the articles are in copyright | not committed: the method, the scripts (`src/mnl/`) and the measured accuracy are in [`data/expansion/newsletter_reading.md`](data/expansion/newsletter_reading.md) |
| Rilly 2003, *Lexique méroïtique* (thesis vol. II, HAL [tel-04793700](https://hal.science/tel-04793700)) | the fullest open lexicon, 937 entries | not committed (copyrighted): extracted from the scans for private analysis; `src/lexique.py` needs it in `data/rilly2003/`. The lexicon test's answer key (`runs/keys/lexique_*.json`, `runs/lexique_judge.json`) gives 68 of its glosses in English paraphrase |
| The TLA's [Demotic sentences](https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-demotic-v18-premium) and the [Comprehensive Coptic Lexicon](https://github.com/KELLIA/dictionary) v1.2, both CC BY-SA 4.0 | 5,660 Demotic lemmata with their word classes and 11,283 Coptic entries with meanings: the pools of the Egyptian search | not committed: download them to `data/sources/egyptian/demotic/train.jsonl` and `data/sources/egyptian/coptic/Comprehensive_Coptic_Lexicon-v1.2-2020.xml`; the list of candidates (`data/discovery/egyptian_candidates.tsv`, CC BY-SA 4.0) holds lemma numbers and forms |
| Rilly, Hintze, Griffith, Millet and others via web sources | the answer key: 82 accepted meanings, 26 grammatical endings, each sourced | `data/gold_lexicon.json`, `data/gold_morphology.json` |
| Starostin's GLD (no licence stated), IDS, ASJP, numerals (CC BY), Rilly 2003 vol. I (HAL) | Nubian, Nara, Taman, Nyima word lists; Rilly's 82 sound correspondences | not committed: `data/nes/README.md` lists every source and how the lists were built; `meroitic_wiktionary.tsv` (CC BY-SA) is included |
| *Fontes Historiae Nubiorum* II–III (Bergen, all rights reserved) | modern transliterations used as ground truth | the readings of about twenty short texts the reading tests are scored against, each with its REM number (`data/expansion/pilot.jsonl`, `printed_type_test.md` and `hand_copy_test.md` there, the scoring scripts in `runs/work/`); otherwise short excerpts |
| Millet, "The Meroitic Inscriptions from Gebel Adda", JSSEA 32 (2005), [the society's PDF](https://news.thessea.org/images/SSEA_assets/journals/JSSEA_32.pdf); *Fontes Historiae Nubiorum* III as a whole, [the copy on Zenodo](https://zenodo.org/records/821860) (the book says all rights reserved, the record CC BY 4.0) | 46 and 12 entries on inscriptions, with comments: the second witness in the check of the coverage map; and FHN III's Demotic and Greek graffiti, read beside its Meroitic texts | not committed (in copyright): `data/sources/jssea/`, `data/sources/fhn/` and their text layers (`data/sources/jssea-text/`, `data/sources/fhn-text/`), the judges' packs and answers in `data/sources/expert/`, and the readers' and judges' packs and answers of the Demotic step in `data/sources/demotic/`; `data/discovery/experts_figures.json` and `experts_words.tsv` hold counts and word forms only, `demotic_figures.json` counts and five title words |

Since 2026-11-12 the readings are also listed by inscription: [`data/inscriptions.jsonl`](data/inscriptions.jsonl)
has one row for each of the 652 inscriptions the project holds a reading of, with its REM or edition number, site,
kind and every reading's source and licence, and the text of the readings that are open;
[`data/inscriptions_map.tsv`](data/inscriptions_map.tsv) says what each of the 899 texts of `corpus_v5` is.
`data/corpus_v6.jsonl`, one row per inscription with real names, is local like the corpora before it.

Every folder of data the project holds, public or local, is listed in [`data/INDEX.md`](data/INDEX.md): what it
is, where it came from, the day it was fetched, its size and its rights, and what is not held.

## Methods

### 1. Cleaning the corpus

The public corpus repeats each text many times with person names swapped from two pools (data augmentation for
embeddings). `src/pool.py` finds the pools from one-slot differences between lines (a clique of 178 private names
and 11 royal names); `src/dedup.py` masks them as `NAME` / `RNAME` and collapses identical skeletons;
`src/collapse.py` merges copies that differ only where a multi-word name filled a `NAME` slot; `src/clean_v2.py`
masks the leftover multi-word names. `src/corpus.py` normalises Millet's spelling (`E` → `o`; capitals that only mark
uncertain readings lowered; `x`, `X` for the two h signs, `S` for the s sign, lowercase `s` for the se sign, `N` for
ñ) and adds the three royal narratives once. Result: 18,090 lines → 662 texts, about 18,100 words
(`data/corpus_v2.jsonl`). Several blind runs found leftovers of the padding; each finding fed the next cleanup.

### 2. Blind tasks and how leaks were caught

Every test is a task file in a folder under `/private/tmp/claude-501/blind/` (copies in `runs/tasks/`, local-only),
solved by a fresh subagent told to read only that file, with no web access; answers go to `runs/answers/`, keys to
`runs/keys/`. Agents report the tools they used, and several runs were asked afterwards whether they recognised the
language. Builders refuse to overwrite a folder a run has used, and `src/build_extra.py check` and
`src/cloze_families.py baseline` rebuild later tasks byte for byte from the repo and the local corpus snapshot
(Reproduce, below).

Leaks found and fixed along the way, each worth knowing for anyone repeating this:
- inscription names used as line labels in a "blind" file (the model recognised them);
- the corpus's own padding, which two restoration runs exploited to score 94% and 93%;
- a glossary plus the model's memory, which together break any letter substitution.

### 3. Step 0: can it recover held-out meanings? (`src/build_tasks.py`, `src/score.py`)

35 words with accepted meanings, split into two folds. Each task gives a glossary of one fold and asks the solver to
match the other fold's words to their meanings, one to one. Four conditions: memory only (M), real corpus (R),
corpus re-spelled with a random letter derangement (S, `src/scramble.py`), and re-spelled words with no corpus (S0).
Scored with an exact permutation p-value (the chance that a random matching gets as many right). All conditions
scored 35/35, and S0 shows why: the glossary lets a model that knows Meroitic invert the cipher.

### 4. A language it can't know (`src/synth.py`)

A generated corpus with the real corpus's scale and texture (1,003 texts, 16k words): funerary formulas, votive
texts, ration lists, labels and three royal annals; invented stems and endings; endings written fused or split;
masked names; lost signs. The same matching task, 52 usable test words over two folds (four dropped by review: absent,
too rare, or spelled like an ending), run twice independently. A blind grammar task on the same corpus is scored
against the generator's eight endings.

### 5. Natural experiments: what memory lacks

Open recall first ("unknown" allowed, no options), then the corpus task only for the words recall missed, so the
corpus has to supply what memory can't. Run twice: 17 words from the answer key (`N_open`), and 68 words glossed as
established or probable in Rilly's 2003 lexicon that occur in 2+ texts (`src/lexique.py`: names, gods, endings,
cross-references and ambiguous spellings excluded). Answers are scored by an independent judge agent against the
published meaning: SAME, TYPE (right kind of word only), WRONG, UNKNOWN (`runs/lexique_judge.json`). A late check
(`python3 -I src/lexique.py judged`) found that the corpus tasks' glossary gave six targets away (`qore` "ruler" listed
while `qor-o`, `qorise`, `qorene` and `qorode` were targets; `mk`, glossed "god, and very probably goddess", for
`mkdi`; `mlo` for `smlo`) and that three items shouldn't have been test words; the report gives the corrected
numbers, and the builder now leaves out of the glossary any word that gives a target away.

### 6. Restoration (`src/cloze.py`, `src/cloze_families.py`)

Mask words in held-out texts and restore them, against an n-gram restorer (2+2 context with backoff) that sees the
same texts as the solver, masks included. Version 3 groups texts into families of near-copies (shared word
trigrams, union-find), holds out 60 small families whole, and scores separately the masks with no parallel anywhere
in the task (no 12+ letter run around the word occurs elsewhere, spaces and case ignored). Compared with an exact
McNemar test.

### 7. Grammar, Kober-style (`src/build_morph.py`, `src/unscramble.py`)

The solver gets a corpus and no meanings and must find the recurring formulas, the bound morphemes, their functions
and the word classes. Run on the scrambled real corpus (scored against the 26 published endings) and on the
synthetic language (scored against the generator).

### 8. Is Meroitic visibly related to Nubian? (`src/cognates.py`, `src/cognates_rules.py`)

Do Meroitic words resemble same-meaning words in 10 Northern East Sudanic word lists more than chance? Raw string
similarity first, then an engine that scores alignments by Rilly's 82 sound correspondences. Validated against 2,000
shuffles of the Meroitic meanings, with Rilly's reconstructions and the words his rules were built from kept out of
the held-out test, because both were made with Meroitic in view. Candidate cognates for unknown words were allowed
only if the held-out test passed; it didn't.

### 9. Discovery runs and adversarial verification

Discovery agents read a text group (funerary formulas, the Hamadab stela REM 1003, the Philae near-bilinguals, the
Tanyidamani stela REM 1044) with web access, proposed hypotheses with evidence, alternatives and a test, and labelled
each ESTABLISHED, PUBLISHED HYPOTHESIS or NEW after a literature search. A separate agent was then told to prove each
NEW claim wrong: harder searches in English, French and German, FHN commentary, Millet's glossary, theses, and a
corpus check for counterexamples (`data/discovery/verification.md`).

### 10. Calibrated readings of unknown words (`runs/unknown/`)

Three independent runs read 29 frequent words of unknown meaning from the corpus, each answer with a strict 1–5
confidence and with evidence from the corpus kept apart from anything recalled. A reading counts only if two runs
agree at confidence 4 or more.

### 11. Reading the script from images (`data/discovery/vision.md`, `data/expansion/`)

Photographs of inscriptions (Wikimedia), Griffith's printed type and Griffith's hand copies. Each reading was written
down, with a timestamp, before the modern transliteration (FHN) was opened, then scored sign by sign; misreadings
are separated from places where Griffith's 1911 reading differs from the modern one.

### 12. Growing the corpus (`src/expand.py`)

Five agents transcribed Griffith's printed inscriptions sign by sign into standard transliteration and the corpus
spelling, marking uncertain signs, with the REM number where there is one (REM 0001–0137 follow Griffith's
numbers). `src/expand.py` drops texts already in the corpus or repeating an earlier Griffith text (half or more of a
text's letter 6-grams occur in one such text, or one with masked names or lost signs spells all of it, both spelled
alike first) and writes `data/corpus_v3.jsonl`. Griffith printed only part of 29 of the 152 texts; those are left
out.

Griffith gives the Karanòg and Shablûl inscriptions only as hand copies, which one reader gets 89% right. But
the same book prints most of their words a second time in type: a table of names, three indexes and tables of the
closing formulae. Readers typed those 48 pages, read each hand copy on its own, and then checked the reading
against the printed entries for that inscription (`src/karanog_refs.py`, `src/karanog.py`,
[`data/expansion/karanog/README.md`](data/expansion/karanog/README.md)). On the four texts FHN prints, fresh
readers who could not see FHN reached 97.7% of signs. Eleven pages (31 inscriptions) were then read again by a
second reader: the two checked readings agree on 97.7% of signs there (98.8% for all 53 pages, weighting the
seven most damaged and the three drawn at random by the pages they stand for), and the 56 places where they
differ were settled against the copy and the type. `src/karanog.py` divides the closing formulae into words as
Griffith's tables do, but for a few rows where the stone has a divider or the typed table differs in a sign.
`src/expand.py` tests the 151 texts against `corpus_v3` but not against each other, as they are separate
inscriptions that share their formulae, and leaves the letter groups of those formulae out of the comparison. It
finds all 151 new and writes them with `corpus_v3` as `data/corpus_v5.jsonl` (899 texts, 21,977 words);
`corpus_v3` itself is left as it was.

### 13. Review

Code changes were reviewed by a fresh Opus 5.5 reviewer that saw the diff and a context pack, never the author's
reasoning, and fixed what it found (four full reviews; the fourth, of `src/lexique.py` and `src/expand.py`, was
stopped partway on Mike's word so the repo could be pushed, and finished before it was shared). They found and fixed
answer leaks, a Monte Carlo p-value printed as 0.0, a baseline that saw less than the solver, a corpus bug that split
words at doubtful-sign marks, a copy detector that missed copies, and rules applied outside the positions Rilly gives
them; each fix changed a reported number, and the report shows the corrected one. Five more full reviews followed
on 2026-11-09 and 10, two of the Newsletter tools and three of the Karanòg scripts and rows; they fixed, among other
things, a scorer that let extra signs go free, references misread as inscription numbers, an editor's "(sic)"
counted as two signs, and formula words that the uniform rows still divided two ways. Tests: `tests/`.

### 14. How much can be translated today (`src/coverage.py`)

Every word of `corpus_v5` gets a gloss, a level and a confidence. A word that is a spelling of an entry of Rilly's
lexicon takes that entry, alone or as a stem with a known ending; masked names, numbers and the names of Griffith's
Karanòg tables are settled the same way. The 1,887 words this leaves went to seventeen independent analysts with
their contexts and the lexicon as a table: each cut the word into parts (an entry, a name, a number or an unknown
piece) and named its kind, and the script kept an answer only if its parts spell the word and its entries exist.
Two more analysed 230 of the most frequent a second time; where the two differ in level, the lower stands. A word
counts as translated when the parts that are words of their own are names, numbers or entries Rilly holds as
established or probable, and an analyst's cut has a confidence of 4 or 5. Near-copies of a text are counted once
in the headline and in the ranking of what blocks most texts. The gloss file leans on the
lexicon and is local-only; the counts, the brief and the list of unknown pieces are public
([`data/discovery/coverage.md`](data/discovery/coverage.md)).

Four corrections follow the first build (`correct`), each a rule: the rest of a masked name of several words that
the padding of the older corpus left behind its mask ("mokelowi", "mete l") is part of the name; a stem of two
signs counts as three letters when one of them is the sign se or ne and Rilly holds the entry as established
(`smlowi`, "is the wife of"); two or three neighbouring words are one word written apart when one of them has
one or two letters and the whole also stands written as one elsewhere (`wo Si` for `woSi`); and a piece that two
blind checkers took for a spelling of a word with an accepted meaning takes that meaning (for two of them,
`mXeyot` and `yetmetl`, the pack showed a word with their letters, and their gloss says so), as do three forms
of "sister" that a reader of the families of Karanòg read so. The corrected map is written beside the first one, whose list the Egyptian and the
variants searches read.

### 15. Egyptian words behind Meroitic ones (`src/egyptian.py`)

A scorer that knows only letters: Meroitic, Demotic and Coptic words are reduced to their consonants in one
alphabet, and an Egyptian word becomes a Meroitic one letter by letter (kept, changed, dropped, or with the article
p or t in front), with chances counted from the aligned known loans. The answer key is the 35 entries of Rilly's
lexicon that two independent readers took as accepted borrowings; each is searched with a model trained on the
others, among the entries of its own kind and then with the neighbouring kinds added (titles with nouns). A match
counts only as far as it beats the best matches of made-up words of the same length; the 64 words with an
accepted meaning and no Egyptian link beat that bar about as often as chance would (0 to 5 times, where 3 are
expected). The best matches for the unknown pieces went to two blind checkers with unmarked decoys. A second run
(`vowels`) compares the written vowels as well, on the Coptic entries only, since Demotic writes none, and keeps
the consonant figures of the same pool beside its own. The word lists, the key and the result files are
local-only; the page, the brief and the two lists of candidates are public
([`data/discovery/egyptian.md`](data/discovery/egyptian.md)).

### 16. Spellings of known words among the unknown pieces (`src/variants.py`)

The same scorer turned on Meroitic itself: each piece of the coverage map's list is compared, vowels included,
with the 688 words of Rilly's lexicon (655 different headword spellings), and may carry one of the 25 known
endings, which the search takes as the Egyptian search takes an article, on words read from their end. The model
starts flat, with no groups of like letters, and counts which letters alternate on the 307 spelling variants that
the lexicon lists under its entries. The test hides each listed variant of a word in turn, everywhere in the
lexicon, trains on the rest and asks for the entry that lists it as the single best match. The bar was written
down before the first run. A match counts only as far as it beats the best matches of 1,000 made-up words of the
same length, and the words with an accepted meaning that the lexicon links to nothing go through the same search,
to see what that yardstick is worth. Every match that beats the bar is packed for two blind checkers with 24
listed variants whose answer is known: 12 with the right entry among the candidates, and 12 decoys with it taken
out. A pack shows under a word only what the coverage map counts as translated or what the lookup took from the
lexicon, never an analyst's guess, and nothing under a word that the map finds the piece in (three items still
showed a word with their own letters that the map cuts otherwise, and the page also gives the count without the
two of them that were confirmed). A piece is confirmed when both
checkers say it is the same word and name one candidate; the script then counts, on the map's gloss file, the
running words that would move, and leaves the map as it is. The lexicon, the gloss file and the result files are
local-only; the page, the brief, the list of every searched piece with its best match and the list of the
confirmed pieces are public ([`data/discovery/variants.md`](data/discovery/variants.md)).

### 17. The map against two printed editions (`src/experts/`)

The coverage map has one source of meanings, so its figure was set beside two others: Millet's edition of the
Gebel Adda inscriptions (2005) and the entries on Meroitic texts in *Fontes Historiae Nubiorum* III (1998). An
entry is matched to a corpus text by the runs of five letters the two share, counted in both directions, and the
pairs are then read side by side (31 texts). A pack gives a judge the edition's printed entry and, beside it, our
words in order with our reading of each; the judge marks every word agree, partly, differ, new, silent or absent
and notes the edition's meaning. One judge reads each of three packs and a second reads one of them again. A
tenth of the readings with a meaning are swapped for another word's, unmarked, and left out of every figure: they
measure how lenient a judge is. A second pass lists every meaning the editions give at all (two readers), looks
each word up as the map does, and has two judges compare the meanings; there each judge sees decoys of its own
in place of our reading, on different lines, drawn so that a decoy shares no content word with our reading or
with the edition's meaning. The editions, the packs and the answers are local-only; the page, the figures and a
list of the words with their verdicts, without readings, are public
([`data/discovery/experts.md`](data/discovery/experts.md)).

### 18. One inscription once (`src/v6/`)

`corpus_v5` holds copies, masked names and phrases quoted in a grammar beside inscriptions. `src/v6/otten.py`
traces each of its older texts to the line of Otten's per-scholar files it was padded from: the line itself, or
the line with one stretch swapped. `src/v6/readings.py` lists every reading held (Griffith's print, the Karanòg
copies, the Newsletter, Millet 2005, FHN III, Otten's narratives and source lines) with the numbers its edition
gives, and compares texts by their runs of five letters, the formulae left out. `src/v6/build.py` makes the
inscriptions: readings that share a number are one, two different numbers of one numbering are two, and a text
without a number goes by letters, where a sure match to one inscription stands and a doubtful one goes to two
readers who see both texts, with known lines and decoys mixed in (`src/v6/packs.py`). A source line is a
reading of an inscription, an example phrase from a grammar, or an inscription not identified; one reading per
inscription is preferred by a fixed order, with the numerals another edition shows and Otten's name tags. The bar for the rule was written before it was scored, and missed.
`src/v6/recount.py` runs the coverage map and the check against the two editions on the new rows, without a new
analyst or judge, and `src/v6/public.py` writes the public table, the map of the old ids and the tables of the
page ([`data/discovery/corpus_v6.md`](data/discovery/corpus_v6.md)).

### 19. Analysts on the unread spellings of the clean corpus (`src/v6/readers.py`)

The recount of step 18 ran without a new analyst, so the spellings that `corpus_v5` does not have stood with the
lookup alone. `src/v6/readers.py packs` takes the words the lookup leaves on `corpus_v6`, without the words an
edition tags as personal names and without those a pack of the first run holds, and writes them into packs like
those of step 14, numbered after them and kept in a folder of their own; the most frequent go into one more pack
for a second analyst. `count` runs the corrected map of `corpus_v6` twice, with the first run's answers alone and
with the new ones added, and reports what moved. The bar on the two analysts' agreement and the gain expected
were written down before the run ([`data/discovery/v6_readers.md`](data/discovery/v6_readers.md)).

### 20. The same people in two scripts (`src/demotic.py`)

The entries of *Fontes Historiae Nubiorum* III are cut from the volume's text layer at the headings that
continue its numbering. Two readers take the 24 Demotic and Greek entries and one the nine Meroitic entries of
the same families; each lists the people an entry's ancient text names, with their titles, their kin and whom
the editors take for the same person elsewhere, and every place where the editors set a Meroitic word beside a
Demotic, Greek or Egyptian one. `merge` joins the lines into people (the same name in the editors' English, or
the editors' own identification, matched by the consonants of the name as the editors or the ancient text write
it, and never to a namesake with another letter or number) and checks two bars written before the run: how many
person lines both readers list, and whether both find the known equations. The equations go through the lookup
and the judges' table of step 17, each judge with decoys of its own
([`data/discovery/demotic.md`](data/discovery/demotic.md)).

### 21. A second scholar for every meaning (`src/lexicon.py`)

`layout` lists every entry of the lexicon that the map of the clean corpus uses, with Rilly's status and page,
the proposals of other scholars that the lexicon records, and the editors' verdicts of step 17 on words built on
the entry (without the words that step found the map misreading). `packs` sets each proposal on an entry Rilly
states as a meaning or a grammar word beside the lexicon's meaning, without the scholar's name, for two judges,
each with decoys of their own: another entry's meaning from outside the line's field of meaning. `check` sends a
sample of the lexicon's citations of Griffith to a reader with Griffith's own texts. The bars and the rules for
the four statuses were committed before any judge answered. `round2` gives each judge again, with the real
proposal, the lines where it saw a decoy, beside a few new decoys, and a writer the meanings to word anew;
`round3` gives both judges every proposal on the other entries the map uses and on the names, beside decoy lines
under new numbers; `public` counts the three rounds and writes the figures and two tables of headwords, each
meaning in words of our own for the entries behind translated words (checked to copy no four words in a row of
the lexicon's), statuses, the scholars cited, the editors' verdicts counted, spellings and the pages of the
statements (`src/lexicon_refs.py`) ([`data/discovery/lexicon.md`](data/discovery/lexicon.md)).

### 22. Whole texts translated and scored, a pilot (`src/f4.py`)

`choose` takes five of the texts Millet's Gebel Adda article (2005) renders into English, one of each kind of
object and three stelae of different lengths, and five texts under an open licence for the cost of a page.
`packs` writes, for a translator agent, each text with the map's reading of every word and the lexicon's entries
with F2's statuses, Millet taken out of all of it (his proposals, the meanings that name him, and his weight in
the statuses); the map's glosses in order are the baseline; a splitter agent cuts Millet's renderings into units
of meaning. `judges` gives two judges each unit beside three unmarked readings in an order of its own: the
translator's, the baseline, and a decoy, the translation of another text sharing as few content words with the
rendering as can be. The bars and the expected scores were committed before any agent answered; `public` writes
the counts ([`data/discovery/f4_pilot.md`](data/discovery/f4_pilot.md)).

### 23. Ways of translating compared, then scored once on held texts (`src/f4r.py`)

`split` writes one splitter's pack for each of the 18 renderings: the pilot's instructions, but a unit is open
only when all of it is untranslated. `handbook` applies the checkers' verdicts (confirmed, corrected,
unsupported) to the handbook its compiler wrote (the instructions both were given by hand are in
`runs/prompts/F4R_handbook_*.md`), and no pack is built from a handbook that was not checked or that names
Millet. `packs` writes, one text to a pack, the writer's pack (the map's reading of each word with its status,
the rules and the handbook) and three translators' packs (the pilot's materials, the rules, the handbook and
the parallels: up to three other places of the corpus for each word, with the map's readings around it);
`editors` writes the pack that makes one translation of the three; `judges` gives two judges each text's units,
at most 20 a pack, beside the readings in an order of their own, with a decoy. A round can judge another
round's readings again (`r1b`, with the rule on kinship). `count` gives each reading's score, its wrong units,
its lead over the glosses unit by unit, the judges' agreement, the decoys and the reading carried on by the rule
set beforehand, none when a bar of the judging is missed ([`data/discovery/f4_rounds.md`](data/discovery/f4_rounds.md)).

### 24. The unread spellings that recur (`src/recurring.py`)

`items` groups the open spellings that stand in three texts or more by the lexicon entry they are filed under,
each with every place it stands. `batches` writes one dossier a batch for the readers who collect what the
sources say (`runs/prompts/RECURRING_literature.md`); `quotes` keeps a statement only when its quote stands in
the file named, and sorts the items into three classes by rule. `verify-packs` and `verify` give the items for
which a later source states a meaning to two readers, and an item passes only when both find it stated firmly
in the same source. `place-packs` and `places` give every place to two checkers (stated, a piece of another
word, open, unclear): a place counts only where both agree, and nothing is taken if their kappa is under 0.6.
`cand-packs` and `cands` list the meanings on record for the items that stay open, kept when two readers list
them. `choice-packs` builds the blind test: each word a code, its places as the map's readings of the words
around it with no spelling and no text number, four meanings of one kind, and among the open words accepted
words with and without their true meaning offered; `choice` counts the choices of five readers against two
bars. `recount` lays the results over the map without changing it. Every bar was set before the agents it binds
were started: committed for the place pass and the blind test, written in the working script for class A; a
command that writes packs refuses once an agent of its step has answered. The page gives the commits and the
times ([`data/discovery/recurring_words.md`](data/discovery/recurring_words.md), section 9).

### 25. Distinct words (`src/words.py`)

`population` says of every running word of the map that needs a meaning what word it is, by the rule set before
the checkers: a word of the lexicon (every spelling built on one entry is that entry), a name, or a stem the map
could not name. `packs` draws 240 of those stems by a fixed seed and writes them for two checkers, each stem with
its places and the spellings that look like it; `count` compares the two (a stem has a case only when both give
it; under a kappa of 0.6 nothing is taken) and estimates how many of the stems are words of their own, with a
range. `public` counts the words of the lexicon again with the review's two corrections, which leave the stems as
they are: an ending or a particle written as a word of its own is a piece, and an entry of any kind of name is a
name. The share of distinct words that have a meaning is the
translated words of the lexicon over the words of the lexicon in use plus that estimate; before the project it was
the same, since every one of those meanings is in the lexicon of 2003, and what a plain lookup of the lexicon
reaches is given apart, as the reach of the map
([`data/discovery/distinct_words.md`](data/discovery/distinct_words.md)).

### 26. The map and its layers (`src/themap.py`)

The analysts' map stays as it is. A later study that resolves places hands over a file of lines, one for each
running word it changes: the text, the word's number, its spelling, the new level and meaning, the reason (a
later source states the meaning there; a piece of a word or name the map holds; a name) and the source. The
script lays these layers over the map in their order each time it runs and stops if a line does not fit: a place
or spelling the map does not have, two lines for one place, a former level that is not the map's, a level that
does not resolve the word. It then
counts the map as it stands: the running words and the distinct spellings that need a meaning and have one, the
same for the base and for a plain lookup of the lexicon, and the distinct words, where a word of the lexicon
counts as translated if the lexicon calls its meaning established or probable or a layer gives it one from a
later source. The estimate of how many unnamed stems are words is carried from section 25's sample while the
layers take at most 2% of those stems out of the unnamed ones; past that it is made again, by the same rule,
from the sampled stems that are still unnamed, and the script stops if a layer adds a stem the sample was not
drawn from. The status table reads its first three rows from
this count ([`data/discovery/map_layers.md`](data/discovery/map_layers.md)).

### 27. The open spellings in one or two texts (`src/rare.py`)

The steps of section 24 again, in a folder of their own, for the open spellings that stand in one or two texts
and hang on an entry of the lexicon. For an entry without an accepted meaning: a literature pass (one reader a
batch of twelve entries, each with the pages of Rilly 2016 and 2021 on which a script finds the headword; every
quote looked for in its file), the entries for which Rilly states a meaning read by two readers, and every place
of those entries and of the ones a reader calls a piece judged by two checkers. For an entry the lexicon calls
sure, only the place pass, with the lexicon's own line in the place of a later statement. A reading of the
places counts only if both checkers answered every place and their kappa is 0.6 or more; if not, the brief is
corrected and fresh checkers read the same packs. `layers` then writes what goes into the map: a stated place
only where the map names every part of the spelling and every stem among them has a meaning; a name where the
entry is one; a piece where the whole word both checkers name is translated or named in the map. The rest is
counted apart and stays open ([`data/discovery/rare_spellings.md`](data/discovery/rare_spellings.md)).

### 28. The open spellings the lexicon does not hold (`src/unnamed.py`)

For each open place of a rare spelling that hangs on no entry of the lexicon, two checkers say whether it is a
name, a piece of a word beside it (they name the whole), a word of its own, or unclear. They see the word, five
words on each side and the map's reading of each, with the word itself shown as unknown, and open no file. Among
the real places stand controls whose answer the map holds and which look the same: translated words built on a
stem of the lexicon, names the analysts recognised that are no entry of the lexicon, and, in the first pilot,
spellings the script cut in two. Where joining the word with a word beside it gives a spelling the map holds,
the pack says so in a note. A reading counts only if both checkers answered every place, their kappa is 0.6 or
more, and each checker calls at most a tenth of the control words a name and at least seven control names in
ten a name. `layer` then writes what goes into the map: a name where both say so; a piece only where both name
the same whole word and the map holds it as translated or named
([`data/discovery/unnamed_spellings.md`](data/discovery/unnamed_spellings.md)).

### 29. A second scholar for the later meanings (`src/second_later.py`)

The method of section 21 on the meanings a later source gave in sections 24 and 27. Each meaning stands beside
every statement of another scholar about its entry: those the literature passes collected from the scholars'
own works (a statement that takes a stance on a meaning, not a bare mention), and the proposals the lexicon of
2003 reports. A tenth more rows are decoys, a meaning beside a statement about another entry. Two judges say of
each row: the same meaning, partly, another, or none stated. The rows count only if both judges answered all of
them, their kappa on "same" against the rest is 0.6 or more, and each took at most a tenth of the decoys for the
same. A meaning is agreed by two scholars when both judges call one of its rows the same, disputed when none is
and both call one another meaning, and stated by one otherwise
([`data/discovery/second_scholar_later.md`](data/discovery/second_scholar_later.md)).

### 30. The leftover parts, and what Millet and Lipiński state (`src/leftover.py`)

Part 1 shows two checkers each place with the spelling's parts as the map cuts them, the named ones with their
entry of the lexicon and the unnamed ones marked. They say whether the unnamed part is nothing but endings, a
known word (they name its entry), a name, unknown or unclear. Among the places stand controls that look the
same: translated words whose endings are shown as unnamed, and translated words with three to five letters
drawn by lot attached. A reading counts only if both checkers answered every place, their kappa is 0.6 or more,
each calls at least 14 of the 20 hidden endings an ending, and each explains at most 2 of the 20 runs of lot
letters. The first reading missed the last of these bars by one answer and is not taken. The second reading
(`packs-again`, `count-again`) keeps the places and the brief, draws the controls anew and has a bar for each
verdict: its bar on the lot letters counts only an ending or a known word, and a place both checkers call a name
is not laid. `layer-again` writes what it lays: a place both call an ending, or a known word and the same one,
unless another stem of the spelling has no meaning
([`data/discovery/leftover_parts_2.md`](data/discovery/leftover_parts_2.md)). Part 2 is the method of section 27
with the source changed: two readers read what Millet 2005 or
Lipiński 2011 states about an entry and say what it gives (a name, a meaning in full, or a meaning that leaves a
Meroitic word as it is), and two checkers judge each place. `layer` writes what goes into the map: a translated
word only when both readers say the meaning is given in full; a name when the lexicon files the entry as one or
both readers say the source calls it one ([`data/discovery/leftover_parts.md`](data/discovery/leftover_parts.md)).
Part 3, the leftover stems (`packs-stems`, `count-stems`, `layer-stems`), gives two checkers the 86 places of the
same kind where the entry recognised is an ending or a particle and the unnamed part is the stem itself, with the
same brief. Four kinds of control are mixed in, 20 of each: a translated word with its stem shown as unnamed (the
answer: a known word, that entry), one with its endings shown as unnamed (ending), a name with endings and the
name shown as unnamed (name), and a translated word whose stem's letters are replaced by letters drawn by lot
(none of the three). The first, second and last kinds are each drawn from 20 different entries of the lexicon,
as the rules said; the names are the 9 personal names the map holds and 11 places of 7 names of the lexicon, drawn
by place, and the page counts their bar once a name as well. Both checkers must answer every place with a
kappa of 0.6 or more; beyond that each verdict stands on its own bars and is laid only if they are met: each
checker finds it at least 14 times in 20 where it is hidden, and says it at most 2 times in 20 of the lot
letters (a name also at most 2 times in 20 of the hidden stems). A known word and a name are laid only where the
spelling has one unnamed part, and a known word only when both checkers name the same entry, which the lexicon
calls established or probable ([`data/discovery/leftover_stems.md`](data/discovery/leftover_stems.md)).

### 31. The blind test again (`src/blind2.py`)

The choice test of section 24 with three changes, set before any reader was started. A choice needs all five
readers. The four options under a word are filled by lot from one pool of accepted meanings and proposals, so
that a proposal no longer stands out by its wording (by that lot, 63 of the 76 words have both sorts among their
four). A filler is never a meaning that no context could tell apart from another option of its word (bull and
cow); an open word's own proposals stay together as the sources give them. The accepted words are the 38 of the
first test and the 5 further entries of the lexicon that have a meaning of their own; in each kind every third by
lot is shown without its true meaning. The bars are those of the first test
([`data/discovery/blind_test_2.md`](data/discovery/blind_test_2.md)).

The run with all 83 accepted words (the commands `words-83`, `packs-83` and `count-83`) takes in the 40 entries
the first run left out, each with the meaning the lexicon gives it in a few words of our own. Twenty-one of them
have only a coarse meaning ("a priestly title", "an administrative title"); such a meaning is the true meaning
of its own words and is never drawn as a filler, since it would be true of any title of its sort it stood
beside. Five groups of near meanings are added, the readings shown are those of the map with its six layers, and
the accepted words' outcomes are also counted by sort of word, because the coarse meanings and the forms of
words already in the test are weak test items
([`data/discovery/blind_test_83.md`](data/discovery/blind_test_83.md)).

### 32. Grammar first, a pilot (`src/grammar.py`)

`split` deals the texts by lot into a tuning set and a held-back set, 40% of each kind of text held back and the
long texts apart; it is drawn once. `dump` writes the tuning texts as a table, one word a line: the spelling, the
map's level, the parts with their entries and a short gloss. A finder, a fresh agent with one angle, sees that
table alone and gives at most 8 rules, each with its cases, what must hold there and a comparison rate, and
writes each rule's count as a function over the table's columns (`runs/grammar/`). `tuning` checks that every
function gives its finder's counts. The functions are committed, and only then does `held-dump` write the
held-back table and `held` run them on it, once: a rule passes with at least 20 cases, holding in at least 80%
of them, at least 30 points above its comparison. `packs` gives the rules that passed to two readers, who search
the sources in hand for each, and `count` calls a rule a finding of ours only when both find it in none. The
second round (`briefs2`, `tuning2`, `held2`, `packs2`, `count2`) does the same on the texts that are not
funerary, with six finders and at most 6 rules each. The figures give every rule with its counts and its
readers' verdicts; a statement that shared four words in a row with a source is reworded there. `parse` cuts the long
texts by the rules that passed: after every word a rule marks as the end of a clause, a sentence or a phrase,
only where that rule has its case and holds, and says of each word without a meaning what a rule that passed
makes of it there, or that none speaks of it; two ends that only a rule's wording names are counted apart and do
not cut
([`data/discovery/grammar_pilot.md`](data/discovery/grammar_pilot.md)).

### 33. Griffith's ostraca and Sayce's reading (`src/ostraca.py`, `src/sayce.py`)

The pages are rendered from the PDFs at high resolution, and every text is typed by hand from the images, never
from the text layer, which drops the marks that carry the signs (ê, š, ñ, ḫ, ẖ, the dot below a doubtful sign).
Every h, every s and every dotted letter is looked at again on a crop of its line enlarged six to sixteen times.
The bar and the lot are committed before the typing: a tenth of the texts, drawn with `secrets.SystemRandom`, is
typed again by a fresh agent that sees the page images and the typing rules only, and the two typings must
agree on 97% of the signs (difflib over the signs of each text). `src/ostraca.py` writes one row per ostracon
(his text as printed, the corpus spelling, the words by line, the doubts: his dots and queries, his notes, ours);
`src/v6/readings.py` reads them as open readings numbered by the article's siglum, since they carry no REM
number. `src/sayce.py` maps Sayce's letters to Griffith's by a table fixed before the comparison and counts how
often each of his units lines up with each of Griffith's signs, lines the two texts up letter by letter, and
classes Griffith's doubted words by what Sayce reads at the same place (classes fixed before the comparison);
against the closed readings it writes counts only
([`data/discovery/ostraca_sayce.md`](data/discovery/ostraca_sayce.md)).

## Reproduce

From a clone of this repository and Otten's corpus, with nothing else:

```bash
git clone https://github.com/Joshua-Otten/Meroitic-Corpus data/otten
python3 -I src/pool.py && python3 -I src/dedup.py && python3 -I src/collapse.py && python3 -I src/corpus.py && python3 -I src/clean_v2.py
python3 -I src/expand.py
python3 -I src/score.py --answers runs/answers
python3 -I tests/test_harness.py && python3 -I tests/test_cognates_rules.py && python3 -I tests/test_lexique.py
python3 -I tests/test_karanog.py && python3 -I tests/test_newsletter.py && python3 -I src/mnl/test_mnl.py
python3 -I tests/test_coverage.py && python3 -I tests/test_egyptian.py && python3 -I tests/test_variants.py
python3 -I tests/test_experts.py && python3 -I tests/test_corpus_v6.py && python3 -I tests/test_akinidad.py
python3 -I tests/test_v6_readers.py && python3 -I tests/test_demotic.py && python3 -I tests/test_lexicon.py
python3 -I tests/test_f4.py && python3 -I tests/test_f4r.py && python3 -I tests/test_recurring.py
python3 -I tests/test_words.py && python3 -I tests/test_themap.py && python3 -I tests/test_rare.py
python3 -I tests/test_unnamed.py && python3 -I tests/test_second_later.py
python3 -I tests/test_leftover.py && python3 -I tests/test_blind2.py && python3 -I tests/test_grammar.py
python3 -I tests/test_findings.py && python3 -I tests/test_ostraca.py && python3 -I tests/test_sayce.py
```

The second line ends `texts 662; tokens 18075; types 1622` (`data/corpus_v2.jsonl`). The third prints
`corpus_v2 662 texts 18075 words -> corpus_v3 748 texts 19066 words (+5%)` and ends
`corpus_v3 748 texts 19066 words -> corpus_v5 899 texts 21977 words (+15%)`. The tests print `skip` for each
check that reads a local-only file, and each file's last line counts the checks passed and skipped
(`src/mnl/test_mnl.py`, a unittest file, ends `OK`); none fails.

Twenty-four things need files that are kept locally (Data, above), so they don't run from a clone:

- `python3 -I src/cloze_families.py copies runs/answers/C3_cloze.json runs/cloze_families_ngram.json` and the other
  restoration checks read the corpus snapshot several runs used (`data/corpus_v2_c3_snapshot.jsonl`, taken before
  the review's fixes to `src/corpus.py`, so it can't be rebuilt);
- `python3 -I src/lexique.py judged` (and the lexicon test's other commands) reads Rilly's lexicon;
- `python3 -I src/cognates_rules.py` reads the NES word lists and Rilly's sound correspondences;
- `python3 -I src/coverage.py first` (and `build`) reads Rilly's lexicon, `corpus_v5` and the analysts' answers;
- `python3 -I src/egyptian.py first` (and `build`, `vowels`) reads the two Egyptian word lists, Rilly's lexicon and the
  answer key drawn from it;
- `python3 -I src/variants.py first` (and `build`, `sample`, `check`, `merge`) reads Rilly's lexicon, `corpus_v5`
  and the coverage map's gloss file;
- `python3 -I src/experts/tally.py` (and the other scripts of `src/experts/`) reads the two editions' text layers,
  the coverage map's gloss file, Rilly's lexicon and the judges' answers;
- `python3 -I src/v6/build.py` (then `src/v6/recount.py` and `src/v6/public.py`; `src/v6/readings.py test` for the
  bar) reads Otten's files, `corpus_v5`, the Newsletter texts, the two editions' text layers, and for the recount
  Rilly's lexicon, the analysts' answers and the judges' answers;
- `python3 -I src/v6/readers.py count` reads Rilly's lexicon, `corpus_v6` and the analysts' answers of both runs;
- `python3 -I src/demotic.py merge` (and `packs`, `table`, `count`) reads the text layer of FHN III, the readers'
  and judges' answers, Rilly's lexicon, the coverage map's gloss file and the lines of the check against the two
  editions;
- `python3 -I src/lexicon.py public` (and `layout`, `packs`, `check`, `round2`, `count`) reads Rilly's lexicon, the
  coverage map's gloss file of the clean corpus, the check against the two editions, the judges' and the writer's
  answers, and for the check, Griffith's own texts.
- `python3 -I src/f4.py count` (and `choose`, `packs`, `judges`, `public`) reads the text layer of Millet 2005,
  `corpus_v6` and its gloss file, Rilly's lexicon, F2's judges' answers, the check against the two editions and
  the translators', splitter's and judges' answers.
- `python3 -I src/f4r.py count r1` (and `split`, `handbook`, `packs`, `editors`, `judges`, `public`, `show`; the
  rounds `r1`, `r1b` and `held`) reads what `src/f4.py` reads, the handbook and its checkers' verdicts, and the
  splitters', writers', translators', editors' and judges' answers.
- `python3 -I src/recurring.py public` (and `items`, `batches`, `quotes`, `verify-packs`, `verify`, `place-packs`,
  `places`, `cand-packs`, `cands`, `choice-packs`, `choice`, `recount`) reads `corpus_v6` and its gloss file,
  Rilly's lexicon, the text layers of the sources and the readers' and checkers' answers.
- `python3 -I src/words.py public` (and `population`, `packs`, `count`) reads `corpus_v6` and its gloss file,
  Rilly's lexicon and the checkers' answers.
- `python3 -I src/themap.py` reads `corpus_v6` (for the plain lookup) and its gloss file, the layers' lines,
  Rilly's lexicon and the figures of the count of distinct words.
- `python3 -I src/rare.py public` (and `layers`; for the runs `g4` and `g2`: `items`, `batches`, `quotes`,
  `verify-packs`, `verify`, `place-packs`, `places`, `place-packs2`, `places2`) reads `corpus_v6` and its gloss file,
  Rilly's lexicon, the text layers of the sources, the layers' lines and the readers' and checkers' answers.
- `python3 -I src/unnamed.py public` (and `pilot-packs`, `pilot`, `pilot2-packs`, `pilot2`, `full-packs`, `full`,
  `layer`) reads `corpus_v6` and its gloss file, Rilly's lexicon, the layers' lines and the checkers' answers.
- `python3 -I src/second_later.py public` (and `rows`, `packs`, `count`) reads Rilly's lexicon, the statements the
  literature passes of sections 24 and 27 collected, the two readers' results and the judges' answers.
- `python3 -I src/leftover.py public` (and `packs`, `count`, `packs-again`, `count-again`, `layer-again`, `setup`,
  `verify-packs`, `verify`, `place-packs`, `places`, `layer`, `packs-stems`, `count-stems`, `layer-stems`) reads `corpus_v6` and its gloss file, Rilly's lexicon, the layers' lines, the results of
  section 27, the text layers of Millet 2005 and Lipiński 2011, and the readers' and checkers' answers.
- `python3 -I src/blind2.py public` (and `words`, `packs`, `count`, and the same three ending in `-83` for the
  run with all 83 accepted words) reads `corpus_v6` and its gloss file, Rilly's lexicon, the layers' lines, the
  proposals collected in section 24 and the readers' answers of both runs.
- `python3 -I src/grammar.py public` (and `split`, `dump`, `briefs`, `tuning`, `held-dump`, `held`, `packs`,
  `count`, the five ending in `2` for the second round, and `parse`) reads `corpus_v6` and its gloss file, the layers'
  lines, the tables of the two sets, the finders' rules and the readers' answers.
- `python3 -I src/rem_pilot.py public` (and `index`, `pick`, `packs`, `score`, `estimate`) reads the REM volumes'
  text layers and plate pages, the readers' answers and the analysts' map of `corpus_v6`.
- `python3 -I src/captions.py public` (and `count`, `packs known`, `judges known`, `score known`) reads the caption pilot's
  inventory, its cut pictures, the readers' answers, the judges' scores and the map with its layers.

## Layout

- `src/`: corpus cleaning, task builders, scorers, the synthetic language, cognate tests, lexicon test, merge,
  the translation coverage map (`coverage.py`), the search for Egyptian sources (`egyptian.py`), the search
  for spellings of known words (`variants.py`), the check of the map against two printed editions (`experts/`),
  the corpus keyed by inscription and its analysts (`v6/`), the same people in Demotic, Greek and Meroitic
  (`demotic.py`), the second scholar for every meaning (`lexicon.py`), whole texts translated and scored
  (`f4.py`, the pilot, and `f4r.py`, the rounds), the unread spellings that recur (`recurring.py`), the count
  of distinct words (`words.py`), the map with its layers (`themap.py`) and the open spellings in one or two
  texts (`rare.py`), the open spellings the lexicon does not hold (`unnamed.py`), the second scholar for the
  later meanings (`second_later.py`), the leftover parts and what Millet and Lipiński state (`leftover.py`),
  the blind test again (`blind2.py`) and the grammar-first pilot (`grammar.py`).
- `tests/`: the checks; `tests/local_only.py` lets a check skip when a local-only file is absent.
- `data/`: answer keys, leads, discovery write-ups, the Griffith transcriptions (`data/expansion/`) and the table
  of inscriptions (`inscriptions.jsonl`, `inscriptions_map.tsv`); the cleaned corpora (`corpus_v2.jsonl`,
  `corpus_v3.jsonl`, `corpus_v5.jsonl`, `corpus_v6.jsonl`), the word lists and Rilly's lexicon are local-only.
- `runs/`: prompts, the task each blind run saw, its answers, keys and scores; `runs/work/` holds the agents'
  working files (transcription scripts, timestamped blind readings); `runs/grammar/` holds the tests of the
  grammar pilot's rules, one function a rule, as they were frozen.
- `docs/report.html`: the summary page's source; `docs/index.html` is the same page as GitHub Pages serves it
  (`python3 -I tests/test_harness.py pages` rebuilds it).
- `LICENSE` (MIT, the code) and `LICENSE-DATA.md` (CC BY 4.0, the data and write-ups, with what is excepted).
- `REPORT.md`: the results. `NEXT_STEPS.md`: what to do next.

## Licence

The code is under the MIT licence ([`LICENSE`](LICENSE)). The Griffith transcriptions, the answer keys, the runs and
the write-ups are under CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)), which also lists the third-party material
that keeps its own terms: the Wiktionary list and the list of Egyptian candidates (CC BY-SA 4.0), the readings
quoted from *Fontes Historiae Nubiorum*, the single words quoted from Millet 2005 and the glosses paraphrased
from Rilly's lexicon.

## Limits

- Blind tests on real Meroitic can't exclude memory: the model has read the decipherment literature.
- The synthetic language's difficulty depends on its generator.
- Judges and readers are the same model family; scoring files are kept line by line so a person can re-judge.
- Griffith's 1911–12 readings differ from the modern REM text in about 4% of signs; rows say they are Griffith's.
- The reading test for printed type covered 12 cursive texts from Philae. The 48 rows in hieroglyphic type were
  not scored, and their notes say so.
- Rilly 2007, Hintze's editions and Hallof 2024 are print-only and were not read; REM is online
  ([Persée](https://www.persee.fr/issue/rem_0000-0000_2000_num_1_1)) but was not read either.
