"""Checks for the open spellings the lexicon does not hold (src/unnamed.py, data/discovery/unnamed_spellings.md).

  python3 -I tests/test_unnamed.py

The map, the lexicon and the checkers' answers are local only: the checks of the method run on made-up words; the
checks of the reported numbers read the public figures file, compare the page with it, and compare it with a count
from the local files where those are present.
"""
import filecmp
import io
import contextlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import recurring as W                # noqa: E402
import themap as M                   # noqa: E402
import unnamed as U                  # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/unnamed_spellings.md"
LEX = {"ato": {"kind": "noun", "status": "established"}, "-lowi": {"kind": "function word", "status": "established"},
       "qo": {"kind": "function word", "status": "established"}}


def word(form, level, *parts, gloss=""):
    return {"form": form, "level": level, "gloss": gloss, "parts": [{"form": f, "entry": e} for f, e in parts]}


def figs():
    return json.loads(U.PUBLIC.read_text(encoding="utf-8"))


def page():
    return " ".join(PAGE.read_text(encoding="utf-8").split())


def pct(x):
    return f"{100 * x:.1f}%"


def stops(fn, part):
    try:
        fn()
    except SystemExit as e:
        assert part in str(e), e
        return True
    raise AssertionError("did not stop")


def made_up():
    return {"T1": [word("ato", "meaning", ("ato", "ato"), gloss="water"), word("zzk", "unknown", ("zzk", "?")), word("lowi", "grammar", ("lowi", "-lowi")),
                   word("Tneyi", "name", ("Tneyi", "NAME")), word("mmr", "hypothesis", ("mmr", "?")), word("atolowi", "meaning", ("ato", "ato"), ("lowi", "-lowi"))],
            "T2": [word("zzk", "hypothesis", ("zzk", "?")), word("atoqq", "hypothesis", ("ato", "ato"), ("qq", "?")), word("wo", "kind", ("wo", "?")),
                   word("woSi", "name", ("woSi", "NAME"), gloss="Isis")],
            "T3": [word("ppp", "unknown", ("ppp", "?")), word("ppp", "meaning", ("ppp", "?"))] + [word("ato", "meaning", ("ato", "ato"))] * 2}


# ---------------------------------------------------------------------------------------------------- the places

def test_the_places_are_the_open_ones_of_rare_spellings_the_lexicon_does_not_hold():
    gl = made_up()
    gl["T4"], gl["T5"] = [word("mmr", "hypothesis", ("mmr", "?"))], [word("mmr", "hypothesis", ("mmr", "?"))]      # mmr stands in three texts
    # zzk twice, wo, and the open place of ppp (as often open as translated: the level it has first counts); not
    # atoqq, which hangs on an entry of the lexicon, nor mmr, which stands in three texts
    assert U.population(gl, LEX) == [("T1", 2), ("T2", 1), ("T2", 3), ("T3", 1)]


def test_a_place_is_shown_with_its_neighbours_and_the_word_judged_as_unknown():
    gl = made_up()
    p = U.shown(gl["T1"], 4, {4}, {"T1": {"kind": "funerary", "site": "Karanog: grave 12"}}, "T1")
    assert (p["text"], p["n"], p["of"], p["form"], p["kind"], p["site"]) == ("T1", 5, 6, "mmr", "funerary", "Karanog")
    assert p["words"] == "ato zzk lowi Tneyi **mmr** atolowi" and "[mmr: ?]" in p["readings"] and p["readings"].count(" · ") == 5
    assert U.shown(gl["T1"], 0, {0, 1}, {}, "T1")["readings"].startswith("[ato: ?] · [zzk: ?] · ")       # a hidden neighbour looks the same


def test_a_cut_control_shows_two_unknown_halves():
    gl = made_up()
    c = {"control": "cut", "text": "T1", "i": 5, "answer": "piece", "whole": "atolowi", "at": 3, "half": 1}
    p = U.place_of(c, gl, {})
    assert p["words"].endswith("mmr ato **lowi**") and p["readings"].endswith("[ato: ?] · [lowi: ?]") and (p["form"], p["n"], p["of"]) == ("lowi", 7, 7)
    assert len(gl["T1"]) == 6                                             # the map itself is not cut
    assert U.right(c, {"case": "piece", "whole": "ato lowi"}) and not U.right(c, {"case": "piece", "whole": "atolo"}) and not U.right(c, {"case": "word"})
    assert U.right({"control": "name", "answer": "name"}, {"case": "name"}) and not U.right({"control": "word", "answer": "word"}, {"case": "name"})


def test_the_script_finds_the_joins_that_give_a_spelling_the_map_holds():
    gl = made_up()
    good = U.holds(gl)
    assert {"ato", "lowi", "atolowi", "woSi", "Tneyi"} <= good and "zzk" not in good and "wo" not in good
    assert U.joins(gl, "T2", 2, good) == [] and U.joins({"T": [word("wo", "kind"), word("Si", "kind")]}, "T", 0, good) == ["woSi"]
    three = {"T": [word("a", "kind"), word("to", "kind"), word("lowi", "grammar")]}
    # with the word before, with the word after, with both: in that order, only those the map holds
    assert U.joins(three, "T", 1, good) == ["ato", "atolowi"] and U.joins(three, "T", 0, good) == ["ato"] and U.joins(three, "T", 2, good) == []


def test_the_second_controls_are_content_words_names_and_particles():
    gl = made_up()
    got = U.controls2(gl, LEX, random.Random(1), {"T1"}, {"word": 2, "name": 1, "particle": 1})
    kinds = {c["control"]: {gl[c["text"]][c["i"]]["form"] for c in got if c["control"] == k} for k in ("word", "name", "particle") for c in got if c["control"] == k}
    assert kinds == {"word": {"ato", "atolowi"}, "name": {"Tneyi"}, "particle": {"lowi"}}          # from the texts of the real places where enough
    assert [c["answer"] for c in got] == ["word", "word", "name", "piece"] and not any("layer" in gl[c["text"]][c["i"]] for c in got)


# ---------------------------------------------------------------------------------------------------- the counts

def answers(cases):
    return {f"Q{i:04d}": ({"case": c[0], "whole": c[1]} if isinstance(c, tuple) else {"case": c}) for i, c in enumerate(cases, 1)}


def test_a_place_has_a_verdict_only_when_both_checkers_agree():
    v = U.verdict
    assert v({"case": "name"}, {"case": "name"}) == "name" and v({"case": "name"}, {"case": "word"}) == "not agreed" and v({"case": "word"}, None) == "not answered by both"
    assert v({"case": "piece", "whole": "woSi"}, {"case": "piece", "whole": "wo Si"}) == "piece"
    assert v({"case": "piece", "whole": "woSi"}, {"case": "piece", "whole": "woS"}) == "piece, the wholes differ"


def test_the_bars_of_the_first_and_of_the_later_readings():
    key = [{"place": f"Q{i:04d}", "control": None, "text": "T", "n": i, "form": f"f{i}"} for i in range(1, 7)]
    key += [{"place": f"Q{i:04d}", "control": "word", "answer": "word", "text": "T", "n": i, "form": "w"} for i in range(7, 17)]
    key += [{"place": f"Q{i:04d}", "control": "name", "answer": "name", "text": "T", "n": i, "form": "n"} for i in range(17, 27)]
    real = ["name", "name", "word", "word", ("piece", "woSi"), "unclear"]
    one = answers(real + ["word"] * 9 + ["piece"] + ["name"] * 7 + ["word"] * 3)
    two = answers(real + ["word"] * 9 + ["name"] + ["name"] * 8 + ["word"] * 2)
    res = U.result_of(key, one, two, second=True)
    assert res["kappa"] == 1.0 and res["verdicts"] == {"name": 2, "word": 2, "piece": 1, "unclear": 1} and res["places"] == res["answered_by_both"] == 6
    assert res["controls"]["1"]["word"] == {"shown": 10, "right": 9, "called_piece": 1, "called_word": 9}
    assert res["bars"] == {"every_place_answered_by_both": True, "kappa": True, "names_called_name": True, "words_called_name": True} and res["taken"]
    assert [r["whole"] for r in res["rows"]] == ["", "", "", "", "woSi", ""]
    # one checker calls two of ten known words a name: over the bar of a tenth
    two2 = answers(real + ["word"] * 8 + ["name"] * 2 + ["name"] * 8 + ["word"] * 2)
    assert not U.result_of(key, one, two2, second=True)["bars"]["words_called_name"]
    # too few names found; a place one checker did not answer
    low = answers(real + ["word"] * 10 + ["name"] * 6 + ["word"] * 4)
    assert not U.result_of(key, one, low, second=True)["bars"]["names_called_name"]
    short = {k: v for k, v in two.items() if k != "Q0003"}
    r = U.result_of(key, one, short, second=True)
    assert not r["bars"]["every_place_answered_by_both"] and not r["taken"] and r["verdicts"]["not answered by both"] == 1
    # the first pilot's bars count a known word called a piece too, and need the cut spellings found
    cuts = [{"place": f"Q{i:04d}", "control": "cut", "answer": "piece", "whole": "atolowi", "text": "T", "n": i, "form": "ato"} for i in range(27, 37)]
    ok = answers(real + ["word"] * 10 + ["name"] * 10 + [("piece", "atolowi")] * 7 + ["word"] * 3)
    first = U.result_of(key + cuts, ok, ok, second=False)
    assert first["bars"]["cuts_called_piece_of_the_whole"] and first["bars"]["words_called_name_or_piece"] and first["taken"]
    bad = answers(real + ["word"] * 9 + ["piece"] + ["name"] * 10 + [("piece", "atolowi")] * 6 + [("piece", "ato")] + ["word"] * 3)
    b = U.result_of(key + cuts, bad, bad, second=False)["bars"]
    assert not b["cuts_called_piece_of_the_whole"] and b["words_called_name_or_piece"]              # one of ten is the bar
    assert U.BARS == {"kappa": 0.6, "words_called_name_or_piece": 0.10, "names_called_name": 0.70, "cuts_called_piece_of_the_whole": 0.70}
    assert U.BARS2 == {"kappa": 0.6, "words_called_name": 0.10, "names_called_name": 0.70}


def test_only_names_and_pieces_of_words_the_map_holds_are_laid():
    gl = made_up()
    rs = [{"text": "T1", "n": 2, "form": "zzk", "verdict": "name", "whole": ""}, {"text": "T2", "n": 3, "form": "wo", "verdict": "piece", "whole": "woSi"},
          {"text": "T1", "n": 5, "form": "mmr", "verdict": "piece", "whole": "mmrzz"}, {"text": "T2", "n": 1, "form": "zzk", "verdict": "piece", "whole": "atoqq"},
          {"text": "T3", "n": 1, "form": "ppp", "verdict": "word", "whole": ""}, {"text": "T2", "n": 2, "form": "atoqq", "verdict": "not agreed", "whole": ""}]
    lines, apart = U.lines_of(gl, rs)
    assert [(o["form"], o["level"], o["why"], o["was"]) for o in lines] == [("zzk", "name", "name", "unknown"), ("wo", "name", "piece", "kind")]
    assert lines[1]["gloss"] == "part of woSi: Isis" and lines[0]["source"] == "two checkers, from the place"
    assert apart == {"piece, the whole word not a form of the map": 1, "piece, the whole word open in the map": 1}
    out = M.lay(gl, lines, "unnamed")                                     # the lines fit src/themap.py
    assert out["T1"][1]["level"] == "name" and out["T2"][2]["level"] == "name" and out["T2"][0]["level"] == "hypothesis"
    assert stops(lambda: U.lines_of(gl, [{"text": "T1", "n": 2, "form": "zzq", "verdict": "name", "whole": ""}]), "the map has 'zzk'")


def test_a_reading_that_missed_a_bar_gives_no_rows():
    home = U.HOME
    with tempfile.TemporaryDirectory() as d:
        U.HOME = Path(d)
        try:
            for folder, taken in (("pilot2", True), ("full", False)):
                U.write(f"{folder}/result.json", {"taken": taken, "rows": [{"place": folder}]})
            assert stops(U.rows, "full missed a bar")
            U.write("full/result.json", {"taken": True, "rows": [{"place": "full"}]})
            assert U.rows() == [{"place": "pilot2"}, {"place": "full"}] and U.TAKEN == ("pilot2", "full")
            (Path(d) / "full" / "answers1").mkdir()
            (Path(d) / "full" / "answers1" / "P01.jsonl").write_text("{}\n", encoding="utf-8")
            assert stops(lambda: U.packs_of("full", [], [], {}, {}, random.Random(1), U.BRIEF2), "answers exist")
        finally:
            U.HOME = home


def test_what_the_checkers_were_given_is_public():
    prompts = (ROOT / "runs/prompts/G3_places.md").read_text(encoding="utf-8")
    assert "\n".join(("    " + l).rstrip() for l in U.BRIEF.strip("\n").splitlines()) in prompts
    assert " ".join(U.NOTE.split()) in " ".join(prompts.split()) and U.BRIEF2.replace(U.NOTE, "") == U.BRIEF
    assert "do not look the spelling up" in U.BRIEF and "This pack lists {places} places" in U.BRIEF


# ------------------------------------------------------------------------------------ the figures and the pages

def test_the_figures_add_up():
    f = figs()
    assert f["taken"] == list(U.TAKEN) and sum(f["readings"][r]["places"] for r in U.TAKEN) == f["places"] == sum(f["verdicts"].values())
    first, second, full = (f["readings"][r] for r in U.READINGS)
    assert not first["taken"] and first["bars"]["kappa"] and not first["bars"]["cuts_called_piece_of_the_whole"] and not first["bars"]["words_called_name_or_piece"]
    for r in (second, full):
        assert r["taken"] and all(r["bars"].values()) and r["answered_by_both"] == r["places"] and r["kappa"] >= U.BARS2["kappa"]
        for c in r["controls"].values():
            assert c["word"].get("called_name", 0) <= U.BARS2["words_called_name"] * c["word"]["shown"]
            assert c["name"]["right"] >= U.BARS2["names_called_name"] * c["name"]["shown"]
    for v in ("word", "name", "piece", "unclear", "not agreed"):
        assert f["verdicts"][v] == second["verdicts"].get(v, 0) + full["verdicts"].get(v, 0), v
    laid = f["laid"]
    assert laid["lines"] == sum(laid["why"].values()) == sum(laid["to"].values()) == sum(laid["was"].values()) and set(laid["was"]) <= set(W.OPEN)
    assert laid["why"]["name"] == f["verdicts"]["name"] and laid["why"]["piece"] + sum(f["left_out"].values()) == f["verdicts"]["piece"]
    assert set(f["cost"]) == set(U.READINGS) and f["cost"]["full"]["agents"] == 50 and f["places_where_a_script_finds_a_join"] < f["places"] / 50


def test_the_figures_hold_counts_only():
    def leaves(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from leaves(v, k)
        elif isinstance(o, list):
            for v in o:
                yield from leaves(v, key)
        else:
            yield key, o
    for key, v in leaves(figs()):
        assert isinstance(v, (int, float)) or v is None or (key == "taken" and v in U.READINGS), (key, v)


def test_the_figures_agree_with_the_map():
    f, m = figs(), json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    layers = {l["name"]: l for l in m["layers"]}
    l, laid = layers[U.LAYER], f["laid"]
    assert (l["places"], l["why"], l["to"], l["was"]) == (laid["lines"], laid["why"], laid["to"], laid["was"])
    names = [x["name"] for x in m["layers"]]
    before = m["layers"][names.index(U.LAYER) - 1]
    assert l["distinct_words_translated"] == before["distinct_words_translated"]                    # the step gives no word a meaning
    assert l["after"]["running"]["need"] == before["after"]["running"]["need"] - (laid["to"].get("name", 0) + laid["to"].get("number", 0))


def test_the_page_says_what_the_figures_say():
    f, text, m = figs(), page(), json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    names = [x["name"] for x in m["layers"]]
    l = m["layers"][names.index(U.LAYER)]
    b, a, n, n0 = m["layers"][names.index(U.LAYER) - 1]["after"], l["after"], l["north_star"], m["layers"][names.index(U.LAYER) - 1]["north_star"]
    v, first, second, full = f["verdicts"], *(f["readings"][r] for r in U.READINGS)
    assert f"{f['spellings']:,} spellings that stand in one or two texts" in text and f"They stand at {f['places']:,} open places" in text
    assert f"named at {f['places_where_a_script_finds_a_join']} of these places" in text
    for label, key in (("a word of its own", "word"), ("a name", "name"), ("a piece of a word or name beside it", "piece"), ("unclear", "unclear"), ("not agreed", "not agreed")):
        assert f"| {label} | {v[key]} |" in text, key
    assert f"On the 100 real places their kappa is {first['kappa']:.2f} (bar 0.6)" in text and f"their kappa is {second['kappa']:.2f} (bar 0.6)" in text
    assert f"their kappa is {full['kappa']:.2f} (bar 0.6)" in text
    c1, c2 = full["controls"]["1"], full["controls"]["2"]
    assert f"| Translated words called a name | at most 10% | {c1['word'].get('called_name', 0)} of {c1['word']['shown']} | {c2['word'].get('called_name', 0)} of {c2['word']['shown']} |" in text
    assert f"| Names called a name | at least 70% | {c1['name']['right']} of {c1['name']['shown']} | {c2['name']['right']} of {c2['name']['shown']} |" in text
    assert f"the checkers called {c1['word'].get('called_piece', 0)} and {c2['word'].get('called_piece', 0)} a piece" in text
    assert f"named for only {f['laid']['why']['piece']} of them. The other {v['piece'] - f['laid']['why']['piece']} stay open" in text
    for label, x in (("Before this step", b), ("With this step", a)):
        r, s = x["running"], x["spellings"]
        assert f"| {label} | {r['translated']:,} of {r['need']:,} | {pct(r['share'])} | {s['translated']:,} of {s['need']:,} | {pct(s['share'])} |" in text, label
    u = m["north_star"]["unnamed_stems"]
    assert f"Of the 240 sampled stems {u['sample_still_unnamed']} are still unnamed" in text
    assert f"{n['translated']} of them have a meaning: {pct(n['star']['point'])} (between {pct(n['star']['low'])} and {pct(n['star']['high'])}), from {pct(n0['star']['point'])}" in text
    assert f"about {n['distinct_words']['point']:,} distinct words (between {n['distinct_words']['low']:,} and {n['distinct_words']['high']:,})" in text
    cost = f["cost"]
    assert f"{sum(c['agents'] for c in cost.values())} agents (Opus, each a fresh one), {sum(c['tokens'] for c in cost.values()):,} subagent tokens" in text
    assert f"the first pilot {cost['pilot']['tokens']:,}, the second {cost['pilot2']['tokens']:,}, the full pass {cost['full']['tokens']:,}" in text


def test_the_summaries_name_the_step():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python3 -I tests/test_unnamed.py" in readme and "- `python3 -I src/unnamed.py public` (and " in readme
    f, m = figs(), json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    l = {x["name"]: x for x in m["layers"]}[U.LAYER]
    c, star = l["after"]["running"], l["north_star"]
    for text in (" ".join(readme.split()), " ".join((ROOT / "NEXT_STEPS.md").read_text(encoding="utf-8").split())):
        assert f"{c['translated']:,} of the {c['need']:,} running words that need a meaning" in text and pct(c["share"]) in text
        assert f"{star['translated']} of about {star['distinct_words']['point']:,}" in text and f"{f['verdicts']['name']} names" in text
        assert "unnamed_spellings.md" in text


# ------------------------------------------------------------------------------------------- with the local files

def test_the_figures_are_the_count_of_the_local_files():
    needs("data/sources/v6", "data/rilly2003", "data/sources/g3/full/result.json", "data/sources/g3/pilot2/result.json", *[l["file"] for l in M.LAYERS])
    assert U.figures() == figs()
    lines, _ = U.lines_of(U.before(), U.rows())
    assert lines == M.lines_of(M.LAYERS[[l["name"] for l in M.LAYERS].index(U.LAYER)])


def test_the_script_writes_the_packs_the_checkers_were_given():
    """Every reading again in a folder of its own, the checkers' answers copied in only after its packs are written:
    the packs come out byte for byte, and the verdicts are those of the run."""
    needs("data/sources/v6", "data/rilly2003", "data/corpus_v6.jsonl", *[f"data/sources/g3/{r}/key.json" for r in U.READINGS], *[l["file"] for l in M.LAYERS[:-1]])
    live = U.HOME
    with tempfile.TemporaryDirectory() as d:
        U.HOME = Path(d)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                for folder, packs in (("pilot", U.pilot_packs), ("pilot2", U.pilot2_packs), ("full", U.full_packs)):
                    packs()
                    names = sorted(p.name for p in (live / folder / "packs").iterdir())
                    assert names == sorted(p.name for p in (Path(d) / folder / "packs").iterdir()), folder
                    assert all(filecmp.cmp(Path(d) / folder / "packs" / n, live / folder / "packs" / n, shallow=False) for n in names), folder
                    for c in (1, 2):
                        shutil.copytree(live / folder / f"answers{c}", Path(d) / folder / f"answers{c}", dirs_exist_ok=True)
                    U.count(folder)
                    assert U.read(f"{folder}/result.json") == json.loads((live / folder / "result.json").read_text(encoding="utf-8")), folder
        finally:
            U.HOME = live


def test_each_rule_was_in_git_before_the_checkers_it_binds():
    needs(*[f"data/sources/g3/{r}/answers1" for r in U.READINGS])

    def committed(phrase, path):
        out = subprocess.run(["git", "-C", str(ROOT), "log", "--reverse", "--format=%ct", f"-S{phrase}", "--", path], capture_output=True, text=True).stdout.split()
        assert out, phrase
        return int(out[0])

    def first_answer(folder):
        return min(os.path.getmtime(f) for c in (1, 2) for f in (U.HOME / folder / f"answers{c}").glob("*.jsonl"))
    rules = "data/discovery/unnamed_spellings.md"
    assert committed("## 4. The bars, set before any checker is started", rules) < first_answer("pilot")
    assert committed("## 7. The second pilot (rules set on", rules) < first_answer("pilot2")
    assert committed("**The full pass** (set at", rules) < first_answer("full")
    assert committed("The brief", "runs/prompts/G3_places.md") < first_answer("pilot")


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
