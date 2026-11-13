"""Checks for F2, the lexicon with a source and a status for every meaning (src/lexicon.py).

  python3 -I tests/test_lexicon.py

Rilly's lexicon, the map's gloss file, the judges' tables and answers are local only: the checks of the method run
on made-up entries and rows; the checks of the reported numbers read the public figures file and compare it with
the local files where those are present.
"""
import json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import lexicon as X    # noqa: E402
from local_only import needs, run   # noqa: E402

FIGURES = ROOT / "data/discovery/lexicon_figures.json"
LOCAL = ("data/rilly2003", "data/sources/v6/analysts/glosses.jsonl", "data/sources/expert/rows.jsonl",
         "data/sources/lexicon/key.json", "data/sources/lexicon/answers")


def entry(h, meaning="king", status="established", level="meaning", props=(), editors=None, uses=3):
    return {"headword": h, "kind": "", "level": level, "status": status, "page": 1, "meaning": meaning,
            "vague": False, "uses": uses, "uses_translated": uses,
            "proposals": [{"id": i, "author": "Someone", "proposal": p} for i, p in props], "editors": editors or {}}


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
                                                                    props=[("P0004", "'the'")])]
    assert [r["id"] for r in X.rows_for_judges(es)] == ["P0001", "P0004"]


def test_the_statuses_as_set_before_the_judges():
    v = {"P1": ("same", "same"), "P2": ("same", "partly"), "P3": ("other", "other"), "P4": ("partly", "partly")}
    assert X.status(entry("a", props=[("P1", "")]), v) == "agreed by two scholars"
    assert X.status(entry("a", props=[("P2", "")]), v) == "stated by one"            # the judges split
    assert X.status(entry("a", props=[("P4", "")]), v) == "stated by one"            # "partly" is not enough
    assert X.status(entry("a", props=[("P3", "")]), v) == "disputed"
    assert X.status(entry("a", props=[("P1", ""), ("P3", "")]), v) == "agreed by two scholars"
    assert X.status(entry("a", editors={"agree": 1}), v) == "agreed by two scholars"
    assert X.status(entry("a", editors={"differ": 2, "partly": 1}), v) == "disputed"
    assert X.status(entry("a", editors={"partly": 2}), v) == "stated by one"
    assert X.status(entry("a"), v) == "stated by one"
    assert X.status(entry("a", status="hypothesis", props=[("P1", "")]), v) == "proposed"
    assert X.status(entry("a", level="kind", props=[("P1", "")]), v) == "proposed"
    assert X.status(entry("a", props=[("P9", "")]), v) == "stated by one"            # a decoyed row counts not


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


def test_answers_are_read_from_every_pack_of_a_judge():
    with tempfile.TemporaryDirectory() as d:
        a = Path(d) / "answers"
        a.mkdir()
        (a / "judge1_a.jsonl").write_text('{"row": "P0001", "verdict": "Same"}\n\n')
        (a / "judge1_b.jsonl").write_text('{"row": "P0002", "verdict": " other "}\n')
        (a / "judge2_a.jsonl").write_text('{"row": "P0001", "verdict": "partly"}\n')
        assert X.answers(1, Path(d)) == {"P0001": "same", "P0002": "other"}
        assert X.answers(2, Path(d)) == {"P0001": "partly"}


def test_public_figures_are_what_the_local_files_give():
    needs(*LOCAL)
    if not FIGURES.exists():
        return
    figs, _ = X.count()
    assert figs == json.loads(FIGURES.read_text(encoding="utf-8"))


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
