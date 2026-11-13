"""Checks for the open reading of REM 1003 from Griffith 1917 (src/akinidad.py).

  python3 -I tests/test_akinidad.py

The source text and the row are public; the closed readings it is compared with are local only, so the checks of
the comparison itself run on made-up texts, and the one that recomputes the published counts is skipped where the
v6 build is absent.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src" / "v6"), str(ROOT / "src" / "experts"), str(ROOT / "src"), str(ROOT / "tests")]

import akinidad as A    # noqa: E402
import expand as E      # noqa: E402
import readings as R    # noqa: E402
from local_only import needs, run   # noqa: E402


def row_file():
    lines = [l for l in A.ROW.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) == 1
    return json.loads(lines[0])


# --- the spelling ---
def test_signs_of_1917_in_the_corpus_spelling():
    cases = {"qêre-yi": "qoreyi", "peštê-ñyi": "peStoNyi", "kzweli": "kdweli", "yitnizebḫel": "yitnidebxel",
             "Nptbiẖ": "nptbiX", "Qeš": "qeS", "abrsl": "abrsl", "Amnirens": "amnirens", "ašr": "aSr",
             "mhrlêsñ": "mXrlosN", "1·2": "1 2", "1032.": "1032.", "q(ê)leb": "qoleb", "šwizê": "Swido", "qer[l]islw": "qerlislw"}
    for printed, corpus in cases.items():
        assert A.to_corpus(A.plain(printed)) == corpus, printed


def test_signs_counted_as_signs():
    assert len(A.SIGN.findall("peštê")) == 4           # p e š tê: tê is one sign
    assert len(A.SIGN.findall("ates")) == 3            # a te s


# --- reading his print ---
SECS = [(1, "(l. 1) Ab : qê-ri : Mn(l. 2)ê : x? : ... : yb (?) : [sb ? :] zz"),
        (2, "(?)..kw : wi 1·2 (l. 3) teñ- kelhe :")]


def test_words_lines_and_doubts():
    ws = A.words(SECS)
    assert [w["corpus"] for w in ws] == ["ab", "qori", "mno", "x", "...", "yb", "sb", "dd", "..kw", "wi", "1", "2",
                                         "teNkelXe"]
    assert [w["line"] for w in ws] == [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3]     # a word is of the line it starts on
    doubt = {w["corpus"]: w["doubt"] for w in ws}
    assert doubt["x"] == "? above a sign" and doubt["yb"] == "? after the word" and doubt["sb"] == "? after the word"
    assert doubt["..kw"] == "(?) by the word" and not doubt["ab"] and not doubt["mno"]
    assert not A.counted(ws[4]) and A.counted(ws[10])                           # a lacuna is no word, a numeral is


def test_text_std_keeps_his_marks():
    assert A.text_std(SECS).startswith("(1) Ab : qê-ri : Mn(2)ê : x?")


# --- the comparison ---
def test_compare_ignores_word_division_and_spelling_folds():
    ws = A.words([(1, "(l. 1) qêreli : kzweli : (l. 2) abc : yekezi")])
    by_line, (la, ln), each = A.compare(ws, "qereli kdw eli xyz yeked i")       # made up: e for o, other divisions
    assert by_line == {1: (2, 2), 2: (1, 2)}
    assert [ok for _, ok in each] == [True, True, False, True]
    assert ln == len("qereli" + "kdweli" + "abc" + "yekedi") and la < ln
    strict = A.compare(ws, "qeroli kdweli abc yekedi", A.exact)[0]          # nothing folded: qore is not qero
    assert strict == {1: (1, 2), 2: (2, 2)}


# --- the files ---
def test_row_is_written_from_the_source():
    assert row_file() == A.row()                       # the row is current: src/akinidad.py writes it so


def test_row_holds_the_whole_text():
    r = row_file()
    ws = E.words(r["text_corpus"])
    assert r["words"] == len(ws) == 337
    assert sorted(map(int, r["lines"])) == list(range(1, 43))                   # every line of the stela, ll. 1-42
    assert " ".join(r["lines"][str(k)] for k in range(1, 43)) == r["text_corpus"]
    assert all(re.fullmatch(r"[a-zA-Z0-9.]+", w) for w in r["text_corpus"].split())
    assert not re.search(r"[A-Z]", re.sub(r"[SNX]", "", r["text_corpus"]))       # capitals only for S, N, X
    assert r["griffith_no"] is None and r["rem"] == "1003"
    assert int(r["uncertain"]) == len({(d["line"], d["word"]) for d in r["doubts"]
                                       if d["why"].startswith(("?", "(?)"))})
    assert {(d["word"], d["why"]) for d in r["doubts"]} >= {(p, why) for p, why in A.OURS}


def test_the_corpus_reads_it_as_an_open_reading_of_rem_1003():
    rows = R.griffith_rows("data/expansion/jea", "griffith")
    assert len(rows) == 1
    g = R.finish(rows[0])
    assert g["key"] == "griffith:G-jea4-1003" and g["numbers"] == {"rem": ["1003"]} and g["v5"] is None
    assert g["open"] and g["typed"] and g["whole"] and g["number"] == "JEA 4 (1917), §§ 1-21"
    assert R.GRIFFITH[-1] == ("data/expansion/jea", "griffith")


def test_corpus_v5_does_not_take_it():
    """src/expand.py reads data/expansion and not its sub-folders: corpus_v3 and corpus_v5 stay as they were."""
    assert not any(r["id"].startswith("G-jea") for r in E.load_griffith())


def test_published_comparison():
    figs = json.loads(A.COMPARISON.read_text())
    r = row_file()
    assert figs["griffith"]["words"] == r["words"] and figs["griffith"]["lines"] == 42
    assert set(figs["against"]) == set(A.CLOSED)
    for v in figs["against"].values():
        assert v["words"] == r["words"] == sum(x["words"] for x in v["by_line"].values())
        assert v["agree"] == sum(x["agree"] for x in v["by_line"].values())
        assert v["share"] == round(v["agree"] / v["words"], 3) and 0 < v["strict"]["agree"] <= v["words"]
    strings = lambda x: [x] if isinstance(x, str) else [s for v in (x.values() if isinstance(x, dict) else x)
                                                           for s in strings(v)] if isinstance(x, (dict, list)) else []
    assert strings(figs) == [figs["how"]]                                      # counts only, no closed text


def test_comparison_recomputed():
    needs("data/sources/v6/inscriptions.jsonl")
    assert A.figures(A.words(), A.closed_readings()) == json.loads(A.COMPARISON.read_text())


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)])
