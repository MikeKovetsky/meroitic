# Next steps

Written 2026-11-09 after two days of runs, and revised the same day after the plan was checked against Otten's paper
and the sources. Results so far: [`REPORT.md`](REPORT.md); methods: [`README.md`](README.md).

The goal from here: an openly licensed and larger Meroitic corpus, an honest method for testing AI on undeciphered
scripts, and both in the hands of the people who can use them. Each step says why, how, the cost and what "done"
looks like.

## Where things stand (2026-11-10, evening)

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
   61.9% of the running words are translated, 106 of 605 legible texts in full, and 1,306 pieces without an
   accepted meaning are ranked by the texts they block, each with its kind where the texts show one (60.5%, 82
   texts and 1,336 pieces as first built). Section E says what it is for.
8. **The search for Egyptian sources** (2026-11-11, [`data/discovery/egyptian.md`](data/discovery/egyptian.md)),
   the first part of step 17 of section E: a negative result. A search by sound finds the known names of gods,
   places and people but only 4 of 14 known borrowed titles, nouns and verbs, and gives nothing above chance for
   the pieces without a meaning. The step's two other parallels, the oracular decrees and the Philae graffiti,
   are still open.
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

Next, in this order:

1. **Offer the Karanòg rows to Otten** as a second pull request, like the first (public domain source, CC BY).
2. **Step 8, Faras** (46 funerary texts, hand copies): the same method, if that article prints indexes too.
3. **Step 6, Griffith's ostraca** in JEA 11: the volume has to be fetched first.
4. **Left over from the quality pass:** the other 42 pages have one reader each; two printed entries were seen by
   no reader (Kar. 17 `sotnkel` and Kar. 111 `tewideqowi`, section 9 of the Karanòg page); word division outside
   the closing formulae still follows each reader, and so does a formula word parted by a divider on the stone;
   the readers' corrections to the typed pages (`ref_corrections.jsonl`) are not yet put into the tables, which is
   why `yidote dikte` stays two words in two rows (the tables are typed with n); and the names table, the weakest
   of the typed pages, has a second typing for its first page only.
5. **Faults found on the way:** eleven lines of the old corpus are the oracular-decree formula tagged
   "funerary" (one of them counted 187 times); three faint letters mistyped in the Tanyidamani printout.

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
    - **Still open in this step:** the oracular decrees (neither list holds Egyptian texts of that kind) and the
      people named in both the Philae graffiti and the Meroitic texts.
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
    of texts and words that every result since rests on.
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
      (point 10) takes 24 of the 26 with an accepted meaning, all but `mXeyot` and `yetmetl`, and reads `smlowi` as
      `sem` "wife" by its own rule.
    - **Next in this step:** the pieces that block the most texts could go to a checker with their three best
      candidates whatever their chance: the right entry is among the three best for 96% of the hidden variants,
      short ones included, and the bar cannot be beaten by a word of three or four letters.
    - **What the coverage map could take from it:** 15 entries count as translated in the map although their
      meaning makes them a variant of a word that has no accepted meaning itself (`kroro`, `qetrri`, `Kine`,
      `qetneyineqeli` and others); 152 running words rest on them. The corrected map still counts them, and 160
      of its words rest on them (section 7 of the coverage page).
