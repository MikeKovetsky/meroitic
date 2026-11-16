"""Checks for the open spellings that stand in one or two texts (src/rare.py, data/discovery/rare_spellings.md).

  python3 -I tests/test_rare.py

The map, the lexicon, the sources and the agents' answers are local only: the checks of the method run on made-up
words; the checks of the reported numbers read the public figures file, compare the page with it, and compare it
with a count from the local files where those are present.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import rare as R                     # noqa: E402
import recurring as W                # noqa: E402
import themap as M                   # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/rare_spellings.md"
LEX = {"ato": {"kind": "noun", "status": "established"}, "kb": {"kind": "verb", "status": "hypothesis"},
       "tlt": {"kind": "noun", "status": "hypothesis"}, "Ms": {"kind": "god name", "status": "hypothesis"},
       "-kete": {"kind": "function word", "status": "hypothesis"}, "-li (1)": {"kind": "function word", "status": "established"},
       "-erike-": {"kind": "verb", "status": "hypothesis"}, "-x": {"kind": "function word", "status": "unknown"}}


def word(form, level, *parts, gloss=""):
    return {"form": form, "level": level, "gloss": gloss, "parts": [{"form": f, "entry": e} for f, e in parts]}


def figs():
    return json.loads(R.PUBLIC.read_text(encoding="utf-8"))


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


# ---------------------------------------------------------------------------------------- what is laid in the map

def test_a_word_is_named_only_when_every_part_has_an_entry():
    assert R.named(word("atoli", "hypothesis", ("ato", "ato"), ("li", "-li (1)")))
    for odd in ("?", "NAME", "ending", "NUMBER", None):
        assert not R.named(word("xatoli", "hypothesis", ("x", odd), ("ato", "ato")))
    assert not R.named({"form": "ato", "level": "hypothesis"}) and not R.named(word("ato", "hypothesis"))


def test_a_stem_without_a_meaning_keeps_a_word_out_and_an_unsure_ending_does_not():
    g = word("kbatotlt", "hypothesis", ("kb", "kb"), ("ato", "ato"), ("tlt", "tlt"), ("x", "-x"), ("m", "Ms"))
    assert R.unsettled(g, LEX, set()) == ["kb", "tlt"]              # ato is sure, Ms a name, -x an ending
    assert R.unsettled(g, LEX, {"kb"}) == ["tlt"] and R.unsettled(g, LEX, {"kb", "tlt"}) == []
    assert R.unsettled(word("q", "hypothesis", ("q", "qqq")), LEX, set()) == ["qqq"]      # a stem the lexicon given does not hold


def test_a_stated_place_becomes_a_name_a_grammar_word_or_a_meaning_by_its_entry():
    assert [R.level_of(k, LEX) for k in ("Ms", "-kete", "kb", "-erike-")] == ["name", "grammar", "meaning", "meaning"]
    assert R.stated_entries({"a": {"verdict": "stated"}, "b": {"verdict": "not stated firmly"}}, {"c": {"verdict": "stated"}}) == {"a", "c"}


def made_up():
    gl = {"T1": [word("kbli", "hypothesis", ("kb", "kb"), ("li", "-li (1)")), word("xkb", "unknown", ("x", "?"), ("kb", "kb")),
                 word("kbtlt", "hypothesis", ("kb", "kb"), ("tlt", "tlt")), word("Ms", "hypothesis", ("Ms", "Ms")),
                 word("kete", "hypothesis", ("kete", "-kete")), word("wo", "kind"), word("woSi", "name", gloss="Isis"),
                 word("to", "kind"), word("tome", "hypothesis"), word("ra", "kind")]}
    forms = [g["form"] for g in gl["T1"]]
    its = {"kb": {"how": "stem", "places": [{"text": "T1", "n": i, "form": forms[i - 1]} for i in (1, 2, 3)]},
           "Ms": {"how": "stem", "places": [{"text": "T1", "n": 4, "form": "Ms"}]},
           "-kete": {"how": "affix", "places": [{"text": "T1", "n": 5, "form": "kete"}]},
           "wo": {"how": "stem", "places": [{"text": "T1", "n": n, "form": forms[n - 1]} for n in (6, 8, 10)]}}
    rows = [{"item": "kb", "place": 1, "verdict": "stated"}, {"item": "kb", "place": 2, "verdict": "stated"},
            {"item": "kb", "place": 3, "verdict": "stated"}, {"item": "Ms", "place": 1, "verdict": "stated"},
            {"item": "-kete", "place": 1, "verdict": "stated"}, {"item": "wo", "place": 1, "verdict": "piece", "whole": "woSi"},
            {"item": "wo", "place": 2, "verdict": "piece", "whole": "tome"}, {"item": "wo", "place": 3, "verdict": "piece", "whole": "rara"},
            {"item": "kb", "place": 1, "verdict": "open"}, {"item": "kb", "place": 1, "verdict": "not agreed"}]
    verified = {k: {"verdict": "stated", "one": {"meaning": f"meaning of {k}", "source": "Rilly 2021", "page": 7}} for k in its}
    return gl, its, rows, verified


def test_only_the_places_the_rules_allow_are_laid():
    gl, its, rows, verified = made_up()
    lines, apart = R.lines_of("g4", gl, its, rows, verified, LEX, {"kb"})
    got = [(o["form"], o["level"], o["why"], o["was"]) for o in lines]
    assert got == [("kbli", "meaning", "stated", "hypothesis"),          # every part named, the stem stated
                   ("Ms", "name", "stated", "hypothesis"),               # the entry is a name
                   ("kete", "grammar", "stated", "hypothesis"),          # an ending written as a word of its own
                   ("wo", "name", "piece", "kind")]                      # a piece of a name the map holds
    assert lines[0]["gloss"] == "meaning of kb" and lines[0]["source"] == "Rilly 2021, p. 7" and lines[0]["item"] == "kb"
    assert lines[3]["gloss"] == "part of woSi: Isis"
    assert apart == {"stated, stem, a part of the spelling unnamed": 1,              # xkb
                     "stated, stem, another stem without a meaning": 1,              # kbtlt: tlt has none
                     "piece, the whole word open in the map": 1, "piece, the whole word not a form of the map": 1}
    # with tlt stated too, kbtlt is laid; for g2 the reason is "form"
    more, _ = R.lines_of("g2", gl, its, rows[:3], verified, LEX, {"kb", "tlt"})
    assert [(o["form"], o["why"]) for o in more] == [("kbli", "form"), ("kbtlt", "form")]
    # an item that no longer fits the map stops the build
    its["Ms"]["places"][0]["form"] = "ms"
    assert stops(lambda: R.lines_of("g4", gl, its, rows, verified, LEX, set()), "the map has 'Ms'")
    # the lines fit src/themap.py: laid over the map they change exactly these words
    its["Ms"]["places"][0]["form"] = "Ms"
    out = M.lay(gl, lines, "x")
    assert [g["level"] for g in out["T1"]] == ["meaning", "unknown", "hypothesis", "name", "grammar", "name", "name", "kind", "hypothesis", "kind"]


def test_the_stated_places_are_split_as_the_rule_for_the_map_needs():
    gl, its, rows, _ = made_up()
    assert R.by_kind("g4", gl, its, rows, LEX, {"kb"}) == {"ending, every part named": 1, "stem, a part unnamed": 1,
                                                          "stem, another stem without a meaning": 1, "stem, every part named": 2}


def test_the_entries_and_the_words_of_the_dictionary():
    gl, its, rows, verified = made_up()
    lines, _ = R.lines_of("g4", gl, its, rows, verified, LEX, {"kb"})
    assert R.dictionary_words(lines, LEX) == ["kb"]                     # Ms is a name, -kete an ending, wo a piece
    assert R.entries_of(its, lines, rows, LEX) == {"with_a_stated_place": 3, "laid_as_a_translated_word": 2, "laid_as_a_name_only": 1,
                                                   "none_laid": 0, "dictionary_words_given_a_meaning": 1}
    sure = {**LEX, "kb": {"kind": "verb", "status": "probable"}}
    assert R.dictionary_words(lines, sure) == []                        # a word the lexicon calls sure is given nothing new


# ------------------------------------------------------------------------------------------------- the readings

def test_the_reading_that_counts_is_the_first_that_met_its_bar():
    home = R.HOME
    with tempfile.TemporaryDirectory() as d:
        R.HOME = Path(d)
        try:
            for rnd, taken in ((1, False), (2, True)):
                f = Path(d) / "g4" / R.FOLDER[rnd] / "result.json"
                f.parent.mkdir(parents=True)
                f.write_text(json.dumps({"taken": taken, "rows": [rnd]}), encoding="utf-8")
            assert R.taken("g4") == (2, {"taken": True, "rows": [2]}) and list(R.readings("g4")) == [1, 2]
            (Path(d) / "g4" / "places2" / "result.json").write_text(json.dumps({"taken": False, "rows": []}), encoding="utf-8")
            assert stops(lambda: R.taken("g4"), "no reading of the places met its bar")
            assert R.readings("g2") == {} and stops(lambda: R.taken("g2"), "no reading")
            # a pack is not written again once an agent has answered
            (Path(d) / "g4" / "places" / "answers1").mkdir()
            (Path(d) / "g4" / "places" / "answers1" / "P01.jsonl").write_text("{}\n", encoding="utf-8")
            assert stops(lambda: R.answered("g4", ["places/answers1", "places/answers2"]), "places/answers1 hold answers")
            R.answered("g4", ["places2/answers1"])
        finally:
            R.HOME = home


def test_the_briefs_differ_from_the_recurring_words_brief_only_as_said():
    assert R.G4_BRIEF.replace("Each\nstands in one or two texts.", "Each\nstands in three texts or more.") == W.PLACE_BRIEF
    assert '"stated": the spelling here is a form of the word (or the ending) of the lexicon' in R.G2_BRIEF
    assert "established or probable. Each stands in one or\ntwo texts." in R.G2_BRIEF and R.G2_BRIEF.count('"stated"') == W.PLACE_BRIEF.count('"stated"')
    second = R.G4_BRIEF.replace(R.REPLY, R.COUNTED.format(places=41))
    assert "This pack lists 41 places: your file must have 41 lines" in second and second.replace(R.COUNTED.format(places=41), R.REPLY) == R.G4_BRIEF
    prompts = (ROOT / "runs/prompts/RARE_places.md").read_text(encoding="utf-8")
    for brief in (R.G2_BRIEF, R.G4_BRIEF):
        assert "\n".join(("    " + l).rstrip() for l in brief.strip("\n").splitlines()) in prompts      # what the checkers were given is public
    assert " ".join(R.COUNTED.split()) in " ".join(prompts.replace("{{", "{").replace("}}", "}").split())


def test_the_leads_find_a_headword_as_a_word_of_its_own():
    pages = {"Rilly 2016": [(3, "The word ked-b-to is a verb."), (4, "Of kedeto nothing is said."), (9, "KEDBTO again")],
             "Rilly 2021": [(n, "no such word") for n in range(1, 4)]}
    assert R.leads("kedbto", pages) == {"Rilly 2016": [3, 9]}            # hyphens and case ignored; not inside kedeto
    assert R.leads("-bto (2)", pages) == {} and R.leads("to", pages) == {}        # a part of a longer word; under three letters
    assert R.plain("-bḫe- (2)") == "bxe" and R.plain("Aẖo") == "aho"
    many = {"Rilly 2016": [(n, "the word mlo") for n in range(1, 20)], "Rilly 2021": []}
    assert R.leads("mlo", many) == {"Rilly 2016": list(range(1, 9))}     # eight pages at most


def test_the_items_are_the_open_spellings_in_one_or_two_texts_of_the_kinds_asked():
    lex = {"ato": {"headword": "ato", "kind": "noun", "status": "established", "page": 1, "meaning": "", "proposals": []},
           "kb": {"headword": "kb", "kind": "verb", "status": "hypothesis", "page": 2, "meaning": "", "proposals": []}}
    gl = {f"T{i}": [word("kbli", "hypothesis", ("kb", "kb")), word("atol", "hypothesis", ("ato", "ato")), word("zz", "unknown", ("zz", "?")),
                    word("ato", "meaning", ("ato", "ato"))] for i in (1, 2)}
    gl["T3"] = [word("kbx", "hypothesis", ("kb", "kb")), word("mm", "hypothesis", ("kb", "kb"))]
    for t in ("T4", "T5", "T6"):
        gl[t] = [word("mm", "hypothesis", ("kb", "kb"))]                 # mm stands in four texts: not rare
    rows = {t: {"site": "Faras", "kind": "funerary"} for t in gl}
    g4 = R.items_of(gl, rows, lex, R.KIND["g4"])
    assert [(it["item"], it["how"], sorted(f["form"] for f in it["forms"]), it["uses"], it["texts"]) for it in g4] == [("kb", "stem", ["kbli", "kbx"], 3, 3)]
    assert [(p["text"], p["n"]) for p in g4[0]["places"]] == [("T1", 1), ("T2", 1), ("T3", 1)] and "**kbli**" in g4[0]["places"][0]["words"]
    g2 = R.items_of(gl, rows, lex, R.KIND["g2"])
    assert [(it["item"], it["how"], it["uses"]) for it in g2] == [("ato", "stem, sure in the lexicon", 2)]        # the open spelling atol, not ato


# ------------------------------------------------------------------------------------ the figures and the pages

def test_the_figures_add_up():
    f = figs()
    g2, g4 = f["g2"], f["g4"]
    for run, g in f.items():
        res = g["readings"][str(g["reading_taken"])]
        assert res["taken"] and res["answered by both"] == res["places"] == g["places_judged"]["places"] and res["kappa"] >= res["bar"] == W.KAPPA
        assert all(not g["readings"][k]["taken"] for k in g["readings"] if int(k) < g["reading_taken"]), run
        assert sum(res["verdicts"].values()) == res["places"] and sum(g["stated"].values()) == res["verdicts"]["stated"]
        laid, out = g["laid"], g["left_out"]
        reason = "form" if run == "g2" else "stated"
        assert set(laid["why"]) == {reason, "piece"} and laid["lines"] == sum(laid["why"].values()) == sum(laid["to"].values()) == sum(laid["was"].values())
        assert laid["why"][reason] == sum(n for k, n in g["stated"].items() if k.endswith("every part named"))
        assert laid["why"][reason] + sum(n for k, n in out.items() if k.startswith("stated")) == res["verdicts"]["stated"]
        assert laid["why"]["piece"] + sum(n for k, n in out.items() if k.startswith("piece")) == res["verdicts"]["piece"]
        assert {w: sum(v.values()) for w, v in laid["to_by_why"].items()} == laid["why"] and set(laid["was"]) <= set(W.OPEN)
        e = g["the_entries"]
        assert e["laid_as_a_translated_word"] + e["laid_as_a_name_only"] + e["none_laid"] == e["with_a_stated_place"] <= g["places_judged"]["entries"]
        assert sum(g["entries_that_are"].values()) == g["entries"] and all(c["agents"] and c["tokens"] for c in g["cost"].values())
    assert (g2["entries"], g2["spellings"], g2["places"], g4["entries"], g4["spellings"], g4["places"]) == (116, 312, 366, 323, 784, 1033)
    assert g2["places_judged"] == {"entries": 116, "places": 366} and g2["the_entries"]["dictionary_words_given_a_meaning"] == 0
    # G4: the first reading missed the bar on an unanswered place, not on the checkers' agreement
    first = g4["readings"]["1"]
    assert not first["taken"] and first["kappa"] >= first["bar"] and first["answered by both"] == first["places"] - 1 and g4["reading_taken"] == 2
    lit, a = g4["literature"], g4["class_a"]
    assert lit["quote_found"] == lit["statements"] and lit["items"] == g4["entries"] == sum(lit["classes"].values()) and lit["batches"] == g4["cost"]["literature"]["agents"]
    assert a["entries"] == lit["classes"]["A"] == sum(a["verdicts"].values()) and sum(a["stated_by"].values()) == sum(a["stated_that_are"].values()) == a["verdicts"]["stated"]
    assert set(a["stated_by"]) == {"Rilly 2016", "Rilly 2021"} and g4["places_judged"]["entries"] == lit["classes"]["A"] + lit["classes"]["B"]
    assert g4["the_entries"]["with_a_stated_place"] <= a["verdicts"]["stated"]
    words = g4["words"]
    assert len(words) == g4["the_entries"]["dictionary_words_given_a_meaning"] and {w["entry"]: w["meaning"] for w in words} == R.MEANINGS
    assert all(w["places_laid"] >= 1 and w["source"] in a["stated_by"] for w in words)


def test_the_figures_agree_with_the_map():
    """The two layers of the map hold what the figures say is laid, and the north star's gain is the new words."""
    f, m = figs(), json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    layers = {l["name"]: l for l in m["layers"]}
    assert [l["name"] for l in M.LAYERS][-2:] == list(R.LAYER.values()) == ["rare_sure", "rare_later"]
    for run, name in R.LAYER.items():
        l, laid = layers[name], f[run]["laid"]
        assert (l["places"], l["why"], l["to"], l["was"]) == (laid["lines"], laid["why"], laid["to"], laid["was"]), run
    new = sum(w["new_to_the_map"] for w in f["g4"]["words"])
    assert m["north_star"]["translated_by_a_layer"] == {"recurring": 9, "rare_sure": 0, "rare_later": new}


def test_the_figures_hold_no_wording_but_ours():
    def strings(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from strings(v, k)
        elif isinstance(o, list):
            for v in o:
                yield from strings(v, key)
        elif isinstance(o, str):
            yield key, o
    lex_kinds = {"", "noun", "verb", "title", "epithet", "adjective", "function word", "numeral or measure"}
    for key, v in strings(figs()):
        assert key in ("entry", "kind", "meaning", "source") and (key != "meaning" or v in R.MEANINGS.values()) \
            and (key != "kind" or v in lex_kinds) and (key != "source" or v in ("Rilly 2016", "Rilly 2021")), (key, v)
    import lexicon as X
    assert all(len(X.words_of(v)) <= X.LONGEST for v in R.MEANINGS.values())


def test_the_page_says_what_the_figures_say():
    f, text, m = figs(), page(), json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    g2, g4, n = f["g2"], f["g4"], m["north_star"]
    L = {l["name"]: l["after"] for l in m["layers"]}
    r2, r4a, r4 = g2["readings"]["1"], g4["readings"]["1"], g4["readings"]["2"]
    judged = g2["places_judged"]["places"] + g4["places_judged"]["places"]
    lines = g2["laid"]["lines"] + g4["laid"]["lines"]
    apart = sum(v for g in (g2, g4) for k, v in g["left_out"].items() if k.startswith("stated"))
    new = sum(w["new_to_the_map"] for w in g4["words"])
    assert f"Two checkers judged {judged:,} places of rare spellings" in text and f"{lines} of them now carry a meaning or a name in the map: {g2['laid']['lines']} where" in text
    assert f"go from {pct(L['recurring']['running']['share'])} to {pct(L['rare_later']['running']['share'])}, and {new} more words of the lexicon have a meaning" in text
    assert f"({n['translated'] - new} to {n['translated']} of about {n['distinct_words']['point']:,}," in text and f"the word at {apart} more places that are not laid" in text
    # G2
    assert f"answered all {r2['places']} places. Their Cohen's kappa is {r2['kappa']:.2f} (bar {r2['bar']})" in text
    s2, s4 = g2["stated"], g4["stated"]
    assert f"Of the {r2['verdicts']['stated']} stated places, {g2['laid']['why']['form']} are laid." in text
    assert f"at {s2['stem, every part named']} of them and leaves a part unnamed at {s2['stem, a part unnamed']}" in text
    assert f"{s2['ending, every part named']} with every part named, {s2['ending, a part unnamed']} with a part unnamed" in text
    to = g2["laid"]["to_by_why"]["form"]
    assert f"{to.get('meaning', 0)} a meaning, {to.get('name', 0)} a name (the entry is a god, a person or a place), {to.get('grammar', 0)} a grammar word" in text
    e2, e4 = g2["the_entries"], g4["the_entries"]
    assert f"{e2['with_a_stated_place']} of the {g2['entries']} entries have a stated place; {e2['laid_as_a_translated_word']} have one laid as a translated word, {e2['laid_as_a_name_only']} only as a name, {e2['none_laid']} none" in text
    # G4
    lit, a = g4["literature"], g4["class_a"]
    assert f"readers collected {lit['statements']:,} statements about the {g4['entries']} entries" in text
    assert f"{lit['classes']['A']} entries are of class A" in text and f"{lit['classes']['B']} of class B" in text and f"{lit['classes']['C']} of class C" in text
    assert f"For {a['verdicts']['stated']} of the {a['entries']} entries both readers find the meaning stated firmly" in text
    assert f"{a['stated_by']['Rilly 2021']} by Rilly 2021, {a['stated_by']['Rilly 2016']} by Rilly 2016" in text
    assert f"kappa was {r4a['kappa']:.2f}, but one place had one checker's answer only" in text and f"a kappa of {r4['kappa']:.2f} (bar {r4['bar']})" in text
    for k, label in (("stated", "the word the later source speaks of (stated)"), ("piece", "a piece of another word or of a name"),
                     ("open", "a word of its own that stays open"), ("unclear", "unclear"), ("not agreed", "not agreed"),
                     ("not answered by both", "answered by one checker only")):
        assert f"| {label} | {r4a['verdicts'].get(k, 0)} | {r4['verdicts'].get(k, 0)} |" in text, k
    assert f"Of the {r4['verdicts']['stated']} stated places, {g4['laid']['why']['stated']} are laid:** {s4['stem, every part named']} under a stem and {s4['ending, every part named']} under an ending" in text
    assert f"{e4['with_a_stated_place']} entries have a stated place; {e4['laid_as_a_translated_word']} have one laid as a translated word, {e4['laid_as_a_name_only']} only as a name, {e4['none_laid']} none" in text
    assert f"{e4['dictionary_words_given_a_meaning']} of the entries laid as translated words are words of the dictionary (no name, no ending); {new} of them are new to the map" in text
    for w in g4["words"]:
        assert f"| `{w['entry']}` | {w['meaning']} | {w['source']}, p. {w['page']} | {w['places_laid']} | {'yes' if w['new_to_the_map'] else 'no, the recurring words gave it'} |" in text, w["entry"]
    # the map and the cost
    for label, x in (("Before (the recurring words laid)", L["recurring"]), ("With G2's layer", L["rare_sure"]), ("With G4's layer too", L["rare_later"])):
        r, s = x["running"], x["spellings"]
        assert f"| {label} | {r['translated']:,} of {r['need']:,} | {pct(r['share'])} | {s['translated']:,} of {s['need']:,} | {pct(s['share'])} |" in text, label
    assert f"{n['translated']} of about {n['distinct_words']['point']:,} distinct words have a meaning, {pct(n['star']['point'])} (between {pct(n['star']['low'])} and {pct(n['star']['high'])})" in text
    cost = [c for g in (g2, g4) for c in g["cost"].values()]
    assert f"{sum(c['agents'] for c in cost)} agents (Opus, each a fresh one), {sum(c['tokens'] for c in cost):,} subagent tokens" in text
    for c in cost:
        assert f"{c['tokens']:,}" in text
    # the rules name the numbers of entries that are endings as the figures have them
    assert f"{g2['entries_that_are']['an ending or a particle']} of G2's {g2['entries']} entries and {g4['entries_that_are']['an ending or a particle']} of G4's {g4['entries']} are endings" in text


def test_the_summaries_name_the_step():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python3 -I tests/test_rare.py" in readme and "- `python3 -I src/rare.py public` (and " in readme
    steps = " ".join((ROOT / "NEXT_STEPS.md").read_text(encoding="utf-8").split())
    f, m = figs(), json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    c = m["current"]["running"]
    for text in (" ".join(readme.split()), steps):
        assert f"{c['translated']:,} of the {c['need']:,} running words that need a meaning" in text and pct(c["share"]) in text
        assert f"{m['north_star']['translated']} of about {m['north_star']['distinct_words']['point']:,}" in text
    assert "rare_spellings.md" in steps and f"{f['g2']['laid']['lines'] + f['g4']['laid']['lines']} places" in steps


# ------------------------------------------------------------------------------------------- with the local files

def test_the_figures_are_the_count_of_the_local_files():
    needs("data/sources/v6", "data/rilly2003", "data/sources/recurring/lit/verify/result.json", "data/sources/rare/g4/places2/result.json",
          "data/sources/rare/g2/places/result.json", *[l["file"] for l in M.LAYERS])
    assert R.figures() == figs()
    # the layers' files are what the rules give on the map with the layers before them
    lex = W.lexicon()
    stated = R.stated_entries(json.loads((R.RECURRING / "lit/verify/result.json").read_text(encoding="utf-8")),
                              json.loads((R.HOME / "g4/lit/verify/result.json").read_text(encoding="utf-8")))
    names = [l["name"] for l in M.LAYERS]
    try:
        for run, name in R.LAYER.items():
            _, _, lines, _ = R.build(run, M.current(upto=names.index(name)), lex, stated)
            assert lines == M.lines_of(M.LAYERS[names.index(name)]), run
    finally:
        W.OUT = R.RECURRING


def test_every_checker_answered_its_own_pack_in_full():
    needs("data/sources/rare/g4/places2/groups.json", "data/sources/rare/g2/places/groups.json")
    for run, folder in (("g2", "places"), ("g4", "places2")):
        groups = json.loads((R.HOME / run / folder / "groups.json").read_text(encoding="utf-8"))
        for c in (1, 2):
            got = W.place_answers(R.HOME / run / folder / f"answers{c}", groups)
            assert len(got) == sum(hi - lo for g in groups for _, lo, hi in g), (run, c)


def test_no_meaning_of_ours_follows_a_source_for_four_words():
    needs("data/rilly2003", "data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt")
    import lexicon as X
    import lexique as L

    def runs(text):
        w = X.words_of(re.sub(r"ffi|ffl|ff|fi|fl|\x00", "ꜰ", text.lower()))
        return {tuple(w[i: i + X.COPIED]) for i in range(len(w) - X.COPIED + 1)}
    grams = set()
    for e in L.load():
        for t in [v for v in e.values() if isinstance(v, str)] + [p.get("proposal") or "" for p in e.get("proposals") or []]:
            grams |= runs(t)
    for path in ("data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt"):
        text = re.sub(r"(?m)^\f?=== page \d+ ===$", " ", (ROOT / path).read_text(encoding="utf-8", errors="replace"))
        grams |= runs(text) | runs(re.sub(r"(?<=[^\W\d_])-[ \t]*\n\s*(?=[^\W\d_])", "", text))
    assert [m for m in R.MEANINGS.values() if runs(m) & grams] == []


def test_each_rule_was_in_git_before_the_answers_it_binds():
    """The page says each bar was committed before its agents were started: the commit that first held the rule is
    older than the first answer of the step, by the files' own times."""
    needs("data/sources/rare/g4/lit/answers", "data/sources/rare/g4/places/answers1", "data/sources/rare/g4/places2/answers1",
          "data/sources/rare/g2/places/answers1")

    def committed(phrase, path):
        out = subprocess.run(["git", "-C", str(ROOT), "log", "--reverse", "--format=%ct", f"-S{phrase}", "--", path],
                             capture_output=True, text=True).stdout.split()
        assert out, phrase
        return int(out[0])

    def first_answer(*folders):
        return min(os.path.getmtime(f) for d in folders for f in (R.HOME / d).glob("*.jsonl"))
    rules, prompts = "data/discovery/rare_spellings.md", "runs/prompts/RARE_places.md"
    assert committed("A place is **stated** only when both checkers say so", rules) < first_answer("g4/lit/answers")
    assert committed("G2: the spellings under an entry the lexicon calls sure", prompts) < first_answer("g2/places/answers1", "g2/places/answers2")
    assert committed("A stated place is laid as translated only where the map names every part", rules) < first_answer("g4/places/answers1", "g4/places/answers2")
    assert committed("G4, the second reading of the places", prompts) < first_answer("g4/places2/answers1", "g4/places2/answers2")
    # and the two additions that came after G2's checkers had answered are said to have
    assert committed("One rule added on 2026-11-16", rules) > first_answer("g2/places/answers1", "g2/places/answers2")
    assert "after G2's checkers had answered and before their answers were counted" in page()


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
