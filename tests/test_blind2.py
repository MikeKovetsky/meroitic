"""Checks for the blind test again (src/blind2.py, data/discovery/blind_test_2.md).

  python3 -I tests/test_blind2.py

The map, the lexicon and the readers' answers are local only: the checks of the method run on made-up words; the
checks of the reported numbers read the public figures file, compare the page with it, and compare it with a
count from the local files where those are present.
"""
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

import blind2 as B                   # noqa: E402
import recurring as W                # noqa: E402
import themap as M                   # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/blind_test_2.md"


def figs():
    return json.loads(B.PUBLIC.read_text(encoding="utf-8"))


def page():
    return " ".join(PAGE.read_text(encoding="utf-8").split())


def stops(fn, part):
    try:
        fn()
    except SystemExit as e:
        assert part in str(e), e
        return True
    raise AssertionError("did not stop")


def word(form, level, *entries, gloss="", **more):
    return {"form": form, "level": level, "gloss": gloss, "parts": [{"form": form, "entry": e} for e in entries]} | more


# ------------------------------------------------------------------------------------------------- the method

def test_a_choice_needs_all_five_readers_here_and_four_in_the_first_test():
    four = ["a", "a", "a", "a", "none"]
    assert W.NEEDED == 4 and W.choice_of(four) == "a" and len(W.ACCEPTED) == 38
    with B.settings():
        assert (W.READERS, W.PACKS, W.NEEDED) == (5, 5, 5) and W.ACCEPTED == B.ACCEPTED and len(W.ACCEPTED) == 38 + len(B.NEW)
        assert W.choice_of(four) is None and W.choice_of(["a"] * 5) == "a" and W.choice_of(["none"] * 5) == "none" and W.choice_of(["a"] * 4) is None
    assert W.NEEDED == 4 and W.choice_of(four) == "a" and len(W.ACCEPTED) == 38       # the first test's own settings are back
    try:
        with B.settings():
            raise KeyError
    except KeyError:
        assert W.NEEDED == 4 and len(W.ACCEPTED) == 38
    assert B.BARS is W.BARS == {"right_when_chosen": 0.80, "chosen_at_least": 8, "wrong_when_absent": 0.10}


def test_a_filler_shares_no_word_and_no_group_with_an_option():
    assert B.near("land, province", "the land") and B.near("bull", "cow") and B.near("cow", "bull") and not B.near("bull", "water")
    assert B.near("to give", "to grant") and not B.near("to give", "to drink")          # "to" is no content word
    pool = {("bull", "noun"), ("cow", "noun"), ("water", "noun"), ("god", "noun"), ("good god", "noun"), ("man", "noun"), ("scribe", "title"),
            ("envoy", "title"), ("to drink", "verb")}
    for seed in range(30):
        opts = B.fill(["cow"], "noun", random.Random(seed), pool)
        assert opts[0] == "cow" and len(opts) == 4 and len(set(opts)) == 4 and "bull" not in opts and not {"god", "good god"} <= set(opts), opts
        assert set(opts[1:]) <= {"water", "god", "good god", "man"}                 # the word's kind has enough: no title, no verb
        none = B.fill([], "noun", random.Random(seed), pool, avoid=["good god"])
        assert not {"god", "good god"} & set(none) and len(none) == 4, none        # nothing near the true meaning that is not shown
        short = B.fill(["scribe"], "title", random.Random(seed), pool)
        assert short[:2] in (["scribe", "envoy"],) and len(short) == 4              # too few titles: filled from the other kinds
    assert len(B.fill(["a"], "noun", random.Random(1), {("b", "noun")})) == 2       # the_words() stops on fewer than four


def test_the_groups_keep_apart_meanings_of_the_test():
    f = figs()
    meanings = {m for r in f["rows"] for m in r["options"]} | {m for m, _ in B.ACCEPTED.values()}
    assert all(m in meanings for g in B.GROUPS for m in g), [m for g in B.GROUPS for m in g if m not in meanings]
    assert f["groups_of_near_meanings"] == len(B.GROUPS) == 17 and all(len(g) >= 2 for g in B.GROUPS)
    for r in f["rows"]:
        own = [r["true"]] if r["true"] else r["candidates"]
        fillers = [m for m in r["options"] if m not in own]
        for i, m in enumerate(fillers):
            assert not any(B.near(m, o) for o in own + fillers[:i]), (r["entry"], m)


def test_the_further_entries_are_sure_alone_in_their_word_and_in_three_texts():
    lex = {"new": {"status": "established"}, "two": {"status": "probable"}, "unsure": {"status": "hypothesis"}, "kdi": {"status": "established"},
           "ste": {"status": "established"}, "-lo": {"status": "established"}}
    gl = {f"T{i}": [word("a", "meaning", "new"), word("b", "meaning", "unsure"), word("c", "meaning", "kdi"), word("d", "meaning", "ste", "-lo"),
                    word("e", "meaning", "two", "new"), word("f", "hypothesis", "two")] + ([word("g", "meaning", "two")] if i < 2 else [])
          for i in range(3)}
    assert B.further(gl, lex) == ["new", "ste"]       # `two` stands alone in two texts only; `kdi` was in the first test; `ste` is one of NEW
    assert not set(B.NEW) & set(B.OUT) and len(B.NEW) + len(B.OUT) == 45 and not (set(B.NEW) | set(B.OUT)) & (set(B.ACCEPTED) - set(B.NEW))
    assert set(B.OUT.values()) == {B.OFFICE, B.FORM, B.NONE, B.ALSO} and all(k in W.KINDS for _, k in B.NEW.values())


def test_an_open_word_keeps_the_places_the_map_still_holds_open():
    its = {"x": {"places": [{"text": "T", "n": n} for n in range(1, 6)]}, "y": {"places": [{"text": "T", "n": 6}, {"text": "T", "n": 7}, {"text": "T", "n": 8}]}}
    cur = {"T": [word("x", "unknown"), word("x", "meaning"), word("x", "hypothesis"), word("x", "kind"), word("x", "name"),
                 word("y", "unknown"), word("y", "name"), word("y", "unknown")]}
    cands = {k: {"name": "", "candidates": [{"meaning": "to give", "kind": "verb"}, {"meaning": "house", "kind": "noun"}]} for k in "xyz"}
    got = B.open_words(cur, its, cands, {"x": [1, 2, 3, 4, 5], "y": [1, 2, 3]})
    assert set(got) == {"x"} and got["x"]["places"] == [("T", 0), ("T", 2), ("T", 3)] and got["x"]["kind"] == "verb"   # y has two open places left
    assert got["x"]["candidates"] == [("to give", "verb"), ("house", "noun")]


def test_a_candidate_is_worded_as_the_public_figures_word_it():
    theirs = "a wording made up here"                                           # a reader's own wording stands in no tracked file
    cand = {"candidates": [{"meaning": "year", "kind": "noun"}, {"meaning": "great paqar", "kind": "title"}, {"meaning": theirs, "kind": "noun"}]}
    assert B.ours("penn", cand) == [("year", "noun"), (W.CANDIDATES_IN_OUR_WORDS["penn", 2], "noun")]     # the second of those kept
    assert B.ours("another", cand) == [("year", "noun"), (theirs, "noun")]


def test_a_piece_is_shown_without_the_spelling_of_its_whole_word():
    cur = {"T": [word("wo", "meaning", gloss="part of woSi: Isis", why="piece"), word("x", "meaning", gloss="part of the offering"),
                 word("y", "name", gloss="part of abc: a name", why="piece")]}
    shown = B.shown_map(cur)
    assert [g["gloss"] for g in shown["T"]] == ["Isis", "part of the offering", "a name"] and cur["T"][0]["gloss"] == "part of woSi: Isis"


def test_an_accepted_word_is_right_wrong_none_or_without_a_choice():
    assert [B.outcome({"choice": c, "true": "water"}) for c in ("water", "silver", "none", None)] == ["right", "wrong", "none", "no choice"]


def test_what_the_readers_were_given_is_public():
    prompts = " ".join((ROOT / "runs/prompts/G6_choice.md").read_text(encoding="utf-8").split())
    assert "`CHOICE_BRIEF` in [`src/recurring.py`](../../src/recurring.py), word for word but for its last line" in prompts
    assert B.COUNTED.format(n="{n}") in prompts and W.CHOICE_BRIEF.count(B.REPLY) == 1
    assert "data/sources/g6/packs/K<n>_r<r>.md" in prompts and "open no other file, do not search the web, do not spawn agents" in prompts
    assert "Do not try to work out which word or which inscription it is" in W.CHOICE_BRIEF


# ------------------------------------------------------------------------------------ the figures and the pages

def test_the_figures_add_up():
    f = figs()
    c, rows = f["choice"], f["rows"]
    assert f["words"] == len(rows) == sum(f["sorts"].values()) == c["words"] == sum(f["packs_of"].values())
    assert f["answers"] == f["answers_expected"] == f["words"] * B.READERS and c["complete"] and all(sum(r["picks"].values()) == B.READERS for r in rows)
    assert (c["readers"], c["needed"], c["packs"]) == (B.READERS, B.NEEDED, B.PACKS) == (5, 5, 5) and c["bars"] == B.BARS and f["seed"] == B.SEED
    for r in rows:                                                              # a choice is what all five readers pick
        top = [m for m, n in r["picks"].items() if n == B.READERS]
        assert r["choice"] == (top[0] if top else None) and len(r["options"]) == 4 and set(r["picks"]) <= set(r["options"]) | {"none"}, r["entry"]
    acc = [r for r in rows if r["sort"] != "open"]
    off, ab = f["accepted_by_outcome"]["offered"], f["accepted_by_outcome"]["absent"]
    assert f["accepted"] == {"all": len(acc), "of_the_first_test": 38, "new": len(B.NEW)} and f["accepted"]["all"] == len(B.ACCEPTED) == 43
    assert sum(off.values()) == c["offered"] == f["sorts"]["offered"] and sum(ab.values()) == c["absent"] == f["sorts"]["absent"]
    assert all(r["true"] in r["options"] for r in acc if r["sort"] == "offered") and all(r["true"] not in r["options"] for r in acc if r["sort"] == "absent")
    assert (c["offered_chosen"], c["offered_right"]) == (off["right"] + off["wrong"], off["right"]) and c["absent_wrong"] == ab["wrong"] and "right" not in ab
    assert c["right_when_chosen"] == round(c["offered_right"] / c["offered_chosen"], 4) and c["wrong_when_absent"] == round(c["absent_wrong"] / c["absent"], 4)
    assert c["bar1"] == (c["offered_chosen"] >= B.BARS["chosen_at_least"] and c["right_when_chosen"] >= B.BARS["right_when_chosen"]) is True
    assert c["bar2"] == (c["wrong_when_absent"] <= B.BARS["wrong_when_absent"]) is False and c["labels_given"] is False
    assert len(f["wrong_choices"]) == off["wrong"] + ab["wrong"] and all(w["chosen"] != w["true"] for w in f["wrong_choices"])
    opened = [r for r in rows if r["sort"] == "open"]
    assert c["open_words"] == len(opened) == sum(c["open"].values()) and "favoured" not in c["open"]
    assert f["open_chosen"] == {r["entry"]: r["choice"] for r in opened if r["verdict"] == "chosen, no label"} and len(f["open_chosen"]) == c["open"]["chosen, no label"]
    assert sorted(w["entry"] for w in f["new_words"]) == sorted(B.NEW) and all(B.NEW[w["entry"]][0] == w["true"] for w in f["new_words"])
    fe = f["further_entries"]
    assert fe["all"] == fe["taken"] + sum(fe["left_out"].values()) == len(fe["by_entry"]) == 45 and fe["taken"] == len(B.NEW)
    assert f["accepted"]["of_the_first_test"] + fe["all"] == 83
    assert f["cost"]["agents"] == B.READERS * B.PACKS and f["when"] == B.WHEN
    assert f["first_test"]["needed"] == 4 and f["places_shown_at_most"] == W.SHOWN and f["words_each_side"] == W.CHOICE_WIDTH


def test_the_figures_hold_only_wordings_that_were_public_or_are_ours():
    """Every meaning in the rows is an accepted meaning or a proposal as the first test's public figures word it,
    or one of the five new accepted meanings, which are ours."""
    first = json.loads(B.FIRST.read_text(encoding="utf-8"))["choice"]["rows"]
    public = {m for r in first for m in r["options"] + r["candidates"] + ([r["true"]] if r["true"] else [])} | {"none"}
    ours = {m for m, _ in B.NEW.values()}
    f = figs()
    for r in f["rows"]:
        for m in r["options"] + r["candidates"] + list(r["picks"]) + [x for x in (r["true"], r["choice"]) if x]:
            assert m in public | ours, (r["entry"], m)
    import lexicon as X
    assert all(len(X.words_of(m)) <= X.LONGEST for m in ours)


def test_the_page_says_what_the_figures_say():
    f, text = figs(), page()
    c, w, fe = f["choice"], f["when"], f["further_entries"]
    off, ab = f["accepted_by_outcome"]["offered"], f["accepted_by_outcome"]["absent"]
    acc = f["accepted"]
    hm = lambda t: t[:5]                                                   # noqa: E731
    pct = lambda x: f"{100 * x:.1f}%"                                      # noqa: E731
    total = acc["of_the_first_test"] + fe["all"]
    assert f"**Not met as worded: {acc['all']} accepted words, not {total}.** Only {fe['taken']} of the {fe['all']} further entries" in text
    assert f"**The accepted words: {acc['all']}, not {total}.**" in text and f"in three texts or more: {total}. The first test had {acc['of_the_first_test']} of them. Of the other {fe['all']}:" in text
    assert f"| A meaning of their own, of one of the four kinds | {fe['taken']} |" in text
    for label, key in (('A title of which only the kind of office is known ("a priestly title")', B.OFFICE), ("A form or a variant of a word of the test, or the same meaning", B.FORM),
                       ("No meaning of its own, or not a noun, title, verb or adjective", B.NONE), ("Also an open word of the test", B.ALSO)):
        assert f"| {label} | {fe['left_out'][key]} |" in text, key
    assert "taken: mother, queen (Candace), the ruler's spouse, to bear (a child), to beget (a child)" in text and {m for m, _ in B.NEW.values()} == {
        "mother", "queen (Candace)", "the ruler's spouse", "to bear (a child)", "to beget (a child)"}
    assert f"{c['absent']} of the {acc['all']}. The other {c['offered']} are shown with it." in text
    assert f"**The open words: {c['open_words']},**" in text and f"the {acc['all']} accepted meanings and the proposals of the open words" in text
    assert "Seventeen groups of meanings" in text and f["groups_of_near_meanings"] == 17
    assert f"five for each of {c['packs']} packs, each a fresh agent (Opus): {f['cost']['agents']}. The lots are drawn with the seed {f['seed']}." in text
    assert "Up to twelve places of the hidden word, six words on each side" in text and (f["places_shown_at_most"], f["words_each_side"]) == (12, 6)
    assert f"at least {100 * B.BARS['right_when_chosen']:.0f}% are right, and there are at least {B.BARS['chosen_at_least']} such words" in text
    assert f"at most {100 * B.BARS['wrong_when_absent']:.0f}% get a choice other than \"none\" (of {c['absent']}: one at most)" in text
    assert int(B.BARS["wrong_when_absent"] * c["absent"]) == 1 and "In the first test four of five were enough." in text and f["first_test"]["needed"] == 4
    # the result
    assert f"## 6. The result (counted at {hm(w['counted'])}, no label given)" in text
    assert (f"The {f['cost']['agents']} readers were started at {hm(w['started'])}, after the commit with the bars ({w['set']}); their answers came between "
            f"{hm(w['first_answer'])} and {hm(w['last_answer'])}. Every reader answered every word of its pack ({f['words']} words, five readers each).") in text
    assert f"| Every reader answers every word | {f['answers']} of {f['answers_expected']} answers | met |" in text
    assert f"| {c['offered_right']} of {c['offered_chosen']} right ({pct(c['right_when_chosen'])}) | met |" in text
    assert f"| **{c['absent_wrong']} of {c['absent']} ({pct(c['wrong_when_absent'])})** | **missed** |" in text
    assert f"| | Shown with their meaning ({c['offered']}) | Shown without it ({c['absent']}) |" in text
    assert f"| All five pick the true meaning | {off['right']} | (not offered) |" in text and f"| All five pick a wrong meaning | {off['wrong']} | {ab['wrong']} |" in text
    assert f"| All five say \"none of these\" | {off['none']} | {ab['none']} |" in text and f"| No choice (the five differ) | {off['no choice']} | {ab['no choice']} |" in text
    wrong = {(x["sort"], x["true"], x["chosen"]) for x in f["wrong_choices"]}
    assert wrong == {("offered", "small, young", "great, elder"), ("absent", "sister", "direct descendant"), ("absent", "god", "silver"), ("absent", "general", "governor")}
    assert '"small, young" was taken for "great, elder"' in text
    assert '"sister" was taken for "direct descendant", "god" for "silver", and "general" for "governor"' in text
    new = {x["true"]: (x["sort"], x["outcome"]) for x in f["new_words"]}
    assert new == {"to bear (a child)": ("offered", "right"), "mother": ("offered", "no choice"), "the ruler's spouse": ("offered", "no choice"),
                   "queen (Candace)": ("offered", "no choice"), "to beget (a child)": ("absent", "no choice")}
    assert 'one was chosen, rightly ("to bear a child"); for the three others shown with their meaning the readers made no choice' in text
    assert f"**The open words ({c['open_words']}), had the bars held.**" in text
    for label, key in (("All five pick the same proposal (no label)", "chosen, no label"), ("All five pick a filler", "a filler chosen"),
                       ('All five say "none of these"', "none of the four"), ("No choice", "no choice")):
        assert f"| {label} | {c['open'][key]} |" in text, key
    seven = f["open_chosen"]
    assert seven == {"wse": "of the country", "wi (1)": "brother", "yed": "silver", "pqrtr": "great prince", "ẖol": "to grant", "qomlise": "good god", "penn": "year"}
    assert ("The seven are `wse` (of the country), `wi` (brother), `yed` (silver), `pqrtr` (great prince), `ẖol` (to grant), `qomlise` (good god) and "
            "`penn` (year). They carry no label.") in text
    # against the first test: its readers all agreed on six of the seven, on the same proposal for five
    first = {r["entry"]: r for r in json.loads(B.FIRST.read_text(encoding="utf-8"))["choice"]["rows"]}
    all5 = {k: max(first[k]["picks"], key=first[k]["picks"].get) for k in seven if max(first[k]["picks"].values()) == 5}
    assert len(all5) == 6 and sum(all5[k] == seven[k] for k in all5) == 5 and (all5["ẖol"], seven["ẖol"]) == ("to present", "to grant")
    assert set(all5) == set(f["first_test"]["all_agree"]["open_candidates"]) & set(seven) and len(first["ẖol"]["candidates"]) == 3
    assert ('Six of them had all five readers of the first test too, five with the same proposal; for `ẖol` the readers then agreed on "to present" '
            'and now on "to grant", two of its three proposals.') in text
    a = f["first_test"]["all_agree"]
    assert f"{c['offered_right']} of {c['offered_chosen']}, against {a['offered_right']} of {a['offered_chosen']}" in text
    assert a["absent_wrong"] == 0 and f"The first test's \"no wrong choice among {f['first_test']['absent']}\" did not hold" in text
    yed = [r for r in f["rows"] if "silver" in r["picks"] and r["picks"]["silver"] == 5]
    assert {(r["entry"], r["sort"]) for r in yed} == {("yed", "open"), ("mk", "absent")} and "all five chose it for the word for \"god\", where it was a filler" in text
    assert f"Cost: {f['cost']['agents']} agents, {f['cost']['tokens']:,} tokens" in text
    assert "A label is not a translation." in text and "No meaning found here is the project's own." in text


def test_the_summaries_name_the_step():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python3 -I tests/test_blind2.py" in readme and "- `python3 -I src/blind2.py public`" in readme
    c = figs()["choice"]
    for name in ("README.md", "NEXT_STEPS.md", "REPORT.md"):
        text = " ".join((ROOT / name).read_text(encoding="utf-8").split())
        assert "blind_test_2.md" in text and "no label is given" in text, name
        assert f"{c['offered_right']} of {c['offered_chosen']}" in text and f"{c['absent_wrong']} of {c['absent']}" in text, name
    assert "`data/sources/g6/`" in (ROOT / "data/INDEX.md").read_text(encoding="utf-8")


# ------------------------------------------------------------------------------------------- with the local files

LOCAL = ("data/sources/g6/result.json", "data/sources/g6/key.json", "data/sources/g6/tokens.json")


def test_the_figures_are_the_count_of_the_local_files():
    needs(*LOCAL)
    assert B.figures() == figs()


def test_the_script_writes_the_packs_the_readers_were_given():
    """The words and the packs again in a folder of its own, the readers' answers copied in afterwards: byte for
    byte the packs of the run, its key and its result."""
    needs(*LOCAL, "data/sources/g6/packs", "data/sources/v6/analysts/glosses.jsonl", "data/rilly2003", "data/sources/recurring/choice/candidates.json")
    live = B.HOME
    with tempfile.TemporaryDirectory() as d:
        B.HOME = Path(d)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                B.packs()
                assert B.read("key.json") == json.loads((live / "key.json").read_text(encoding="utf-8"))
                names = sorted(p.name for p in (live / "packs").iterdir())
                assert len(names) == B.READERS * B.PACKS and names == sorted(p.name for p in (B.HOME / "packs").iterdir())
                assert all(filecmp.cmp(B.HOME / "packs" / n, live / "packs" / n, shallow=False) for n in names)
                for r in range(1, B.READERS + 1):
                    shutil.copytree(live / f"reader{r}", B.HOME / f"reader{r}", dirs_exist_ok=True)
                assert stops(B.packs, "the readers have answered")
                B.count()
                assert B.read("result.json") == json.loads((live / "result.json").read_text(encoding="utf-8"))
        finally:
            B.HOME = live
    assert W.NEEDED == 4


def test_the_test_reads_the_map_as_it_was_when_it_was_set():
    assert B.LAYERS == tuple(l["name"] for l in M.LAYERS[:len(B.LAYERS)])
    layers = M.LAYERS
    M.LAYERS = layers[1:]
    try:
        assert stops(B.the_map, "the layers of the test are no longer")
    finally:
        M.LAYERS = layers


def test_the_rules_were_in_git_before_the_readers_were_started():
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout
    w = B.WHEN
    assert git("log", "-1", "--format=%cI", w["set_in"]).strip() == f"2026-11-16T{w['set']}-08:00"
    assert w["set"] < w["started"] < w["first_answer"] <= w["last_answer"] < w["counted"]
    for phrase in ("## 3. The bars, set before any reader is started", "**A choice needs all five readers:**", "**The accepted words: 43, not 83.**"):
        out = git("log", "--reverse", "--format=%cI", f"-S{phrase}", "--", "data/discovery/blind_test_2.md").split()
        assert out and out[0][11:19] <= w["set"] and phrase in PAGE.read_text(encoding="utf-8"), phrase


def test_the_times_of_the_answers_are_the_files():
    needs("data/sources/g6/reader1", "data/sources/g6/reader5")
    import datetime
    import zoneinfo
    pacific = zoneinfo.ZoneInfo("America/Los_Angeles")
    times = sorted(datetime.datetime.fromtimestamp(f.stat().st_mtime, pacific).strftime("%H:%M:%S")
                   for r in range(1, B.READERS + 1) for f in (B.HOME / f"reader{r}").glob("K*.jsonl"))
    assert len(times) == B.READERS * B.PACKS and (times[0], times[-1]) == (B.WHEN["first_answer"], B.WHEN["last_answer"]), (times[0], times[-1])


def test_no_new_meaning_follows_a_source_for_four_words():
    needs("data/rilly2003", "data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt")
    import lexicon as X
    import lexique as Q

    def runs(text):
        w = X.words_of(re.sub(r"ffi|ffl|ff|fi|fl|\x00", "ꜰ", text.lower()))
        return {tuple(w[i: i + X.COPIED]) for i in range(len(w) - X.COPIED + 1)}
    grams = set()
    for e in Q.load():
        for t in [v for v in e.values() if isinstance(v, str)] + [p.get("proposal") or "" for p in e.get("proposals") or []]:
            grams |= runs(t)
    for path in ("data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt"):
        text = re.sub(r"(?m)^\f?=== page \d+ ===$", " ", (ROOT / path).read_text(encoding="utf-8", errors="replace"))
        grams |= runs(text) | runs(re.sub(r"(?<=[^\W\d_])-[ \t]*\n\s*(?=[^\W\d_])", "", text))
    assert [m for m, _ in B.NEW.values() if runs(m) & grams] == []


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
