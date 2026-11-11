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
