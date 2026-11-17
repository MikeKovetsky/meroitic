"""Checks for the map and its layers (src/themap.py, data/discovery/map_layers.md).

  python3 -I tests/test_themap.py

The map, the layers' files and the lexicon are local only: the checks of the method run on made-up words and
lines; the checks of the reported numbers read the public figures file, compare the page and the reporting skill
with it, and compare it with a count from the local files, and with the two studies' own counts, where those are
present.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import themap as M                   # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/map_layers.md"
SKILL = ROOT / ".claude/skills/reporting/SKILL.md"


def g(form, level, gloss="", **more):
    return {"form": form, "level": level, "gloss": gloss, "parts": [{"form": form, "entry": form}], **more}


def line(text, n, form, level="meaning", why="stated", **more):
    return {"text": text, "n": n, "form": form, "level": level, "gloss": "eat", "why": why, "source": "Rilly 2021, p. 12",
            "was": "hypothesis", "item": form, **more}


def figs():
    return json.loads(M.PUBLIC.read_text(encoding="utf-8"))


def page():
    return " ".join(PAGE.read_text(encoding="utf-8").split())


def stops(fn, part):
    try:
        fn()
    except SystemExit as e:
        assert part in str(e), e
        return True
    raise AssertionError("did not stop")


# ---------------------------------------------------------------------------------------------------- the layers

def test_a_layer_changes_only_the_words_it_names_and_leaves_the_base_alone():
    gl = {"T1": [g("ato", "meaning", "water"), g("xrkete", "hypothesis", "may you eat (?)", evidence="x")], "T2": [g("wo", "hypothesis")]}
    out = M.lay(gl, [line("T1", 2, "xrkete"), line("T2", 1, "wo", level="name", why="piece", gloss="part of woSi: Isis")], "recurring")
    w = out["T1"][1]
    assert (w["level"], w["gloss"], w["source"], w["by"], w["why"], w["was"]) == ("meaning", "eat", "Rilly 2021, p. 12", "layer: recurring", "stated", "hypothesis")
    assert w["form"] == "xrkete" and w["parts"] == gl["T1"][1]["parts"] and w["evidence"] == "x"      # the rest of the word stays
    assert out["T2"][0]["level"] == "name" and out["T1"][0] is gl["T1"][0]
    assert gl["T1"][1]["level"] == "hypothesis" and "by" not in gl["T1"][1]                          # the base is not touched
    assert M.lay(gl, [], "empty") == gl


def test_a_layer_that_does_not_fit_the_map_stops_the_build():
    gl = {"T1": [g("ato", "meaning"), g("xrkete", "hypothesis")]}
    assert stops(lambda: M.lay(gl, [line("T1", 2, "xrkte")], "x"), "no word 'xrkte' at ('T1', 2)")          # another spelling
    assert stops(lambda: M.lay(gl, [line("T1", 3, "xrkete")], "x"), "no word")                             # past the end
    assert stops(lambda: M.lay(gl, [line("T1", 0, "ato")], "x"), "no word")                                # words are numbered from 1
    assert stops(lambda: M.lay(gl, [line("T9", 1, "ato")], "x"), "no word")                                # no such text
    assert stops(lambda: M.lay(gl, [line("T1", 2, "xrkete"), line("T1", 2, "xrkete")], "x"), "two lines")
    assert stops(lambda: M.lay(gl, [line("T1", 2, "xrkete", level="hypothesis")], "x"), "the level 'hypothesis'")   # a layer only resolves
    assert stops(lambda: M.lay(gl, [line("T1", 2, "xrkete", why="a guess")], "x"), "the reason 'a guess'")
    # a line must say the level the word has: the figures count what the layers moved from it
    assert stops(lambda: M.lay(gl, [line("T1", 1, "ato", why="form")], "x"), "has the level 'meaning' in the map, the line says 'hypothesis'")
    assert stops(lambda: M.lay(gl, [{k: v for k, v in line("T1", 2, "xrkete").items() if k != "was"}], "x"), "the line says None")
    # a later layer cannot change a word that an earlier one changed
    once = M.lay(gl, [line("T1", 2, "xrkete")], "first")
    assert stops(lambda: M.lay(once, [line("T1", 2, "xrkete", why="form", was="meaning")], "second"), "was changed by the layer first already")
    twice = M.lay(once, [line("T1", 1, "ato", why="form", was="meaning")], "second")
    assert (twice["T1"][0]["layer"], twice["T1"][1]["layer"]) == ("second", "first") and set(M.WHY) == {"stated", "form", "piece", "name"}


def test_the_layers_are_named_once_and_point_at_local_files_and_public_pages():
    names = [l["name"] for l in M.LAYERS]
    assert len(names) == len(set(names)) and names[0] == "recurring"
    ignored = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "--no-index", "--stdin"], input="\n".join(l["file"] for l in M.LAYERS),
                             capture_output=True, text=True).stdout.split()
    for l in M.LAYERS:
        assert l["file"] in ignored and l["file"].startswith("data/sources/"), l["name"]      # the lines hold glosses: local only
        assert (ROOT / l["page"]).is_file() and l["laid"] >= "2026-11-16" and l["what"], l["name"]


# ---------------------------------------------------------------------------------------------------- the counts

def test_the_counts_leave_names_numerals_and_lost_words_out_of_the_share():
    gl = {"T1": [g("ato", "meaning"), g("lo", "grammar"), g("Tneyi", "name"), g("12", "number"), g("x..", "lost"), g("al", "unknown")],
          "T2": [g("al", "kind"), g("al", "meaning"), g("ato", "hypothesis"), g("ato", "meaning"), g("yiteb", "hypothesis")]}
    c = M.counts(gl)
    assert c["running"] == {"translated": 4, "named": 2, "open": 4, "lost": 1, "need": 8, "share": 0.5, "all": 11, "of_all": round(6 / 11, 4)}
    # a spelling has the level it has most often: `ato` is translated (2 of 3), `al` is open (2 of 3)
    assert c["spellings"] == {"translated": 2, "named": 2, "open": 2, "lost": 1, "need": 4, "share": 0.5, "all": 7}
    empty = M.counts({})
    assert empty["running"]["share"] is None and empty["running"]["of_all"] is None and empty["spellings"]["all"] == 0


def test_a_layer_gives_a_dictionary_word_a_meaning_only_by_a_stated_place():
    lex = {"ḫr": {"status": "hypothesis"}, "ato": {"status": "established"}, "wte": {"status": ""}, "pqr": {"status": "hypothesis"}}
    known = {"ḫr", "ato", "wte"}
    one = [line("T", 1, "x", item="ḫr"), line("T", 2, "x", item="ḫr"),            # twice stated: one word
           line("T", 3, "x", item="ato"),                                         # translated by the lexicon already
           line("T", 4, "x", item="wte", why="piece"), line("T", 5, "x", item="pqr"),   # a piece; a word that is not in use
           {"text": "T", "n": 6, "form": "x", "why": "stated"}]                   # a line without an item
    two = [line("U", 1, "x", item="ḫr"), line("U", 2, "x", item="wte")]
    got = M.given_by_layers([("first", one), ("second", two)], known, lex)
    assert got == {"first": ["ḫr"], "second": ["wte"]}                            # a word counts for the first layer that gives it
    # a stated place laid as a name gives no word a meaning, and neither does a form of a word the lexicon calls sure
    assert M.given_by_layers([("x", [line("T", 1, "x", item="wte", level="name"), line("T", 2, "x", item="ḫr", why="form")])], known, lex) == {"x": []}


def test_the_north_star_before_us_is_the_north_star():
    lex = {"a": {"status": "established"}, "b": {"status": "probable"}, "c": {"status": "hypothesis"}, "d": {"status": "unknown"}}
    unnamed = {"point": 96, "low": 60, "high": 116}
    n = M.north_star({"a", "b", "c", "d"}, lex, [("recurring", [line("T", 1, "x", item="c")])], unnamed)
    assert (n["dictionary_words"], n["translated_by_the_lexicon"], n["translated_by_a_layer"], n["translated"]) == (4, 2, {"recurring": 1}, 3)
    assert n["distinct_words"] == {"point": 100, "low": 64, "high": 120}
    assert n["star"] == {"point": 0.03, "low": round(3 / 120, 4), "high": round(3 / 64, 4)} and n["before_us"] == n["star"]


def test_the_estimate_is_carried_while_few_stems_go_and_made_again_from_the_sample_when_more_do():
    import words as D
    words = {"unnamed_stems": 1000, "unnamed_words": {"point": 800, "low": 700, "high": 900}}
    never = lambda: stops(lambda: None, "the sample must not be read")              # noqa: E731
    stems = lambda n: {f"s{i}" for i in range(n)}                                   # noqa: E731
    drawn = lambda: stems(1000)                                                     # noqa: E731
    assert M.unnamed_words(words, stems(1000), never, drawn) == (words["unnamed_words"], {"sampled": 1000, "now": 1000})
    assert M.unnamed_words(words, stems(980), never, drawn) == (words["unnamed_words"], {"sampled": 1000, "now": 980})     # DRIFT is 2%
    assert stops(lambda: M.unnamed_words(words, stems(1001), never, drawn), "1 of them not among the 1000")              # a stem the sample never saw
    # a stem the sample never saw stops the count also when the layers took others out, so that the number is lower
    assert stops(lambda: M.unnamed_words(words, stems(990) | {"new"}, never, drawn), "draw and judge a new sample")
    assert stops(lambda: M.unnamed_words(words, stems(900) | {"new"}, never, drawn), "(new)")
    # past DRIFT: the sampled stems that are still unnamed, by the rule of the count of distinct words
    sample = {"s0": "word", "s1": "word", "s2": "same", "s3": "name", "s4": "unclear", "s5": "not agreed", "s990": "word", "s995": "piece"}
    got, rests = M.unnamed_words(words, stems(900), lambda: sample, drawn)
    left = {"word": 2, "same": 1, "name": 1, "unclear": 1, "not agreed": 1}         # s990 and s995 are no longer unnamed
    assert got == D.estimate(900, left) and got["point"] == round(900 * 2.5 / 4) and got["low"] <= got["point"] <= got["high"]
    assert rests == {"sampled": 1000, "now": 900, "sample_still_unnamed": 6, "its_verdicts": {"word": 2, "same": 1, "name": 1, "unclear": 1, "not agreed": 1}}
    assert M.DRIFT == 0.02


def test_a_share_is_rounded_once_from_its_counts():
    """156 of 1,284 is 12.1495%: 12.1%. Its share in the figures, 0.1215, would give 12.2% if it were rounded again."""
    n = {"translated": 156, "distinct_words": {"point": 1284, "low": 1023, "high": 1356}, "star": {"point": 0.1215, "low": 0.115, "high": 0.1525}}
    assert M.star_pct(n) == {"point": "12.1%", "low": "11.5%", "high": "15.2%"} and M.pct(n["star"]["point"]) == "12.2%"
    figs = {side: {"running": {"translated": 1215, "need": 10000, "share": 0.1215}, "spellings": {"translated": 1, "need": 3, "share": 0.3333}}
            for side in ("lookup", "base", "current")} | {"north_star": n}
    out = M.lines(figs)
    assert out[0] == "plain lookup: running words translated 1215 of 10000 = 12.2%; distinct spellings translated 1 of 3 = 33.3%"   # 12.15 exactly
    assert out[-1] == "north star: 156 of about 1284 = 12.1% (11.5% to 15.2%)"


# ------------------------------------------------------------------------------------ the figures and the pages

def test_the_figures_add_up():
    f = figs()
    assert [l["name"] for l in f["layers"]] == [l["name"] for l in M.LAYERS] and f["current"] == f["layers"][-1]["after"]
    before = f["base"]
    for l in f["layers"]:
        assert sum(l["why"].values()) == sum(l["to"].values()) == sum(l["was"].values()) == l["places"] and set(l["why"]) <= set(M.WHY)
        gained = sum(n for k, n in l["to"].items() if k in ("meaning", "grammar")) - sum(n for k, n in l["was"].items() if k in ("meaning", "grammar"))
        assert l["after"]["running"]["translated"] - before["running"]["translated"] == gained, l["name"]
        assert l["after"]["running"]["all"] == before["running"]["all"] and l["after"]["running"]["lost"] == before["running"]["lost"]
        before = l["after"]
    for c in (f["base"], f["current"], f["lookup"]):
        for side in ("running", "spellings"):
            s = c[side]
            assert s["translated"] + s["named"] + s["open"] + s["lost"] == s["all"] and s["need"] == s["translated"] + s["open"]
            assert s["share"] == round(s["translated"] / s["need"], 4)
    assert f["base"]["running"]["all"] == f["lookup"]["running"]["all"] == 10290 and f["inscriptions"] == 548
    assert f["lookup"]["running"]["share"] < f["base"]["running"]["share"] <= f["current"]["running"]["share"]
    n = f["north_star"]
    assert n["translated"] == n["translated_by_the_lexicon"] + sum(n["translated_by_a_layer"].values()) and n["before_us"] == n["star"]
    assert set(n["translated_by_a_layer"]) == {l["name"] for l in M.LAYERS}
    assert n["star"]["point"] == round(n["translated"] / n["distinct_words"]["point"], 4) and n["star"]["low"] <= n["star"]["point"] <= n["star"]["high"]
    u, w = n["unnamed_stems"], json.loads(M.WORDS.read_text(encoding="utf-8"))
    assert u["sampled"] == w["unnamed_stems"] >= u["now"]
    if u["sampled"] - u["now"] <= M.DRIFT * u["sampled"]:
        assert n["unnamed_words"] == w["unnamed_words"] and set(u) == {"sampled", "now"}
    else:                                                                # made again from the sampled stems still unnamed
        assert sum(u["its_verdicts"].values()) == u["sample_still_unnamed"] <= w["sample"]["sampled"]
        assert n["unnamed_words"]["low"] <= n["unnamed_words"]["point"] <= n["unnamed_words"]["high"] <= u["now"]
    assert n["distinct_words"] == {k: n["dictionary_words"] + v for k, v in n["unnamed_words"].items()}
    assert f["layers"][-1]["north_star"] == {k: n[k] for k in ("translated", "distinct_words", "star", "unnamed_stems")}
    left = u["sampled"]
    for l in f["layers"]:
        s = l["north_star"]
        assert s["translated"] == l["distinct_words_translated"] and s["star"]["point"] == round(s["translated"] / s["distinct_words"]["point"], 4), l["name"]
        assert s["unnamed_stems"]["sampled"] == u["sampled"] and s["unnamed_stems"]["now"] <= left, l["name"]       # a layer only takes stems out
        left = s["unnamed_stems"]["now"]


def test_the_figures_hold_counts_only():
    """Every value of the figures file is a number, but for the four words that describe a layer: no line of a
    layer, with its spelling, its meaning or its source, is in it."""
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
        assert isinstance(v, (int, float)) and not isinstance(v, bool) or key in ("name", "page", "laid", "what"), (key, v)
    described = {(l["name"], l["page"], l["laid"], l["what"]) for l in M.LAYERS}
    assert {(l["name"], l["page"], l["laid"], l["what"]) for l in figs()["layers"]} == described


def test_the_page_says_what_the_figures_say():
    f, text = figs(), page()
    pct = lambda x: f"{100 * x:.1f}%"                                     # noqa: E731
    of = lambda x: pct(x["translated"] / x["need"])                       # noqa: E731  a share divided from its counts, rounded once
    b, c, lk, n = f["base"], f["current"], f["lookup"], f["north_star"]
    for name, x in (("Plain lookup of the lexicon", lk), ("The base", b), ("With the layers", c)):
        r, s = x["running"], x["spellings"]
        assert f"| {name} | {r['translated']:,} of {r['need']:,} | {of(r)} | {s['translated']:,} of {s['need']:,} | {of(s)} | {pct(r['of_all'])} |" in text, name
    assert of(c["running"]) == M.lines(f)[2].split(" = ")[1].split(";")[0] != pct(c["running"]["share"])   # 4186 of 7077 is 59.149%: 59.1%, not 59.2%
    for l in f["layers"]:
        why = l["why"]
        assert (f"| `{l['name']}` | {l['laid']} | {l['places']} | {why.get('stated', 0)} | {why.get('form', 0)} | {why.get('piece', 0)} | {why.get('name', 0)} | "
                f"{of(l['after']['running'])} |") in text, l["name"]
        assert f"[{l['page'].split('/')[-1]}]({l['page'].split('/')[-1]})" in PAGE.read_text(encoding="utf-8"), l["name"]
    first = f["layers"][0]
    already = sum(first["was"].get(k, 0) for k in ("meaning", "grammar", "name"))
    assert f"{already} of its {first['places']} places were translated or named in the base already" in text
    s = M.star_pct(n)                                                    # a share is divided from its counts and rounded once
    assert f"{n['translated']} of about {n['distinct_words']['point']:,} distinct words, {s['point']} (between {s['low']} and {s['high']})" in text
    assert f"and {n['translated']} of about {n['distinct_words']['point']:,} distinct words ({s['point']})" in text
    n4 = {l["name"]: l for l in f["layers"]}["unnamed"]["north_star"]    # the example of a share rounded twice: the map with four layers
    assert f"With four layers, {n4['translated']} of {n4['distinct_words']['point']:,} is {100 * n4['translated'] / n4['distinct_words']['point']:.4f}%" in text
    assert f"holds the share rounded to four places, {n4['star']['point']}, and rounding that again gives {pct(n4['star']['point'])}" in text
    assert pct(n4["star"]["point"]) != M.star_pct(n4)["point"]
    assert f"{n['translated_by_the_lexicon']} by the lexicon of 2003 and {sum(n['translated_by_a_layer'].values())} by a later source" in text
    u = n["unnamed_stems"]
    assert f"The layers make {u['sampled'] - u['now']} of those stems names, so {u['now']:,} are left" in text and f"at most {100 * M.DRIFT:.0f}% of the stems" in text
    pieces = {l["name"]: l for l in f["layers"]}["unnamed"]["to"].get("meaning", 0)
    assert f"the {pieces} pieces of translated words that `unnamed` lays are such places" in text
    assert f"made again from the {u['sample_still_unnamed']} sampled stems that are still unnamed" in text
    assert f"about {n['unnamed_words']['point']} of the {u['now']:,} are words of their own (between {n['unnamed_words']['low']} and {n['unnamed_words']['high']})" in text
    by_name = {l["name"]: l for l in f["layers"]}
    three, four = (M.star_pct(by_name[k]["north_star"])["point"] for k in ("rare_later", "unnamed"))
    assert f"from {three} to {four}, is a correction of the count of words" in text
    by = n["translated_by_a_layer"]                                      # the fifth and the sixth layer take no stem; each gives two words a meaning
    for name in ("rare_millet", "leftover"):
        assert by_name[name]["north_star"]["unnamed_stems"] == by_name["unnamed"]["north_star"]["unnamed_stems"], name
    five = M.star_pct(by_name["rare_millet"]["north_star"])["point"]
    six = by_name["leftover"]
    assert by["rare_millet"] == by["leftover"] and f["layers"][-2] is six
    assert f"and the {by['leftover']} words each gives a meaning bring the north star from {four} to {five} and then to {M.star_pct(six['north_star'])['point']}" in text
    seven = f["layers"][-1]                                              # the seventh layer makes one more stem a name and gives no word a meaning
    gone = six["north_star"]["unnamed_stems"]["now"] - seven["north_star"]["unnamed_stems"]["now"]
    assert seven["name"] == "leftover_stems" and by["leftover_stems"] == 0 and gone == 1
    assert (seven["north_star"]["translated"], seven["north_star"]["distinct_words"]) == (n["translated"], n["distinct_words"])
    assert (f"The seventh, `leftover_stems`, makes {gone} more stem a name and gives no word a meaning: the count of distinct words goes from about "
            f"{six['north_star']['distinct_words']['point']:,} to about {n['distinct_words']['point']:,}, and the north star stays at {s['point']}") in text
    assert M.star_pct(six["north_star"])["point"] == s["point"]
    assert "The layers `rare_sure`, `unnamed` and `leftover_stems` add none" in text
    a = first["after"]                                                   # the map after the first layer alone
    gain = a["running"]["translated"] - b["running"]["translated"]
    names = a["running"]["named"] - b["running"]["named"]
    assert f"So {gain} running words more are translated, and {names} more are names" in text
    assert f"{b['running']['need']:,} words that need one become {a['running']['need']:,}" in text
    assert f"{first['to'].get('meaning', 0)} places become a meaning, {first['to'].get('name', 0)} a name, {first['to'].get('grammar', 0)} a grammatical function" in text
    was = first["was"]
    assert f"({was.get('meaning', 0)} with a meaning, {was.get('grammar', 0)} as a grammar word, {was.get('name', 0)} as a name)" in text
    assert f"The other {first['places'] - already} were open" in text
    assert f"({of(c['running'])}, from {of(b['running'])})" in text and f"({b['spellings']['translated']} to {a['spellings']['translated']})" in text
    assert (f"{by['recurring']} through the layer `recurring`, {by['rare_later']} through `rare_later` and {by['leftover']} through `leftover`; "
            f"Lipiński 2011: {by['rare_millet']} through `rare_millet`") in text
    assert by["rare_sure"] == by["unnamed"] == 0
    for l in f["layers"][1:]:
        to = l["to"]
        words = to.get("meaning", 0) + to.get("grammar", 0)
        become = "1 place becomes a translated word" if words == 1 else f"{words} places become translated words"
        assert f"{become} and {to.get('name', 0)} names; all {l['places']} were open" in text, l["name"]
        assert set(l["was"]) <= {"hypothesis", "kind", "unknown"}, l["name"]
    stated = sum(l["why"].get("stated", 0) for l in f["layers"] if l["name"] != "rare_millet")
    assert {l["name"] for l in f["layers"] if l["why"].get("stated")} == {"recurring", "rare_later", "leftover", "rare_millet"}
    both = json.loads((PAGE.parent / "leftover_parts_figures.json").read_text(encoding="utf-8"))
    left, again = both["part_2"], both["part_1_again"]
    assert {w["source"] for w in again["words"]} == {"Rilly 2016", "Rilly 2021"}
    mine = by_name["leftover"]                                           # the sixth layer is the second reading of the unnamed parts
    assert (mine["places"], mine["why"], mine["to"], mine["was"]) == (again["laid"]["lines"], again["laid"]["why"], again["laid"]["to"], again["laid"]["was"])
    assert (f"The {again['places']} places of steps G2 and G4 that `rare_sure` and `rare_later` left open: both checkers of those steps recognised the "
            f"word, but the map leaves a part of the spelling unnamed.") in text
    assert (f"{mine['why']['form']} forms of a word the lexicon calls sure and {mine['why']['stated']} places of a word for which Rilly states a meaning") in text
    assert "A place both checkers call a name is not laid." in text and "the second is the layer `leftover`" in text
    by_why = left["laid"]["to_by_why"]
    assert by_why["stated"] == {"name": by_name["rare_millet"]["why"]["stated"] - by_why["stated"]["meaning"], "meaning": sum(w["places_laid"] for w in left["words"])}
    assert f"The {stated} stated places of `recurring`, `rare_later` and `leftover` rest on Rilly's readings of 2016 and 2021.**" in text
    assert (f"The {by_name['rare_millet']['why']['stated']} stated places of `rare_millet` rest on Millet 2005 ({by_why['stated']['name']}, all of them names "
            f"of places) and on Lipiński 2011 ({by_why['stated']['meaning']}).") in text
    assert {w["source"] for w in left["words"]} == {"Lipinski 2011"}
    assert (f"({by_name['rare_millet']['why']['stated']}: {by_why['stated']['name']} of entries the lexicon files as place names, {by_why['stated']['meaning']} of the "
            f"{len(left['words'])} words Lipiński gives a meaning in full), {by_why['name']['name']} places of two entries that both readers say Millet calls a "
            f"personal name, and {by_why['piece']['name']} piece of a name the map holds") in text.replace("two words Lipiński", f"{len(left['words'])} words Lipiński")
    stems = json.loads((PAGE.parent / "leftover_stems_figures.json").read_text(encoding="utf-8"))
    assert (f"{left['the_places']['kappa']:.2f} for `rare_millet`, {again['kappa']:.2f} for `leftover` and {stems['kappa']:.2f} for `leftover_stems`, "
            f"against a bar of 0.6") in text
    laid = stems["laid"]                                                 # the seventh layer is the leftover stems
    assert (seven["places"], seven["why"], seven["to"], seven["was"]) == (laid["lines"], laid["why"], laid["to"], laid["was"])
    assert (f"The layer holds the places both call a name ({laid['to']['name']}) and the one place where both call the unnamed part an ending "
            f"({laid['to']['grammar']}); at no place did both recognise a word the lexicon knows.") in text
    assert laid["to"]["grammar"] == 1 and "known" not in stems["verdicts"] and stems["words"] == []
    g5 = json.loads((PAGE.parent / "second_scholar_later_figures.json").read_text(encoding="utf-8"))
    st = g5["statuses"]
    assert (f"Step G5 set each of Rilly's {g5['entries']} later meanings, those behind these places among them, beside what other scholars say: "
            f"{st['agreed by two scholars'] + st['agreed by two scholars, with a dissent']} are stated by another scholar too "
            f"({st['agreed by two scholars, with a dissent']} with a dissent), {st['disputed']} are disputed and {st['stated by one']} rest on Rilly alone") in text
    g3 = json.loads((PAGE.parent / "unnamed_spellings_figures.json").read_text(encoding="utf-8"))["readings"]
    assert f"{g3['pilot2']['kappa']:.2f} and {g3['full']['kappa']:.2f} for the two readings behind `unnamed`, and" in text
    # the coverage page's measure on the map as it stands is the last column of section 3, for the map with the layers
    assert f"Its measure on the map as it stands is the last column of section 3: {pct(c['running']['of_all'])}." in text


def test_the_cut_of_the_step_and_its_waiver_are_said_plainly():
    """G1 asked for the three pages that count from the map to be rebuilt. They are not, and Mike waived it (2026-11-16,
    13:52, "Yes, waive it."): every page that tells of the step says so in his words, and none says it still waits."""
    for path in ("data/discovery/map_layers.md", "NEXT_STEPS.md", "REPORT.md", "README.md", ".claude/skills/reporting/SKILL.md"):
        text = " ".join((ROOT / path).read_text(encoding="utf-8").split())
        assert '"Yes, waive it."' in text, path
        assert "waits for Mike's word" not in text and "waiting for Mike's word" not in text, path
    assert "NOT MET as written, on purpose, and waived by Mike on 2026-11-16 at 13:52" in page()
    steps = " ".join((ROOT / "NEXT_STEPS.md").read_text(encoding="utf-8").split())
    assert "Not built as the step said: the three pages that count from the map" in steps and "and Mike waived it on 2026-11-16 at 13:52" in steps


def test_the_pages_that_keep_the_base_point_here():
    """The studies run on the analysts' map keep their numbers and say where the map as it stands is counted."""
    f = figs()
    for name in ("v6_readers.md", "lexicon.md", "f4_rounds.md", "recurring_words.md"):
        text = (PAGE.parent / name).read_text(encoding="utf-8")
        assert "[map_layers.md](map_layers.md)" in text, name
        assert f"]({name})" in PAGE.read_text(encoding="utf-8"), name
    # the coverage page's own figure is the base's wider measure (translated or named, of all words): the page, its
    # figures file and the map's figures agree on it
    v6 = " ".join((PAGE.parent / "v6_readers.md").read_text(encoding="utf-8").split())
    r = json.loads((PAGE.parent / "corpus_v6_readers.json").read_text(encoding="utf-8"))
    wide = f["base"]["running"]["translated"] + f["base"]["running"]["named"]
    assert f"| {f['base']['running']['all']:,} | {wide:,} | {100 * f['base']['running']['of_all']:.1f}% |" in v6 and wide in set(_numbers(r))


def _numbers(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from _numbers(v)
    elif isinstance(o, list):
        for v in o:
            yield from _numbers(v)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        yield o


def test_the_reporting_skill_reads_these_figures():
    skill = " ".join(SKILL.read_text(encoding="utf-8").split())
    f = figs()
    for key in ("`data/discovery/map_figures.json`", "`north_star.translated`", "`north_star.distinct_words.point`", "`north_star.star.point`",
                "`north_star.star.low`", "`north_star.star.high`", "`current.running.share`", "`lookup.running.share`",
                "`current.spellings.share`", "`lookup.spellings.share`", "`python3 -I src/themap.py`"):
        assert key in skill, key
    # the skill quotes what the command prints, line for line, so its example cannot go stale when a layer is laid
    raw = SKILL.read_text(encoding="utf-8")
    for l in M.lines(f):
        assert l + "\n" in raw, l


def test_the_figures_are_the_count_of_the_local_files():
    needs("data/sources/v6", "data/rilly2003", "data/sources/words/population.json", "data/sources/words/r2/result.json", *[l["file"] for l in M.LAYERS])
    assert M.figures() == figs()


def test_the_stated_places_rest_on_the_sources_the_page_names():
    """Section 6: the stated places of `recurring`, `rare_later` and `leftover` cite Rilly 2016 or 2021, each on an
    entry whose later meaning step G5 judged; those of `rare_millet` cite Millet 2005 (names of places) or Lipiński
    2011 (translated words)."""
    needs(*[l["file"] for l in M.LAYERS])
    g5 = json.loads((PAGE.parent / "second_scholar_later_figures.json").read_text(encoding="utf-8"))["by_entry"]
    for l in M.LAYERS:
        stated = [o for o in M.lines_of(l) if o["why"] == "stated"]
        if l["name"] in ("recurring", "rare_later", "leftover"):
            assert stated and all(o["source"].startswith(("Rilly 2016,", "Rilly 2021,")) and o["item"] in g5 for o in stated), l["name"]
        elif l["name"] == "rare_millet":
            assert sorted({(o["source"].split(",")[0], o["level"]) for o in stated}) == [("Lipinski 2011", "meaning"), ("Millet 2005", "name")]
        else:
            assert not stated, l["name"]


def test_the_two_studies_count_the_same():
    """The recurring open words counted the map with their overlay themselves, and the count of distinct words
    said what the north star would be with it: both agree with the map as it stands after the first layer."""
    f = figs()
    after = f["layers"][0]["after"]["running"]
    r = json.loads((ROOT / "data/discovery/recurring_words_figures.json").read_text(encoding="utf-8"))["recount"]
    assert (r["after"]["read"], r["after"]["names"], r["after"]["open"], r["after"]["lost"], r["after"]["share"]) == \
        (after["translated"], after["named"], after["open"], after["lost"], after["share"])
    assert (r["before"]["read"], r["before"]["share"]) == (f["base"]["running"]["translated"], f["base"]["running"]["share"])
    w = json.loads((ROOT / "data/discovery/distinct_words_figures.json").read_text(encoding="utf-8"))
    first = f["layers"][0]["distinct_words_translated"]              # what the count of distinct words gave beforehand as its "next"
    assert w["next"]["translated"] == first and w["next"]["star"] == f["layers"][0]["north_star"]["star"]
    assert f["layers"][-1]["distinct_words_translated"] == f["north_star"]["translated"]
    assert [l["distinct_words_translated"] for l in f["layers"]] == sorted(l["distinct_words_translated"] for l in f["layers"])
    assert w["translated"] == f["north_star"]["translated_by_the_lexicon"] and w["dictionary_words"] == f["north_star"]["dictionary_words"]
    assert w["map"]["running_translated"] == f["base"]["running"]["translated"] and w["lookup"]["translated"] <= w["translated"]


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
