"""Checks for the Karanog scripts (src/karanog.py, src/karanog_refs.py, runs/work/karanog/score_fhn.py and
compare_readers.py): on made-up readings and entries, and the numbers data/expansion/karanog/README.md reports.

  python3 -I tests/test_karanog.py
"""
import json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests"), str(ROOT / "runs/work/karanog")]

import karanog as K   # noqa: E402
import karanog_refs as R   # noqa: E402
import compare_readers, compare_typings, score_fhn   # noqa: E402
from local_only import needs, run   # noqa: E402

READINGS = ROOT / "data/expansion/karanog/readings"


def test_number_takes_karanog_and_shablul_only():
    assert K.number("Kar. 47") == ("Kar", 47) and K.number(" Sh. 6 ") == ("Sh", 6)
    assert K.number("Inscr. 94") is None and K.number("Kar. 47 b") is None and K.number(None) is None
    assert K.number("Kar. 39 b", part_ok=True) == ("Kar", 39) and K.number("Kar. 39 x", part_ok=True) is None


def test_signs_are_counted_as_signs():
    assert K.signs("aki(2)ñtelo : pese?to [.][.] se") == ["a", "k", "i", "ñ", "te", "l", "o", "p", "e", "se", "to", ".", ".", "se"]
    assert K.signs("(12)") == [] and K.signs(" : ") == []
    # a line number or a query mark parts two signs: t and e, not the te sign; s and e, not the se sign
    assert K.signs("arwt(14)e") == ["a", "r", "w", "t", "e"] and K.signs("psos?e") == ["p", "s", "o", "s", "e"]
    assert K.signs("pe(6)seto") == ["p", "e", "se", "to"]
    # a restoration in square brackets is not read from the copy: lost, as in the other Griffith files
    assert K.signs("ḫ[rp]ḫñ") == ["ḫ", ".", ".", "ḫ", "ñ"]
    # Griffith's "(sic)" by a sign is not the signs s and i (Kar. 84, Sh. 2), and it parts two signs too
    assert K.signs("ted(sic)ḫe") == ["te", "d", "ḫ", "e"] and K.signs("t(sic)e") == ["t", "e"]
    assert K.stray("(1)wosi : s?o(2)r[.]e(sic)yi [r : p]") == "" and K.stray("wosi (c) š-") == "(c)š-"


def test_corpus_spelling():
    # s is the se sign and S the s sign in the corpus; ñ, ḫ and ẖ become N, x and X
    assert K.to_corpus("wosi : aso(2)reyi") == "woSi aSoreyi"
    assert K.to_corpus("peseto : akiñte(5)lowi") == "pesto akiNtelowi"          # pe-se-to
    assert K.to_corpus("pes(6)to") == "peSto"                                    # pe-s-to
    assert K.to_corpus("ato mẖe : psiḫrkete") == "ato mXe pSixrkete"
    # a line number inside a word does not split it; a divider and a gap do
    assert K.to_corpus("ye(16)tmdelo(17)wi") == "yetmdelowi"
    assert K.to_corpus("nb(13)r : wñ(14)li") == "nbr wNli" and K.to_corpus("wosi:sori") == "woSi Sori"
    assert K.to_corpus("psos?e(7)kete") == "pSoSekete"                           # s? then e: the s sign
    assert K.to_corpus("(4)ted(sic)ḫe?l?owi : a(sic)mẖe") == "tedxelowi amXe"      # Kar. 84, Sh. 2
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
        # Kar. 3's parts come back in another order: no count of signs changed rather than a wrong one
        swapped = [dict(first[0], text="Kar. 3", part=p, caption="Kar. 3. Altar") for p in ("A", "B")]
        write(done, "copy_only.jsonl", first + swapped)
        write(done, "final.jsonl", final + [dict(o, entries=0, check_notes="") for o in swapped[::-1]])
        write(done, "kept_against_type.jsonl", [{"text": "Kar. 2", "copy": "sori", "type": "soreyi", "why": "clear"}])
        write(done, "unplaced.jsonl", [{"text": "Sh. 4", "source": "Index A", "reading": "pesto", "why": "lost"}])
        write(open_, "copy_only.jsonl", [dict(first[2], text="Kar. 9")])          # no final.jsonl: not checked yet
        rows = K.rows(root, root / "no_refs")
        # a reading that names no inscription stops the build: it would otherwise be left out without a word
        write(open_, "final.jsonl", [dict(final[2], text="Kar. 39 b")])
        try:
            K.rows(root, root / "no_refs")
        except ValueError as e:
            assert "'Kar. 39 b'" in str(e) and "final.jsonl" in str(e), e
        else:
            raise AssertionError("a reading of 'Kar. 39 b' was dropped without an error")
        # so does a reading that holds something tokens() would drop, such as a note in brackets
        write(open_, "final.jsonl", [dict(final[2], text="Kar. 9", reading="qo : se (copy blurred)")])
        try:
            K.rows(root, root / "no_refs")
        except ValueError as e:
            assert "Kar. 9" in str(e) and "(copy blurred)" in str(e) and "final.jsonl" in str(e), e
        else:
            raise AssertionError("a reading with a note in it was built without an error")
    assert [r["griffith_no"] for r in rows] == [2, 3, "Sh4"], rows                # Karanog first, Kar. 9 left out
    kar, kar3, sh = rows
    assert "signs changed" not in kar3["notes"] and "0 printed entries placed." in kar3["notes"]
    assert kar["rem"] == "0202" and sh["rem"] == "" and kar["site"] == "Karanog" and sh["site"] == "Shablul"
    assert kar["page"] == "p. 129 (leaf n144)" and kar["object"] == "Stela" and sh["object"] == "Altar"
    assert kar["text_std"] == "A: (1)wosi : so(2)reyi | B: ato mẖe"
    assert kar["text_corpus"] == "woSi Soreyi ato mXe" and kar["signs"] == 15 and kar["uncertain"] == 0
    assert "3 printed entries placed, 1 signs changed" in kar["notes"] and "sori (type: soreyi)" in kar["notes"]
    assert "formula A" in kar["notes"] and "before woman" in kar["notes"]
    assert sh["text_corpus"] == "qo .s" and sh["signs"] == 3 and sh["uncertain"] == 1
    assert "pesto (Index A)" in sh["notes"]
    assert all(K.ACCURACY in r["notes"] for r in rows)                          # the measured accuracy, in each row


def test_an_inscription_read_twice_takes_the_settled_reading():
    obj = lambda text, reading, **more: dict({"text": text, "part": "", "page": "leaf_144", "caption": f"{text}. Stela", "labels": [],
                                              "reading": reading}, **more)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, second = root / "readings/C01", root / "second/S144"
        pack.mkdir(parents=True)
        second.mkdir(parents=True)
        write(pack, "copy_only.jsonl", [obj("Kar. 2", "wosi : kore"), obj("Kar. 3", "ato mḫe")])
        write(pack, "final.jsonl", [obj("Kar. 2", "wosi : qore", entries=2, check_notes="names table"),
                                    obj("Kar. 3", "ato mẖe", entries=1, check_notes="")])
        # the second reader's own reading is not the row's: only what it settled is
        write(second, "final.jsonl", [obj("Kar. 2", "wosi : qere", entries=2, check_notes="")])
        once = K.rows(root / "readings", root / "no_refs", root / "second")
        write(second, "settled.jsonl", [obj("Kar. 2", "wosi : qere?", entries=2, check_notes="names table", settled_notes="the e is hatched")])
        write(second, "decisions.jsonl", [{"text": "Kar. 2", "first": "o", "second": "e", "chosen": "e?", "verdict": "second",
                                           "evidence": "copy", "why": "a hook"}])
        kar2, kar3 = K.rows(root / "readings", root / "no_refs", root / "second")
        # settled parts that are not the first reader's parts stop the build, and so does a note inside a settled reading
        for bad, word in ((obj("Kar. 2", "wosi", part="A"), "parts of Kar. 2"), (obj("Kar. 2", "wosi (blurred)"), "(blurred)")):
            write(second, "settled.jsonl", [bad])
            try:
                K.rows(root / "readings", root / "no_refs", root / "second")
            except ValueError as e:
                assert word in str(e) and "settled.jsonl" in str(e), e
            else:
                raise AssertionError(f"a settled file with {word} was built without an error")
    assert [r["text_std"] for r in once] == ["wosi : qore", "ato mẖe"] and "second time" not in once[0]["notes"]
    assert kar2["text_std"] == "wosi : qere?" and kar2["text_corpus"] == "woSi qere" and kar2["uncertain"] == 1
    # the note still counts the first reader's own check (k to q), then says what the second reading changed (o to e)
    assert "2 printed entries placed, 1 signs changed by the check." in kar2["notes"]
    assert ("(second_reading/S144): the two checked readings differed at 1 places" in kar2["notes"]
            and "0 for the first reading, 1 for the second, 0 for neither and 0 left open; 1 signs of the first reader's row changed."
            in kar2["notes"]), kar2["notes"]
    assert "names table" in kar2["notes"] and "the e is hatched" in kar2["notes"]
    assert kar3 == once[1] and "second time" not in kar3["notes"]               # read once: as before


def test_two_readers_are_compared_sign_by_sign():
    C = compare_readers
    assert C.distance(list("wosi"), list("wosi")) == 0 and C.distance(list("wosi"), list("wesiy")) == 2
    assert C.distance([], list("ab")) == 2 and C.distance(["te", "l"], ["t", "e", "l"]) == 2
    # lost signs are counted apart: each reader estimates a hatched stretch in its own way
    assert C.read(["wo[.][.]si", "(2)ato : m[.]"]) == (["w", "o", "s", "i", "a", "to", "m"], 3)
    obj = lambda text, reading, part="": {"text": text, "part": part, "reading": reading}
    first = {("Kar", 2): ["wosi : qore", "ato m[.]e"], ("Sh", 4): ["pesto"]}
    with tempfile.TemporaryDirectory() as tmp:
        second = Path(tmp)
        (second / "S144").mkdir()
        (second / "S190").mkdir()
        (second / "pick.json").write_text(json.dumps({"damaged": ["144"], "random": ["190"], "control": []}))
        write(second / "S144", "final.jsonl", [obj("Kar. 2", "wosi : (2)qere", "A"), obj("Kar. 2", "ato? m[.][.]ḫe", "B")])
        write(second / "S190", "final.jsonl", [obj("Sh. 4", "pesto")])
        rows = C.compare("final.jsonl", first, second)
        diff = C.differences(first, second)
        assert C.groups(second) == {"S144": "damaged", "S190": "random"}
        write(second / "S190", "final.jsonl", [obj("Sh. 5", "pesto")])           # a text nobody read first
        try:
            C.compare("final.jsonl", first, second)
        except ValueError as e:
            assert "('Sh', 5) has no first reading" in str(e), e
        else:
            raise AssertionError("a second reading of a text with no first reading was compared")
    # Kar. 2: 12 signs of the first reading (8 and 4; to is one sign); o read e, and a ḫ that only the second reader has,
    # are 2 apart; a query mark, a line number and a part's letter are no difference; lost signs 1 and 2
    assert rows == [("S144", ("Kar", 2), 12, 2, 1, 2), ("S190", ("Sh", 4), 4, 0, 0, 0)], rows
    assert diff == [{"pack": "S144", "text": "Kar. 2", "first": "o", "second": "e", "before": "wosiq", "after": "reatome"},
                    {"pack": "S144", "text": "Kar. 2", "first": "", "second": "ḫ", "before": "oreatom", "after": "e"}], diff


def named(refs):
    return [(site, n, part, cf, flag) for site, n, part, cf, line, flag in R.parse_refs(refs)]


def test_formula_words_are_divided_as_griffith_divides_them():
    entry = lambda source, reading, **kw: dict({"source": source, "reading": reading, "compare_only": False}, **kw)
    entries = [entry("formula A (table)", "ato m(?)ẖe : psoẖekete"),           # his query and the divider are no signs
               entry("formula B (table)", "at mẖe psiḫr"),
               entry("formula C (table)", "pisi plete"), entry("Index C", "pisiplete"),   # a gap in the type, not a word end
               entry("formula E (table)", "ḫ[rp]ḫ dole"),                        # a restoration: no pair from this entry
               entry("formula A (table)", "ab cd"),                              # four signs together: too short
               entry("Index A", "pesto l akiñtelowi"),                           # an index sets endings apart: not used
               entry("formula B (table)", "nsedokel dole", compare_only=True)]
    w = lambda *words: [tuple(K.tokens(x)) for x in words]
    pairs = K.phrases(entries)
    assert pairs == [tuple(w("ato", "mẖe")), tuple(w("mẖe", "psoẖekete")), tuple(w("at", "mẖe")), tuple(w("mẖe", "psiḫr"))], pairs
    show = lambda ws: " ".join("".join(x) for x in ws)
    part = lambda text: (show(K.divided(K.words_of(text), pairs)[0]), K.divided(K.words_of(text), pairs)[1])
    assert part("atomẖe psoẖekete") == ("ato mẖe psoẖekete", 1)
    assert part("atomẖepsoẖekete atmẖe") == ("ato mẖe psoẖekete at mẖe", 3)
    assert part("psoẖatmẖe") == ("psoẖ at mẖe", 2)                               # cut before the first word too
    assert part("atmẖepsiḫrkte") == ("at mẖe psiḫrkte", 2)                       # but not after the second
    assert part("ato mẖe pisiplete pestol") == ("ato mẖe pisiplete pestol", 0)   # already parted, or no pair
    assert part("at[.]mẖe") == ("at.mẖe", 0)                                     # a lost sign between: not the pair


def test_the_title_read_two_ways_is_spelled_one_way():
    words = [K.tokens(x) for x in ("slms", "slmsleb", "slẖs", "islms", "slm")]
    out, n = K.one_spelling(words)
    assert (["".join(x) for x in out], n) == (["slẖs", "slẖsleb", "slẖs", "islms", "slm"], 2)
    assert K.spell(out[:2]) == "SlXS SlXSleb"


def test_rows_part_formula_words_and_leave_the_reading_alone():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "C01").mkdir()
        (root / "refs").mkdir()
        obj = lambda n, reading: {"text": f"Kar. {n}", "part": "", "page": "leaf_144", "caption": f"Kar. {n}. Altar", "labels": [],
                                  "reading": reading, "entries": 1, "check_notes": ""}
        final = [obj(1, "wosi : slms : atomẖe : psoẖte"), obj(2, "wosi : atmẖe")]
        write(root / "C01", "copy_only.jsonl", final)
        write(root / "C01", "final.jsonl", final)
        write(root / "refs", "Kar_001.jsonl", [{"source": "formula A (table)", "reading": "ato mẖe psoẖte", "compare_only": False}])
        one, two = K.rows(root, root / "refs")
        old = K.EVERYWHERE
        K.EVERYWHERE = 1                      # a pair printed apart for one inscription is parted in every row
        try:
            everywhere = K.rows(root, root / "refs")[1]
        finally:
            K.EVERYWHERE = old
    assert one["text_std"] == "wosi : slms : atomẖe : psoẖte" and one["text_corpus"] == "woSi SlXS ato mXe pSoXte"
    assert "1 word boundary is Griffith's, from his formula tables and 1 word read slms is written slẖs" in one["notes"]
    assert two["text_corpus"] == "woSi atmXe" and "text_corpus differs" not in two["notes"]     # no entry of its own
    assert everywhere["text_corpus"] == "woSi atmXe"                                             # (at, mẖe) is no pair of Kar. 1


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
    # a footnote mark is not part of the number (Index A, womnitẖ)
    assert named("title of C, Kar. 72, 75¹") == [("Kar", 72, "", False, ""), ("Kar", 75, "", False, "")]
    assert named("Sh. 5 ♂ ¹") == [("Sh", 5, "", False, "")]
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
        index = lambda reading, refs: {"page": "ref_pdf111", "kind": "index", "index": "A", "reading": reading, "supplied": "",
                                       "refs": refs, "gloss": "", "notes": ""}
        # "ib." is the inscription the entry above names (Index C: tewide n. BB. Kar. 111, tewideqowi n. A. ib.)
        write(refs / "typed/I1", "ref_pdf111.jsonl", [index("ant : boqḫw", "Kar. 47 ♂, cf. 121"), index("aqel", "Kar. graff. 22"),
                                                      index("aqelowi", "ib."), index("tewide", "Kar. 111"), index("tewideqowi", "ib.")])
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
    assert got[("Kar", 111)] == [("Index A", "tewide", False), ("Index A", "tewideqowi", False)]
    assert ("formula A (table)", "ato mẖe", False) in got[("Kar", 1)]
    assert ("Kar", 133) not in per and ("Sh", 0) not in per
    assert sorted(o.get("text") or o["reading"] for o in none) == ["Inscr. 137", "Kar. 133", "Sh. 0", "aqel", "aqelowi"]
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
    assert (len(rows), sum(r["signs"] for r in rows), words) == (151, 16440, 2915)
    objs = R.typed()
    per, _ = R.tables(objs)
    assert (len(objs), sum(o["typist"] == "QA" for o in objs), len(per), sum(map(len, per.values()))) == (2722, 4, 152, 3550)
    assert min(map(len, per.values())) >= 2
    packs = [p for p in sorted(READINGS.iterdir()) if p.is_dir()]
    first = [o for p in packs for o in K.load(p, "copy_only.jsonl")]
    final = [o for p in packs for o in K.load(p, "final.jsonl")]
    count = lambda name: sum(len(K.load(p, name)) for p in packs)
    assert (sum(len(K.signs(o["reading"])) for o in first), sum(K.changed(a["reading"], b["reading"]) for a, b in zip(first, final)),
            sum(o["entries"] for o in final), count("kept_against_type.jsonl"), count("ref_corrections.jsonl"),
            count("unplaced.jsonl")) == (16759, 2405, 3468, 230, 66, 84)
    # the measured accuracy, by the first test's measure (signs right = FHN's signs less the edit distance)
    toks, align, fhn = score_fhn.first_test(ROOT)
    total = lambda name: tuple(map(sum, zip(*[r[:2] for r in score_fhn.score(
        toks, align, fhn, score_fhn.readings([READINGS / p / name for p in ("C09", "C14", "C21")])).values()])))
    assert total("final.jsonl") == (654, 639) and total("copy_only.jsonl") == (654, 582)
    assert "639 of 654 signs right (97.7%)" in K.ACCURACY and "582 (89.0%)" in K.ACCURACY


def test_reported_pack_table():
    # data/expansion/karanog/README.md, section 4: one row a pack, as the readers' files give it, and the total
    table = {}
    for line in (K.KAR / "README.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 7 and re.fullmatch(r"[CP]\d\d|All", cells[0]):
            table[cells[0]] = cells[1:]
    span = lambda site, ns: f"{site}. {ns[0]}" + (f", {ns[1]}" if len(ns) == 2 else f" to {ns[-1]}" if ns[1:] else "")
    num = lambda cell: int(cell.split()[0].replace(",", ""))
    total = [0] * 5
    for p in sorted(p for p in READINGS.iterdir() if p.is_dir()):
        first, final = K.load(p, "copy_only.jsonl"), K.load(p, "final.jsonl")
        texts = sorted({K.number(o["text"]) for o in final}, key=lambda t: (t[0] != "Kar", t[1]))
        sites = {s: [n for t, n in texts if t == s] for s in ("Kar", "Sh")}
        assert all(ns == list(range(ns[0], ns[-1] + 1)) for ns in sites.values() if ns), p.name
        got = [sum(len(K.signs(o["reading"])) for o in first), sum(K.changed(a["reading"], b["reading"]) for a, b in zip(first, final)),
               sum(o["entries"] for o in final), len(K.load(p, "kept_against_type.jsonl")), len(K.load(p, "ref_corrections.jsonl"))]
        row = table.pop(p.name)
        assert (row[0], [num(c) for c in row[1:]]) == (", ".join(span(s, ns) for s, ns in sites.items() if ns), got), p.name
        total = [t + g for t, g in zip(total, got)]
    row = table.pop("All")
    assert [num(c) for c in row] == [len(K.rows())] + total and f"({total[1] / total[0]:.1%})" in row[2], row
    assert not table, table                                                      # no row for a pack that is not there


def test_karanog_rows_are_new_to_the_corpus():
    # README, section 1: by src/expand.py's test all 151 are new to corpus_v2 and the other Griffith files
    # (corpus_v3), and corpus_v5 has the size the README and NEXT_STEPS.md give. Without the formulae left out
    # (own_letters) the test takes three short texts for copies of older ones, as it did until 2026-11-10.
    needs("data/corpus_v2.jsonl")
    import expand
    v3 = lines(ROOT / "data/corpus_v2.jsonl")
    v3 += expand.merge(v3, expand.load_griffith())[0]
    karanog = expand.load_griffith("data/expansion/karanog")
    added, dupes, partial = expand.merge(v3, karanog, among=False, own_letters=True)
    assert len(added) == 151 and not dupes and not partial, dupes
    tok = lambda rows: sum(len(r["text"].split()) for r in rows)
    assert (len(v3), tok(v3)) == (748, 19066) and (len(v3) + len(added), tok(v3) + tok(added)) == (899, 21981)
    assert [g["id"] for g, _ in expand.merge(v3, karanog, among=False)[1]] == ["G-karanog-63", "G-karanog-66", "G-karanog-Sh17"]


def test_reported_second_reading_numbers():
    # data/expansion/karanog/README.md, section 6: eleven pages read by two readers
    C = compare_readers
    group = C.groups()
    assert sorted(group) == sorted(p.name for p in C.SECOND.iterdir() if p.is_dir()) and len(group) == 11
    assert [sum(g == k for g in group.values()) for k in ("damaged", "random", "control")] == [7, 3, 1]

    def totals(name):
        out = {}
        for pack, _, n, d, _, _ in C.compare(name):
            for g in (group[pack], "all"):
                right, signs = out.get(g, (0, 0))
                out[g] = (right + n - d, signs + n)
        return out
    assert totals("copy_only.jsonl") == {"damaged": (1708, 2036), "random": (823, 926), "control": (226, 244), "all": (2757, 3206)}
    assert totals("final.jsonl") == {"damaged": (1999, 2061), "random": (939, 948), "control": (242, 245), "all": (3180, 3254)}
    rows = C.compare("final.jsonl")
    assert len(rows) == 31 and sum(d == 0 for _, _, _, d, _, _ in rows) == 10
    # the places where the two checked readings differ, and how the second reader settled them
    diff = C.differences()
    again = K.twice(C.SECOND)
    decided = [d for _, _, ds in again.values() for d in ds]
    assert len(diff) == len(decided) == 56 and len(again) == 31 and len({d["text"] for d in diff}) == 21
    assert [sum(d["verdict"] == v for d in decided) for v in ("first", "second", "other", "open")] == [26, 17, 2, 11]
    assert [sum(d["evidence"] == e for d in decided) for e in ("copy", "type", "both")] == [25, 6, 25]
    by_group = lambda g: [sum(d["verdict"] == v for pack, _, ds in again.values() if group[pack] == g for d in ds)
                          for v in ("first", "second", "other", "open")]
    assert (by_group("damaged"), by_group("random"), by_group("control")) == ([19, 16, 2, 8], [5, 1, 0, 3], [2, 0, 0, 0])
    # what settling changed in the first reader's rows, by the measure of the comparison
    first, settled = C.first_readings("final.jsonl"), {n: [o["reading"] for o in objs] for n, (_, objs, _) in again.items()}
    assert sum(C.distance(C.read(first[n])[0], C.read(parts)[0]) for n, parts in settled.items()) == 26
    assert sum(len(C.read(first[n])[0]) for n in settled) == 3254
    # the control, Kar. 77, against FHN: first reader, second reader, settled reading
    toks, align, fhn = score_fhn.first_test(ROOT)
    score = lambda path: score_fhn.score(toks, align, fhn, score_fhn.readings([path]))["0277"][:2]
    assert [score(p) for p in (READINGS / "C14/final.jsonl", C.SECOND / "S171/final.jsonl", C.SECOND / "S171/settled.jsonl")] \
        == [(134, 128), (134, 127), (134, 128)]


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
    assert toks(score_fhn.clean("ted(sic)lowi")) == ["te", "d", "l", "o", "w", "i"]         # Griffith's sic
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
