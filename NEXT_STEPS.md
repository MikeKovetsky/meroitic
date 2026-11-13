# Next steps

Written 2026-11-09 after two days of runs, and revised the same day after the plan was checked against Otten's paper
and the sources. Results so far: [`REPORT.md`](REPORT.md); methods: [`README.md`](README.md).

The goal from here: an openly licensed and larger Meroitic corpus, an honest method for testing AI on undeciphered
scripts, and both in the hands of the people who can use them. Each step says why, how, the cost and what "done"
looks like.

## Where things stand (written 2026-11-10; points 7 to 16 added up to 2026-11-13)

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

Next, in this order (the small steps; the four big pieces are in section F):

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

The order: F1, then F2, then F3 and F4 side by side. Outside the four, the path through people stays open in
section A: a specialist's reading of one page would be worth more than any of these runs.
