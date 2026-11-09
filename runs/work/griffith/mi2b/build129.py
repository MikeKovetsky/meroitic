import json, sys
sys.path.insert(0, '/private/tmp/claude-501/griffith_scripts/mi2b')
from mkrows import conv
SRC, ITEM = 'Meroitic Inscriptions II (Griffith 1912)', 'archaeologicals20egyp'
LINES = ("' | ' marks each line of Griffith's type (he sets one phrase per type line; an overflow printed right-aligned "
         "on the next line is joined to its line); (n) is his superscript stone-line number, kept where printed; "
         "[x] his restoration; [.] a lost sign (hatched); [...] his dots.")
R = []
def row(no, page, obj, site, std, notes):
    corpus, signs, unc = conv(std)
    R.append({'source': SRC, 'item': ITEM, 'griffith_no': no, 'rem': f'{no:04d}', 'page': page, 'object': obj,
              'site': site, 'text_std': std, 'text_corpus': corpus, 'uncertain': unc, 'signs': signs,
              'notes': notes + ' ' + LINES})
row(129, 'pp. 54-55 (n73-n74)',
    'Rectangular sandstone stela with a small rectangular projection at the top, 20 lines in the later style of cursive '
    '(style g), 56 x 39.5 cm; British Museum no. 892 (presented by A. H. Rhind 1865; Budge, Sudan ii 444; Guide 1909 no. 1050)',
    'Faras: "from the island of Faras" (BM record); Griffith treats the provenance as confirmed by an altar of the same man '
    'from the Oxford excavations at Faras 1910-11',
    "wosi : soreyi : | mlowitrqowi : | syekeli t[d](2)ḫelowi : | ansyi : syeteli : te rikelowi : | qo(3)reñ : krorolowi : | "
    "qoreñ : nkdeyotowi : | womn[i](4)se krorolowi : | apotelẖ : aromelitowi : | apo(5)te : mẖeyotowi : | "
    "[a]potelw : qorete : mẖeyot : (6)nte : | ydi asḫyki : ye tekelowi : | ssi : mete : (7)mleyotowi : | "
    "apote : ẖlitetelowi : | ḫlbeñ [:] (8)ẖlitetelowi : | qo[.]ẖdḫ[.]y : akilopkri (9)[...]wdi : | "
    "kḫẖḫsel [:] ẖ[...]se : sqkelowi : | ḫr(10)pḫñ : pẖrse[te] : atpete : | yetmdelo(11)wi : | "
    "si[.]ḫẖn[...]to : kroro : sibwi ye : | ye(12)tmdelowi [:] | ateqi : sdoseteleb : ye(13)tmdelowi : | "
    "beliloke : pedemete(14)leb : yetmdelowi : | trtekese : t(15)ketoreteleb : yetmdelowi : | "
    "mle(16)yose : atiyeteleb : yetmdelo(17)wi : | ato : mẖe : yiẖekete : | atmẖe p[s](18)ḫrkete : | "
    "ḫmlolw : ẖolkete : | wos : qe(19)trri : | mklẖ : qetrri : | nsedo(20)kel : d[o]lekw : ẖolketese :",
    "20 stone lines, numbered (2)-(20) in the type. Griffith's English: Malewitar, born of Shayakeli (?), begotten of the "
    "anashayi in Shaye; qeren-akrere, qeren of Nakazeye, wemanis-akrere, chief envoy of Rome, envoy of Makheye, nate of the "
    "envoy-law qerete of Makheye, yazi ashakhayaki (?) yeteke, shashi-mete-maleyes, envoy in Khalite, khalben in Khalite, "
    "....s shaqake (?), kin of the kharpkhan in Pakharas Atapete, kin of the shi....-akrere Shibawiye, kin of ateqis in "
    "Shazes, of belilekes in Pezeme, of tartekeses in Taketere, of maleyeses in Atiye; formulae A B C, extended invocation "
    "to Isis and Mak-lakh, formula E. His queries (? printed over the sign): y and l of syekeli; k, y, a of asḫyki and i of "
    "ydi; ḫ and l of ḫlbeñ; a and p of akilopkri; q, o and the lost sign of qo[.]ẖdḫ[.]y; q of sqkelowi; the restored divider "
    "after kḫẖḫsel; e of atpete; to of si[.]ḫẖn[...]to; l and te of t(15)ketoreteleb and of atiyeteleb; y of yiẖekete; p of "
    "p[s]ḫrkete. His note to l. 8: for qo[.]ẖdḫ[.]y '[.]kroro might perhaps be read'. In [a]potelw only the second stroke of "
    "a is bracketed; the whole sign is bracketed here. His formula table (p. 60) prints formula B as p[si]ḫrkete (s and i "
    "restored) where the text has p[s]ḫrkete; its A, C and E agree with the text, and the p. 59 table confirms q (not w) in "
    "qetrri. Printed spaces kept as printed inside words known as one: 'te rikelowi', 'ye tekelowi', 'sibwi ye'. Every "
    "3-shaped sign was decided at 3.5-4x beside sure examples on the page: m narrow and smooth, ẖ wide with a pointed middle "
    "(ẖ in apotelẖ, mẖeyot, ẖlite-, ẖdḫ, kḫẖḫsel, ẖ[...]se, pẖrse, ḫẖn, mẖe, ẖolkete, mklẖ, ẖolketese). No sign left "
    "uncertain by me.")
row(130, 'p. 56 (n75)',
    'Square sandstone table of offerings with spout, 12 horizontal lines of late cursive, 32 x 36 cm; British Museum no. 901 '
    '(presented by Greville J. Chester 1865; Budge, Sudan ii 445; Guide 1909 no. 1051)',
    'Said to be from Dakka (information from Budge); the BM Guide says "from the Sudan (?)"',
    "wosi : soreyi : | qo tebi(2)silẖlowi : | antlẖ : qo(3)retite ptenoti : | teri(4)keli terikelowi : | "
    "tse(5)yis·e tedḫeli ted(6)ḫelowi : | pelmosleb (7)apoteoleb yet(8)mdelo : | mklẖli am mẖe pi(9)siḫrkete : | "
    "ḫmomo(10)le ḫitkkete mlolowi",
    "12 stone lines per Griffith; the type numbers (2)-(10). Griffith: 'The lettering is exceedingly incorrect', probably "
    "a foreigner's monument. His English: the honourable Tebishi-lakh, truly begotten of the chief qeren in Qereti (?) "
    "Patenete, truly born of Tasayishe (?), kin of strategi and envoys; O Mak-lakh; formulae B C; Male. His queries: i "
    "after (2) in tebisilẖlowi; q and t of qoretite and t of ptenoti; s of tseyis·e; ḫ, t and the second k of ḫitkkete; "
    "m, o, m, o of ḫmomole. 'sic' over the second o of apoteoleb and over the m of 'am' (for at, formula B). In tseyis·e "
    "the middle dot marks two signs, s (Griffith's š) + e, not the se sign. His formula table (p. 60) prints B as "
    "posiḫrkete with 'sic' over o, where the text (checked at 3.5x) has pi(9)siḫrkete.")
row(131, 'p. 56 (n75)',
    'Tablet in the shape of a square table of offerings, the projection at the top shaped as the disk and horns of Isis '
    'instead of a spout; lines between rules; Moscow Museum, formerly Golenischeff collection (copied from the former '
    "owner's photographs)",
    'Not stated',
    "wosi : soreyi : mklẖli : | yere(2)kiñmrẖli : bekelẖli : | kelke(3)ni mtlbe tedḫeli tedḫe(4)lebkwi : | "
    "smtlẖ : qrki(5)li : terikeli : | terikele(6)bkwi : | ssimete : pelmetreyo(7)se : mnptme : | "
    "bese : ẖboye : yetm(8)delebkwi : | mlkeyose : tepeye(9)tmite : yetmdelebkwi : | ato mẖe (10)psoẖebḫeketese : | "
    "at mẖe : ye(11)ḫrbḫeketese : | ḫmlol : molb(12)ḫeketese :",
    "Griffith describes ten lines between rules, but his type numbers stone lines (2)-(12). Two deceased, plural formulae. "
    "His English: O Isis, O Osiris, O Mak-lakh; Yerekiñamarakhali and Beke-lakhali, truly born of the kelkeni Matalabe, "
    "truly begotten of the chief shamat Qarkili, kin of the shashi-mete pelametareyes Amanap-tame and the bes (?) Khabeye, "
    "kin of the malakeyes Tepeye-tamite; formulae A B C. His notes: l. 4, for smt-lh cf. Kar. 52, Shab. 4, 'the m always "
    "uncertain'; l. 8, mlkeyose 'belonging to the malakeye (?)', cf. 132/4. His queries: ẖ of yerekiñmrẖli, m of smtlẖ, ẖ of "
    "ẖboye. Overflow lines joined: tedḫe + lebkwi (stone l. 4), yetmde + lebkwi (l. 9). His formula table (p. 60) agrees "
    "with A, B and C here.")
row(132, 'p. 57 (n76)',
    'Flat altar-shaped stone, roughly rectangular, the projection for the spout below, 11 horizontal lines of late '
    'characters without rules (cf. Areika Pl. 36 no. 5114); listed under the Moscow Museum',
    'Not stated',
    "wosi : asoreyi | (2)qo wyeteyeqo(3)wi | ḫlbiñ : adb(4)[li]to : | mlekye : ḫ(5)lbiñ yitkite(6)lo : | "
    "pelmos : tni n[.](7)tkelo : mlolo : | a(8)retroye : td(9)ḫelo : | petmos : amni(10)tnide terike(11)lo",
    "11 stone lines, numbered (2)-(11). No formulae (Griffith). His English: the honourable (?) Wayeteye, khalbiñ of the "
    "azab, malakaye and khalbiñ in Yitaki, natake of the strategus Tani, male, born of Areteréye, begotten of the strategus "
    "Amanitanize. His queries: m, n, i of amni(10)tnide; 'sic' over the t of petmos (for pelmos). The type has o in "
    "aretroye where his English has Areterêye.")
row(133, 'p. 57 (n76)',
    'Rectangular altar with spout, whitish sandstone; deep rectangular tank with four steps on each side; five pail-shaped '
    'vessels in the spout channel; the inscription runs round the borders of the tank; Cairo Museum no. 41772 (first copied '
    'from a large photograph and two squeezes in Berlin)',
    'Not stated',
    "wos : we(2)tñyiñ qe(3)li : | sori : wetr(4)ri : | qo : qedi : siye(5)qowi : | snpteli : te(6)rikeli (7)ter[i](8)kelowi : | "
    "(9)qomye : ted(10)ḫelowi : | atomẖe : (11)psiẖekete : | (12)atm(13)ẖe : p(14)siḫrkete :",
    "14 stone lines, numbered (2)-(14). Extended invocation to Isis and Osiris (also reprinted p. 59, agreeing), then "
    "Griffith's 'the honoured (?) Qezi-Shiye, truly begotten of Shanapatali, born of Qemaye'; formulae A B (his p. 60 table "
    "agrees). His queries: s of snpteli, m of qomye. Overflow joined: ter[i]ke + lowi. 'atomẖe' is printed as one group "
    "(no space, checked at 3x).")
row(134, 'p. 58 (n77)',
    'Square altar with spout, reddish-yellow sandstone, sunk square field and channel with four loaves; one line of '
    'ill-engraved cursive round the edge; 28 x 28 cm (35 cm with spout); Berlin Inventory no. 17333',
    'Purchased by Borchardt at Luxor (with nos. 135, 136); find-place not known',
    "wosi (2)soreyi : | no(3)noyeqo | atomẖe ps[...] | atmẖo psiḫrk[e]te :",
    "One line round the edge; Griffith's type in 4 lines with stone numbers (2), (3). His English: O Isis, O Osiris! "
    "Neneye; formulae A B. The type has o, not e, in the name (no-noye) and in atmẖo; Griffith's dots after ps (formula A "
    "incomplete); 'atomẖe' printed as one group. His p. 60 table prints the e of psiḫrk[e]te as lost (hatched), not restored.")
row(135, 'p. 58 (n77)',
    'Rectangular altar-shaped tablet of sandstone, seven horizontal lines of late writing between engraved rules, ending '
    'on the spout; 32 x 29.5 cm (39 cm with spout); Berlin Inventory no. 17334',
    'Purchased with no. 134 (Borchardt, Luxor)',
    "wosi : soreyi | pme(2)teqowi : tebikiqo(3)wi : | stemeyye : te(4)rikelebkwi : | tye(5)si : tdḫelebkwi | "
    "a(6)to : mẖe yoẖeb : | at : m(7)ẖe yiḫrb | ḫmlol : (8)yitkb :",
    "Seven lines plus the spout; the type numbers (2)-(8). His English: O Isis, O Osiris! Pamete and Tebiki, begotten of "
    "Shatemeyaye, born of Tayeshi; formulae A B C (plural, abbreviated: yoẖeb, yiḫrb, yitkb; his p. 60 table agrees and calls "
    "C 'type approaching D'). 'sic' over the o of yoẖeb.")
row(136, 'p. 58 (n77)',
    'Rectangular altar with spout, coarse granular pale yellow sandstone, flat surface with seven horizontal lines of late '
    'characters, much injured and worn (red paint left in the incisions); 22 x 22.5 cm; Berlin Inventory no. 17335',
    'Purchased with nos. 134, 135 (Borchardt, Luxor)',
    "wosi : sorey[i] [:] | (2)abryeqowi | (3)swe yi bye : ted(4)ḫeli tedḫelowi | (5)ato mẖe yiẖeke(6)te | at mẖe yi[ḫ](7)rkete",
    "Seven stone lines, numbered (2)-(7). His English: O Isis, O Osiris! Abaraye, truly born of Shaweyibaye; formulae A B "
    "(his p. 60 table agrees). The mother's name is printed in three groups with clear gaps ('swe yi bye'), kept as printed.")
row(137, 'p. 58 (n77)',
    'Oblong altar with short spout, soft yellowish sandstone, flat top marked as a sunken field with channel and four '
    'loaves; archaic inscription, double: (a) round the border, (b) in six horizontal lines in the field; 34 x 25 cm; '
    'Berlin Inventory no. 19327',
    'Purchased by Schäfer at Aswan, 1909',
    "(a) (1)nweliqo : | (2)mlewye : ssiẖe(3)telo : qoriselo : | kde(4)yoñqo : wosi : a(5)soreyi : | "
    "(b) (1)nweliqo : kdeyo(2)ñqo : | wosi asore(3)yi : | attḫ mloli : (4)yitḫbḫte : ato : | "
    "m(5)ḫ : yiẖbḫte : ẖr(6)mḫ : yiwebḫte :",
    "Two texts in one row: '(a)' and '(b)' mark them, and Griffith numbers the lines of each separately (a 1-5, b 1-6). "
    "Rudely executed; abnormal arrangement and rare terminal formulae (Griffith). His English: a. Naweli, malewaye in "
    "Shashikhe (?), belonging to the king; and Kazeyeñ. O Isis, O Osiris! b. Naweli and Kazeyeñ. O Isis, O Osiris! "
    "Formulae G A F. His queries: l of mlewye, i of mloli, ẖ of ẖrmḫ. His p. 60 table agrees: G = attḫ mloli : yitḫbḫte, "
    "A = ato : mḫ : yiẖbḫte, F = ẖrmḫ : yiwebḫte.")
with open('/private/tmp/claude-501/griffith_scripts/mi2b/rows_129_137.jsonl', 'w') as f:
    for r in R:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
tot = sum(r['signs'] for r in R); unc = sum(r['uncertain'] for r in R)
for r in R:
    print(r['griffith_no'], r['signs'], r['uncertain'], r['text_corpus'][:90])
print('total', tot, 'uncertain', unc)
