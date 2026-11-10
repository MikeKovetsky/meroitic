"""Checks for the Karanog scripts (src/karanog.py, src/karanog_refs.py), on made-up readings and entries.

  python3 -I tests/test_karanog.py
"""
import json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src")]

import karanog as K   # noqa: E402
import karanog_refs as R   # noqa: E402


def test_number_takes_karanog_and_shablul_only():
    assert K.number("Kar. 47") == ("Kar", 47) and K.number(" Sh. 6 ") == ("Sh", 6)
    assert K.number("Inscr. 94") is None and K.number("Kar. 47 b") is None and K.number(None) is None


def test_signs_are_counted_as_signs():
    assert K.signs("aki(2)ñtelo : pese?to [.][.] se") == ["a", "k", "i", "ñ", "te", "l", "o", "p", "e", "se", "to", ".", ".", "se"]
    assert K.signs("(12)") == [] and K.signs(" : ") == []


def test_corpus_spelling():
    # s is the se sign and S the s sign in the corpus; ñ, ḫ and ẖ become N, x and X
    assert K.to_corpus("wosi : aso(2)reyi") == "woSi aSoreyi"
    assert K.to_corpus("peseto : akiñte(5)lowi") == "pesto akiNtelowi"          # pe-se-to
    assert K.to_corpus("pes(6)to") == "peSto"                                    # pe-s-to
    assert K.to_corpus("ato mẖe : psiḫrkete") == "ato mXe pSixrkete"
    # a line number inside a word does not split it; a divider and a gap do
    assert K.to_corpus("ye(16)tmdelo(17)wi") == "yetmdelowi"
    assert K.to_corpus("nb(13)r : wñ(14)li") == "nbr wNli"
    # lost signs are dots, query marks go, restored signs in square brackets are blanked
    assert K.to_corpus("ted?[.]ḫ?elowi") == "ted.xelowi"
    assert K.to_corpus("ḫ[rp]ḫñ") == "x..xN"
    assert K.to_corpus("[.][.] : [.]") == ".. ."
    assert K.to_corpus("") == ""


def test_changed_counts_signs_not_marks():
    assert K.changed("wosi : sori", "wosi : sori") == 0
    assert K.changed("so(2)lkte", "ẖolkte") == 1                      # one sign, the line number is not one
    assert K.changed("boko", "boq") == 2                              # two signs became one
    assert K.changed("pm?rsetelo", "pẖrsetelo") == 1                  # dropping a query alone changes nothing
    assert K.changed("ps?te", "pste") == 0


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


def named(refs):
    return [(site, n, part, cf, flag) for site, n, part, cf, line, flag in R.parse_refs(refs)]


def test_references_name_inscriptions():
    assert named("Kar. 47 ♂, cf. 121") == [("Kar", 47, "", False, ""), ("Kar", 121, "", True, "")]
    assert named("Kar. 3, 17 ♂, 23 (pl.), Sh. 4") == [("Kar", 3, "", False, ""), ("Kar", 17, "", False, ""),
                                                    ("Kar", 23, "", False, ""), ("Sh", 4, "", False, "")]
    assert named("Kar. 39 b, 64a") == [("Kar", 39, "b", False, ""), ("Kar", 64, "a", False, "")]
    # a short range is a range, "118-20" is 118 to 120, a wide one is two monuments of one person
    assert [n for _, n, *_ in R.parse_refs("Kar. 77-79")] == [77, 78, 79]
    assert [n for _, n, *_ in R.parse_refs("Kar. 118-20")] == [118, 119, 120]
    assert named("Kar. 19-89 (woman)") == [("Kar", 19, "", False, "pair"), ("Kar", 89, "", False, "pair")]
    # the Shablul numbers stop at 20: the list goes on with Karanog; text/line gives the line
    assert R.parse_refs("Sh. 1, 2, 9. Later 64/23") == [("Sh", 1, "", False, None, ""), ("Sh", 2, "", False, None, ""),
                                                      ("Sh", 9, "", False, None, ""), ("Kar", 64, "", False, "23", "")]
    # not inscriptions: pages, chapters, graffiti, other publications, numbers in brackets, numbers out of range
    assert named("Kar. 29, see p. 81") == [("Kar", 29, "", False, "")]
    assert named("see pp. 24, 55") == [] and named("Kar. graff. 22") == [] and named("Kar. 28, cf. Inscr. 59") == [("Kar", 28, "", False, "")]
    assert named("Kar. 47 (four times, 12)") == [("Kar", 47, "", False, "")] and named("Kar. 209") == []
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
    assert sorted(o["reading"] for o in none) == ["aqel", "dole"]
    assert "corrected to 'bi'" in next(o for o in objs if o["reading"] == "srbiye")["notes"]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"{len(tests)} checks passed")
