# Readings of MI I nos. 1-37, transcribed from Griffith's printed Meroitic type.
# Convention: hieroglyphic type reads right to left (signs face left), lines top to bottom, columns top to bottom.
# "(n)" = Griffith's superscript stone-column number, at the point where it falls in reading order.
# "[x]" = Griffith's square brackets (restored); half-brackets (damaged trace) = "x?"; "[.]" = one lost sign (one per printed dot or hatched cell).
# " | " = printed line break at a word boundary; "|" = printed line break inside a word.
import json
HIERO = ("Meroitic hieroglyphic type, read right to left (signs face left); [x] = Griffith's restoration (blanked in "
         "text_corpus and not counted in signs), x? after a sign = Griffith's '?' or a half-bracketed trace.")
R = []
def add(no, page, obj, site, text, notes):
    R.append(dict(no=no, page=page, object=obj, site=site, text_std=text, notes=notes))

# saved 10:12
add(1, "p. 52 (leaf n63)", "base of a kneeling granite ram (statue), inscribed round the base", "Soba",
    "[.][.][.][.][.][.][.]reqerem [q?o]re : mni|tkel : pwrite : lḫ[te] : amn | [.][.][.][.][.][.][.][.]tbḫ[.][.][.][.]",
    HIERO + " Three printed lines; line 1 holds a cartouche (lost start + reqerem), followed by an Egyptian ankh sign with "
    "Griffith's '?' and a raised dot, both left out of the text. Lacunae are Griffith's dots, one [.] per dot (he estimates "
    "about seven signs lost before the cartouche's r). Griffith: the cartouche falls into two halves, '...re' and Qerem "
    "(title of the deceased on Kar. 45); qore follows the cartouche ('I have noted space only for one sign at the corner'); "
    "mnitkel = the royal title Amanitakel, as at Kalabsha 94/1; pwrite : lḫte is a phrase like those after divine names at "
    "Naga (nos. 6 ff.); then the name of Ammon (amn...). His restoration of the end (not transcribed): "
    "'pwrite : lḫ[te] : amn[....]teli : [mlowi : yi]tbḫ[te] :'. Copies of Duemichen 1863 and Ward collated with the "
    "original in January 1910; photographs Pls. XV, XVI. Cross-check: FHN III gives the Son of Rê name on this ram as "
    "Mnhreqerem (REM 0001), which ends in the reqerem read here right to left.")

add(2, "p. 53 (leaf n64)", "two cartouches beside a rock relief of a king and the sun-god", "Gebel Geili (Gebel Qeili)",
    "s?o?r?kḫr?or? | [.]q?n?ḫlme",
    HIERO + " Printed as two vertical cartouches, read top to bottom, right cartouche first; within a row of two signs the "
    "right one first. Each cartouche is topped by two flat signs with dots under them, not read. Left cartouche: a hatched "
    "(lost) block at the top, written as one [.]. All '?' are Griffith's. Griffith: 'hardly legible on the small "
    "photograph. The signs face to the right in the original. Most are doubtful; if the first cartouche is rightly read, it "
    "is the name of the prince at Amara (see Part II., no. 84), but the reading is too uncertain to serve as the basis for "
    "any argument.' Photograph Pl. XIV, fig. 2. Cross-check: FHN III reads the Gebel Qeili names as Sorkrr (Son of Rê "
    "name) and Mnslhe (throne name), REM 0002, and the same king's name as Sorkror at Amara (REM 0084), which confirms "
    "that the right cartouche is Griffith's 'first'; Griffith's type has an extra ḫ and o in it, and the second cartouche "
    "differs from Mnslhe.")

PYLON = ("Griffith prints the text in three parts: the first side line, the central cartouche (with an Egyptian bee "
         "title and two flat signs above it, not read), and the third side line. The side lines are the same on both "
         "towers ('all these letters except m being visible on either side'; the m 'is from my collation, but is not "
         "well supported by the photograph'); he reads the first as 'in ... mte' and says the third line is as in nos. "
         "6 and 7. The divider in the third line is printed in round brackets. In the cartouche a horizontal rule marks the "
         "joint between a worn upper block and a better lower block, and three dots mark a gap. ")
add(3, "p. 55 (leaf n66)", "pylon, left (south) tower, three columns in front of and above the king", "Naga, temple of the lion-god (Apedemak)",
    "[.][.][.][.][.]m?teteli | [ntkm]ni [.][.][.]qoro? | [mlo]wi : yitetbḫte",
    HIERO + " " + PYLON + "The king's name on the upper block (ntkm) is Griffith's proposed restoration, printed without brackets in his type and bracketed here: Natakamani's and "
    "Amanitere's names 'would suit the lacunae admirably... A careful examination with a good ladder might establish these "
    "readings, for which there seems in fact some justification in the photograph of the cartouche on the left.' The title "
    "below: 'The king's name was thus followed by his title qêrê (or qore)'. Breasted photos 506, 507; L., D., V., Bl. 56; Pl. XVII.")
add(4, "p. 55 (leaf n66)", "pylon, right (north) tower, three columns in front of and above the queen", "Naga, temple of the lion-god (Apedemak)",
    "[.][.][.][.][.]m?teteli | [mnitore] [.][.][.]k?tkel | [mlo]wi : yitetbḫte",
    HIERO + " " + PYLON + "The queen's name (mnitore, Amanitore) on the upper block is Griffith's proposed restoration (see no. 3), printed without brackets in his type and bracketed here. "
    "The title below is 'katakel', 'like the king's title Amanitakel in 1 and 94'; 'I was inclined to read l for the first "
    "k, but both the photograph and Lepsius's copy support k'. Breasted photos 506, 507; Pl. XVII. Cross-check: FHN III "
    "lists the queen's Daughter of Rê name with the title ktke/ktkel ('Candace') in a cartouche on this pylon as REM 0004.")

WALL = ("Text kept in Griffith's printed order. Griffith: 'In the above readings the order of the columns is disregarded "
        "in order to bring together the parallel phrases in the different inscriptions, putting the distinctive name of the "
        "deity at the beginning.' His superscript stone-column numbers are kept as '(n)' where they fall, so the stone order "
        "can be rebuilt by sorting the segments. Griffith: the gods and goddesses alike have pwrite : lbḫte, the gods also "
        "mlowi : yitebḫte, the goddesses ntke : lbḫte; 'A careful revision with the original would no doubt confirm or "
        "correct many doubtful readings' (copies collated from a ladder, January 1910). A raised dot printed inside "
        "pw-r-ite in several captions is left out.")
add(6, "p. 58 (leaf n69)", "caption of the lion-headed god (Apedemak), south wall, relief", "Naga, temple of the lion-god",
    "(1)[pede]mk : pwri(2)[te : l?]b?ḫte : | mlo(3)[wi : y]itebḫte",
    HIERO + " " + WALL + " Griffith: the name of the lion-god (Apezemak) must probably be restored, 'but whether with "
    "initial a, as in 18, is not certain. There seems hardly room for this.' Nos. 5, 6 and 9 have the signs in relief on a "
    "sunk ground. L., D., V., 62; Breasted photos 515, 516.")
add(7, "p. 58 (leaf n69)", "caption of the hawk-headed god (Haroeris or Harmakhis), south wall", "Naga, temple of the lion-god",
    "(3)[.][.]r?m?o?ke : mlo[wi l(1)bḫte :] | pwrite : lb(2)[ḫte :] mlowi : | yite?b",
    HIERO + " " + WALL + " Griffith: the name may have begun with Horus, Ar, with or without initial a; if moke is right "
    "it may be a word for the sun, 'but I was inclined to read toke on the original'. 'The terminal te is perhaps omitted "
    "twice after ḫb'. L., D., V., 61; Breasted photos 513, 514.")
add(8, "p. 58 (leaf n69)", "caption of the ram-headed god Ammon, south wall", "Naga, temple of the lion-god",
    "(1)[amni] : pwrite (2)[lb]ḫy : ml|owi : (3)[l]bḫte : s?ñptete",
    HIERO + " " + WALL + " The s is Griffith's š (pool with lotus), marked '?'. Griffith: 'Some form of the name of Ammon must have stood here: at the end to the customary phrases is added' s?ñptete, 'which looks like a place-name, \"in Napata (?)\", preceded by a doubtful sign'. L., D., V., 61.")
add(9, "p. 58 (leaf n69)", "caption of Khons, south wall, signs in relief", "Naga, temple of the lion-god",
    "aqediselo",
    HIERO + " One line, no divider. Griffith: 'The inscription of Khons, complete in one line, is cut in relief, like many of "
    "the royal names, while the others are incised. His name consists of Aqezis, the third word in the title of the "
    "human-headed Ammon in his temple'. L., D., V., 61.")
add(10, "p. 58 (leaf n69)", "caption of the ram-headed god Khnum, south wall", "Naga, temple of the lion-god",
    "(1)amnbsi : pwi(2)[ri]te? : l?o|[y?]ḫte : (3)[.][.][.][.]l?o?[.][.][.][.]",
    HIERO + " " + WALL + " Griffith prints 'sic' after pwi (the stone's i before the restored ri). The god's name reads "
    "amnbsi; Griffith: it 'can hardly be a rendering of the Greek Khnoubis. It seems rather to be analysable as a form of the "
    "name Ammon'. L., D., V., 61.")
add(13, "p. 58 (leaf n69)", "caption of Muth (Mut), north wall", "Naga, temple of the lion-god",
    "(2)ḫ[.][.][.]l[.]tl?i (3)pwrite : lbḫte | (1)nt[ki] : [l]bḫte",
    HIERO + " " + WALL + " Hatched (lost) areas: one [.] per hatched strip (one, then three). L., D., V., 58; Breasted photo 509.")
add(14, "p. 59 (leaf n70)", "caption of a negro goddess with a hawk on her head, north wall", "Naga, temple of the lion-god",
    "(1)[.][.]semi : [.]m?i(2)[.][.]li : p?wri(3)te : | l[.]ḫite : kesekeyi",
    HIERO + " " + WALL + " Hatched (lost) areas: one [.] per hatched strip. Griffith takes the deity to be a deified negress "
    "or a negro divinity, perhaps a negro Hathor.")
add(15, "p. 59 (leaf n70)", "caption of Hathor, north wall", "Naga, temple of the lion-god",
    "(2)at : riqo : (1)pwrite : lbḫy | (3)ntke : lbḫte",
    HIERO + " " + WALL + " Griffith prints '(sic)' after ntke. Griffith: 'The spelling of the name Hathor, At-(a)ri with "
    "affix qê, is very curious and interesting... Atari as compared to Egyptian Hathôr'.")
add(16, "p. 59 (leaf n70)", "caption of Satis, north wall", "Naga, temple of the lion-god",
    "[.]l?t[.][.]mni : (2)pwrite : lbḫte : | (3)ntki : lbḫte :",
    HIERO + " " + WALL + " Hatched (lost) areas: one [.] per hatched strip; a raised dot between t and l left out. Griffith: "
    "a descriptive name 'such as \"[Consort of] Amani\"' seems to be used, Amani standing for Khnum as in no. 10.")
add(18, "p. 58 (leaf n69)", "caption of the three-headed Apedemak, right half of the back (west) wall", "Naga, temple of the lion-god",
    "(2)apedemki (1)pwrite : lbḫ|(3)te? : ntke? : lbḫte",
    HIERO + " " + WALL + " The only caption here that spells the god's name with initial a. Griffith: 'All doubts about the reading of the middle line are set at rest by the inscriptions from the temple of the Lion-god at Meroë (Meroë, nos. 5, 7-10)'; on this (right, his own left) side the three-headed god 'has the phrase of the goddesses' (ntke : lbḫte). L., D., V., 59; Breasted photos 511, 512.")
add(19, "p. 58 (leaf n69)", "caption of the three-headed Apedemak, left half of the back (west) wall", "Naga, temple of the lion-god",
    "(2)[.][.][.][.][.][.][.][.](3)[.][.][.][.][.][.][.] : [pw](1)rite [:] l|bḫte :",
    HIERO + " " + WALL + " Lacunae: 8 and 7 dots as printed. An Egyptian ankh sign ends the text and is left out (Griffith: 'the ankh at the end is remarkable'). "
    "L., D., V., 59; Breasted photos 510, 511.")

# saved 10:24: Lion temple royal names, graffito 21, Amun temple 23-37
ROYAL = ("Griffith prints the royal names once for the royal cartouche groups of the walls (nos. 5, 11, 17, 20): 'Before "
         "each figure of the king and queen was engraved a cartouche, and two cartouches on a kind of banner or panel before "
         "the prince. They are best preserved on the back wall (nos. 17, 20).' This row gives those printed names "
         "(king, queen, prince's title cartouche, prince's name cartouche); it is not a separate copy of this number. "
         "Griffith: the prince's first cartouche 'with the usual termination lo, may mean \"the great (?) paqar\"', to be "
         "read first 'to judge by the direction of the signs'; the second is 'Arika-kha-rêr... with the common honorific (?) "
         "termination qo'. Egyptian titles above the cartouches (bee, etc.) are not Meroitic and are left out. Same printed "
         "text as nos. 5, 17 and 20. Cross-check: FHN III gives the prince Arikankharor's title and name in REM 0005 and 0017 "
         "as pqrtr-qo and Arikḫror-qo; Griffith's type has pqrtr-lo for the title.")
add(5, "pp. 56-57 (leaves n67-n68)", "royal cartouches (king, queen, prince) before the royalties on the south wall, signs in relief", "Naga, temple of the lion-god",
    "ntkmni | mnitore | pqrtrlo | arikḫrorqo", HIERO + " " + ROYAL + " Griffith: nos. 5, 6 and 9 on the south wall have the "
    "signs in relief on a sunk ground; the prince's cartouches 'are preserved only on the back and south walls'.")
add(17, "pp. 56-57 (leaves n67-n68)", "royal cartouches (king, queen, prince) on the back (west) wall", "Naga, temple of the lion-god",
    "ntkmni | mnitore | pqrtrlo | arikḫrorqo", HIERO + " " + ROYAL)
add(20, "pp. 56-57 (leaves n67-n68)", "royal cartouches (king, queen, prince) on the back (west) wall", "Naga, temple of the lion-god",
    "ntkmni | mnitore | pqrtrlo | arikḫrorqo", HIERO + " " + ROYAL)
add(21, "p. 60 (leaf n71)", "graffito, eleven lines, below the arm of the three-headed Apedemak, right half of the back wall", "Naga, temple of the lion-god",
    "pdmk : [.]y be teli :",
    "Meroitic cursive type, read right to left; spaces are Griffith's. Only line 1, as Griffith restores it: 'it was so much "
    "injured that, except in the first line, only a few scattered signs could be recognized. Here we may restore: ... "
    "\"Apezemak ... in ..ybe.\"' (so ybe-te-li may be one word). The hatched sign after the divider is written [.]. Cut "
    "neatly, 'in Meroite demotic of the later type' (Breasted photo 512).")

AMUN = ("The standard texts of the Amun temple are printed once on p. 63 and assigned by Griffith to several numbers; this "
        "row carries the printed text, not a separate copy. ")
HH = "amni : notete : aqedise : qom|lise"
RH = "amni : (lẖ :) ariteñ : tolktete"
HHN = ("Griffith: 'The standard inscription with the human-headed form is given twice in 23, 36, and once in 37... The "
       "name Amani is followed by a group which might mean \"in Nête\", i.e. perhaps Ne (Thebes) or Napata. The next is the "
       "name of Khons in no. 9 above... The last word is made up of well-known elements.' ")
RHN = ("Griffith: 'The inscription with the ram-headed Ammon occurs twice in 24, 35, once in 37, and in the inscriptions of "
       "the column 34': 'Amani the great, chief (?) god (?) in Têlakte.' The second word, lẖ, is printed in round brackets: "
       "'is only in the single-line inscription of the doorways'. ")
NAMES = ("The royal cartouches before the royalties carry Egyptian prenomens and titles (not transcribed) with the Meroitic "
         "names, printed on p. 63 as ntkmni (king), mnitore (queen) and arkḫtna (prince, 'Araka-khatani'; final a as printed, "
         "where no. 34 and FHN III have Arkhtni). They are not in text_std: Griffith gives them once for the doorways, not "
         "per number, though FHN III counts them in REM 0023, 0024, 0027, 0029, 0031, 0033-0038.")
add(23, "p. 63 (leaf n74)", "first (pylon) gateway, architrave, left scene: king, queen and prince before the human-headed Ammon; two short columns before the god and one behind (23, 23a)",
    "Naga, temple of Ammon (Lepsius's temple d)", HH,
    HIERO + " " + AMUN + HHN + NAMES + " L., D., V., 60a; Breasted photo 532; Pls. XXI, XXII (Pl. XXII copies 23, 24).")
add(24, "p. 63 (leaf n74)", "first (pylon) gateway, architrave, right scene: royalties before the ram-headed Ammon (24, 24a)",
    "Naga, temple of Ammon", RH, HIERO + " " + AMUN + RHN + NAMES + " L., D., V., 60a; Breasted photo 532; Pl. XXII.")
add(35, "p. 63 (leaf n74)", "second gateway, façade architrave, scene with the ram-headed Ammon ('like 24')",
    "Naga, temple of Ammon", RH, HIERO + " " + AMUN + RHN + "L., D., V., 67b (Breasted photo 533). Same printed text as no. 24.")
add(36, "p. 63 (leaf n74)", "second gateway, façade architrave, scene with the human-headed Ammon ('like 23')",
    "Naga, temple of Ammon", HH, HIERO + " " + AMUN + HHN + "L., D., V., 67b (Breasted photo 533). Same printed text as no. 23.")
add(37, "p. 63 (leaf n74)", "third gateway, façade ('inscriptions 37, 38, like 35, 36')",
    "Naga, temple of Ammon", "amni : notete : aqodise : qom|lise | amni : (lẖ :) ariteñ : tolktete",
    HIERO + " " + AMUN + "Griffith gives no. 37 one copy of each standard text, and notes that '37 here gives qo instead of "
    "qe' in aqedise, so aqodise is written here. Which copy carries the bracketed lẖ is not stated. L., D., V., 68a-c. "
    "Same printed texts as nos. 23 and 24 apart from aqodise.")

NILE = ("Nile inscriptions: 'They fall into two groups, those of the right or southern side (in this temple) and those of "
        "the left or northern.' Printed once per side; 'The inscriptions begin with ato \"water\" (see Part II., no. 97), and "
        "end with ...kete like the formula A of the funerary texts'. Griffith: 'The two phrases were evidently identical, "
        "except for the group ẖ.tmt in the second replacing the two groups ireqw : ḫwitllw in the first'; he is tempted to "
        "restore the lost sign of the left side as p (ẖ[p]tmt), and compares a fragment from Meroe (Meroe no. 21). ")
RIGHT = "ato : ireqw : ḫwitllw : diy|ẖokete"
LEFT = "ato : ẖ[.]tmt : tl[l]w : diyẖo|[kete]"
add(26, "p. 64 (leaf n75)", "column of inscription between two Nile figures, lower half of the left jamb, first gateway (left side)",
    "Naga, temple of Ammon", LEFT, HIERO + " " + NILE + "Printed once for left-side inscriptions 26 and 30. L., D., V., 66b.")
add(30, "p. 64 (leaf n75)", "column of inscription between Nile figures, passage-way of the first gateway, left side",
    "Naga, temple of Ammon", LEFT, HIERO + " " + NILE + "Printed once for left-side inscriptions 26 and 30 (same text as no. 26). L., D., V., 66d.")
add(28, "p. 64 (leaf n75)", "column of inscription between two Nile figures, lower half of the right jamb, first gateway (right side)",
    "Naga, temple of Ammon", RIGHT, HIERO + " " + NILE + "Printed once for right-side inscriptions 28 and 32. L., D., V., 66b; Breasted photo 532.")
add(32, "p. 64 (leaf n75)", "column of inscription between Nile figures, passage-way of the first gateway, right side",
    "Naga, temple of Ammon", RIGHT, HIERO + " " + NILE + "Printed once for right-side inscriptions 28 and 32 (same text as no. 28). L., D., V., 66d.")
add(29, "p. 64 (leaf n75)", "passage-way of the first gateway, left side: the ram-headed Ammon gives life to the king",
    "Naga, temple of Ammon", "amni : medese?[l?](2)[.][.][.] : [.]ḫd?sep",
    HIERO + " Hatched (lost) areas: one [.] per hatched strip. The '?' marks are Griffith's. Griffith: 'The first phrase is "
    "attached to the king in 34, 84. The termination of a word with p, if correct, is unusual.' L., D., V., 66c.")
add(31, "p. 64 (leaf n75)", "passage-way of the first gateway, right side: the ram-headed Ammon gives life to the queen",
    "Naga, temple of Ammon", "mn[i?]berote : m[.](2)stoẖepteke?[te?]",
    HIERO + " The '?' marks are Griffith's; the hatched sign after m is written [.]. Griffith: 'The first part might mean "
    "\"Ammon in Berê\"' (footnote: 'Possibly \"Meroë\"'); 'The second looks like a phrase of the type of formula A in the "
    "funerary texts', toẖe standing perhaps for atoẖe. L., D., V., 66d.")
add(34, "p. 65 (leaf n76)", "column in the court behind the first gateway: four vertical lines of inscription on the shaft",
    "Naga, temple of Ammon",
    "a?mni : ariteñ : tolktetel | ntkmni amnim[dese]l | mnitore arite[ñl]mdesel | arkḫtni mkedkel (:) md?|esel : ẖp?l : lb[.]ḫte",
    HIERO + " Griffith prints one composite text: 'The four vertical lines of inscription, so far as they are preserved and "
    "legible, repeat the same text, the only difference being in the third group from the end. The inscription on the north "
    "side (l. 1), completed from the parallels, gives' this text; 'The restorations in [ ] are from the Amara columns, no. "
    "84.' The three royal cartouches (Natakamani, Amanitore, the prince Arkḫtni) open printed lines 2 to 4. Variants for "
    "the group ẖp?l : West face (4) teñkel, East face (2) yi?r?e?wkel (Griffith's '?'), South face (3) 'almost if not quite "
    "illegible'; Lepsius's copy of line 3 has mñl for mdesel, 'probably only a mistake of the ancient or the modern copyist'. The first three words "
    "are the titles of the ram-headed Ammon (as in no. 24) 'with l added to the last word. The rest of the inscription, "
    "except the name of the prince, is exactly like no. 84 at Amara'. One [.] for the hatched strip in lb[.]ḫte. L., D., V., "
    "and Breasted; Pl. XXIII.")

if __name__ == '__main__':
    with open('draft.jsonl', 'w') as f:
        for r in sorted(R, key=lambda r: r['no']):
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(len(R), 'rows')
