"""Checks for the count of distinct words (src/words.py, data/discovery/distinct_words.md).

  python3 -I tests/test_words.py

The map, the lexicon of 2003 and the checkers' answers are local only: the checks of the method run on made-up
words and answers; the checks of the reported numbers read the public figures file, compare the page and the
summaries with it, and compare it with a count from the local files where those are present.
"""
import contextlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import words as D                    # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/distinct_words.md"
LOCAL = "data/sources/words"
LEX = {"kdi": {"kind": "noun", "status": "established"}, "ḫr": {"kind": "verb", "status": "hypothesis"},
       "mlo": {"kind": "adjective", "status": "probable"}, "-lo": {"kind": "function word", "status": "established"},
       "-kete": {"kind": "function word", "status": "hypothesis"}, "ps-": {"kind": "function word", "status": "hypothesis"},
       "Akine": {"kind": "place name", "status": "hypothesis"}, "Amni": {"kind": "god name", "status": "established"}}


def g(form, level, *parts):
    return {"form": form, "level": level, "parts": [{"form": f, "entry": e} for f, e in parts]}


def figs():
    return json.loads(D.PUBLIC.read_text(encoding="utf-8"))


def page():
    return " ".join(PAGE.read_text(encoding="utf-8").split())


def between(text, start, end):
    assert text.count(start) == 1, start
    i = text.index(start)
    return text[i: text.index(end, i + len(start))]


def lines(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join((r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)) + "\n" for r in rows), encoding="utf-8")


# ------------------------------------------------------------------------------------------- what each word is

def test_a_running_word_is_a_dictionary_word_a_name_or_an_unnamed_stem():
    # the map's own names, numerals and lost words are not counted at all
    assert D.identity(g("Tneyi", "name", ("Tneyi", "NAME")), LEX) == ("none", ())
    assert D.identity(g("12", "number"), LEX) == ("none", ())
    assert D.identity(g("k..i", "lost", ("k..i", "kdi")), LEX) == ("none", ())
    # every spelling of one entry is that entry, whatever its endings and its level
    assert D.identity(g("kdilo", "meaning", ("kdi", "kdi"), ("lo", "-lo")), LEX) == ("dictionary", ("kdi",))
    assert D.identity(g("pSxrkete", "hypothesis", ("pS", "ps-"), ("xr", "ḫr"), ("kete", "-kete")), LEX) == ("dictionary", ("ḫr",))
    assert D.identity(g("kdimlo", "meaning", ("kdi", "kdi"), ("mlo", "mlo")), LEX) == ("dictionary", ("kdi", "mlo"))
    # a word of endings and particles only counts for those
    assert D.identity(g("pSkete", "kind", ("pS", "ps-"), ("kete", "-kete")), LEX) == ("dictionary", ("ps-", "-kete"))
    # built on a name and on no stem: a name, by the lexicon or by the map's own mark
    assert D.identity(g("akiNlo", "hypothesis", ("akiN", "Akine"), ("lo", "-lo")), LEX) == ("name", ())
    assert D.identity(g("arkiwlo", "hypothesis", ("arkiw", "NAME"), ("lo", "-lo")), LEX) == ("name", ())
    # a name beside a stem is the stem's word
    assert D.identity(g("amnikdi", "hypothesis", ("amni", "Amni"), ("kdi", "kdi")), LEX) == ("dictionary", ("kdi",))
    # no stem the lexicon has: the longest piece the map could not name, else the whole spelling
    assert D.identity(g("diyXokete", "unknown", ("diyXo", "?"), ("kete", "-kete")), LEX) == ("stem", ("diyXo",))
    assert D.identity(g("atetbx", "unknown", ("a", "?"), ("tetbx", "?")), LEX) == ("stem", ("tetbx",))
    assert D.identity(g("yiteb", "unknown"), LEX) == ("stem", ("yiteb",))
    assert D.identity(g("yiteb", "unknown", ("yiteb", "not an entry")), LEX) == ("stem", ("yiteb",))
    # a piece left over beside a known stem is no word of its own
    assert D.identity(g("kditllw", "unknown", ("kdi", "kdi"), ("tllw", "?")), LEX) == ("dictionary", ("kdi",))
    # the signs S and s, X and x are different signs: a stem keeps its case
    assert D.identity(g("Sxi", "unknown", ("Sxi", "?")), LEX)[1] != D.identity(g("sXi", "unknown", ("sXi", "?")), LEX)[1]


LEX2 = dict(LEX, **{"Mso": {"kind": "name", "status": "hypothesis"}, "Mlo": {"kind": "people name", "status": "established"},
                    "at (1)": {"kind": "title", "status": "hypothesis"}, "-erike-": {"kind": "verb", "status": "established"},
                    "t- (1)": {"kind": "function word", "status": "hypothesis"}, "-se": {"kind": "", "status": "established"}})


def test_the_north_star_counts_no_ending_and_no_name_as_a_word():
    """counted(): identity() as set, with the review's two corrections, and nothing else changed."""
    c = lambda w: D.counted(*D.identity(w, LEX2), LEX2)                                     # noqa: E731
    assert [D.ending(h, LEX2) for h in ("-lo", "ps-", "t- (1)", "-se", "-erike-", "kdi", "Mso")] == [True] * 4 + [False] * 3
    # an entry of the kinds "name" and "people name" was a word as set; it is a name, and a stem beside it stays
    assert D.identity(g("mSo", "hypothesis", ("mSo", "Mso")), LEX2) == ("dictionary", ("Mso",))
    assert c(g("mSo", "hypothesis", ("mSo", "Mso"))) == c(g("mlo", "hypothesis", ("mlo", "Mlo"))) == ("name", ())
    assert c(g("atmSo", "hypothesis", ("at", "at (1)"), ("mSo", "Mso"))) == ("dictionary", ("at (1)",))
    # an ending or a particle written as a word, or a word made only of them, is a piece, as the checkers' case has it
    assert D.identity(g("lo", "grammar", ("lo", "-lo")), LEX2) == ("dictionary", ("-lo",))
    assert c(g("lo", "grammar", ("lo", "-lo"))) == c(g("pSkete", "kind", ("pS", "ps-"), ("kete", "-kete"))) == ("piece", ())
    # a stem the lexicon writes with hyphens is a word, without the endings around it
    assert c(g("terikelowi", "meaning", ("t", "t- (1)"), ("erike", "-erike-"), ("lowi", "-lo"))) == ("dictionary", ("-erike-",))
    # nothing else changes, and an unnamed stem never does: the sample is drawn from the same stems
    for w in (g("kdilo", "meaning", ("kdi", "kdi"), ("lo", "-lo")), g("Tneyi", "name", ("Tneyi", "NAME")),
              g("akiNlo", "hypothesis", ("akiN", "Akine"), ("lo", "-lo")), g("diyXokete", "unknown", ("diyXo", "?"), ("kete", "-kete")),
              g("terikSelowi", "unknown", ("t", "t- (1)"), ("erik", "-erike-"), ("Se", "?"), ("lowi", "-lo")), g("yiteb", "unknown")):
        assert c(w) == D.identity(w, LEX2), w["form"]


def test_the_population_counts_each_entry_and_each_stem_once():
    gl = {"T1": [g("kdilo", "meaning", ("kdi", "kdi"), ("lo", "-lo")), g("kdi", "meaning", ("kdi", "kdi")), g("diyXokete", "unknown", ("diyXo", "?"), ("kete", "-kete")),
                 g("Tneyi", "name", ("Tneyi", "NAME")), g("akiNlo", "hypothesis", ("akiN", "Akine"), ("lo", "-lo"))],
          "T2": [g("diyXo", "unknown", ("diyXo", "?")), g("xrkete", "hypothesis", ("xr", "ḫr"), ("kete", "-kete")), g("yiteb", "unknown"), g("lo", "grammar", ("lo", "-lo"))]}
    known, stems, c = D.population_of(gl, LEX)
    assert dict(known) == {"kdi": 2, "ḫr": 1, "-lo": 1} and c == {"dictionary": 4, "stem": 3, "none": 1, "name": 1}
    assert sorted(stems) == ["diyXo", "yiteb"]
    assert stems["diyXo"] == {"stem": "diyXo", "uses": 2, "texts": 2, "forms": {"diyXokete": 1, "diyXo": 1}, "places": [["T1", 2], ["T2", 0]]}
    # translated: the entries in use that the lexicon calls established or probable
    assert D.translated(known, LEX) == ["-lo", "kdi"]
    # with the review's corrections the ending written as a word is a piece and a name of the kind "name" a name;
    # the stems are the same
    gl["T2"].append(g("mSo", "hypothesis", ("mSo", "Mso")))
    known, fixed, c = D.population_of(gl, LEX2, fix=True)
    assert dict(known) == {"kdi": 2, "ḫr": 1} and c == {"dictionary": 3, "stem": 3, "none": 1, "name": 2, "piece": 1} and fixed == stems
    assert dict(D.population_of(gl, LEX2)[0]) == {"kdi": 2, "ḫr": 1, "-lo": 1, "Mso": 1} and D.translated(known, LEX2) == ["kdi"]


# ---------------------------------------------------------------------------------------------------- the sample

def test_a_look_alike_is_one_sign_away_or_two_for_a_long_stem():
    assert D.distance("yiteb", "yitek") == 1 and D.distance("yiteb", "yiteb") == 0 and D.distance("yiteb", "yite") == 1
    assert D.distance("yiteb", "bitey") == 2 and D.distance("abc", "xyz") == 3 and D.distance("ab", "abcdef") == 3
    assert (D.reach("ab"), D.reach("abc"), D.reach("abcdef"), D.reach("abcdefg")) == (0, 1, 1, 2)
    pool = ["yitek", "yite", "yiteb", "bitey", "yitebxe", "kdi"]
    assert D.alikes("yiteb", pool) == ["yite", "yitek"]                  # the stem itself and what is two away are left out
    assert D.alikes("yitebxe", ["yiteb", "yitebxte", "yitebke"]) == ["yitebke", "yitebxte", "yiteb"]
    assert D.alikes("ab", ["ab", "abc", "a"]) == []                     # too short to compare
    assert len(D.alikes("abcd", [f"abc{c}" for c in "efghijkl"])) == D.ALIKE


def test_the_sample_is_drawn_by_the_seed_and_gives_every_stem_its_chance():
    stems = {f"s{i:04d}": {} for i in range(1000)}
    a = D.sample_of(stems)
    assert a == D.sample_of(dict(reversed(list(stems.items())))) and len(a) == len(set(a)) == D.SAMPLE == 240
    assert a != D.sample_of(stems, seed=D.SEED + 1) and set(a) <= set(stems)
    assert D.sample_of({"a": {}, "b": {}}) == ["a", "b"]
    hits = sum("s0007" in D.sample_of(stems, n=100, seed=s) for s in range(400))
    assert 20 <= hits <= 62                                              # about one draw in ten


def test_the_packs_are_not_written_again_once_answered():
    for rnd, folder in (("r1", "answers2"), ("r2", "r2/answers1")):
        with tempfile.TemporaryDirectory() as d:
            old, D.OUT = D.OUT, Path(d)
            try:
                lines(Path(d) / folder / "S01.jsonl", [{"stem": "a", "case": "word"}])
                try:
                    D.packs(rnd)
                    raise AssertionError("the packs were written over")
                except SystemExit as e:
                    assert "not written again" in str(e)
            finally:
                D.OUT = old


def test_the_second_reading_has_the_same_brief_with_its_rules():
    assert D.BRIEF2.replace(D.RULES2, "") == D.BRIEF and D.RULES2 in D.BRIEF2
    assert D.ROUNDS["r1"]["brief"] is D.BRIEF and D.ROUNDS["r2"]["brief"] is D.BRIEF2 and D.LAST == "r2"
    assert (D.ROUNDS["r1"]["folder"], D.ROUNDS["r2"]["folder"]) == ("", "r2/")
    text = page()
    for rule in ("A stem with no lost sign is a \"word\" unless something shown marks it as another case",
                 "\"Unclear\" only when a sign is lost in the stem's own word or in the word right before or after it",
                 "\"Name\" only when the place gives a reason", "\"Piece\" only when the word beside it completes it"):
        assert rule in text, rule


# ----------------------------------------------------------------------------------------------------- the count

def test_a_stem_has_a_case_only_when_both_checkers_give_it():
    assert D.verdict({"case": "word"}, {"case": "word"}) == "word"
    assert D.verdict({"case": "word"}, {"case": "name"}) == "not agreed"
    assert D.verdict({"case": "unclear"}, {"case": "unclear"}) == "unclear"
    assert D.verdict({"case": "word"}, None) == "not answered by both"


def test_a_checkers_file_counts_only_for_its_own_pack():
    groups = [["a", "b"], ["c"]]
    with tempfile.TemporaryDirectory() as d:
        lines(Path(d) / "S01.jsonl", [{"stem": "a", "case": "word"}, "not json", {"stem": "a", "case": "name"},
                                       {"stem": "c", "case": "word"}, {"stem": "b", "case": "maybe"}])
        lines(Path(d) / "S02.jsonl", [{"stem": "c", "case": "piece"}])
        got = D.sample_answers(Path(d), groups)
    assert {k: v["case"] for k, v in got.items()} == {"a": "word", "c": "piece"}


def test_the_interval():
    lo, hi = D.wilson(50, 100)
    assert round(lo, 3) == 0.404 and round(hi, 3) == 0.596
    assert D.wilson(0, 100)[0] == 0.0 and round(D.wilson(0, 100)[1], 3) == 0.037
    assert round(D.wilson(100, 100)[1], 9) == 1.0 and D.wilson(0, 0) == (0.0, 1.0)
    assert D.wilson(10.5, 100)[0] < 0.105 < D.wilson(10.5, 100)[1]       # a half count is a share like any other


def test_the_estimate_and_its_range():
    v = {"word": 40, "same": 10, "known": 20, "name": 15, "piece": 5, "unclear": 4, "not agreed": 6}     # 100 stems sampled
    e = D.estimate(1000, v)
    # the point: 45 words (a "same" counts a half) of the 90 decided, times the stems
    assert e["point"] == 500
    # the low end: 45 of all 100, at the lower bound; the high end: 45 and the 10 open ones, at the upper bound
    assert e["low"] == round(1000 * D.wilson(45, 100)[0]) and e["high"] == round(1000 * D.wilson(55, 100)[1])
    assert e["low"] < 450 < e["point"] < 550 < e["high"]
    assert D.estimate(1000, {"unclear": 3, "not agreed": 2})["point"] is None
    # the star: more unnamed words, a lower share
    s = D.star(160, 440, e)
    assert s == {"point": round(160 / 940, 4), "low": round(160 / (440 + e["high"]), 4), "high": round(160 / (440 + e["low"]), 4)}
    assert s["low"] < s["point"] < s["high"]


def pop_of(n=10):
    return {"stems": {f"s{i}": {"uses": 1} for i in range(n)}, "unnamed_stems": 1000, "dictionary_words": 440, "translated": 160,
            "before": {"translated": 130}}


def test_the_next_step_counts_only_words_in_use_that_a_later_source_gives():
    stated = [{"item": "ḫr", "places_stated": 3}, {"item": "-kete", "places_stated": 2}, {"item": "kdi", "places_stated": 5},
              {"item": "ps-", "places_stated": 0}, {"item": "Akine", "places_stated": 4}, {"item": "nowhere", "places_stated": 1}]
    with tempfile.TemporaryDirectory() as d:
        old, D.RECURRING = D.RECURRING, Path(d) / "figures.json"
        try:
            D.RECURRING.write_text(json.dumps({"class_a": {"stated": stated}}), encoding="utf-8")
            # kdi is sure in 2003 already, ps- holds in no place, Akine and nowhere are no dictionary word in use
            assert D.stated_later(LEX, {"ḫr": 1, "-kete": 1, "kdi": 2, "ps-": 1}) == ["-kete", "ḫr"]
            assert D.stated_later(LEX, {"ḫr": 1}) == ["ḫr"]
        finally:
            D.RECURRING = old


def test_nothing_is_taken_when_the_bar_is_missed():
    pop, groups = pop_of(), [[f"s{i}" for i in range(5)], [f"s{i}" for i in range(5, 10)]]
    cases = ["word", "word", "name", "known", "piece", "word", "name", "same", "word", "unclear"]
    one = {f"s{i}": {"case": c} for i, c in enumerate(cases)}
    out = D.results(pop, groups, one, dict(one))
    assert out["kappa"] == 1.0 and out["taken"] and out["verdicts"] == {"word": 4, "name": 2, "known": 1, "piece": 1, "same": 1, "unclear": 1}
    assert out["unnamed_words"]["point"] == 500 and out["distinct_words"]["point"] == 940
    assert out["star"]["point"] == round(160 / 940, 4) and out["star_before"]["point"] == round(130 / 940, 4)
    # a stem not answered by both: nothing is taken, whatever the agreement on the rest
    two = {k: v for k, v in one.items() if k != "s3"}
    out = D.results(pop, groups, one, two)
    assert out["kappa"] == 1.0 and not out["taken"] and "star" not in out and out["verdicts"]["not answered by both"] == 1
    # checkers who disagree at chance level: nothing is taken
    two = {f"s{i}": {"case": c} for i, c in enumerate(cases[5:] + cases[:5])}
    out = D.results(pop, groups, one, two)
    assert out["kappa"] < D.KAPPA and not out["taken"] and "unnamed_words" not in out


# ------------------------------------------------------------------------------------ the page and the figures

def test_the_bar_on_the_page_is_the_scripts():
    text = page()
    assert f"{D.SAMPLE} of the unnamed stems, drawn by a fixed seed" in text and f"in {D.SAMPLE // D.PACK} packs of {D.PACK}" in text
    assert f"is under {D.KAPPA}, or a stem is not answered by both, nothing is taken" in text
    assert "counts a half" in text and "95% interval" in text and D.Z == 1.96
    for case in D.CASES:
        assert f"- **{case}**:" in PAGE.read_text(encoding="utf-8"), case
    assert (D.SHOWN, D.WIDTH) == (6, 6) and "up to six places with six words on each side" in text


def test_the_prompts_are_in_the_repository():
    launch = (ROOT / "runs/prompts/WORDS_launch.md").read_text(encoding="utf-8")
    assert "`BRIEF`" in launch and "`BRIEF2`" in launch and "`RULES2`" in launch
    assert "data/sources/words/packs/S<nn>_c<1|2>.md" in launch and "data/sources/words/r2/packs/S<nn>_c<1|2>.md" in launch
    # the two launch lines, as quoted (indented four spaces): the same but for the path
    blocks = [" ".join(b.split()) for b in "\n".join(l if l.startswith("    ") else "\n" for l in launch.splitlines()).split("\n\n") if b.strip()]
    assert len(blocks) == 2 and blocks[1] == blocks[0].replace("data/sources/words/packs/", "data/sources/words/r2/packs/"), blocks
    assert "Do not use your own knowledge of Meroitic" in " ".join(D.BRIEF.split())
    for case in D.CASES:
        assert f'"{case}"' in D.BRIEF, case


def test_each_reading_was_set_before_its_checkers_answered():
    """The commit that set a reading's bar or rules is in this history and older than that reading's first answer
    file (local); the page names it."""
    for rnd, r in D.ROUNDS.items():
        sha = figs()["readings"][rnd]["set_in"]
        assert sha == r["set_in"] and f"`{sha}`" in PAGE.read_text(encoding="utf-8"), rnd
        assert subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", sha, "HEAD"]).returncode == 0, rnd
    needs(f"{LOCAL}/answers1", f"{LOCAL}/answers2", f"{LOCAL}/r2/answers1", f"{LOCAL}/r2/answers2")
    for rnd, r in D.ROUNDS.items():
        set_at = int(subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%ct", r["set_in"]], capture_output=True, text=True, check=True).stdout)
        first = min(f.stat().st_mtime for c in (1, 2) for f in (ROOT / LOCAL / f"{r['folder']}answers{c}").glob("*.jsonl"))
        assert set_at < first, (rnd, set_at, first)


def test_the_figures_add_up():
    f = figs()
    r = f["running"]
    assert sum(r.values()) == 10290 and r["stem"] == f["unnamed_running_words"]
    assert f["translated"] <= f["dictionary_words"] and f["unnamed_in_one_place"] <= f["unnamed_stems"]
    s = f["sample"]
    assert s["sampled"] == s["answered by both"] == sum(s["verdicts"].values()) == D.SAMPLE and s["seed"] == D.SEED
    assert s["taken"] is (s["kappa"] >= s["bar"]) and s["bar"] == D.KAPPA and s["taken"] and s["reading"] == D.LAST
    for rnd, r in f["readings"].items():
        assert r["sampled"] == r["answered by both"] == sum(r["verdicts"].values()) == D.SAMPLE and r["taken"] is (r["kappa"] >= r["bar"]), rnd
    assert not f["readings"]["r1"]["taken"] and {k: v for k, v in f["readings"][D.LAST].items() if k not in ("set_in", "not_agreed")} == {k: v for k, v in s.items() if k not in ("seed", "reading")}
    u = D.estimate(f["unnamed_stems"], s["verdicts"])
    assert f["unnamed_words"] == u and u["low"] <= u["point"] <= u["high"]
    assert f["distinct_words"] == {k: f["dictionary_words"] + v for k, v in u.items()}
    assert f["star"] == D.star(f["translated"], f["dictionary_words"], u)
    # before us is now (Mike, 2026-11-16): every translated word's meaning predates the project
    assert f["star_before"] == f["star"]
    assert f["next"]["translated"] == f["translated"] + f["next"]["stated_later"]
    assert f["next"]["star"] == D.star(f["next"]["translated"], f["dictionary_words"], u)
    assert f["star"]["point"] <= f["next"]["star"]["point"]
    # what a plain lookup reaches: the reach of the map, no part of the north star
    lk = f["lookup"]
    assert lk["translated"] <= f["translated"] and lk["dictionary_words"] <= f["dictionary_words"] and sum(lk["running"].values()) == sum(f["running"].values())
    # the first count, and what the review's corrections took out of it: the unnamed side is the same
    first, fix, r = f["first_count"], f["corrections"], f["running"]
    assert sum(first["running"].values()) == sum(r.values()) and first["running"]["stem"] == r["stem"] and first["running"]["none"] == r["none"]
    assert f["dictionary_words"] == first["dictionary_words"] - sum(c["entries"] for c in fix.values())
    assert f["translated"] == first["translated"] - sum(c["translated"] for c in fix.values())
    assert first["distinct_words"] == {k: first["dictionary_words"] + v for k, v in u.items()}
    assert first["star"] == D.star(first["translated"], first["dictionary_words"], u)
    assert r["piece"] == first["running"]["dictionary"] - r["dictionary"] - (r["name"] - first["running"]["name"])
    m = f["map"]
    assert m["running_words"] == sum(r.values()) and m["running_need"] == m["running_words"] - r["none"] and m["inscriptions"] == 548
    assert m["running_translated"] <= m["running_need"] and m["spellings_translated"] <= m["spellings_need"] <= m["spellings"]
    b = f["beside_a_stem"]
    assert b["three_signs_or_more_no_stem"] <= b["pieces"] <= b["running_words"] <= r["dictionary"]
    for rnd, rd in f["readings"].items():
        assert sum(v["count"] for v in rd["not_agreed"].values()) == rd["verdicts"].get("not agreed", 0), rnd
        assert all(v["in_one_place"] <= v["count"] for v in rd["not_agreed"].values()), rnd
    t = f["tokens"]
    assert all(t[r]["agents"] == 2 * (D.SAMPLE // D.PACK) and t[r]["tokens"] > 0 for r in D.ROUNDS)
    assert t["all"] == {"agents": sum(t[r]["agents"] for r in D.ROUNDS), "tokens": sum(t[r]["tokens"] for r in D.ROUNDS)}


def test_the_figures_hold_counts_only():
    text = D.PUBLIC.read_text(encoding="utf-8")
    for word in ('"stems"', '"rows"', '"why"', '"of"', '"places"', '"forms"', '"one"', '"two"'):
        assert word not in text, word


def pct(x):
    return f"{100 * x:.1f}%"


def lookup_share(f):
    """What a plain lookup's reach would read as a share: no write-up may give it as the north star before us."""
    return pct(f["lookup"]["translated"] / f["distinct_words"]["point"])


def test_the_page_says_what_the_figures_say():
    f, text = figs(), page()
    s, u, d, m, b = f["sample"], f["unnamed_words"], f["distinct_words"], f["map"], f["beside_a_stem"]
    st, sb, first, lk, e = f["star"], f["star_before"], f["first_count"], f["lookup"], f["corrections"]["endings"]
    # in short: before us is now, and no meaning is the project's
    assert (f"holds about {d['point']:,} distinct words (between {d['low']:,} and {d['high']:,}), and {f['translated']} of them have a "
            f"meaning: {pct(st['point'])} (between {pct(st['low'])} and {pct(st['high'])})") in text
    assert f"Before the project it was the same: each of the {f['translated']} has its meaning in the lexicon of 2003, and the project has added no meaning" in text
    assert f"{f['dictionary_words']} are words of the dictionary" in text
    assert f"took the endings and particles written as a word of their own for words and gave {pct(first['star']['point'])}" in text
    assert "| R5 | \"“Before us” should really equal “Now”\"" in PAGE.read_text(encoding="utf-8") and lookup_share(f) not in text
    # spellings, and the four things a running word is
    assert f"The corpus has {m['spellings']:,} different spellings" in text
    assert f"({m['spellings_translated']} of the {m['spellings_need']:,} that need one, {pct(m['spellings_translated'] / m['spellings_need'])})" in text
    assert f"{f['dictionary_words']} dictionary words are in use, and {f['translated']} of them are translated; {f['running']['piece']} running words are pieces" in text
    assert f"{f['unnamed_stems']:,} unnamed stems, under {f['unnamed_running_words']:,} running words; {f['unnamed_in_one_place']} of them stand in one place" in text
    # the two readings
    one = f["readings"]["r1"]
    agreed, wu, wn = one["sampled"] - one["verdicts"]["not agreed"], one["not_agreed"]["word/unclear"], one["not_agreed"]["word/name"]
    assert f"Their Cohen's kappa is {one['kappa']:.2f}, under the bar of {one['bar']}" in text
    assert f"They agree on {agreed} stems and not on {one['verdicts']['not agreed']}" in text
    assert (f"Of the {one['verdicts']['not agreed']}, {wu['count']} are \"word\" for one checker and \"unclear\" for the other, "
            f"{wu['in_one_place']} of them stems that stand in one place") in text and f"; {wn['count']} are \"word\" against \"name\"" in text
    assert f"Their Cohen's kappa is {s['kappa']:.2f} (bar {s['bar']})" in text
    for case in list(D.CASES) + ["not agreed"]:
        assert f"| {case} | {one['verdicts'].get(case, 0)} | {s['verdicts'].get(case, 0)} |" in text, case
    v, n = s["verdicts"], s["sampled"]
    assert "about two in three of the sampled stems are words of their own, one in eleven is a piece, one in six is unclear" in text
    assert abs(v["word"] / n - 2 / 3) < 0.02 and abs(v["piece"] / n - 1 / 11) < 0.01 and abs(v["unclear"] / n - 1 / 6) < 0.01
    # the north star
    assert f"about {u['point']:,} distinct words among the unnamed stems (between {u['low']:,} and {u['high']:,})" in text
    assert f"With the {f['dictionary_words']} dictionary words that makes about {d['point']:,} distinct words in all (between {d['low']:,} and {d['high']:,})" in text
    for name, star, n in (("Now", st, f["translated"]), ("Before us", sb, f["translated"]),
                          ("With the recurring-words results in the map", f["next"]["star"], f["next"]["translated"])):
        assert f"| {name} | {n} | {pct(star['point'])} | {pct(star['low'])} to {pct(star['high'])} |" in text, name
    assert (f"A plain lookup of the lexicon, word by word, reaches {lk['dictionary_words']} of the {f['dictionary_words']} dictionary words and "
            f"{lk['translated']} of the {f['translated']} translated ones; the other {f['translated'] - lk['translated']} stand in the corpus only in "
            "spellings the lookup does not know") in text
    assert f"{f['next']['stated_later']} more dictionary words count as translated" in text and "older than the project" in text
    assert f"({pct(m['running_translated'] / m['running_need'])}: {m['running_translated']:,} of the {m['running_need']:,} that need a meaning)" in text
    # what the review corrected, and the first count
    assert (f"so {e['entries']} endings, prefixes and particles that stand as a written word of their own counted as dictionary words, "
            f"{e['translated']} of them translated") in text
    assert f["corrections"]["names"] == {"entries": 1, "translated": 0} and "One entry of the kind \"name\" counted as a dictionary word" in text
    assert f"The first count gave {first['translated']} of about {first['distinct_words']['point']:,} distinct words ({pct(first['star']['point'])}, between {pct(first['star']['low'])} and {pct(first['star']['high'])})" in text
    # limits and cost
    assert f"({b['pieces']} different pieces in {b['running_words']} running words; {b['three_signs_or_more_no_stem']} of them have three signs or more" in text
    more = b["three_signs_or_more_no_stem"]
    assert f"Were all {more} words, the share would be {pct(f['translated'] / (d['point'] + more))}" in text
    t = f["tokens"]
    assert f"{t['all']['agents']} fresh agents, {t['all']['tokens']:,} subagent tokens" in text
    assert f"{t['r1']['tokens']:,} for the first reading and {t['r2']['tokens']:,} for the second" in text
    assert f"the words of these {m['inscriptions']} inscriptions" in text


def test_the_summaries_quote_the_figures():
    f = figs()
    read = lambda name: " ".join((ROOT / name).read_text(encoding="utf-8").split())        # noqa: E731
    parts = {"README": between(read("README.md"), "18. **Counted by distinct words", "## The question"),
             "REPORT": read("REPORT.md")[read("REPORT.md").index("## Day nine (2026-11-16): distinct words"):],
             "NEXT_STEPS": between(read("NEXT_STEPS.md"), "19. **Distinct words translated", "Next, in this order")}
    st, d, m, lk, e = f["star"], f["distinct_words"], f["map"], f["lookup"], f["corrections"]["endings"]
    for name, text in parts.items():
        assert f"{pct(st['point'])} (between {pct(st['low'])} and {pct(st['high'])})" in text or f"({pct(st['point'])}, between {pct(st['low'])} and {pct(st['high'])})" in text, name
        assert f"{f['translated']} of about {d['point']:,}" in text and ("the same as before the project" in text or "it was the same" in text), name
        # before us is now: the lookup's reach is never given as a share, as if it were the north star before the project
        assert lookup_share(f) not in text, name
    readme, report, steps = parts["README"], parts["REPORT"], parts["NEXT_STEPS"]
    assert f"the map ties its spellings to {f['dictionary_words']} words of the lexicon, {f['translated']} of them" in readme
    assert (f"a plain lookup of the lexicon finds {lk['translated']} of them, and the map recognises the other {f['translated'] - lk['translated']} "
            "in spellings the lookup does not know") in readme
    assert f"The first count took the endings and particles written as words for words and gave {pct(f['first_count']['star']['point'])}" in readme
    assert f"a word of the lexicon ({f['dictionary_words']} in use, {f['translated']} of them" in report
    assert f"({f['unnamed_stems']:,}, of which {f['unnamed_in_one_place']} stand in one place)" in report
    assert f"About {d['point']:,} distinct words (between {d['low']:,} and {d['high']:,})" in report
    assert f"Before the project it was the same: each of the {f['translated']} has its meaning in the lexicon of 2003" in report
    assert f"({lk['translated']} of the {f['translated']})" in report
    assert f"it would be {f['next']['translated']} ({pct(f['next']['star']['point'])})" in report
    assert f"the spellings ({pct(m['spellings_translated'] / m['spellings_need'])} of those" in report and f"the running words ({pct(m['running_translated'] / m['running_need'])})" in report
    assert f"{f['first_count']['translated']} of about {f['first_count']['distinct_words']['point']:,}, {pct(f['first_count']['star']['point'])}" in report
    assert f"({e['entries']} entries, {e['translated']} of them translated)" in report
    assert f"kappa {f['sample']['kappa']:.2f}" in report and f"kappa {f['readings']['r1']['kappa']:.2f}" in report
    assert f"{f['tokens']['all']['agents']} fresh agents, {f['tokens']['all']['tokens']:,} subagent tokens" in report
    assert f"the same as before the project (each of those meanings is in the lexicon of 2003), against {pct(m['running_translated'] / m['running_need'])} of the running words" in steps
    assert f"{f['dictionary_words']} are words of the lexicon" in steps and f"sample of the {f['unnamed_stems']:,} stems" in steps
    assert f"kappa {f['sample']['kappa']:.2f}" in steps and f"(G1: {f['next']['stated_later']} words," in steps


def test_the_reporting_skill_names_the_figures_as_they_are():
    """The reporting skill reads the north star from the figures file by these keys, says that before us is now, and
    gives the lookup's reach as it is; its log's first row, the status of the day of this count, gives the north star
    as these figures do (later rows are of the map with its layers: tests/test_themap.py)."""
    f = figs()
    skill = " ".join((ROOT / ".claude/skills/reporting/SKILL.md").read_text(encoding="utf-8").split())
    for key in ("`translated`", "`distinct_words.point`", "`star.point`", "`star.low`", "`star.high`", "`next.star.point`", "`lookup.translated`"):
        assert key in skill, key
    assert f["star_before"] == f["star"] and "**Before us: the same as Now.**" in skill
    assert f"({f['lookup']['translated']} of {f['translated']} on 2026-11-16)" in skill
    row = [l for l in (ROOT / ".claude/skills/reporting/STATUS_LOG.md").read_text(encoding="utf-8").splitlines() if l.startswith("| 2026-")][0]
    st, d = f["star"], f["distinct_words"]
    assert f"| {pct(st['point'])} ({f['translated']} of about {d['point']:,}; range {pct(st['low'])} to {pct(st['high'])}) |" in row
    assert f"Before us: {pct(f['star_before']['point'])}," in row and f"(G1): {pct(f['next']['star']['point'])}," in row


def test_the_readme_lists_the_script_among_the_local_commands():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    start = "- `python3 -I src/words.py public` (and "
    listed = between(" ".join(text.split()), start, ") reads")[len(start):]
    assert sorted([c.strip("` ") for c in listed.split(",")] + ["public"]) == sorted(D.COMMANDS)
    assert "python3 -I tests/test_words.py" in text
    for c in D.COMMANDS:
        assert f"python3 -I src/words.py {c} " in D.__doc__, c


def test_the_figures_are_the_count_of_the_local_files():
    """population.json is what the map and the lookup give now, the sample is the seed's draw from its stems (the
    same with the review's corrections), each reading's result is what its answers give, and the figures are all
    that counted."""
    needs(f"{LOCAL}/population.json", f"{LOCAL}/sample.json", f"{LOCAL}/answers1", f"{LOCAL}/answers2", f"{LOCAL}/r2/answers1",
          f"{LOCAL}/r2/answers2", "data/sources/v6", "data/sources/lexicon", "data/corpus_v6.jsonl", "data/rilly2003")
    import recurring as W
    pop, groups = D.read("population.json"), D.read("sample.json")
    assert D.population_figures() == pop
    gl, lex = W.the_map(), W.lexicon()
    assert D.population_of(gl, lex, fix=True)[1] == D.population_of(gl, lex)[1]
    assert [s for grp in groups for s in grp] == D.sample_of(pop["stems"])
    for rnd, r in D.ROUNDS.items():
        sub = r["folder"]
        out = D.results(pop, groups, D.sample_answers(D.OUT / f"{sub}answers1", groups), D.sample_answers(D.OUT / f"{sub}answers2", groups))
        assert out == D.read(f"{sub}result.json"), rnd
    assert D.figures() == figs()


def test_every_pack_is_what_the_script_writes():
    """Both readings' packs, and the sample, written again in a folder of their own from population.json: byte for
    byte what the checkers read."""
    needs(f"{LOCAL}/population.json", f"{LOCAL}/sample.json", f"{LOCAL}/packs", f"{LOCAL}/r2/packs", "data/sources/v6",
          "data/sources/lexicon", "data/corpus_v6.jsonl", "data/rilly2003")
    real = D.OUT
    with tempfile.TemporaryDirectory() as d:
        D.OUT = Path(d)
        try:
            (D.OUT / "population.json").write_bytes((real / "population.json").read_bytes())
            with contextlib.redirect_stdout(io.StringIO()):
                for rnd in D.ROUNDS:
                    D.packs(rnd)
        finally:
            D.OUT = real
        for rnd, r in D.ROUNDS.items():
            folder = f"{r['folder']}packs"
            names = sorted(p.name for p in (real / folder).iterdir())
            assert names == sorted(p.name for p in (Path(d) / folder).iterdir()) and len(names) == 2 * D.SAMPLE // D.PACK, rnd
            for name in names:
                assert (Path(d) / folder / name).read_bytes() == (real / folder / name).read_bytes(), (rnd, name)
        assert (Path(d) / "sample.json").read_bytes() == (real / "sample.json").read_bytes()


def test_both_readings_saw_the_same_items():
    """The packs of the second reading differ from the first's only in the brief."""
    needs(f"{LOCAL}/packs", f"{LOCAL}/r2/packs")
    for k in range(1, D.SAMPLE // D.PACK + 1):
        for c in (1, 2):
            a = (D.OUT / "packs" / f"S{k:02d}_c{c}.md").read_text(encoding="utf-8").split("\n---\n", 1)[1]
            b = (D.OUT / "r2" / "packs" / f"S{k:02d}_c{c}.md").read_text(encoding="utf-8").split("\n---\n", 1)[1]
            assert a == b, (k, c)


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
