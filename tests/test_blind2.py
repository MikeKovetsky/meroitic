"""Checks for the blind test again (src/blind2.py, data/discovery/blind_test_2.md) and for its run with all 83
accepted words (data/discovery/blind_test_83.md).

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


def test_the_options_are_told_by_the_sorts_they_hold():
    """Both sorts: an accepted meaning of the test and a proposal of one of its open words among the four. Near
    proposals: two of an open word's own proposals share a content word or a group."""
    rows = [{"sort": "open", "entry": "x", "candidates": ["to present", "to grant"], "options": ["to present", "to grant", "water", "boat"]},
            {"sort": "open", "entry": "y", "candidates": ["house"], "options": ["house", "to present", "boat", "silver"]},
            {"sort": "offered", "entry": "ato", "candidates": [], "options": ["water", "god", "man", "wife"]},
            {"sort": "absent", "entry": "kdi", "candidates": [], "options": ["to grant", "house", "boat", "silver"]}]
    assert {"water", "god", "man", "wife"} <= {m for m, _ in B.ACCEPTED.values()} and not {"boat", "silver", "house"} & {m for m, _ in B.ACCEPTED.values()}
    assert B.options_of(rows) == {"words": 4, "of_both_sorts": 1, "open_words_with_near_proposals": ["x"]}


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
    assert 'one was chosen, rightly ("to bear (a child)"); for the three others shown with their meaning the readers made no choice' in text
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
    # the review's two corrections of section 2, which stands as it was written before the readers
    o = f["options"]
    assert "Now the two sorts stand mixed under every word." in text and "**Never two near meanings.**" in text
    assert f"they hold both an accepted meaning and a proposal under {o['of_both_sorts']} of the {o['words']} words" in text and o["words"] == f["words"]
    near = o["open_words_with_near_proposals"]
    assert (f"under {len(near)} open words ({', '.join(f'`{e}`' for e in near)}) two or three of the four are near meanings") in text
    accepted = {m for m, _ in B.ACCEPTED.values()}                              # both figures counted again from the rows
    proposals = {m for r in f["rows"] if r["sort"] == "open" for m in r["candidates"]}
    assert o["of_both_sorts"] == sum(bool(set(r["options"]) & accepted and set(r["options"]) & proposals) for r in f["rows"])
    assert set(near) == {r["entry"] for r in f["rows"] if r["sort"] == "open" and any(B.near(a, b) for a in r["candidates"] for b in r["candidates"] if a != b)}


def test_the_summaries_name_the_step():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python3 -I tests/test_blind2.py" in readme and "- `python3 -I src/blind2.py public`" in readme
    o = figs()["options"]
    assert f"by that lot, {o['of_both_sorts']} of the {o['words']} words have both sorts among their four" in " ".join(readme.split())
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


def test_no_pack_shows_a_hidden_spelling():
    """As in the first test: no pack shows the spelling of a word it hides, and each pack offers each of its words the
    key's four meanings, in the order of that reader's letters."""
    needs(*LOCAL, "data/sources/g6/packs", "data/sources/v6/analysts/glosses.jsonl", "data/rilly2003")
    assert hidden_spellings_shown() == []


def hidden_spellings_shown():
    """[(pack, reader, spelling)] for every hidden spelling a pack shows; the packs' letters are checked on the way."""
    key, gl, shown = B.read("key.json"), B.shown_map(B.the_map()), []
    for n in range(1, B.PACKS + 1):
        mine = [w | {"code": c} for c, w in key["words"].items() if w["pack"] == n]
        tokens = W.tokens_of(mine, gl)
        for r in range(1, B.READERS + 1):
            body = (B.HOME / "packs" / f"K{n}_r{r}.md").read_text(encoding="utf-8").split("\n---\n", 1)[1]
            shown += [(n, r, tok) for tok in tokens if re.search(rf"(?<![A-Za-zḫẖšñ]){re.escape(tok)}(?![A-Za-zḫẖšñ])", body)]
            for w in mine:
                block = body[body.index(f"## `{w['code']}`"):].split("\n## `", 1)[0]
                letters = key["letters"][f"{w['code']}/{r}"]
                assert re.findall(r"(?m)^[ABCD]\. (.*)$", block) == letters and sorted(letters) == sorted(w["options"]), (w["code"], r)
    return shown


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
    assert [m for m, _ in list(B.NEW.values()) + list(B.NEW_83.values()) if runs(m) & grams] == []


# ------------------------------------------------------------------------- the run with all 83 accepted words

PAGE_83 = ROOT / "data/discovery/blind_test_83.md"
LOCAL_83 = ("data/sources/g6b/result.json", "data/sources/g6b/key.json", "data/sources/g6b/tokens.json", "data/sources/g6b/pack_wording.json",
            "data/sources/g6/result.json")
MAP_83 = ("data/sources/v6/analysts/glosses.jsonl", "data/rilly2003", "data/sources/recurring/choice/candidates.json",
          "data/sources/rare/g4m/overlay.jsonl", "data/sources/g8b/overlay.jsonl")


def figs83():
    return json.loads(B.PUBLIC_83.read_text(encoding="utf-8"))


def page83():
    return " ".join(PAGE_83.read_text(encoding="utf-8").split())


def settings_now():
    return (B.HOME, B.ANSWERS, B.PUBLIC, B.SEED, B.PACKS, B.LAYERS, dict(B.NEW), dict(B.OUT), dict(B.ACCEPTED), list(B.GROUPS), B.COARSE, B.SORTS, B.WHEN)


def test_the_run_with_83_has_its_own_settings_and_gives_the_first_runs_back():
    first = settings_now()
    with B.run_83():
        assert (B.HOME, B.ANSWERS, B.PUBLIC, B.SEED, B.PACKS) == (B.HOME_83, "data/sources/g6b", B.PUBLIC_83, 20261126, 8)
        assert B.LAYERS == first[5] + ("rare_millet", "leftover") == tuple(l["name"] for l in M.LAYERS[:6])
        assert B.OUT == {} and len(B.NEW) == 45 and len(B.ACCEPTED) == 83 and len(B.GROUPS) == 22 and B.SORTS is B.SORT and B.WHEN is B.WHEN_83
        assert set(B.NEW) == set(first[6]) | set(first[7])                  # every one of the 45 further entries is in
        with B.settings():
            assert (W.READERS, W.PACKS, W.NEEDED) == (5, 8, 5) and len(W.ACCEPTED) == 83
        assert len(W.ACCEPTED) == 38
    assert settings_now() == first
    try:
        with B.run_83():
            raise KeyError
    except KeyError:
        assert settings_now() == first


def test_the_40_entries_the_first_run_left_out_are_in_each_with_its_sort_and_meaning():
    assert {h: B.SORT[h] for h in B.OUT} == B.OUT and {why: len(hs) for why, hs in B.MORE.items()} == {B.OFFICE: 20, B.FORM: 15, B.NONE: 3, B.ALSO: 2}
    assert all(B.SORT[h] == B.OF_THE_FIVE for h in B.NEW) and len(B.SORT) == 45 == len(B.NEW_83) and set(B.NEW_83) == set(B.NEW) | set(B.OUT)
    assert all(k in W.KINDS for _, k in B.NEW_83.values()) and len(B.ACCEPTED_83) == 83 and not set(B.NEW_83) & set(W.ACCEPTED)
    coarse = {h for h, (m, _) in B.NEW_83.items() if m in B.COARSE_83}
    assert len(coarse) == 21 and coarse == set(B.MORE[B.OFFICE]) | {"kroro"} and len(B.COARSE_83) == 5
    # a form or a variant has the meaning of its word of the test; the two that are open words too, the map's meaning
    for form, word_of_the_test in (("pesto", "peseto"), ("mẖe", "mḫe"), ("ntke (1)", "ntki"), ("l (2)", "tre")):
        assert B.NEW_83[form] == W.ACCEPTED[word_of_the_test], form
    assert B.NEW_83["dḫe"] == B.NEW_83["t-dḫe"] == B.NEW["te-dḫe-l"] and B.NEW_83["apote-lẖ"][0].endswith(W.ACCEPTED["apote"][0])
    assert len(B.GROUPS_83) == len(B.GROUPS) + 5 and B.GROUPS_83[:len(B.GROUPS)] == B.GROUPS


def test_a_coarse_meaning_is_never_a_filler():
    pool = {(B.PRIEST, "title"), (B.ADMIN, "title"), ("scribe", "title"), ("envoy", "title"), ("general", "title"), ("governor", "title"),
            ("viceroy", "title")}
    assert not B.near(B.PRIEST, "scribe") and B.COARSE == frozenset()         # in the first run nothing is coarse
    assert any(B.PRIEST in B.fill(["scribe"], "title", random.Random(s), pool) for s in range(30))
    with B.run_83():
        assert B.near(B.PRIEST, "scribe") and not B.near("scribe", B.PRIEST) and {B.PRIEST, B.ADMIN, B.TITLE} <= B.COARSE and len(B.COARSE) == 5
        for seed in range(30):
            opts = B.fill(["scribe"], "title", random.Random(seed), pool)
            assert len(opts) == 4 and not set(opts) & B.COARSE, opts
            own = B.fill([B.PRIEST], "title", random.Random(seed), pool)     # it stands as the true meaning of its own word
            assert own[0] == B.PRIEST and len(own) == 4 and not set(own[1:]) & B.COARSE, own
            assert not set(B.fill([], "title", random.Random(seed), pool, avoid=[B.ADMIN])) & B.COARSE
    assert not B.near(B.PRIEST, "scribe")
    f = figs83()
    assert set(f["coarse_meanings"]) == set(B.COARSE_83) and sum(f["coarse_meanings"].values()) == 21
    for r in f["rows"]:
        own = [r["true"]] if r["true"] else r["candidates"]
        assert not (set(r["options"]) - set(own)) & set(B.COARSE_83), r["entry"]


def test_the_outcomes_are_counted_by_sort_of_word():
    rows = [{"sort": "offered", "entry": "tqi", "true": "a", "choice": "a"}, {"sort": "absent", "entry": "slẖ", "true": "a", "choice": "b"},
            {"sort": "offered", "entry": "ste", "true": "m", "choice": None}, {"sort": "absent", "entry": "kdi", "true": "w", "choice": "none"},
            {"sort": "offered", "entry": "kdi", "true": "w", "choice": "w"}, {"sort": "open", "entry": "wse", "true": None, "choice": "x"}]
    with B.run_83():
        assert B.by_sort(rows) == {B.OFFICE: {"absent: wrong": 1, "offered: right": 1}, B.OF_THE_FIRST: {"absent: none": 1, "offered: right": 1},
                                   B.OF_THE_FIVE: {"offered: no choice": 1}}
    assert B.SORTS is None                                                    # the first run's result has no count by sort


def test_the_figures_of_the_run_with_83_add_up():
    import collections
    f = figs83()
    c, rows = f["choice"], f["rows"]
    assert f["words"] == len(rows) == sum(f["sorts"].values()) == c["words"] == sum(f["packs_of"].values()) == 116 and len(f["packs_of"]) == B.PACKS_83
    assert f["answers"] == f["answers_expected"] == f["words"] * B.READERS and c["complete"] and all(sum(r["picks"].values()) == B.READERS for r in rows)
    assert (c["readers"], c["needed"], c["packs"]) == (B.READERS, B.NEEDED, B.PACKS_83) == (5, 5, 8) and c["bars"] == B.BARS
    assert f["seed"] == B.SEED_83 and f["layers"] == list(B.LAYERS_83) and f["groups_of_near_meanings"] == len(B.GROUPS_83) == 22 and f["groups_added"] == 5
    for r in rows:                                                              # a choice is what all five readers pick
        top = [m for m, n in r["picks"].items() if n == B.READERS]
        assert r["choice"] == (top[0] if top else None) and len(r["options"]) == 4 and set(r["picks"]) <= set(r["options"]) | {"none"}, r["entry"]
    acc = [r for r in rows if r["sort"] != "open"]
    off, ab = f["accepted_by_outcome"]["offered"], f["accepted_by_outcome"]["absent"]
    assert f["accepted"] == {"all": len(acc), "of_the_first_test": 38, "new": 45} and len(acc) == len(B.ACCEPTED_83) == 83
    assert sum(off.values()) == c["offered"] == f["sorts"]["offered"] and sum(ab.values()) == c["absent"] == f["sorts"]["absent"]
    assert all(r["true"] in r["options"] for r in acc if r["sort"] == "offered") and all(r["true"] not in r["options"] for r in acc if r["sort"] == "absent")
    assert (c["offered_chosen"], c["offered_right"]) == (off["right"] + off["wrong"], off["right"]) and c["absent_wrong"] == ab["wrong"] and "right" not in ab
    assert c["right_when_chosen"] == round(c["offered_right"] / c["offered_chosen"], 4) and c["wrong_when_absent"] == round(c["absent_wrong"] / c["absent"], 4)
    assert c["bar1"] == (c["offered_chosen"] >= B.BARS["chosen_at_least"] and c["right_when_chosen"] >= B.BARS["right_when_chosen"]) is True
    assert c["bar2"] == (c["wrong_when_absent"] <= B.BARS["wrong_when_absent"]) is False and c["labels_given"] is False
    assert len(f["wrong_choices"]) == off["wrong"] + ab["wrong"] and all(w["chosen"] != w["true"] for w in f["wrong_choices"])
    opened = [r for r in rows if r["sort"] == "open"]
    assert c["open_words"] == len(opened) == sum(c["open"].values()) == 33 and "favoured" not in c["open"]
    assert f["open_chosen"] == {r["entry"]: r["choice"] for r in opened if r["verdict"] == "chosen, no label"} and len(f["open_chosen"]) == c["open"]["chosen, no label"]
    assert sorted(w["entry"] for w in f["new_words"]) == sorted(B.NEW_83) and all(B.NEW_83[w["entry"]][0] == w["true"] for w in f["new_words"])
    assert f["further_entries"]["taken"] == f["further_entries"]["all"] == 45 and f["further_entries"]["left_out"] == {}
    # by sort of word: every accepted word once, and the sorts' counts are those of the two columns
    total = collections.Counter()
    for v in f["by_sort"].values():
        total.update(v)
    assert dict(total) == {f"offered: {k}": n for k, n in off.items()} | {f"absent: {k}": n for k, n in ab.items()}
    assert {k: sum(v.values()) for k, v in f["by_sort"].items()} == {B.OF_THE_FIRST: 38, B.OF_THE_FIVE: 5, B.OFFICE: 20, B.FORM: 15, B.NONE: 3, B.ALSO: 2}
    by_entry = {r["entry"]: r for r in acc}
    assert {h: v["sort"] for h, v in f["the_40"].items()} == B.OUT
    for h, v in f["the_40"].items():
        assert (v["meaning"], v["kind"]) == B.NEW_83[h] and v["meaning"] == by_entry[h]["true"], h
        assert (v["shown"], v["outcome"]) == (by_entry[h]["sort"], B.outcome(by_entry[h])), h
    again = collections.defaultdict(collections.Counter)
    for r in acc:
        again[B.SORT.get(r["entry"], B.OF_THE_FIRST)][f"{r['sort']}: {B.outcome(r)}"] += 1
    assert {k: dict(v) for k, v in again.items()} == f["by_sort"]
    cost = f["cost"]
    assert cost["agents"] == B.READERS * B.PACKS_83 == cost["with_a_count"] + len(cost["without_a_count"]) == 40 and cost["with_a_count"] == 31
    assert f["when"] == B.WHEN_83 and f["run_with_43"] == {k: figs()["choice"][k] for k in f["run_with_43"]}
    assert f["first_test"]["needed"] == 4 and f["places_shown_at_most"] == W.SHOWN and f["words_each_side"] == W.CHOICE_WIDTH


def test_the_figures_of_the_run_with_83_hold_only_wordings_that_were_public_or_are_ours():
    first = json.loads(B.FIRST.read_text(encoding="utf-8"))["choice"]["rows"]
    public = {m for r in first for m in r["options"] + r["candidates"] + ([r["true"]] if r["true"] else [])} | {"none"}
    ours = {m for m, _ in B.NEW_83.values()}
    f = figs83()
    for r in f["rows"]:
        for m in r["options"] + r["candidates"] + list(r["picks"]) + [x for x in (r["true"], r["choice"]) if x]:
            assert m in public | ours, (r["entry"], m)
    import lexicon as X
    assert all(len(X.words_of(m)) <= X.LONGEST for m in ours)
    if B.PACK_WORDING.exists():                                                # the packs' wording of four meanings stays local
        theirs = B.pack_wording()
        assert set(theirs) <= ours and len(theirs) == 4
        for name in ("data/discovery/blind_test_83_figures.json", "data/discovery/blind_test_83.md", "src/blind2.py"):
            assert not any(v in (ROOT / name).read_text(encoding="utf-8") for v in theirs.values()), name


def test_the_page_of_the_run_with_83_says_what_the_figures_say():
    import datetime
    f, text = figs83(), page83()
    c, w, acc = f["choice"], f["when"], f["accepted"]
    off, ab = f["accepted_by_outcome"]["offered"], f["accepted_by_outcome"]["absent"]
    hm = lambda t: t[:5]                                                   # noqa: E731
    pct = lambda x: f"{100 * x:.1f}%"                                      # noqa: E731
    # what was set before the readers
    assert '"No, do not waive". So the test is run again with all 83.' in text and f"Set: all {acc['all']} (section 2)." in text
    assert f"**The accepted words: {acc['all']}.** The {len(B.ACCEPTED)} of the last run, and the {len(B.OUT)} it left out" in text
    for label, key in (("A title of which only the kind of office is known", B.OFFICE), ("A form or a variant of a word of the test", B.FORM),
                       ("No meaning of its own in the lexicon, or not of the four kinds", B.NONE), ("Also an open word of the test", B.ALSO)):
        assert f"| {label} | {len(B.MORE[key])} |" in text, key
    office = {m: sum(v[0] == m for v in B.MORE[B.OFFICE].values()) for m in B.COARSE_83}
    assert all(f'"{m}" ({n})' in text for m, n in office.items()) and sum(office.values()) == 20 and B.MORE[B.FORM]["kroro"][0] == B.TITLE
    assert all(f'"{B.NEW_83[h][0]}"' in text for h in ("pesto", "qor", "qorise", "dḫe", "apote-lẖ", "qetneyineqeli", "qetrri", "dot", "pke", "dik", "l (2)", "wi (1)", "qor-o"))
    assert f"{c['absent']} of the {acc['all']}. The other {c['offered']} are shown with it." in text and f"**The open words: {c['open_words']},**" in text
    assert "Five groups of near meanings are added" in text and f["groups_added"] == 5 and "**A coarse meaning is never a filler.**" in text
    assert f"five for each of {c['packs']} packs ({f['words']} words), each a fresh agent (Opus): {f['cost']['agents']}. Seed {f['seed']}." in text
    assert f"(of {c['absent']}: two at most)" in text and int(B.BARS["wrong_when_absent"] * c["absent"]) == 2
    assert "those of the map with its six layers" in text and len(f["layers"]) == 6
    assert "**This is the third run of the test, and the first two each missed a bar.**" in text
    # the result
    assert f"## 6. The result (counted at {hm(w['counted'])}, no label given)" in text
    assert (f"The first {w['readers_before_the_limit']} readers were started from {hm(w['started'])}, after the commit with the bars ({w['set']}); "
            f"their answers came between {hm(w['first_answer'])} and {hm(w['last_answer_before_the_limit'])}. Then the session's usage limit stopped the launch.") in text
    secs = lambda t: datetime.timedelta(hours=int(t[:2]), minutes=int(t[3:5]), seconds=int(t[6:8])).total_seconds()   # noqa: E731
    late = round((secs(w["resumed"]) - secs(w["set"])) / 60)
    assert (f"The last {w['readers_after_the_limit']} readers (three of pack 7 and the five of pack 8) were started at {hm(w['resumed'])}, {late} minutes after "
            f"the commit, when the limit was lifted; their answers came at {hm(w['last_answer'])}.") in text and hm(w["first_answer_after"]) == hm(w["last_answer"])
    assert w["readers_before_the_limit"] + w["readers_after_the_limit"] == f["cost"]["agents"] and late == 72
    assert f"the {f['cost']['agents']} packs and the key were written at {w['packs_written']} and not again" in text
    assert f"Every reader answered every word of its pack ({f['words']} words, five readers each)." in text
    assert f"| Every reader answers every word | {f['answers']} of {f['answers_expected']} answers | met |" in text
    assert f"| {c['offered_right']} of {c['offered_chosen']} right ({pct(c['right_when_chosen'])}) | met |" in text
    assert f"| **{c['absent_wrong']} of {c['absent']} ({pct(c['wrong_when_absent'])})** | **missed** |" in text
    assert f"| | Shown with their meaning ({c['offered']}) | Shown without it ({c['absent']}) |" in text
    assert f"| All five pick the true meaning | {off['right']} | (not offered) |" in text and f"| All five pick a wrong meaning | {off['wrong']} | {ab['wrong']} |" in text
    assert f"| All five say \"none of these\" | {off['none']} | {ab['none']} |" in text and f"| No choice (the five differ) | {off['no choice']} | {ab['no choice']} |" in text
    wrong = {(x["sort"], x["true"], x["chosen"]) for x in f["wrong_choices"]}
    assert wrong == {("offered", "wife", "mother's kin"), ("absent", "general", "governor"), ("absent", "to plunder", "to send"),
                     ("absent", "small, young", "great, elder"), ("absent", "a favourable sacrifice", "life"),
                     ("absent", "an administrative title", "chief envoy"), ("absent", "a priestly title", "temple administrator")}
    assert '"wife" was taken for "mother\'s kin"' in text
    assert ('"general" was taken for "governor", "to plunder" for "to send", "small, young" for "great, elder", "a favourable sacrifice" for "life", '
            '"an administrative title" for "chief envoy", and "a priestly title" for "temple administrator"') in text
    forty = [0, 0]
    for label, key in (("One of the 38 of the first test", B.OF_THE_FIRST), ("One of the five that the run with 43 added", B.OF_THE_FIVE),
                       ("A title of which only the kind of office is known", B.OFFICE), ("A form or a variant of a word of the test", B.FORM),
                       ("No meaning of its own, or not of the four kinds", B.NONE), ("Also an open word of the test", B.ALSO)):
        v = f["by_sort"][key]
        right, chosen = v.get("offered: right", 0), v.get("offered: right", 0) + v.get("offered: wrong", 0)
        wrongly, absent = v.get("absent: wrong", 0), sum(n for k, n in v.items() if k.startswith("absent"))
        assert f"| {label} | {sum(v.values())} | {right} of {chosen} | {wrongly} of {absent} |" in text, key
        if key in B.MORE:
            forty = [forty[0] + right, forty[1] + chosen]
    assert f"The {len(B.OUT)} words that are new here" in text and f"({forty[0]} of {forty[1]})" in text and forty[0] == forty[1]
    v = f["by_sort"][B.OF_THE_FIRST]
    assert f"among the 38 words of the first test, {v['absent: wrong']} of {sum(n for k, n in v.items() if k.startswith('absent'))} got a wrong choice" in text
    assert f"**The open words ({c['open_words']}), had the bars held.**" in text
    for label, key in (("All five pick the same proposal (no label)", "chosen, no label"), ("All five pick a filler", "a filler chosen"),
                       ('All five say "none of these"', "none of the four"), ("No choice", "no choice")):
        assert f"| {label} | {c['open'][key]} |" in text, key
    eight = f["open_chosen"]
    assert eight == {"pl (2)": "lord of", "wse": "of the country", "penn": "year", "mlowi": "health", "pqrtr": "great prince", "yed": "silver",
                     "wi (1)": "brother", "qomlise": "good god"}
    assert ("The eight are `pl` (lord of), `wse` (of the country), `penn` (year), `mlowi` (health), `pqrtr` (great prince), `yed` (silver), `wi` (brother) "
            "and `qomlise` (good god). They carry no label.") in text
    before = figs()["open_chosen"]
    assert len(set(before) & set(eight)) == 6 and all(before[k] == eight[k] for k in set(before) & set(eight)) and set(before) - set(eight) == {"ẖol"}
    assert {r["entry"]: r["verdict"] for r in f["rows"] if r["entry"] == "ẖol"} == {"ẖol": "no choice"}
    assert "Six of them had all five readers of the run with 43 too; `ẖol`, chosen then, got no choice now." in text
    fillers = {r["entry"]: r["choice"] for r in f["rows"] if r["sort"] == "open" and r["verdict"] == "a filler chosen"}
    assert fillers == {"attḫ": "a great meal", "amero": "priest of Amun"} and 'The two fillers chosen: "a great meal" for `attḫ` and "priest of Amun" for `amero`.' in text
    # the three runs side by side
    one, two = json.loads(B.FIRST.read_text(encoding="utf-8"))["choice"], f["run_with_43"]
    for label, needs_, r in (("The first test", "four of five", one), ("The run with 43 accepted words", "all five", two), ("This run, with 83", "all five", c)):
        assert (f"| {label} | {needs_} | {r['offered_right']} of {r['offered_chosen']} ({pct(r['right_when_chosen'])}) | "
                f"{r['absent_wrong']} of {r['absent']} ({pct(r['wrong_when_absent'])}) |") in text, label
    assert one["needed"] == 4 and "**This is the method's third miss.**" in text and "**The pattern of the run with 43 held with 83 words.**" in text
    assert "The lexicon calls it a variant of `akroro`, which is not in the test" in text and B.OUT["kroro"] == B.FORM
    cost = f["cost"]
    assert (f"Cost: {cost['agents']} readers. {cost['with_a_count']} of them reported {cost['tokens_counted']:,} tokens together") in text
    assert "The other nine wrote their complete answer files" in text and len(cost["without_a_count"]) == 9 and "none is estimated here" in text
    assert "A label is not a translation" in text and "No meaning found here is the project's own." in text
    # the review's correction of section 2, which stands as it was written before the readers
    o = f["options"]
    near = o["open_words_with_near_proposals"]
    assert "proposals of the open words, those of the word's kind first, never two near meanings." in text and o["words"] == f["words"]
    assert (f"under {len(near)} open words ({', '.join(f'`{e}`' for e in near)}) two or three of the four are near meanings") in text
    assert f"The four options hold both an accepted meaning and a proposal under {o['of_both_sorts']} of the {o['words']} words." in text
    def close(a, b):                                                            # the run's rule, in the wording of the figures
        return bool(W.content(a) & W.content(b)) or any(a in g and b in g for g in B.GROUPS_83)
    for r in f["rows"]:                                                         # no filler is near another option
        own = [r["true"]] if r["true"] else r["candidates"]
        fillers = [m for m in r["options"] if m not in own]
        assert not any(close(m, x) for i, m in enumerate(fillers) for x in own + fillers[:i]), r["entry"]
    assert set(near) == {r["entry"] for r in f["rows"] if r["sort"] == "open" and any(close(a, b) for a in r["candidates"] for b in r["candidates"] if a != b)}
    accepted = {m for m, _ in B.ACCEPTED_83.values()}
    proposals = {m for r in f["rows"] if r["sort"] == "open" for m in r["candidates"]}
    assert o["of_both_sorts"] == sum(bool(set(r["options"]) & accepted and set(r["options"]) & proposals) for r in f["rows"])


def test_the_figures_of_the_run_with_83_need_the_packs_wording():
    """Without the local file of the packs' wording, the figures of the run with 83 are not counted: they would carry
    a wording that follows the lexicon's for four words in a row."""
    saved = B.PACK_WORDING
    B.PACK_WORDING = B.HOME_83 / "no such file.json"
    try:
        assert stops(B.figures_83, "the figures would carry the packs' wording of four meanings")
    finally:
        B.PACK_WORDING = saved


def test_the_summaries_name_the_run_with_83():
    c = figs83()["choice"]
    for name in ("README.md", "NEXT_STEPS.md", "REPORT.md"):
        text = " ".join((ROOT / name).read_text(encoding="utf-8").split())
        assert "blind_test_83.md" in text and '"No, do not waive"' in text, name
        assert f"{c['offered_right']} of {c['offered_chosen']}" in text and f"{c['absent_wrong']} of {c['absent']}" in text, name
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "`words-83`, `packs-83` and `count-83`" in readme and "third miss" in readme
    assert "`data/sources/g6b/`" in (ROOT / "data/INDEX.md").read_text(encoding="utf-8")
    assert "blind_test_83.md" in (ROOT / "data/discovery/blind_test_2.md").read_text(encoding="utf-8")
    prompts = " ".join((ROOT / "runs/prompts/G6_choice_83.md").read_text(encoding="utf-8").split())
    assert "data/sources/g6b/packs/K<n>_r<r>.md" in prompts and "word for word" in prompts


def test_the_figures_of_the_run_with_83_are_the_count_of_the_local_files():
    needs(*LOCAL_83)
    assert B.figures_83() == figs83()
    names = {f"K{n}_r{r}": B.HOME_83 / f"reader{r}" / f"K{n}.jsonl" for n in range(1, B.PACKS_83 + 1) for r in range(1, B.READERS + 1)}
    key = json.loads((B.HOME_83 / "key.json").read_text(encoding="utf-8"))
    size = {n: sum(w["pack"] == n for w in key["words"].values()) for n in range(1, B.PACKS_83 + 1)}
    for name in figs83()["cost"]["without_a_count"]:                            # the nine without a count wrote complete files
        assert len(names[name].read_text(encoding="utf-8").splitlines()) == size[int(name[1])], name


def test_the_script_writes_the_packs_of_the_run_with_83():
    """As for the first run: the packs again in a folder of its own, the answers copied in afterwards: byte for byte
    the packs of the run, its key and its result with the count by sort."""
    needs(*LOCAL_83, *MAP_83, "data/sources/g6b/packs")
    with B.run_83():
        live = B.HOME
        with tempfile.TemporaryDirectory() as d:
            B.HOME = Path(d)
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    B.packs()
                    assert (B.HOME / "key.json").read_bytes() == (live / "key.json").read_bytes()
                    names = sorted(p.name for p in (live / "packs").iterdir())
                    assert len(names) == B.READERS * B.PACKS == 40 and names == sorted(p.name for p in (B.HOME / "packs").iterdir())
                    assert all(filecmp.cmp(B.HOME / "packs" / n, live / "packs" / n, shallow=False) for n in names)
                    assert "`data/sources/g6b/reader1/K1.jsonl`" in (B.HOME / "packs" / "K1_r1.md").read_text(encoding="utf-8")
                    for r in range(1, B.READERS + 1):
                        shutil.copytree(live / f"reader{r}", B.HOME / f"reader{r}", dirs_exist_ok=True)
                    assert stops(B.packs, "the readers have answered")
                    B.count()
                    assert (B.HOME / "result.json").read_bytes() == (live / "result.json").read_bytes()
            finally:
                B.HOME = live
    assert W.NEEDED == 4 and B.HOME == ROOT / "data/sources/g6"


def test_one_pack_of_the_run_with_83_shows_one_hidden_spelling():
    """Pack 5 hides the words for "nephew, niece" and for "child". In one place they are joined in one word, and the
    pack shows the letters of the second as a piece cut off the first. No other pack shows a hidden spelling, and
    neither of the two words counted for a bar: all five said "none" of the first, and made no choice for the second."""
    needs(*LOCAL_83, *MAP_83, "data/sources/g6b/packs")
    with B.run_83():
        shown = hidden_spellings_shown()
        key = B.read("key.json")
        assert shown == [(5, r, "mete") for r in range(1, B.READERS + 1)]
        two = {w["entry"]: c for c, w in key["words"].items() if w["pack"] == 5 and w["entry"] in ("yetmde", "mte")}
        for r in range(1, B.READERS + 1):
            body = (B.HOME / "packs" / f"K5_r{r}.md").read_text(encoding="utf-8")
            assert re.findall(r"(?<![A-Za-zḫẖšñ])mete(?![A-Za-zḫẖšñ])\S*", body) == [f"mete-l-{two['yetmde']}-lowi"], r
    rows = {r["entry"]: r for r in figs83()["rows"] if r["sort"] != "open"}
    assert (rows["yetmde"]["sort"], B.outcome(rows["yetmde"])) == ("absent", "none") and (rows["mte"]["sort"], B.outcome(rows["mte"])) == ("offered", "no choice")
    text = page83()
    assert "**One pack showed one hidden spelling.**" in text and "all five readers said \"none of these\" of the first and made no choice for the second" in text


def test_the_rules_of_the_run_with_83_were_in_git_before_its_readers():
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout
    w = B.WHEN_83
    assert git("log", "-1", "--format=%cI", w["set_in"]).strip() == f"2026-11-16T{w['set']}-08:00"
    assert (w["set"] < w["packs_written"] < w["started"] < w["first_answer"] <= w["last_launch_before_the_limit"] < w["last_answer_before_the_limit"]
            < w["resumed"] < w["first_answer_after"] <= w["last_answer"] < w["counted"])
    for phrase in ("## 3. The bars, set before any reader is started", "**The accepted words: 83.**", "**A coarse meaning is never a filler.**",
                   "**This is the third run of the test, and the first two each missed a bar.**"):
        out = git("log", "--reverse", "--format=%cI", f"-S{phrase}", "--", "data/discovery/blind_test_83.md").split()
        assert out and out[0][11:19] <= w["set"] and phrase in PAGE_83.read_text(encoding="utf-8"), phrase


def test_the_times_of_the_run_with_83_are_the_files():
    needs("data/sources/g6b/reader1", "data/sources/g6b/reader5", "data/sources/g6b/packs", "data/sources/g6b/key.json")
    import datetime
    import zoneinfo
    pacific = zoneinfo.ZoneInfo("America/Los_Angeles")
    at = lambda f: datetime.datetime.fromtimestamp(f.stat().st_mtime, pacific).strftime("%H:%M:%S")   # noqa: E731
    w = B.WHEN_83
    times = sorted(at(f) for r in range(1, B.READERS + 1) for f in (B.HOME_83 / f"reader{r}").glob("K*.jsonl"))
    before, after = w["readers_before_the_limit"], w["readers_after_the_limit"]
    assert len(times) == before + after == 40 and (times[0], times[before - 1]) == (w["first_answer"], w["last_answer_before_the_limit"]), times[:2]
    assert (times[before], times[-1]) == (w["first_answer_after"], w["last_answer"]), times[-2:]
    late = sorted(f"K{f.stem[1:]} r{r}" for r in range(1, B.READERS + 1) for f in (B.HOME_83 / f"reader{r}").glob("K*.jsonl") if at(f) > w["resumed"])
    assert late == sorted([f"K7 r{r}" for r in (3, 4, 5)] + [f"K8 r{r}" for r in range(1, 6)])       # three of pack 7 and the five of pack 8
    written = {at(f) for f in list((B.HOME_83 / "packs").glob("K*_r*.md")) + [B.HOME_83 / "key.json"]}
    assert written == {w["packs_written"]}, written                           # the packs and the key were not written again


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
