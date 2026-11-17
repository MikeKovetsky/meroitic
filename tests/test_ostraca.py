"""Checks for Griffith's ostraca of Meroitic Studies V as open readings (src/ostraca.py).

  python3 -I tests/test_ostraca.py

The source text, the rows and the figures are public (Griffith's article is in the public domain); the blind second
typing and the map are local, so the checks that recompute from them are skipped where they are absent.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src" / "v6"), str(ROOT / "src" / "experts"), str(ROOT / "src"), str(ROOT / "tests")]

import ostraca as O     # noqa: E402
import expand as E      # noqa: E402
import readings as R    # noqa: E402
import build as B       # noqa: E402
import recount as V     # noqa: E402
from local_only import needs, run   # noqa: E402

D = "̣"


def rows_file():
    return [json.loads(l) for l in O.ROW.read_text(encoding="utf-8").splitlines() if l.strip()]


# --- the spelling ---
def test_signs_of_1925_in_the_corpus_spelling():
    cases = {"qê": "qo", "šmeñtêñ": "SmeNtoN", "azḫblês": "adxblos", "mẖzi": "mXdi", "trêzes-lw": "trodeslw",
             "arb[te]": "arbte", "(y)eqêqebli-šê": "yeqoqebliSo", "ṃlḫl": "mlxl", "*artepê": "artepo",
             "q" + D + "êrli-šê": "qorliSo", "ḫ" + D + "mṛkeli": "xmrkeli", "6·3": "6 3", "·4½": "4", "15·5½": "15 5",
             "·ḷ": "1", "40": "40", "a.ṭ..ḳ": "a.t..k"}
    for printed, corpus in cases.items():
        assert O.to_corpus(printed) == corpus, printed
    assert O.to_corpus("mhzi") == "mhdi"                   # a plain h is no letter of the corpus: a dropped mark shows


def test_signs_counted_as_signs():
    assert O.signs("qê li keñ") == ["q", "ê", "l", "i", "k", "e", "ñ"]
    assert O.signs("arbte 2·6") == ["a", "r", "b", "te"]                  # te one sign, numerals no signs
    assert O.signs("ṭ" + D + "ê ⍋ *ḫ") == ["tê", "ḫ"]                     # tê one sign, the dot and symbol go


# --- reading his print ---
def test_tokens_lines_and_full_stops():
    assert O.tokens("(1) ab : cd. (2) ef 2·6.") == [(1, "ab"), (1, "cd"), (2, "ef"), (2, "2·6")]
    assert O.tokens("tkiñ-lw ·9 ·2 (sic).") == [(1, "tkiñ-lw"), (1, "·9"), (1, "·2")]
    assert O.tokens("a..r. qe") == [(1, "a..r."), (1, "qe")]              # a lost sign mid-text is not a full stop
    assert O.tokens("te 40(?) ·9 ....") == [(1, "te"), (1, "40"), (1, "(?)"), (1, "·9"), (1, "....")]


def test_words_kinds_and_doubts():
    ws = O.words("(1) qê li ⍋ 1" + D + "·3 *ḫ (2) ... ṃe // l // ·4½ ab(?)")
    assert [(w["corpus"], w["kind"]) for w in ws] == [
        ("qo", "word"), ("li", "word"), ("1", "numeral"), ("3", "numeral"), ("x", "word"), ("...", "lost"),
        ("me", "word"), ("...", "lost"), ("l", "word"), ("...", "lost"), ("4", "numeral"), ("ab", "word")]
    assert [w["line"] for w in ws][:5] == [1] * 5 and ws[5]["line"] == 2
    doubt = [(w["corpus"], w["doubt"]) for w in ws if w["doubt"]]
    assert doubt == [("1", "dot below a sign"), ("3", "dot below a sign"), ("me", "dot below a sign"),
                     ("ab", "(?) after it")]


def test_a_note_on_a_mark_the_corpus_leaves_out_stands_on_its_line():
    t = {"no": "B.O. 1", "printed": "(1) mrê : qe 74·8. (2) a..r. tepe[re]t 16·6 ⍋ ...... 1·5."}
    got = [(d["line"], d["word"]) for d in O.doubts(t, O.words(t["printed"]))]
    assert got == [(1, "qe"), (2, "⍋"), (1, "mrê")]
    try:
        O.doubts({"no": "B.O. 1", "printed": "(1) mrê : qe 74·8."}, O.words("(1) mrê : qe 74·8."))
    except SystemExit as e:
        assert "⍋" in str(e)                               # a note whose mark is not in the text stops the build
    else:
        raise AssertionError("a note on a mark that is not in the text passed")


# --- the files ---
def test_rows_are_written_from_the_source():
    assert rows_file() == O.rows()


def test_the_rows_hold_the_texts():
    rs = rows_file()
    nos = [r["number"] for r in rs]
    assert len(rs) == 46 and len(set(nos)) == 46 and "F.O. 38" not in nos
    assert nos == [f"F.O. {n}" for n in range(1, 41) if n != 38] + [f"B.O. {n}" for n in range(1, 7)] + ["D.O. 1"]
    for r in rs:
        assert r["griffith_no"] is None and r["rem"] == "" and r["object"].startswith("ostracon")
        assert r["site"].startswith(("Faras", "Buhen", "Dakkah")) and r["source"] == O.WORK
        for w in r["text_corpus"].split():
            assert re.fullmatch(r"\d+|[.]+|[abdeiklmnopqrstwxySNX.]+", w), (r["number"], w)
        assert " ".join(r["lines"][k] for k in sorted(r["lines"], key=int)) == r["text_corpus"]
        assert r["words"] == sum(1 for w in r["text_corpus"].split() if re.search(r"[A-Za-z]", w))
        assert r["numerals"] == sum(1 for w in r["text_corpus"].split() if w.isdigit())
    assert sum(r["words"] for r in rs) == 275 and sum(r["signs"] for r in rs) == 959
    listed = {(r["number"], d["word"]) for r in rs for d in r["doubts"]}
    assert {(n, w) for n, w, _ in O.NOTES + O.COPIES + O.OURS if w != "·"} <= listed
    whys = {(r["number"], d["word"]): d["why"] for r in rs for d in r["doubts"]}
    assert all(whys[(n, w)] == why for n, w, why in O.COPIES)                   # where his copy differs, said


def test_the_corpus_reads_them_as_open_readings():
    rows = [r for r in R.griffith_rows("data/expansion/jea", "griffith") if "jea11" in r["key"]]
    assert len(rows) == 46
    g = R.finish(next(r for r in rows if r["number"] == "F.O. 1 (JEA 11, 1925)"))
    assert g["key"] == "griffith:G-jea11-F.O. 1" and g["numbers"] == {"article": ["F.O. 1"]} and g["v5"] is None
    assert g["open"] and g["typed"] and g["whole"]
    assert B.name_of([g]) == "F.O. 1" and "article" in B.SYSTEMS
    jea4 = R.finish(next(r for r in R.griffith_rows("data/expansion/jea", "griffith") if "jea4" in r["key"]))
    assert jea4["numbers"] == {"rem": ["1003"]}                          # a text with a REM number keeps it


def test_corpus_v5_does_not_take_them():
    assert not any(r["id"].startswith("G-jea") for r in E.load_griffith())


def test_the_map_is_drawn_on_its_own_texts():
    texts = V.map_texts()
    assert len(texts) == 548 and not any(t.startswith(("F.O.", "B.O.", "D.O.")) for t in texts)
    rows = [{"id": "REM 0001", "reading": "mnl:x", "text": "a", "names": [], "v5": None},
            {"id": "F.O. 1", "reading": "griffith:x", "text": "b", "names": [], "v5": None}]
    assert [r["id"] for r in V.rows_for_map(rows)] == ["REM 0001"]
    assert [r["id"] for r in V.rows_for_map(rows, texts={"REM 0001", "F.O. 1"})] == ["REM 0001", "F.O. 1"]


# --- the second typing and the figures ---
def test_blind_counts_signs():
    first = {n: "qê li keñ" for n in O.LOT}
    second = dict(first, **{O.LOT[0]: "qê li ke"})
    b = O.blind(first, second)
    assert b["signs_first"] == 7 * len(O.LOT) and b["agree"] == b["signs_first"] - 1
    assert b["share"] == round((b["agree"]) / b["signs_first"], 4) and b["met"] == (b["share"] >= O.BAR)


def test_published_figures():
    figs = json.loads(O.FIGURES.read_text(encoding="utf-8"))
    assert {k: v for k, v in figs.items() if k in O.figures()} == O.figures()
    s = figs["second_typing"]
    assert s["lot"] == list(O.LOT) and s["met"] and s["agree"] == s["signs_first"] == s["signs_second"]
    m = figs["map"]
    assert m["now_in_a_second_text"] == len(m["which"]) and m["spellings"] == sum(m["on_the_map"].values())


def test_the_copy_check_counts():
    import tempfile
    rows = [{"text": "F.O. 1", "word": "atr", "verdict": "differs"}, {"text": "F.O. 1", "word": "ab", "verdict": "same"},
            {"text": "F.O. 6", "word": "qê", "verdict": "cannot tell"},
            {"text": "F.O. 1", "dividers_copy": 10, "dividers_typed": 10, "detail": "same total, different places: x"},
            {"text": "F.O. 6", "dividers_copy": 0, "dividers_typed": 0}, {"text": "D.O. 1", "dividers_copy": 7, "dividers_typed": 6}]
    with tempfile.TemporaryDirectory() as d:
        path = pathlib.Path(d) / "check.jsonl"
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        c = O.copy_check(path)
    assert c["texts"] == 2 and c["words"] == 3 and c["by_verdict"] == {"cannot tell": 1, "differs": 1, "same": 1}
    assert c["differs"] == [["F.O. 1", "atr"]] and c["dividers_differ"] == ["D.O. 1", "F.O. 1"]
    assert O.copy_check(pathlib.Path("/nonexistent/check.jsonl")) is None
    figs = json.loads(O.FIGURES.read_text(encoding="utf-8"))
    assert set(map(tuple, figs["copy_check"]["differs"])) <= {(n, w) for n, w, _ in O.COPIES}    # each one said


def test_published_figures_recomputed():
    needs("data/sources/ostraca/blind/second_typing.txt", "data/sources/v6/analysts/glosses.jsonl")
    figs = json.loads(O.FIGURES.read_text(encoding="utf-8"))
    assert figs["second_typing"] == O.blind() and figs["map"] == O.recurrence()
    needs("data/sources/ostraca/copies/check.jsonl")
    assert figs["copy_check"] == O.copy_check()


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)])
