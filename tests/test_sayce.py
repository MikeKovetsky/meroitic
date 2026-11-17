"""Checks for Sayce's reading of REM 1003 and its comparison with Griffith's (src/sayce.py).

  python3 -I tests/test_sayce.py

Sayce's text and the counts are public; the closed readings and the blind second typing are local, so the checks
that recompute from them are skipped where they are absent.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src" / "v6"), str(ROOT / "src" / "experts"), str(ROOT / "src"), str(ROOT / "tests")]

import sayce as S       # noqa: E402
import akinidad as A    # noqa: E402
from local_only import needs, run   # noqa: E402


# --- his letters ---
def test_his_units_as_griffiths_signs():
    assert S.split("toh") == ["te"] and S.split("rhe") == ["z"] and S.split("th") == ["t"] and S.split("t") == ["tê"]
    assert S.split("pi") == ["p", "i"] and S.split("ka") == ["q", "a"] and S.split("sh") == ["š"]
    assert S.units("k'-r-e-y-i") == [("k", False), ("'", False), ("r", False), ("e", False), ("y", False),
                                     ("i", False)]
    assert S.units("y-e-th-g-b(?)-ḥ-e")[4] == ("b", True)                       # his (?) doubts the sign before it
    assert [u for u, x in S.units("[ḥ-r-]p-ḥ-e") if x] == ["ḥ", "r"]           # restored, then his own p
    assert S.units("a-...-m") == [("a", False), (".", True), (".", True), (".", True), ("m", False)]


def test_tidy_closes_the_spaces_inside_a_word():
    assert S.tidy("y-e-th-g-b (?)-ḥ-e : Y") == "y-e-th-g-b(?)-ḥ-e : Y"
    assert S.tidy("[ḥ-r-] p-ḥ-e-g-e :") == "[ḥ-r-]p-ḥ-e-g-e :"
    assert S.tidy("B-e-u-[i-] g-[e :] sh") == "B-e-u-[i-]g-[e] : sh"
    assert S.tidy("a- . . . m (?)-rh-e") == "a-...-m(?)-rh-e"


def test_words_lines_numerals_and_doubts():
    ws = S.words([(1, "k'-r : A-g-i-"), (2, "n-i-rhe-rhe : a-b-r XII : t-l (?) . . ."), (3, "e-m'-k-e")])
    assert [(w["line"], w["corpus"], w["kind"]) for w in ws] == [
        (1, "qor", "word"), (1, "akinidd", "word"), (2, "abr", "word"), (2, "XII", "numeral"), (2, "tol", "word"),
        (2, ".", "lost"), (2, ".", "lost"), (2, ".", "lost"), (3, "emoqe", "word")]
    assert ws[4]["doubt"] == "(?) after it" and not ws[0]["doubt"]
    assert S.roman("CCLII") == 252 and S.roman("MMMCCCC") == 3400 and S.roman("CXV") == 115


def test_doubted_words_are_classed_as_the_page_fixes():
    """The classes of data/discovery/ostraca_sayce.md: a sign or numeral he queries, also where a space parts it
    from his "(?)", and a place he prints as lost are "also unsure"; letters he has inside the place count."""
    g = lambda printed, doubt="?": {"line": 1, "printed": printed, "griffith": printed, "corpus": printed,
                                    "doubt": doubt}
    gw = [g("qor"), g("58"), g("wi", ""), g("pet"), g("ye", ""), g("abde"), g("lmn"), g("sb")]
    sw = S.words([(1, "k'-r : L (?) V : u-i : . . . : y-e : a-b-th-rh-e : l-m-n (?) : s-b")])
    assert sw[1]["kind"] == "numeral" and sw[1]["doubt"] and sw[-2]["signs"][-1] == ("n", True)
    closed = {"k": "qor 58 wi pet ye abde lmn sb"}
    got = {d["griffith"]: (d["sayce"], d["class"], d["k"]) for d in S.doubted(gw, sw, closed)}
    assert got == {"qor": ("qor", "confirms", "both"), "58": ("505", "also unsure", "Griffith"),
                   "pet": ("###", "also unsure", "Griffith"),            # where he has no letter he has no say
                   "abde": ("abtde", "reads otherwise", "Griffith"), "lmn": ("lmn", "also unsure", "both"),
                   "sb": ("sb", "confirms", "both")}, got


# --- the files ---
def test_the_whole_text_is_typed():
    ws = S.words()
    assert sorted({w["line"] for w in ws}) == list(range(1, 43))
    assert all(w["corpus"].replace(".", "") == "" or all(c in "abdeiklmnopqrstwxySNX." for c in w["corpus"])
               for w in ws if w["kind"] == "word")
    assert not any("?" in s for w in ws if w["kind"] == "word" for s, _ in w["signs"])   # every unit has a value
    saved = json.loads(S.WORDS.read_text(encoding="utf-8"))
    assert saved == [{k: w[k] for k in ("line", "printed", "griffith", "corpus", "doubt", "kind")} for w in ws]


def test_published_comparison():
    figs = json.loads(S.COMPARISON.read_text(encoding="utf-8"))
    again = S.figures(closed=None)
    assert {k: v for k, v in figs.items() if k in again and k != "second_typing"} == \
        {k: v for k, v in again.items() if k != "second_typing"}
    d = figs["doubted"]
    assert d["words"] == 38 == sum(d["by_class"].values()) == len(d["places"])
    assert set(d["by_class"]) <= {"confirms", "reads otherwise", "also unsure", "not found"}
    for key, v in figs.get("against_closed", {}).items():
        assert key in A.CLOSED and sum(v["doubted_sides_with"].values()) == 38
        assert v["share"] == round(v["agree"] / v["sayce_words"], 3)
    strings = lambda x: [x] if isinstance(x, str) else [s for v in (x.values() if isinstance(x, dict) else x)
                                                           for s in strings(v)] if isinstance(x, (dict, list)) else []
    assert all(len(s) < 400 for s in strings(figs.get("against_closed", {})))           # counts, no closed text


def test_published_comparison_recomputed():
    needs("data/sources/v6/inscriptions.jsonl", "data/sources/sayce/blind/second_typing.txt")
    figs = json.loads(S.COMPARISON.read_text(encoding="utf-8"))
    assert S.figures(closed=A.closed_readings()) == figs


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)])
