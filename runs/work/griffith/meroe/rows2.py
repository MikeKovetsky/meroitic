import json
rows = json.load(open('/private/tmp/claude-501/griffith_scripts/meroe/rows.json'))
P = ("PARTIAL, not the inscription: Griffith prints only these words in type (names in his commentary pp. 74-77, formulae in his tables pp. 79-80); "
     "the full text is only in his hand copy, not read here. '||' separates excerpts, in the order of the text where known. "
     "Each [.] = one of Griffith's lacuna dots or hatched (damaged) signs; [x] = his restoration; '?' = his '?' or my doubt. ")
MID = "Meroe, middle cemetery, "
def r(no, page, obj, site, std, notes, rem=""):
    rows.append(dict(griffith_no=no, rem=rem, page=page, object=obj, site=site, text_std=std, notes=P + notes))
r(23, "pp. 74, 80 (leaves n205, n211)", "half of a rectangular offering table (altar) with spout", "Meroe, north group, grave 501",
  "doke || [.] mete [.] || ḫmlol : ẖolkete",
  "Style f. Name doke (Griffith's Zêke); mother '...mete...' (his Mete); formula C complete (p. 80). About a third of the text remains. Pls. LV (ii), LXX.")
r(24, "pp. 74, 79-80 (leaves n205, n210, n211)", "rectangular offering table (altar) with spout", "Meroe, north group, grave 505",
  "[.][.][.]toto || kdimkeli || skñye || ato mẖe : psoẖe : ketese : || at mẖe : psḫrke : tese || ḫmlol : pẖo[l] [:] ketese",
  "Style e. Deceased '..toto' (his '..têtê', a hatched damaged sign before it); mother kdimkeli (his Kazimakeli); father skñye (his Shakañye); formulae A, B, C. Pls. LV (iv), LXX.")
r(25, "pp. 75, 79 (leaves n206, n210)", "rectangular offering table (altar) with spout, two figures of Anubis", MID + "grave 302",
  "krpose || a?so || ato : mlo yel",
  "Style d, very archaic. Father krpose (his Karpês); deceased a?so (his Ashê, with his '?'); a variety of formula A ends the text. The mother's name (his Arêr..) is also printed in type but was not read here. "
  "Griffith: a peculiar early sign for the s of Isis, and Osiris misspelt with w for y. Pls. LV (i), LXX.")
r(26, "pp. 75, 79-80 (leaves n206, n210, n211)", "offering table (altar)", MID + "grave 302",
  "dorekid || ato mẖe : psoẖ[.] || at mlo : p[.]",
  "Style e (f in his table). Deceased's and mother's names lost with the invocation; father dorekid (his Zêrekiz); formulae A, B. Pl. LXX.")
r(27, "pp. 75, 79 (leaves n206, n210)", "offering table (altar)", MID + "tomb 307",
  "nkñ || ss?inoli || ato mlo elḫte : || at mlo elḫ || ḫ?mosidt",
  "Style d. Mother nkñ (his Nakañ); father ss?inoli (his Shashinêli, with his '?'); formulae A, B (early forms); deceased ḫ?mosidt (his Kamêshizati, '?' on one sign), written in the spout and 'probably to be read last'. The first sign of the name is the c-shaped ḫ in the type, though his English has K. Pls. LV (iii), LXX.")
r(28, "pp. 75, 79 (leaves n206, n210)", "offering table (altar)", MID + "tomb 307",
  "ato mlo : elḫte : || at mlo [.]",
  "Style d; 'the writing is extraordinarily bad'. Formulae A, B (early). The mother's name (his Ayzeke) is printed in type but was not read here; the deceased's name is illegible. Pls. LVI (i), LXXI.")
r(29, "p. 79 (leaf n210)", "offering table (altar), spout broken off", MID + "tomb 307",
  "ato mlo : yel[.]", "Style d. Formula A only (early); the names are almost destroyed. Pls. LVI (ii), LXXI.")
r(30, "p. 75 (leaf n206)", "offering table (altar)", MID + "tomb 307",
  "ylḫñ",
  "Style d. Only the name ylḫñ (his Yalkhañ), 'perhaps for a woman'; 'Isis invoked without Osiris'. REM 0430 per FHN III, which cites 'the unique invocation Wosi Msmni' (Isis and Mash-Amani) in 'the offering table text REM 0430 from Meroe City'; "
  "the match rests on that description and the REM 0400+N numbering (FHN: nos. 2, 5, 7-10, 12, 15, 18, 19), not on an explicit concordance. Pls. LVI (iii), LXXI.", rem="0430")
r(31, "p. 80 (leaf n211)", "offering table (altar)", MID + "tomb 307",
  "[.] ḫmlol : ẖolkte", "Style d-e. Only formula C, from the end of four lines between the figures. Pls. LVI (iv), LXXI.")
r(34, "p. 79 (leaf n210)", "offering table (altar), libation streaming", MID + "tomb 307",
  "atoẖ?e : yetḫte", "Style c, 'strangely ill-engraved'. Only formula A (early form). Pls. LVI (vii), LXXI.")
r(36, "p. 76 (leaf n207)", "offering table (altar) inscribed on two sides", MID + "tomb 307",
  "wosi", "Only the end of the second text (style c), 'probably the name of Isis'. Pls. LVI (ix), LXXI.")
r(37, "pp. 76, 80 (leaves n207, n211)", "offering table (altar), later style", MID + "tomb 307",
  "nnibess || ḫmlol : pẖolkete", "Style e. Deceased probably nnibess (his Nanibeshash); formula C, followed by 'a rare development of the invocation' (not printed). Pls. LVII (iv), LXXII.")
r(38, "pp. 76, 80 (leaves n207, n211)", "offering table (altar), centre raised", MID + "tomb 307",
  "ye [.][.][.] pdit?to || kebow? || [.][.][.][.][.] psiḫri?",
  "Style f. Name 'ye... pdit?to' (his Ye... pazitite, '?' his); mother kebow? (his Kebêw); then the end of formula B. Pls. LVII (i), LXXII.")
r(40, "p. 79-80 (leaves n210, n211)", "offering table (altar)", MID + "grave 311",
  "ato m[.]e : psomte || atẖe psḫrkete", "Style e. Formulae A, B; the name is much injured; A and B are followed by the names of Isis and Osiris (not printed). Pls. LVII (iii), LXXII.")
r(41, "pp. 76, 79 (leaves n207, n210)", "offering table (altar), water between two amphorae", MID + "grave 325",
  "ato : et?ḫte || srw? ato",
  "Style c, 'curiously obscure'. Formula A (early form, his '?'); then a line in the field that Griffith thinks 'may be Meroitic', with a vertical stroke between the two groups (left out) and 'or with l for w' as his alternative. "
  "His alternative reading of l. 5 (the stone turned over) and the other field line (perhaps Egyptian demotic 'man of Aswan') are not included. Pls. LVII (v), LXXII.")
r(42, "pp. 79-80 (leaves n210, n211)", "offering table (altar), spout broken off", MID + "grave 326",
  "ato [.][.] e [.][.] ḫrkte || ḫmlol : ẖolkte", "Style e. Formulae A and B fused ('may be faulty'; Griffith's 'sic' on the k), then C. Pls. LVII (vi), LXXII.")
r(45, "p. 79 (leaf n210)", "offering table (altar)", MID + "grave 362",
  "ẖolkete", "Style d. Only 'the isolated word as if from C'. Pls. LVIII (ii), LXXIII.")
r(46, "pp. 77, 79-80 (leaves n208, n210, n211)", "offering table (altar), much injured", MID + "grave 362",
  "ato mẖi : psoẖketese || a[t] mḫe rekete[se] || ḫmlol : ẖolkete :",
  "Style e. Formulae A, B, C (Griffith's 'sic' on the r of B); the invocation is repeated at the end (not printed). The mother's name (his Taqanili) is printed in type but was not read here. Pls. LVIII (iii), LXXIII.")
r(47, "pp. 77, 79-80 (leaves n208, n210, n211)", "offering table (altar)", MID + "grave 362",
  "kelekele || tidbli || ato mẖe p[.] || lowitḫe || pẖole ke [.][.]",
  "Style f. Mother kelekele (his Kelekele); father tidbli (his Tizabli); formula A begins in l. 5; l. 8 (lowitḫe, in brackets in his table) and l. 9 (the end of C?) are in the spout. Pls. LIX (i), LXXIV.")
r(49, "p. 79 (leaf n210)", "offering table (altar), Isis and Anubis with blank labels", MID + "grave 307 (excavator's note-book)",
  "ato mlo esrẖ?e?", "Style d. Only the formula resembling A (his '?' on two signs). Pls. LIX (ii), LXXIV.")
for x in rows:
    if x['griffith_no'] == 51:
        x['notes'] = x['notes'].replace("for the group d-r-p-(damaged sign) 'in l. 5' he suggests d-o-r-o-s as 'a possible reading'", "for one group 'in l. 5' he prints an alternative 'possible reading' (not included)")
    if x['griffith_no'] == 14:
        x['notes'] = x['notes'].replace("mdewetye is his '..mazetye (?)'", "mdewetye is his '..mazetye (?)' (his English has two signs fewer)")
rows.sort(key=lambda x: x['griffith_no'])
json.dump(rows, open('/private/tmp/claude-501/griffith_scripts/meroe/rows_all.json', 'w'), ensure_ascii=False, indent=1)
print(len(rows))
