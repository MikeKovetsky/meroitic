"""Checks for the rule-based cognate engine: the correspondence mapping, the NES spellings, the scorer
and the validation's statistics.

  python3 -I tests/test_cognates_rules.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import cognates_rules as cr   # noqa: E402
from local_only import needs, run   # noqa: E402

# local-only (README, Data): Rilly's correspondences and the word lists without an open licence
RULES_TSV = "data/nes/sound_correspondences.tsv"
LISTS = [f"data/nes/{l}.tsv" for l in ("old_nubian", "nobiin", "kenzi", "dongolawi", "midob", "birgid", "hill_nubian",
                                         "nara", "taman", "nyima", "proto_nes")]

SL = cr.Slot


def seg(s):
    return tuple(s)


def test_pattern_reads_the_script():
    assert cr.pattern("kdi") == (SL("C", "k", "I"), SL("C", "d", "M"), SL("V", "i", ""))   # [kadi]: d is M (T23)
    assert cr.pattern("ato") == (SL("V", "A", ""), SL("C", "t", "M"), SL("V", "o", ""))   # [aʈu]: t is M (T48)
    assert cr.pattern("qo") == (SL("C", "q", "I"), SL("V", "o", ""))
    assert cr.pattern("mte")[1] == SL("C", "t", "F") and cr.pattern("ked")[-1] == SL("C", "d", "F")  # T51, T22
    assert cr.pattern("abr") == (SL("V", "A", ""), SL("C", "b", "M"), SL("C", "r", "F"))   # inherent a: no slot
    assert cr.pattern("yer") == (SL("V", "Y", ""), SL("C", "r", "F"))                      # y- is a dummy
    assert cr.pattern("l-") == (SL("C", "l", "IF"),)
    assert cr.pattern("dime")[-2:] == (SL("C", "m", "F"), SL("V", "e", ""))
    assert [s.sym for s in cr.pattern("qore")] == ["q", "o", "r", "e"]


def test_corpus_spelling_maps_onto_the_standard_one():
    assert cr.mer_letters("yiroXe") == cr.mer_letters("yiroẖe") == "yiroẖe"
    assert cr.mer_letters("kemxr") == "kemḫr"
    assert cr.mer_letters("tmNteleb") == "tmneteleb"            # N is the ne sign
    assert cr.mer_letters("SSimete") == "ssimete"               # S is the s sign
    assert cr.mer_letters("atE") == "ato"                       # Millet's E is the o sign
    assert cr.pattern("kiN")[-2:] == (SL("C", "n", "F"), SL("V", "e", ""))
    for u in cr.UNKNOWN:                                        # every sign of the unknown words is read
        letters = cr.mer_letters(u)
        assert len(letters) >= len(u) and set(letters) <= set("abdeiklmnopqrstwyḫẖ"), u


def test_reflexes_follow_the_rules():
    d = cr.reflexes("d", "I", "nubian")
    assert d["r"][0] == 1.0 and "T78" in d["r"][1] and "T81" in d["r"][1]      # wide ~ wer-i, *r > d
    assert d["t"][0] == 1.0 and "n" not in d                                    # Nara n only
    assert cr.reflexes("d", "I", "nara")["n"][0] == 0.8
    assert cr.reflexes("l", "I", "nubian")["d"][0] == 1.0                      # lambdacism
    assert abs(cr.reflexes("l", "M", "nubian")["d"][0] - cr.POS_FACTOR) < 1e-12  # seen initially, counts less
    assert cr.reflexes("ḫ", "I", "nubian")["g"][0] == cr.reflexes("ẖ", "I", "nubian")["g"][0] == 1.0
    assert "t" in cr.reflexes("k", "I", "nyima") and "t" not in cr.reflexes("k", "I", "nubian")
    assert "ŋ" in cr.reflexes("k", "I", "nubian") and "ŋ" not in cr.reflexes("k", "I", "nara")
    assert cr.reflexes("b", "M", "nubian")["g"][2] == "rounded"
    assert cr.reflexes("p", "I", "nubian")["b"][0] == 1.0                      # p is a spelling of /b/
    groups = cr.expected("kdi").split()
    assert set(groups[0].split("|")) >= {"k", "ŋ"} and set(groups[1].split("|")) >= {"d", "r", "t"}
    assert "Ø" in cr.expected("dime").split()[2] and "Ø" not in cr.expected("mte").split()[0]


def tsv_rows():
    import csv
    with open(ROOT / "data/nes/sound_correspondences.tsv") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_rules_keep_their_rows_positions():
    needs(RULES_TSV)
    rows, pf = tsv_rows(), cr.POS_FACTOR
    cited = [r[5] for r in cr.RULES] + [t[-1] for t in cr.TWO.values()] + [d[3] for d in cr.DROPS.values()]
    assert all(1 <= n <= len(rows) for ns in cited for n in ns)                  # every T<n> is a row
    for m, n, w, p, groups, ns, cond in cr.RULES:                               # a shift stated for 2003-table
        if m != n and ns and max(ns) <= 53:                                     # positions only holds there
            stated = {rows[k - 1]["environment_or_note"].split("position ")[1][0] for k in ns}
            assert set(p or "IMF") <= stated, (m, n, p, stated)
    assert cr.reflexes("b", "M", "nubian")["g"][0] == 0.9                       # internal *g > b (T64) ...
    assert abs(cr.reflexes("b", "I", "nubian")["g"][0] - 0.9 * pf) < 1e-12      # ... initial *g > ḫ (T62)
    assert abs(cr.reflexes("b", "I", "nyima")["f"][0] - 0.8 * pf) < 1e-12       # Nyima f is medial (T19)
    assert abs(cr.reflexes("r", "F", "nyima")["l"][0] - 0.9 * pf) < 1e-12       # final r is Nyima r (T44)
    assert abs(cr.reflexes("ḫ", "M", "nyima")["t"][0] - 0.7 * pf) < 1e-12       # Nyima ṭ is initial (T26)
    assert abs(cr.reflexes("ḫ", "I", "nara")["h"][0] - 0.9 * pf) < 1e-12        # Nara h is medial (T28)
    for pos, grp in (("I", "nubian"), ("M", "nyima"), ("F", "taman")):          # p is a spelling of /b/ (T58)
        p, b = cr.reflexes("p", pos, grp), cr.reflexes("b", pos, grp)
        assert {n: (w, c) for n, (w, _, c) in p.items() if n != "p"} == {n: (w, c) for n, (w, _, c) in b.items()}
        assert all("T58" in lab for n, (_, lab, _) in p.items() if n != "p")


def test_rules_keep_their_rows_languages():
    assert "s" not in cr.reflexes("t", "M", "nubian") and "s" not in cr.reflexes("t", "F", "nara")
    assert cr.reflexes("t", "F", "taman")["s"][0] == 0.8                        # Proto-Taman *s (T51)
    assert "d" not in cr.reflexes("t", "M", "taman")                           # Proto-Taman keeps *t (T49)
    assert "d" not in cr.reflexes("k", "I", "nyima")                           # Ama d̪ is from *g, not *k (T75)
    assert cr.align("ato", seg("esti"), "nobiin") > cr.align("ato", seg("esti"), "nara")   # *st is Nubian (T48)
    assert abs(cr.reflexes("d", "M", "nara")["r"][0] - cr.POS_FACTOR) < 1e-12  # medial d is Nara d (T23)
    assert "q~Ø (T80)" in cr.align("qore", seg("uru"), "nobiin", trace=True)[1]
    assert "q~Ø (T80)" not in cr.align("qore", seg("uru"), "nara", trace=True)[1]     # Nubian u- (T80)
    assert "q~Ø (T80)" not in cr.align("qo", seg("ŋu"), "nobiin", trace=True)[1]      # word-initial u only


def test_same_sound_yields_where_every_row_says_otherwise():
    pf = cr.POS_FACTOR
    for mer, pos, grp in [("m", "F", "nubian"), ("m", "F", "nyima"), ("l", "I", "nubian"), ("l", "I", "taman"),
                          ("l", "F", "nara"), ("d", "M", "nubian"), ("d", "M", "nyima"), ("d", "F", "nyima"),
                          ("d", "I", "nara"), ("b", "M", "nyima"), ("t", "M", "nyima")]:
        assert abs(cr.reflexes(mer, pos, grp)[mer][0] - pf) < 1e-12, (mer, pos, grp)
    for mer, pos, grp in [("m", "M", "nubian"), ("l", "M", "nubian"), ("l", "F", "nubian"), ("d", "M", "nara"),
                          ("d", "F", "nubian"), ("b", "M", "nubian"), ("b", "F", "nyima"), ("t", "M", "taman"),
                          ("k", "F", "nubian"), ("w", "M", "nara")]:
        assert cr.reflexes(mer, pos, grp)[mer][0] == 1.0, (mer, pos, grp)      # stated, or no row says otherwise
    assert abs(cr.align("dime", seg("tim"), "nobiin") - (1.0 + 0.25 + pf) / 2) < 1e-12    # d~t, i~i, final m~m


def test_segments_handle_each_spelling():
    assert cr.segments("kˈaːčč") == seg("kac")                                 # GLD: stress, length, č
    assert cr.segments("ùbúrtí") == seg("uburti")                              # tone marks
    assert cr.segments("ɔṭo") == seg("oto") and cr.segments("ṯɛ̀g") == seg("teg")
    assert cr.segments("ǯˈugur") == seg("jugur") and cr.segments("ʃwi") == ("ʃ", "w", "i")
    assert cr.segments("weː˥r") == seg("wer")                                  # numerals: tone bars
    assert cr.segments("gEu", "asjp") == seg("geu") and cr.segments("ma5", "asjp") == ("m", "a", "ɲ")
    assert cr.segments("mas3l", "asjp") == seg("masel") and cr.segments("Nisti", "asjp") == ("ŋ", "i", "s", "t", "i")
    assert cr.segments("ouer", "wiktionary", "old_nubian") == seg("wer")       # Coptic ⲟⲩ before a vowel
    assert cr.segments("ourou", "wiktionary", "old_nubian") == seg("uru")
    assert cr.segments("godço", "wiktionary", "old_nubian") == seg("godjo")    # ⳝ
    assert cr.segments("ö́öshì", "wiktionary", "midob") == ("o", "ʃ", "i")


def test_variants_split_alternatives_not_asjp_modifiers():
    assert cr.variants("mb~a", "asjp") == ["mba"]
    assert cr.variants("o*w", "asjp") == ["ow"]
    v = cr.variants("dˈıl-t ~ dˈıl-tı")
    assert "dˈıltı" in v and "dˈılt" in v and "dˈıl" in v
    assert "douls̄t" in cr.variants("dulist- {douls̄t-} #")
    assert cr.variants("farrɛ [Wb.]") == ["farrɛ"]


def test_regular_beats_near_beats_irregular():
    reg = cr.align("kdi", seg("kari"), "nobiin")
    near = cr.align("kdi", seg("kali"), "nobiin")
    irr = cr.align("kdi", seg("kami"), "nobiin")
    assert reg > near > irr
    assert cr.align("wle", seg("wel"), "dongolawi") > cr.align("wle", seg("kari"), "nobiin")
    assert cr.align("ḫre", seg("gor"), "dongolawi") == 1.0                   # ḫ~g, r~r over two consonants


def test_conditions_and_vanishing_sounds():
    assert cr.align("abore", ("a", "ŋ", "g", "u", "r"), "nobiin") == cr.align("abore", seg("agur"), "nobiin")
    assert cr.align("abore", seg("agur"), "nobiin") > cr.align("abore", seg("agir"), "nobiin")   # b~g by o/u only
    assert cr.align("qore", seg("uru"), "nobiin") > 1.0 > cr.align("qore", seg("iri"), "nobiin")  # q~Ø before u
    assert cr.align("kdi", seg("ter"), "nyima") > cr.align("kdi", seg("ter"), "nobiin")       # Nyima k > t
    assert "m~Ø (T40)" in cr.align("dime", seg("ti"), "nobiin", trace=True)[1]           # dime ~ *tii
    assert cr.align("dime", seg("ti"), "nobiin") > cr.align("mte", seg("ti"), "nobiin")  # only a final m vanishes
    assert cr._drop(SL("C", "m", "F"), seg("ti"), 2, "nubian") == (0.5, "m~Ø (T40)")
    assert cr._drop(SL("C", "m", "M"), seg("ti"), 2, "nubian")[0] == cr.DEL


def test_trace_names_the_correspondences():
    score, used = cr.align("ḫre", seg("gor"), "dongolawi", trace=True)
    assert score == 1.0 and used[0].startswith("ḫ~g (T26") and used[1].startswith("r~r (T41")
    _, used = cr.align("abore", ("a", "ŋ", "g", "u", "r"), "nobiin", trace=True)
    assert "+ŋ unwritten nasal (T59)" in used and any(u.startswith("b~g (T64") for u in used)
    assert cr.align("st", seg("osti"), "nobiin", trace=True)[0] == cr.align("st", seg("osti"), "nobiin")


def row(gloss, form="x", lang="nobiin"):
    return cr.Row(lang, form, gloss, frozenset(cr.cognates.keys(gloss)), "gld", "", ((form, seg(form)),))


def test_shuffle_p_is_never_zero_and_ties_count_against():
    words = [(f"w{i}", frozenset({g}), g) for i, g in enumerate(["water", "fire", "stone", "tree", "bird", "fish"])]
    rows = [row(g) for _, _, g in words]
    perfect = {f: [1.0 if j == i else 0.0 for j in range(len(rows))] for i, (f, _, _) in enumerate(words)}
    t = cr.shuffle_test(words, rows, perfect, sims=500)
    assert t["stat"] == 1.0 and t["p"] >= 1 / 501 and t["p"] < 0.05
    flat = {f: [0.5] * len(rows) for f, _, _ in words}
    assert cr.shuffle_test(words, rows, flat, sims=200)["p"] == 1.0


def test_top_precision_shares_ties():
    words = [("a", frozenset({"water"}), "water"), ("b", frozenset({"fire"}), "fire")]
    rows = [row("water"), row("stone"), row("fire"), row("tree")]
    S = {"a": [1.0, 1.0, 0.0, 0.0], "b": [0.0, 0.0, 0.2, 0.9]}
    t = cr.top_test(words, rows, S, sims=50)
    assert abs(t["prec"] - 0.25) < 1e-12 and t["hits"] == ["a"]                # (1/2 + 0) / 2
    assert abs(t["chance"] - 0.25) < 1e-12                                       # one row in four, each word
    t2 = cr.top_test(words, rows, S, sims=50, k=2)
    assert abs(t2["prec"] - 0.5) < 1e-12                                         # (1/2 + 1/2) / 2
    assert cr.ranks(words, rows, S) == [1.5, 2]                                 # a's water row ties with stone


def test_ranks_break_ties_at_random():
    assert cr.tie_rank([0.9, 0.5, 0.1], 0.9) == 1                              # alone at the top
    assert cr.tie_rank([1.0, 1.0, 1.0, 0.2], 1.0) == 2                         # one of three tied: (3 + 1) / 2
    assert cr.tie_rank([2.0, 1.0, 1.0, 1.0, 1.0, 1.0], 1.0, hits=2) == 3       # 1 above, first of 2 among 5
    rows = [row("water"), row("stone"), row("tree"), row("fire")]
    words = [("a", frozenset({"water"}), "water")]
    assert cr.ranks(words, rows, {"a": [0.5, 0.5, 0.5, 0.5]}) == [2.5]         # a flat scorer earns no rank


def test_proto_repeats_are_one_form():
    rows = [cr.Row("proto_nes", f, "g", frozenset(), "literature", "", tuple((v, seg(v)) for v in vs))
            for f, vs in (("*ᵑkod", ["kod"]), ("*kod-", ["kod"]), ("*ŋod-", ["ŋod"]), ("*kari", ["kari"]))]
    forms = cr.proto_forms(rows)
    assert len(forms) == 3 and forms[frozenset({seg("kod")})] == [0, 1]
    scores = {k: max(cr.align("ked", rows[i].variants[0][1], "proto_nes") for i in ix) for k, ix in forms.items()}
    t = scores[frozenset({seg("kod")})]
    assert cr.tie_rank(scores.values(), t) == 1                                # its repeat is not a rival


def test_rank_median_is_the_middle():
    assert cr.rank_stats([1, 2, 3, 10]) == (2.5, 1, 4)                         # even count: mean of the middle two
    assert cr.rank_stats([1, 3, 471, 551, 900, 1200]) == (511, 1, 2)
    assert cr.rank_stats([7, 12, 30]) == (12, 7, 1)


def test_validation_words_leave_out_loans_names_and_circular_lists():
    needs(*LISTS)
    words, left = cr.gold_words()
    forms = {f for f, _, _ in words}
    assert not forms & set(cr.LOANS) and {f for f, _ in left} >= set(cr.LOANS)
    assert {"pelmos", "peseto", "apote", "ant", "kisri", "tewiseti"} <= {f for f, _ in left}
    assert {"kdi", "wle", "qore", "sem"} <= forms and not forms & {"wos", "amni", "bedewe", "nob", "ms"}
    rows = cr.load_nes()
    assert {r.lang for r in rows} == {"old_nubian", "nobiin", "kenzi", "dongolawi", "midob", "birgid",
                                      "hill_nubian", "nara", "taman", "nyima"}                 # no proto_nes
    assert not any(r.dataset == "wiktionary" and r.form in ("theophilos", "M") for r in rows)  # names, letters
    assert {r.lang for r in cr.load_nes(proto=True)} == {"proto_nes"}


def test_lists_need_both_tests():
    res = {"rule": {"all": {"p": 0.01}, "held": {"p": 0.2}}}
    assert not cr.earned(res)
    res["rule"]["held"]["p"] = 0.04
    assert cr.earned(res)


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")])
