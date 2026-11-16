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


def test_the_north_star_before_us_is_the_north_star():
    lex = {"a": {"status": "established"}, "b": {"status": "probable"}, "c": {"status": "hypothesis"}, "d": {"status": "unknown"}}
    unnamed = {"point": 96, "low": 60, "high": 116}
    n = M.north_star({"a", "b", "c", "d"}, lex, [("recurring", [line("T", 1, "x", item="c")])], unnamed)
    assert (n["dictionary_words"], n["translated_by_the_lexicon"], n["translated_by_a_layer"], n["translated"]) == (4, 2, {"recurring": 1}, 3)
    assert n["distinct_words"] == {"point": 100, "low": 64, "high": 120}
    assert n["star"] == {"point": 0.03, "low": round(3 / 120, 4), "high": round(3 / 64, 4)} and n["before_us"] == n["star"]


def test_the_estimate_is_carried_only_while_the_layers_take_few_stems():
    assert M.carried(1000, 1000) == {"sampled": 1000, "now": 1000} and M.carried(1000, 980) == {"sampled": 1000, "now": 980}
    assert stops(lambda: M.carried(1000, 979), "draw and judge a new sample")        # more than DRIFT of the stems went
    assert stops(lambda: M.carried(1000, 1001), "draw and judge a new sample")       # a stem the sample never saw
    assert M.DRIFT == 0.02


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
    u = n["unnamed_stems"]
    assert 0 <= u["sampled"] - u["now"] <= M.DRIFT * u["sampled"]
    assert u["sampled"] == json.loads(M.WORDS.read_text(encoding="utf-8"))["unnamed_stems"]


def test_the_figures_hold_counts_only():
    text = M.PUBLIC.read_text(encoding="utf-8")
    for word in ('"gloss"', '"source"', '"form"', '"text"', '"item"'):
        assert word not in text, word


def test_the_page_says_what_the_figures_say():
    f, text = figs(), page()
    pct = lambda x: f"{100 * x:.1f}%"                                     # noqa: E731
    b, c, lk, n = f["base"], f["current"], f["lookup"], f["north_star"]
    for name, x in (("Plain lookup of the lexicon", lk), ("The base", b), ("With the layers", c)):
        r, s = x["running"], x["spellings"]
        assert f"| {name} | {r['translated']:,} of {r['need']:,} | {pct(r['share'])} | {s['translated']:,} of {s['need']:,} | {pct(s['share'])} | {pct(r['of_all'])} |" in text, name
    for l in f["layers"]:
        why = l["why"]
        assert f"| `{l['name']}` | {l['laid']} | {l['places']} | {why.get('stated', 0)} | {why.get('piece', 0)} | {why.get('name', 0)} |" in text, l["name"]
        assert f"[{l['page'].split('/')[-1]}]({l['page'].split('/')[-1]})" in PAGE.read_text(encoding="utf-8"), l["name"]
    first = f["layers"][0]
    already = sum(first["was"].get(k, 0) for k in ("meaning", "grammar", "name"))
    assert f"{already} of its {first['places']} places were translated or named in the base already" in text
    assert f"{n['translated']} of about {n['distinct_words']['point']:,} distinct words, {pct(n['star']['point'])} (between {pct(n['star']['low'])} and {pct(n['star']['high'])})" in text
    assert f"{n['translated_by_the_lexicon']} by the lexicon of 2003 and {sum(n['translated_by_a_layer'].values())} by a later source" in text
    u, words = n["unnamed_stems"], json.loads(M.WORDS.read_text(encoding="utf-8"))
    assert f"a sample of the {u['sampled']:,} stems the base could not name. The layer makes {u['sampled'] - u['now']} of them names, so {u['now']:,} are left" in text
    assert f"(about {words['unnamed_words']['point']} of them are words)" in text and f"more than {100 * M.DRIFT:.0f}% of those stems" in text
    gain = c["running"]["translated"] - b["running"]["translated"]
    names = c["running"]["named"] - b["running"]["named"]
    assert f"So {gain} running words more are translated, and {names} more are names" in text
    assert f"{b['running']['need']:,} words that need one become {c['running']['need']:,}" in text
    assert f"{first['to'].get('meaning', 0)} places become a meaning, {first['to'].get('name', 0)} a name, {first['to'].get('grammar', 0)} a grammatical function" in text
    was = first["was"]
    assert f"({was.get('meaning', 0)} with a meaning, {was.get('grammar', 0)} as a grammar word, {was.get('name', 0)} as a name)" in text
    assert f"The other {first['places'] - already} were open" in text
    assert f"({pct(c['running']['share'])}, from {pct(b['running']['share'])})" in text and f"({b['spellings']['translated']} to {c['spellings']['translated']})" in text


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
    needs("data/sources/v6", "data/rilly2003", *[l["file"] for l in M.LAYERS])
    assert M.figures() == figs()


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
    if len(M.LAYERS) == 1:
        assert w["next"]["translated"] == f["north_star"]["translated"] and w["next"]["star"] == f["north_star"]["star"]
    assert w["translated"] == f["north_star"]["translated_by_the_lexicon"] and w["dictionary_words"] == f["north_star"]["dictionary_words"]
    assert w["map"]["running_translated"] == f["base"]["running"]["translated"] and w["lookup"]["translated"] <= w["translated"]


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
