# saved 10:24: Lion temple royal names, graffito 21, Amun temple 23-37
ROYAL = ("Griffith prints the royal names once for the royal cartouche groups of the walls (nos. 5, 11, 17, 20): 'Before "
         "each figure of the king and queen was engraved a cartouche, and two cartouches on a kind of banner or panel before "
         "the prince. They are best preserved on the back wall (nos. 17, 20).' This row gives those printed names "
         "(king, queen, prince's title cartouche, prince's name cartouche); it is not a separate copy of this number. "
         "Griffith: the prince's first cartouche 'with the usual termination lo, may mean \"the great (?) paqar\"', to be "
         "read first 'to judge by the direction of the signs'; the second is 'Arika-kha-rêr... with the common honorific (?) "
         "termination qo'. Egyptian titles above the cartouches (bee, etc.) are not Meroitic and are left out. Same printed "
         "text as no. 17/20.")
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
         "names, printed on p. 63 as ntkmni (king), mnitore (queen) and arkḫtna (prince, 'Araka-khatani').")
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
    "illegible'; Lepsius's copy of line 3 has ñl for the l..sedm group, 'probably only a mistake'. The first three words "
    "are the titles of the ram-headed Ammon (as in no. 24) 'with l added to the last word. The rest of the inscription, "
    "except the name of the prince, is exactly like no. 84 at Amara'. One [.] for the hatched strip in lb[.]ḫte. L., D., V., "
    "and Breasted; Pl. XXIII.")
