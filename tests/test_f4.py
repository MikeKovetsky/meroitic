"""Checks for the pilot of F4, whole texts translated and scored (src/f4.py).

  python3 -I tests/test_f4.py

Millet 2005, Rilly's lexicon, the map's gloss file and the agents' answers are local only: the checks of the
method run on made-up texts, units and answers; the checks of the reported numbers read the public figures file
and compare it with a count from the local files where those are present.
"""
import collections
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import f4 as F                       # noqa: E402
from local_only import needs, run    # noqa: E402

LOCAL = ("data/sources/jssea-text/pages.txt", "data/sources/v6/analysts/glosses.jsonl", "data/corpus_v6.jsonl")
ANSWERED = ("data/sources/f4/key.json", "data/sources/f4/answers")


def cand(i, kind, words, covered):
    return {"id": i, "kind": kind, "words": words, "covered": covered}


def g(form, level, gloss="", **more):
    return {"form": form, "level": level, "gloss": gloss, **more}


def lines(path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in items), encoding="utf-8")


def test_the_object_an_entry_is_on():
    assert F.object_kind("GA41: Sandstone offering table with single spout") == "offering table"
    assert F.object_kind("GA07: Relatively well-made sandstone offering-table") == "offering table"
    assert F.object_kind("GA47: A small wooden label with cotton string attached") == "label"
    assert F.object_kind("GA28: Inscription consisting of two slabs of sandstone") == "stela"
    assert F.object_kind("GA04: Sandstone stela, register no. 63:3:30") == "stela"
    assert F.object_kind("GA99: A bowl") == "other"
    assert F.object_kind("GA98: " + "x " * 100 + "stela") == "other"          # only the first lines count


def test_a_numbered_line_after_a_side_or_a_part():
    block = "GA47: label\nTEXT\nrecto 1: txbo : se\n2: adke\nverso 1: kele\nA 1: wos\nCOMMENTARY\n3: nothing"
    assert F.text_letters(block) == "thboseadkekelewos"          # x read as h, as prepare.reduced_expert


def test_the_choice_of_texts():
    cands = [cand("L1", "label", 8, 0.5), cand("O1", "offering table", 8, 1.0), cand("O2", "offering table", 10, 1.0),
             cand("O3", "offering table", 30, 0.6), cand("S1", "stela", 10, 1.0), cand("S2", "stela", 11, 0.9),
             cand("S3", "stela", 20, 0.86), cand("S4", "stela", 25, 0.84), cand("S5", "stela", 90, 0.5),
             cand("S6", "stela", 60, 0.95)]
    # one of each other kind, the best covered and then the longest; stelae covered enough: S1 S2 S3 S6
    assert F.choose(cands) == ["L1", "O2", "S6", "S2", "S1"]
    assert F.choose(cands, covered=0.5) == ["L1", "O2", "S5", "S3", "S1"]
    assert F.choose([cand("S1", "stela", 10, 1.0)]) == ["S1"]                   # one stela: chosen once
    assert F.choose([cand("S1", "stela", 10, 0.1)]) == []


def test_the_pages_sample():
    rows, gl = {}, {}
    for n in range(40):
        kind = list(F.PAGES)[n % len(F.PAGES)]
        rows[f"T{n:02d}"] = {"open": n % 7 != 0, "kind": kind}
        gl[f"T{n:02d}"] = [g("w", "lost" if k < (n % 5) else "meaning") for k in range(5 + n % 9)]
    a, b = F.pages_sample(rows, gl), F.pages_sample(rows, gl)
    assert a == b and len(a) == sum(F.PAGES.values()) and len(set(a)) == len(a)
    for i in a:
        assert rows[i]["open"] and F.MIN_WORDS <= len(gl[i]) <= F.MAX_WORDS
        assert sum(x["level"] == "lost" for x in gl[i]) <= F.LOST_SHARE * len(gl[i])
    assert collections.Counter(rows[i]["kind"] for i in a) == collections.Counter(F.PAGES)
    assert F.pages_sample(rows, gl, seed="another") != a


def test_the_baseline_is_the_map_word_by_word():
    gs = [g("woSi", "name", "Isis +i"), g("ameqe", "name", "NAME"), g("ato", "meaning", "water"),
          g("aribet", "kind", "[title]"), g("Sm", "hypothesis", "wife (?)"), g("pqr", "hypothesis", "prince"),
          g("brtoye", "unknown", "?"), g("lx.", "lost", "<lx.>"), g("qo", "grammar", "this one")]
    assert F.baseline(gs) == ("Isis +i · Ameqe (a name) · water · [aribet: title] · wife (?) · prince (?) · "
                              "[brtoye: ?] · [lx.: signs lost] · this one")


def test_millet_is_taken_out_of_the_statuses():
    def e(props, editors=None):
        return {"headword": "h", "kind": "noun", "level": "meaning", "status": "established", "page": 1,
                "meaning": "m", "uses": 3, "uses_translated": 3, "editors": editors or {},
                "proposals": [{"id": i, "author": a, "proposal": p} for i, a, p in props]}
    verdicts = {"P1": ("same", "same"), "P2": ("other", "other"), "P3": ("same", "same")}
    only_millet = e([("P1", "Millet 1982", "'king'")])
    assert F.blind_statuses([only_millet], verdicts, {}) == {"h": "stated by one"}
    speaks_of_him = e([("P3", "Hofmann", "corroborates Millet's hypothesis")])
    assert F.blind_statuses([speaks_of_him], verdicts, {}) == {"h": "stated by one"}
    both = e([("P1", "Millet", "'king'"), ("P3", "Griffith", "'king'")])
    assert F.blind_statuses([both], verdicts, {}) == {"h": "agreed by two scholars"}
    # the editors' verdicts are the ones passed in: without Millet's, an entry he alone agreed with is not agreed
    edited = e([], editors={"agree": 2})
    assert F.blind_statuses([edited], verdicts, {}) == {"h": "stated by one"}
    assert F.blind_statuses([edited], verdicts, {"h": {"agree": 1}}) == {"h": "agreed by two scholars"}
    assert F.blind_statuses([dict(edited, uses_translated=0)], verdicts, {}) == {}
    assert F.scrub("according to Millet") == F.WITHHELD and F.scrub("water") == "water" and F.scrub(None) == ""


def test_the_translators_pack_hides_millet():
    lex = {"ato": {"headword": "ato", "kind": "noun", "page": 30, "status": "established", "meaning": "water",
                   "proposals": [{"author": "Millet", "proposal": "water"}, {"author": "Griffith", "proposal": "water"}]},
           "bqo": {"headword": "bqo", "kind": "verb", "page": 50, "status": "hypothesis",
                   "meaning": "to control, according to Millet", "proposals": []}}
    rows = {"T1": {"site": "Adda", "kind": "funerary"}}
    gl = {"T1": [g("ato", "meaning", "water", parts=[{"entry": "ato"}]),
                 g("mrbqo", "hypothesis", "control (Millet)", parts=[{"entry": "bqo"}], by="analyst",
                   evidence="as Millet reads it")]}
    gl["T1"].append(g("bqol", "hypothesis", "would mean to control +l", parts=[{"entry": "bqo"}, {"entry": "ending"}]))
    text, withheld = F.translator_pack(["T1"], rows, gl, lex, {"ato": "agreed by two scholars"}, {}, "out.jsonl")
    assert "Millet" not in text and "control" not in text and "Griffith: water" in text
    assert withheld == 4                    # two glosses, a note and a meaning of the lexicon
    assert "ato (agreed by two scholars)" in text and "bqo (not rated by F2; Rilly: hypothesis)" in text
    assert F.millet_heads(lex) == {"bqo"}
    # the baseline withholds what the translator's pack withholds
    assert F.baseline(gl["T1"], F.millet_heads(lex)) == "water · [mrbqo: ?] · [bqol: ?]"
    assert F.baseline(gl["T1"]) == "water · [mrbqo: ?] · would mean to control +l (?)"


def test_the_sections_of_an_entry():
    block = ("GA41: Sandstone offering table\nTEXT\n1: wos wet\nJSSEA 32 (2005) 33\n2: sori\nCOMMENTARY\nA lady.\n"
             "22 Studies Millet\nRENDERING\n“O Isis!\nO Osiris!”\n")
    t, r = F.sections(block)
    assert t == "1: wos wet\n2: sori" and r == "“O Isis!\nO Osiris!”"
    two = "TEXT\n1: a\nNOTES\nx\nTEXT\n1: b\nRENDERING\none\nRENDERING\ntwo"
    assert F.sections(two) == ("1: a\n\n1: b", "one\n\ntwo")


def test_a_unit_in_our_copy():
    ours = "wosisoreyiqoameqemeteyetedhelowi"
    assert F.in_copy("ameqemeteye", ours) and F.in_copy("tedxelowi", ours)          # x read as h, as reduced_expert
    assert F.in_copy("ameqemetaye", ours)                                               # half its runs of four
    assert not F.in_copy("kadilakhoye", ours)
    assert F.in_copy("", ours) and F.in_copy(None, ours) and F.in_copy("qo", ours)
    assert F.in_copy("ẖelowi", ours) and F.in_copy("tedḫelowi", ours)                   # ẖ and ḫ read as h


def test_the_decoys_share_the_fewest_words():
    rend = {"A": "O Isis! May she drink much water.", "B": "The king built the temple of Amun."}
    dec = {"X": "Isis gives water.", "Y": "The king's temple.", "Z": "A list of jars and baskets."}
    # (X, Y) shares 4 words, (X, Z) 2, (Y, X) none: the first assignment with the fewest
    assert F.assign_decoys(rend, dec) == ({"A": "Y", "B": "X"}, {"A": 0, "B": 0})
    assert F.assign_decoys(rend, {"X": dec["X"], "Y": dec["Y"]}) == ({"A": "Y", "B": "X"}, {"A": 0, "B": 0})
    assert F.assign_decoys({"A": rend["A"]}, {"X": dec["X"]}) == ({"A": "X"}, {"A": 2})
    assert F.clean("born of Ameqemeteye", "The king built a temple") and not F.clean("the king", "a king's son")


def test_each_judge_has_an_order_of_their_own():
    a = {(j, t): F.order_of(j, t) for j in (1, 2) for t in ("GA 28", "GA 41", "GA 53", "GA 37", "GA 47")}
    assert a == {(j, t): F.order_of(j, t) for j in (1, 2) for t in ("GA 28", "GA 41", "GA 53", "GA 37", "GA 47")}
    assert all(sorted(o.values()) == sorted(F.READINGS) and list(o) == list(F.LETTERS) for o in a.values())
    assert len({tuple(o.values()) for o in a.values()}) > 1
    assert any(a[1, t] != a[2, t] for t in ("GA 28", "GA 41", "GA 53", "GA 37", "GA 47"))


def test_a_translation_must_give_every_word():
    gs = [g("woSi", "name"), g("ato", "meaning")]
    ok = {"words": [{"n": 1, "form": "woSi", "status": "name"}, {"n": 2, "form": "ato", "status": "agreed"}],
          "translation": "O Isis, water"}
    assert F.check_translation(ok, gs) == []
    assert F.check_translation({**ok, "words": ok["words"][:1]}, gs)
    assert F.check_translation({**ok, "words": ok["words"][::-1]}, gs)
    assert F.check_translation({**ok, "translation": " "}, gs) == ["no running translation"]
    bad = {**ok, "words": [ok["words"][0], {**ok["words"][1], "status": "sure"}]}
    assert F.check_translation(bad, gs) == ["unknown statuses: sure"]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "t.jsonl"
        lines(p, [{"text": "T1", **ok}, {"text": "T1", "words": []}, {"text": "T9", **ok}])
        got, faults = F.translations(p, ["T1", "T2"], {"T1": gs, "T2": gs})
        assert got["T1"]["translation"] == "O Isis, water" and faults == {"T2": ["not answered"]}
    assert F.text_id("GA41", ["GA 41", "GA 4"]) == "GA 41" and F.text_id("GA 4", ["GA 41", "GA 4"]) == "GA 4"
    assert F.text_id("T9", ["T1"]) is None and F.text_id(None, ["T1"]) is None


def test_the_score_and_the_tallies():
    assert F.score({"given": 2, "partly": 2, "wrong": 1, "missing": 5}) == 0.3
    assert F.score({"unanswered": 3}) is None and F.score({}) is None
    assert F.score({"given": 1, "unanswered": 1}) == 1.0           # unanswered lines are counted apart
    v = {("T", "U01", "baseline"): "given", ("T", "U02", "baseline"): "partly"}
    assert F.tallies(v, [("T", "U01"), ("T", "U02"), ("T", "U03")], "baseline") == collections.Counter(
        {"given": 1, "partly": 1, "unanswered": 1})
    one = {("T", "U01", "translator"): "given", ("T", "U01", "baseline"): "missing", ("T", "U02", "translator"): "wrong"}
    two = {("T", "U01", "translator"): "given", ("T", "U01", "baseline"): "partly", ("T", "U02", "translator"): "wrong"}
    a = F.judges_agreement(one, two, [("T", "U01"), ("T", "U02")])
    assert a["pairs"] == 3 and a["same"] == 2


def make_run(d):
    """A made-up run of the pilot: two texts, the splitter's units, both judges' answers, and a key."""
    out = Path(d)
    gl = {"T1": [g("woSi", "name"), g("ato", "meaning")], "T2": [g("qore", "meaning")],
          "P1": [g("x", "unknown")], "P2": [g("y", "unknown")]}
    lines(out / "answers" / "translator_pilot.jsonl", [
        {"text": t, "words": [{"n": n, "form": w["form"], "status": "agreed"} for n, w in enumerate(gl[t], 1)],
         "translation": "tr " + t} for t in ("T1", "T2")])
    lines(out / "answers" / "translator_pages.jsonl", [
        {"text": t, "words": [{"n": 1, "form": gl[t][0]["form"], "status": "open"}], "translation": "decoy " + t}
        for t in ("P1", "P2")])
    lines(out / "answers" / "splitter.jsonl", [
        {"text": "T1", "unit": "U01", "english": "O Isis", "meroitic": "wosi", "kind": "god"},
        {"text": "T1", "unit": "U02", "english": "much water", "meroitic": "ato", "kind": "formula"},
        {"text": "T1", "unit": "U03", "english": "wetneyinqe", "meroitic": "wetneyineqeli", "kind": "other", "open": True},
        {"text": "T2", "unit": "U01", "english": "the king", "meroitic": "qore", "kind": "title"},
        {"text": "T2", "unit": "U02", "english": "of Faras", "meroitic": "pedeme", "kind": "place"}])
    key = {"pilot": ["T1", "T2"], "pages": ["P1", "P2"], "decoys": {"T1": "P1", "T2": "P2"},
           "decoy_shared_words": {"T1": 0, "T2": 0}, "blind": {},
           "order": {"1": {"T1": {"A": "translator", "B": "baseline", "C": "decoy"},
                           "T2": {"A": "decoy", "B": "translator", "C": "baseline"}},
                     "2": {"T1": {"A": "baseline", "B": "decoy", "C": "translator"},
                           "T2": {"A": "translator", "B": "baseline", "C": "decoy"}}},
           "units": {"T1": {"U01": {"kind": "god", "open": False, "doubt": False, "in_copy": True, "clean": True},
                            "U02": {"kind": "formula", "open": False, "doubt": False, "in_copy": True, "clean": False},
                            "U03": {"kind": "other", "open": True, "doubt": False, "in_copy": True, "clean": True}},
                     "T2": {"U01": {"kind": "title", "open": False, "doubt": False, "in_copy": True, "clean": True},
                            "U02": {"kind": "place", "open": False, "doubt": False, "in_copy": False, "clean": True}}}}
    (out / "key.json").write_text(json.dumps(key), encoding="utf-8")
    # what each judge said of each reading, by reading name; written under the letters of its own order
    said = {1: {("T1", "U01"): ("given", "given", "missing"), ("T1", "U02"): ("given", "partly", "given"),
                ("T2", "U01"): ("partly", "wrong", "missing"), ("T2", "U02"): ("missing", "missing", "missing")},
            2: {("T1", "U01"): ("given", "given", "given"), ("T1", "U02"): ("given", "missing", "missing"),
                ("T2", "U01"): ("partly", "wrong", "missing"), ("T2", "U02"): ("given", "missing", "missing")}}
    for j in (1, 2):
        out_lines = []
        for (t, u), vs in said[j].items():
            by_name = dict(zip(F.READINGS, vs))
            for letter, name in key["order"][str(j)][t].items():
                out_lines.append({"text": t, "unit": u, "reading": letter, "verdict": by_name[name]})
        out_lines.append({"text": "T1", "unit": "U01", "reading": "A", "verdict": "wrong"})     # a second line: ignored
        out_lines.append({"text": "T1", "unit": "U03", "reading": "A", "verdict": "given"})    # an open unit: not judged
        lines(out / "answers" / f"judge{j}.jsonl", out_lines)
    return out, gl


def test_the_count_of_a_made_up_run():
    with tempfile.TemporaryDirectory() as d:
        out, gl = make_run(d)
        figs = F.count(out, rows={"T1": {}}, gl=gl)
        assert figs["units"]["all"] == 5 and figs["units"]["open"] == 1 and figs["units"]["judged"] == 4
        assert figs["units"]["scored"] == 3 and figs["units"]["not_in_copy"] == 1
        s1, s2 = figs["scores"]["1"], figs["scores"]["2"]
        assert (s1["translator"]["given"], s1["translator"]["partly"]) == (2, 1) and s1["translator"]["score"] == 0.8333
        assert s1["baseline"]["score"] == 0.5 and s1["baseline"]["wrong"] == 1
        assert s2["translator"]["score"] == 0.8333 and s2["baseline"]["score"] == 0.3333
        assert figs["score"]["translator"] == 0.8333 and figs["score"]["baseline"] == 0.4166
        assert figs["lead"] == 0.4167
        assert figs["with_units_not_in_copy"]["translator"] == 0.75        # judge 2 gave U02 of T2; judge 1 did not
        assert figs["per_text"] == {"T1": {"translator": 1.0, "baseline": 0.625}, "T2": {"translator": 0.5, "baseline": 0.0}}
        assert figs["per_text_mean"] == {"translator": 0.75, "baseline": 0.3125}
        assert figs["unit_by_unit"] == {"1": {"same": 1, "better": 2}, "2": {"same": 1, "better": 2}}
        # the decoys: only clean units count (T1 U01 and T2 U01; T1 U02 shares a word with its decoy)
        assert figs["decoys_measure"]["1"] == {"clean_units": 2, "accepted": 0, "verdicts": {"missing": 2}}
        assert figs["decoys_measure"]["2"] == {"clean_units": 2, "accepted": 1, "verdicts": {"given": 1, "missing": 1}}
        assert figs["bars"]["decoys_accepted"] is False
        assert figs["agreement"]["pairs"] == 6 and figs["agreement"]["same"] == 5
        assert figs["translator"]["words"] == 5 and figs["translator"]["statuses"] == {"agreed": 3, "open": 2}


def test_the_packs_are_not_written_again():
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        lines(out / "answers" / "splitter.jsonl", [{}])
        try:
            F.packs(out)
        except SystemExit as e:
            assert "not writing" in str(e)
        else:
            raise AssertionError("packs() wrote over an answered run")
        lines(out / "answers" / "judge2.jsonl", [{}])
        try:
            F.judges(out)
        except SystemExit as e:
            assert "not writing" in str(e)
        else:
            raise AssertionError("judges() wrote over an answered run")


def test_the_chosen_texts():
    needs(*LOCAL)
    ids, pages, cands = F.texts()
    assert len(cands) == 18 and ids == ["GA 47", "GA 41", "GA 28", "GA 53", "GA 37"]
    assert pages == ["REM 0240", "Meroe 27", "REM 0209", "REM 0405", "REM 0091c"]
    assert F.rendered().__len__() == 20


def test_the_public_figures():
    if not F.PUBLIC.exists():
        return
    figs = json.loads(F.PUBLIC.read_text(encoding="utf-8"))
    assert figs["bars_set"] == F.BARS and figs["expected"] == {k: list(v) if isinstance(v, tuple) else v
                                                               for k, v in F.EXPECTED.items()}
    assert figs["units"]["scored"] == sum(figs["units"]["per_text"].values())
    for j in ("1", "2"):
        for name in F.READINGS:
            s = figs["scores"][j][name]
            assert sum(s[v] for v in F.VERDICTS) + s["unanswered"] == figs["units"]["scored"]
    needs(*LOCAL, *ANSWERED)
    rows, gl = F.rows_of(), F.glosses_of()
    again = F.count(rows=rows, gl=gl)
    again["tokens"], again["sizing"] = F.TOKENS, F.sizing(again, F.TOKENS, rows, gl)
    assert json.loads(json.dumps(again, ensure_ascii=False)) == figs



def between(text, start, end):
    """The text from start (which stands once) to end, its spaces as one."""
    assert text.count(start) == 1, start
    rest = text[text.index(start):]
    return " ".join((rest[:rest.index(end)] if end in rest else rest).split())


def test_the_summaries_quote_the_figures():
    if not F.PUBLIC.exists():
        return
    f = json.loads(F.PUBLIC.read_text(encoding="utf-8"))
    read = lambda name: (ROOT / name).read_text(encoding="utf-8")   # noqa: E731
    parts = {"page": between(read("data/discovery/f4_pilot.md"), "## 1. Answer first", "## 2. The texts"),
             "README": between(read("README.md"), "15. **Five inscriptions", "## The question"),
             "REPORT": between(read("REPORT.md"), "## Day five, late night (2026-11-12): whole texts", "7. **Cost:**"),
             "NEXT_STEPS": between(read("NEXT_STEPS.md"), "16. **F4, the pilot", "Next, in this order"),
             "summary page": between(read("docs/report.html"), "<tr><td>Translate five inscriptions whole", "</tr>")}
    pct = lambda x: f"{100 * x:.1f}%"                                 # noqa: E731
    must = [pct(f["score"]["translator"]), pct(f["score"]["baseline"]), pct(f["wrong"]["translator"]),
            pct(f["wrong"]["baseline"]), f"{f['agreement']['kappa']:.2f}", str(f["units"]["scored"])]
    for name, text in parts.items():
        missing = [m for m in must if m not in text]
        assert not missing, (name, missing)
    for name in ("page", "REPORT"):
        assert pct(f["per_text_mean"]["translator"]) in parts[name] and pct(f["per_text_mean"]["baseline"]) in parts[name]
    assert f"trails by {-100 * f['lead']:.1f}" in parts["page"]
    total = f"{f['sizing']['pilot_total']:,} subagent tokens"
    assert total in parts["page"] and total in " ".join(read("REPORT.md").split())
    assert f["sizing"]["pilot_total"] == sum(F.TOKENS.values())
    assert round(f["sizing"]["scored_run"]["total"] / 1e6, 1) == 2.1 and round(f["sizing"]["pages_run"]["translator"] / 1e6, 1) == 5.3


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
