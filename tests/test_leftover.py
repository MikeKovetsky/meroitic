"""Checks for the leftover parts and the meanings Millet and Lipinski state (src/leftover.py,
data/discovery/leftover_parts.md, leftover_parts_2.md for the second reading of part 1, and leftover_stems.md for
part 3, the leftover stems).

  python3 -I tests/test_leftover.py

The map, the lexicon, the sources and the agents' answers are local only: the checks of the method run on made-up
words; the checks of the reported numbers read the public figures file, compare the page with it, and compare it
with a count from the local files where those are present.
"""
import collections
import contextlib
import filecmp
import io
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import leftover as L                 # noqa: E402
import rare as R                     # noqa: E402
import recurring as W                # noqa: E402
import themap as M                   # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/leftover_parts.md"
PAGE_AGAIN = ROOT / "data/discovery/leftover_parts_2.md"
PAGE_STEMS = ROOT / "data/discovery/leftover_stems.md"
LEX = {"ato": {"kind": "noun", "status": "established"}, "kb": {"kind": "verb", "status": "hypothesis"},
       "Skl": {"kind": "place name", "status": "unknown"}}


def figs():
    return json.loads(L.PUBLIC.read_text(encoding="utf-8"))


def stems():
    return json.loads(L.PUBLIC_STEMS.read_text(encoding="utf-8"))


def page(path=PAGE):
    return " ".join(path.read_text(encoding="utf-8").split())


def stops(fn, part):
    try:
        fn()
    except SystemExit as e:
        assert part in str(e), e
        return True
    raise AssertionError("did not stop")


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


def a_reading(d, said):
    """A made-up reading of part 1 in folder d: 20 hidden endings, 20 runs of lot letters and the real places of
    `said` ({place: (checker 1's case, checker 2's case)} or with an entry: ("known", "ato")), one pack."""
    key = [{"place": f"E{i:02d}", "control": "ending", "answer": "ending"} for i in range(20)]
    key += [{"place": f"J{i:02d}", "control": "junk", "answer": "unknown", "front": True, "parts": [["zz", None], ["ato", "ato"]]} for i in range(20)]
    key += [{"place": q, "control": None, "run": "g2", "entry": "ato", "text": "T", "n": 1, "form": "atox"} for q in said]
    L.write("key.json", key, d)
    L.write("groups.json", [[p["place"] for p in key]], d)
    for c in (1, 2):
        (d / f"answers{c}").mkdir()
        lines = [{"place": p["place"], "case": p["answer"]} for p in key if p["control"]]
        for q, pair in said.items():
            a = pair[c - 1]
            lines.append({"place": q, "case": a[0], "entry": a[1]} if isinstance(a, tuple) else {"place": q, "case": a})
        (d / f"answers{c}" / "P01.jsonl").write_text("".join(json.dumps(l) + "\n" for l in lines), encoding="utf-8")


def with_lexicon(fn):
    old = W.lexicon
    W.lexicon = lambda: LEX
    try:
        return fn()
    finally:
        W.lexicon = old


# ------------------------------------------------------------------------------------------------- the method

def test_a_place_has_a_verdict_only_when_both_checkers_agree():
    said = {"Q1": ("ending", "ending"), "Q2": ("ending", "unknown"), "Q3": ("name", "name"), "Q4": (("known", "ato"), ("known", "ato")),
            "Q5": (("known", "ato"), ("known", "kb")), "Q6": (("known", "kb"), ("known", "kb")), "Q7": ("unknown", "unknown")}
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        a_reading(d, said)
        with_lexicon(lambda: quiet(L.count, d))
        res = L.read("result.json", d)
    got = {r["place"]: r["verdict"] for r in res["rows"]}
    assert got == {"Q1": "ending", "Q2": "not agreed", "Q3": "name", "Q4": "known", "Q5": "known, not the same sure entry",
                   "Q6": "known, not the same sure entry", "Q7": "unknown"}        # kb is no sure entry of the lexicon
    assert res["places"] == res["answered_by_both"] == 7 and all(res["bars"].values()) and res["taken"]
    assert res["by_run"] == {"g2": res["verdicts"], "g4": {}}


def test_one_explained_run_of_lot_letters_too_many_misses_the_bar():
    """Each checker may explain 2 of the 20 runs of lot letters, as an ending, a known word or a name; a third
    one, by either checker, misses the bar and nothing is taken. A hidden ending missed 7 times misses its bar."""
    def reading(change):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a_reading(d, {"Q1": ("ending", "ending"), "Q2": ("unknown", "unknown")})
            f = d / "answers1" / "P01.jsonl"
            lines = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines()]
            change(lines)
            f.write_text("".join(json.dumps(l) + "\n" for l in lines), encoding="utf-8")
            with_lexicon(lambda: quiet(L.count, d))
            return L.read("result.json", d)

    def explain(n, case="name", kind="J"):
        def change(lines):
            for l in [l for l in lines if l["place"].startswith(kind)][:n]:
                l["case"] = case
        return change
    assert reading(explain(2))["taken"] and reading(explain(2, "ending"))["bars"]["junk_explained"]
    for case in ("name", "ending", "known"):
        r = reading(explain(3, case))
        assert not r["bars"]["junk_explained"] and not r["taken"] and r["controls"]["1"]["junk"][f"called_{case}"] == 3, case
    assert reading(explain(3, "unclear"))["taken"]                              # unclear explains nothing
    assert reading(explain(6, "unknown", "E"))["taken"] and not reading(explain(7, "unknown", "E"))["bars"]["endings_called_ending"]
    r = reading(lambda lines: lines.pop())                                      # a place without one checker's answer
    assert not r["bars"]["every_place_answered_by_both"] and not r["taken"]
    assert L.BARS == {"kappa": 0.6, "junk_explained": 0.10, "endings_called_ending": 0.70} and L.CONTROLS == {"ending": 20, "junk": 20}


def test_the_second_reading_counts_only_endings_and_known_words_against_the_lot_letters():
    """The second reading has a bar for each verdict: a run of lot letters called a name misses none, since a name
    is not laid; a third run called an ending or a known word, by either checker, misses the bar."""
    def reading(change, again=True):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a_reading(d, {"Q1": ("ending", "ending"), "Q2": ("unknown", "unknown")})
            f = d / "answers2" / "P01.jsonl"
            lines = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines()]
            change(lines)
            f.write_text("".join(json.dumps(l) + "\n" for l in lines), encoding="utf-8")
            with_lexicon(lambda: quiet(L.count, d, again))
            return L.read("result.json", d)

    def call(*cases):
        def change(lines):
            for l, case in zip([l for l in lines if l["place"].startswith("J")], cases):
                l["case"] = case
        return change
    r = reading(call(*["name"] * 20))                                           # every run called a name: no bar rests on it
    assert r["taken"] and set(r["bars"]) == {"every_place_answered_by_both", "kappa", "junk_called_ending_or_known", "endings_called_ending"}
    assert not reading(call(*["name"] * 20), again=False)["taken"]              # the first reading's bar counts a name
    assert reading(call("ending", "known", "name", "name"))["taken"]
    for cases in (("ending",) * 3, ("known",) * 3, ("ending", "known", "ending")):
        r = reading(call(*cases))
        assert not r["bars"]["junk_called_ending_or_known"] and not r["taken"], cases
    assert L.rule() == (L.HOME, L.SEED, L.BARS, "junk_explained", ("ending", "known", "name"))
    assert L.rule(True) == (L.HOME_AGAIN, L.SEED_AGAIN, L.BARS_AGAIN, "junk_called_ending_or_known", L.LAID) and L.LAID == ("ending", "known")
    assert L.BARS_AGAIN == {"kappa": 0.6, "junk_called_ending_or_known": 0.10, "endings_called_ending": 0.70}
    assert L.SEED_AGAIN != L.SEED and L.HOME_AGAIN != L.HOME


def test_the_second_reading_lays_an_ending_or_a_known_word_and_never_a_name():
    def g(form, *parts, **more):
        return {"form": form, "level": "unknown", "parts": [{"form": f, "entry": e} for f, e in parts]} | more

    def row(q, run, entry, n, form, verdict):
        return {"place": q, "run": run, "entry": entry, "text": "T", "n": n, "form": form, "verdict": verdict}
    gl = {"T": [g("atox", ("ato", "ato"), ("x", None)), g("atoy", ("ato", "ato"), ("y", None)), g("kbx", ("kb", "kb"), ("x", None)),
                g("kbzz", ("kb", "kb"), ("zz", "zz")), g("Sklx", ("Skl", "Skl"), ("x", None)), g("atoz", ("ato", "ato"), ("z", None)),
                g("atow", ("ato", "ato"), ("w", None)), g("atov", ("ato", "ato"), ("v", None))]}
    rows = [row("Q4", "g4", "kb", 4, "kbzz", "ending"), row("Q3", "g4", "kb", 3, "kbx", "known"), row("Q5", "g4", "Skl", 5, "Sklx", "ending"),
            row("Q1", "g2", "ato", 1, "atox", "ending"), row("Q2", "g2", "ato", 2, "atoy", "name"), row("Q6", "g2", "ato", 6, "atoz", "unknown"),
            row("Q7", "g2", "ato", 7, "atow", "not agreed"), row("Q8", "g2", "ato", 8, "atov", "known, not the same sure entry")]
    lex = LEX | {"zz": {"kind": "noun", "status": "hypothesis"}}
    verified = {"g2": {"ato": {"one": {"meaning": "water", "source": "the lexicon of 2003", "page": 1}}},
                "g4": {"kb": {"one": {"meaning": "to do", "source": "Rilly 2021", "page": 2}}, "Skl": {"one": {"meaning": "a town", "source": "Rilly 2016", "page": 3}}}}
    out, apart = L.lines_again(rows, gl, lex, {"kb"}, verified)
    assert out == [                                                             # the places of G2 first, then those of G4
        {"text": "T", "n": 1, "form": "atox", "item": "ato", "was": "unknown", "level": "meaning", "gloss": "water", "why": "form", "source": "the lexicon of 2003, p. 1"},
        {"text": "T", "n": 3, "form": "kbx", "item": "kb", "was": "unknown", "level": "meaning", "gloss": "to do", "why": "stated", "source": "Rilly 2021, p. 2"},
        {"text": "T", "n": 5, "form": "Sklx", "item": "Skl", "was": "unknown", "level": "name", "gloss": "a town", "why": "stated", "source": "Rilly 2016, p. 3"}]
    assert apart == {L.OTHER_STEM: 1} and all(o["why"] in M.WHY for o in out)   # Q4: zz is a stem without a meaning; Q2, a name, is not laid
    assert stops(lambda: L.lines_again([row("Q1", "g2", "ato", 1, "atoq", "ending")], gl, lex, set(), verified), "the map has changed at this place")
    laid = {"T": [gl["T"][0] | {"layer": "another"}]}
    assert stops(lambda: L.lines_again(rows[3:4], laid, lex, set(), verified), "the map has changed at this place")
    with tempfile.TemporaryDirectory() as d:                                    # a reading that missed a bar lays nothing
        L.write("result.json", {"taken": False, "rows": rows}, Path(d))
        assert stops(lambda: L.build_again(Path(d)), "a bar was missed: nothing is laid")


def test_a_checkers_file_counts_only_for_its_own_pack():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        L.write("groups.json", [["Q1", "Q2"], ["Q3"]], d)
        (d / "answers1").mkdir()
        (d / "answers1" / "P01.jsonl").write_text('{"place": "Q1", "case": "ending"}\n{"place": "Q1", "case": "name"}\nnot json\n'
                                                   '{"place": "Q3", "case": "name"}\n{"place": "Q2", "case": "a guess"}\n', encoding="utf-8")
        (d / "answers1" / "P02.jsonl").write_text('{"place": "Q3", "case": "unknown"}\n["Q3"]\n', encoding="utf-8")
        got = L.answers(1, d)
    assert {k: v["case"] for k, v in got.items()} == {"Q1": "ending", "Q3": "unknown"}     # the first line wins; a case outside CASES is none


def test_the_lot_letters_are_told_by_checker_and_by_place():
    """A run of lot letters is explained as the first reading's bar counts it: an ending, a known word or a name;
    "unclear" explains nothing (J4)."""
    key = [{"place": f"J{i}", "control": "junk", "front": i < 2, "parts": [["zz", None], ["te", "te-dḫe-l"]] if i < 2 else [["ato", "ato"], ["zz", None]]}
           for i in range(5)] + [{"place": "E0", "control": "ending"}]
    one = {"J0": {"case": "name"}, "J1": {"case": "name"}, "J2": {"case": "unknown"}, "J3": {"case": "ending"}, "J4": {"case": "unclear"}, "E0": {"case": "ending"}}
    two = {"J0": {"case": "name"}, "J1": {"case": "unknown"}, "J2": {"case": "unknown"}, "J3": {"case": "unknown"}, "J4": {"case": "unknown"}, "E0": {"case": "ending"}}
    got = L.lot_letters(key, one, two)
    assert got["shown"] == 5 and got["explained"] == {"1": 3, "2": 1} and got["explained_as"] == {"1": {"name": 2, "ending": 1}, "2": {"name": 1}}
    assert got["unknown_by_both"] == 1 and [(x["word"], x["letters"], x["answers"]) for x in got["explained_at"]] == [
        ("te-dḫe-l", "before", ["name", "name"]), ("te-dḫe-l", "before", ["name", "unknown"]), ("ato", "after", ["ending", "unknown"])]
    assert L.rule()[4] == L.EXPLAINS                                            # the figure counts what the first reading's bar counts


def test_a_word_of_the_dictionary_counts_for_the_first_layer_that_gives_it_a_meaning():
    """src/themap.py's rule for the north star: a word an earlier layer gave a meaning is not counted again."""
    def line(item):
        return {"item": item, "why": "stated", "level": "meaning"}
    lex = {"kb": {"kind": "verb", "status": "hypothesis"}, "zz": {"kind": "noun", "status": "hypothesis"}}
    saved = M.LAYERS, M.lines_of, M.current, L.D.population_of
    M.LAYERS = [{"name": "earlier"}, {"name": L.LAYER}, {"name": L.LAYER_AGAIN}]
    M.lines_of = lambda layer: [line("kb")] if layer["name"] == "earlier" else [line("zz")]
    M.current = lambda upto=None: {}
    L.D.population_of = lambda gl, lex, fix=False: ({"kb": 1, "zz": 1}, {}, {})
    try:
        assert L.first_given(L.LAYER, [line("kb"), line("zz")], lex) == ["zz"]
        assert L.first_given(L.LAYER_AGAIN, [line("zz")], lex) == []
    finally:
        M.LAYERS, M.lines_of, M.current, L.D.population_of = saved


def test_part_1_reads_the_map_as_it_was_when_the_step_was_set():
    assert L.BEFORE == tuple(l["name"] for l in M.LAYERS[:len(L.BEFORE)]) and L.LAYER == M.LAYERS[len(L.BEFORE)]["name"]
    assert L.LAYER_AGAIN == M.LAYERS[len(L.BEFORE) + 1]["name"] and len(M.LAYERS) == len(L.BEFORE) + 3
    # part 3 was set on the six layers before its own, which is the last
    assert L.BEFORE_STEMS == tuple(l["name"] for l in M.LAYERS[:-1]) and L.LAYER_STEMS == M.LAYERS[-1]["name"]
    layers = M.LAYERS
    M.LAYERS = [{"name": "another"}] + layers
    try:
        assert stops(L.before, "the layers before this step are no longer")
        assert stops(L.before_stems, "the layers before this step are no longer")
    finally:
        M.LAYERS = layers


def a_stems(d, said, wrong=None):
    """A made-up part 3 in folder d, one pack: 20 hidden stems of `ato`, 20 hidden endings, 20 names and 20 runs of
    lot letters, each answered rightly by both checkers but for `wrong` ({(checker, kind): (how many of that kind,
    the case said of them, the entry said)}), and the real places of `said` ({place: (checker 1's answer, checker
    2's answer, how many parts of the spelling are unnamed)}; an answer is a case or ("known", an entry))."""
    wrong = wrong or {}
    key = [{"place": f"{kind[0].upper()}{i:02d}", "control": kind, "answer": answer} | ({"answer_entry": "ato"} if kind == "stem" else {})
           for kind, answer in (("stem", "known"), ("ending", "ending"), ("name", "name"), ("lot", "unknown")) for i in range(20)]
    key += [{"place": q, "control": None, "run": "g2", "entry": "-qo", "text": "T", "n": n, "form": f"zz{n}qo",
             "parts": [["zz", None]] * v[2] + [["qo", "-qo"]]} for n, (q, v) in enumerate(said.items(), 1)]
    L.write("key.json", key, d)
    L.write("groups.json", [[p["place"] for p in key]], d)
    for c in (1, 2):
        (d / f"answers{c}").mkdir()
        lines = []
        for p in key:
            if p["control"]:
                many, case, entry = (wrong.get((c, p["control"])) or (0, "", "")) + ("",) * 3 if False else (*(wrong.get((c, p["control"])) or (0, "")), "")[:3]
                if int(p["place"][1:]) < many:
                    lines.append({"place": p["place"], "case": case, "entry": entry})
                else:
                    lines.append({"place": p["place"], "case": p["answer"], "entry": p.get("answer_entry", "")})
            else:
                a = said[p["place"]][c - 1]
                lines.append({"place": p["place"], "case": a[0], "entry": a[1]} if isinstance(a, tuple) else {"place": p["place"], "case": a})
        (d / f"answers{c}" / "P01.jsonl").write_text("".join(json.dumps(l) + "\n" for l in lines), encoding="utf-8")


def counted_stems(said, wrong=None, drop=None):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        a_stems(d, said, wrong)
        if drop:                                                                # one checker leaves a place out
            f = d / "answers1" / "P01.jsonl"
            f.write_text("".join(l + "\n" for l in f.read_text(encoding="utf-8").splitlines() if json.loads(l)["place"] != drop), encoding="utf-8")
        with_lexicon(lambda: quiet(L.count_stems, d))
        return L.read("result.json", d)


SAID = {"R1": ("name", "name", 1), "R2": ("unknown", "unknown", 1), "R3": (("known", "ato"), ("known", "ato"), 1), "R4": ("ending", "ending", 2)}


def test_each_verdict_of_the_stems_stands_on_its_own_bars():
    res = counted_stems(SAID)
    assert res["taken"] == {"known": True, "ending": True, "name": True} and res["kappa"] == 1.0 and res["places"] == res["answered_by_both"] == 4
    assert res["verdicts"] == {"name": 1, "unknown": 1, "known": 1, "ending": 1}
    assert [(r["place"], r["unnamed"], r["known_entry"]) for r in res["rows"]] == [("R1", 1, ""), ("R2", 1, ""), ("R3", 1, "ato"), ("R4", 2, "")]
    # one bar missed by one answer stops its own verdict and no other
    for wrong, lost in (({(1, "lot"): (3, "name")}, "name"), ({(2, "stem"): (3, "name")}, "name"), ({(2, "name"): (7, "unknown")}, "name"),
                        ({(1, "lot"): (3, "known", "ato")}, "known"), ({(1, "stem"): (7, "unknown")}, "known"), ({(2, "stem"): (7, "known", "kb")}, "known"),
                        ({(2, "lot"): (3, "ending")}, "ending"), ({(1, "ending"): (7, "unknown")}, "ending")):
        taken = counted_stems(SAID, wrong)["taken"]
        assert taken == {v: v != lost for v in L.VERDICTS}, (wrong, taken)
    # at the bar itself every verdict stands: 2 of 20 said wrongly, 14 of 20 found
    at = {(1, "lot"): (2, "name"), (2, "lot"): (2, "ending"), (1, "stem"): (6, "unknown"), (2, "ending"): (6, "unknown"), (2, "name"): (6, "unknown")}
    assert counted_stems(SAID, at)["taken"] == {"known": True, "ending": True, "name": True}
    assert round(L.HIT * L.N_STEMS) == 14 and round(L.FALSE * L.N_STEMS) == 2
    # a hidden stem counts as found only with its own entry, a homonym number or a hyphen aside
    assert counted_stems(SAID, {(1, "stem"): (20, "known", "ato (2)")})["controls"]["1"]["stem_with_its_entry"] == 20
    assert counted_stems(SAID, {(1, "stem"): (20, "known", "kb")})["controls"]["1"]["stem_with_its_entry"] == 0
    # the two bars every verdict needs: a place one checker left out, or a kappa under 0.6, and nothing is taken
    assert counted_stems(SAID, drop="E03")["taken"] == {"known": False, "ending": False, "name": False}
    apart = {"R1": ("name", "unknown", 1), "R2": ("unknown", "name", 1), "R3": ("name", "name", 1), "R4": ("unknown", "unknown", 1)}
    res = counted_stems(apart)
    assert res["kappa"] < 0.6 and not any(res["taken"].values()) and res["general"] == {"every_place_answered_by_both": True, "kappa": False}


def test_a_known_stem_needs_the_same_sure_entry_from_both():
    said = {"R1": (("known", "ato"), ("known", "ato"), 1), "R2": (("known", "ato"), ("known", "kb"), 1), "R3": (("known", "kb"), ("known", "kb"), 1),
            "R4": ("name", "name", 1), "R5": ("unknown", "unknown", 1), "R6": ("name", "ending", 1)}
    rows = {r["place"]: (r["verdict"], r["known_entry"]) for r in counted_stems(said)["rows"]}
    assert rows == {"R1": ("known", "ato"), "R2": ("known, not the same sure entry", ""), "R3": ("known, not the same sure entry", ""),   # kb is not sure
                    "R4": ("name", ""), "R5": ("unknown", ""), "R6": ("not agreed", "")}


def test_the_stems_lay_a_known_word_a_name_and_an_ending_each_by_its_rule():
    def g(form, *parts, **more):
        return {"form": form, "level": "unknown", "parts": [{"form": f, "entry": e} for f, e in parts]} | more

    def row(q, n, form, verdict, unnamed=1, entry=""):
        return {"place": q, "run": "g2", "entry": "-qo", "text": "T", "n": n, "form": form, "unnamed": unnamed, "verdict": verdict, "known_entry": entry}
    gl = {"T": [g("zzqo", ("zz", None), ("qo", "-qo")), g("atqo", ("at", None), ("qo", "-qo")), g("xyqo", ("x", None), ("y", None), ("qo", "-qo")),
                g("zzyqo", ("zz", None), ("y", None), ("qo", "-qo")), g("atyqo", ("at", None), ("y", None), ("qo", "-qo")),
                g("zzkbqo", ("zz", None), ("kb", "kb"), ("qo", "-qo")), g("wwqo", ("ww", None), ("qo", "-qo")), g("vvqo", ("vv", None), ("qo", "-qo")),
                g("uuqo", ("uu", None), ("qo", "-qo"))]}
    rows = [row("Q1", 1, "zzqo", "name"), row("Q2", 2, "atqo", "known", 1, "ato"), row("Q3", 3, "xyqo", "ending", 2),
            row("Q4", 4, "zzyqo", "name", 2), row("Q5", 5, "atyqo", "known", 2, "ato"), row("Q6", 6, "zzkbqo", "name"),
            row("Q7", 7, "wwqo", "unknown"), row("Q8", 8, "vvqo", "known, not the same sure entry"), row("Q9", 9, "uuqo", "not agreed")]
    lex = {"ato": {"kind": "noun", "status": "established", "meaning": "water", "page": 7}, "kb": {"kind": "verb", "status": "hypothesis"},
           "-qo": {"kind": "function word", "status": "established"}}
    every = {"known": True, "ending": True, "name": True}
    out, apart = L.lines_stems({"taken": every, "rows": rows}, gl, lex, set())
    base = {"text": "T", "item": "-qo", "was": "unknown"}
    assert out == [
        base | {"n": 1, "form": "zzqo", "level": "name", "gloss": "a name, by its place in the text", "why": "name", "source": "two checkers"},
        base | {"n": 2, "form": "atqo", "level": "meaning", "gloss": "ato: water", "why": "form", "source": "the lexicon of 2003, p. 7"},
        base | {"n": 3, "form": "xyqo", "level": "grammar", "gloss": "endings or particles only", "why": "form", "source": "the lexicon's entries of the endings"}]
    assert [list(o) for o in out] == [["text", "n", "form", "item", "was", "level", "gloss", "why", "source"]] * 3
    # a name and a known word need a spelling with one unnamed part; an ending may fill several; no line beside a stem without a meaning
    assert apart == {f"name: {L.MORE_UNNAMED}": 1, f"known: {L.MORE_UNNAMED}": 1, f"name: {L.OTHER_STEM}": 1}
    assert all(o["why"] in M.WHY and o["level"] in W.READ + W.NAMED for o in out)
    assert L.lines_stems({"taken": every, "rows": rows}, gl, lex, {"kb"})[1] == {f"name: {L.MORE_UNNAMED}": 1, f"known: {L.MORE_UNNAMED}": 1}   # kb stated by a later source
    # a verdict whose bars were missed is not laid, the others are
    for lost, levels in (("name", ["meaning", "grammar"]), ("known", ["name", "grammar"]), ("ending", ["name", "meaning"])):
        out, apart = L.lines_stems({"taken": every | {lost: False}, "rows": rows}, gl, lex, set())
        assert [o["level"] for o in out] == levels and apart[f"{lost}: {L.BARS_MISSED}"] == sum(r["verdict"] == lost for r in rows), lost
    assert L.lines_stems({"taken": dict.fromkeys(L.VERDICTS, False), "rows": rows}, gl, lex, set())[0] == []
    # the map must still be what the checkers saw
    assert stops(lambda: L.lines_stems({"taken": every, "rows": [row("Q1", 1, "zzqe", "name")]}, gl, lex, set()), "the map has changed at this place")
    laid = {"T": [gl["T"][0] | {"layer": "another"}]}
    assert stops(lambda: L.lines_stems({"taken": every, "rows": rows[:1]}, laid, lex, set()), "the map has changed at this place")


def a_map_for_controls(entries=30):
    """A made-up map: `entries` sure words, three places each (the first 25 with a stem of four letters, the others
    of two), 9 personal names and 15 names the lexicon holds, each with an ending; a word a layer has laid and a
    word of one part, which no control may take."""
    def word(form, level, *parts, **more):
        return {"form": form, "level": level, "parts": [{"form": f, "entry": e} for f, e in parts]} | more
    lex = {f"w{i:02d}": {"kind": "noun", "status": "established"} for i in range(entries)}
    lex |= {f"N{i:02d}": {"kind": "place name", "status": "established"} for i in range(15)}
    lex |= {"-lo": {"kind": "function word", "status": "established"}, "-qo": {"kind": "function word", "status": "established"}}
    stem = lambda i: f"s{i:02d}x" if i < 25 else f"{'bdklm'[i - 25]}a"                 # noqa: E731
    gl = {f"T{k}": [word(stem(i) + "lo", "meaning", (stem(i), f"w{i:02d}"), ("lo", "-lo")) for i in range(entries)] for k in range(3)}
    gl["P"] = [word(f"p{i}yeqo", "name", (f"p{i}ye", "NAME"), ("qo", "-qo")) for i in range(9)]
    gl["H"] = [word(f"n{i:02d}qo", "name", (f"n{i:02d}", f"N{i:02d}"), ("qo", "-qo")) for i in range(15)]
    gl["X"] = [word("s00xlo", "meaning", ("s00x", "w00"), ("lo", "-lo"), layer="another"), word("s01x", "meaning", ("s01x", "w01"))]
    return gl, lex


def test_the_controls_of_the_stems_take_twenty_entries_a_kind_and_no_word_twice():
    gl, lex = a_map_for_controls()
    cs = L.controls_stems(gl, lex, random.Random(5))
    assert collections.Counter(c["control"] for c in cs) == dict.fromkeys(L.KINDS_STEMS, L.N_STEMS)
    assert len({(c["text"], c["i"]) for c in cs}) == len(cs) == 4 * L.N_STEMS and not any(c["text"] == "X" for c in cs)

    def stem(c):
        return next(p for p in gl[c["text"]][c["i"]]["parts"] if p["entry"] == "NAME" or not W.affix(p["entry"]))
    for kind in ("stem", "ending", "lot"):                                      # twenty different entries a kind
        assert len({stem(c)["entry"] for c in cs if c["control"] == kind}) == L.N_STEMS, kind
    holds = {g["form"] for gs in gl.values() for g in gs}
    for c in cs:
        parts = gl[c["text"]][c["i"]]["parts"]
        if c["control"] == "stem":                                              # the stem hidden, three letters or more, its entry the answer
            assert c["hide"] == [parts.index(stem(c))] and len(stem(c)["form"]) >= 3 and (c["answer"], c["answer_entry"]) == ("known", stem(c)["entry"])
        elif c["control"] == "ending":                                          # every ending hidden, the stem shown
            assert c["hide"] == [j for j, p in enumerate(parts) if W.affix(p["entry"])] and c["answer"] == "ending"
        elif c["control"] == "lot":                                             # as many letters by lot as the stem has, three at least, no spelling of the map
            assert len(c["junk"]) == max(3, len(stem(c)["form"])) and c["junk"] not in holds and c["at"] == parts.index(stem(c)) and c["answer"] == "unknown"
        else:
            assert c["hide"] == [parts.index(stem(c))] and c["answer"] == "name"
    names = [c for c in cs if c["control"] == "name"]                           # every personal name of the map, filled up with names the lexicon holds
    assert sum(c["text"] == "P" for c in names) == 9 and sum(c["text"] == "H" for c in names) == L.N_STEMS - 9
    assert any(len(stem(c)["form"]) < 3 for c in cs if c["control"] in ("ending", "lot"))    # a short stem may have its endings hidden or its letters replaced
    assert L.controls_stems(gl, lex, random.Random(5)) == cs != L.controls_stems(gl, lex, random.Random(6))
    few, lex_few = a_map_for_controls(15)
    assert stops(lambda: L.controls_stems(few, lex_few, random.Random(5)), "too few entries for a kind of control")


def test_the_controls_are_counted_by_entry_and_a_name_once():
    """Each kind by the entries its words were drawn from; a personal name of the map by its spelling; a name of the
    lexicon that stands twice is one name, found by a checker only if both its places are called a name."""
    def word(form, level, *parts):
        return {"form": form, "level": level, "parts": [{"form": f, "entry": e} for f, e in parts]}
    gl = {"T": [word("abclo", "meaning", ("abc", "w1"), ("lo", "-lo")), word("abclo", "meaning", ("abc", "w1"), ("lo", "-lo")),
                word("deflo", "meaning", ("def", "w2"), ("lo", "-lo")), word("pyeqo", "name", ("pye", "NAME"), ("qo", "-qo")),
                word("ryeqo", "name", ("rye", "NAME"), ("qo", "-qo")), word("aSoreqo", "name", ("aSore", "Asori"), ("qo", "-qo")),
                word("aSoreqo", "name", ("aSore", "Asori"), ("qo", "-qo"))]}
    key = [{"place": q, "control": kind, "text": "T", "i": i} for q, kind, i in (("S1", "stem", 0), ("S2", "stem", 2), ("E1", "ending", 1), ("L1", "lot", 2),
                                                                                 ("N1", "name", 3), ("N2", "name", 4), ("N3", "name", 5), ("N4", "name", 6), ("Q1", None, 0))]
    name, unknown = {"case": "name"}, {"case": "unknown"}
    ans = {1: dict.fromkeys(("N1", "N2", "N3", "N4"), name), 2: {"N1": name, "N2": unknown, "N3": name, "N4": unknown}}
    got = L.control_entries(key, gl, ans)
    assert got["entries"] == {"stem": 2, "ending": 1, "name": 3, "lot": 1} and got["names_of_the_lexicon"] == {"places": 2, "entries": 1}
    assert got["name_found_counted_once"] == {"names": 3, "found": {"1": 3, "2": 1}, "bar_met": False}    # Asori found at one of its places only


def test_the_letters_by_lot_stand_in_the_stems_place():
    gl, lex = a_map_for_controls()
    old = L.U.shown
    L.U.shown = lambda gs, i, hide, rows, t: {"form": gs[i]["form"], "level": gs[i]["level"], "hidden": sorted(hide)}
    try:
        c = next(c for c in L.controls_stems(gl, lex, random.Random(5)) if c["control"] == "lot")
        p = L.place_of_stems(c, gl, {})
        real = gl[c["text"]][c["i"]]
        assert p["parts"][c["at"]] == (c["junk"], None) and p["form"] == "".join(f for f, _ in p["parts"]) != real["form"] and p["level"] == "unknown"
        assert [e for _, e in p["parts"]].count(None) == 1 and p["hidden"] == [c["i"]] and gl[c["text"]][c["i"]] is real   # the map itself is not changed
        s = next(c for c in L.controls_stems(gl, lex, random.Random(5)) if c["control"] == "stem")
        shown = L.place_of_stems(s, gl, {})
        assert shown["form"] == gl[s["text"]][s["i"]]["form"] and shown["parts"][s["hide"][0]][1] is None
    finally:
        L.U.shown = old


def test_part_2_is_the_brief_of_g4_with_the_source_changed():
    b = L.brief()
    assert "Millet 2005 or Lipinski 2011, the one that states it most firmly" in b and "Rilly 2016 or Rilly 2021" not in b
    assert '"stance": "accepts", "what": "word", ' in b and '"partly" when\n  the meaning it gives leaves a Meroitic word as it is' in b
    assert "Judge only what Millet 2005 or Lipinski 2011 states" in b and "`data/sources/jssea-text/pages.txt`" in b
    rest = b
    for new, old in ((L.NEW_SOURCE, L.OLD_SOURCE), (L.NEW_WHAT, ""), (L.NEW_FILES, L.OLD_FILES)):
        rest = rest.replace(new, old)
    assert rest == W.VERIFY_BRIEF                                               # nothing else differs from the brief of G4
    old = W.VERIFY_BRIEF
    W.VERIFY_BRIEF = old.replace("Rilly 2016 or Rilly 2021", "Rilly")
    try:
        assert stops(L.brief, "the brief of G4 has changed")
    finally:
        W.VERIFY_BRIEF = old


def test_an_entry_is_stated_only_by_millet_or_lipinski_and_says_what_is_given():
    def v(source_a, source_b, what_a, what_b, verdict="stated"):
        return {"verdict": verdict, "one": {"source": source_a, "what": what_a}, "two": {"source": source_b, "what": what_b}}
    made = {"a": v("Millet 2005", "Millet 2005", "word", "word"), "b": v("Rilly 2021", "Rilly 2021", "word", "word"),
            "c": v("Lipinski 2011", "Lipinski 2011", "name", "word"), "d": v("Millet 2005", "Millet 2005", "partly", "partly"),
            "e": v("Millet 2005", "Millet 2005", "name", "name", "not stated firmly"), "f": v("Millet 2005", "Lipinski 2011", "a guess", "a guess")}
    out, verify = W.OUT, R.verify
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "lit/verify").mkdir(parents=True)
        (Path(d) / "lit/verify/result.json").write_text(json.dumps(made), encoding="utf-8")
        R.verify = lambda run: setattr(W, "OUT", Path(d))                      # the count of the two readers, made up above
        try:
            quiet(L.verify)
            got = json.loads((Path(d) / "lit/verify/result.json").read_text(encoding="utf-8"))
        finally:
            W.OUT, R.verify = out, verify
    assert {k: (x["verdict"], x["what"]) for k, x in got.items()} == {
        "a": ("stated", "word"), "b": ("not stated by Millet 2005 or Lipinski 2011", "word"), "c": ("stated", "differ"),
        "d": ("stated", "partly"), "e": ("not stated firmly", "name"), "f": ("not stated by Millet 2005 or Lipinski 2011", "differ")}


def test_a_stated_place_is_a_word_only_when_both_readers_say_the_meaning_is_given_in_full():
    def line(item, why="stated", level="meaning"):
        return {"item": item, "why": why, "level": level}
    verified = {"w": {"what": "word"}, "n": {"what": "name"}, "p": {"what": "partly"}, "d": {"what": "differ"}, "x": {}}
    laid = [line("w"), line("n"), line("p"), line("d"), line("x"), line("p", level="name"), line("p", "piece"), line("d", "piece", "name")]
    out, apart = L.given_as(laid, verified, {"another reason": 2})
    assert out == [line("w"), line("n", "name", "name"), line("p", level="name"), line("p", "piece"), line("d", "piece", "name")]
    assert apart == {"another reason": 2, L.LEFT: 3}
    assert all(o["why"] in M.WHY for o in out)


def test_a_name_is_a_place_name_by_the_lexicon_or_a_personal_name_by_both_readers():
    def v(a, b):
        return {"one": {"meaning": a}, "two": {"meaning": b}}
    assert L.name_kind("Skl", v("a town", "a place"), LEX) == "a place name"
    assert L.name_kind("kb", v("personal name X", "the personal name X of a scribe"), LEX) == "a personal name"
    assert L.name_kind("kb", v("personal name X", "a name"), LEX) == "a name" and L.name_kind("gone", v(None, None), LEX) == "a name"


def test_what_the_checkers_were_given_is_public():
    prompts = (ROOT / "runs/prompts/G8_parts.md").read_text(encoding="utf-8")
    assert "\n".join(("    " + l).rstrip() for l in L.BRIEF.strip("\n").splitlines()) in prompts
    assert "Some places are put in on purpose: their answer is known. They look like the others." in L.BRIEF
    assert "This pack lists {places} places: your file must have {places} lines" in L.BRIEF
    assert "The second reading of a place pass" in Path(R.__file__).read_text(encoding="utf-8") and "{places} lines, one for each place, none left out" in R.COUNTED
    again = (ROOT / "runs/prompts/G8_parts_2.md").read_text(encoding="utf-8")   # the second reading: the same brief, another folder
    assert "The brief of the first reading, in [`G8_parts.md`](G8_parts.md), word for word." in again
    assert f"/{L.HOME_AGAIN.relative_to(ROOT)}/packs/P<nn>_c<1|2>.md" in again and f"`{L.HOME_AGAIN.relative_to(ROOT)}/answers<1|2>/P<nn>.jsonl`" in again


# ------------------------------------------------------------------------------------ the figures and the pages

def test_the_figures_add_up():
    f = figs()
    one, two = f["part_1"], f["part_2"]
    assert one["places"] == sum(one["places_by_run"].values()) == sum(one["verdicts"].values()) == one["answered_by_both"]
    assert one["controls"] == L.CONTROLS and one["lines_expected"] == one["places"] + sum(one["controls"].values()) == one["answered"]["1"] == one["answered"]["2"]
    assert one["verdicts"] == {k: sum(v.get(k, 0) for v in one["verdicts_by_run"].values()) for k in one["verdicts"]}
    lot = one["lot_letters"]
    assert lot["shown"] == L.CONTROLS["junk"] and lot["unknown_by_both"] + len(lot["explained_at"]) == lot["shown"]
    assert all(sum(lot["explained_as"][j].values()) == lot["explained"][j] for j in "12")
    most = L.BARS["junk_explained"] * lot["shown"]
    assert one["bars"]["junk_explained"] == all(n <= most for n in lot["explained"].values())
    assert one["bars"]["endings_called_ending"] == all(h["called_ending"] >= L.BARS["endings_called_ending"] * h["shown"] for h in one["hidden_endings"].values())
    assert one["bars"]["kappa"] == (one["kappa"] >= L.BARS["kappa"]) and one["taken"] == all(one["bars"].values())
    assert not one["taken"] and max(lot["explained"].values()) == most + 1       # the first reading: one bar missed, by one answer
    assert two["entries"] == sum(two["entries_by_source"].values()) == sum(two["read_twice"].values()) == len(two["by_entry"])
    assert two["read_twice"]["stated"] == sum(two["gives"].values()) and two["gives"]["name"] == sum(two["names"].values())
    for e in two["by_entry"]:
        assert (e["verdict"] == "stated") == bool(e["gives"]) == bool(e["source"]) and bool(e["meaning"]) == (e["gives"] in ("word", "name")), e
        assert e["gives"] != "word" or e["meaning"] == L.MEANINGS[e["entry"]], e
    p = two["the_places"]
    assert p["taken"] and p["places"] == p["answered by both"] == two["places"] == sum(p["verdicts"].values()) and p["kappa"] >= p["bar"] == 0.6
    laid, out = two["laid"], two["left_out"]
    assert laid["lines"] == sum(laid["why"].values()) == sum(laid["to"].values()) == sum(laid["was"].values())
    assert {w: sum(v.values()) for w, v in laid["to_by_why"].items()} == laid["why"]
    stated_out = sum(n for k, n in out.items() if k.startswith("stated"))
    assert p["verdicts"]["stated"] == laid["why"]["stated"] + laid["why"]["name"] + stated_out
    assert p["verdicts"]["piece"] == laid["why"]["piece"] + sum(n for k, n in out.items() if k.startswith("piece"))
    assert {w["entry"]: w["meaning"] for w in two["words"]} == L.MEANINGS and sum(w["places_laid"] for w in two["words"]) == laid["to"]["meaning"]
    cost = f["cost"]
    assert cost["all"] == {k: sum(v[k] for s, v in cost.items() if s != "all") for k in ("agents", "tokens")}
    assert cost["part 1, the checkers"]["agents"] == 2 * one["packs"] and [w["step"] for w in f["when"]] == [w["step"] for w in L.WHEN]
    # the second reading of part 1: the same places, its own bars, and what it lays
    a = f["part_1_again"]
    assert (a["places"], a["places_by_run"], a["controls"], a["packs"], a["lines_expected"]) == (one["places"], one["places_by_run"], one["controls"], one["packs"], one["lines_expected"])
    assert a["places"] == sum(a["verdicts"].values()) == a["answered_by_both"] and a["answered"] == {"1": a["lines_expected"], "2": a["lines_expected"]}
    assert a["verdicts"] == {k: sum(v.get(k, 0) for v in a["verdicts_by_run"].values()) for k in a["verdicts"]}
    lot = a["lot_letters"]
    assert lot["shown"] == L.CONTROLS["junk"] and lot["unknown_by_both"] + len(lot["explained_at"]) == lot["shown"]
    called = {j: sum(lot["explained_as"][j].get(k, 0) for k in L.LAID) for j in "12"}
    assert a["bars_set"] == L.BARS_AGAIN and one["bars_set"] == L.BARS and set(a["bars"]) == {"every_place_answered_by_both", "kappa", *(set(L.BARS_AGAIN) - {"kappa"})}
    assert a["bars"]["junk_called_ending_or_known"] == all(n <= L.BARS_AGAIN["junk_called_ending_or_known"] * lot["shown"] for n in called.values())
    assert a["bars"]["endings_called_ending"] == all(h["called_ending"] >= L.BARS_AGAIN["endings_called_ending"] * h["shown"] for h in a["hidden_endings"].values())
    assert a["bars"]["kappa"] == (a["kappa"] >= L.BARS_AGAIN["kappa"]) and a["taken"] == all(a["bars"].values()) and a["taken"]
    laid = a["laid"]
    assert laid["lines"] == sum(laid["why"].values()) == sum(laid["to"].values()) == sum(laid["was"].values()) == sum(laid["by_run"].values())
    assert {w: sum(v.values()) for w, v in laid["to_by_why"].items()} == laid["why"] and set(laid["why"]) == {"form", "stated"}
    assert laid["by_run"] == {"g2": laid["why"]["form"], "g4": laid["why"]["stated"]}
    assert sum(a["verdicts"][k] for k in L.LAID) == laid["lines"] + sum(a["left_out"].values()) and set(a["left_out"]) == {L.OTHER_STEM}
    assert a["not_laid"] == {"name": a["verdicts"]["name"]} and a["not_laid"]["name"] > 0      # both called them a name; none is laid
    assert {w["entry"]: w["meaning"] for w in a["words"]} == L.MEANINGS_AGAIN and all(w["places_laid"] >= 1 for w in a["words"])
    assert cost["part 1 again, the checkers"]["agents"] == 2 * a["packs"]


def test_the_figures_hold_no_wording_of_a_source():
    def strings(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from strings(v, k)
        elif isinstance(o, list):
            for v in o:
                yield from strings(v, key)
        elif isinstance(o, str):
            yield key, o
    f = figs()
    allowed = {"entry": None, "word": None, "kind": {"", "noun", "title", "verb", "place name"}, "source": {"", *L.SOURCES, "Rilly 2016", "Rilly 2021"},
               "verdict": {"stated", "not stated firmly", "not stated by Millet 2005 or Lipinski 2011"}, "gives": {"", *L.WHAT, "differ"},
               "meaning": {"", "a place name", "a personal name", "a name", *L.MEANINGS.values(), *L.MEANINGS_AGAIN.values()}, "letters": {"before", "after"},
               "answers": set(L.CASES), "step": {w["step"] for w in L.WHEN}}
    for key, v in strings(f):
        if key in ("set_in", "set", "started", "first_answer", "last_answer", "counted"):
            assert re.fullmatch(r"[0-9a-f]{7}|\d\d:\d\d:\d\d", v), (key, v)
        else:
            assert key in allowed and (allowed[key] is None or v in allowed[key]), (key, v)
    heads = {e["entry"] for e in f["part_2"]["by_entry"]} | {"qo", "te-dḫe-l", "ato", "t-erike-l"} | set(L.MEANINGS_AGAIN)
    assert {v for k, v in strings(f) if k in ("entry", "word")} <= heads       # headwords of the lexicon, nothing else
    import lexicon as X
    assert all(len(X.words_of(v)) <= X.LONGEST for v in [*L.MEANINGS.values(), *L.MEANINGS_AGAIN.values()])


def test_the_map_lays_what_the_figures_say():
    f = figs()["part_2"]
    layers = json.loads(M.PUBLIC.read_text(encoding="utf-8"))["layers"]
    mine = {l["name"]: l for l in layers}[L.LAYER]
    assert [l["name"] for l in layers][:len(L.BEFORE)] == list(L.BEFORE) and layers[len(L.BEFORE)] is mine
    assert (mine["places"], mine["why"], mine["to"], mine["was"]) == (f["laid"]["lines"], f["laid"]["why"], f["laid"]["to"], f["laid"]["was"])
    before = layers[len(L.BEFORE) - 1]
    assert mine["after"]["running"]["translated"] - before["after"]["running"]["translated"] == f["laid"]["to"]["meaning"]
    assert before["after"]["running"]["need"] - mine["after"]["running"]["need"] == f["laid"]["to"]["name"]
    assert mine["distinct_words_translated"] - before["distinct_words_translated"] == len(f["words"])
    a, again = figs()["part_1_again"], layers[len(L.BEFORE) + 1]                # the second reading of part 1 is the layer after it
    assert again["name"] == L.LAYER_AGAIN and again is layers[-2]
    assert (again["places"], again["why"], again["to"], again["was"]) == (a["laid"]["lines"], a["laid"]["why"], a["laid"]["to"], a["laid"]["was"])
    assert again["after"]["running"]["translated"] - mine["after"]["running"]["translated"] == a["laid"]["to"]["meaning"]
    assert mine["after"]["running"]["need"] - again["after"]["running"]["need"] == a["laid"]["to"]["name"]
    assert again["distinct_words_translated"] - mine["distinct_words_translated"] == len(a["words"])
    s, last = stems(), layers[-1]                                               # part 3, the leftover stems, is the last layer
    assert last["name"] == L.LAYER_STEMS
    assert (last["places"], last["why"], last["to"], last["was"]) == (s["laid"]["lines"], s["laid"]["why"], s["laid"]["to"], s["laid"]["was"])
    assert last["after"]["running"]["translated"] - again["after"]["running"]["translated"] == sum(s["laid"]["to"].get(k, 0) for k in W.READ)
    assert again["after"]["running"]["need"] - last["after"]["running"]["need"] == s["laid"]["to"]["name"]
    assert last["distinct_words_translated"] == again["distinct_words_translated"] and s["words"] == []


def test_the_page_says_what_the_figures_say():
    f, text = figs(), page()
    one, two, cost = f["part_1"], f["part_2"], f["cost"]
    w1, w2, w3 = f["when"][:3]
    again = f["part_1_again"]["laid"]
    assert (f"**The second reading of part 1 met its bars** ([leftover_parts_2.md](leftover_parts_2.md)) and is the map's sixth layer, `leftover`: "
            f"{again['lines']} places, {again['to']['meaning']} of them translated words and {again['to']['name']} names.") in text
    both = [again, two["laid"]]
    assert (f"**The step in all:** {sum(x['lines'] for x in both)} places are laid, {sum(x['to']['meaning'] for x in both)} of them as translated words and "
            f"{sum(x['to']['name'] for x in both)} as names, and {len(two['words']) + len(f['part_1_again']['words'])} words of the dictionary get a meaning "
            f"a scholar published; it took {cost['all']['agents']} agents and {cost['all']['tokens']:,} tokens.") in text
    g5 = json.loads((ROOT / "data/discovery/second_scholar_later_figures.json").read_text(encoding="utf-8"))["by_entry"]
    assert {w["entry"]: g5[w["entry"]] for w in f["part_1_again"]["words"]} == {     # so not "each from one scholar"
        "nbr": "agreed by two scholars", "yiroẖe": "agreed by two scholars, with a dissent"}
    assert f"It met its bars and lays {again['lines']} places." in text
    hm = lambda t: t[:5]                                                   # noqa: E731
    lot, ends = one["lot_letters"], one["hidden_endings"]
    v = one["verdicts"]
    # section 1 and 2: the places and the entries
    assert f"**{one['places']} places, not 182.**" in text and f"**{two['entries']} entries, not 8.**" in text
    assert (f"For {two['entries_by_source']['Millet 2005']} entries of G4 without a meaning from Rilly's later work, Millet 2005 states one" in text
            and f"and Lipiński 2011 for {two['entries_by_source']['Lipinski 2011']} more. They stand at {two['places']} places." in text)
    assert f"the {one['places']} places of [the rare spellings](rare_spellings.md)" in text
    assert f"({one['places_by_run']['g2']} of G2, {one['places_by_run']['g4']} of G4;" in text
    assert f"**Controls:** {sum(one['controls'].values())} places of known answer" in text and f"two for each of {one['packs']} packs" in text
    assert f"{one['controls']['ending']} translated words of one stem" in text and f"and {one['controls']['junk']} translated words with three to five" in text
    # section 6: the first reading of part 1
    assert f"## 6. Part 1: the result (counted at {hm(w1['counted'])}, nothing taken)" in text
    assert (f"Six checkers (two for each of {one['packs']} packs) were started at {hm(w1['started'])}, after the commit that set the bars "
            f"({w1['set']}); the last answer came at {hm(w1['last_answer'])}.") in text and cost["part 1, the checkers"]["agents"] == 6
    assert (f"| Every place answered by both | {one['answered']['1']} of {one['lines_expected']} ({one['places']} places, "
            f"{sum(one['controls'].values())} controls) | met |") in text
    assert f"| Kappa of 0.6 or more on the real places | {one['kappa']:.2f} | met |" in text
    need = round(L.BARS["endings_called_ending"] * ends["1"]["shown"])
    assert f"| Each checker calls at least {need} of {ends['1']['shown']} hidden endings an ending | {ends['1']['called_ending']} and {ends['2']['called_ending']} | met |" in text
    most = round(L.BARS["junk_explained"] * lot["shown"])
    assert (f"| Each checker explains at most {most} of {lot['shown']} runs of letters drawn by lot | **{lot['explained']['1']}** and "
            f"{lot['explained']['2']} | **missed by one** |") in text
    assert set(lot["explained_as"]["1"]) == set(lot["explained_as"]["2"]) == {"name"} and sum(lot["explained"].values()) == 5
    assert 'All five explanations were "a name"' in text and "The five answers stand at three places" in text and len(lot["explained_at"]) == 3
    at = [(x["word"], x["letters"]) for x in lot["explained_at"]]
    assert sorted(at) == [("qo", "before"), ("te-dḫe-l", "before"), ("te-dḫe-l", "before")]
    assert 'before `qo` ("this one") once and before the word for "born of" twice' in text
    assert f"At the other {lot['unknown_by_both']} places, where no name is expected, both said \"unknown\" every time." in text
    for label, key in (("ending", "ending"), ("unknown", "unknown"), ("a name", "name"), ("a known word, the same entry", "known"),
                       ("unclear", "unclear"), ("not agreed", "not agreed")):
        assert f"| {label} | {v[key]} |" in text, key
    assert sum(v.values()) == one["places"] and f"What the checkers said of the {one['places']} real places" in text
    found = sum(e["called_ending"] for e in ends.values())
    assert f"({found} of {sum(e['shown'] for e in ends.values())} hidden endings found, 0 of {2 * lot['shown']} runs of lot letters called an ending)" in text
    assert f"The {v['name']} places both checkers call a name rest on that same judgment" in text and f"the {v['ending']} places stay open" in text
    c1 = cost["part 1, the checkers"]
    assert f"Cost: {c1['agents']} agents, {c1['tokens']:,} tokens" in text
    assert "A second reading, with a bar set beforehand for each verdict and fresh checkers, is on its own page ([leftover_parts_2.md](leftover_parts_2.md))" in text
    assert PAGE_AGAIN.exists()
    # section 7: part 2
    assert f"## 7. Part 2: the result (counted at {hm(w3['counted'])}, bars met)" in text
    assert (f"Four readers (two for each of 2 packs) were started at {hm(w2['started'])}, after the commit with the added rule ({w2['set']}); "
            f"their answers came between {hm(w2['first_answer'])} and {hm(w2['last_answer'])}.") in text
    assert f"Four checkers (two for each of 2 packs) were started at {hm(w3['started'])}; their answers came between {hm(w3['first_answer'])} and {hm(w3['last_answer'])}." in text
    assert f"| Stated by Millet 2005 or Lipiński 2011, by both readers | {two['read_twice']['stated']} |" in text
    assert f"| Not stated firmly by both | {two['read_twice']['not stated firmly']} |" in text and len(two["read_twice"]) == 2
    assert two["names"] == {"a place name": 5, "a personal name": 2} and f"| A name (five places, two persons) | {two['gives']['name']} |" in text
    assert f"| A meaning that leaves a Meroitic word as it is | {two['gives']['partly']} |" in text and f"| A meaning in full | {two['gives']['word']} |" in text
    words = {w["entry"]: w for w in two["words"]}
    assert set(words) == {"mse", "kdimdḫe"} and {w["source"] for w in two["words"]} == {"Lipinski 2011"}
    assert f'"{words["mse"]["meaning"]}" for `mse`, and "{words["kdimdḫe"]["meaning"]}" (our wording) for `kdimdḫe`' in text
    assert {e["entry"]: e["kind"] for e in two["by_entry"]}["mse"] == "title" and "The lexicon of 2003 files `mse` as a title" in text
    p = two["the_places"]
    assert f"| Every place answered by both | {p['answered by both']} of {p['places']} | met |" in text and f"| Kappa of 0.6 or more | {p['kappa']:.2f} | met |" in text
    for label, key in (('the word the source speaks of ("stated")', "stated"), ("open", "open"), ("a piece of another word", "piece"),
                       ("unclear", "unclear"), ("not agreed", "not agreed")):
        assert f"| {label} | {p['verdicts'][key]} |" in text, key
    laid, by = two["laid"], two["laid"]["to_by_why"]
    assert f"**What can be laid: {laid['lines']} places.**" in text
    assert f"| A name, of an entry the lexicon files as a place name | {by['stated']['name']} |" in text
    assert f"| A name, of an entry both readers say the source calls a personal name | {by['name']['name']} |" in text
    assert f"| A piece of a word the map holds as a name | {by['piece']['name']} |" in text and set(by["piece"]) == {"name"}
    assert (words["mse"]["places_laid"], words["mse"]["texts"], words["kdimdḫe"]["places_laid"]) == (3, 1, 1)
    assert f"| A translated word (`mse` three times in one text, `kdimdḫe` once) | {laid['to']['meaning']} |" in text
    out = two["left_out"]
    pieces = sum(n for k, n in out.items() if k.startswith("piece"))
    assert (f"**What stays open:** {out['stated, stem, a part of the spelling unnamed']} stated places where the map leaves a part of the spelling unnamed, "
            f"{out[L.LEFT]} where the meaning leaves a Meroitic word as it is, and {pieces} pieces whose whole word the map does not hold or holds open.") in text
    assert len(out) == 4 and out[L.LEFT] == two["gives"]["partly"]              # one place for each of the three entries
    assert (f"{laid['to']['meaning']} running words and {len(words)} words of the dictionary get a meaning, each from one scholar, and "
            f"{laid['to']['name']} places leave the count of words that need one") in text
    r, c = cost["part 2, the readers"], cost["part 2, the checkers"]
    assert (f"Cost: {r['agents'] + c['agents']} agents, {r['tokens'] + c['tokens']:,} tokens ({r['agents']} readers {r['tokens']:,}; "
            f"{c['agents']} checkers {c['tokens']:,}).") in text
    # the map with this layer
    m = json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    mine, before = (x for x in m["layers"] if x["name"] in (L.LAYER, L.BEFORE[-1]))
    before, mine = (before, mine) if mine["name"] == L.LAYER else (mine, before)
    pct = lambda x: f"{100 * x:.1f}%"                                      # noqa: E731
    a, b = mine["after"], before["after"]
    s, s0 = M.star_pct(mine["north_star"]), M.star_pct(before["north_star"])
    assert (f"{a['running']['translated']:,} of the {a['running']['need']:,} running words that need a meaning are translated "
            f"({pct(a['running']['share'])}, from {pct(b['running']['share'])}), {a['spellings']['translated']} of {a['spellings']['need']:,} distinct spellings "
            f"({pct(a['spellings']['share'])}, from {pct(b['spellings']['share'])}) and {mine['north_star']['translated']} of about "
            f"{mine['north_star']['distinct_words']['point']:,} distinct words ({s['point']}, between {s['low']} and {s['high']}, from {s0['point']})") in text


def test_the_second_readings_page_says_what_the_figures_say():
    f, text = figs(), page(PAGE_AGAIN)
    one, a, cost = f["part_1"], f["part_1_again"], f["cost"]["part 1 again, the checkers"]
    w = f["when"][3]
    hm = lambda t: t[:5]                                                   # noqa: E731
    lot, ends, v, laid = a["lot_letters"], a["hidden_endings"], a["verdicts"], a["laid"]
    assert w["step"] == "part 1 again, the unnamed parts"
    assert (f"It is the map's sixth layer, `leftover`: {laid['lines']} places, {laid['to']['meaning']} of them translated words and "
            f"{laid['to']['name']} names.") in text
    # sections 2 and 3: what stays, what changes, the bars
    assert f"**The places:** the same {a['places']} ({a['places_by_run']['g2']} of G2, {a['places_by_run']['g4']} of G4)" in text
    assert f"{a['controls']['ending']} translated words with their endings shown as unnamed" in text
    assert f"{a['controls']['junk']} translated words with three to five letters drawn by lot" in text
    assert f"with the seed {L.SEED_AGAIN}: the {sum(a['controls'].values())} controls" in text
    assert f"**Six fresh checkers** (two for each of {a['packs']} packs, Opus)" in text and cost["agents"] == 6 == 2 * a["packs"]
    most, need = round(L.BARS_AGAIN["junk_called_ending_or_known"] * lot["shown"]), round(L.BARS_AGAIN["endings_called_ending"] * ends["1"]["shown"])
    assert f"each checker calls at most {most} of the {lot['shown']} runs of letters drawn by lot an ending or a known word" in text
    assert f"each checker calls at least {need} of the {ends['1']['shown']} hidden endings an ending" in text
    assert "**A name is no longer laid.**" in text and '**For "a name":** no bar, because nothing rests on it any more.' in text
    assert "If a bar is missed, nothing is taken, and there is no third reading." in text
    # section 4: the first reading's answers would have met these bars
    first = one["lot_letters"]
    assert all(set(first["explained_as"][j]) <= {"name"} for j in "12") and all(e["called_ending"] == e["shown"] for e in one["hidden_endings"].values())
    assert (f"neither checker called a run of lot letters an ending or a known word, and both found all {one['hidden_endings']['1']['shown']} hidden endings") in text
    # section 5: the result
    assert f"## 5. The result (counted at {hm(w['counted'])}, bars met)" in text
    assert (f"The six checkers were started at {hm(w['started'])}, after the commit with the bars ({w['set']}); their answers came between "
            f"{hm(w['first_answer'])} and {hm(w['last_answer'])}.") in text
    assert (f"| Every place answered by both | {a['answered']['1']} of {a['lines_expected']} ({a['places']} places, "
            f"{sum(a['controls'].values())} controls) | met |") in text
    assert f"| Kappa of 0.6 or more on the real places | {a['kappa']:.2f} | met |" in text
    called = [sum(lot["explained_as"][j].get(k, 0) for k in L.LAID) for j in "12"]
    assert f"| Each checker calls at most {most} of {lot['shown']} runs of lot letters an ending or a known word | {called[0]} and {called[1]} | met |" in text
    assert (f"| Each checker calls at least {need} of {ends['1']['shown']} hidden endings an ending | {ends['1']['called_ending']} and "
            f"{ends['2']['called_ending']} | met |") in text
    assert f"| Both checkers say, of the {a['places']} places | Places |" in text and set(v) == {"unknown", "ending", "name", "known", "not agreed"}
    for label, key in (("unknown", "unknown"), ("ending", "ending"), ("a name (not laid)", "name"), ("a known word, the same entry", "known"),
                       ("not agreed", "not agreed")):
        assert f"| {label} | {v[key]} |" in text, key
    assert (f"**What can be laid: {laid['lines']} places.** {laid['to']['meaning']} become translated words and {laid['to']['name']} become names "
            f"(their entry is a name by the lexicon).") in text
    assert a["left_out"] == {L.OTHER_STEM: 1} and "One place both checkers call an ending stays open, because another stem of its spelling has no meaning." in text
    assert f"The {v['name']} places both call a name stay open, as the rule says." in text
    v1 = one["verdicts"]
    for label, x, y in (("Kappa", f"{one['kappa']:.2f}", f"{a['kappa']:.2f}"), ("Both say ending", v1["ending"], v["ending"]), ("Both say unknown", v1["unknown"], v["unknown"]),
                        ("Both say a name", v1["name"], v["name"]), ("Not agreed", v1["not agreed"], v["not agreed"])):
        assert f"| {label} | {x} | {y} |" in text, label
    assert a["kappa"] < one["kappa"] and v["ending"] < v1["ending"] and "The second reading agrees less and gives less, and it is the one that counts." in text
    assert {"word": "t-erike-l", "letters": "before", "answers": ["name", "name"]} in lot["explained_at"]
    assert 'Letters drawn by lot that stood before "begotten of" were again called a name by both checkers' in text
    # the map with this layer, and the two words it is the first to lay
    m = json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    by_name = {x["name"]: x for x in m["layers"]}
    mine, before = by_name[L.LAYER_AGAIN], by_name[L.LAYER]
    pct = lambda x: f"{100 * x:.1f}%"                                      # noqa: E731
    x, b = mine["after"], before["after"]
    s, s0 = M.star_pct(mine["north_star"]), M.star_pct(before["north_star"])
    assert (f"{x['running']['translated']:,} of the {x['running']['need']:,} running words that need a meaning are translated "
            f"({pct(x['running']['share'])}, from {pct(b['running']['share'])}), {x['spellings']['translated']} of {x['spellings']['need']:,} distinct spellings "
            f"({pct(x['spellings']['share'])}, from {pct(b['spellings']['share'])}) and {mine['north_star']['translated']} of about "
            f"{mine['north_star']['distinct_words']['point']:,} distinct words ({s['point']}, between {s['low']} and {s['high']}, from {s0['point']})") in text
    words = {w["entry"]: w for w in a["words"]}
    assert (words["nbr"]["source"], words["yiroẖe"]["source"]) == ("Rilly 2016", "Rilly 2021")
    assert (f"The {len(words)} words of the dictionary that this layer is the first to lay as translated words are `nbr` (\"{words['nbr']['meaning']}\", by Rilly 2016) "
            f"and `yiroẖe` (\"{words['yiroẖe']['meaning']}\", our wording, by Rilly 2021).") in text
    assert f"Cost: {cost['agents']} agents, {cost['tokens']:,} tokens" in text
    assert "`data/sources/g8b/run.py`" not in text and "- `python3 -I src/leftover.py layer-again`" not in text


def test_the_stems_figures_add_up_and_hold_counts_only():
    f = stems()
    assert f["places"] == sum(f["places_by_run"].values()) == sum(f["verdicts"].values()) == f["answered_by_both"]
    assert sum(sum(v.values()) for v in f["verdicts_by_run"].values()) == f["places"]
    assert f["lines_expected"] == f["places"] + sum(f["controls"].values()) == f["answered"]["1"] == f["answered"]["2"]
    assert f["controls"] == dict.fromkeys(f["controls"], L.N_STEMS) and set(f["controls"]) == set(L.KINDS_STEMS)
    ce = f["control_entries"]                                                   # the rule's 20 entries a kind: kept but for the names
    assert {k: ce["entries"][k] for k in ("stem", "ending", "lot")} == dict.fromkeys(("stem", "ending", "lot"), L.N_STEMS)
    personal = L.N_STEMS - ce["names_of_the_lexicon"]["places"]
    assert ce["entries"]["name"] == personal + ce["names_of_the_lexicon"]["entries"] == ce["name_found_counted_once"]["names"] < L.N_STEMS
    once = ce["name_found_counted_once"]
    assert once["bar_met"] == all(n >= L.HIT * once["names"] for n in once["found"].values()) is True
    assert all(once["found"][j] <= f["controls_by_checker"][j]["name"]["called_name"] for j in "12")
    for j in "12":
        c = f["controls_by_checker"][j]
        for kind in L.KINDS_STEMS:
            assert sum(v for k, v in c[kind].items() if k.startswith("called_")) == c[kind]["shown"] == L.N_STEMS, (j, kind)
        assert c["stem_with_its_entry"] <= c["stem"].get("called_known", 0)
    assert f["bars_set"] == {"kappa": L.BARS["kappa"], "found_at_least": L.HIT, "said_wrongly_at_most": L.FALSE, "of": L.N_STEMS}
    assert f["general"]["kappa"] == (f["kappa"] >= L.BARS["kappa"])
    assert f["taken"] == {v: all(f["general"].values()) and all(f["bars"][v].values()) for v in L.VERDICTS}
    # each bar is what the controls say
    c = f["controls_by_checker"]
    found = {"known": lambda x: x["stem_with_its_entry"], "ending": lambda x: x["ending"].get("called_ending", 0), "name": lambda x: x["name"].get("called_name", 0)}
    for v in L.VERDICTS:
        assert f["bars"][v]["found"] == all(found[v](c[j]) >= L.HIT * L.N_STEMS for j in "12"), v
        assert f["bars"][v]["not_said_of_lot_letters"] == all(c[j]["lot"].get(f"called_{v}", 0) <= L.FALSE * L.N_STEMS for j in "12"), v
    assert f["bars"]["name"]["not_said_of_known_stems"] == all(c[j]["stem"].get("called_name", 0) <= L.FALSE * L.N_STEMS for j in "12")
    laid = f["laid"]
    assert laid["lines"] == sum(laid["why"].values()) == sum(laid["to"].values()) == sum(laid["was"].values())
    assert laid["lines"] + sum(f["left_out"].values()) == sum(f["verdicts"].get(v, 0) for v in L.VERDICTS)
    assert set(laid["why"]) <= set(M.WHY) and set(laid["to"]) <= set(W.READ + W.NAMED) and set(laid["was"]) <= set(W.OPEN)
    assert laid["to"].get("name", 0) == laid["why"].get("name", 0) == f["verdicts"].get("name", 0) and f["words"] == []
    s = f["steadiness"]
    assert s["with_one_verdict"] <= s["at_two_places_or_more"] <= s["spellings"] <= f["places"] and sum(s["its_verdicts"].values()) == s["the_most_places"]
    assert f["one_unnamed_part"] <= f["places"]

    def strings(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from strings(v, k)
        elif isinstance(o, list):
            for v in o:
                yield from strings(v, key)
        elif isinstance(o, str):
            yield key, o
    for key, v in strings(f):                                                   # no spelling, no entry, no word of a pack: the step's name and its times
        assert (key == "step" and v == L.WHEN_STEMS["step"]) or (key in ("set_in", "set", "started", "first_answer", "last_answer", "counted")
                                                                   and re.fullmatch(r"[0-9a-f]{7}|\d\d:\d\d:\d\d", v)), (key, v)


def test_the_stems_page_says_what_the_figures_say():
    f, text = stems(), page(PAGE_STEMS)
    v, laid, one, two = f["verdicts"], f["laid"], f["controls_by_checker"]["1"], f["controls_by_checker"]["2"]
    names, grammar = laid["to"]["name"], laid["to"]["grammar"]
    assert f"{laid['lines']} of the {f['places']} places are laid, {names} as names and {grammar} as a word of grammar" in text
    assert "No stem was recognised as a word the lexicon knows." in text and "known" not in v
    assert f"the map's seventh layer, `{L.LAYER_STEMS}`" in text and "`leftover_stems_figures.json`" in text and "`src/leftover.py`" in text
    assert f"the {f['places']} places of [the rare spellings](rare_spellings.md)" in text
    assert f"({f['places_by_run']['g2']} of G2, {f['places_by_run']['g4']} of G4), on the map with its six layers" in text and len(L.BEFORE_STEMS) == 6
    controls = sum(f["controls"].values())
    assert f"**Controls: {controls} places of known answer,** {L.N_STEMS} of each kind" in text
    assert f"Each kind takes {L.N_STEMS} different entries of the lexicon" in text
    assert f"two for each of {f['packs']} packs ({f['lines_expected']} places), each a fresh agent (Opus): {2 * f['packs']}. Seed {L.SEED_STEMS}." in text
    hit, false = round(L.HIT * L.N_STEMS), round(L.FALSE * L.N_STEMS)
    assert (f"| Verdict | It is found (each checker, at least {hit} of {L.N_STEMS}) | It is not said wrongly (each checker, at most {false} of "
            f"{L.N_STEMS}) |") in text
    assert f"| Verdict | Found (at least {hit} of {L.N_STEMS}) | Said wrongly (at most {false} of {L.N_STEMS}) | |" in text
    assert f"Cohen's kappa of the two checkers over the five cases, on the real places, is {L.BARS['kappa']} or more." in text
    assert f"| Every place answered by both | {f['lines_expected']} of {f['lines_expected']} ({f['places']} places, {controls} controls) | met |" in text
    assert f"| Kappa of 0.6 or more on the real places | {f['kappa']:.2f} | met |" in text and all(f["taken"].values())
    lot = lambda x, case: x["lot"].get(f"called_{case}", 0)                     # noqa: E731
    assert (f"| A known word | {one['stem_with_its_entry']} and {two['stem_with_its_entry']} hidden stems named with their entry | "
            f"{lot(one, 'known')} and {lot(two, 'known')} runs of lot letters called a known word | met |") in text
    assert (f"| Ending | {one['ending']['called_ending']} and {two['ending']['called_ending']} | {lot(one, 'ending')} and {lot(two, 'ending')} runs of lot "
            f"letters called ending | met |") in text
    assert (f"| A name | {one['name']['called_name']} and {two['name']['called_name']} | {lot(one, 'name')} and {lot(two, 'name')} runs of lot letters, and "
            f"{one['stem'].get('called_name', 0)} and {two['stem'].get('called_name', 0)} hidden stems, called a name | met |") in text
    for label, key in (("unknown", "unknown"), ("a name", "name"), ("ending", "ending"), ("a known word", "known"), ("not agreed", "not agreed")):
        assert f"| {label} | {v.get(key, 0)} |" in text, label
    assert set(v) <= {"unknown", "name", "ending", "known", "not agreed"}
    assert f"**What can be laid: {laid['lines']} places,** {names} as names and {grammar} as a word of grammar" in text
    assert f["left_out"] == {} and "No place is left out for a second unnamed part or for another stem without a meaning." in text
    assert (f"though both found such stems where they were hidden ({one['stem_with_its_entry']} and {two['stem_with_its_entry']} of "
            f"{L.N_STEMS})") in text
    s = f["steadiness"]
    assert (s["the_most_places"], s["its_verdicts"]) == (5, {"name": 2, "not agreed": 2, "unknown": 1})
    assert "One spelling stands at five places of one text: the two checkers call it a name at two, differ at two, and call it unknown at one." in text
    assert f"Cost: {f['cost']['agents']} agents, {f['cost']['tokens']:,} tokens" in text and f["cost"]["agents"] == 2 * f["packs"]
    w = f["when"]
    assert (f"The eight checkers were started at {w['started'][:5]}, after the commit with the bars ({w['set']}); their answers came between "
            f"{w['first_answer'][:5]} and {w['last_answer'][:5]}.") in text and f"counted at {w['counted'][:5]}" in text
    # the map with this layer: the shares divided from the counts
    m = json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    by_name = {x["name"]: x for x in m["layers"]}
    mine, before = by_name[L.LAYER_STEMS], by_name[L.LAYER_AGAIN]
    of = lambda x: f"{100 * x['translated'] / x['need']:.1f}%"                  # noqa: E731
    a, b = mine["after"], before["after"]
    star, star0 = M.star_pct(mine["north_star"]), M.star_pct(before["north_star"])
    assert (f"{a['running']['translated']:,} of the {a['running']['need']:,} running words that need a meaning are translated "
            f"({of(a['running'])}, from {of(b['running'])}), {a['spellings']['translated']} of {a['spellings']['need']:,} distinct spellings "
            f"({of(a['spellings'])}, from {of(b['spellings'])}) and {mine['north_star']['translated']} of about "
            f"{mine['north_star']['distinct_words']['point']:,} distinct words ({star['point']}, between {star['low']} and {star['high']}, from "
            f"{star0['point']})") in text
    gone = before["north_star"]["unnamed_stems"]["now"] - mine["north_star"]["unnamed_stems"]["now"]
    assert (f"the {names} names leave the count of words that need a meaning, and {gone} of the stems the map could not name is now a name") in text
    assert b["running"]["need"] - a["running"]["need"] == names and mine["north_star"]["translated"] == before["north_star"]["translated"]
    assert "`data/sources/g9/run.py`" not in text and "- `python3 -I src/leftover.py layer-stems`" not in text
    # the review's two corrections of sections 2 and 3, which stand as they were written before the checkers
    ce = f["control_entries"]
    lex_names, once = ce["names_of_the_lexicon"], ce["name_found_counted_once"]
    assert (f"they are the {L.N_STEMS - lex_names['places']} personal names the map holds and {lex_names['places']} places of {lex_names['entries']} "
            f"names of the lexicon, drawn by place, so that four names stand twice. Counted once each, the {once['names']} names were found by each "
            f"checker {once['found']['1']} and {once['found']['2']} times, which still meets the bar of 70%.") in text and once["bar_met"]
    assert lex_names["places"] - lex_names["entries"] == 4 and round(100 * L.HIT) == 70
    assert ('"A word of grammar when both call every unnamed part an ending: the spelling is then endings or particles only." At the one place '
            'laid so it is not') in text and laid["to"] == {"name": names, "grammar": 1}
    for cmd in ("packs-stems", "count-stems", "layer-stems", "public"):
        assert f"python3 -I src/leftover.py {cmd}" in PAGE_STEMS.read_text(encoding="utf-8") and cmd in L.COMMANDS, cmd
    # the two earlier pages of the step point here
    for path in (PAGE, PAGE_AGAIN):
        assert "[leftover_stems.md](leftover_stems.md)" in path.read_text(encoding="utf-8"), path.name
    assert (f"{laid['lines']} of them are laid, {names} as names and {grammar} as a word of grammar, the map's seventh layer; no stem was recognised as a "
            f"word the lexicon knows") in page()


def test_the_summaries_name_the_step():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python3 -I tests/test_leftover.py" in readme and "- `python3 -I src/leftover.py public`" in readme
    f = figs()
    laid, again = f["part_2"]["laid"], f["part_1_again"]["laid"]
    for name in ("README.md", "NEXT_STEPS.md", "REPORT.md"):
        text = " ".join((ROOT / name).read_text(encoding="utf-8").split())
        assert "leftover_parts.md" in text and "leftover_parts_2.md" in text, name
        assert f"{laid['lines']} places" in text and f"{laid['to']['name']} of them as names and {laid['to']['meaning']} as translated words" in text, name
        assert "The first reading of the unnamed parts is not taken" in text, name
        assert f"{again['lines']} places, {again['to']['meaning']} of them as translated words and {again['to']['name']} as names" in text, name
    index = (ROOT / "data/INDEX.md").read_text(encoding="utf-8")
    assert "`data/sources/g8/`" in index and "`data/sources/g8b/`" in index and "`data/sources/rare/`" in index
    # part 3, and the map as it stands with its layer
    s, m = stems(), json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    of = lambda x: f"{100 * x['translated'] / x['need']:.1f}%"                  # noqa: E731
    r, sp, n, star = m["current"]["running"], m["current"]["spellings"], m["north_star"], M.star_pct(m["north_star"])
    stands = (f"{r['translated']:,} of the {r['need']:,} running words that need a meaning are translated ({of(r)}), {sp['translated']} of "
              f"{sp['need']:,} distinct spellings ({of(sp)}) and {n['translated']} of about {n['distinct_words']['point']:,} distinct words "
              f"({star['point']}, between {star['low']} and {star['high']})")
    for name in ("README.md", "NEXT_STEPS.md", "REPORT.md"):
        text = " ".join((ROOT / name).read_text(encoding="utf-8").split())
        assert "leftover_stems.md" in text and (name == "NEXT_STEPS.md" or '"run it and document everything in our doc"' in text), name
        assert (f"The map's seventh layer lays {s['laid']['lines']} places, {s['laid']['to']['name']} of them as names and {s['laid']['to']['grammar']} as a "
                f"translated word") in text, name
        assert f"The map as it stands: {stands}" in text, name
    assert "`data/sources/g9/`" in index and "`packs-stems`, `count-stems`, `layer-stems`" in readme


# ------------------------------------------------------------------------------------------- with the local files

LOCAL = ("data/sources/g8/result.json", "data/sources/g8/key.json", "data/sources/g8b/result.json", "data/sources/g8b/key.json",
         "data/sources/g8b/overlay.jsonl", "data/sources/rare/g4m/places/result.json", "data/sources/rare/g4m/overlay.jsonl",
         "data/sources/v6/analysts/glosses.jsonl", "data/rilly2003")


def test_the_figures_are_the_count_of_the_local_files():
    needs(*LOCAL)
    assert L.figures() == figs()


def test_the_layer_is_what_the_script_builds():
    needs(*LOCAL)
    _, _, _, lines, _ = L.build()
    assert lines == M.lines_of({l["name"]: l for l in M.LAYERS}[L.LAYER])
    gl = L.before()
    assert all(gl[o["text"]][o["n"] - 1]["level"] == o["was"] and "layer" not in gl[o["text"]][o["n"] - 1] for o in lines)
    again, apart, _ = L.build_again()                                           # the second reading of part 1, on the same map
    assert again == M.lines_of({l["name"]: l for l in M.LAYERS}[L.LAYER_AGAIN]) and apart == figs()["part_1_again"]["left_out"]
    assert all(gl[o["text"]][o["n"] - 1]["level"] == o["was"] and "layer" not in gl[o["text"]][o["n"] - 1] for o in again)
    assert not {(o["text"], o["n"]) for o in again} & {(o["text"], o["n"]) for o in lines}
    res = L.read("result.json", L.HOME_AGAIN)                                   # no place both checkers call a name is among the lines
    named = {(r["text"], r["n"]) for r in res["rows"] if r["verdict"] == "name"}
    assert named and not named & {(o["text"], o["n"]) for o in again}


def test_the_script_writes_the_packs_the_checkers_were_given():
    """Each reading of part 1 again in a folder of its own, the checkers' answers copied in afterwards: the key and
    the packs of the run (but for the folder the brief names), and its result. The two readings have the same
    places and other controls."""
    needs(*LOCAL, *[f"data/sources/{g}/{x}" for g in ("g8", "g8b") for x in ("packs", "answers1", "answers2")])
    for again, live in ((False, L.HOME), (True, L.HOME_AGAIN)):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            quiet(L.packs, d, again)
            assert L.read("key.json", d) == L.read("key.json", live) and L.read("groups.json", d) == L.read("groups.json", live), again
            names = sorted(p.name for p in (live / "packs").iterdir())
            assert names == sorted(p.name for p in (d / "packs").iterdir()) and len(names) == 6
            for n in names:
                mine = (d / "packs" / n).read_text(encoding="utf-8").replace(str(d), str(live.relative_to(ROOT)))
                assert mine == (live / "packs" / n).read_text(encoding="utf-8"), (again, n)
            assert stops(lambda: L.packs(live, again), "answers exist: the packs are not written again")
            for c in (1, 2):
                shutil.copytree(live / f"answers{c}", d / f"answers{c}", dirs_exist_ok=True)
                assert all(filecmp.cmp(live / f"answers{c}" / p.name, p, shallow=False) for p in (d / f"answers{c}").iterdir())
            quiet(L.count, d, again)
            assert L.read("result.json", d) == L.read("result.json", live), again
    one, two = L.read("key.json"), L.read("key.json", L.HOME_AGAIN)
    real = lambda key: sorted((p["run"], p["entry"], p["text"], p["i"]) for p in key if p["control"] is None)     # noqa: E731
    ctrl = lambda key: sorted((p["control"], p["text"], p["i"], p.get("junk", "")) for p in key if p["control"])  # noqa: E731
    assert real(one) == real(two) and ctrl(one) != ctrl(two) and [p["place"] for p in one] == [p["place"] for p in two]
    assert [p["control"] for p in one] != [p["control"] for p in two]           # dealt anew


def test_part_2_writes_its_packs_and_results_again():
    """Part 2 again in a folder of its own, the agents' answers copied in after each set of packs is written: the
    entries, the packs of the readers and of the checkers byte for byte, both results, and the layer's lines."""
    needs(*LOCAL, "data/sources/rare/g4m/lit/verify/packs", "data/sources/rare/g4m/places/packs", "data/sources/rare/g4/items.json")
    live, out, brief = R.HOME, W.OUT, W.VERIFY_BRIEF
    mine = live / L.RUN

    def same(*names):
        for name in names:
            assert json.loads((L.HOME2 / name).read_text(encoding="utf-8")) == json.loads((mine / name).read_text(encoding="utf-8")), name

    def same_packs(folder, n):
        names = sorted(p.name for p in (mine / folder / "packs").iterdir())
        assert len(names) == n and names == sorted(p.name for p in (L.HOME2 / folder / "packs").iterdir()), folder
        assert all(filecmp.cmp(L.HOME2 / folder / "packs" / x, mine / folder / "packs" / x, shallow=False) for x in names), folder

    def answers(folder):
        for c in (1, 2):
            shutil.copytree(mine / folder / f"answers{c}", L.HOME2 / folder / f"answers{c}", dirs_exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "g4").symlink_to(live / "g4")
        R.HOME, L.HOME2 = d, d / L.RUN
        try:
            quiet(L.setup)
            quiet(L.verify_packs)
            assert W.VERIFY_BRIEF == brief                                      # the brief of G4 is as it was
            same("items.json", "lit/checked.json", "lit/classes.json", "lit/verify/groups.json")
            same_packs("lit/verify", 4)
            answers("lit/verify")
            assert stops(L.setup, "hold answers: not written again") and stops(L.verify_packs, "hold answers: not written again")
            quiet(L.verify)
            same("lit/verify/result.json")
            quiet(L.place_packs)
            same("places/groups.json")
            same_packs("places", 4)
            answers("places")
            assert stops(L.place_packs, "hold answers: not written again")
            quiet(L.places)
            same("places/result.json")
            lines = L.build()[3]
            assert lines == [json.loads(l) for l in (mine / "overlay.jsonl").read_text(encoding="utf-8").splitlines()]
        finally:
            R.HOME, L.HOME2, W.OUT = live, mine, out
    assert sorted(it["item"] for it in L.picked()[0]) == sorted(e["entry"] for e in figs()["part_2"]["by_entry"])


LOCAL_STEMS = ("data/sources/g9/result.json", "data/sources/g9/key.json", "data/sources/g9/overlay.jsonl", "data/sources/g9/tokens.json",
               "data/sources/g8b/overlay.jsonl", "data/sources/rare/g4m/overlay.jsonl", "data/sources/v6/analysts/glosses.jsonl", "data/rilly2003")


def test_the_stems_figures_are_the_count_of_the_local_files():
    needs(*LOCAL_STEMS)
    assert L.figures_stems() == stems()
    assert stems()["cost"] == {"agents": 8, "tokens": sum(json.loads(L.TOKENS_STEMS.read_text(encoding="utf-8"))["checkers"].values())}


def test_the_stems_layer_is_what_the_script_builds():
    needs(*LOCAL_STEMS)
    lines, apart = L.build_stems()
    assert lines == M.lines_of(M.LAYERS[-1]) and M.LAYERS[-1]["name"] == L.LAYER_STEMS and apart == stems()["left_out"]
    gl = L.before_stems()                                                       # the map with the six layers before it: every place open and not yet laid
    assert all(gl[o["text"]][o["n"] - 1]["level"] == o["was"] and "layer" not in gl[o["text"]][o["n"] - 1] for o in lines)
    mine = {(o["text"], o["n"]) for o in lines}
    assert len(mine) == len(lines) and not any(mine & {(o["text"], o["n"]) for o in M.lines_of(l)} for l in M.LAYERS[:-1])
    res = L.read("result.json", L.HOME_STEMS)                                   # only the places of a verdict whose bars are met, and all of them
    by = {(r["text"], r["n"]): r["verdict"] for r in res["rows"]}
    assert all(res["taken"].values()) and {k for k, v in by.items() if v in L.VERDICTS} == mine
    assert all((o["level"] == "name") == (by[o["text"], o["n"]] == "name") for o in lines)
    # the places are those of G2 and G4 that part 1 was not given: none of its places is among them
    for home in (L.HOME, L.HOME_AGAIN):
        assert not {(p["text"], p["i"]) for p in L.read("key.json", home) if p["control"] is None} & {(t, n - 1) for t, n in by}, home.name
    # the page's review: the one place laid as a word of grammar holds a verb stem the lexicon writes with hyphens
    import words as D
    lex = W.lexicon()
    stems_written_as_affixes = [[p["entry"] for p in gl[o["text"]][o["n"] - 1]["parts"] if p.get("entry") in lex and W.affix(p["entry"])
                                 and not D.ending(p["entry"], lex)] for o in lines if o["level"] == "grammar"]
    assert stems_written_as_affixes == [["-erike-"]] and lex["-erike-"]["kind"] == "verb"


def test_the_script_writes_the_stems_packs_again():
    """Part 3 again in a folder of its own, the checkers' answers copied in afterwards: the key and the packs of the
    run (but for the folder the brief names), its result and its lines. The controls: 20 of each kind, each kind
    from 20 different entries, no word twice, none of them a real place."""
    needs(*LOCAL_STEMS, *[f"data/sources/g9/{x}" for x in ("packs", "answers1", "answers2")])
    live = L.HOME_STEMS
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        quiet(L.packs_stems, d)
        assert L.read("key.json", d) == L.read("key.json", live) and L.read("groups.json", d) == L.read("groups.json", live)
        names = sorted(p.name for p in (live / "packs").iterdir())
        assert names == sorted(p.name for p in (d / "packs").iterdir()) and len(names) == 8
        for n in names:
            mine = (d / "packs" / n).read_text(encoding="utf-8").replace(str(d), str(live.relative_to(ROOT)))
            assert mine == (live / "packs" / n).read_text(encoding="utf-8"), n
            assert mine.startswith(L.BRIEF.split("{places}")[0])                # the brief of the leftover parts, word for word
        assert stops(lambda: L.packs_stems(live), "answers exist: the packs are not written again")
        for c in (1, 2):
            shutil.copytree(live / f"answers{c}", d / f"answers{c}", dirs_exist_ok=True)
        quiet(L.count_stems, d)
        assert (d / "result.json").read_bytes() == (live / "result.json").read_bytes()
        quiet(L.layer_stems, d)
        assert (d / "overlay.jsonl").read_bytes() == (live / "overlay.jsonl").read_bytes()
    key, gl = L.read("key.json", live), L.before_stems()
    ctrl = [p for p in key if p["control"]]
    assert collections.Counter(p["control"] for p in ctrl) == dict.fromkeys(L.KINDS_STEMS, L.N_STEMS)
    assert len({(p["text"], p["i"]) for p in key}) == len(key) == stems()["lines_expected"]

    def stem(p):
        return next(x for x in gl[p["text"]][p["i"]]["parts"] if x.get("entry") == "NAME" or not W.affix(x["entry"]))
    for kind in ("stem", "ending", "lot"):
        assert len({stem(p)["entry"] for p in ctrl if p["control"] == kind}) == L.N_STEMS, kind
    assert all(p["answer_entry"] == stem(p)["entry"] and len(stem(p)["form"]) >= 3 for p in ctrl if p["control"] == "stem")
    assert all(len(p["junk"]) == max(3, len(stem(p)["form"])) and p["form"] != gl[p["text"]][p["i"]]["form"] for p in ctrl if p["control"] == "lot")
    assert sum(any(x.get("entry") == "NAME" for x in gl[p["text"]][p["i"]]["parts"]) for p in ctrl if p["control"] == "name") == 9
    # every real place hangs on an ending or a particle that both checkers of G2 or G4 had recognised, and its stem is unnamed
    assert all(W.affix(p["entry"]) and any(e is None for _, e in p["parts"]) for p in key if p["control"] is None)


def test_the_stems_rules_were_in_git_before_the_checkers_were_started():
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout
    w = L.WHEN_STEMS
    assert git("log", "-1", "--format=%cI", w["set_in"]).strip() == f"2026-11-16T{w['set']}-08:00"
    assert w["set"] < w["started"] < w["first_answer"] <= w["last_answer"] < w["counted"]
    for phrase in ("## 3. The bars, set before any checker is started", "**Each verdict then stands on its own bars.**",
                   "| A name | the names called a name | the letters by lot called a name; the hidden stems called a name |",
                   "- **a name** when both call it a name and the spelling has one unnamed part;",
                   "If bar 1 or 2 is missed, nothing is taken, and the step stops until Mike has seen why."):
        out = git("log", "--reverse", "--format=%cI", f"-S{phrase}", "--", str(PAGE_STEMS.relative_to(ROOT))).split()
        assert out and out[0][11:19] <= w["set"], phrase
        assert phrase in PAGE_STEMS.read_text(encoding="utf-8"), phrase
    prompt = (ROOT / "runs/prompts/G9_stems.md").read_text(encoding="utf-8")
    assert "The brief of the leftover parts, in [`G8_parts.md`](G8_parts.md), word for word." in prompt and "data/sources/g9/packs/P<nn>_c<1|2>.md" in prompt


def test_the_times_of_the_stems_answers_are_the_files():
    needs("data/sources/g9/answers1", "data/sources/g9/answers2")
    import datetime
    import zoneinfo
    pacific = zoneinfo.ZoneInfo("America/Los_Angeles")
    w = L.WHEN_STEMS
    times = sorted(datetime.datetime.fromtimestamp(f.stat().st_mtime, pacific).strftime("%H:%M:%S")
                   for a in w["answers"] for f in (ROOT / "data/sources" / a).glob("*.jsonl"))
    assert len(times) == 8 and (times[0], times[-1]) == (w["first_answer"], w["last_answer"]), (times[0], times[-1])


def test_each_rule_was_in_git_before_its_agents_were_started():
    """Each step's commit is git's, at its time; its agents were started after it, answered after that and were
    counted after their last answer; the bars and the rule the page names stand in those commits."""
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout
    for w in L.WHEN:
        assert git("log", "-1", "--format=%cI", w["set_in"]).strip() == f"2026-11-16T{w['set']}-08:00", w["step"]
        assert w["set"] < w["started"] < w["first_answer"] <= w["last_answer"] < w["counted"], w["step"]
    for phrase, w, path in (("## 3. Part 1: the bars, set before any checker is started", L.WHEN[0], PAGE),
                            ("Each checker explains (as an ending, a known word or a name) at most 10% of the letters drawn by lot", L.WHEN[0], PAGE),
                            ("**Added on 2026-11-16 at 15:35, before any reader of part 2 was started.**", L.WHEN[1], PAGE),
                            ("**A translated word** only when both readers say the source gives a meaning in full.", L.WHEN[1], PAGE),
                            ("## 3. The bars, set before any checker is started", L.WHEN[3], PAGE_AGAIN),
                            ("each checker calls at most 2 of the 20 runs of letters drawn by lot an", L.WHEN[3], PAGE_AGAIN),
                            ("- **A name is no longer laid.**", L.WHEN[3], PAGE_AGAIN),
                            ("6. If a bar is missed, nothing is taken, and there is no third reading.", L.WHEN[3], PAGE_AGAIN)):
        out = git("log", "--reverse", "--format=%cI", f"-S{phrase}", "--", str(path.relative_to(ROOT))).split()
        assert out and out[0][11:19] <= w["set"], phrase
        assert phrase in path.read_text(encoding="utf-8"), phrase


def test_the_times_of_the_answers_are_the_files():
    """WHEN's first and last answer of each step are the times of the agents' answer files (Pacific time)."""
    needs("data/sources/g8/answers1", "data/sources/g8b/answers1", "data/sources/rare/g4m/places/answers1", "data/sources/rare/g4m/lit/verify/answers1")
    import datetime
    import zoneinfo
    pacific = zoneinfo.ZoneInfo("America/Los_Angeles")
    for w in L.WHEN:
        times = sorted(datetime.datetime.fromtimestamp(f.stat().st_mtime, pacific).strftime("%H:%M:%S")
                       for a in w["answers"] for f in (ROOT / "data/sources" / a).glob("*.jsonl"))
        assert times and (times[0], times[-1]) == (w["first_answer"], w["last_answer"]), (w["step"], times[0], times[-1])


def test_no_meaning_of_ours_follows_a_source_for_four_words():
    needs("data/rilly2003", "data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt", "data/sources/jssea-text/pages.txt",
          "data/sources/lipinski2011-text/pages.txt")
    import lexicon as X
    import lexique as Q

    def runs(text):
        w = X.words_of(re.sub(r"ffi|ffl|ff|fi|fl|\x00", "ꜰ", text.lower()))
        return {tuple(w[i: i + X.COPIED]) for i in range(len(w) - X.COPIED + 1)}
    grams = set()
    for e in Q.load():
        for t in [v for v in e.values() if isinstance(v, str)] + [p.get("proposal") or "" for p in e.get("proposals") or []]:
            grams |= runs(t)
    for path in ("data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt", "data/sources/jssea-text/pages.txt",
                 "data/sources/lipinski2011-text/pages.txt"):
        text = re.sub(r"(?m)^\f?=== page \d+ ===$", " ", (ROOT / path).read_text(encoding="utf-8", errors="replace"))
        grams |= runs(text) | runs(re.sub(r"(?<=[^\W\d_])-[ \t]*\n\s*(?=[^\W\d_])", "", text))
    assert [m for m in [*L.MEANINGS.values(), *L.MEANINGS_AGAIN.values()] if runs(m) & grams] == []


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
