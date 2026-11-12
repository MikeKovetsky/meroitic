"""Checks for the comparison of the coverage map with two printed editions (src/experts/).

  python3 -I tests/test_experts.py

The editions' text, our gloss file and the judges' answers are local only, so the checks of the method run on
made-up rows and answers; the checks of the reported numbers read the public figures file, and compare it with
the local files where those are present.
"""
import contextlib, csv, io, json, pathlib, re, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src" / "experts"), str(ROOT / "src"), str(ROOT / "tests")]

import close as K      # noqa: E402
import missing as M    # noqa: E402
import publish as U    # noqa: E402
import tally as T      # noqa: E402
from local_only import needs, run   # noqa: E402

PAGE = ROOT / "data/discovery/experts.md"
FIGURES = ROOT / "data/discovery/experts_figures.json"
WORDS = ROOT / "data/discovery/experts_words.tsv"
LOCAL = ("data/sources/expert/rows.jsonl", "data/sources/expert/figures.json",
         "data/sources/expert/meanings_figures.json", "data/sources/expert/missing_grouped.tsv",
         "data/sources/expert/answers/judge1_A.jsonl", "data/sources/expert/answers/extractor.jsonl",
         "data/sources/expert/answers/reader_held.jsonl", "data/rilly2003", "data/sources/coverage/corrected/glosses.jsonl")

# --- src/experts/tally.py ---
def row(i, level, decoy=False, source="millet", pack="A"):
    return {"row": f"M1-{i:03d}", "source": source, "entry": "GA1", "text": "T1", "form": f"w{i}", "level": level,
            "ours": "x", "decoy": decoy, "pack": pack}


def ans(*verdicts, doubt=()):
    return {f"M1-{i:03d}": {"verdict": v, "expert": "e", "doubt": i in doubt} for i, v in enumerate(verdicts, 1)}


def test_count_and_share():
    rows = [row(i, "meaning") for i in range(1, 7)]
    c = T.count(rows, ans("agree", "agree", "partly", "differ", "silent", "absent"))
    assert (c["rows"], c["given"], c["agree"], c["silent"]) == (6, 4, 2, 1)
    assert c["agree_share"] == 0.5 and c["agree_or_partly_share"] == 0.75
    assert T.count(rows, ans("silent"))["agree_share"] is None          # nothing given: no share
    assert T.count(rows, {})["rows"] == 0                               # rows without an answer are not counted
    assert T.count(rows, {})["unanswered"] == 6 and c["unanswered"] == 0
    assert T.count(rows, ans("new", "agree"))["agree_share"] == 0.5     # "new" is in the denominator
    assert T.count(rows, ans("partly", "differ", "differ", "agree"))["agree_or_partly_share"] == 0.5


def test_kappa():
    assert T.kappa([("a", "a"), ("b", "b")]) == 1.0
    assert T.kappa([("a", "b"), ("b", "a")]) == -1.0
    assert T.kappa([("a", "a"), ("a", "b"), ("b", "a"), ("b", "b")]) == 0.0
    assert T.kappa([("a", "a"), ("a", "a"), ("a", "b"), ("b", "b")]) == 0.5   # unequal marginals
    rows = [row(1, "meaning"), row(2, "meaning")]
    t = T.two_judges(rows, ans("partly", "silent"), ans("differ", "absent"))    # same class, other verdict
    assert (t["rows"], t["same_verdict"], t["same_class"]) == (2, 0, 2) and t["kappa_classes"] == 1.0 and t["kappa"] == 0.0
    assert T.kappa([]) is None and T.kappa([("a", "a")]) is None        # chance agreement 1: undefined


def test_decoys_and_levels_are_kept_apart():
    rows = [row(1, "meaning"), row(2, "meaning", decoy=True), row(3, "hypothesis"), row(4, "name"), row(5, "unknown")]
    one = ans("agree", "agree", "new", "differ", "silent", doubt={1})
    f = T.figures(rows, {"judge1": one, "judge2": ans("agree", "differ", "new", "agree", "silent")})
    assert f["translated"]["all"]["rows"] == 2 and f["translated"]["all"]["agree"] == 1     # the decoy is left out
    assert f["translated"]["name"]["differ"] == 1 and f["translated"]["meaning"]["agree"] == 1
    assert f["not_translated"]["all"]["new"] == 1 and f["not_translated"]["unknown"]["silent"] == 1
    assert f["decoys_by_judge"]["judge1"]["agree"] == 1 and f["decoys_by_judge"]["judge2"]["differ"] == 1
    assert f["translated"]["agree_with_doubt"] == 1
    two = f["two_judges"]["judge2"]
    assert two["all rows"]["rows"] == 5 and two["all rows"]["same_verdict"] == 3
    assert two["translated, decoys left out"]["rows"] == 2 and two["translated, decoys left out"]["same_verdict"] == 1


def test_second_judge_on_some_rows():
    rows = [row(1, "meaning"), row(2, "meaning", decoy=True), row(3, "name", pack="C"),
            row(4, "meaning", source="fhn", pack="C"), row(5, "meaning", decoy=True, pack="C"), row(6, "unknown", pack="C")]
    one = ans("agree", "agree", "agree", "differ", "silent", "silent", doubt={3})
    del one["M1-004"]                                                    # the first judge left row 4 out
    two = {k: v for k, v in ans("x", "x", "agree", "agree", "differ", "silent").items() if k >= "M1-003"}
    f = T.figures(rows, {"judge1": one, "judge2": two})
    t = f["two_judges"]["judge2"]
    assert t["all rows"]["rows"] == 3 and t["all rows"]["same_verdict"] == 2     # only rows both judged
    assert t["translated, decoys left out"]["rows"] == 1
    assert t["translated, by this judge"]["agree"] == 2
    assert t["translated, by the first judge on the same rows"]["agree"] == 1
    assert t["translated, by the first judge on the same rows"]["unanswered"] == 1
    assert f["decoys_by_judge"]["judge2"]["rows"] == 1 and f["decoys_by_judge"]["judge2"]["unanswered"] == 0
    assert f["decoys_by_judge"]["judge1"]["rows"] == 2
    assert f["translated"]["all"]["rows"] == 2 and f["translated"]["all"]["unanswered"] == 1
    assert f["translated"]["meaning"]["agree"] == 1
    assert f["translated"]["Millet 2005"]["rows"] == 2 and f["translated"]["FHN III"]["unanswered"] == 1
    assert f["translated"]["agree_with_doubt"] == 1                      # rows 1 and 3 agree, only 3 with doubt


def test_answers_are_checked():
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "judge1_A.jsonl"
        p.write_text("\n".join([
            json.dumps({"row": "M1-001", "verdict": "agree", "expert": "Isis", "doubt": False}),
            json.dumps({"row": "M1-001", "verdict": "differ", "expert": "", "doubt": False}),   # twice
            json.dumps({"row": "M1-002", "verdict": "maybe", "expert": "", "doubt": False}),    # no such verdict
            json.dumps({"row": "M9-001", "verdict": "agree", "expert": "", "doubt": False}),    # no such row
            "not json",
            json.dumps({"row": "M1-003", "verdict": "silent", "doubt": "true"}),                # doubt must be true
            json.dumps({"row": ["M1-004"], "verdict": "agree"}),                                # not a row id
        ]) + "\n", encoding="utf-8-sig")                                                       # with a BOM
        got, bad = T.load_answers(p, {"M1-001", "M1-002", "M1-003", "M1-004"})
    assert got["M1-001"]["verdict"] == "agree" and set(got) == {"M1-001", "M1-003"}
    assert got["M1-003"] == {"verdict": "silent", "expert": "", "doubt": False}
    assert len(bad) == 7 and sum("no answer" in b for b in bad) == 2    # M1-002 and M1-004


def test_lists():
    rows = [row(1, "meaning"), row(2, "hypothesis"), row(3, "meaning", decoy=True), row(4, "unknown")]
    judges = {"judge1": ans("differ", "new", "differ", "silent"), "judge2": ans("agree", "new", "agree", "silent")}
    diff = T.listed(rows, judges, ("partly", "differ", "new"), True)
    assert [x["row"] for x in diff] == ["M1-001"] and diff[0]["second judge"] == "agree: e"
    assert [x["row"] for x in T.listed(rows, judges, T.GIVEN, False)] == ["M1-002"]
    judges["judge2"]["M1-004"] = {"verdict": "new", "expert": "f", "doubt": False}   # only the second judge
    assert [x["row"] for x in T.listed(rows, judges, T.GIVEN, False, any_judge=True)] == ["M1-002", "M1-004"]
    d = T.decoy_list([{**r, "really": "y"} for r in rows], judges)
    assert [(x["row"], x["our real reading"], x["judge1 verdict"]) for x in d] == [("M1-003", "y", "differ")]


def test_main_end_to_end():
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        rows = [row(1, "meaning"), row(2, "unknown"), row(3, "meaning", decoy=True),
                row(4, "grammar", pack="B"), row(5, "meaning", pack="C")]
        (d / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows
                                              + [{**row(9, "name"), "row": None}]), encoding="utf-8")
        (d / "answers").mkdir()
        line = lambda i, v: json.dumps({"row": f"M1-{i:03d}", "verdict": v, "expert": "m", "doubt": False}) + "\n"
        (d / "answers/judge1_A.jsonl").write_text(line(1, "agree") + line(2, "new") + line(3, "agree") + line(5, "agree"))
        (d / "answers/judge1_C.jsonl").write_text(line(5, "differ"))
        (d / "answers/judge2_C.jsonl").write_text(line(5, "agree"))
        (d / "answers/judge1_A.old.jsonl").write_text(line(1, "differ"))
        with contextlib.redirect_stdout(io.StringIO()):
            T.main(["tally.py", str(d)])
        f = json.loads((d / "figures.json").read_text())
        assert f["rows"] == 5 and f["decoys"] == 1
        assert f["translated"]["all"]["agree"] == 1 and f["translated"]["all"]["differ"] == 1
        assert f["translated"]["all"]["unanswered"] == 1                         # pack B has no file
        assert any("no such file" in p for p in f["problems"]["judge1_B.jsonl"])
        assert any("unknown row" in p for p in f["problems"]["judge1_A.jsonl"])   # row 5 is in pack C
        assert f["problems"]["judge1_A.old.jsonl"] and f["decoys_by_judge"]["judge1"]["agree"] == 1
        assert f["two_judges"]["judge2"]["all rows"]["rows"] == 1
        missing = (d / "missing_meanings.tsv").read_text().splitlines()
        assert len(missing) == 2 and missing[1].startswith("M1-002\t")
        assert len((d / "decoys.tsv").read_text().splitlines()) == 2


# --- src/experts/missing.py ---
def test_spellings():
    assert M.spellings("qorise") == ["qoris"]                          # se is the sign s, other s is S
    assert M.spellings("peseto") == ["pesto"]
    assert M.spellings("sem") == ["sm"] and M.spellings("as") == ["aS"]
    assert M.spellings("ñ-a-ne") == ["NaN"] and M.spellings("fia") == ["Na"]   # ñ, ne and the OCR's fi
    assert M.spellings("Mnise mte") == ["mnismte"]
    assert M.spellings("axide") == ["axide"]                            # Millet's x is ḫ, our x
    assert sorted(M.spellings("lh", "Millet 2005")) == ["lX", "lh"]     # Millet's h is ẖ: X, or a plain h
    assert sorted(M.spellings("lh", "FHN III")) == ["lX", "lh", "lx"]   # FHN has lost the marks: either
    assert len(M.spellings("hah", "FHN III")) == 9 and len(M.spellings("hah", "Millet 2005")) == 4
    assert len(set(M.spellings("hhhhhh", "FHN III"))) == 81             # at most four h are varied


def test_kind_of():
    assert M.kind_of("part of ssor, scribe") == "a piece of another word"
    assert M.kind_of("end of the name Tedeqelibale") == "a piece of another word"
    assert M.kind_of("perhaps the beginning of another name") == "a piece of another word"
    assert M.kind_of("Taraqa, personal name") == "a personal name"
    assert M.kind_of("Isemne, a king (Yismeniye)") == "a personal name"
    assert M.kind_of("of the king") == "a word"                         # a word for king, not a name
    assert M.kind_of("in Taman") == "a place or a people"
    assert M.kind_of("Temeya, an ethnic group") == "a place or a people"
    assert M.kind_of("Ballana (Boqh)") == "a place or a people"
    assert M.kind_of("he captured") == "a word" and M.kind_of("") == "a word"


def test_worst_of_parts():
    assert M.worst_of([]) == "not in the map"                           # no letters: nothing found
    assert M.worst_of(["translated", "translated"]) == "translated"
    assert M.worst_of(["translated", "held without an accepted meaning (kind)"]) == \
        "held without an accepted meaning (kind)"
    assert M.worst_of(["held without an accepted meaning (kind)", "not in the map", "translated"]) == "not in the map"


def test_grouping():
    head = ["row", "source", "entry", "text", "word", "level", "our reading", "verdict", "the expert's meaning",
            "expert unsure", "second judge"]
    lines = [["M1-001", "Millet 2005", "GA1", "T1", "abc", "unknown", "—", "new", "brother", "yes", ""],
             ["M2-004", "Millet 2005", "GA2", "T2", "abc", "hypothesis", "kin", "agree", "brother", "", ""],
             ["F3-002", "FHN III", "300", "T3", "abc", "unknown", "—", "silent", "", "", "new: sibling"],
             ["M1-002", "Millet 2005", "GA1", "T1", "trq", "unknown", "—", "new", "Taraqa, personal name", "", ""]]
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "missing_meanings.tsv"
        with p.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(head)
            w.writerows(lines)
        got = {r["word"]: r for r in M.judged({"wi": ("brother", 3), "qore": ("ruler", 9)}, p)}
    a = got["abc"]
    assert a["places"] == 3 and a["kind"] == "a word" and a["expert unsure"] == "yes"
    assert a["verdicts"] == "agree 1, new 1, silent 1" and a["the expert's meaning"] == "brother; sibling"
    assert a["our map"] == "hypothesis, unknown" and a["entries"] == "FHN III 300, Millet 2005 GA1, Millet 2005 GA2"
    assert a["translated words of our map with a like meaning"] == "wi = brother"
    assert got["trq"]["kind"] == "a personal name" and got["trq"]["translated words of our map with a like meaning"] == ""


# --- src/experts/close.py ---
def found(word, meaning, source="Millet 2005", entries=("GA1",), doubt=False, by="extractor"):
    return {"source": source, "entries": list(entries), "word": word, "meaning": meaning, "doubt": doubt, "from": by}


def stub(table):
    """Replace close.held by a lookup in a small table {word: (state, reading)}."""
    K.held = lambda word, source, m: table.get(word, ("not in the map", ""))


def test_comments_start_at_the_heading():
    assert K.comments("GA1: a stela\nTEXT\n1: wos\nCOMMENTARY\nIsis.\nRENDERING\nO Isis") == "COMMENTARY\nIsis.\nRENDERING\nO Isis"
    assert K.comments("246 Medik\nText\nWosi\nComments\nThe text") == "Comments\nThe text"
    assert K.comments("GA2: no heading here") == "GA2: no heading here"
    assert K.comments("GA3: x\nRENDERING\nO Isis") == "RENDERING\nO Isis"          # a rendering without commentary


def test_lines_are_merged_per_source_word_and_meaning():
    stub({"pelmos": ("translated", "general, strategos"), "penn": ("held without an accepted meaning (kind)", "[noun]")})
    rows = K.lines([found("pelmos", "general", entries=["GA4"]),
                    found("Pelmos", "General", entries=["GA29"], doubt=True, by="reader_held"),     # the same line
                    found("pelmos", "general", source="FHN III", entries=["246"]),                 # another source
                    found("pelmos", "strategus", entries=["GA17"]),                                # another meaning
                    found("penn", "year", doubt=True), found("ktwse", "of the Candace")], None)
    assert [r["line"] for r in rows] == ["L001", "L002", "L003", "L004", "L005"]
    first = rows[0]
    assert first["entries"] == ["GA29", "GA4"] and first["doubt"] is False          # unsure only if every mention is
    assert first["from"] == "extractor, reader_held" and first["our map"] == "translated" and first["judged"]
    assert rows[3]["doubt"] is True and rows[3]["judged"]                           # a proposal of ours is judged
    assert rows[4]["our map"] == "not in the map" and not rows[4]["judged"]         # nothing of ours to judge


def test_a_reading_of_marks_only_is_not_judged():
    stub({"x": ("held without an accepted meaning (unknown)", "? / —"), "y": ("translated", "ḫbḫne")})
    rows = K.lines([found("x", "a thing"), found("y", "a title")], None)
    assert [r["judged"] for r in rows] == [False, True]


def test_a_decoy_neither_echoes_our_reading_nor_fits_the_expert():
    rows = [{"line": f"L{i:03d}", "judged": True, "ours": o, "meaning": m} for i, (o, m) in enumerate([
        ("their mother", "she was the mother of"), ("it is the one of the mothers", "mother"),
        ("general, strategos", "strategus"), ("water", "water"), ("abundant bread", "much bread"),
        ("great", "big"), ("viceroy", "prince"), ("agent of Isis", "agent"), ("scribe", "writer"),
        ("nephew, niece", "relative")], 1)]
    for seed in range(40):
        shown = K.with_decoys(rows, seed=seed, share=0.5)
        assert len(shown) == 5
        for r in rows:
            if r["line"] in shown:
                near = K.content(r["ours"]) | K.content(r["meaning"])
                assert not K.shares(K.content(shown[r["line"]]), near), (r, shown[r["line"]])
                assert shown[r["line"]] != r["ours"]
    assert K.content("their mother") == K.content("it is the one of the mothers") == {"mothe"}
    assert K.content("the god") == {"god"} and K.shares(K.content("god"), K.content("goddess Isis"))
    assert not K.shares(K.content("water"), K.content("land"))
    pair = [{"line": "L001", "judged": True, "ours": "god", "meaning": "deity"},          # a word of three letters
            {"line": "L002", "judged": True, "ours": "goddess Isis", "meaning": "lady"},
            {"line": "L003", "judged": True, "ours": "general / water", "meaning": "general of the water"},
            {"line": "L004", "judged": True, "ours": "land / ruler", "meaning": "ruler of the land"}]
    assert K.with_decoys(pair[:2], share=1.0) == {}                                      # "goddess" echoes "god"
    one = {"line": "L005", "judged": True, "ours": "viceroy", "meaning": "prince"}       # one word: no reading of one
    assert K.with_decoys(pair[2:] + [one], share=1.0) == {"L003": "land / ruler", "L004": "general / water"}
    assert K.with_decoys([r for r in rows if "mother" in r["ours"]], share=1.0) == {}     # no far reading: no decoy
    assert K.with_decoys(rows + [{"line": "L099", "judged": False, "ours": "", "meaning": "x"}], share=0.0) == {}


def test_each_judge_has_decoys_of_its_own_and_no_line_is_without_a_real_reading():
    rows = [{"line": f"L{i:03d}", "judged": i != 4, "ours": o, "meaning": m} for i, (o, m) in enumerate([
        ("general, strategos", "strategus"), ("water", "water"), ("abundant bread", "much bread"),
        ("", "a thing"), ("viceroy", "prince"), ("agent of Isis", "agent"), ("scribe", "writer"),
        ("great", "big"), ("wife", "spouse"), ("cattle", "herd"), ("north", "northward")], 1)]
    out = K.table_rows(rows, seed=3, share=0.2)
    shown = [t for t in out if t["row"]]
    assert sorted(t["line"] for t in shown) == sorted(r["line"] for r in rows if r["judged"])   # every line once
    assert [t["row"] for t in shown] == [f"X{n:03d}" for n in range(1, 11)]                # numbered as shown
    assert [t["line"] for t in shown] != sorted(t["line"] for t in shown)                  # and shuffled
    first, second = [t for t in shown if t["decoy"] == 1], [t for t in shown if t["decoy"] == 2]
    assert len(first) == 2 and len(second) == 2                                            # a fifth of ten, each
    for t in shown:
        assert K.shown_to(t, 1) == (t["decoy_reading"] if t["decoy"] == 1 else t["ours"])
        assert K.shown_to(t, 2) == (t["decoy_reading"] if t["decoy"] == 2 else t["ours"])
        assert t["ours"] in (K.shown_to(t, 1), K.shown_to(t, 2))                           # one judge sees ours
        assert (t["decoy_reading"] is None) == (t["decoy"] == 0)
        if t["decoy"]:
            assert t["decoy_reading"] != t["ours"]
    assert [(t["line"], t["row"], t["decoy"]) for t in out if not t["row"]] == [("L004", None, 0)]
    again = K.table_rows(rows, seed=3, share=0.2)
    assert [(t["line"], t["decoy"], t["decoy_reading"]) for t in again] == [(t["line"], t["decoy"], t["decoy_reading"]) for t in out]
    a, b = K.decoys_by_judge(rows, 2, seed=5, share=0.9)                                   # more asked than there are
    assert not set(a) & set(b) and len(a) + len(b) <= 10


def test_decoys_are_spread_through_the_table():
    code = lambda i: chr(97 + i // 26) + chr(97 + i % 26)
    rows = [{"line": f"L{i:03d}", "judged": True, "ours": f"q{code(i)}zz", "meaning": f"v{code(i)}yy"}
            for i in range(80)]
    middle = 0
    for seed in range(12):
        out = K.table_rows(rows, seed=seed)
        at = [n for n, t in enumerate(out) if t["decoy"]]
        assert len(at) == 16                                                   # 8 for each judge
        for judge in (1, 2):
            mine = [n for n, t in enumerate(out) if t["decoy"] == judge]
            assert min(mine) < 80 - 16 and max(mine) >= 16, (seed, judge, mine)  # not a block at either end
        middle += sum(20 <= n < 60 for n in at)
    assert 0.3 < middle / (12 * 16) < 0.7                                      # about half in the middle half


def test_count_end_to_end():
    stub({"pelmos": ("translated", "general, strategos"), "wos": ("translated", "Isis"),
          "mte": ("translated", "child"), "lh": ("translated", "great"), "kdi": ("translated", "woman"),
          "ato": ("held without an accepted meaning (hypothesis)", "water?"), "penn": ("not in the map", ""),
          "ant": ("held without an accepted meaning (kind)", "a title")})
    lines = K.lines([found("pelmos", "general"), found("wos", "Isis"), found("mte", "second, junior"),
                     found("lh", "great", doubt=True), found("kdi", "lady"), found("ato", "water"), found("ant", "priest"),
                     found("penn", "year")], None)
    rows = K.table_rows(lines, seed=1, share=0.0)
    for r in rows:                                          # wos is decoyed for the first judge, kdi for the second
        if r["word"] in ("wos", "kdi", "ant"):
            r["decoy"], r["decoy_reading"] = (2 if r["word"] == "kdi" else 1), "great"
    by = {r["word"]: r["row"] for r in rows}
    with tempfile.TemporaryDirectory() as d:
        folder = pathlib.Path(d)
        (folder / "answers").mkdir()
        (folder / "meanings_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        answer = lambda word, v: json.dumps({"row": by[word], "verdict": v}) + "\n"
        (folder / "answers/meanings_judge1.jsonl").write_text(
            answer("pelmos", "agree") + answer("wos", "agree") + answer("mte", "differ") + answer("ato", "agree")
            + answer("kdi", "partly") + answer("lh", "silent") + answer("ant", "differ"))                           # silent was not asked
        (folder / "answers/meanings_judge2.jsonl").write_text(
            answer("pelmos", "agree") + answer("wos", "agree") + answer("mte", "new") + answer("kdi", "differ"))
        with contextlib.redirect_stdout(io.StringIO()):
            K.count(folder)
        f = json.loads((folder / "meanings_figures.json").read_text())
        lacking = {l["word"]: l["why"] for l in csv.DictReader((folder / "lacking.tsv").open(), delimiter="\t")}
        checked = {l["word"]: (l["first judge"], l["second judge"]) for l in csv.DictReader((folder / "meanings_checked.tsv").open(), delimiter="\t")}
        decoys = list(csv.DictReader((folder / "meanings_decoys.tsv").open(), delimiter="\t"))
    assert (f["lines"], f["judged"], f["decoys"]) == (8, 7, {"first judge": 2, "second judge": 1})
    t1, t2 = f["translated, first judge"], f["translated, second judge"]
    # the first judge's decoy (wos) is left out of its figures; lh is unanswered (its verdict was not one asked)
    assert (t1["rows"], t1["agree"], t1["differ"], t1["partly"], t1["unanswered"]) == (3, 1, 1, 1, 1)
    assert (t2["rows"], t2["agree"], t2["new"], t2["differ"], t2["unanswered"]) == (3, 2, 1, 0, 1)
    assert f["decoys, first judge"]["agree"] == 1 and f["decoys, first judge"]["rows"] == 2
    assert f["decoys, second judge"]["differ"] == 1 and f["decoys, second judge"]["rows"] == 1
    held1 = f["held without an accepted meaning, first judge"]                  # ant, decoyed for it, left out
    assert (held1["rows"], held1["agree"], held1["unanswered"]) == (1, 1, 0)
    assert f["held without an accepted meaning, second judge"]["unanswered"] == 2
    assert f["two judges, translated"]["rows"] == 2 and f["two judges, translated"]["same_verdict"] == 1
    assert any("not one the judges were given" in p for p in f["problems"]["meanings_judge1"])
    assert lacking == {"mte": "our map reads the word otherwise (both judges)",
                       "kdi": "our map reads the word otherwise (the one judge who saw our reading)",
                       "lh": "not judged: no verdict from either judge",
                       "ato": "our map has no accepted meaning for the word",
                       "penn": "our map has no accepted meaning for the word",
                       "ant": "our map has no accepted meaning for the word"}                 # wos: agreed by the second
    assert checked["ant"] == ("(saw a decoy)", "")
    assert checked["wos"] == ("(saw a decoy)", "agree") and checked["kdi"] == ("partly", "(saw a decoy)")
    assert sorted((x["word"], x["our real reading"], x["the decoy shown"], x["shown to"], x["verdict"]) for x in decoys) == [
        ("ant", "a title", "great", "the first judge", "differ"), ("kdi", "woman", "great", "the second judge", "differ"),
        ("wos", "Isis", "great", "the first judge", "agree")]


def test_why_a_line_is_on_the_list():
    v = lambda a, b, state="translated", decoy=0: K.verdict_of({"row": "X001", "our map": state, "decoy": decoy},
                                                      {"X001": {"verdict": a}} if a else {},
                                                      {"X001": {"verdict": b}} if b else {})
    assert v("agree", "agree") == ""
    assert v("differ", "partly") == "our map reads the word otherwise (both judges)"
    assert v("new", "new") == "our map reads the word otherwise (both judges)"
    assert v("agree", "differ") == v("partly", "agree") == "our map may read the word otherwise (one judge of two)"
    assert v("differ", None, decoy=2) == v(None, "new", decoy=1) == \
        "our map reads the word otherwise (the one judge who saw our reading)"
    assert v("differ", None) == "our map may read the word otherwise (one judge; the other gave no verdict)"
    assert v("agree", None) == v(None, "agree") == ""                                      # the one who saw it agrees
    assert v(None, None) == "not judged: no verdict from either judge"
    assert v("agree", "agree", "not in the map") == "our map has no accepted meaning for the word"
    assert v(None, None, "held without an accepted meaning (kind)") == "our map has no accepted meaning for the word"


def test_readers_lines_are_read_with_care():
    with tempfile.TemporaryDirectory() as d:
        folder = pathlib.Path(d)
        (folder / "answers").mkdir()
        (folder / "answers" / "reader_held.jsonl").write_text("﻿" + "\n".join([
            json.dumps({"source": "Millet 2005", "entries": ["GA04", "GA29"], "word": "pelmos", "meaning": "general", "doubt": False}),
            json.dumps({"source": "FHN III", "entry": "246", "word": "ant", "meaning": "hont-priest", "doubt": "yes"}),
            json.dumps({"source": "FHN III", "word": "", "meaning": "nothing"}),          # no word
            json.dumps({"source": "FHN III", "word": "qore"}),                             # no meaning
            "not json", json.dumps(["a", "list"]),
        ]) + "\n", encoding="utf-8")
        got = K.answers_of("reader_held", folder)
    assert [(a["source"], a["word"], a["entries"], a["doubt"]) for a in got] == [
        ("Millet 2005", "pelmos", ["GA04", "GA29"], False), ("FHN III", "ant", ["246"], False)]


# --- src/experts/publish.py and the page ---
def test_groups_by_the_wording_of_our_reading():
    assert U.group_of("nephew, niece +lowi") == U.group_of("(part of yetmdelowi)") == "yetmde"
    assert U.group_of("this one") == U.group_of("this one is") == U.group_of("this is Tnkde") == "qo"
    assert U.group_of("dialectal or orthographic variant of qo") == "qo"
    assert U.group_of("it is this") == U.group_of("Isis") == U.group_of("") == "other"


def test_kinds_of_difference():
    kind = lambda form, verdict, expert: U.difference_of({"form": form}, {"verdict": verdict, "expert": expert})
    assert kind("l", "differ", "the numeral 1") == U.DIFFERENCES[0]
    assert kind("l", "differ", "the article") == U.DIFFERENCES[3]              # an l that is no numeral
    assert kind("mlo", "new", "good") == U.DIFFERENCES[2]
    assert kind("atoye", "differ", "Atoye (personal name)") == kind("So", "differ", "first part of Osiris") == U.DIFFERENCES[1]
    assert kind("dime", "differ", "day") == kind("x", "partly", "renamed thing") == U.DIFFERENCES[3]


def test_breakdown_and_words_on_made_up_rows():
    rows = [dict(row(i, level, decoy), ours=ours, form=form) for i, (level, ours, form, decoy) in enumerate([
        ("meaning", "nephew, niece", "yetmde", False), ("grammar", "this one", "qo", False),
        ("meaning", "to give", "l", False), ("meaning", "adjective", "mlo", False),
        ("meaning", "water +ye", "atoye", False), ("meaning", "cow", "dime", False),
        ("meaning", "water", "ato", False), ("meaning", "water", "ato", True), ("unknown", "", "abrite", False)], 1)]
    one = {f"M1-{i:03d}": {"verdict": v, "expert": e, "doubt": False} for i, (v, e) in enumerate([
        ("partly", "relative"), ("differ", "the noble"), ("differ", "the numeral 1"), ("new", "good"),
        ("differ", "Atoye, a personal name"), ("differ", "day"), ("agree", "water"), ("agree", "water"),
        ("new", "brother")], 1)}
    groups, kinds = U.breakdown(rows, one)
    assert (groups["yetmde"]["rows"], groups["yetmde"]["partly"]) == (1, 1) and groups["qo"]["differ"] == 1
    other = groups["other"]
    assert (other["rows"], other["given"], other["agree"], other["differ"], other["new"]) == (5, 5, 1, 3, 1)   # no decoy
    assert kinds == dict(zip(U.DIFFERENCES, (1, 1, 1, 1)))                     # the untranslated word is not in it
    table = {(w["word"], w["level"]): w for w in U.words(rows, one)}
    assert (table["ato", "meaning"]["places"], table["ato", "meaning"]["agree"], table["ato", "meaning"]["a decoy was shown"]) == (2, 1, 1)
    assert table["abrite", "unknown"]["new"] == 1 and len(table) == 8
    assert list(table["qo", "grammar"]) == ["word", "level", "places", *T.VERDICTS, "a decoy was shown", "no answer"]


def page():
    return re.sub(r"\s+", " ", PAGE.read_text(encoding="utf-8"))


def cells(c, share=True):
    agree = f"{c['agree']} ({c['agree_share']:.1%})" if share else f"{c['agree']}"
    return f"| {c['rows']} | {c['given']} | {agree} | {c['partly']} | {c['differ']} | {c['new']} |"


def test_reported_numbers():
    f, text = json.loads(FIGURES.read_text(encoding="utf-8")), page()
    t, n, w = f["translated"], f["not translated"], f["words"]
    for label, key in (("all", "all"), ("level meaning", "meaning"), ("level grammar", "grammar"), ("level name", "name"),
                       ("level number", "number"), ("against Millet 2005", "Millet 2005"), ("against FHN III", "FHN III")):
        assert f"| {label} {cells(t[key])}" in text, label
    a = t["all"]
    assert f"{a['agree']} of {a['given']} words ({a['agree_share']:.1%})" in text
    quiet = a["silent"] + a["absent"]
    assert f"for {quiet} of the {a['rows']} words the map counts as translated in these texts ({quiet / a['rows']:.1%})" in text
    assert f"silent on {a['silent']} of the {a['rows']} words, and {a['absent']} are not in its text" in text
    assert f"{t['agree_with_doubt']} of the {a['agree']} agreements" in text and f"overlap in part for {a['partly']} more and differ for {a['differ'] + a['new']}" in text
    assert f"(hypothesis) {cells(n['hypothesis'])}".replace("(hypothesis) |", "(the lexicon has a proposal) |") in text
    assert f"(only the kind of word is known) {cells(n['kind'])}" in text and f"| unknown {cells(n['unknown'], share=False)}" in text
    assert f"does not count as translated ({n['all']['rows']})" in text
    g = f["groups"]
    assert cells(g["yetmde"], share=False) in text and cells(g["qo"], share=False) in text
    assert f"| every other word {cells(g['other'])}" in text
    assert f"{g['other']['agree']} of {g['other']['given']} words ({g['other']['agree_share']:.1%})" in text
    d = f["other differences"]
    assert f"The {sum(d.values())} non-agreements of the last row" in text
    for label, key in (("typed as the letter `l`", U.DIFFERENCES[0]), ("read as a word", U.DIFFERENCES[1]),
                       ("only the kind of word", U.DIFFERENCES[2]), ("meaning or identification", U.DIFFERENCES[3])):
        assert f"{label}: {d[key]}.**" in text, label
    assert f"{w['in the texts']:,} in those texts. {w['judged']:,} were judged ({w['judged, Millet 2005']} against Millet, {w['judged, FHN III']} against FHN); {w['masked names, not judged']} masked names and {w['lost, not judged']} words" in text
    x = f["texts"]
    assert f"{x['held by both']} inscriptions, {x['Millet 2005']} of Millet's and {x['FHN III']} of FHN's" in text
    assert f"**Decoys:** {w['decoys']} readings" in text
    one, two = f["decoys"]["judge1"], f["decoys"]["judge2"]
    assert f"for {one['given']} of the {one['rows']} decoys and marked {one['differ']} \"differ\", {one['partly']} \"partly\" and {one['agree']} \"agree\"" in text
    assert f"saw {two['rows']}, found a meaning for {two['given']} and marked all {two['differ']}" in text and two["given"] == two["differ"]
    both = f["two judges"]["judge2"]["all rows"]
    assert f"On the {both['rows']} words both read they gave the same verdict on {both['same_verdict']} (Cohen's kappa {both['kappa']:.2f})" in text
    m = f["meanings"]
    assert f"Together {m['lines from the readers']} lines, {m['lines']} different" in text and f"For the {m['judged']} lines" in text
    for label, key in (("translated", "translated"), ("a proposal only (hypothesis)", "held without an accepted meaning (hypothesis)"),
                       ("the kind only", "held without an accepted meaning (kind)"), ("unknown", "held without an accepted meaning (unknown)"),
                       ("not in the map", "not in the map")):
        assert f"| {label} | {m['our map'][key]} |" in text, label
    j1, j2 = m["translated, first judge"], m["translated, second judge"]
    assert f"on {j1['agree']} of {j1['rows']} and the second on {j2['agree']} of {j2['rows']}" in text
    lack, sure = m["lacking"], m["lacking, stated as sure"]
    for label, key in (("no accepted meaning for the word", "our map has no accepted meaning for the word"),
                       ("both judges say the edition reads it otherwise", "our map reads the word otherwise (both judges)"),
                       ("the one judge who saw our reading", "our map reads the word otherwise (the one judge who saw our reading)"),
                       ("one judge of two", "our map may read the word otherwise (one judge of two)")):
        assert f"{label} | {lack[key]} | {sure[key]} |" in text, label
    assert f"| all | {sum(lack.values())} | {sum(sure.values())} |" in text
    md = m["decoys"]
    assert f"each judge saw {md['first judge']} decoys" in text and md["first judge"] == md["second judge"]
    assert m["decoys, first judge"]["agree"] == m["decoys, second judge"]["agree"] == 0
    assert f"accepted none of the {md['first judge'] + md['second judge']}" in text
    pair = m["two judges, translated"]
    assert f"on the {pair['rows']} lines of the meanings table both saw with our reading, on {pair['same_verdict']} ({pair['kappa']:.2f})" in text
    k = f["new in the held texts"]
    assert (f"for {k['all']} words the map leaves without one: {k['a personal name']} personal names, {k['a piece of another word']} "
            f"pieces of other words, {k['a place or a people']} places or peoples and {k['a word']} words, {k['a word, marked as unsure']} of them") in text
    lines = WORDS.read_text(encoding="utf-8").splitlines()
    assert f"`experts_words.tsv` | {len(lines) - 1} lines" in text


def test_public_files_hold_counts_and_word_forms_only():
    """No reading of ours and no meaning of the experts' may reach a public file: the figures hold numbers under
    fixed labels, the word list holds a word, a level and counts."""
    def strings(x):
        if isinstance(x, dict):
            for v in x.values():
                yield from strings(v)
        elif isinstance(x, list):
            for v in x:
                yield from strings(v)
        elif isinstance(x, str):
            yield x
    assert list(strings(json.loads(FIGURES.read_text(encoding="utf-8")))) == []          # every value is a number
    rows = list(csv.DictReader(WORDS.open(encoding="utf-8"), delimiter="\t"))
    assert list(rows[0]) == ["word", "level", "places", *T.VERDICTS, "a decoy was shown", "no answer"]
    levels = set(T.TRANSLATED) | {"hypothesis", "kind", "unknown"}
    for r in rows:
        assert r["level"] in levels and re.fullmatch(r"[^\s]+", r["word"]), r
        counts = [int(r[c]) for c in list(r)[2:]]
        assert counts[0] == sum(counts[1:]) and counts[0] > 0, r


def test_public_files_are_what_the_local_files_give():
    needs(*LOCAL)
    assert U.public_figures() == json.loads(FIGURES.read_text(encoding="utf-8"))
    every = [json.loads(l) for l in (U.FOLDER / "rows.jsonl").open(encoding="utf-8")]
    rows = [r for r in every if r["row"]]
    table = [{k: str(v) for k, v in line.items()} for line in U.words(rows, U.first_judge(rows))]
    assert table == list(csv.DictReader(WORDS.open(encoding="utf-8"), delimiter="\t"))
    assert sum(int(t["places"]) for t in table) == len(rows)


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
