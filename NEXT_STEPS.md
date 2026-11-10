# Next steps

Written 2026-11-09 after two days of runs, and revised the same day after the plan was checked against Otten's paper
and the sources. Results so far: [`REPORT.md`](REPORT.md); methods: [`README.md`](README.md).

The goal from here: an openly licensed and larger Meroitic corpus, an honest method for testing AI on undeciphered
scripts, and both in the hands of the people who can use them. Each step says why, how, the cost and what "done"
looks like.

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
   - **Status, 2026-11-10: the test passed and 19 of the 152 texts are read**
     ([`data/expansion/karanog/README.md`](data/expansion/karanog/README.md)). Fresh readers who could not see
     FHN reached 97.7% of signs on the four test texts (89.0% from the hand copies alone). The check now uses
     three printed sources, not one: the indexes, Griffith's table of names and parentage (pp. 87–94) and his
     tables of the closing formulae (pp. 42–53). All 48 pages are typed, for all 152 texts. Left to do: the other
     133 texts (46 page scans to fetch from archive.org, about 11 million subagent tokens), then the merge by
     `src/expand.py`. The estimate above was too low: a page of hand copies takes a reader about an hour.
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
     Qasr Ibrim, Arminna, Shokan, Tabo, Sedeinga and Meroë. 256 texts were typed that day, 185 of them new to the
     corpus. They are kept on the author's machine, for analysis and for checking readings like FHN: the articles
     are in copyright.
8. **Faras funerary texts** (46, Griffith 1922, hand copies, archive.org `bibliothquedel234ecol`): the Karanòg
   pipeline once it passes. Check first whether that article has indexes like Karanòg's.
9. **FHN's modern transliterations** (about 30 texts, OCR in `/private/tmp/claude-501/expansion/survey/fhn/`):
   clean modern readings for private analysis only (FHN is "all rights reserved").
10. **Mask names in the Griffith rows** the way `corpus_v2` masks them, so frequency counts in `corpus_v3` mean the
    same thing; and relax `src/expand.py`'s duplicate test, which counts a short label inside a longer text as
    present (the +86 texts are a lower bound).
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
