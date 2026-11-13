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


PAGE = ROOT / "data/discovery/lexicon.md"
JUDGES = (99371, 101866, 98363, 89296)                     # the cost, by hand from the task notifications


def test_reported_numbers():
    f, text = json.loads(FIGURES.read_text(encoding="utf-8")), " ".join(PAGE.read_text(encoding="utf-8").split())
    w, e, j = f["words"], f["entries"], f["two judges"]
    assert w["all"] == 10290 and f["translated_by_one_lexicon"] == w["names and numbers"] + w["meaning or grammar"]
    assert (f"**Of the {w['all']:,} running words of the clean corpus, {f['translated_by_one_lexicon']:,} "
            f"({f['translated_by_one_lexicon'] / w['all']:.1%}) are translated by one lexicon") in text
    assert (f"{f['agreed_by_two_scholars']:,} ({f['agreed_by_two_scholars'] / w['all']:.1%}) rest only on meanings "
            "that a second scholar gives too") in text
    assert (f"Of the {w['meaning or grammar']:,} words the map translates as a meaning or a grammar word, "
            f"{w['every entry agreed']:,} ({w['every entry agreed'] / w['meaning or grammar']:.1%})") in text
    assert f"uses {e['used']} entries of the lexicon; {e['behind_translated_words']} of them stand behind" in text
    assert f"{e['with_a_proposal_of_another_scholar']} of the {e['behind_translated_words']} entries have" in text
    assert f"words built on {e['with_the_editors_verdict']} of the {e['behind_translated_words']} entries" in text
    assert f"without the scholar's name: {f['rows']} proposals" in text
    for k in ("1", "2"):
        d = f[f"decoys, judge {k}"]
        assert d["shown"] == 41 and f"| {d['accepted']} of {d['shown']} |" in text
    assert f"| {j['kappa_same_or_not']:.2f} |" in text and f["bars"] == {"kappa_same_or_not": True, "decoys_accepted": True}
    assert f"On the {j['rows']} lines both judges saw" in text and f"gave the same verdict on {j['same_verdict']}" in text
    assert f"(kappa {j['kappa']:.2f} on the four verdicts)" in text
    for s in ("agreed by two scholars", "disputed", "stated by one", "proposed"):
        assert f"| {s} | {e['statuses'][s]} | {e['statuses_by_use'][s]:,} |" in text, s
    assert sum(e["statuses"].values()) == e["behind_translated_words"]
    by = e["agreed_by"]
    assert (f"{by['judges and editors']} entries by both the judges and the editors, {by['judges']} by the judges "
            f"alone, {by['editors']} by the editors alone. {e['agreed_with_a_dissent']} of the "
            f"{e['statuses']['agreed by two scholars']} also have a dissent") in text
    assert e["agreed_only_through_an_unnamed_source"] == ["-o (1)"]
    assert "One entry, `-o` (246 uses), is agreed only through a view the lexicon records without a scholar's name" in text
    alone = f["if_a_decoyed_row_kept_its_one_real_verdict"]
    assert (f"{alone['entries_that_change']} entries would change status and the second figure would be "
            f"{alone['agreed_by_two_scholars']:,} ({alone['agreed_by_two_scholars'] / w['all']:.1%}), not "
            f"{f['agreed_by_two_scholars']:,}") in text
    assert f"so the {f['rows'] - j['rows']} lines that carried a decoy" in text
    g = f["griffith_check"]
    v = g["verdicts"]
    assert (f"| {v.get('as stated', 0)} | {v.get('otherwise', 0)} | {v.get('not found', 0)} |" in text
            and sum(v.values()) == 20 and g["bars"] == {"found": True, "as_stated_share_of_found": True})
    assert f"Both bars are met: {g['found']} found, all as the lexicon states them. The {v['not found']} not found" in text
    assert v.get("otherwise", 0) == 0 and g["found"] == v["as stated"]          # "all as the lexicon states them"
    assert "the check against Griffith's text 250,976, about ten minutes." in text
    assert (f"four judges' packs {sum(JUDGES):,} subagent tokens ({JUDGES[0]:,} and {JUDGES[1]:,} for the first "
            f"judge, {JUDGES[2]:,} and {JUDGES[3]:,} for the second)") in text


def between(text, start, end):
    """The text from start (which stands once) to end, its spaces as one."""
    assert text.count(start) == 1, start
    rest = text[text.index(start):]
    return " ".join(rest[:rest.index(end)].split())


def test_the_summaries_quote_the_figures():
    f = json.loads(FIGURES.read_text(encoding="utf-8"))
    read = lambda name: (ROOT / name).read_text(encoding="utf-8")
    parts = {"README": between(read("README.md"), "14. **A second scholar", "## The question"),
             "REPORT": between(read("REPORT.md"), "## Day five, night", "6. **Cost:**"),
             "NEXT_STEPS": between(read("NEXT_STEPS.md"), "15. **F2, first pass", "Next, in this order"),
             "summary page": between(read("docs/report.html"), "<tr><td>Ask of every meaning", "</tr>")}
    w, e = f["words"], f["entries"]
    st = e["statuses"]
    must = [f"{f['agreed_by_two_scholars']:,}", f"{f['agreed_by_two_scholars'] / w['all']:.1%}", f"{w['all']:,}",
            f"{f['translated_by_one_lexicon']:,}", f"{f['translated_by_one_lexicon'] / w['all']:.1%}",
            str(e["behind_translated_words"]), str(st["agreed by two scholars"]), str(st["disputed"]),
            str(st["stated by one"]), str(st["proposed"])]
    for name, text in parts.items():
        missing = [m for m in must if m not in text]
        assert not missing, (name, missing)
    for name in ("README", "REPORT", "summary page"):
        assert f"{f['two judges']['kappa_same_or_not']:.2f}" in parts[name] and str(f["rows"]) in parts[name], name
    report = " ".join(read("REPORT.md").split())
    assert f"four judges' packs {sum(JUDGES):,} subagent tokens, the check against Griffith 250,976: " \
           f"{sum(JUDGES) + 250976:,} before the review" in report
    alone = f["if_a_decoyed_row_kept_its_one_real_verdict"]["agreed_by_two_scholars"]
    assert f"the figure would be {alone:,} ({alone / w['all']:.1%})" in parts["REPORT"]


def test_public_figures_are_what_the_local_files_give():
    needs(*LOCAL)
    if not FIGURES.exists():
        return
    figs, st = X.count()
    assert figs == json.loads(FIGURES.read_text(encoding="utf-8"))
    entries = [json.loads(l) for l in (X.OUT / "entries.jsonl").read_text(encoding="utf-8").splitlines()]
    rows = X.table_rows(entries, st, X.verdicts_of())
    lines = X.TABLE.read_text(encoding="utf-8").splitlines()
    assert len(lines) == len(rows) + 1 == figs["entries"]["behind_translated_words"] + 1
    assert [l.split("\t")[0] for l in lines[1:]] == [r["headword"] for r in rows]


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
