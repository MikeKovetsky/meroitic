import json, sys
sys.path.insert(0, '/private/tmp/claude-501/griffith_scripts/mi2b')
from mkrows import conv
SRC, ITEM = 'Meroitic Inscriptions II (Griffith 1912)', 'archaeologicals20egyp'
LINES = ("' | ' separates the rows of Griffith's table (its sections A, B, C, E) that hold this text, right part before "
         "left part within a row; (n) is his superscript stone-line number, kept where printed; [x] his restoration; "
         "[.] a lost sign; [...] his dots.")
JOIN = ("A line number set between signs leaves no word space of its own in the type (16-20 px before it and 36-39 px "
        "after it, the same at every number), so words meeting at a line number are written joined, as printed.")
R = []
def row(no, page, obj, site, std, notes):
    corpus, signs, unc = conv(std)
    R.append({'source': SRC, 'item': ITEM, 'griffith_no': no, 'rem': f'{no:04d}', 'page': page, 'object': obj,
              'site': site, 'text_std': std, 'text_corpus': corpus, 'uncertain': unc, 'signs': signs,
              'notes': notes + ' ' + LINES})
row(123, 'p. 50 (n69); description p. 48 (n67); English p. 52 (n71)',
    'Graffito, seven lines neatly inscribed on one block, beginning at the junction with another block, '
    '24 x 15.5 cm; squeezes Lepsius and Borchardt, photo (Berlin Academy) no. 472; published L., D., VI, Bl. 1, no. 5; '
    'Pls. XXXVII, XL',
    'Philae, Gate of Hadrian: outer face of the west wall, south of the gateway, a little north of no. 122 and higher up',
    "tewiseti : pelmosl : ye(2)tmde : apote yeso : | di(3)lẖe tbo : | "
    "wos : pileqete(4)l : wos tebwetel : nbe(5)tw : yeberwi : | yiwri(6)yipno wos mkdilẖ : k(7)sbñ wos sebto",
    "7 stone lines; superscripts (2)-(7) printed. Printed only in the Table of Seven Graffiti of Philae (p. 50), "
    "assembled from its rows in section order: A (the right column tewiseti, then the left part), B, C (right part, "
    "then left part), E; section D has no row for 123 (its lines numbered 7 to 10 belong to 122). Griffith's queries: "
    "'?' over the ẖ and the e of di(3)lẖe; 'sic' over the e after l in pileqete(4)l. His note (p. 48): all is clear on "
    "the squeezes 'except the sign' e '(?) at the beginning of l. 3, which might possibly be' a 3-shaped sign (m/ẖ) or "
    "w, 'or even an accidental cutting'; in the table the superscript 3 stands before l of lẖe. A crack runs through "
    "the first six lines near the right-hand edges. His English (p. 52): 'The adoration made by (?) the kin of the "
    "strategus, the envoy, zilake-tabê, remaining (?) before Isis in Philae, Isis in Tebawe ....... Isis the great "
    "goddess (?), belonging to the kashbañs of Isis.' He compares tbo with 101/11 and di?e with 64; 122 and 123 end in "
    "the same three words (ksbñ wos sebto; 122 prints dividers between them). " + JOIN + " So di(3)lẖe, nbe(5)tw and "
    "yiwri(6)yipno are joined; yiwri and yipno may be two words. 3-shaped signs decided at 3-5x beside the sure m of "
    "pelmosl and ye(2)tmde (round top) and the closed s of yeso and ksbñ: ẖ (angular top, pointed middle) in di(3)lẖe "
    "and in mkdilẖ, which a first look at 2.5x had read ?kdils; p (left-pointing vertices, as in apote), not k, in "
    "yipno. No sign left uncertain by me.")
row(125, 'p. 50 (n69); description p. 49 (n68); notes pp. 51-52 (n70-n71)',
    'Graffito on a loose block, found and photographed by Junker\'s expedition of 1909; Pls. XXXVIII, XL',
    'Philae, loose block on the island; Griffith thinks it may have come from the temple of Harendotes or its approach',
    "tewiseti : pẖope aso : | (2)ḫbḫeñ dqtele nḫred(3)se : keñydi | arette te : (4)bwetele aḫrlo :",
    "4 stone lines; superscripts (2)-(4) printed. Printed only in the Table of Seven Graffiti of Philae (p. 50), "
    "assembled from its rows A, B and C, with 'end' after C. Griffith's queries: '?' over the a of aso; 'sic' over the "
    "divider in te : (4)bwetele, which splits Tebawe. His English (p. 52): 'The adoration made by (?) Pkhêpe, "
    "nakharezas keñayze of the khabkheñ in Zaq, worshipping (?) Harendotes in Tebawe.' His notes (p. 51): arette is "
    "Aretate, the god Harendotes (Hr-nt-yt-f); dqtele (125/2) is a place-name, 'in Zaq', its appendage spelt as in "
    "te : bwetele (125/3-4); aḫrlo, 'worshipper' (?), replaces the usual words of piety. The type has keñydi, final i "
    "(the i of tewiseti), where his English has keñayze. A tiny speck after q in dqtele is not a divider. " + JOIN +
    " ẖ in pẖope decided at 3x (angular top, pointed middle, against the round-topped m of 123), and Griffith renders "
    "it kh (Pkhêpe); k (right-pointing vertices) in keñydi. No sign left uncertain by me.")
with open('/private/tmp/claude-501/griffith_scripts/mi2b/rows_123_125.jsonl', 'w') as f:
    for r in R:
        line = json.dumps(r, ensure_ascii=False)
        assert json.loads(line) == r and len(r) == 12
        f.write(line + '\n')
for r in R:
    print(r['griffith_no'], r['signs'], r['uncertain'], '|', r['text_corpus'])
