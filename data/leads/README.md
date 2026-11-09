# Bilingual leads for Meroitic: ranked

Compiled 2026-11-08 from web sources. Each lead has its own file with the texts, the citations and the gaps.
No long bilingual text exists; what exists is people, titles and places named on both sides of the
Egyptian-Meroitic frontier. Two findings change the brief:

1. **Rilly withdrew "arme = Rome".** In his 2014 paper on the second Hamadab stela (REM 1039) he writes that
   `armil` and `armeyose` in REM 1003 have nothing to do with Rome; the Romans are `Tmey` in REM 1039, which
   also names Aswan (`Sewane`), Qasr Ibrim (`Pedeme`) and Napata (`Npte`). The Meroitic word for Rome that
   is attested is `Arome`, in 3rd-century AD titles ("great envoy to Rome").
2. **REM 1003 is the Hamadab stela in the British Museum (EA 1650)**, the "Akinidad stela". The local file
   `data/otten/Data/HamadabStelaOfAmanirenasNarrative.txt` is REM 1003, not REM 1039.

## Ranking

| Rank | Lead | File | What is online | Concrete pairings | What is missing |
|---|---|---|---|---|---|
| 1 | Philae and the Dodecaschoenus, 3rd century AD | [01-philae-dodecaschoenus.md](01-philae-dodecaschoenus.md) | Everything essential: FHN III (open access) prints the Meroitic texts REM 0088, 0089, 0097-0111, 0321, 0544 and the Demotic and Greek texts Ph. 410, 416, 417, 421, I. Philae II 180-181 with translations; Ashby 2016 (open PhD) and Griffith 1911 (public domain) add the analysis | 8 people named in Meroitic and in Demotic or Greek (plus Tami in Demotic and Greek); 24 titles, words and names, including `apote-lh Arome-li-s` = Demotic `pꜣ wpte ꜥꜣ n Hrme` "great envoy to Rome" and `peseto` = `pꜣ sꜣ-nsw` = ψεντης | No Meroitic sentence translates a Demotic one; Griffith 1912 and 1937, Pope 2008/9 and 2014, Cruz-Uribe 2016 and REM itself are print or paid; REM 0312 not seen |
| 2 | Words in Greek, Latin, Demotic, Coptic | [04-foreign-renderings.md](04-foreign-renderings.md) | Griffith 1911 pp. 8-10, FHN II-III, the classical texts | 36 rows in one consolidated table (titles, place names, divine and royal names), each marked as an Egyptian loan into Meroitic, a Meroitic word written abroad, or an independent equivalent | Most titles are Egyptian loans, so they fix sounds more than native vocabulary; Burkhardt's 36 "Meroitic" Demotic graffiti with Meroitic personal names were not listed |
| 3 | The war with Rome, 25-21/20 BC | [02-war-with-rome.md](02-war-with-rome.md) | The full Roman side (Strabo 17.1.54, Dio 54.5.4-6, Pliny 6.181-182 and 186, Res Gestae 26) in public-domain text; REM 1003 and REM 0092 in FHN II; Rilly's 2014 abstract | About 6 word meanings (`abr` man, `kdi` woman, `apote` envoy, `pelmos` general, `qes` Kush, `Tmey` Romans), 3 places named by Rilly in REM 1039, 6 Meroitic town names matched to Pliny's list, the royal names, and the men/women counts of REM 1003 | Rilly's reading and facsimile of REM 1039, the one text that names the Romans and the war's towns; Hofmann 1981's analysis of REM 1003 |
| 4 | Royal and divine names in two scripts | [03-royal-names.md](03-royal-names.md) | Griffith 1911 (his own account of the start); FHN II-III "Titles" entries, which list every Egyptian and Meroitic writing of each ruler's name | 8 royal names or titles (Natakamani *Ndkꜣmn* / `Ntkmni`, Amanitore *Imn-ꜥryt* / `Mnitore`, Candace *Kn-tj-[k]y* / `ktke` / Κανδάκη, Teqorideamani `Tkrrmn` / `(Te)qoridmni`, Ergamenes, Amanirenas, Akinidad); 6 divine names | Griffith 1911a and Lepsius' plates were not found online; the later rulers' Egyptian forms were not extracted; little vocabulary beyond names |

Philae ranks first because it is the only place where the same people, writing in two languages within a
few years, give their titles both ways. The consolidated equations rank second because they can be used at
once. The war has the most potential, since REM 1039 is a narrative of a war also told by Strabo, but almost
none of that potential is reachable until Rilly's reading is published or obtained. The royal names rank
last because Griffith already used them to set the sound values.

## The sources that carry most of the weight

1. Fontes Historiae Nubiorum II and III (Eide, Hägg, Pierce, Török 1996, 1998), open access from the
   University of Bergen: [FHN II PDF](https://data.ub.uib.no/files/manlib/ubb/ubb-msref/ubb-msref-0939/ubb-msref-0939-078/ubb-msref-0939-078-fon/ubb-msref-0939-078-fon-02/pdf/ubb-msref-0939-078-fon-02_orig.pdf)
   (42 MB) and [FHN III PDF](https://data.ub.uib.no/files/manlib/ubb/ubb-msref/ubb-msref-0939/ubb-msref-0939-078/ubb-msref-0939-078-fon/ubb-msref-0939-078-fon-03/pdf/ubb-msref-0939-078-fon-03_orig.pdf)
   (57 MB). The PDFs have a text layer, but its OCR garbles the diacritics (ñ, ḫ) and the Greek; every
   transliteration quoted in these files was read from the page images.
2. [Ashby 2016, *Calling Out to Isis: The Enduring Nubian Presence at Philae*](https://knowledge.uchicago.edu/records/c229v-78575/files/Ashby_uchicago_0330D_13172.pdf)
   (University of Chicago PhD).
3. [Griffith 1911, *Karanog: the Meroitic inscriptions of Shablul and Karanog*](https://archive.org/details/karangmeroitic00grifuoft),
   public domain, with the full equation list on pp. 8-10.
4. Rilly 2014, "Fragments of the Meroitic report of the war between Rome and Meroe", 13th Conference for
   Nubian Studies, Neuchâtel: abstract in the [HAL API record](https://api.archives-ouvertes.fr/search/?q=halId_s:halshs-01482774&fl=title_s,abstract_s,citationFull_s)
   (the [HAL page](https://shs.hal.science/halshs-01482774v1) is behind a bot check).
5. The classical texts on [LacusCurtius](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Strabo/17A3*.html)
   and [Perseus](http://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.02.0137:book=6:chapter=35).

## Using these files with the local corpus

1. The local corpus (`data/otten/Data/mero-corpus.txt`) has the Meroitic Chamber texts (REM 0097-0111), the
   "envoy to Rome" texts (REM 0129 and probably 0312), the Faras list of viceroys (REM 0544) and REM 1003.
   Search strings are in lead 1.
2. It does **not** have REM 0088 (Taêse), REM 0089 (Wayekiye A) or REM 0321 (Abratoye). Their
   transliterations are in lead 1 and can be added.
3. The corpus spells *o* as `E`, *ḫ* as `x`, *ñ* as `N`, and often `S` where FHN has *s*; the mapping is not
   one-to-one. It also swaps personal names, and `data/texts.jsonl` replaces names with `NAME` and was being
   rewritten while these notes were made, so pairings by personal name must be checked against the REM
   readings quoted here, and texts should be found by string, not by ID.

## What would add the most, in order

1. Rilly's reading of REM 1039 (the Romans as `Tmey`, the towns, "enslaved all the men, women, girls and
   boys" in lines 3-4). The obvious places to look are the Neuchâtel 2014 proceedings and Rilly's later
   books; neither was checked.
2. The Meroitic personal names in Demotic graffiti (Burkhardt 1985's 36 graffiti; Cruz-Uribe 2016's new
   ones), matched against names in the corpus, to get more sound correspondences like Wyekiye = *Wygyꜣ*.
3. Griffith 1912 (*Meroitic Inscriptions II*) and 1937 (Demotic graffiti catalogue) scans, to check the
   Philae readings against the plates.
4. Pope 2014, *Meroitic Diplomacy and the Festival of Entry* (Peeters), for the revised Ph. 416 and the
   Meroitic Chamber.
