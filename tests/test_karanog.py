"""Checks for the Karanog scripts (src/karanog.py, src/karanog_refs.py, runs/work/karanog/score_fhn.py): on
made-up readings and entries, and the numbers data/expansion/karanog/README.md reports.

  python3 -I tests/test_karanog.py
"""
import json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests"), str(ROOT / "runs/work/karanog")]

import karanog as K   # noqa: E402
import karanog_refs as R   # noqa: E402
import compare_typings, score_fhn   # noqa: E402
from local_only import needs, run   # noqa: E402

READINGS = ROOT / "data/expansion/karanog/readings"


def test_number_takes_karanog_and_shablul_only():
    assert K.number("Kar. 47") == ("Kar", 47) and K.number(" Sh. 6 ") == ("Sh", 6)
    assert K.number("Inscr. 94") is None and K.number("Kar. 47 b") is None and K.number(None) is None


def test_signs_are_counted_as_signs():
    assert K.signs("aki(2)ñtelo : pese?to [.][.] se") == ["a", "k", "i", "ñ", "te", "l", "o", "p", "e", "se", "to", ".", ".", "se"]
    assert K.signs("(12)") == [] and K.signs(" : ") == []
    # a line number or a query mark parts two signs: t and e, not the te sign; s and e, not the se sign
    assert K.signs("arwt(14)e") == ["a", "r", "w", "t", "e"] and K.signs("psos?e") == ["p", "s", "o", "s", "e"]
    assert K.signs("pe(6)seto") == ["p", "e", "se", "to"]
    # a restoration in square brackets is not read from the copy: lost, as in the other Griffith files
    assert K.signs("ḫ[rp]ḫñ") == ["ḫ", ".", ".", "ḫ", "ñ"]


def test_corpus_spelling():
    # s is the se sign and S the s sign in the corpus; ñ, ḫ and ẖ become N, x and X
    assert K.to_corpus("wosi : aso(2)reyi") == "woSi aSoreyi"
    assert K.to_corpus("peseto : akiñte(5)lowi") == "pesto akiNtelowi"          # pe-se-to
    assert K.to_corpus("pes(6)to") == "peSto"                                    # pe-s-to
    assert K.to_corpus("ato mẖe : psiḫrkete") == "ato mXe pSixrkete"
    # a line number inside a word does not split it; a divider and a gap do
    assert K.to_corpus("ye(16)tmdelo(17)wi") == "yetmdelowi"
    assert K.to_corpus("nb(13)r : wñ(14)li") == "nbr wNli"
    assert K.to_corpus("psos?e(7)kete") == "pSoSekete"                           # s? then e: the s sign
    # lost signs are dots, query marks go, restored signs in square brackets are blanked
    assert K.to_corpus("ted?[.]ḫ?elowi") == "ted.xelowi"
    assert K.to_corpus("ḫ[rp]ḫñ") == "x..xN" and K.to_corpus("ab[r : p]") == "ab.."
    assert K.to_corpus("[.][.] : [.]") == ".. ."
    assert K.to_corpus("") == ""


def test_changed_counts_signs_not_marks():
    assert K.changed("wosi : sori", "wosi : sori") == 0
    assert K.changed("so(2)lkte", "ẖolkte") == 1                      # one sign, the line number is not one
    assert K.changed("boko", "boq") == 2 and K.changed("boq", "boko") == 2      # the longer side of a change
    assert K.changed("wosi", "wosiye") == 2 and K.changed("wosiye", "wosi") == 2  # signs added or dropped count
    assert K.changed("pm?rsetelo", "pẖrsetelo") == 1                  # dropping a query alone changes nothing
    assert K.changed("ps?te", "pste") == 0
    assert K.changed("arwt(14)e", "arwt(14)l") == 1                   # Kar. 47: e became l, the t stayed


def write(d, name, objs):
    (d / name).write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs))


def test_rows_join_parts_and_skip_unchecked_packs():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        done, open_ = root / "C01", root / "C02"
        done.mkdir()
        open_.mkdir()
        first = [{"text": "Kar. 2", "part": "A", "page": "leaf_144", "caption": "Kar. 2. Stela", "labels": ["before woman"],
                  "reading": "(1)wosi : so(2)reyi"},
                 {"text": "Kar. 2", "part": "B", "page": "leaf_144", "caption": "Kar. 2. Stela", "labels": [],
                  "reading": "ato mḫe"},
                 {"text": "Sh. 4", "part": "", "page": "leaf_190", "caption": "Sh. 4. Altar", "labels": [], "reading": "qo : [.]se?"}]
        final = [dict(first[0], entries=2, check_notes=""), dict(first[1], reading="ato mẖe", entries=1, check_notes="formula A"),
                 dict(first[2], entries=0, check_notes="")]
        write(done, "copy_only.jsonl", first)
        write(done, "final.jsonl", final)
        write(done, "kept_against_type.jsonl", [{"text": "Kar. 2", "copy": "sori", "type": "soreyi", "why": "clear"}])
        write(done, "unplaced.jsonl", [{"text": "Sh. 4", "source": "Index A", "reading": "pesto", "why": "lost"}])
        write(open_, "copy_only.jsonl", [dict(first[2], text="Kar. 9")])          # no final.jsonl: not checked yet
        rows = K.rows(root)
        # a reading that names no inscription stops the build: it would otherwise be left out without a word
        write(open_, "final.jsonl", [dict(final[2], text="Kar. 39 b")])
        try:
            K.rows(root)
        except ValueError as e:
            assert "'Kar. 39 b'" in str(e) and "final.jsonl" in str(e), e
        else:
            raise AssertionError("a reading of 'Kar. 39 b' was dropped without an error")
    assert [r["griffith_no"] for r in rows] == [2, "Sh4"], rows                   # Karanog first, Kar. 9 left out
    kar, sh = rows
    assert kar["rem"] == "0202" and sh["rem"] == "" and kar["site"] == "Karanog" and sh["site"] == "Shablul"
    assert kar["page"] == "p. 129 (leaf n144)" and kar["object"] == "Stela" and sh["object"] == "Altar"
    assert kar["text_std"] == "A: (1)wosi : so(2)reyi | B: ato mẖe"
    assert kar["text_corpus"] == "woSi Soreyi ato mXe" and kar["signs"] == 15 and kar["uncertain"] == 0
    assert "3 printed entries placed, 1 signs changed" in kar["notes"] and "sori (type: soreyi)" in kar["notes"]
    assert "formula A" in kar["notes"] and "before woman" in kar["notes"]
    assert sh["text_corpus"] == "qo .s" and sh["signs"] == 3 and sh["uncertain"] == 1
    assert "pesto (Index A)" in sh["notes"]
    assert all(K.ACCURACY in r["notes"] for r in rows)                          # the measured accuracy, in each row


def named(refs):
    return [(site, n, part, cf, flag) for site, n, part, cf, line, flag in R.parse_refs(refs)]


def test_references_name_inscriptions():
    assert named("Kar. 47 ♂, cf. 121") == [("Kar", 47, "", False, ""), ("Kar", 121, "", True, "")]
    assert named("Kar. 3, 17 ♂, 23 (pl.), Sh. 4") == [("Kar", 3, "", False, ""), ("Kar", 17, "", False, ""),
                                                    ("Kar", 23, "", False, ""), ("Sh", 4, "", False, "")]
    assert named("Kar. 39 b, 64a, 101 c") == [("Kar", 39, "b", False, ""), ("Kar", 64, "a", False, ""), ("Kar", 101, "c", False, "")]
    # a letter alone after a comma is another part of the number before it
    assert named("Kar. 38, 101 a, b, c, in form H.") == [("Kar", 38, "", False, ""), ("Kar", 101, "a", False, ""),
                                                        ("Kar", 101, "b", False, ""), ("Kar", 101, "c", False, "")]
    assert R.parse_refs("later 30/13, 31 a/15, b/14, 38/5") == [("Kar", 30, "", False, "13", ""), ("Kar", 31, "a", False, "15", ""),
                                                              ("Kar", 31, "b", False, "14", ""), ("Kar", 38, "", False, "5", "")]
    assert named("Kar. 8 a, &c.") == [("Kar", 8, "a", False, "")]
    # a short range is a range, "118-20" is 118 to 120, a wide one is two monuments of one person
    assert [n for _, n, *_ in R.parse_refs("Kar. 77-79")] == [77, 78, 79]
    assert [n for _, n, *_ in R.parse_refs("Kar. 118-20")] == [118, 119, 120]
    assert named("Kar. 19-89 (woman)") == [("Kar", 19, "", False, "pair"), ("Kar", 89, "", False, "pair")]
    # the Shablul numbers stop at 20: the list goes on with Karanog; text/line gives the line
    assert R.parse_refs("Sh. 1, 2, 9. Later 64/23") == [("Sh", 1, "", False, None, ""), ("Sh", 2, "", False, None, ""),
                                                      ("Sh", 9, "", False, None, ""), ("Kar", 64, "", False, "23", "")]
    # not inscriptions: pages, chapters, graffiti, other publications, numbers in brackets, numbers out of range
    assert named("Kar. 29, see p. 81") == [("Kar", 29, "", False, "")] and named("Kar. 29, see p. 81, 47")[-1][1] == 47
    assert named("see pp. 24, 55") == [] and named("Kar. graff. 22") == [] and named("Kar. 28, cf. Inscr. 59") == [("Kar", 28, "", False, "")]
    # after "pp." every number is a page, up to the next site
    assert named("Kar. 56, see pp. 9, 82") == [("Kar", 56, "", False, "")]
    assert named("Kar. 126, in form B. Kar. 95, Sh. 9, see pp. 45, 48") == [("Kar", 126, "", False, ""), ("Kar", 95, "", False, ""),
                                                                           ("Sh", 9, "", False, "")]
    assert named("Kar. 12, see pp. 24, 55; Kar. 30") == [("Kar", 12, "", False, ""), ("Kar", 30, "", False, "")]
    assert named("Kar. 47 (four times, 12)") == [("Kar", 47, "", False, "")] and named("Kar. 209") == [] and named("Kar. 0") == []
    assert named("Kar. 105, 126, Kar. Ostr. 1/7") == [("Kar", 105, "", False, ""), ("Kar", 126, "", False, "")]
    assert named("n. B. Kar. 34, cf. Kar. Ostr. 3") == [("Kar", 34, "", False, "")]
    assert named("in form D 2. Kar. 36, 127,") == [("Kar", 36, "", False, ""), ("Kar", 127, "", False, "")]
    assert named("n. A 2. Kar. 8") == [("Kar", 8, "", False, "")] and named("Kar. 92, see p. 82, note 5") == [("Kar", 92, "", False, "")]
    # a form printed inside the entry has its own object: its numbers are not the head word's
    assert named("Kar. 7, 130. {pḫkete} Kar. 93, see p. 48") == [("Kar", 7, "", False, ""), ("Kar", 130, "", False, "")]
    assert named("Kar. 15 (man), cf. 21 ♂; Kar. 30") == [("Kar", 15, "", False, ""), ("Kar", 21, "", True, ""), ("Kar", 30, "", False, "")]
    assert R.text_id("Kar. 39 b") == ("Kar", 39, "b") and R.text_id("Sh. 1") == ("Sh", 1, "") and R.text_id("Inscr. 94/12") is None


def test_typed_pages_are_repaired_and_tabled():
    name = lambda page, text, col, reading, **kw: dict({"page": page, "kind": "name", "text": text, "person": 1, "col": col,
                                                        "reading": reading, "marks": "", "notes": ""}, **kw)
    with tempfile.TemporaryDirectory() as tmp:
        refs = Path(tmp)
        for d in ("typed/N1", "typed/N2", "typed/I1", "typed/F1", "second_typing/QA"):
            (refs / d).mkdir(parents=True)
        write(refs / "typed/N1", "ref_pdf103.jsonl", [name("ref_pdf103", "Kar. 1", "B", "sriiye"), name("ref_pdf103", "Kar. 6", "B", "tẖiye")])
        write(refs / "typed/N2", "ref_pdf107.jsonl", [name("ref_pdf107", "Kar. 72", "A", "tiiye")])           # not N1: left alone
        write(refs / "second_typing/QA", "ref_pdf103.jsonl", [name("ref_pdf103", "Kar. 1", "B", "srbiye"), name("ref_pdf103", "Kar. 6", "B", "tmiye")])
        write(refs / "typed/I1", "ref_pdf111.jsonl", [
            {"page": "ref_pdf111", "kind": "index", "index": "A", "reading": "ant : boqḫw", "supplied": "", "refs": "Kar. 47 ♂, cf. 121", "gloss": "", "notes": ""},
            {"page": "ref_pdf111", "kind": "index", "index": "A", "reading": "aqel", "supplied": "", "refs": "Kar. graff. 22", "gloss": "", "notes": ""}])
        write(refs / "typed/F1", "ref_pdf059.jsonl", [
            {"page": "ref_pdf059", "kind": "formula", "formula": "A", "text": "Kar. 1", "reading": "ato mẖe", "where": "table", "notes": ""},
            {"page": "ref_pdf059", "kind": "formula", "formula": "A", "text": "Kar. 133", "reading": "ato mẖe", "where": "table", "notes": ""},
            {"page": "ref_pdf059", "kind": "formula", "formula": "A", "text": "Sh. 0", "reading": "ato mẖe", "where": "table", "notes": ""},
            {"page": "ref_pdf068", "kind": "formula", "formula": "E", "text": "Inscr. 137", "reading": "dole", "where": "prose", "notes": ""}])
        objs = R.typed(refs)
    per, none = R.tables(objs)
    got = {k: [(e["source"], e["reading"], e["compare_only"]) for e in v] for k, v in per.items()}
    # the first typist's "ii" is b + i; the second typing is added only where it still differs
    assert ("names table, column B (person 1)", "srbiye", False) in got[("Kar", 1)] and len(got[("Kar", 1)]) == 2, got[("Kar", 1)]
    assert [r for _, r, _ in got[("Kar", 6)]] == ["tẖiye", "tmiye"], got[("Kar", 6)]
    assert [r for _, r, _ in got[("Kar", 72)]] == ["tiiye"]
    assert got[("Kar", 47)] == [("Index A", "ant : boqḫw", False)] and got[("Kar", 121)] == [("Index A", "ant : boqḫw", True)]
    assert ("formula A (table)", "ato mẖe", False) in got[("Kar", 1)]
    assert ("Kar", 133) not in per and ("Sh", 0) not in per
    assert sorted(o.get("text") or o["reading"] for o in none) == ["Inscr. 137", "Kar. 133", "Sh. 0", "aqel"]
    assert "corrected to 'bi'" in next(o for o in objs if o["reading"] == "srbiye")["notes"]


def lines(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def test_files_in_the_repo_are_what_the_scripts_write():
    # src/karanog_refs.py and src/karanog.py were run after their last change
    objs = R.typed()
    per, _ = R.tables(objs)
    assert lines(R.REFS / "all_refs.jsonl") == objs
    tables = {p.stem: lines(p) for p in (R.REFS / "by_inscription").glob("*.jsonl")}
    assert tables == {f"{s}_{n:03d}": es for (s, n), es in per.items()}
    assert lines(K.KAR / "griffith_karanog.jsonl") == K.rows()


def test_reported_karanog_numbers():
    # data/expansion/karanog/README.md, sections 1, 2 and 4, and NEXT_STEPS.md, step 5
    rows = K.rows()
    words = sum(len([w for w in r["text_corpus"].split() if w.strip(".")]) for r in rows)
    assert (len(rows), sum(r["signs"] for r in rows), words) == (19, 2170, 342)
    objs = R.typed()
    per, _ = R.tables(objs)
    assert (len(objs), sum(o["typist"] == "QA" for o in objs), len(per), sum(map(len, per.values()))) == (2722, 4, 152, 3545)
    assert min(map(len, per.values())) >= 2
    packs = [p for p in sorted(READINGS.iterdir()) if p.is_dir()]
    first = [o for p in packs for o in K.load(p, "copy_only.jsonl")]
    final = [o for p in packs for o in K.load(p, "final.jsonl")]
    count = lambda name: sum(len(K.load(p, name)) for p in packs)
    assert (sum(len(K.signs(o["reading"])) for o in first), sum(K.changed(a["reading"], b["reading"]) for a, b in zip(first, final)),
            sum(o["entries"] for o in final), count("kept_against_type.jsonl"), count("ref_corrections.jsonl"),
            count("unplaced.jsonl")) == (2195, 237, 492, 33, 14, 39)
    # the measured accuracy, by the first test's measure (signs right = FHN's signs less the edit distance)
    toks, align, fhn = score_fhn.first_test(ROOT)
    total = lambda name: tuple(map(sum, zip(*[r[:2] for r in score_fhn.score(
        toks, align, fhn, score_fhn.readings([READINGS / p / name for p in ("C09", "C14", "C21")])).values()])))
    assert total("final.jsonl") == (654, 639) and total("copy_only.jsonl") == (654, 582)
    assert "639 of 654 signs right (97.7%)" in K.ACCURACY and "582 (89.0%)" in K.ACCURACY


def test_reported_typing_agreement():
    # data/expansion/karanog/README.md, section 3: the four pages typed twice
    got = {}
    for q in sorted((R.REFS / "second_typing/QA").glob("ref_pdf*.jsonl")):
        first = next((R.REFS / "typed").glob(f"*/{q.name}"))
        got[q.stem] = compare_typings.compare(compare_typings.load(first), compare_typings.load(q))[:2]
    assert got == {"ref_pdf059": (766, 780), "ref_pdf103": (389, 398), "ref_pdf113": (643, 646), "ref_pdf130": (565, 568)}


def test_score_counts_extra_signs_and_parts_signs_at_marks():
    toks, align, _ = score_fhn.first_test(ROOT)
    assert toks(score_fhn.clean("psos?e(7)kete")) == ["p", "s", "o", "s", "e", "k", "e", "te"]   # s? e, not se
    assert toks(score_fhn.clean("arwt(14)e [.]se?")) == ["a", "r", "w", "t", "e", "se"]
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "final.jsonl"
        write(Path(tmp), f.name, [{"text": "Kar. 47", "part": "", "reading": "(1)wosi : sor(2)eyi"},
                                  {"text": "Kar. 77", "part": "", "reading": "ato mẖe : pẖ"}, {"text": "Kar. 2", "part": "", "reading": "qo"}])
        rd = score_fhn.readings([f])
    assert sorted(rd) == ["0247", "0277"]
    # (the edition's signs, right, different, missing, extra): line numbers and dividers are not signs, and
    # pẖ against pẖte is one sign missing
    res = score_fhn.score(toks, align, {"0247": "wosi soreyi", "0277": "ato mẖe pẖte", "0321": "wosi"}, rd)
    assert res["0247"][:5] == (10, 10, 0, 0, 0) and res["0277"][:5] == (8, 7, 0, 1, 0) and "0321" not in res
    # an extra sign counts against the reading, as in the first test: 6 of 8, not 8 of 8
    res = score_fhn.score(toks, align, {"0247": "wosi sore"}, {"0247": "wosi soreyi"})
    assert res["0247"][:5] == (8, 6, 0, 0, 2)


def test_reported_carrier_numbers():
    needs(score_fhn.CARRIER)
    toks, align, _ = score_fhn.first_test(ROOT)
    res = score_fhn.score(toks, align, score_fhn.carrier(ROOT),
                          score_fhn.readings([READINGS / p / "final.jsonl" for p in ("C09", "C14")]))
    assert sorted(res) == ["0247", "0277", "0278"] and tuple(map(sum, zip(*[r[:2] for r in res.values()]))) == (609, 598)


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")])
