import json, sys
sys.path.insert(0, '/private/tmp/claude-501/griffith_scripts/mi2b')
from mkrows import conv
SRC, ITEM = 'Meroitic Inscriptions II (Griffith 1912)', 'archaeologicals20egyp'
LINES = ("' | ' marks each line of Griffith's type (he sets one phrase per type line; an overflow printed right-aligned "
         "on the next line is joined to its line); (n) is his superscript stone-line number, kept where printed; "
         "[x] his restoration; [.] a lost sign (hatched); [...] his dots.")
SITE = ("Philae, temple of Isis, the Meroitic Chamber (second of four small chambers on the east side of the forecourt, "
        "between the two pylons, opposite the Birth-house)")
REUSE = ("Reading reused from the printed-type test of 2026-11-09 (/private/tmp/claude-501/griffith_scripts/readings.md), "
         "where it scored against FHN III no. 267 (REM 0097-0111): ")
R = []
def row(no, page, obj, std, notes):
    corpus, signs, unc = conv(std)
    R.append({'source': SRC, 'item': ITEM, 'griffith_no': no, 'rem': f'{no:04d}', 'page': page, 'object': obj,
              'site': SITE, 'text_std': std, 'text_corpus': corpus, 'uncertain': unc, 'signs': signs,
              'notes': notes + ' ' + LINES})
row(106, 'p. 38 (n57); entry p. 41 (n60)',
    'Label to figure I (right-hand series) in the band of figures of the Meroitic Chamber; published L., D. VI Bl. 5 '
    'no. 15; Berlin Academy photo; Pls. XXIV, XXX',
    'qo kroro bekemetelo pesetolo',
    REUSE + "22 of 22 FHN signs; read with Griffith's English unseen. One type line, printed on p. 38 beside no. 98; "
    "Griffith's entry (p. 41) says only 'See no. 98' for the sense (98 begins 'akrêrê, second(?) Beke-'). Re-checked "
    "on the test's crop z106.png.")
row(107, 'p. 38 (n57); entry p. 41 (n60)',
    'Label to figure J (right-hand series) in the band of figures of the Meroitic Chamber; published L., D. VI Bl. 5 '
    'no. 16; Berlin Academy photo; Pls. XXV, XXX',
    'qo kroro bekemetelo | pelmos adblito',
    REUSE + "28 of 28 FHN signs; read with Griffith's English unseen. Two type lines, printed on p. 38 beside no. 98; "
    "Griffith's entry (p. 41) says 'See no. 98'. Re-checked on the test's crop z107.png.")
row(108, 'p. 41 (n60)',
    'Label to figure K (a child) in the band of figures of the Meroitic Chamber; published L., D. VI Bl. 5 no. 17; '
    'Berlin Academy photo; Pls. XXV, XXX',
    'snneblilo mseqeto',
    REUSE + "11 of 13 FHN signs, both differences being Griffith's type against FHN (FHN Snñ*blilo: the type has n, n, "
    "e). One type line. Griffith prints his own '?' at the e of mseqeto (the test log wrote it as e?; under this file's "
    "convention it is his doubt, not a reading doubt). Griffith: the only label without the introductory qo; perhaps "
    "two descriptive words (cf. Kar. 37 for the first), or Shananebli a name followed by a genitive epithet, perhaps "
    "'(son, or slave) of Masaqe'.")
row(109, 'p. 41 (n60)',
    'Label to figure L in the band of figures of the Meroitic Chamber; published L., D. VI Bl. 5 no. 18; Pls. XXVI, XXX',
    'qo : mstrqoye wosqerlo',
    REUSE + "18 of 18 FHN signs. Printed inline in the commentary on p. 41 (entry: 'See no. 111'). Griffith prints 'sic' "
    "over the o after q, and says the label 'is carelessly written with two mistakes'. His English: 'The honourable "
    "Mashtaraqaye, qer (prophet?) of Isis.' He treats Mashtaraq and Mashtaraqaye (nos. 99-103, 109-111) as one man.")
row(111, 'p. 41 (n60), foot of the left column and head of the right',
    'Inscription in a column before figure O in the band of figures of the Meroitic Chamber; published L., D. VI Bl. 5 '
    'no. 20; Pls. XXVII, XXX',
    'qo qoreñ wosse perite wosse wos | (5)qer mstrq : ye yewi wosi yntke | lw (10)pibr pẖe qoleb ksbñ wosse | '
    'bto skel nḫeñ',
    REUSE + "75 of 78 FHN signs. Two changes to the test's text: (1) its 'qleb' is corrected to 'qoleb': at 4x "
    "(mi2b/m_111_qleb.png) the type has the q sign and then a separate long slash, the o sign, as in 'qo' at the head "
    "of the text (FHN reads q*leb, so the test's scoring did not catch it); (2) Griffith's superscript stone-line "
    "numbers 5 (before qer) and 10 (before pibr) are added. He cites the text as 111/15 for ksbñ wosse, but no "
    "superscript 15 is printed. Four type lines. Where FHN reads Mst(rqo)ye and *qewi, the type has 'mstrq : ye yewi' "
    "(checked by zoom in the test). Griffith: 'The inscription is ill-written and injured'; ll. 1-5 'The honourable (?) "
    "qeren of Isis, Agent (perite) of Isis, qer of(?) Isis, Mashtaraqaye', the equivalent of the demotic titles p qrny "
    "n Ìs, p rt n Ìs; the separation of ye from the name is curious and the next word is not intelligible; he is "
    "tempted to emend so as to give the name its usual ending; ksbñ wosse are the last words of graffiti 122 and 123, "
    "'belonging to the kashabans of Isis'.")
with open('/private/tmp/claude-501/griffith_scripts/mi2b/rows_106_111.jsonl', 'w') as f:
    for r in R:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
for r in R:
    print(r['griffith_no'], r['signs'], r['uncertain'], r['text_corpus'])
