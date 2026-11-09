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
BH = 'Philae, roof of the Birth-house'
row(110, 'p. 42 (n61)',
    'Label to figure M in the scenes of the Meroitic Chamber; published Lepsius, Denkmaeler VI, Bl. 5, no. 19',
    'Philae, Meroitic Chamber',
    'qo ḫbḫelẖ mstrqyeqo :',
    "One line, printed inline in the commentary on p. 42, not in a type block (p. 41: '110 to figure M. Published ib., "
    "no. 19. See no. 111.'). Griffith's English: 'The honourable chief khabkhen Mashtaraqaye.' The title is printed ḫbḫe "
    "followed by lẖ ('chief'); its fourth sign is the e sign, not ñ, although the English has khabkhen. Griffith treats "
    "the Mashtaraq and Mashtaraqaye of nos. 99-103 and 109-111 as one man, and 102, 103 and 110 as his prayers to Isis. "
    "3-shaped signs checked at 3.5x: ẖ in lẖ (pointed middle), m and s in mstrqyeqo.")
row(112, 'p. 42 (n61)',
    'Foot graffito: two feet in relief with toes in a sunk rectangle, two rudely incised feet on the left, and in front '
    'three sides of a large outlined rectangle enclosing two lines of inscription; rectangle 21 x 47 cm; squeeze '
    'Borchardt, original compared January 1910 (Pls. XXXI, XXXVI)',
    BH + ', south side',
    'stqo : leb : n[.]kete : yet : ẖlikmlo : | qo : re (2)nni dito : plmos atolit | yetemdelo :',
    "Two stone lines; Griffith sets three type lines, all kept as printed, and his superscript 2 marks where stone line 2 "
    "begins (after re). Griffith's queries (? printed over the sign): b of leb, the n before the hatched loss, i of "
    "ẖlikmlo; one more ? is printed between type lines 2 and 3, under the first n of nni (or over the l of yetemdelo). "
    "The hatched loss after n is about one sign wide, and Griffith's English has one dot. Griffith's English: 'The "
    "feet(?) of N.keteye, the ....., belonging to(?) the king Nanizi(?), related to the strategus of the water.' "
    "Commentary: stqo 'occurs in each graffito, here and in 113, in the plural'; 'The unusual spelling of' yetmdelo "
    "'occurs also in Kar. 100': the commentary prints that word with t (yetmdelo), while the text has the te sign "
    "(yetemdelo), checked at 5x. plmos is printed without e. 3-shaped signs checked at 2.5x beside the sure ẖ of no. 110 "
    "and the m of yetemdelo: ẖ at the start of ẖlikmlo, m inside it, s in stqo and plmos.")
row(113, 'p. 42 (n61)',
    'Foot graffito: one line to the right of the feet of no. 112, beneath the edge of the outlined rectangle; length '
    '16 cm; in the same squeeze as no. 112 (Pls. XXXI, XXXVI)',
    BH + ', south side',
    'stqoleb ad do[.]se',
    "One line. Griffith prints a ? at the upper left of the last sign of each word (b of stqoleb, d of ad, se of "
    "do[.]se). The hatched loss is one sign wide. Griffith's English: 'The feet of Azaze . s(?).' Commentary: perhaps "
    "the record of a modest attendant on the personage of 112, and the second pair of feet may be his.")
row(114, 'p. 43 (n62)',
    'Foot graffito: outline of two feet with toes as seen from above; in front an inscription in three lines, about '
    '19 x 7.5 cm; squeeze Borchardt (Pls. XXXII, XXXVI)',
    BH + ', south side',
    'stqo : semsti : sḫi : yet [...]',
    "Griffith does not print the three stone lines as they stand: the type is his provisional rearrangement. It 'should "
    "begin with' stqo '(l. 3) like the others, and if we treat l. 1 as a word omitted from l. 2, a remarkable parallel "
    "to 112 is obtained'. So the word order here is Griffith's, not the stone's, and he does not say which word is l. 1. "
    "His dots end the type. Griffith's queries: s of semsti, ḫ and i of sḫi. Griffith's English: 'The foot of the "
    "pilgrim (?) Shakhiye.' He adds: 'Some further signs are on the left, perhaps to be read in a column, if not "
    "meaningless scrawls. [e] following [t], as in the hand-copy, is practically impossible, and it can be seen in the "
    "photograph that there is a hole at this spot, so that it can fairly be neglected.' The same pilgrim (?) word is "
    "printed semeti in nos. 116 and 117. 3-shaped signs checked at 2.5x: m then s in semsti (closed, no tail), s in sḫi.")
row(116, 'p. 43 (n62)',
    'Foot graffito: outline of two feet with very long toes and nails as seen from above; in front an obscure Egyptian '
    'demotic inscription; at the side of the left foot a shield-shaped panel with a Meroitic inscription in four lines; '
    'feet 27 cm, shield 21 x 14 cm; squeeze Borchardt, photos Berlin Academy 722, 723, original compared January 1910 '
    '(Pls. XXXIII, XXXVI)',
    BH + ', west side',
    'stqo : semeti : [sḫi :] yeso : mete : | [...] tiy : lito :',
    "Four stone lines; Griffith sets two type lines and prints no line numbers. [sḫi :] is his restoration in square "
    "brackets, with his ? on its s. The second type line opens with his dots. His other query: t of tiy. Griffith's "
    "English: 'The foot of the pilgrim (?) Shakhiye (?) . . .' 3-shaped signs checked at 2.5x: m in semeti and mete "
    "(smooth, long tail), s in stqo and yeso (closed).")
row(117, 'p. 43 (n62)',
    'Foot graffito: outline of two feet with toes and sandal-tie, neatly cut in a rectangular frame topped by a pointed '
    'triangle with a diamond-shaped hole, as a tablet for suspension; between the frame top and the feet two '
    'inscriptions, three short lines in the right-hand corner and three longer lines to the left; feet 27.5 cm, tablet '
    '50 x 33 cm; squeeze Borchardt, photos Berlin Academy 722, 723 (Pls. XXXIV, XXXVI)',
    BH + ', north side',
    'stq : semeti : sḫi : ye mte : ant | pelqete : lito',
    "Six stone lines in two groups; Griffith prints them in his reading order in two type lines: 'the inscription was "
    "begun near the middle, and as there was not room to complete it after filling two lines, the end was written in "
    "the right-hand corner.' He marks sic over the q of stq (no o follows) and over the q of pelqete, which the type "
    "prints as ')' (the q without its stroke): 'The use of ) for [q] is very remarkable.' It is read q here by that note "
    "and by the place name (pelqe-, Philae). Griffith's ? over the e of semeti. Griffith's English: 'The foot(?) of the "
    "pilgrim(?) Shakhiye the younger (?), prophet of him (or \"her\") that is in Philae.' 3-shaped signs checked at "
    "2.5x: s in stq and sḫi, m in semeti and mte.")
row(118, 'p. 43 (n62)',
    'Graffito in black ink on the south end of the cornice, copied by H. Schaefer; looked for in January 1910, when '
    'only doubtful traces appeared to exist (Pl. XXXVI)',
    'Philae, West River-gate (undecorated stone doorway in the enclosure wall, south of Hadrian\'s gateway and west of '
    'the Birth-house)',
    'wosnsqo : metq? [...]',
    "Only part is printed, from Schaefer's copy, ending in Griffith's dots. Griffith's queries: both s of wosnsqo, the t "
    "of metq and its last sign. That last sign is the ')' sort which Griffith reads as q in no. 117 ('The use of ) for "
    "[q] is very remarkable'); it is read q here and marked uncertain, because the volume states that value only for "
    "117. Griffith: 'The first group must contain a proper name.' No translation. 3-shaped signs checked at 5x: both s "
    "of wosnsqo closed; m of metq smooth with a long tail.")
with open('/private/tmp/claude-501/griffith_scripts/mi2b/rows_110_118.jsonl', 'w') as f:
    for r in R:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
for r in R:
    print(r['griffith_no'], r['signs'], r['uncertain'], '|', r['text_corpus'])
