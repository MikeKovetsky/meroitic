"""Checks for F2, the lexicon with a source and a status for every meaning (src/lexicon.py).

  python3 -I tests/test_lexicon.py

Rilly's lexicon, the map's gloss file, the judges' tables and answers are local only: the checks of the method run
on made-up entries and rows; the checks of the reported numbers read the public figures file and table and compare
them with the local files where those are present.
"""
import csv, json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import lexicon as X    # noqa: E402
from local_only import needs, run   # noqa: E402

FIGURES = ROOT / "data/discovery/lexicon_figures.json"
LOCAL = ("data/rilly2003", "data/sources/v6/analysts/glosses.jsonl", "data/sources/expert/rows.jsonl",
         "data/sources/expert/answers", "data/sources/lexicon/entries.jsonl", "data/sources/lexicon/key.json",
         "data/sources/lexicon/answers")
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
                      "l (2)": "stated by one", "-wi (5)": "proposed", "-to (2)": AGREED}, st
        assert figs["words"] == {"all": 13, "names and numbers": 2, "meaning or grammar": 10, "every entry agreed": 5,
                                 "with an unnamed ending": 2, "with an unnamed ending no agreed entry spells": 1}
        assert figs["translated_by_one_lexicon"] == 12 and figs["agreed_by_two_scholars"] == 7
        assert figs["if_an_unnamed_ending_must_be_spelled_like_an_agreed_one"] == {"agreed_by_two_scholars": 6,
                                                                                   "endings": {"li": 1}}
        assert figs["if_an_agreement_on_a_piece_of_a_word_did_not_count"] == {"entries_agreed_only_so": ["-to (2)"],
                                                                              "agreed_by_two_scholars": 6}
        assert figs["as_first_counted"] == {"statuses": {AGREED: 3, "disputed": 2, "stated by one": 1, "proposed": 2},
                                            "entries_that_change": 2, "agreed_by_two_scholars": 6}
        alone = figs["if_a_decoyed_row_kept_its_one_real_verdict"]           # P4 keeps the second judge's "same"
        assert alone["entries_that_change"] == 1 and alone["agreed_by_two_scholars"] == 8
        assert figs["two judges"]["rows"] == 3 and figs["decoys, judge 1"] == {"shown": 1, "accepted": 0,
                                                                               "verdicts": {"other": 1}}
        e = figs["entries"]
        assert e["used"] == 9 and e["behind_translated_words"] == 8 and e["with_the_editors_verdict"] == 3
        assert e["agreed_by"] == {"judges": 2, "editors": 2} and e["agreed_with_a_dissent"] == 0
        assert figs["griffith_check"] is None                                   # not answered
        rows = {r["headword"]: r for r in X.table_rows(X.entries_of(d / "lex", d / "expert"), st, X.verdicts_of(d / "lex"))}
        assert (rows["l (2)"]["another_meaning"], rows["l (2)"]["editors_differ"]) == ("", 0)       # the numeral
        assert (rows["qo"]["another_meaning"], rows["qo"]["editors_differ"]) == ("Someone; Millet 2005 or FHN III", 1)
        assert (rows["Wos"]["same_meaning"], rows["Wos"]["status"]) == ("Millet 2005 or FHN III", AGREED)
        assert X.table_text([]) == "\t".join(X.COLUMNS) + "\n"


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
CHECK = 250976                                             # the check against Griffith, the same


def table():
    with X.TABLE.open(encoding="utf-8") as f:
        return {r["headword"]: r for r in csv.DictReader(f, delimiter="\t")}


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
    assert disputed[:4] == ["qo", "mlo", "mte", "nse doke"]
    assert (f"`qo` ({uses('qo')} uses), `mlo` ({uses('mlo')}), `mte` ({uses('mte')}) and `nse doke` "
            f"({uses('nse doke')}) lead") in text
    assert (f"`-wi` ({uses('-wi (5)')} uses), `ps-` ({uses('ps-')}), `-te` ({uses('-te (4)')}), `-kete` "
            f"({uses('-kete')})") in text and all(t[h]["status"] == "proposed" for h in ("-wi (5)", "ps-", "-te (4)", "-kete"))
    assert e["agreed_only_through_an_unnamed_source"] == ["-o (1)"]
    assert (f"One entry, `-o` ({uses('-o (1)')} uses), is agreed only through a view the lexicon records without a "
            "scholar's name") in text
    assert f"{e['only_a_kind']} of the {e['behind_translated_words']} entries are titles or epithets" in text
    alone = f["if_a_decoyed_row_kept_its_one_real_verdict"]
    assert (f"{alone['entries_that_change']} entries would change status and the second figure would be "
            f"{share(alone['agreed_by_two_scholars'])}, not {f['agreed_by_two_scholars']:,}") in text
    assert f"so the {f['rows'] - j['rows']} lines that carried a decoy" in text
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
            f"and {st['proposed']} proposed ({first['entries_that_change']} entries change), and a second figure of "
            f"{share(first['agreed_by_two_scholars'])}") in text
    assert all(t[h]["status"] == AGREED for h in ("Wos", "Sori", "Asori", "Npte")) and t["Mnp"]["status"] == "stated by one"
    assert t["l (2)"]["status"] == t["-so (2)"]["status"] == "stated by one"
    assert f"`l` \"to give\" ({uses('l (2)')} uses) and `-so` were disputed only through such words" in text
    assert f"the check against Griffith's text {CHECK:,}, about ten minutes." in text
    assert (f"four judges' packs {sum(JUDGES):,} subagent tokens ({JUDGES[0]:,} and {JUDGES[1]:,} for the first "
            f"judge, {JUDGES[2]:,} and {JUDGES[3]:,} for the second)") in text


NUMBER = re.compile(r"\d{4}-\d\d-\d\d|\d[\d,]*(?:\.\d+)?%?")
# numbers a text may state without a figure behind them: years and dates, the step and item it names, the bars set
# beforehand and the costs by hand
STATED = {"1911", "1916", "17", "2003", "2005", "2026", "2026-11-12", "23", "0.6", "10%", "90%", "1.4", "1.8",
          f"{sum(JUDGES):,}", f"{CHECK:,}", f"{sum(JUDGES) + CHECK:,}"} | {f"{c:,}" for c in JUDGES}


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
    w = f["words"]
    for n in (f["translated_by_one_lexicon"], f["agreed_by_two_scholars"], f["as_first_counted"]["agreed_by_two_scholars"],
              f["if_a_decoyed_row_kept_its_one_real_verdict"]["agreed_by_two_scholars"],
              f["if_an_unnamed_ending_must_be_spelled_like_an_agreed_one"]["agreed_by_two_scholars"],
              f["if_an_agreement_on_a_piece_of_a_word_did_not_count"]["agreed_by_two_scholars"]):
        out.add(f"{n / w['all']:.1%}")
    out.add(f"{w['every entry agreed'] / w['meaning or grammar']:.1%}")
    walk({"lines with a decoy": f["rows"] - f["two judges"]["rows"], "sample": X.SAMPLE, "found": X.CHECK_BARS["found"],
          "decoys shown": sum(f[f"decoys, judge {j}"]["shown"] for j in "12"),
          "decoys accepted": sum(f[f"decoys, judge {j}"]["accepted"] for j in "12")})
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
             "NEXT_STEPS": between(read("NEXT_STEPS.md"), "15. **F2, first pass", "Next, in this order"),
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
    assert f"{s} stated by one and {p} only proposed." in parts["README"]
    assert f"{a} agreed by two scholars, {d} disputed, {s} stated by one, {p} only proposed." in parts["REPORT"]
    assert f"{a} are agreed, {d} disputed, {s} stated by one and {p} only proposed." in parts["NEXT_STEPS"]
    assert f"{a} are agreed, {d} disputed (" in parts["summary page"]
    assert f"{s} stated by one, {p} only proposed." in parts["summary page"]
    assert f"A second scholar for {a} of the {e['behind_translated_words']} entries" in parts["README"]
    for name in ("README", "REPORT", "summary page"):
        assert f"{f['two judges']['kappa_same_or_not']:.2f}" in parts[name] and str(f["rows"]) in parts[name], name
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
    alone = f["if_a_decoyed_row_kept_its_one_real_verdict"]["agreed_by_two_scholars"]
    ends = f["if_an_unnamed_ending_must_be_spelled_like_an_agreed_one"]["agreed_by_two_scholars"]
    assert f"the figure would be {alone:,} ({alone / w['all']:.1%})" in parts["REPORT"]
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


def test_public_figures_are_what_the_local_files_give():
    needs(*LOCAL)
    if not FIGURES.exists():
        return
    figs, st = X.count()
    assert figs == json.loads(FIGURES.read_text(encoding="utf-8"))
    entries = X.entries_of()
    assert X.TABLE.read_text(encoding="utf-8") == X.table_text(X.table_rows(entries, st, X.verdicts_of()))
    assert len(table()) == figs["entries"]["behind_translated_words"]
    # the first count's evidence is the file written with the packs: the editors' verdicts, nothing left out
    first = X.editors(leave_out=lambda r, a: False)
    assert all(e["first_editors"] == dict(first.get(e["headword"], {})) for e in entries)


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
