"""Checks for F2, the lexicon with a source and a status for every meaning (src/lexicon.py).

  python3 -I tests/test_lexicon.py

Rilly's lexicon, the map's gloss file, the judges' tables and answers are local only: the checks of the method run
on made-up entries and rows; the checks of the reported numbers read the public figures file and table and compare
them with the local files where those are present.
"""
import collections, csv, json, re, sys, tempfile, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import lexicon as X    # noqa: E402
from local_only import needs, run   # noqa: E402

FIGURES = ROOT / "data/discovery/lexicon_figures.json"
LOCAL = ("data/rilly2003", "data/sources/v6/analysts/glosses.jsonl", "data/sources/expert/rows.jsonl",
         "data/sources/expert/answers", "data/sources/lexicon/entries.jsonl", "data/sources/lexicon/key.json",
         "data/sources/lexicon/answers", "data/sources/lexicon/round2/key.json",
         "data/sources/lexicon/round2/answers", "data/sources/lexicon/round3/key.json",
         "data/sources/lexicon/round3/answers")
AGREED = "agreed by two scholars"


def entry(h, meaning="king", status="established", level="meaning", props=(), editors=None, uses=3, kind=""):
    return {"headword": h, "kind": kind, "level": level, "status": status, "page": 1, "meaning": meaning,
            "vague": False, "uses": uses, "uses_translated": uses,
            "proposals": [{"id": i, "author": "Someone", "proposal": p} for i, p in props], "editors": editors or {}}


def lines(path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in items), encoding="utf-8")


def test_a_view_without_a_name():
    assert X.unnamed("unnamed") and X.unnamed("earlier view") and X.unnamed(" ") and not X.unnamed("Griffith 1911a")


def test_rilly_is_not_another_scholar():
    e = {"proposals": [{"author": "Rilly 1999", "proposal": "x"}, {"author": " rilly", "proposal": "y"},
                       {"author": "Griffith", "proposal": "'king'"}, {"author": "Hintze", "proposal": " "},
                       {"author": "", "proposal": "z"}, {"author": "Hofmann", "proposal": "'ruler'"}]}
    assert [p["author"] for p in X.others(e)] == ["Griffith", "Hofmann"]
    assert X.others({}) == [] and X.others({"proposals": None}) == []


def test_the_stem_a_word_is_built_on():
    assert X.stem_of(["qore"]) == "qore" and X.stem_of(["qore", "-se (1)"]) == "qore"
    assert X.stem_of(["ending", "mlo"]) == "mlo"                       # a pseudo-entry is no entry
    assert X.stem_of(["ps-", "ḫr", "-kete"]) == "ḫr"
    assert X.stem_of(["-se (1)"]) == "-se (1)"                         # an ending alone is its own stem
    assert X.stem_of(["at (2)", "mẖe"]) is None                       # two stems: no one entry
    assert X.stem_of([]) is None and X.stem_of(None) is None and X.stem_of(["NAME"]) is None


def test_only_entries_rilly_states_go_to_the_judges():
    es = [entry("qore", props=[("P0001", "'ruler'")]), entry("ps-", status="hypothesis", level="kind",
                                                              props=[("P0002", "'son'")]),
          entry("ant", props=[("P0003", "'priest'")], uses=0), entry("-l", level="grammar",
                                                                    props=[("P0004", "'the'")]),
          entry("Wos", level="name", props=[("P0005", "'Isis'")])]
    assert [r["id"] for r in X.rows_for_judges(es)] == ["P0001", "P0004"]     # names were not sent


def test_the_statuses_as_set_before_the_judges():
    v = {"P1": ("same", "same"), "P2": ("same", "partly"), "P3": ("other", "other"), "P4": ("partly", "partly")}
    assert X.status(entry("a", props=[("P1", "")]), v) == AGREED
    assert X.status(entry("a", props=[("P2", "")]), v) == "stated by one"            # the judges split
    assert X.status(entry("a", props=[("P4", "")]), v) == "stated by one"            # "partly" is not enough
    assert X.status(entry("a", props=[("P3", "")]), v) == "disputed"
    assert X.status(entry("a", props=[("P1", ""), ("P3", "")]), v) == AGREED
    assert X.status(entry("a", editors={"agree": 1}), v) == AGREED
    assert X.status(entry("a", editors={"differ": 2, "partly": 1}), v) == "disputed"
    assert X.status(entry("a", editors={"partly": 2, "new": 3}), v) == "stated by one"
    assert X.status(entry("a"), v) == "stated by one"
    assert X.status(entry("a", status="hypothesis", props=[("P1", "")]), v) == "proposed"
    assert X.status(entry("a", level="kind", props=[("P1", "")]), v) == "proposed"
    assert X.status(entry("a", props=[("P9", "")]), v) == "stated by one"            # a decoyed row counts not
    # a name Rilly states is rated like a meaning (item 3); the first count called it "proposed"
    isis = entry("Wos", level="name", kind="god name", editors={"agree": 25})
    assert X.status(isis, v) == AGREED and X.status(entry("Mnp", level="name"), v) == "stated by one"
    assert X.status(isis, v, rated=("meaning", "grammar")) == "proposed"
    assert X.status(entry("Mnp", status="hypothesis", level="hypothesis"), v) == "proposed"


def expert_folder(d, rows, verdicts):
    """A made-up check against the editions: rows.jsonl and the first judge's answers, pack A."""
    lines(d / "rows.jsonl", [{"row": r, "pack": "A", "decoy": decoy, "form": form, "entry_of": of,
                              "level": "meaning", "ours": "x"} for r, form, of, decoy in rows])
    lines(d / "answers" / "judge1_A.jsonl", [{"row": r, "verdict": v, "expert": e} for r, v, e in verdicts])
    return d


def test_a_word_the_map_misread_is_not_an_editors_reading():
    with tempfile.TemporaryDirectory() as d:
        folder = expert_folder(Path(d), [("M1", "l", ["l (2)"], False), ("M2", "atoye", ["ato", "ending"], False),
                                         ("M3", "ato", ["ato"], False), ("M4", "woSi", ["Wos", "ending"], False),
                                         ("M5", "mlo", ["mlo"], False), ("M6", "qo", ["qo"], True),
                                         ("M7", "mXe", ["mẖe"], False)],
                               [("M1", "differ", "the numeral 1"), ("M2", "differ", "Atoye (personal name)"),
                                ("M3", "differ", "bread"), ("M4", "agree", "Isis, a goddess's name"),
                                ("M5", "new", "part of the good"), ("M6", "agree", "this one"),
                                ("M7", "partly", "part of the name Makhalikade")])
        seen = {h: dict(c) for h, c in X.editors(folder).items()}
        assert seen == {"ato": {"differ": 1}, "Wos": {"agree": 1}, "mlo": {"new": 1}}, seen
        first = {h: dict(c) for h, c in X.editors(folder, leave_out=lambda r, a: False).items()}
        assert first == {"l (2)": {"differ": 1}, "ato": {"differ": 2}, "Wos": {"agree": 1}, "mlo": {"new": 1},
                         "mẖe": {"partly": 1}}, first                           # a decoy never counts
    # an agreement on a piece of another word counts under the rule; count() gives the figure without it
    assert X.on_a_piece({"ours": "end of terikelowi written apart"}, {"verdict": "agree", "expert": "was her father"})
    assert X.on_a_piece({"ours": "x"}, {"verdict": "agree", "expert": "part of peseto, King's Son"})
    assert not X.on_a_piece({"ours": "x"}, {"verdict": "differ", "expert": "part of peseto"})
    assert not X.on_a_piece({"ours": "ruler, sovereign"}, {"verdict": "agree", "expert": "king"})


def test_an_unnamed_ending_rests_on_an_agreed_one_spelled_like_it():
    es = [{"headword": h, "kind": k} for h, k in (("-lowi", "function word"), ("qowi", "function word"),
                                                   ("wi (1)", "noun"), ("-li (1)", "function word"),
                                                   ("-se (1)", "function word"), ("-se (2)", "function word"))]
    st = {"-lowi": AGREED, "qowi": AGREED, "wi (1)": AGREED, "-li (1)": "stated by one", "-se (1)": AGREED,
          "-se (2)": "stated by one"}
    assert X.ends_like(st, es) == {"lowi", "qowi", "se"}                    # not the noun wi, not -li


def test_count_end_to_end():
    """The statuses, the two figures and the sensitivities on made-up files (item 3 and 4 of the docstring)."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        es = [entry("mlo", props=[("P1", "'good'")]), entry("-li (1)", level="grammar", kind="function word"),
              entry("-lowi", level="grammar", kind="function word", props=[("P3", "'copula'")]),
              entry("Wos", level="name", kind="god name", editors={"agree": 1}),
              entry("qo", level="grammar", props=[("P2", "'noble'")], editors={"differ": 1}),
              entry("l (2)", props=[("P4", "'to give'")], editors={"differ": 1}),
              entry("-wi (5)", status="hypothesis", level="hypothesis", kind="function word"),
              entry("-to (2)", level="grammar", kind="function word", editors={"agree": 1}), entry("abr", uses=0)]
        lines(d / "lex" / "entries.jsonl", es)
        (d / "lex" / "key.json").write_text(json.dumps({"order": ["P1", "P2", "P3", "P4"],
                                                        "decoys": {"1": {"P4": "'water'"}, "2": {}}}))
        lines(d / "lex" / "answers" / "judge1_a.jsonl", [{"row": r, "verdict": v} for r, v in
                                                         (("P1", "same"), ("P2", "other"), ("P3", "same"), ("P4", "other"))])
        lines(d / "lex" / "answers" / "judge2_a.jsonl", [{"row": r, "verdict": v} for r, v in
                                                         (("P1", "same"), ("P2", "other"), ("P3", "same"), ("P4", "same"))])
        expert_folder(d / "expert", [("M1", "woSi", ["Wos", "ending"], False), ("M2", "l", ["l (2)"], False),
                                     ("M3", "qo", ["qo"], False), ("M4", "to", ["-to (2)"], False)],
                      [("M1", "agree", "Isis"), ("M2", "differ", "the numeral 1"), ("M3", "differ", "the noble"),
                       ("M4", "agree", "part of peseto, King's Son")])
        g = lambda form, level, *parts: {"form": form, "level": level, "parts": [{"form": f, "entry": h} for f, h in parts]}
        lines(d / "glosses.jsonl", [{"id": "T1", "glosses": [
            g("mlo", "meaning", ("mlo", "mlo")), g("mlolowi", "meaning", ("mlo", "mlo"), ("lowi", "ending")),
            g("mloli", "meaning", ("mlo", "mlo"), ("li", "ending")), g("qo", "grammar", ("qo", "qo")),
            g("NAME", "name"), g("12", "number"), g("woSmlo", "meaning", ("woS", "Wos"), ("mlo", "mlo")),
            g("l", "meaning", ("l", "l (2)")), g("xyz", "unknown"), g("psxrkete", "meaning", ("kete", "-wi (5)")),
            g("qomlo", "meaning", ("qo", "qo"), ("mlo", "mlo")), g("qoli", "grammar", ("qo", "qo"), ("li", "ending")),
            g("mloto", "meaning", ("mlo", "mlo"), ("to", "-to (2)"))]}])
        figs, st = X.count(d / "lex", d / "glosses.jsonl", d / "expert")
        assert st == {"mlo": AGREED, "qo": "disputed", "-li (1)": "stated by one", "-lowi": AGREED, "Wos": AGREED,
                      "l (2)": "stated by one", "-wi (5)": "proposed", "-to (2)": AGREED,
                      "abr": "stated by one"}, st                              # abr: behind no translated word
        assert figs["words"] == {"all": 13, "names and numbers": 2, "meaning or grammar": 10, "every entry agreed": 5,
                                 "with an unnamed ending": 2, "with an unnamed ending no agreed entry spells": 1}
        assert figs["translated_by_one_lexicon"] == 12 and figs["agreed_by_two_scholars"] == 7
        assert figs["if_an_unnamed_ending_must_be_spelled_like_an_agreed_one"] == {"agreed_by_two_scholars": 6,
                                                                                   "endings": {"li": 1}}
        assert figs["if_an_agreement_on_a_piece_of_a_word_did_not_count"] == {"entries_agreed_only_so": ["-to (2)"],
                                                                              "agreed_by_two_scholars": 6}
        assert figs["as_first_counted"] == {"statuses": {AGREED: 3, "disputed": 2, "stated by one": 1, "proposed": 2},
                                            "entries_that_change": 2, "agreed_by_two_scholars": 6}
        alone = figs["with_round_one_alone"]                                  # no round two yet: the same count
        assert alone["entries_that_change"] == 0 and alone["agreed_by_two_scholars"] == 7 and "round two" not in figs
        assert figs["two judges"]["rows"] == 3 and figs["decoys, judge 1"] == {"shown": 1, "accepted": 0,
                                                                               "verdicts": {"other": 1}}
        e = figs["entries"]
        assert e["used"] == 9 and e["behind_translated_words"] == 8 and e["with_the_editors_verdict"] == 3
        o = figs["other entries"]
        assert o["count"] == 1 and o["statuses"]["stated by one"] == 1 and o["stated_by_rilly"] == {"meaning": 1}
        assert figs["all entries"] == {AGREED: 4, "disputed": 1, "stated by one": 3, "proposed": 1}
        assert figs["without_round_three"]["entries_that_change"] == [] and "round three" not in figs
        # the stricter rule: Wos and -to are agreed through one editor's "agree" on one word
        strict = figs["if_the_editors_had_to_agree_on_two_words_and_most"]
        assert strict["entries_that_change"] == 2 and strict["agreed_by_two_scholars"] == 5     # woSmlo and mloto
        assert e["agreed_by"] == {"judges": 2, "editors": 2} and e["agreed_with_a_dissent"] == 0
        assert figs["griffith_check"] is None                                   # not answered
        rows = {r["headword"]: r for r in X.table_rows(X.entries_of(d / "lex", d / "expert"), st, X.verdicts_of(d / "lex"))}
        assert (rows["l (2)"]["another_meaning"], rows["l (2)"]["editors_differ"]) == ("", 0)       # the numeral
        assert (rows["qo"]["another_meaning"], rows["qo"]["editors_differ"]) == ("Someone; Millet 2005 or FHN III", 1)
        assert (rows["Wos"]["same_meaning"], rows["Wos"]["status"]) == ("Millet 2005 or FHN III", AGREED)
        assert X.table_text([]) == "\t".join(X.COLUMNS) + "\n"
        # round two: the first judge reads P4, decoyed for it in round one, with the real proposal, beside a decoy
        lines(d / "lex" / "round2" / "answers" / "judge1_c.jsonl", [{"row": "P4", "verdict": "same"},
                                                                    {"row": "P1", "verdict": "other"},
                                                                    {"row": "P9", "verdict": "Same."}])
        (d / "lex" / "round2" / "key.json").write_text(json.dumps(
            {"1": {"order": ["P4", "P1"], "real": ["P4"], "decoys": {"P1": "'water'"}},
             "2": {"order": [], "real": [], "decoys": {}}}))
        assert X.verdicts_of(d / "lex")["P4"] == ("same", "same") and "P4" not in X.verdicts_of(d / "lex", rounds=1)
        figs2, st2 = X.count(d / "lex", d / "glosses.jsonl", d / "expert")
        assert st2["l (2)"] == AGREED and {h for h in st if st[h] != st2[h]} == {"l (2)"}
        assert figs2["agreed_by_two_scholars"] == 8 and figs2["with_round_one_alone"] == {
            "statuses": {s: sum(v == s for h, v in st.items() if h != "abr") for s in X.STATUSES}, "entries_that_change": 1,
            "agreed_by_two_scholars": 7}
        r2 = figs2["round two"]
        assert r2["decoys, judge 1"] == {"shown": 1, "accepted": 0, "verdicts": {"other": 1}}
        assert r2["all lines"]["rows"] == 4 and r2["lines_reread"] == {"1": 1, "2": 0} and r2["unanswered"] == {"1": 0, "2": 0}
        assert r2["unknown_verdicts"] == 1 and r2["bars"] == {"kappa_same_or_not": True, "decoys_accepted": True}
        assert figs2["two judges"] == figs["two judges"]                       # round one's agreement stays as it was


def test_round_two_takes_the_real_verdict_of_the_judge_who_saw_a_decoy():
    """verdicts_of (item 6): on a row decoyed for one judge in round one, that judge's verdict of round two, for
    either judge; never a verdict on a decoy, of either round; a row left unanswered in round two stays out."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "key.json").write_text(json.dumps({"order": ["P1", "P2", "P3", "P4", "P5", "P6"], "decoys": {
            "1": {"P1": "'x'", "P6": "'x'"}, "2": {"P2": "'y'", "P5": "'z'"}}}))
        lines(d / "answers" / "judge1_a.jsonl", [{"row": r, "verdict": v} for r, v in
                                                 (("P1", "partly"), ("P2", "partly"), ("P3", "partly"), ("P4", "same"),
                                                  ("P5", "other"), ("P6", "partly"))])
        lines(d / "answers" / "judge2_a.jsonl", [{"row": r, "verdict": v} for r, v in
                                                 (("P1", "other"), ("P2", "partly"), ("P3", "partly"), ("P4", "same"),
                                                  ("P5", "partly"), ("P6", "other"))])
        assert X.verdicts_of(d) == X.verdicts_of(d, rounds=1) == {"P3": ("partly", "partly"), "P4": ("same", "same")}
        # round two: judge 1 rereads P1 (P6 is not in its key), judge 2 rereads P2 and P5; each sees a decoy on a
        # row it read with the real proposal in round one; judge 2 leaves P5 unanswered
        (d / "round2" / "answers").mkdir(parents=True)
        (d / "round2" / "key.json").write_text(json.dumps(
            {"1": {"order": ["P3", "P1"], "real": ["P1"], "decoys": {"P3": "'w'"}},
             "2": {"order": ["P2", "P4", "P5"], "real": ["P2", "P5"], "decoys": {"P4": "'v'"}}}))
        assert X.verdicts_of(d) == X.verdicts_of(d, rounds=1)                  # not answered yet: round one alone
        lines(d / "round2" / "answers" / "judge1_c.jsonl", [{"row": "P1", "verdict": "same"},
                                                            {"row": "P3", "verdict": "other"},
                                                            {"row": "P6", "verdict": "same"}])
        lines(d / "round2" / "answers" / "judge2_c.jsonl", [{"row": "P2", "verdict": "Same "},
                                                            {"row": "P4", "verdict": "other"}])
        assert X.verdicts_of(d) == {"P1": ("same", "other"), "P2": ("partly", "same"), "P3": ("partly", "partly"),
                                    "P4": ("same", "same")}
        assert X.verdicts_of(d, rounds=1) == {"P3": ("partly", "partly"), "P4": ("same", "same")}


def test_the_bars_of_a_round():
    """A decoy bar of a tenth allows 4 of 41 and 1 of 10, not 1 of 4; an undefined kappa misses its bar."""
    ok = {"kappa_same_or_not": 0.6}
    assert X.bars(ok, [{"shown": 41, "accepted": 4}, {"shown": 10, "accepted": 1}, {"shown": 0, "accepted": 0}]) == \
        {"kappa_same_or_not": True, "decoys_accepted": True}
    assert X.bars(ok, [{"shown": 4, "accepted": 0}, {"shown": 4, "accepted": 1}])["decoys_accepted"] is False
    assert X.bars({"kappa_same_or_not": None}, [])["kappa_same_or_not"] is False
    assert X.bars({"kappa_same_or_not": 0.59}, [])["kappa_same_or_not"] is False
    assert X.caught(["other", None, "partly", "same"]) == {"shown": 4, "accepted": 2,
                                                           "verdicts": {"other": 1, None: 1, "partly": 1, "same": 1}}
    a = X.agreement([("same", "same"), ("same", "same")])                       # chance agreement 1: no kappa
    assert a["rows"] == 2 and a["same_verdict"] == 2 and a["kappa_same_or_not"] is None


def test_public_refuses_a_copied_or_long_meaning():
    """`public` writes neither file when a meaning in our words copies the lexicon or runs past LONGEST words, and
    refuses before it reads the local files the tables need (figures()), so that it refuses in a clone without
    them too."""
    saved, wrote = (X.count, X.PUBLIC, X.write_table, X.figures), []

    def too_early(counted=None):
        raise AssertionError("public read the tables' local files before it refused")
    with tempfile.TemporaryDirectory() as d:
        try:
            X.PUBLIC, X.write_table = Path(d) / "figures.json", lambda rows, path=None, columns=None: wrote.append(rows)
            X.figures = too_early
            for bad in ({"copied_after_rewording": 1, "longest_meaning_in_words": 3},
                        {"copied_after_rewording": 0, "longest_meaning_in_words": X.LONGEST + 1}):
                X.count = lambda: ({"meanings": bad}, {})
                try:
                    X.main(["lexicon.py", "public"])
                except SystemExit as e:
                    assert "nothing written" in str(e), e
                else:
                    raise AssertionError(f"public wrote with {bad}")
                assert not X.PUBLIC.exists() and not wrote
        finally:
            X.count, X.PUBLIC, X.write_table, X.figures = saved


def test_a_copy_is_four_words_in_a_row():
    """The check of the meanings in our words (item 6): quotes around a phrase and a homonym's number do not hide
    a copy, of the lexicon's meaning or of a proposal; three words in a row are no copy. Made-up texts."""
    assert X.words_of("'Under the old red bridge', someone’s k- (2)") == ["under", "the", "old", "red", "bridge",
                                                                          "someone's", "k"]
    e = {"meaning": "'under the old red bridge'", "proposals": [{"proposal": "a cousin of k- (2) in the rowing songs"}]}
    assert X.copied("under the old red bridge", e) and X.copied("cousin of k- in rowing", e)
    assert not X.copied("the old way", e) and not X.copied("under the bridge, a cousin", e)
    assert X.shared_run("", "a b c d") == 0 and X.shared_run("Painter of the Boat", "the painter of the boat") == 4


def test_the_sample_of_griffith():
    es = [entry("qore"), entry("ps-", status="hypothesis", level="kind"), entry("ant", uses=0)]
    es[0]["proposals"] = [{"id": "P1", "author": "Griffith", "proposal": "x"},
                          {"id": "P2", "author": "Griffith 1911a ", "proposal": "y"},
                          {"id": "P3", "author": "Griffith 1912", "proposal": "z"},            # a text we do not hold
                          {"id": "P4", "author": "Hintze", "proposal": "w"}]
    for e in es[1:]:
        e["proposals"] = [{"id": "P9", "author": "Griffith", "proposal": "v"}]             # not read by the judges
    assert [r["id"] for r in X.griffith(es)] == ["P1", "P2"] and [r["id"] for r in X.attributions(es)] == ["P1", "P2"]
    with tempfile.TemporaryDirectory() as d:
        assert X.checked(es, Path(d)) is None
        lines(Path(d) / "answers" / "griffith_check.jsonl",
              [{"row": "P1", "verdict": "Not found"}, {"row": "P2", "verdict": "as stated"},
               {"row": "P2", "verdict": "otherwise"}, {"row": "P8", "verdict": "as stated"}])
        g = X.checked(es, Path(d))
        assert g["verdicts"] == {"not found": 1, "as stated": 1} and g["found"] == 1 and g["unanswered"] == 0
        assert g["drawn_from"] == 2 and g["without_a_year"] == {"drawn_from": 1, "drawn": 1, "not_found": 1}
        assert g["bars"] == {"found": False, "as_stated_share_of_found": True}


def test_decoys_fall_outside_the_line_and_its_field():
    es = [entry("qore", "ruler, sovereign"), entry("wi", "brother"), entry("ato", "water"), entry("at", "bread"),
          entry("kdi", "woman"), entry("yer", "milk"), entry("dime", "cow"), entry("tre", "to give"),
          entry("teneke", "west"), entry("ḫlbi", "bull"), entry("mk", "god"), entry("sem", "wife")]
    rows = [{"id": f"P{n:04d}", "headword": e["headword"], "meaning": e["meaning"], "proposal": f"'{e['meaning']}'"}
            for n, e in enumerate(es * 5, 1)]
    first, second = X.decoys(rows, es)
    assert first and second and not set(first) & set(second)                  # different rows for the two judges
    by = {r["id"]: r for r in rows}
    for shown in (first, second):
        for rid, d in shown.items():
            r = by[rid]
            assert d.startswith("'") and d.strip("'") != r["meaning"]
            assert not X.K.shares(X.K.content(d), X.K.content(r["meaning"] + " " + r["proposal"]))
            assert not X.fields(d) & X.fields(r["meaning"])                   # "kinsman" is no decoy for "brother"
    assert X.fields("brother") == {"kin"} and X.fields("king's son") >= {"kin", "rank"} and not X.fields("water")
    assert X.decoys(rows, es) == [first, second]                             # the same draw again


def test_the_judges_tables_are_never_written_again():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "answers").mkdir()
        (Path(d) / "answers" / "judge1_a.jsonl").write_text('{"row": "P0001", "verdict": "same"}\n')
        try:
            X.packs(Path(d))
        except SystemExit as e:
            assert "not writing the tables again" in str(e)
        else:
            raise AssertionError("the tables were written over a judge's answers")
        # round two's packs and the writer's, each once its answers are in (item 6)
        for name, write, said in (("judge2_c.jsonl", X.second_round, "round two's answers"),
                                  ("meanings.jsonl", X.meanings_pack, "the writer's answers")):
            lines(Path(d) / "round2" / "answers" / name, [{"row": "P0001", "verdict": "same"}])
            try:
                write(Path(d))
            except SystemExit as e:
                assert said in str(e) and "not writing its pack" in str(e), e
            else:
                raise AssertionError(f"{write.__name__} wrote over {name}")


def test_answers_are_read_from_every_pack_of_a_judge():
    with tempfile.TemporaryDirectory() as d:
        a = Path(d) / "answers"
        a.mkdir()
        (a / "judge1_a.jsonl").write_text('{"row": "P0001", "verdict": "Same"}\n\n')
        (a / "judge1_b.jsonl").write_text('{"row": "P0002", "verdict": " other "}\n')
        (a / "judge2_a.jsonl").write_text('{"row": "P0001", "verdict": "partly"}\n')
        assert X.answers(1, Path(d)) == {"P0001": "same", "P0002": "other"}
        assert X.answers(2, Path(d)) == {"P0001": "partly"}


def round_three_folder(d):
    """Made-up rounds one and two, answered, and the entries of round three: rows R... of round three draw their
    decoys from the proposals both judges of round one called "same"."""
    es = [entry("qore", "king, ruler", props=[("P01", "'ruler'"), ("P02", "'lord', 'chief'")]),
          entry("sem", "wife", props=[("P03", "'wife'")]), entry("ato", "water", props=[("P04", "'water'")]),
          entry("at", "bread", props=[("P05", "'bread'"), ("P06", "the same sense")]),
          entry("adb", "land", props=[("P07", "'land, desert'"), ("P08", "a noun of adb, 'land'")]),
          entry("tre", "to give", props=[("P09", "'to give' (accepted as sure)")]),
          entry("dime", "cow", props=[("P10", "compares Nubian ti")]),
          entry("kdi", "woman", uses=0, props=[("P20", "'female'"), ("P21", "compares Nubian karri")]),
          entry("Wos", "Isis", level="name", kind="god name", props=[("P22", "'Isis'")]),
          entry("Pilqe", "Philae", level="name", kind="place name", uses=0, props=[("P23", "Coptic pilakeh")]),
          entry("ase", "cow", status="hypothesis", level="hypothesis", uses=0, props=[("P24", "'female child'")])]
    lines(d / "entries.jsonl", es)
    first = [p["id"] for e in es if X.judged(e) for p in e["proposals"]]
    (d / "key.json").write_text(json.dumps({"order": first, "decoys": {"1": {}, "2": {}}}))
    for j in "12":
        lines(d / "answers" / f"judge{j}_a.jsonl", [{"row": r, "verdict": "same"} for r in first])
    return es


def test_round_three_reads_every_real_line_beside_decoy_lines():
    """third_round() (item 7): each judge reads every real line of the entries rounds one and two did not send,
    and decoy lines of its own, all under new ids; a decoy is a real proposal both judges called "same" that
    quotes a gloss and stands far from the line, also by the field of persons; it refuses once answered."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        es = round_three_folder(d)
        assert [r["id"] for r in X.rows_for_judges(es, X.judged3)] == ["P20", "P21", "P22", "P23"]
        pool = X.decoy_pool3(es, X.verdicts_of(d, rounds=2))
        assert [i for _, i, _, _ in pool] == ["P01", "P02", "P03", "P04", "P05", "P07", "P09"]   # P06 says "same"
        # P08 names its own entry, P10 quotes no gloss; Wos's P22 was never sent
        kdi = {e["headword"]: e for e in es}["kdi"]
        assert "P03" not in [i for i, _ in X.far_from(kdi, pool)]                    # "wife" is no decoy for "woman"
        assert X.fields("woman") == set() and X.fields("woman", X.FIELD_STEMS3) == {"person"}
        assert X.fields("wife", X.FIELD_STEMS3) == {"kin", "person"} and X.fields("titles", X.FIELD_STEMS3) == {"rank"}
        key = X.third_round(d, n=2)
        assert key == X.third_round(d, d / "again", n=2)                             # the same draw again
        on = []
        for j in "12":
            text = (d / "round3" / "packs" / f"judge{j}.md").read_text(encoding="utf-8")
            ids = re.findall(r"^\| (R\d{3}) \|", text, re.M)
            assert ids == [f"R{k:03d}" for k in range(1, 7)] and "P0" not in text.split("|---|")[-1]
            assert sorted(key[j]["real"].values()) == ["P20", "P21", "P22", "P23"]   # every real line
            assert len(key[j]["decoys"]) == 2 and set(key[j]["real"]).isdisjoint(key[j]["decoys"])
            froms = [x["from"] for x in key[j]["decoys"].values()]
            assert len(set(froms)) == 2 and set(froms) <= {i for _, i, _, _ in pool}
            on += [x["on"] for x in key[j]["decoys"].values()]
            assert f"round3/answers/judge{j}.jsonl" in text and "or a name" in text
        assert len(set(on)) == 4                                                     # different lines for the two
        lines(d / "round3" / "answers" / "judge1.jsonl", [{"row": "R001", "verdict": "same"}])
        try:
            X.third_round(d, n=2)
        except SystemExit as e:
            assert "round three's answers" in str(e)
        else:
            raise AssertionError("round three's packs were written over its answers")


def test_round_three_counts():
    """verdicts_of() takes round three's verdicts on its real lines, never on a decoy line; count() gives its
    bars and the statuses of the other entries, and keeps the count without it."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        round_three_folder(d / "lex")
        key = X.third_round(d / "lex", n=2)
        verdict = {"P20": ("same", "same"), "P21": ("other", "same"), "P22": ("other", "other"), "P23": ("same", "same")}
        for k, j in enumerate("12"):
            got = [{"row": l, "verdict": verdict[p][k]} for l, p in key[j]["real"].items()]
            got += [{"row": l, "verdict": "partly" if j == "2" else "other"} for l in key[j]["decoys"]]
            lines(d / "lex" / "round3" / "answers" / f"judge{j}.jsonl", got)
        assert X.third(d / "lex") == verdict and "P20" not in X.verdicts_of(d / "lex", rounds=2)
        assert X.verdicts_of(d / "lex")["P22"] == ("other", "other")
        expert_folder(d / "expert", [("M1", "kdi", ["kdi"], False)], [("M1", "agree", "woman")])
        g = lambda form, level, *parts: {"form": form, "level": level, "parts": [{"form": f, "entry": h} for f, h in parts]}
        lines(d / "glosses.jsonl", [{"id": "T1", "glosses": [g("qore", "meaning", ("qore", "qore")),
                                                              g("woS", "name", ("woS", "Wos")),
                                                              g("kdi", "kind", ("kdi", "kdi"))]}])
        figs, st = X.count(d / "lex", d / "glosses.jsonl", d / "expert")
        r3 = figs["round three"]
        assert r3["real_lines"] == 4 and r3["decoy_lines"] == {"1": 2, "2": 2} and r3["unanswered"] == {"1": 0, "2": 0}
        assert r3["decoys, judge 1"]["accepted"] == 0 and r3["decoys, judge 2"]["accepted"] == 2
        assert r3["all lines"]["rows"] == 4 and r3["bars"]["decoys_accepted"] is False
        assert st["Wos"] == "disputed" and st["kdi"] == AGREED and st["Pilqe"] == AGREED and st["ase"] == "proposed"
        o = figs["other entries"]
        assert o["statuses"] == {AGREED: 2, "disputed": 0, "stated by one": 0, "proposed": 1}
        assert o["without_round_three"] == {AGREED: 1, "disputed": 0, "stated by one": 1, "proposed": 1}
        assert o["agreed_by"] == {"judges and editors": 1, "judges": 1} and o["proposed_by_level"] == {"hypothesis": 1}
        assert figs["without_round_three"]["entries_that_change"] == ["Wos"]


def test_the_stricter_rule_for_the_editors():
    """strict(): the editors' "agree" counts when they read at least two words built on the entry the same way
    and more the same than partly or otherwise; item 3's rule takes one."""
    keep = lambda **ed: X.strict(entry("a", editors=ed))["editors"]["agree"]
    assert keep(agree=2) == 2 and keep(agree=3, partly=1, differ=1) == 3
    assert keep(agree=1) == 0 and keep(agree=6, partly=49) == 0 and keep(agree=2, partly=2) == 0
    assert X.strict(entry("a", editors={"differ": 1}))["editors"] == {"differ": 1, "agree": 0}


def test_round_one_fields_stay_as_drawn():
    """Round three's field for persons is a table of its own (FIELDS3): round one's fields, with which its key and
    round two's packs were drawn, are as they were, and round three's judges read round one's text but for a
    word on names and the row ids."""
    assert X.FIELDS == {
        "kin": "mother father brother sister child son daughter nephew niece cousin kinsman relative parent "
               "wife husband consort born begotten family relation filiation",
        "rank": "king queen ruler sovereign lord noble prince princess viceroy governor mayor chief official "
                "consort royal title envoy agent priest prophet",
        "god": "god goddess divine deity osiris isis amun amanap apedemak"}
    assert all(X.FIELDS3[k].startswith(v) for k, v in X.FIELDS.items())
    head, rest = X.JUDGE3.split("dictionary:\n", 1)
    assert "or a name, whose meaning is whom or what it names" in head and "P0001" not in X.JUDGE3
    assert rest.replace('"R001"', '"P0001"') == X.JUDGE.split("dictionary:\n", 1)[1]
    assert head.split("Each line")[0] == X.JUDGE.split("Each line")[0]


def test_spellings_and_confirmed_variants():
    """lexicon_refs: Rilly's spellings without the homonym's number, his notes in English; a confirmed piece goes
    to the entry it names (with its number, or by a spelling Rilly lists), not where it is already a spelling: a
    piece of the corpus's letters as it stands, a headword piece by its spellings in those letters. The entries'
    forms are in the corpus's letters, as coverage.entry() gives them (s the se sign, S the s sign, X for ẖ)."""
    assert X.R.spellings({"headword": "-se (1)", "variants": ["Mn (peut-être)", "x (arch.)", " ", "-se"]}) == \
        ["-se", "Mn (?)", "x (archaic)"]
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "confirmed.tsv"
        f.write_text("piece\t" + X.R.PIECE_IS + "\t" + X.R.CHECKED_AS + "\n" + "".join(f"{a}\t{k}\t{b}\n" for a, k, b in (
            ("smlo", "letters", "smlo (1)"), ("qoriti", "letters", "Qoreti"), ("aberse", "letters", "abr"),
            ("Aqedise", "headword", "Aqodise"), ("tepke", "headword", "tipke"), ("snmd", "letters", "smlo (2)"),
            ("aroẖe", "headword", "yiroẖe"), ("yesebe", "headword", "esebe"), ("aroXe", "letters", "yiroẖe"))),
            encoding="utf-8")
        printed = {"smlo (1)": {"variants": []}, "Simlo": {"variants": ["Smlo"]}, "Qoreti": {"variants": []},
                   "abr": {"variants": ["br"]}, "Aqedise": {"variants": ["Qedise", "Aqodise"]},
                   "yiroẖe": {"variants": ["aroẖe"]}, "esebe": {"variants": []}, "yesebe": {"variants": ["esebe (arch.)"]}}
        used = set(printed)
        mine = {h: {"forms": set().union(*(X.L.corpus_spellings(s) for s in [h] + printed[h]["variants"]))} for h in used}
        assert "Smlo" in mine["smlo (1)"]["forms"] and "smlo" not in mine["smlo (1)"]["forms"]     # smlo is se-m-l-o
        got = X.R.confirmed(used, mine, printed, f)
        # Aqedise and yesebe are their own headwords, aroẖe a variant Rilly lists under yiroẖe, in either letters;
        # yesebe is new to esebe, whose spellings it is not
        assert got == {"given": {"smlo (1)": ["smlo"], "Qoreti": ["qoriti"], "abr": ["aberse"], "esebe": ["yesebe"]},
                       "already": ["Aqedise", "aroXe", "aroẖe"], "unmatched": ["snmd", "tepke"]}, got


def test_the_pages_a_record_or_a_running_head_gives():
    """record_page: a page of one author's one work; printed_page: a page's own number counts where a page near
    it shows the same offset (a lone number in a table does not), else the nearest such page's offset."""
    rp = lambda author, text="x": X.R.record_page({"author": author, "proposal": text})
    assert rp("Hintze 1979", '"Variante" (p. 34)') == "p. 34" and rp("Hintze 1979", "(p. 34) and (p. 55)") == "pp. 34, 55"
    assert rp("Griffith 1911a (p. 101)") == "p. 101" and rp("Griffith 1911a (p. 101); Hintze 1963") is None
    assert rp("Griffith 1911a (pp. 101, 103)") == "pp. 101, 103" and rp("Hintze 1979", "(pp. 34-36)") == "pp. 34-36"
    assert rp("Hintze", "(p. 34)") is None and rp("Millet", "(cf. Edwards-Fuller 2000, p. 89)") is None
    assert rp("Priese 1971", "against Trigger (p. 277 [1.13.8])") is None
    pages = {1: "36 INSCRIPTIONS OF KARAN6G\ntext", 2: "DESCRIPTIVE PHRASES 37\ntext", 3: "DESCRIPTIVE PHRASES\ntext",
             4: "69\n109\ntext", 5: "40 INSCRIPTIONS\n1 For two more", 6: "MEROITIC STUDIES\n41\ntext",
             9: "Plate XXXI\n12", 10: "text only"}
    assert [X.R.own_number(pages[n]) for n in (1, 2, 3, 4, 5, 6, 9, 10)] == [36, 37, None, 69, 40, 41, None, None]
    assert [X.R.printed_page(pages, n) for n in (1, 3, 4, 6, 10)] == [36, 38, 39, 41, None]


def test_the_editions_pages_and_fhn_index():
    """edition_pages: each edition's entry once per verdict, with its pages; the index's references as printed."""
    got = X.R.edition_pages({"qore": {"agree": {("fhn", "300"), ("millet", "GA05")}, "differ": {("fhn", "300")},
                                      "partly": {("millet", "GA06")}}, "x": {"agree": {("millet", "GA99")}}},
                            millet={"GA05": (3, 4), "GA06": (5, 5)})
    assert got == {"qore": ["FHN III, FHN 300, pp. 1103-1107 (the same)", "Millet 2005, GA05, pp. 3-4 (the same)",
                            "FHN III, FHN 300, pp. 1103-1107 (otherwise)"]}
    idx = X.R.fhn_index()
    assert idx["kdke"] == ["FHN IV p. 1293 (kdke): see ktke", "FHN IV p. 1293 (kdwe): see ktke",
                           "FHN IV p. 1293 (ktke): FHN 510, 718, 719-22, 723-24, 897-904", "FHN IV p. 1330 (kdwe): FHN 722",
                           "FHN IV p. 1330 (ktke): FHN 510, 903"]
    assert idx["Wos"] == ["FHN IV p. 1262 (Asi): FHN 920-21", "FHN IV p. 1265 (Wos): see Isis"]
    assert idx["Pedeme"] == ["FHN IV p. 1308 (Pedeme): FHN 556, 807-8, 879, 931, 1032, 1036-37"]   # a place
    pages = [p for _, p, _, _ in X.R.FHN4]
    assert pages == sorted(pages)                                              # in the order of the volume


def fhn_key(s):
    """A spelling as FHN IV's index and Rilly's lexicon can be compared: FHN's ñ is Rilly's ne, its ḫ his ḫ and ẖ;
    case, marks under letters, brackets and hyphens aside."""
    s = unicodedata.normalize("NFD", s.replace("ñ", "ne").replace("Ñ", "Ne"))
    return re.sub(r"[^a-z]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def test_fhn_index_as_the_text_layer_prints_it():
    """FHN4, read from the scan's images, against its text layer and its rule (lexicon_refs, item 5): every FHN page
    it gives stands on the page of FHN IV it names; every entry it names is one the map uses and is spelled like the
    term or lists a spelling like it, but for the Meroitic names FHN gives for three gods; and every entry so
    spelled has the term, but for those FHN's gloss or the term's form leaves out."""
    needs("data/sources/fhn4-text/pages.txt", "data/sources/lexicon/entries.jsonl", "data/rilly2003")
    text = X.R.pages_of(X.R.FHN4_TEXT)
    used = {json.loads(l)["headword"] for l in (X.OUT / "entries.jsonl").read_text(encoding="utf-8").splitlines()}
    for h, page, term, where in X.R.FHN4:
        assert h in used, h
        on = re.sub(r"-\s*\n\s*", "-", text[page - X.R.FHN4_OFFSET])          # "1025-" and "31" on two lines
        for n in ([] if where.startswith("see") else re.findall(r"\d+(?:-\d+)?", where)):
            assert n in on, (h, page, n)
    printed, spelled = X.lexicon()[1], {}
    for h in used:
        for s in X.R.spellings(printed[h]):
            spelled.setdefault(fhn_key(X.C.bare(s)), set()).add(h)
    gods = {"Amani": {"Amni"}, "Asi": {"Wos"}, "Asor": {"Asori"}}            # "(Mer. Amûn)", "(Mer. Isis)"...
    # spelled so, but another thing: the gloss (Horus, not are; king, not "it is the king"; Amûn, not Amûn of
    # Thebes; bread; the locative suffix; North), or a word where the entry is an ending (qo, not -qo)
    other = {("Ar[e]", "are (3)"), ("Mni, Mno", "Amnote"), ("qore/qoro", "qor-o"), ("at", "ant"), ("at", "at (1)"),
             ("qo", "-qo"), ("ḫr", "ḫr")} | {("-te", h) for h in ("-se (2)", "-te (4)", "-te (5)", "t- (1)", "te (1)")}
    given = collections.defaultdict(set)
    for h, page, term, where in X.R.FHN4:
        given[(page, term)].add(h)
    for (page, term), hs in given.items():
        like = set().union(*(spelled.get(fhn_key(f), set()) for f in re.split(r"/|, ", term)))
        assert hs - like <= gods.get(term, set()), (page, term, hs - like)
        assert not {h for h in like - hs if (term, h) not in other}, (page, term, like - hs)


def test_griffiths_own_pages():
    """griffith_pages: the printed page of each proposal the check found as stated, read from the page's head."""
    needs("data/sources/lexicon/answers/griffith_check.jsonl", "data/sources/karanog-text/pages.txt",
          "data/sources/griffith-jea-text")
    got = X.R.griffith_pages()
    assert len(got) == 15 and got["P0013"] == "Karanòg (1911), p. 39" and got["P0064"] == "Karanòg (1911), p. 51"
    assert got["P0229"] == "Meroitic Studies IV (1917), p. 167" and got["P0189"] == "Meroitic Studies II (1916), p. 124"


PAGE = ROOT / "data/discovery/lexicon.md"
JUDGES = (99371, 101866, 98363, 89296)                     # the cost, by hand from the task notifications
CHECK = 250976                                             # the check against Griffith, the same
ROUND2 = (71296, 72644)                                    # round two's judges, the same
WRITER = 100947                                            # the writer of the meanings, the same
ROUND3 = (86127, 85265)                                    # round three's judges, the same
EMPTY = {"ps-", "-te (4)", "t- (1)", "-te (5)", "-to (1)", "yi-", "-bete-"}   # entries the lexicon gives no meaning


def table(path=X.TABLE):
    with path.open(encoding="utf-8") as f:
        return {r["headword"]: r for r in csv.DictReader(f, delimiter="\t")}


def other_table():
    return table(X.OTHER_TABLE)


def test_reported_numbers():
    f, text = json.loads(FIGURES.read_text(encoding="utf-8")), " ".join(PAGE.read_text(encoding="utf-8").split())
    w, e, j, t = f["words"], f["entries"], f["two judges"], table()
    share = lambda n, of=w["all"]: f"{n:,} ({n / of:.1%})"
    assert w["all"] == 10290 and f["translated_by_one_lexicon"] == w["names and numbers"] + w["meaning or grammar"]
    assert (f"**Of the {w['all']:,} running words of the clean corpus, {share(f['translated_by_one_lexicon'])} are "
            f"translated by one lexicon, Rilly's of 2003; {share(f['agreed_by_two_scholars'])} are names, numbers or "
            "words built only on entries that a second scholar reads the same way.**") in text
    assert (f"Of the {w['meaning or grammar']:,} words the map translates as a meaning or a grammar word, "
            f"{share(w['every entry agreed'], w['meaning or grammar'])} are built only on such entries") in text
    first = f["as_first_counted"]
    assert f"as first counted, the second figure was {share(first['agreed_by_two_scholars'])}" in text
    assert f"uses {e['used']} entries of the lexicon; {e['behind_translated_words']} of them stand behind" in text
    assert f"{e['with_a_proposal_of_another_scholar']} of the {e['behind_translated_words']} entries have" in text
    assert (f"judged words built on {e['with_the_editors_verdict']} of the {e['behind_translated_words']} entries; on "
            f"{e['with_the_editors_reading']} of them the editors give such a word a meaning") in text
    assert f"without the scholar's name: {f['rows']} proposals" in text
    for k in ("1", "2"):
        d = f[f"decoys, judge {k}"]
        assert f"saw {d['shown']} decoys" in text and f"| {d['accepted']} of {d['shown']} |" in text
    assert f"| {j['kappa_same_or_not']:.2f} |" in text and f["bars"] == {"kappa_same_or_not": True, "decoys_accepted": True}
    assert f"On the {j['rows']} lines both judges saw" in text and f"gave the same verdict on {j['same_verdict']}" in text
    assert f"(kappa {j['kappa']:.2f} on the four verdicts)" in text
    for s in X.STATUSES:
        assert f"| {s} | {e['statuses'][s]} | {e['statuses_by_use'][s]:,} |" in text, s
    assert sum(e["statuses"].values()) == e["behind_translated_words"]
    by = e["agreed_by"]
    assert (f"{by['judges and editors']} entries by both the judges and the editors, {by['judges']} by the judges "
            f"alone, {by['editors']} by the editors alone. {e['agreed_with_a_dissent']} of the "
            f"{e['statuses'][AGREED]} also have a dissent") in text
    y = t["yetmde"]
    assert y["status"] == AGREED and (f"agreed through the editors' reading of {y['editors_agree']} words, while they "
                                      f"read {y['editors_partly']} others only partly the same, and "
                                      f"{len(y['another_meaning'].split('; '))} scholars proposed") in text
    uses = lambda h: t[h]["uses_in_translated_words"]
    disputed = sorted((h for h in t if t[h]["status"] == "disputed"), key=lambda h: -int(uses(h)))
    assert disputed[:4] == ["qo", "mlo", "mte", "-so (2)"]
    assert (f"`qo` ({uses('qo')} uses), `mlo` ({uses('mlo')}), `mte` ({uses('mte')}) and `-so` "
            f"({uses('-so (2)')}) lead") in text
    assert (f"`-wi` ({uses('-wi (5)')} uses), `ps-` ({uses('ps-')}), `-te` ({uses('-te (4)')}), `-kete` "
            f"({uses('-kete')})") in text and all(t[h]["status"] == "proposed" for h in ("-wi (5)", "ps-", "-te (4)", "-kete"))
    assert e["agreed_only_through_an_unnamed_source"] == ["-o (1)"]
    assert (f"One entry, `-o` ({uses('-o (1)')} uses), is agreed only through a view the lexicon records without a "
            "scholar's name") in text
    assert f"{e['only_a_kind']} of the {e['behind_translated_words']} entries are titles or epithets" in text
    o, ot = f["other entries"], other_table()
    assert o["count"] == e["used"] - e["behind_translated_words"] == len(ot)
    al = f["all entries"]
    assert al == {s: e["statuses"][s] + o["statuses"][s] for s in X.STATUSES}
    assert (f"Every one of the {e['used']} entries the map uses has a status: {al[AGREED]} are agreed by two scholars, "
            f"{al['disputed']} disputed, {al['stated by one']} stated by one and {al['proposed']} only proposed") in text
    assert (f"The other {o['count']} entries stand behind names, or behind words the map does not translate. Rilly "
            f"states {sum(o['stated_by_rilly'].values())} of them as a name, a meaning or a grammar word; "
            f"{o['with_a_proposal_of_another_scholar']} of these have a proposal of another scholar, and the editors "
            f"read words built on {o['with_the_editors_verdict']}. The other {o['statuses']['proposed']} he gives") in text
    for s in X.STATUSES:                                                          # section 5's table
        assert f"| {s} | {o['statuses'][s]} | {o['statuses_by_use'][s]:,} |" in text, s
    lv = o["proposed_by_level"]
    assert (f"as a hypothesis ({lv['hypothesis']}), by their kind only ({lv['kind']}) or without a meaning "
            f"({lv['unknown']})") in text and sum(lv.values()) == o["statuses"]["proposed"]
    ou = lambda h: int(ot[h]["uses"])
    assert (f"`ḫr` ({ou('ḫr')} uses) and `ẖol` ({ou('ẖol')}) and the title `pqr` ({ou('pqr')})" in text
            and all(ot[h]["status"] == "proposed" for h in ("ḫr", "ẖol", "pqr")))
    assert f"The editors read words built on {o['proposed_with_an_editors_agree']} of them as the lexicon does" in text
    ob = o["agreed_by"]
    assert (f"**Agreed:** {o['statuses'][AGREED]}, nearly all names: {ob['judges']} by the judges alone, {ob['editors']} "
            f"by the editors alone, {ob['judges and editors']} by both; {o['agreed_with_a_dissent']} of them also") in text
    assert (f"Horus (`Ar`, {ou('Ar (1)')} uses), Philae (`Pilqe`, {ou('Pilqe')}), Sedeinga (`Atiye`, {ou('Atiye')}) "
            f"and Faras (`Pẖrse`, {ou('Pẖrse')})") in text
    disputed3 = sorted((h for h in ot if ot[h]["status"] == "disputed"), key=lambda h: -ou(h))
    assert disputed3 == ["Tebwe", "Nlote", "yeto", "Brebri"] and len(disputed3) == o["statuses"]["disputed"]
    assert (f"`Tebwe` ({ou('Tebwe')} uses), the Abaton for the lexicon, Thebes for Török" in text
            and f"`Nlote` ({ou('Nlote')}), `yeto` ({ou('yeto')}) and `Brebri` ({ou('Brebri')})" in text)
    assert (f"**Stated by one:** {o['statuses']['stated by one']}, nearly all names" in text
            and ot["Amni"]["status"] == "stated by one" and f"Amun (`Amni`, {ou('Amni')} uses) is one" in text)
    w3 = o["without_round_three"]
    assert (f"Without round three, {w3[AGREED]} of the {o['count']} would be agreed, {w3['disputed']} disputed and "
            f"{w3['stated by one']} stated by one.") in text
    r3 = f["round three"]
    assert r3["unanswered"] == {"1": 0, "2": 0} and r3["unknown_verdicts"] == 0 and r3["bars"] == \
        {"kappa_same_or_not": True, "decoys_accepted": True}
    assert (f"{r3['lines_on']['other entries']} on the other entries and {r3['lines_on']['names behind translated words']} "
            f"on the names inside translated words") in text and sum(r3["lines_on"].values()) == r3["real_lines"]
    assert f"Each judge read all {r3['real_lines']} real lines" in text
    assert all(f"and {n} lines more, each with a" in text for n in set(r3["decoy_lines"].values()))
    assert f"| {r3['all lines']['kappa_same_or_not']:.2f} |" in text
    for k in "12":
        d = r3[f"decoys, judge {k}"]
        assert d == {"shown": 20, "accepted": 0, "verdicts": {"other": 20}} and f"| {d['accepted']} of {d['shown']} |" in text
    assert (f"On the {r3['all lines']['rows']} real lines the judges gave the same verdict on {r3['all lines']['same_verdict']} "
            f"(kappa {r3['all lines']['kappa']:.2f} on the four verdicts)") in text
    wo = f["without_round_three"]
    assert wo["entries_that_change"] == ["Mnp"] and wo["agreed_by_two_scholars"] == f["agreed_by_two_scholars"]
    assert (f"the god `Mnp` ({uses_of(t, 'Mnp')} uses), whose meaning two of its proposals give as the lexicon does "
            "and one otherwise") in text and t["Mnp"]["same_meaning"] and t["Mnp"]["another_meaning"]
    sr = f["if_the_editors_had_to_agree_on_two_words_and_most"]
    assert (f"{sr['statuses'][AGREED]} of the {e['behind_translated_words']} would be agreed ({sr['entries_that_change']} "
            f"entries change) and the second figure would be {share(sr['agreed_by_two_scholars'])}") in text
    assert f"Held to a stricter rule for the editors' readings it would be {share(sr['agreed_by_two_scholars'])}" in text
    rf, cv = f["references"], f["references"]["confirmed_variants"]
    assert (f"{rf['entries_with_variants_rilly_lists']} entries have variants" in text
            and f"{cv['given']} of the {cv['pieces']} go to {cv['entries']} entries the map uses; "
                f"{len(cv['already_a_spelling_of_the_entry_they_name'])} are already a spelling of the entry they "
                f"name, and {len(cv['naming_no_entry_the_map_uses'])} names an entry the map does not use" in text)
    assert cv["given"] + len(cv["already_a_spelling_of_the_entry_they_name"]) + len(cv["naming_no_entry_the_map_uses"]) \
        == cv["pieces"]
    assert (f"of the {rf['agreeing_or_dissenting_proposals']} proposals both judges found the same or otherwise, Rilly's "
            f"record gives a page for none" in text and rf["with_a_page_in_rillys_record"] == 0
            and f"For {rf['with_griffiths_own_page']} of them the table gives Griffith's own page" in text)
    assert f"for {rf['entries_with_an_editions_page']} entries, the entries of Millet 2005 and FHN III" in text
    assert (f"for {rf['entries_with_fhn_index']} entries, FHN IV's indexes" in text
            and f"({rf['fhn_index_items']} references, read from the page images" in text)
    alone = f["with_round_one_alone"]
    assert (f"With round one alone, {alone['entries_that_change']} entries had another status and the second figure "
            f"was {share(alone['agreed_by_two_scholars'])}.") in text
    assert f"with the first round alone it was {share(alone['agreed_by_two_scholars'])}" in text
    assert f"so the {f['rows'] - j['rows']} lines that carried a decoy" in text
    r2 = f["round two"]
    assert r2["lines_reread"] == {"1": 41, "2": 41} and r2["unanswered"] == {"1": 0, "2": 0}
    assert r2["unknown_verdicts"] == 0
    assert (f"on all {r2['all lines']['rows']} lines the judges gave the same verdict on {r2['all lines']['same_verdict']} "
            f"(kappa {r2['all lines']['kappa']:.2f} on the four verdicts, {r2['all lines']['kappa_same_or_not']:.2f} on") in text
    d1, d2 = r2["decoys, judge 1"], r2["decoys, judge 2"]
    assert d1 == {"shown": 4, "accepted": 0, "verdicts": {"other": 4}} and "The first judge called its 4 decoys \"other\"" in text
    assert d2 == {"shown": 4, "accepted": 1, "verdicts": {"other": 3, "partly": 1}} and r2["bars"]["decoys_accepted"] is False
    assert "the second called 3 \"other\" and 1 \"partly\"" in text and "round two's decoys fail it" in text
    m = f["meanings"]
    assert m["written"] == e["behind_translated_words"] and m["copied_after_rewording"] == 0
    assert m["longest_meaning_in_words"] <= 8 and m["reworded_for_a_copy"] == sorted(X.REWORDED)
    assert (f"A writer worded the meaning of each of the {m['written']} entries anew, in at most eight words" in text
            and f"; {m['empty']} are empty, where the lexicon gives no meaning" in text)
    assert all(bool(r["meaning_in_our_words"]) == (r["headword"] not in EMPTY) for r in t.values())
    ends = f["if_an_unnamed_ending_must_be_spelled_like_an_agreed_one"]
    lead = "`, `-".join(list(ends["endings"])[:2]) + "` and `-" + list(ends["endings"])[2]
    assert (f"{w['with an unnamed ending']} of the {w['every entry agreed']:,} words carry one, and for "
            f"{w['with an unnamed ending no agreed entry spells']} of them no agreed ending or function word is "
            f"spelled like it (`-{lead}` lead). Held to those, the second figure would be "
            f"{share(ends['agreed_by_two_scholars'])}") in text
    pieces = f["if_an_agreement_on_a_piece_of_a_word_did_not_count"]
    assert pieces["entries_agreed_only_so"] == ["-lowi", "-to (2)"]
    assert (f"`-lowi` and `-to` are agreed only so: the map read `elowi` as the end of `terikelowi` written apart, and "
            f"the editor read `to` as a part of `peseto`. Without such agreements the second figure would be "
            f"{share(pieces['agreed_by_two_scholars'])}.") in text
    g = f["griffith_check"]
    v, y = g["verdicts"], g["without_a_year"]
    assert (f"| {v.get('as stated', 0)} | {v.get('otherwise', 0)} | {v.get('not found', 0)} |" in text
            and sum(v.values()) == X.SAMPLE and g["unanswered"] == 0
            and g["bars"] == {"found": True, "as_stated_share_of_found": True})
    assert (f"The lexicon gives {g['drawn_from']} of the proposals" in text and f"A sample of {X.SAMPLE} of them" in text
            and f"{y['drawn_from']} of the {g['drawn_from']} give no year" in text
            and f"{y['drawn']} of the {X.SAMPLE} drawn are among them" in text)
    assert (f"Both bars are met: {g['found']} found, all as the lexicon states them. The {v['not found']} not found "
            "all cite Griffith without a year") in text and y["not_found"] == v["not found"]
    assert v.get("otherwise", 0) == 0 and g["found"] == v["as stated"]          # "all as the lexicon states them"
    st = first["statuses"]
    assert (f"As first counted: {st[AGREED]} agreed, {st['disputed']} disputed, {st['stated by one']} stated by one "
            f"and {st['proposed']} proposed ({first['entries_that_change']} entries change against the count with both "
            f"rounds), and a second figure of "
            f"{share(first['agreed_by_two_scholars'])}") in text
    assert all(t[h]["status"] == AGREED for h in ("Wos", "Sori", "Asori", "Npte", "Mnp"))     # Mnp: round three
    assert t["l (2)"]["status"] == AGREED and t["-so (2)"]["status"] == "disputed"                 # round two
    assert f"`l` \"to give\" ({uses('l (2)')} uses) and `-so` were disputed only through such words" in text
    assert f"the check against Griffith's text {CHECK:,}, about ten minutes;" in text
    assert (f"round two's two judges {sum(ROUND2):,} ({ROUND2[0]:,} and {ROUND2[1]:,}), about two minutes each; the "
            f"writer {WRITER:,}, about four minutes; round three's two judges {sum(ROUND3):,} ({ROUND3[0]:,} and "
            f"{ROUND3[1]:,}), about three minutes each.") in text
    assert (f"four judges' packs {sum(JUDGES):,} subagent tokens ({JUDGES[0]:,} and {JUDGES[1]:,} for the first "
            f"judge, {JUDGES[2]:,} and {JUDGES[3]:,} for the second)") in text


NUMBER = re.compile(r"\d{4}-\d\d-\d\d|\d[\d,]*(?:\.\d+)?%?")
# numbers a text may state without a figure behind them: years and dates, the step and item it names, the bars set
# beforehand and the costs by hand
STATED = {"1911", "1916", "17", "2003", "2005", "2026", "2026-11-12", "23", "0.6", "10%", "90%", "1.4", "1.8",
          f"{sum(JUDGES):,}", f"{CHECK:,}", f"{sum(JUDGES) + CHECK:,}", f"{sum(ROUND2):,}", f"{WRITER:,}",
          f"{sum(ROUND3):,}"} | {f"{c:,}" for c in JUDGES + ROUND2 + ROUND3}


def known(f):
    """Every number of the figures file and of the public table, as a text writes it, and the shares and bars
    the texts draw from them."""
    out = set()

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, int) and not isinstance(x, bool):
            out.update({str(x), f"{x:,}"})
        elif isinstance(x, float):
            out.add(f"{x:.2f}")
    walk(f)
    for r in table().values():
        walk({c: int(r[c]) for c in ("uses_in_translated_words", "editors_agree", "editors_partly", "editors_differ")})
    for r in other_table().values():
        walk({c: int(r[c]) for c in ("uses", "editors_agree", "editors_partly", "editors_differ")})
    w = f["words"]
    for n in (f["translated_by_one_lexicon"], f["agreed_by_two_scholars"], f["as_first_counted"]["agreed_by_two_scholars"],
              f["with_round_one_alone"]["agreed_by_two_scholars"],
              f["if_an_unnamed_ending_must_be_spelled_like_an_agreed_one"]["agreed_by_two_scholars"],
              f["if_an_agreement_on_a_piece_of_a_word_did_not_count"]["agreed_by_two_scholars"],
              f["if_the_editors_had_to_agree_on_two_words_and_most"]["agreed_by_two_scholars"]):
        out.add(f"{n / w['all']:.1%}")
    out.add(f"{w['every entry agreed'] / w['meaning or grammar']:.1%}")
    walk({"lines with a decoy": f["rows"] - f["two judges"]["rows"], "sample": X.SAMPLE, "found": X.CHECK_BARS["found"],
          "decoys shown": sum(f[f"decoys, judge {j}"]["shown"] for j in "12"),
          "decoys accepted": sum(f[f"decoys, judge {j}"]["accepted"] for j in "12"),
          "round three's decoys": sum(f["round three"][f"decoys, judge {j}"]["shown"] for j in "12"),
          "round three's lines": {j: f["round three"]["real_lines"] + n for j, n in f["round three"]["decoy_lines"].items()},
          "stated by Rilly among the other entries": sum(f["other entries"]["stated_by_rilly"].values()),
          "confirmed variants already a spelling, or naming no entry": [
              len(f["references"]["confirmed_variants"][k])
              for k in ("already_a_spelling_of_the_entry_they_name", "naming_no_entry_the_map_uses")]})
    return out


def numbers(text):
    """The numbers of a text, outside its code blocks, that are neither below 10 nor stated."""
    found = {t.rstrip(",") for t in NUMBER.findall(re.sub(r"```.*?```", " ", text, flags=re.S))}
    return {t for t in found if t not in STATED and not (t.isdigit() and int(t) < 10)}


def test_every_number_on_the_page_is_counted():
    f = json.loads(FIGURES.read_text(encoding="utf-8"))
    text = PAGE.read_text(encoding="utf-8")
    cost = text.index("**Cost,** from the task notifications, by hand")
    assert not numbers(text[:cost]) - known(f), numbers(text[:cost]) - known(f)


def between(text, start, end):
    """The text from start (which stands once) to end, or to the text's end, its spaces as one."""
    assert text.count(start) == 1, start
    rest = text[text.index(start):]
    return " ".join((rest[:rest.index(end)] if end in rest else rest).split())


def test_the_summaries_quote_the_figures():
    f = json.loads(FIGURES.read_text(encoding="utf-8"))
    read = lambda name: (ROOT / name).read_text(encoding="utf-8")
    parts = {"README": between(read("README.md"), "14. **A second scholar", "## The question"),
             "README, step 21": between(read("README.md"), "### 21. A second scholar", "## Reproduce"),
             "REPORT": between(read("REPORT.md"), "## Day five, night", "6. **Cost:**"),
             "REPORT, review": between(read("REPORT.md"), "7. **What the review changed in the count:**", "\n\n"),
             "REPORT, round two": between(read("REPORT.md"), "**Round two of F2**", "\n\n"),
             "REPORT, round three": between(read("REPORT.md"), "**Round three of F2**", "\n\n"),
             "REPORT, pages": between(read("REPORT.md"), "**Spellings and pages:**", "\n\n"),
             "NEXT_STEPS": between(read("NEXT_STEPS.md"), "15. **F2: a second scholar", "Next, in this order"),
             "NEXT_STEPS, F2": between(read("NEXT_STEPS.md"), "    - First pass, 12 November", "24. **F3."),
             "summary page": between(read("docs/report.html"), "<tr><td>Ask of every meaning", "</tr>")}
    w, e = f["words"], f["entries"]
    st = e["statuses"]
    must = [f"{f['agreed_by_two_scholars']:,}", f"{f['agreed_by_two_scholars'] / w['all']:.1%}", f"{w['all']:,}",
            f"{f['translated_by_one_lexicon']:,}", f"{f['translated_by_one_lexicon'] / w['all']:.1%}",
            str(e["behind_translated_words"]), str(st[AGREED]), str(st["disputed"]),
            str(st["stated by one"]), str(st["proposed"])]
    for name in ("README", "REPORT", "NEXT_STEPS", "summary page"):
        missing = [m for m in must if m not in parts[name]]
        assert not missing, (name, missing)
    a, d, s, p = st[AGREED], st["disputed"], st["stated by one"], st["proposed"]   # small numbers: as phrases
    assert f"{a} entries are agreed by two scholars, {d} disputed (" in parts["README"]
    assert f"{s} stated by one and {p} only proposed. One" in parts["README"]
    assert f"{a} agreed by two scholars, {d} disputed, {s} stated by one, {p} only proposed." in parts["REPORT"]
    assert f"{a} are agreed, {d} disputed, {s} stated by one and {p} only proposed, after three" in parts["NEXT_STEPS"]
    al, o = f["all entries"], f["other entries"]
    whole = (f"{al[AGREED]} agreed, {al['disputed']} disputed, {al['stated by one']} stated by one, {al['proposed']} "
             "proposed")
    assert f"of all {e['used']}, {al[AGREED]} are agreed, {al['disputed']} disputed, {al['stated by one']} stated by " \
           f"one and {al['proposed']} only proposed" in parts["README"]
    assert f"Every one of the {e['used']} entries the map uses has a status ({whole})" in parts["NEXT_STEPS"]
    assert f"Of all {e['used']} the map uses, {al[AGREED]} are agreed" in parts["summary page"]
    st3 = o["statuses"]
    assert (f"a status for the {o['count']} other entries the map uses ({st3[AGREED]} agreed, {st3['disputed']} "
            f"disputed, {st3['stated by one']} stated by one, {st3['proposed']} proposed)") in parts["NEXT_STEPS, F2"]
    r3 = sum(f["round three"][f"decoys, judge {j}"]["shown"] for j in "12")
    for name in ("README", "summary page", "NEXT_STEPS, F2"):
        assert f"0 of {r3}" in parts[name] and f["round three"]["bars"]["decoys_accepted"], name
    assert f"{a} are agreed, {d} disputed (" in parts["summary page"]
    assert f"{s} stated by one, {p} only proposed." in parts["summary page"]
    assert f"A second scholar for {a} of the {e['behind_translated_words']} entries" in parts["README"]
    for name in ("README", "REPORT", "summary page"):
        assert f"{f['two judges']['kappa_same_or_not']:.2f}" in parts[name] and str(f["rows"]) in parts[name], name
    # round two's decoys, whose bar the second judge misses by its letter, are stated beside round one's
    r2 = [f["round two"][f"decoys, judge {j}"] for j in "12"]
    assert not f["round two"]["bars"]["decoys_accepted"] and r2[1]["accepted"] == 1
    late = f"{sum(d['accepted'] for d in r2)} of {sum(d['shown'] for d in r2)} in round two"
    for name in ("README", "summary page"):
        assert late in parts[name], name
    assert (f"In round two the second judge accepted {r2[1]['accepted']} of its {r2[1]['shown']} decoys, which "
            "misses the decoy bar by its letter") in parts["REPORT"]
    assert "by the letter of the bar" in parts["REPORT, round two"]
    t = table()
    lead = sorted((h for h in t if t[h]["status"] == "disputed"), key=lambda h: -int(t[h]["uses_in_translated_words"]))[:3]
    assert f"{st['disputed']} disputed (`{lead[0]}`, `{lead[1]}` and `{lead[2]}` lead)" in parts["README"]
    assert f"`{lead[0]}`, `{lead[1]}` and `{lead[2]}` lead the disputed" in parts["REPORT"]
    assert (f"{st['disputed']} disputed (<code>{lead[0]}</code>, <code>{lead[1]}</code> and <code>{lead[2]}</code> "
            "lead)") in parts["summary page"]
    for name, text in parts.items():
        assert not numbers(text) - known(f), (name, numbers(text) - known(f))
    report = " ".join(read("REPORT.md").split())
    assert f"four judges' packs {sum(JUDGES):,} subagent tokens, the check against Griffith {CHECK:,}: " \
           f"{sum(JUDGES) + CHECK:,} before the review" in report
    alone = f["with_round_one_alone"]["agreed_by_two_scholars"]
    ends = f["if_an_unnamed_ending_must_be_spelled_like_an_agreed_one"]["agreed_by_two_scholars"]
    assert f"with round one alone the figure would be {alone:,} ({alone / w['all']:.1%})" in parts["REPORT"]
    assert f"With the first round of judges alone it was {alone:,} ({alone / w['all']:.1%})" in parts["REPORT"]
    assert f"the figure would be {ends:,} ({ends / w['all']:.1%})" in parts["REPORT"]
    pieces = f["if_an_agreement_on_a_piece_of_a_word_did_not_count"]["agreed_by_two_scholars"]
    assert f"without the editors' agreements on pieces of words (which make `-lowi` and `-to` agreed) {pieces:,} " \
           f"({pieces / w['all']:.1%})" in parts["REPORT"]
    first = f["as_first_counted"]
    assert (f"As first counted: {first['statuses'][AGREED]} agreed, {first['statuses']['disputed']} disputed, "
            f"{first['statuses']['stated by one']} stated by one, {first['statuses']['proposed']} proposed, and "
            f"{first['agreed_by_two_scholars']:,} words") in parts["REPORT, review"]
    assert f"The review corrected the first count ({first['agreed_by_two_scholars']:,} words)" in parts["README"]
    assert "[the lexicon's page](lexicon.md)" in read("data/discovery/v6_readers.md")   # the map points to its second figure


def uses_of(t, h):
    return t[h]["uses_in_translated_words"]


def entries_by(entries):
    return {e["headword"]: e for e in entries}


def test_public_figures_are_what_the_local_files_give():
    needs(*LOCAL)
    if not FIGURES.exists():
        return
    needs("data/sources/karanog-text/pages.txt", "data/sources/griffith-jea-text", "data/sources/jssea-text")
    figs, st, entries, verdicts, refs = X.figures()
    assert figs == json.loads(FIGURES.read_text(encoding="utf-8"))
    # as `public` writes it, byte for byte: no count may take its order from a set, which changes from run to run
    assert json.dumps(figs, ensure_ascii=False, indent=1) + "\n" == FIGURES.read_text(encoding="utf-8")
    mine = X.our_meanings()
    assert X.TABLE.read_text(encoding="utf-8") == X.table_text(X.table_rows(entries, st, verdicts, mine, refs))
    assert X.OTHER_TABLE.read_text(encoding="utf-8") == X.table_text(X.other_rows(entries, st, verdicts, refs),
                                                                     X.OTHER_COLUMNS)
    assert len(table()) == figs["entries"]["behind_translated_words"]
    assert len(other_table()) == figs["other entries"]["count"] == len(entries) - len(table())
    every = {**table(), **other_table()}
    assert {h: r["status"] for h, r in every.items()} == st                     # every entry the map uses, rated
    # the meanings in our words: REWORDED stands for exactly those the writer copied, and no meaning of the table
    # shares COPIED words in a row with any text of its entry as the lexicon prints it (the meaning in French and
    # in English, Rilly's discussion, every proposal, his own included)
    by = entries_by(entries)
    answers = (X.ROUND2 / "answers" / "meanings.jsonl").read_text(encoding="utf-8").splitlines()
    writer = {a["headword"]: a["meaning"] for a in (json.loads(l) for l in answers if l.strip()) if a.get("meaning")}
    assert {h for h, m in writer.items() if X.copied(m, by[h])} == set(X.REWORDED)
    assert not [h for h, m in mine.items() if m and X.copied(m, by[h])]
    printed = X.lexicon()[1]
    texts = lambda p: [v for v in p.values() if isinstance(v, str)] + [q.get("proposal") or "" for q in p["proposals"]]
    assert not [h for h, r in table().items() if r["meaning_in_our_words"]
                and max(X.shared_run(r["meaning_in_our_words"], t) for t in texts(printed[h])) >= X.COPIED]
    # the first count's evidence is the file written with the packs: the editors' verdicts, nothing left out
    first = X.editors(leave_out=lambda r, a: False)
    assert all(e["first_editors"] == dict(first.get(e["headword"], {})) for e in entries)


def test_round_two_packs_are_what_the_code_writes():
    """Round two's packs and key were written before its judges and the writer answered: second_round() and
    meanings_pack() write them again byte for byte, into a folder of their own, and decoys() still draws round
    one's decoys as round one's key holds them."""
    needs(*LOCAL, "data/sources/lexicon/round2/packs")
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "round2"
        X.second_round(X.OUT, out)
        X.meanings_pack(X.OUT, out)
        for f in ("key.json", "packs/judge1_c.md", "packs/judge2_c.md", "packs/meanings.md"):
            assert (out / f).read_bytes() == (X.ROUND2 / f).read_bytes(), f
    entries = [json.loads(l) for l in (X.OUT / "entries.jsonl").read_text(encoding="utf-8").splitlines()]
    key = json.loads((X.OUT / "key.json").read_text(encoding="utf-8"))
    assert X.decoys(X.rows_for_judges(entries), entries) == [key["decoys"]["1"], key["decoys"]["2"]]


def test_round_three_packs_are_what_the_code_writes():
    """Round three's packs and key were written before its judges answered: third_round() writes them again byte
    for byte, into a folder of its own."""
    needs("data/sources/lexicon/entries.jsonl", "data/sources/lexicon/key.json", "data/sources/lexicon/answers",
          "data/sources/lexicon/round2/key.json", "data/sources/lexicon/round2/answers",
          "data/sources/lexicon/round3/key.json", "data/sources/lexicon/round3/packs")
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "round3"
        X.third_round(X.OUT, out)
        for f in ("key.json", "packs/judge1.md", "packs/judge2.md"):
            assert (out / f).read_bytes() == (X.ROUND3 / f).read_bytes(), f


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
