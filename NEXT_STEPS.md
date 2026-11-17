# Next steps

Written 2026-11-09 after two days of runs, and revised the same day after the plan was checked against Otten's paper
and the sources. Results so far: [`REPORT.md`](REPORT.md); methods: [`README.md`](README.md).

The goal from here: an openly licensed and larger Meroitic corpus, an honest method for testing AI on undeciphered
scripts, and both in the hands of the people who can use them. Each step says why, how, the cost and what "done"
looks like.

## Where things stand (written 2026-11-10; points 7 to 25 added up to 2026-11-16)

Done since this plan was written:

1. **Step 5, Karanòg:** see its status below. The method passed its test and all 151 texts that have a hand copy
   are read, checked and built. Reviewed and published on 2026-11-10.
2. **Step 7, the Meroitic Newsletter:** 256 texts typed and kept locally; the method, the scripts and the measured
   accuracy are public in [`data/expansion/newsletter_reading.md`](data/expansion/newsletter_reading.md).
3. **Step 2, the two leads,** tested on texts they had never seen: the first got weaker, the second held
   ([`REPORT.md`](REPORT.md)).
4. **Four smaller tests** on the new texts (a held-out grammar test, the oracular decrees read blind, Meeks's 1973
   word list against Rilly 2003, and a collation of editions): section 5 of the Newsletter page.
5. **Step 1, outreach:** Otten has the email and the pull request; Rilly, Hallof (through Beinlich) and Smith were
   asked on 2026-11-09 for typed texts. On the evening of 2026-11-10 the pull request had no comment yet, and
   Otten had added Meroitic–Egyptian word lists to his repository that day (his first commit there since 2024).
   The mailbox, checked the same evening, held no reply and no bounce from any of the four.
6. **A quality pass on the Karanòg rows** (the same evening; sections 5 and 6 of the Karanòg page):
   - **A second reader for eleven of the 53 pages:** the seven most damaged, three drawn at random and the page of
     Kar. 77. After the check the two readers agree on 3,180 of 3,254 signs (97.7%; 97.0% on the damaged pages,
     99.1% on the random ones), which gives 98.8% for all 53 pages, weighted by page. The 56 differing places
     were settled against the copy and the type, which changed 26 signs of the rows.
   - **Uniform rows:** the closing formulae are divided into words as Griffith's formula tables divide them, but
     for a few rows where the stone has a divider or the typed table differs in a sign, and the title `slẖs` has
     one spelling. The d or n of `yidotedikte` is d in every row now.
   - **The duplicate tests:** the Karanòg one no longer takes shared formulae for a copy, so all 151 texts are in
     `corpus_v5`. The Newsletter one already left the formulae out; its three texts wrongly marked as duplicates
     are back (188 new) because `src/mnl/mnl_dedupe.py` now names the three pairs that the collation found to be
     different texts.

7. **The translation coverage map** (2026-11-11, [`data/discovery/coverage.md`](data/discovery/coverage.md)):
   every word of `corpus_v5` glossed from Rilly's lexicon. After four corrections made the same day (point 10),
   62.0% of the running words are translated, 106 of 605 legible texts in full, and 1,304 pieces without an
   accepted meaning are ranked by the texts they block, each with its kind where the texts show one (60.5%, 82
   texts and 1,336 pieces as first built). Section E says what it is for.
8. **The search for Egyptian sources** (2026-11-11, [`data/discovery/egyptian.md`](data/discovery/egyptian.md)),
   the first part of step 17 of section E: a negative result. A search by sound finds the known names of gods,
   places and people but only 4 of 14 known borrowed titles, nouns and verbs, and gives nothing above chance for
   the pieces without a meaning. Of the step's two other parallels, the oracular decrees are still open and the
   Philae graffiti are done (point 14).
9. **The search for spellings of known words** (2026-11-11, [`data/discovery/variants.md`](data/discovery/variants.md)),
   step 21 of section E. The search brings 187 of 242 hidden variants back to their own entry (77%), but its
   test missed the bar, because only 105 (43%) stand out from made-up words. Two blind checkers confirmed 48 of
   the 105 matches of unknown pieces that beat the bar, 29 of them new; 26 would move 59 running words of the
   coverage map (60.5% to 60.7%; 54 without two whose packs showed a word with their own letters glossed).
10. **Six ways of finding meanings, and the map corrected** (2026-11-11, [`REPORT.md`](REPORT.md), Day four,
    night). Six agents dug into the ways that need no new source; none found a new meaning, and each named
    sources we do not hold as its limit. What they found wrong in the map is corrected (section 7 of the
    coverage page): the padding's leftovers after masked names, `smlowi`, words written apart, the confirmed
    spellings and three forms of "sister". What it leaves wrong is listed there too.
11. **The map checked against two printed editions** (2026-11-12, [`data/discovery/experts.md`](data/discovery/experts.md)).
    In the 31 inscriptions that Millet's Gebel Adda article (2005) or *Fontes Historiae Nubiorum* III also print,
    the edition gives a meaning to 397 of the 537 words the map counts as translated, and the map's meaning to
    276 of them (69.5%; 85.2% outside `yetmde` and `qo`, which Rilly reads otherwise than both editions). The
    check found the numeral 1 typed as `l` in one text of the older corpus and eleven names or pieces of words
    read as words, and almost no meaning the map lacks. Both editions are kept locally. Section F draws the
    consequence.
12. **The corpus keyed by inscription** (2026-11-12, [`data/discovery/corpus_v6.md`](data/discovery/corpus_v6.md)),
    piece F1 of section F: built without an agent, then read by two readers. The 899 texts of `corpus_v5` hold
    289 inscriptions; `corpus_v6` holds 548 with real names, and the public table 563 with every reading's
    source and licence. The matching rule missed its bar (45 of 54 known pairs), so numbers decide before
    letters; of the 17 doubtful matches the readers settled all but 3.
13. **Analysts on the unread spellings of the clean corpus** (2026-11-12,
    [`data/discovery/v6_readers.md`](data/discovery/v6_readers.md)): 930 spellings read, 139 running words more
    translated, 52.7% from 51.3%. About half of what was expected: the unread words are pieces of words and
    single words of obscure texts.
14. **The same people in Demotic, Greek and Meroitic** (2026-11-12,
    [`data/discovery/demotic.md`](data/discovery/demotic.md)), a part of step 17: four people carry titles in two
    languages, and where the two texts give the same office the titles line up with the lexicon; the editors' 125
    equations add no meaning that is new and sure.
15. **F2: a second scholar for every meaning** (2026-11-12,
    [`data/discovery/lexicon.md`](data/discovery/lexicon.md)): 4,105 of 10,290 running words (39.9%) are built
    only on meanings a second scholar gives too, against 5,419 (52.7%) translated by one lexicon; of the 177
    entries behind translated words, 84 are agreed, 22 disputed, 51 stated by one and 20 only proposed, after
    three rounds of judges. Every one of the 594 entries the map uses has a status (114 agreed, 26 disputed, 94
    stated by one, 360 proposed). The public tables give each meaning behind a translated word in words of our
    own, each entry's spellings with the confirmed variants, and pages where the sources in hand give them.
    Left: a meaning in our words for the 417 other entries, and the pages of the scholars whose works we lack.
16. **F4, the pilot: five texts translated whole and scored** (2026-11-12,
    [`data/discovery/f4_pilot.md`](data/discovery/f4_pilot.md)). A translator blind to Millet's edition gets 58.3%
    of his 57 scored units of meaning, the map's glosses in order 60.5% (3.5% and 6.1% wrong; judges' kappa 0.97,
    no decoy accepted). The translator adds a readable text and the status of every word, not meaning the
    renderings can see. The full scored run would cost about 2.1 million subagent tokens; pages for the 304
    open inscriptions from this translator about 6.3 million.
17. **F4, the rounds: a translator with a handbook, scored on held texts** (2026-11-13,
    [`data/discovery/f4_rounds.md`](data/discovery/f4_rounds.md)). On the 13 renderings of Millet's held back
    (218 units) the glosses get 58.5%, a writer of sentences 69.3%, one translator 73.9% and a panel of three
    with an editor 74.9%, with 9.2%, 4.4%, 2.8% and 2.3% of the units wrong (judges' kappa 0.88; 1 of 186 clean
    decoy units accepted by each judge). The panel's lead of 16.4 points is over the bar of 5 set beforehand.
    The panel is not shown to beat one translator. Not built yet: the pages for the 304 open inscriptions, and
    the scoring against Griffith's own translations.
18. **The unread spellings that recur** (2026-11-13,
    [`data/discovery/recurring_words.md`](data/discovery/recurring_words.md)). The goal named that day is the
    meaning of all words: the map reads 50.1% of the running words that need one. Of the 1,108 running words
    under the 154 open spellings that stand in three texts or more, 273 take a meaning Rilly states in 2016 or
    2021, 192 are pieces of a longer word or name, 425 stay open and 218 are unclear or not agreed (two
    checkers a place, kappa 0.91). Laid over the map that gives 53.9%; since 2026-11-16 it is the map's first
    layer (point 20). A blind test
    of the proposals on record for the open words missed both bars (right for 13 of 17 accepted words where
    the readers chose, 76.5% against 80%; a wrong meaning chosen for 2 of 11 where the true one was not offered,
    18.2% against 10%), so no proposal is labelled. Open: the same pass on the 2,203 open spellings that stand in
    one or two texts (steps G2 to G4 of section G; G2 and G4 are done, point 21).
19. **Distinct words translated, the north star** (2026-11-16,
    [`data/discovery/distinct_words.md`](data/discovery/distinct_words.md)). Counted once each, 127 of about
    1,307 distinct words have a meaning: 9.7% (between 9.2% and 12.1%), the same as before the project (each of
    those meanings is in the lexicon of 2003), against 50.1% of the running words. 377 are words of the lexicon
    (an ending or a particle written as a word of its own is a piece, not a word); the others are estimated from a
    sample of the 1,107 stems the map cannot name (two checkers, kappa 0.94 on the second reading). The steps of
    section G move this number only where they give a word of the dictionary a meaning (G1: 9 words, Rilly's of
    2016 and 2021; G4 and G7 where they find one) or correct the count of words (G3). Only a meaning of the
    project's own would set it apart from before us.
20. **The map with its layers** (2026-11-16, [`data/discovery/map_layers.md`](data/discovery/map_layers.md);
    step G1). The 385 places point 18 resolved are laid over the analysts' map as its first layer, each with its
    source (`src/themap.py`); the analysts' map is not changed. With this layer: 3,916 of the 7,265 running
    words that need a meaning are translated (53.9%, from 50.1%), 626 of 2,944 distinct spellings (21.3%), and 136
    of about 1,307 distinct words (10.4%, between 9.8% and 13.0%; before us the same). The status table reads
    its first three rows from this count. Not built as the step said: the three pages that count from the map
    (coverage, the translations' baseline, the lexicon's statuses) are not rebuilt; they keep their dated numbers
    and point to the new page, and Mike waived that part on 2026-11-16 ("Yes, waive it."). The other dated studies
    keep the analysts' map too. The layers of G2 and G4 followed the same day (point 21).
21. **The open spellings in one or two texts that hang on an entry of the lexicon** (2026-11-16,
    [`data/discovery/rare_spellings.md`](data/discovery/rare_spellings.md); steps G2 and G4). Two checkers judged
    1,061 places; 268 places are laid in the map as two layers (109 under words the lexicon calls sure and 159
    under entries to which Rilly gives a meaning in 2016 or 2021; 24 of the 268 are pieces of a word the map
    holds). The map as it stands:
    4,149 of the 7,230 running words that need a meaning are translated (57.4%), 814 of 2,917 distinct spellings (27.9%) and 156 of about 1,307 distinct words (11.9%, between 11.3% and 14.9%); before us the north star is the same. 20 entries of the
    lexicon get a meaning; by the later source several are forms of one another. Open: the 182 places where
    both checkers recognise the word but the map leaves a part of the spelling unnamed (or, at one, another stem
    has no meaning), the 159 entries for which Rilly's later work states no meaning firmly, and a second scholar
    for Rilly's meanings (G5).
22. **The open spellings the lexicon does not hold** (2026-11-16,
    [`data/discovery/unnamed_spellings.md`](data/discovery/unnamed_spellings.md); step G3). Two checkers judged
    all 1,225 open places from the place alone, with controls: 828 are words of their own, 111 names, 41 pieces, 245
    unclear or not agreed (a first pilot missed its bars and is not taken). The 111 names and 7 pieces are the map's
    fourth layer. The map with that layer: 4,154 of the 7,117 running words that need a meaning are translated (58.4%), 815 of 2,813 distinct spellings (29.0%) and 156 of about 1,284 distinct words (12.1%, between 11.5% and 15.2%).
    Nothing is deciphered by this: fewer words need a meaning, and the count of distinct words is corrected. The
    north star is recounted from the old sample's stems still unnamed, not from a new sample as the reporting rules
    had said; asked, Mike answered "why do you need my approval to recount? this is obvious you need to recount to
    show the up to date result?". Open: the 828 words of their own, which are what is left to decipher among these
    spellings.
23. **A second scholar for Rilly's later meanings** (2026-11-16,
    [`data/discovery/second_scholar_later.md`](data/discovery/second_scholar_later.md); step G5). 33 of the 66
    meanings are also stated by another scholar (15 of them with a dissent), 13 are disputed, 20 rest on Rilly
    alone. No count of the map changes.
24. **The leftover parts, and the meanings Millet and Lipiński state** (2026-11-16,
    [`data/discovery/leftover_parts.md`](data/discovery/leftover_parts.md); a follow-up to G2 and G4). The first
    reading of the unnamed parts is not taken: one checker explained 3 of the 20 runs of lot letters, one more than
    the bar allowed. Asked whether to read again with a bar for each verdict, Mike said: "Yes, read again". The
    second reading, by fresh checkers on controls drawn anew, met its bars (kappa 0.66): the map's sixth layer
    lays 32 places, 27 of them as translated words and 5 as names; a place both checkers call a name is not laid
    ([`data/discovery/leftover_parts_2.md`](data/discovery/leftover_parts_2.md)). For 15 entries Millet 2005 or
    Lipiński 2011 states a meaning; 12 are stated firmly, 7 of them as names and 2 as a meaning in full. The
    map's fifth layer lays 17 places, 13 of them as names and 4 as translated words. The map with these two layers:
    4,185 of the 7,099 running words that need a meaning are translated (59.0%), 840 of 2,798 distinct spellings (30.0%) and 160 of about 1,284 distinct words (12.5%, between 11.8% and 15.6%).
25. **The blind test again** (2026-11-16, [`data/discovery/blind_test_2.md`](data/discovery/blind_test_2.md);
    step G6). No label is given. With the meaning offered, 17 accepted words got a meaning from all five readers and
    16 of 17 the right one; without it, 3 of 13 got a wrong one from all five, where the bar allowed one. A choice
    among four meanings from the contexts alone is not a test a proposal can pass: this is its second miss. No
    count of the map changes. That run took 43 of the plan's 83 accepted words, and Mike did not waive the
    rest ("No, do not waive"). So the test was run again with all 83
    ([`data/discovery/blind_test_83.md`](data/discovery/blind_test_83.md)): 36 of 37 right with the meaning
    offered, 6 of 27 wrongly chosen without it, where the bar allowed two. No label is given: the third miss.
26. **The leftover stems** (2026-11-16, [`data/discovery/leftover_stems.md`](data/discovery/leftover_stems.md);
    the 86 places that point 24 did not give to checkers, where the unnamed part is the stem itself). Two fresh
    checkers, four kinds of control, and bars of its own for each verdict; all were met (kappa 0.79). No stem is
    a word the lexicon knows. The map's seventh layer lays 23 places, 22 of them as names and 1 as a translated
    word. The map as it stands:
    4,186 of the 7,077 running words that need a meaning are translated (59.1%), 841 of 2,781 distinct spellings (30.2%) and 160 of about 1,283 distinct words (12.5%, between 11.8% and 15.6%).
27. **Grammar first, a pilot** (2026-11-16, [`data/discovery/grammar_pilot.md`](data/discovery/grammar_pilot.md);
    Mike: "how can we make more structural strategic moves", then "Yes, start it"). Rules of the grammar were
    found on 329 texts and tested on the 219 others, each rule by a function committed before the held-back
    texts were touched. Over two rounds 73 rules were proposed, 53 passed on held-back texts and 1 is a finding of ours, where the bar set beforehand was 3.
    The 41 rules of the first round that passed describe the epitaph, and the sources in hand state or partly
    state every one; outside the epitaphs the texts are too few for rules of word order. The pilot ended on its
    first evening. Its last part, the parse of the long royal texts, was built after the review asked for it:
    the rules that passed cut the 7 long texts 11 times, 6 of them in one text built like an epitaph, and speak
    of 51 of their 925 words without a meaning; the long royal texts stay uncut. No count of the map changes.

Next, in this order (the small steps; the four big pieces are in section F, and the steps toward the meaning of
all words in section G):

1. **Offer the Karanòg rows to Otten** as a second pull request, like the first (public domain source, CC BY).
2. **Step 8, Faras** (46 funerary texts, hand copies): the same method, if that article prints indexes too. The
   volume is in hand since 13 November.
3. **Step 6, Griffith's ostraca** in JEA 11: the volume is in hand since 13 November, as page images without a
   text layer, and so is JEA 15 with his Meroitic Studies VI.
4. **Left over from the quality pass:** the other 42 pages have one reader each; two printed entries were seen by
   no reader (Kar. 17 `sotnkel` and Kar. 111 `tewideqowi`, section 9 of the Karanòg page); word division outside
   the closing formulae still follows each reader, and so does a formula word parted by a divider on the stone;
   the readers' corrections to the typed pages (`ref_corrections.jsonl`) are not yet put into the tables, which is
   why `yidote dikte` stays two words in two rows (the tables are typed with n); and the names table, the weakest
   of the typed pages, has a second typing for its first page only.
5. **Faults found on the way:** eleven lines of the old corpus are the oracular-decree formula tagged
   "funerary" (one of them counted 187 times); three faint letters mistyped in the Tanyidamani printout.
6. **No download is left for these steps or for F4** (13 November). Fetched that day from archive.org, all public
   domain, and kept locally: Griffith's *Meroitic Inscriptions* I and II (1911–12), *Meroë, the City of the
   Ethiopians* (1911), the *Recueil Champollion* (1922) with his Faras article, and *Journal of Egyptian
   Archaeology* 11 and 15. F4 reads none of them to start: its sources were in hand before. Also fetched: the
   half of *Liverpool Annals* 7 that archive.org holds. It prints Sayce's reading of REM 1003, all 42 lines in
   the letter values he used, and no picture of the stone; it is not yet typed or compared. Not fetched, on
   purpose: the Nubian grammars of step 18, the REM volumes of step 7, and the books that have to be bought.

## A. Share

1. **Write to Joshua Otten** (George Mason University) with an offer, not a complaint.
   - Why: [his paper](https://aclanthology.org/2025.alp-1.11/) names the blocker himself ("If more Meroitic examples
     could be gathered and made machine-readable, then we could expand our corpus"; "Eventually we will need an OCR
     model for the Meroitic REM texts"), and it describes the name-swap padding openly (871 examples swapped up to
     17,257). What it leaves out is that the released file is the padded version.
   - Offer: the 152 Griffith inscriptions (CC BY 4.0, with source page, and REM number for 127), the reading method
     with its measured accuracy, and the scripts that undo the padding (`src/pool.py` and the three after it).
   - Ask: a note in his repository that `mero-corpus.txt` is the padded version, and the 871 originals beside it as
     one file (its `Data/` folder has them only in the per-scholar files, with translations and page notes).
     [The open issue there](https://github.com/Joshua-Otten/Meroitic-Corpus/issues/1) asks for a licence and a
     provenance line for the same reason.
   - He is also the route to Claude Rilly, whom the paper thanks "for his thorough review and advice".
   - **Done, 2026-11-09:** the email is sent, and
     [123 of the Griffith texts are offered as a pull request on his repository](https://github.com/Joshua-Otten/Meroitic-Corpus/pull/2).
2. **Send the two open leads** with that message, for Rilly or another specialist (Jochen Hallof, Solange Ashby):
   - `wi` before a numeral marks a total: in the Tanyidamani stela, `mk lte wi 12` follows exactly twelve items
     each counted "1" (Hofmann 1981 found a sum on REM 1003; check Hintze 1960 first);
   - the vocative `-i` placed at the end of "god + epithet" (Osiris is never `Soreyi` before an epithet in 11 texts;
     Rilly published the "Isis + Osiris" case; check Rilly & de Voogt 2012, p. 155, and Heyler 1964).
   Any future "new" claim goes through the adversarial check first (`data/discovery/verification.md` shows how),
   and through Rilly's lexicon in `data/rilly2003/`.
   - **Status, 2026-11-09:** both went to Otten in this wording. The same evening they were tested on 185 texts
     they had never seen ([`REPORT.md`](REPORT.md), "Leads 1 and 2 on texts they had never seen"). The second held,
     9 of 9. The first got weaker: the `wi` number on REM 1003 is not the sum of its counts, and at Tabo `wi` stands
     before one numeral after another. Reword the first before it goes to anyone else: the Tanyidamani sum is real,
     the meaning "total" is not shown, and "X are N" fits better.
3. **Write to So Miyagawa** (University of Tsukuba), whose
   [project from 2026](https://tiar.centers.tsukuba.ac.jp/en/fellow/1911/) applies language models to Meroitic: the
   blind-test findings (README, What's new, 3 and 4) are the part most useful to him.
4. **A paper venue exists but has no open call:** the Ancient Language Processing workshop published Otten's paper
   (editions in 2023 and 2025). No call for a next edition was found on 2026-11-09.

## B. Grow the open corpus

5. **Karanòg, checked against Griffith's own printed indexes** (about 150 funerary texts, the largest single gain).
   - Why: one reader reads Griffith's hand copies at 88.8% (`data/expansion/hand_copy_test.md`), with the errors in
     names, rare titles and closing formulas. Griffith's Indexes A to C
     ([pp. 95–122](https://archive.org/details/karangmeroitic00grifuoft/page/n125)) print every name, title and
     descriptive phrase of every Karanòg text a second time, in Meroitic type, tagged with the text's number and the
     word's role (name of the deceased, of the mother, of the father, title, place). The model reads that type at
     99.6% against the print (measured on Griffith's other volumes, not on these indexes).
   - How: transcribe the indexes (28 pages of type) into one table: word, role, text numbers. Read each hand copy
     as before, then replace or confirm every name, title and phrase from the table.
   - Test first: Kar. 47, 77, 78 and 121 against FHN with fresh agents. The bar is 95% of signs. Four texts are a
     small test, and FHN prints no other Karanòg text.
   - Before starting: the page images are in `/private/tmp/claude-501/expansion/`, which macOS empties on restart.
     Copy them to a folder listed in `.gitignore`, or download them again from archive.org
     (`data/expansion/README.md` has the item ids).
   - Cost: about 1 hour for the test, 2 to 3 hours for 150 texts. Done: `griffith_karanog.jsonl`, merged by
     `src/expand.py`, with the measured accuracy in its notes.
   - **Status, 2026-11-10, evening: done for all 151 texts that have a hand copy**
     ([`data/expansion/karanog/README.md`](data/expansion/karanog/README.md)). Griffith gives no copy of Sh. 20.
     - The test passed: fresh readers who could not see FHN reached 97.7% of signs on the four test texts (89.0%
       from the hand copies alone).
     - The check uses three printed sources, not one: the indexes, Griffith's table of names and parentage
       (pp. 87–94) and his tables of the closing formulae (pp. 42–53). All 48 pages are typed, for all 152 texts.
     - The result: 16,440 signs and 2,911 words in `data/expansion/karanog/griffith_karanog.jsonl`. The check
       placed 3,468 printed entries and changed 2,405 of the 16,759 signs first read (14.4%).
     - `src/expand.py` merges all 151 into a new `corpus_v5`: 899 texts and 21,977 words, against 748 and 19,066
       in `corpus_v3`, which stays as it was. Three short texts (Kar. 63, Kar. 66, Sh. 17) were held back at first
       as "already present"; that was the formula overlap of step 10, and for these rows the test now leaves the
       letter groups of the formulae out.
     - Eleven pages were read a second time and the rows made uniform the same evening ("Where things stand",
       point 6).
     - The estimate above was too low: a page of hand copies takes a reader about an hour, and typing the
       reference pages and reading all the copies cost about 14 million subagent tokens.
6. **Griffith's JEA "Meroitic Studies"** (about 45 ostraca, public domain, printed in Latin letters): OCR, then
   check every word against the page image. The cheapest texts that can be published.
7. **A first look inside the REM.** The *Répertoire d'épigraphie méroïtique* (Leclant and others, 2000) is
   [online at Persée](https://www.persee.fr/issue/rem_0000-0000_2000_num_1_1) in three volumes, REM 0001 to 1278:
   about 1,280 inscriptions against about 480 in Griffith. Otten's paper describes it as photographs and facsimile
   drawings without transliteration; that was not checked here. Open one volume, see what an entry holds, and score
   a reading on entries FHN also prints. It is not openly licensed: for analysis and for checking readings, not for
   republishing.
   - **The complete transliterations exist in print (checked 2026-11-09).** Jochen Hallof, *Analytisches
     Wörterbuch des Meroitischen*, volume 7, "Dokumente" (J.H. Röll, 2024, SRaT 13.7, ISBN 978-3-89754-629-5):
     hardcover, 340 pages, 139.00 EUR. [The publisher's free 23-page sample](https://www.lehmanns.de/media/116874085)
     opens with "Inscriptions REM 0001 to REM 2780" and gives each entry's object, findspot, present location,
     dating, publication and transliteration with line numbers. No e-book or online version was found.
     [Lehmanns.de](https://www.lehmanns.de/shop/geisteswissenschaften/68060973-9783897546295-analytisches-woerterbuch-des-meroitischen-analytic-meroitic-dictionary)
     had one copy and ships within Europe only; Blackwell's was out of stock and Amazon.de did not deliver to the
     United States; the publisher (info@roell-verlag.de) ships outside Europe at the actual postage, by email order.
     Reading it would take about 7 million subagent tokens at the rate measured on the Newsletter. It is in
     copyright: for private analysis unless the author agrees to more.
   - **Found since (2026-11-09):** the scans of the *Meroitic Newsletter* (issues 6 to 30, 1971 to 2003) print
     transliterations with REM numbers: Heyler's 1971 transcription of REM 1001 to 1110, and later editions from
     Qasr Ibrim, Arminna, Shokan, Tabo, Sedeinga and Meroë. 256 texts were typed that day, 188 of them new to the
     corpus. They are kept on the author's machine, for analysis and for checking readings like FHN: the articles
     are in copyright.
8. **Faras funerary texts** (46, Griffith 1922, hand copies, archive.org `bibliothquedel234ecol`): the Karanòg
   pipeline once it passes. Check first whether that article has indexes like Karanòg's.
9. **FHN's modern transliterations** (about 30 texts, OCR in `/private/tmp/claude-501/expansion/survey/fhn/`):
   clean modern readings for private analysis only (FHN is "all rights reserved").
10. **Mask names in the Griffith rows** the way `corpus_v2` masks them, so frequency counts in `corpus_v3` mean the
    same thing; and relax `src/expand.py`'s duplicate test, which counts a short label inside a longer text as
    present (the +86 texts are a lower bound). For the Karanòg rows the test leaves the formulae out since
    2026-11-10; the older Griffith rows are still tested the old way.
11. **A glyph classifier for Griffith's type** (23 forms) would cut the cost of the remaining printed texts, not
    raise their accuracy (reading is already at 99.6% against the print); the 12 scored texts in
    `runs/work/griffith/` are its test set. Low priority.

## C. Measurements

12. **Rebuild and rerun the corpus meaning test** with the fixed builder (`src/lexique.py` leaves out of the
    glossary a word that gives a target away) instead of removing leaked items afterwards; judge again. About 40
    minutes. The builders refuse to replace the first run's keys (`runs/keys/lexique_items.json`,
    `lexique_open.json`), which `judged` and the tests read, so the new run needs its own key names first.
13. **Does more data help?** Not by comparing `corpus_v2` with `corpus_v3`: a 5% change over about 35 test words
    is too small to show. A learning curve on the synthetic language would show it (25%, 50%, 100% and 200% of the
    corpus), but `synth.corpus()` has its size fixed at 1,000 texts, and with 52 test words a run it needs three or
    more runs per size. Optional: under the corpus goal the answer would not change the plan.
14. **A second synthetic language** with a different generator (other formula types, number-conditioned plurals) to
    check that the 79–83% matching rate isn't an artefact of one design.

## D. Parked

15. **Cognates:** the sound-law engine found no signal on held-out words. A real test needs more independent NES
    vocabulary (culture and kin words are missing for most languages) rather than a better scorer.

## E. Toward translation

The coverage map (point 7 above) turns "closer to a translation" into a number and a list. What moves the number:

16. **The verbs of the benedictions first.** `ḫr` and `ẖol` stand in 116 and 70 texts, and Rilly gives each a
    proposal only. An accepted meaning for `ḫr` alone would complete 11 texts.
17. **Egyptian parallels for the titles and the counted things** in the list: borrowed titles, the oracular
    decrees (an Egyptian kind of text) and the Philae graffiti that name the same people in Demotic. Test the
    method first on known loans held out.
    - **The search for borrowed words is done (2026-11-11), with a negative result**
      ([`data/discovery/egyptian.md`](data/discovery/egyptian.md)):
      a search by sound puts the true source among the five best candidates for 4 of the 14 known borrowed
      titles, nouns and verbs (the bar was most of them), though for all 10 names of gods, places and people with a
      source among the Demotic names of their kind it is among the three best. Of the 383 unknown pieces searched,
      22 and 26 beat the 5% bar where 19 are expected by chance, and two blind checkers found no new source among
      the 33 best matches. Sound alone does not tell a loan from a look-alike in a pool of thousands.
    - **With the vowels compared too** (the Coptic entries only): the true source is among the five best for 7
      of 13 loans against 4, so a vowel-aware search is the better tool once a word is known to be a loan. It
      does not find loans: 13 of 241 unknown pieces beat the 5% bar, where chance gives 12.
    - **Still open in this step:** the oracular decrees (neither list holds Egyptian texts of that kind).
    - **The people named in both the Philae graffiti and the Meroitic texts: done (2026-11-12)**
      ([`data/discovery/demotic.md`](data/discovery/demotic.md)), from the 22 Demotic graffiti and two Greek
      inscriptions that *Fontes Historiae Nubiorum* III prints in translation. Four people have a title in both:
      `perite` is the Demotic "agent" for two, `peseto` "the king's son" and the Greek `psentes` for one, `kroro`
      the Demotic `3krre` for one. It confirms; it adds no meaning that is new and sure.
    - **What it leaves:** the Demotic list holds graffiti of Meroitic officials at Philae (`qrnyꜣ` for `qorene`,
      `ꜣrbtgꜥyꜣ` for `arebetke`, `wygy` for Wayekiye). Reading those sentences beside the Meroitic titles is
      the parallel that carries meaning; it needs the names of the older corpus unmasked, and it can start from
      the six groups of Philae texts that [`data/discovery/philae.md`](data/discovery/philae.md) already sets side
      by side. And at least 16 pieces of the coverage map's list are forms of words the lexicon already links to
      Egyptian (`prSn` for `plsn`, `petmoS` for `pelmos`): the map could count them.
    - **The answer key:** two independent readers went through the 207 entries of
      the lexicon that mention Egyptian, Demotic, Coptic, Greek or Latin and agreed on 198: 69 are borrowings into
      Meroitic for both readers (35 of them with an accepted meaning, 33 with the source word printed: 19 names
      and 14 titles, nouns and verbs), 49 are Meroitic names in Egyptian or Greek letters, and the rest are
      rejected or mention the language for another reason. The table is local, like the lexicon.
    - The search side, fetched on 2026-11-11 and kept locally: the Coptic lexicon of
      [KELLIA's dictionary](https://github.com/KELLIA/dictionary) (`Comprehensive_Coptic_Lexicon-v1.2-2020.xml`,
      12.3 MB; CC BY-SA 4.0 as coptic-dictionary.org and the file's own header say; vowels and English meanings)
      and the TLA's [Demotic sentences](https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-demotic-v18-premium)
      (`train.jsonl`, 7.3 MB, CC BY-SA 4.0; lemma forms, no lemma meanings).
    - Otten's `bilingual_dicts` (added 2026-11-10) pair words by meaning for his alignment experiments
      (`qEr` with `nswt`); they are not loans.
18. **A Nubian comparison that uses the kind of each word.** The list says what kind of word half the unknown
    pieces are (670 of 1,336: title, kin term, verb, counted thing); matching each only against Nubian words of
    that kind cuts the chance look-alikes that sank the cognate test (D 15). Step 17 shows how far that goes: a
    pool of a few hundred words of one kind was small enough (the names of gods), a pool of thousands was not.
    It needs a larger Nubian word list with culture and kin words: Reinisch's *Die Nuba-Sprache* (1879) and
    Lepsius's *Nubische Grammatik* (1880) are public domain and on archive.org, untyped.
19. **More texts.** 995 of the 1,336 pieces stand in a single text once near-copies are set aside, so context
    cannot place them; Hallof's volume 7 (step 7 above) would triple the texts.
20. **Left open by the map itself:** the lexicon is the state of 2003 (Rilly's 2016 list accepts `pqr`, `wide`,
    `nbr` and `sr`, which it holds as proposals); 1,657 leftover words have one analyst only; a word with two
    accepted entries is not disambiguated; and the older corpus divides words unevenly. The corrections of
    2026-11-11 treat two leftovers of the padding in the map (`mokelowi` and `mete l` after a masked name) but
    not in the corpus, which still holds the padded frames as texts: removing them there would change the counts
    of texts and words that every result since rests on. The check of 2026-11-12 added two faults of the same
    kind: the numeral 1 typed as `l` after each prince's name in the epitaph of Makheye, a text that stands four
    times, and names the older corpus did not mark as names. Piece F1 below is the remedy for all of them.
21. **Spelling variants inside Meroitic.** The Egyptian search stumbled on at least 16 pieces of the map's list
    that are spellings or forms of known words (`prSn` for `plsn`, `petmoS` for `pelmos`). Searched for on
    purpose, each piece would be compared with the about 800 entries of the lexicon, a pool small enough for a
    search by letters to work (step 17), and the spellings Rilly lists as variants are the test: hide each and see
    whether the search brings it back to its entry. Each hit that two checkers confirm moves a piece of the map
    to a known word.
    - **Done (2026-11-11)** ([`data/discovery/variants.md`](data/discovery/variants.md)). The bar, set before the run: two thirds of
      the hidden variants back to their own entry as the single best match, and half of them with a match that
      stands out from made-up words. 187 of 242 come back (77%, reached; 232 among the three best), 105 stand out
      as well (43%, not reached): a word of three or four letters cannot stand out, and none of the 93 does.
    - **On the pieces:** 82 of 1,140 beat the 5% bar where made-up words predict 57, but words that are known to
      be nobody's variant beat it as often (8 of 76). Letters rank the candidates; they do not decide.
    - **The check:** two blind checkers confirmed 48 of the 105 matches under the bar, 19 of them pairs the
      lexicon links itself and 29 new. 26 of the new ones are a word with an accepted meaning and would move 59
      running words (60.5% to 60.7%; 54 without `mXeyot` and `yetmetl`, whose packs showed a word with the piece's
      letters and its gloss). Both named the right entry for 6 of 12 known variants and accepted a
      look-alike for 1 of 12, so the list is fairly safe and short of what is there.
    - **Open in the check:** `smlowi` (81 running words): both checkers take it for a known word, one for `sem`
      with `-lowi`, one for the title `smlo` with `-wi`. The list of the 48 is
      [`data/discovery/variants_confirmed.tsv`](data/discovery/variants_confirmed.tsv). The corrected coverage map
      (point 10) takes all 26 with an accepted meaning, saying of `mXeyot` and `yetmetl` that their packs showed a
      hint, and reads `smlowi` as `sem` "wife" by its own rule.
    - **Next in this step:** the pieces that block the most texts could go to a checker with their three best
      candidates whatever their chance: the right entry is among the three best for 96% of the hidden variants,
      short ones included, and the bar cannot be beaten by a word of three or four letters.
    - **What the coverage map could take from it:** 15 entries count as translated in the map although their
      meaning makes them a variant of a word that has no accepted meaning itself (`kroro`, `qetrri`, `Kine`,
      `qetneyineqeli` and others); 152 running words rest on them. The corrected map still counts them, and 160
      of its words rest on them (section 7 of the coverage page).

## F. The next big pieces (defined 2026-11-12)

Steps 1 to 21 are single runs. After five days, what limits every result is not a missing run but four things
in the structure of the project: the corpus the numbers are counted on, the single lexicon behind every meaning,
tests that live in separate scripts, and the lack of anything a reader can read. Each piece below is a build of
days, not hours. The costs are estimates from what the runs so far cost.

22. **F1. One inscription once: a corpus keyed by inscription, with real names and a source for every text.**
    - Why: every figure is counted on `corpus_v5`, and 662 of its 899 texts are Otten's file, with names masked
      and name-swapped copies (608 texts and 8,786 of the 21,977 words are left when near-copies count once). Found
      in it so far: leftovers of the padding read as words, a numeral typed as a letter in a text that stands
      four times, names not marked as names, uneven word division, decree lines tagged as funerary. The map
      patches the padding's leftovers and words written apart, not the rest, and none is fixed in the corpus
      (step 20).
    - What: one row per inscription, with its REM or edition number, site and kind; under it every reading we
      hold (Otten's line, Griffith's print, the Karanòg copies, the Newsletter, Millet 2005, FHN) with its source
      and licence; and one preferred reading with real names and one rule of word division. The old ids map to it.
    - How: match readings by shared runs of letters, as `src/experts/prepare.py` does, confirm each match by a
      reader who sees both, and restore names from the editions that print them.
    - Done: every text of `corpus_v5` is mapped to an inscription or marked as an example phrase from a grammar;
      a `corpus_v6` in which no inscription stands twice; the coverage map and the check against the editions
      counted again on it. Measured by: inscriptions, the share with a REM number, with real names, with two
      readings, and under an open licence.
    - Cost: 2 to 4 million subagent tokens and one to two days. Hallof's volume 7 (step 7) would complete it;
      without it the piece covers what is in hand.
    - Comes first: F2 to F4 are all counted on it.
    - **Status, 2026-11-12: built** ([`data/discovery/corpus_v6.md`](data/discovery/corpus_v6.md)). Otten's file
      is undone from his own per-scholar files, so every older text has a source line with real names. Done: the
      table of 563 inscriptions, the map of all 899 old ids, `corpus_v6` with 548 inscriptions, the coverage map
      and the expert check counted again (60.0% and 71.4% on the inscriptions that were in the corpus, against
      62.0% and 69.5%), and two readers on the 17 doubtful matches, for 253,065 subagent tokens. Reviewed at the
      full tier (523,726 subagent tokens).
    - **What it leaves for later:** 966 words of the new inscriptions (and 47 of the others) had no analyst;
      they were read the same day ([the readers' page](data/discovery/v6_readers.md) gives what that changed);
      nine Gebel Adda inscriptions are held only as a text layer of Millet 2005 and could be typed; 8 texts
      quoted by Millet 1968 are not identified, one of which may be Griffith's Meroë 27 or 28; 3 doubtful matches
      are not settled; the kind of text is not known for 112 inscriptions; and word division still follows each
      edition.
23. **F2. A lexicon with a source and a status for every meaning.**
    - Why: "translated" in the map means that one lexicon of 2003 accepts the meaning. The check of 2026-11-12
      shows what that hides: two other scholars agree for 85% of the words outside `yetmde` and `qo`, and differ
      on those two, on `mete`, on `peseto`. And the lexicon is in copyright, so the map's readings cannot be
      published or reused.
    - What: a table of words with their spellings (the confirmed variants of step 21 included), their kind, and
      for every meaning the scholars who state it, with page, and a status: agreed by two independent scholars,
      stated by one, disputed, or proposed. The meanings are worded here and cited, not copied, so the table can
      be public.
    - Sources in hand: Griffith 1911–12 (public domain), Rilly 2003, FHN III, Millet 2005, Rilly's 2016 overview.
      FHN's index volume (FHN IV) is in hand since 12 November, local only: its Meroitic indexes gloss 62
      titles and 51 words. FHN's volume II is in hand since 12 November too (from Bergen's server, not on
      Zenodo; local only). Worth adding later, to check the result: Rilly and de Voogt 2012.
    - Done: every entry the map uses has a status; the map gives two figures, "translated by one lexicon" and
      "agreed by two scholars"; the table is published under CC BY.
    - Cost: 2 to 3 million subagent tokens.
    - First pass, 12 November: statuses for all 177 entries behind translated words and the second figure
      (point 15 above), and in a second round the decoyed lines read again with the real proposal and the
      meanings worded anew for the public table.
    - Round three, 12 November: a status for the 417 other entries the map uses (30 agreed, 4 disputed, 43
      stated by one, 340 proposed), after two judges read every proposal on them and on the names (kappa 0.90, 0
      of 40 decoys accepted). Every entry's spellings with 33 of the 48 confirmed variants of step 21, and the
      pages where the sources in hand give them: the editions' entries (100 entries), FHN IV's indexes (113) and
      Griffith's own page (10 of the 206 proposals both judges found the same or otherwise). Still open: a meaning
      in our words for the 417 other entries; the pages of the other scholars, whose works we do not hold (papers
      in the Meroitic Newsletter, whose scans we hold, need Rilly's bibliography to be found); FHN IV's glosses as
      the statement of a second scholar.
24. **F3. One harness: the test of a model on a language nobody reads.**
    - Why: this is the project's second goal, and today it is six studies with their own packs, decoys and
      judges (`lexique`, `synth`, `cloze`, `egyptian`, `variants`, `experts`). What they taught is written in
      pages, not in code: a bar set before the run, made-up words as the measure of chance, two blind judges,
      decoys that neither echo the answer nor stand beside it. Nobody can run "the Meroitic test" on another
      model.
    - What: one package with the tasks (hidden meanings with names masked, hidden spellings, hidden loans,
      restoration, the synthetic twin language), one protocol, one report, and the same run on two models or more.
    - Done: one command produces the report from a clone for the tasks whose data is public, and skips the rest;
      a table of models; a write-up fit for the Ancient Language Processing workshop (step 4).
    - Cost: 1 to 2 million subagent tokens to build, and 3 to 5 million for each model's run.
25. **F4. Whole texts, translated and scored.**
    - Why: the map is word by word. "106 of 605 texts complete" is not one translated text, and a visitor of the
      project sees none. The check gives the way to score a translation: against a printed rendering, word by
      word, by judges who see both.
    - What: for each inscription a line-by-line translation built from F2's table, with the status of every word
      shown and the open words left open; scored against Millet's 20 renderings and Griffith's own translations
      where they exist; a page per text for the 304 texts whose source is in the public domain.
    - Done: the texts with a full rendering counted, their agreement with the printed renderings measured, and
      the pages public.
    - Cost: 2 to 4 million subagent tokens. Needs F1 and F2.
    - **Pilot, 12 November** ([`data/discovery/f4_pilot.md`](data/discovery/f4_pilot.md)): five of Millet's 20
      renderings, a translator blind to Millet, the map's glosses in order as the baseline, two judges with
      decoys. Both bars met (kappa 0.97; no decoy accepted). Translator 58.3% of 57 units, baseline 60.5%: under
      the 5 points of lead set beforehand, so the translator adds readability, not meaning. 560,981 subagent
      tokens.
    - **Next in this step:** (a) fix the splitter's rule so that a unit is open only where all of it is
      untranslated, let the judges know that two names of a place are one, and give the baseline every gloss
      the translator sees (a word the map counts as unknown was "?" in the pilot's baseline); (b) a pilot of the
      lighter step for the pages (the map's readings written as sentences, each word's status kept) on the same
      five texts, scored the same way; (c) then the scored run of the 13 held renderings not in the pilot (about
      1.6 million subagent tokens at the pilot's rates, about 0.4 million less with one judge), and Griffith's
      own translations as a second rendering for the Karanòg pages.

    - **The rounds, 13 November** ([`data/discovery/f4_rounds.md`](data/discovery/f4_rounds.md)): items (a) and
      (b) are done and the scored run of (c) too, for the 13 held renderings. The scoring's three faults are
      fixed; the lighter step is the "writer" (69.3% on the held texts); a translator with rules, a handbook and
      parallels gets 73.9% and a panel of three with an editor 74.9%, against 58.5% for the glosses. Cost:
      17,879,477 subagent tokens.
    - **Next in this step now:** the pages for the 304 open inscriptions, built with the panel, as the rule set
      before the held texts were run decided (section 7 of the page): about 450,000 subagent tokens a text,
      about 137 million for the 304 (one translator alone about 112,000 and 34 million; the panel's 1.0 point
      over it is not shown to be a gain). Then Griffith's own translations as a second rendering. Neither is
      built yet.

The order: F1, then F2, then F3 and F4 side by side. Outside the four, the path through people stays open in
section A: a specialist's reading of one page would be worth more than any of these runs.

## G. Toward the meaning of all words (defined 2026-11-15)

Mike, 2026-11-13: "our goal is to decipher the meaning of all words". 2026-11-15: "define next steps".

**Where the count stands.** With the results of point 18 laid over the map, 7,265 of the 10,290 running words of
`corpus_v6` need a meaning and 3,916 have one (53.9%). The 3,349 that stay open are of four kinds, and each kind
has its own step:

| Kind | Running words | Spellings | Step |
|---|---|---|---|
| a. The spelling is open, but the lexicon calls its stem or ending established or probable | 366 | 312 | G2 |
| b. The lexicon holds the entry without an accepted meaning, and the spelling stands in one or two texts | 1,032 | 784 | G4 |
| c. The lexicon does not hold the spelling, and it stands in one or two texts | 1,225 | 1,107 | G3 |
| d. Places of the 154 recurring spellings that point 18 left: 378 open, 124 pieces of a word the map does not read, 137 unclear, 77 not agreed | 716 | 127 | G5, G6 |

Ten more are open places of five spellings that the map takes as names elsewhere.

The steps, in this order. Each keeps the rules of point 18, one of them more strictly: two readers a place, each
bar committed before its readers are started (point 18 did so for every bar but that of the stated meanings, which
went into git only with its result), a count that follows from a figures file, and nothing called a meaning of
ours unless it passes a test set beforehand.

1. **G1. Put the overlay into the map.** The 385 places of point 18 (273 stated by Rilly in 2016 or 2021, 66
   pieces of a word or name the map reads, 46 places of seven names) become a layer of the map's build, each with
   its source. Done when the map's own figure is 53.9%, the pages that count from the map (coverage, the
   translations' baseline, the lexicon's statuses) are rebuilt from the same file, and the checks and the review
   pass. No agents but the review.
   **Built on 2026-11-16** (point 20, [`data/discovery/map_layers.md`](data/discovery/map_layers.md)): the layer is
   laid by `src/themap.py` and the map's figure is 53.9%. One part is not built as written, and Mike waived it on
   2026-11-16 at 13:52, asked whether the three pages could keep their numbers and point to the new page: "Yes,
   waive it." The three pages are not counted again. They report dated work on the analysts' map, two of them rest
   on judges, and the translations' baseline is the status table's "Before us"; they point to the new page, which
   counts the map as it stands.
2. **G2. The spellings under a sure stem** (kind a: 366 running words under 116 lexicon entries). Most should be
   rarer spellings or compounds of words the map already reads. The place pass of point 18 again: two checkers
   say for each place whether it holds the lexicon's word. If every one were read the share would be 58.9%; the
   first pass kept about half of what its first readers counted (273 of 531), so expect less. About 16 checkers.
   **Done on 2026-11-16** (point 21): 245 of 366 places stated by both checkers (kappa 0.70); 109 laid in the
   map: 103 of the stated places, those whose every part the map names, and 6 pieces of a word it holds.
3. **G3. The spellings that are not in the lexicon** (kind c: 1,225 running words, most of them standing once).
   Point 18 found a sixth of the recurring places to be pieces of a longer word or name that the edition's word
   division cut, and seven items to be names. So first a pilot on 100 places drawn by a fixed seed: a script
   proposes the joins with the neighbouring words that give a form the map reads, two checkers decide (a piece, a
   name, a word of its own, unclear), and the bar is set beforehand. A name or a piece of a name needs no
   meaning; a piece of a word the map reads takes that word's. This step deciphers nothing: it corrects the
   count of what is left to decipher. If half of kind c left that count, the share would be 58.9% with nothing
   else changed.
   **Done on 2026-11-16** (point 22): 111 names and 7 pieces laid; a tenth of kind c left the count, not a half,
   and the share is 58.4%.
4. **G4. The later sources on the rest of the lexicon's open entries** (kind b: 1,032 running words under 323
   entries). The literature pass, the two readers and the place pass of point 18 again. A first search by
   headword finds only 51 entries of kinds a and b named in Rilly 2016 or 2021, covering 175 running words, so
   the yield will be small. It comes after G2 and G3, which cost less for more.
   **Done on 2026-11-16** (point 21): 57 entries with a meaning stated by Rilly in 2016 or 2021, 181 places stated
   by both checkers, 159 places laid in the map; 20 words of the dictionary new with a meaning.
5. **G5. A second scholar for the stated meanings.** The 26 meanings of point 18 are Rilly's alone. The method
   of F2 on them: does FHN, Millet 2005 or Griffith state the same, or dissent, as Millet does on `sete`? The
   result is a status for each meaning (agreed by two, stated by one, disputed), not a higher count.
   **Done on 2026-11-16** (point 23), with the meanings of G4: 33 agreed, 13 disputed, 20 stated by one.
6. **G6. The blind test again, with what the first one taught.** The bar set beforehand at "all five readers
   agree" (seen after the first count: 12 of 15 right, and no wrong choice among the 11 words whose meaning was
   not offered); the 83 lexicon entries the map reads in three texts or more as accepted words, instead of 38;
   fillers worded like the candidates. If the bars hold, a proposal on record for one of the 378 open places
   can be called favoured by the contexts. It is the only way in hand to say anything about kind d.
   **Done on 2026-11-16** (point 25), in two runs: no label is given. With 43 accepted words one bar held (16
   of 17 right with the meaning offered) and one was missed (3 of 13 wrong without it); 5 of the 45 further
   entries have a meaning of their own that can be offered. Mike did not waive the 83, so the second run took
   them all, the 40 others with the meaning the lexicon gives them, however coarse: 36 of 37 right, 6 of 27
   wrong, the same bar missed. Nothing is left to try by this method: more accepted words and a stricter rule of choice
   changed nothing in what it cannot do, which is to tell a right proposal from a wrong one chosen for want of
   the right one.
7. **G7. New evidence, on Mike's word.** After G6 the sources in hand are used up for meanings. What would move
   the count further: an answer from Rilly, Hallof or Smith to the letters of 9 November (none had come by 15
   November, and the pull request to Otten had no comment); the works we do not hold that state meanings for
   open words (Rilly 2007 and 2010, Hofmann 1981, Hintze 1979); and Hallof's edition of 2,780 inscriptions,
   which would turn many spellings that stand once into spellings that recur and can be tested. Purchases are
   parked, and the results are frozen before a new source is opened.

**What is left of section G after 2026-11-16:** G7 alone. G1 to G6 are done, and so are their follow-ups: the
leftover parts with their two readings and the meanings Millet and Lipiński state (point 24), and the leftover
stems, the 86 places of the same kind where the unnamed part is the stem itself (point 26). With the sources in
hand, no step is left that could give a word a meaning. Section H notes three paths that would bring in evidence from outside
the texts.

**What the grammar pilot adds to that** (point 27): the other way that needs no new source is closed as well.
New grammar cannot be tested on this little text: only the epitaph's formulas and the habits of the script come
back often enough, and scholars have described both. What is left is evidence the project does not hold: more
texts, the works named under G7, and the scholars who hold them. The pilot leaves 15 points where the count is
sharper than what the sources in hand say, and one rule they do not state (on the sign `q`); whether Rilly's
grammar of 2007 or Hintze 1979 state them is a question for a scholar, and would be a concrete thing to ask one.

Not on this path: the pages for the 304 open inscriptions and Griffith's translations as a second rendering
(F4, above) assemble meanings scholars already have.

## H. Paths that bring evidence from outside the texts (noted 2026-11-16, 20:54)

Asked whether the project is a dead end, I answered yes for the texts alone. Mike: "but we didnt have claude
code+fable for a centure. and not enough attention to this language. are you sure there are no scientific
methods left to attack it?", and then: "note down these paths in the doc if not yet". He is right that one door
was closed too fast. What the tests of sections F and G and the grammar pilot close is narrow: a meaning or a
rule got from these 548 texts alone. Three paths bring evidence from outside them. None is started, and none
has a bar yet: each gets one, committed before its first agent, like every step above.

**Launched on 2026-11-16** (Mike, asked "Should I launch the three tracks now?": "Yes, launch all"). The rules
and the bars of all three, set before any agent was started, are on
[`data/discovery/outside_evidence.md`](data/discovery/outside_evidence.md): H1 is its track A, H2 its track B,
H3 its track C. Results are written there.

**H1. Whole dictionaries of the related languages, each proposal checked by the contexts** (the first to try).

- **What:** type whole dictionaries of Nubian and its relatives, thousands of words each, in the place of the
  short lists used so far. Let regular sound correspondences propose, for each Meroitic word without a meaning,
  the words it could be a relative of. Give each proposal to the blind choice as one of its four meanings.
- **Why it is not closed:** the comparison of 9 November (D 15, `data/discovery/cognates_rules.md`) had 31
  words that the correspondences were not built from and lists of a few hundred words a language, 5,442 rows
  in all. It came out at chance, so by its own rule no proposal for an unknown word was ever made. That shows
  that short lists carry no signal that generalises, not that dictionaries carry none.
- **Why the two halves fit:** the blind choice fails only where the true meaning is missing from the options.
  Where it was offered, five readers who agreed were right in 16 of 17 and in 36 of 37 words (G6). A dictionary
  of a related language is a source of meanings from outside the texts. Step E 18 adds a filter that costs
  nothing: match a word only against words of its own kind, which the contexts do give.
- **What it needs:** the dictionaries. Reinisch's *Die Nuba-Sprache* (1879) and Lepsius's *Nubische Grammatik*
  (1880) are public domain and on archive.org, untyped (E 18); what else is free has to be looked up. One list
  of downloads goes to Mike before anything is fetched.
- **How it is known early whether it works:** the whole path is run blind on the words whose meaning is known,
  with the bar set beforehand: how many meanings it recovers, and how many wrong ones it lets through. If it
  fails there, it stops there.
- **What is not known:** how much of the vocabulary has a recognisable relative at all. The sound
  correspondences in hand were built by one scholar from about 20 word series; a handful of words more would
  already be the project's first meanings of its own.

**H2. The Kushites' own Egyptian texts as a stand-in bilingual.**

- **What:** the kings of Kush had royal stelae written in Egyptian for centuries before Meroitic was written.
  *Fontes Historiae Nubiorum* I and II translate them. Read the Meroitic royal and temple texts beside them,
  frame by frame: the titles and epithets of the king and the gods, the dating, the lists of booty and gifts
  with their numbers, the order of the parts.
- **What it needs:** nothing new. Volume I is held and not yet used (`data/INDEX.md`), volume II is typed.
- **How it is known early:** where a frame holds a Meroitic word whose meaning is known, the Egyptian word in
  the same place must have that meaning more often than a draw by lot would give. Only then is an open word
  read off a frame.
- **What speaks against it:** the two tries of this kind on 11 November (the offering formulas against the
  Egyptian funerary wishes, the titles against the Demotic graffiti) found nothing that the lexicon does not
  have. The royal texts were not compared with the Egyptian royal texts.

**H3. Names as small sentences.**

- **What:** a Meroitic personal name is often a compound, with a god's name or a known word in it. Split the
  names the map marks into the parts that come back, and compare how the parts stand (first or last, with
  which god, in men's or women's names) with how such names are built in Egyptian and in Nubian.
- **What it needs:** nothing new: the map marks the names, and the epitaphs say who is whose mother and father.
- **How it is known early:** parts that are known words (`mlo`, `lẖ`) must come out as what they are.
- **What speaks against it:** like the contexts, it may give the kind of a part sooner than its meaning.

The write-up names these paths under what would change its answer ([FINDINGS.md](FINDINGS.md), section 7).
