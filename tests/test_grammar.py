"""Checks for the grammar-first pilot (src/grammar.py, data/discovery/grammar_pilot.md, runs/grammar/).

  python3 -I tests/test_grammar.py

The map, the tables, the finders' rules and the readers' answers are local only: the checks of the method run on
made-up words and rules; the checks of the reported numbers read the public figures file, compare the page with
it, and compare it with a count from the local files where those are present. The rules' tests in runs/grammar/
are public and are checked as they stand.
"""
import ast
import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import grammar as G                  # noqa: E402
import recurring as W                # noqa: E402
import themap as M                   # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/grammar_pilot.md"
HEAD = "\t".join(G.COLUMNS)
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def figs():
    return json.loads(G.PUBLIC.read_text(encoding="utf-8"))


def page():
    return " ".join(PAGE.read_text(encoding="utf-8").split())


def stops(fn, part):
    try:
        fn()
    except SystemExit as e:
        assert part in str(e), e
        return True
    raise AssertionError("did not stop")


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout.strip()


@contextlib.contextmanager
def set_to(obj, **values):
    """Module values (or dict entries) replaced for the length of a check."""
    get = (lambda k: obj[k]) if isinstance(obj, dict) else (lambda k: getattr(obj, k))
    put = (lambda k, v: obj.__setitem__(k, v)) if isinstance(obj, dict) else (lambda k, v: setattr(obj, k, v))
    old = {k: get(k) for k in values}
    for k, v in values.items():
        put(k, v)
    try:
        yield
    finally:
        for k, v in old.items():
            put(k, v)


@contextlib.contextmanager
def a_home():
    """A folder of its own in the place of data/sources/grammar/."""
    with tempfile.TemporaryDirectory() as d:
        with set_to(G, HOME=Path(d)):
            yield Path(d)


def m(cases, holds, comparison):
    return {"cases": cases, "holds": holds, "rate": round(holds / cases, 4) if cases else None, "comparison_rate": comparison}


def a_table(path, kinds):
    """A made-up table: one text of three words for each kind given."""
    lines = [HEAD] + ["\t".join([f"T{k}", kind, "3", str(n), f"w{n}", "unknown", f"w{n}=?", "?"])
                      for k, kind in enumerate(kinds, 1) for n in (1, 2, 3)]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------------------------------- the bars

def test_a_rule_passes_only_over_every_bar():
    """At least 20 cases, holding in at least 80%, at least 30 points above the comparison: a rule one short of a
    bar does not pass, and each verdict names the bars it missed."""
    assert G.BARS == {"cases": 20, "rate": 0.80, "margin": 0.30}
    assert G.verdict_of(m(20, 16, 0.5)) == "passed"                                   # exactly at each of the three bars
    assert G.verdict_of(m(19, 19, 0.1)) == "not passed: fewer than 20 cases"
    assert G.verdict_of(m(100, 79, 0.1)) == "not passed: holds in under 80%"
    assert G.verdict_of(m(100, 85, 0.555)) == "not passed: under 30 points above its comparison"       # 29.5 points
    assert G.verdict_of(m(100, 60, 0.5)) == "not passed: holds in under 80%; under 30 points above its comparison"
    assert G.verdict_of(m(10, 5, 0.4)) == "not passed: fewer than 20 cases; holds in under 80%; under 30 points above its comparison"
    assert G.verdict_of(m(0, 0, 0.0)) == "not passed: fewer than 20 cases"
    assert G.verdict_of(m(50, 50, None)) == "not passed: under 30 points above its comparison"
    # each bar is the one that decides: with that bar alone one step lower, the rule just under it passes
    for bar, lower, rule in (("cases", 19, m(19, 19, 0.1)), ("rate", 0.79, m(100, 79, 0.1)), ("margin", 0.29, m(100, 85, 0.555))):
        assert G.verdict_of(rule) != "passed"
        with set_to(G.BARS, **{bar: lower}):
            assert G.verdict_of(rule) == "passed", bar
    assert G.why_not("not passed: fewer than 20 cases; holds in under 80%") == "fewer than 20 cases"


def test_a_rule_without_a_test_is_dropped_and_a_test_is_counted_as_it_returns():
    rs = {k: {"tuning": {"cases": 30, "holds": 29, "comparison_rate": 0.1}} for k in ("A-1", "A-2", "A-3")}
    ts = {"A-1": lambda rows: (len(rows), len(rows) - 1, 0.123456), "A-2": lambda rows: (len(rows), 0, 0.0)}
    out = G.result_of(rs, ts, list(range(25)))
    assert out["A-1"] == {"cases": 25, "holds": 24, "rate": 0.96, "comparison_rate": 0.1235, "tuning": rs["A-1"]["tuning"], "verdict": "passed"}
    assert out["A-2"]["verdict"] == "not passed: holds in under 80%; under 30 points above its comparison"
    assert out["A-3"] == {"verdict": "dropped: no test could be written from its wording"}
    assert G.same_as_finder(m(30, 29, 0.104), rs["A-1"]["tuning"]) and not G.same_as_finder(m(30, 28, 0.1), rs["A-1"]["tuning"])
    assert not G.same_as_finder(m(30, 29, 0.11), rs["A-1"]["tuning"])


# ------------------------------------------------------------------------------------------------- the readers

def test_a_rule_is_ours_only_when_both_readers_find_it_nowhere():
    nf, st, pt = {"verdict": "not found"}, {"verdict": "stated"}, {"verdict": "partly"}
    assert G.ours(nf, nf)
    assert not any(G.ours(a, b) for a, b in ((nf, st), (st, nf), (nf, pt), (pt, pt), (st, st), (nf, None), (None, nf), (None, None)))
    with a_home() as d:
        nov = d / "novelty"
        for c in (1, 2):
            (nov / f"answers{c}").mkdir(parents=True)
        (nov / "groups.json").write_text(json.dumps([["A-1", "A-2"], ["B-1"]]), encoding="utf-8")
        line = lambda rid, verdict, source="": json.dumps({"id": rid, "verdict": verdict, "source": source})       # noqa: E731
        # reader 1: a rule of the other pack, a second line for A-1, a verdict that is none of the three and a broken line do not count
        (nov / "answers1/N1.jsonl").write_text("\n".join([line("A-1", "not found"), line("A-2", "stated", "Rilly 2016"), line("B-1", "not found"),
                                                          line("A-1", "stated", "Rilly 2021"), line("A-2", "perhaps"), "{broken"]) + "\n", encoding="utf-8")
        (nov / "answers2/N1.jsonl").write_text("\n".join([line("A-1", "not found", "searched q"), line("A-2", "partly", "Griffith 1911, Karanog")]) + "\n",
                                               encoding="utf-8")
        (nov / "answers2/N2.jsonl").write_text(line("B-1", "not found") + "\n", encoding="utf-8")          # reader 1 never answered pack 2
        quiet(G.count, 1)
        out = G.the_readers(1)
    assert out["A-1"] == {"one": "not found", "two": "not found", "ours": True, "sources": []}
    assert out["A-2"] == {"one": "stated", "two": "partly", "ours": False, "sources": ["Griffith 1911, Karanog", "Rilly 2016"]}
    assert out["B-1"] == {"one": None, "two": "not found", "ours": False, "sources": []}
    assert [G.readers_of(out[k]) for k in ("A-1", "A-2", "B-1")] == ["not found by both", "stated by one, partly by the other", "another pair"]


def test_the_readers_packs_hold_the_rules_that_passed_and_are_not_written_twice():
    with a_home() as d:
        rules = [{"id": f"L1-{j}", "statement": f"statement {j}", "cases": f"cases {j}", "holds": f"holds {j}", "comparison": "c",
                  "tuning": {"cases": 40, "holds": 39, "comparison_rate": 0.1}} for j in range(1, 7)]
        (d / "rules").mkdir()
        (d / "rules/L1.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rules), encoding="utf-8")
        res = {r["id"]: m(30, 29, 0.1) | {"verdict": "passed"} for r in rules[:5]} | {"L1-6": m(30, 3, 0.1) | {"verdict": "not passed: holds in under 80%"}}
        (d / "result.json").write_text(json.dumps({"rules": res}), encoding="utf-8")
        quiet(G.packs, 1)
        groups = json.loads((d / "novelty/groups.json").read_text(encoding="utf-8"))
        assert sorted(map(len, groups)) == [2, 3] and sorted(x for g in groups for x in g) == [f"L1-{j}" for j in range(1, 6)]
        for n, g in enumerate(groups, 1):
            one, two = [(d / f"novelty/packs/N{n}_r{c}.md").read_text(encoding="utf-8") for c in (1, 2)]
            head, body = one.split("\n---\n\n")
            assert head == G.READERS_BRIEF.replace("<<N>>", str(len(g))).replace("<<ANSWERS>>", f"data/sources/grammar/novelty/answers1/N{n}.jsonl")
            assert two == one.replace("answers1/", "answers2/") and "<<" not in one
            assert re.findall(r"## Rule `(L1-\d)`", body) == g and "statement 6" not in body          # both readers, the same rules in the same order
            assert all(f"- Counted on texts it was not found in: 29 of 30 cases." in body for _ in g)
        (d / "novelty/answers1/N1.jsonl").write_text("{}\n", encoding="utf-8")
        assert stops(lambda: G.packs(1), "answers exist: the packs are not written again")


def test_a_readers_source_is_given_as_the_work():
    assert G.work("Griffith 1911, Karanog") == "Griffith 1911 (Karanog)" and G.work("Griffith, Meroitic Studies II (JEA)") == "Griffith, Meroitic Studies"
    assert G.work("Rilly 2021 (Dotawo)") == "Rilly 2021" and G.work("Rilly 2016, UCLA Encyclopedia of Egyptology") == "Rilly 2016"
    assert G.work("Rilly 2003 (lexicon, entry -kete)") == "Rilly 2003" and G.work("FHN III") == "Fontes Historiae Nubiorum"
    assert stops(lambda: G.work("a book nobody named"), "a source the figures do not know")


# ------------------------------------------------------------------------------------- the split and the tables

def test_the_split_holds_back_two_fifths_of_each_kind_and_is_drawn_once():
    gl = {f"a{i:02d}": [{}] for i in range(20)} | {f"b{i:02d}": [{}] for i in range(10)} | {f"long{i}": [{}] * G.LONG for i in range(5)}
    rows = {t: {"kind": "funerary" if t[0] != "b" else None} for t in gl}
    sp = G.split_of(gl, rows)
    held, tuning = set(sp["held"]), set(sp["tuning"])
    assert held | tuning == set(gl) and not held & tuning and sp["seed"] == G.SEED == 20261128
    assert [sum(t.startswith(p) for t in held) for p in ("a", "b", "long")] == [8, 4, 2]              # 40% of each stratum, long texts apart
    assert G.split_of(gl, rows) == sp and G.split_of(gl, rows, seed=1)["held"] != sp["held"]
    with a_home() as d:
        (d / "split.json").write_text("{}", encoding="utf-8")
        assert stops(G.split, "the split is drawn: not drawn again")
    with set_to(M, LAYERS=[{"name": "recurring"}, {"name": "another"}]):
        assert stops(G.the_map, "the layers are no longer")


def test_the_tables_are_one_word_a_line_and_the_second_rounds_table_has_no_epitaph():
    gl = {"T1": [{"form": "atolo", "level": "meaning", "gloss": "water  it\nis " + "x" * 80, "parts": [{"form": "ato", "entry": "ato"}, {"form": "lo", "entry": None}]},
                 {"form": "...", "level": "lost"}],
          "T2": [{"form": "qo", "level": "grammar", "gloss": "this one", "parts": [{"form": "qo", "entry": "-qo"}]}]}
    rows = {"T1": {"kind": "funerary"}, "T2": {}}
    lines = list(G.lines_of(["T1", "T2"], gl, rows))
    assert lines[0] == ["T1", "funerary", "2", "1", "atolo", "meaning", "ato=ato lo=?", ("water it is " + "x" * 80)[:70]]
    assert lines[1] == ["T1", "funerary", "2", "2", "...", "lost", "", ""] and lines[2][:4] == ["T2", "not known", "1", "1"]
    with a_home() as d:
        (d / "split.json").write_text(json.dumps({"tuning": ["T1", "T2"], "held": []}), encoding="utf-8")
        with set_to(G, the_map=lambda: gl), set_to(W, corpus_rows=lambda: rows):
            quiet(G.dump)
        table = G.rows_of(d / "tuning.tsv")
        assert [(r["text"], r["n"], r["words_in_text"], r["parts"]) for r in table] == [("T1", 1, 2, "ato=ato lo=?"), ("T1", 2, 2, ""), ("T2", 1, 1, "qo=-qo")]
        assert (d / "tuning.tsv").read_text(encoding="utf-8").splitlines()[0] == HEAD
        assert [r["text"] for r in G.rows_of(d / "tuning_nf.tsv")] == ["T2"]                          # no funerary row for the second round
        assert (d / "tuning_texts.md").read_text(encoding="utf-8").startswith("## T1 (funerary, 2 words)\n\natolo ...\n")


def test_the_second_rounds_tests_see_no_funerary_row():
    """On the held-back texts the second round's functions are given only the words of texts that are not funerary,
    and its result says how many those are."""
    with a_home() as d, tempfile.TemporaryDirectory() as t:
        a_table(d / ".held/held.tsv", ["funerary", "graffito", "funerary", "royal or temple (stela, wall, cartouche, label)"])
        assert len(G.held_rows(1)) == 12 and [r["kind"] for r in G.held_rows(2)].count("funerary") == 0 and len(G.held_rows(2)) == 6
        for letter in "LM":
            (Path(t) / f"{letter}9.py").write_text(f"def test_{letter}9_1(rows):\n    return len(rows), sum(r['kind'] == 'funerary' for r in rows), 0.0\n",
                                                   encoding="utf-8")
        for folder, rid in (("rules", "L9-1"), ("rules2", "M9-1")):
            (d / folder).mkdir()
            (d / folder / "x.jsonl").write_text(json.dumps({"id": rid, "tuning": {"cases": 1, "holds": 1, "comparison_rate": 0.0}}) + "\n", encoding="utf-8")
        with set_to(G, TESTS=Path(t), frozen=lambda rnd: "abc1234 00:00:00"):
            assert sorted(G.tests(1)) == ["L9-1"] and sorted(G.tests(2)) == ["M9-1"]
            quiet(G.held, 1)
            quiet(G.held, 2)
        one, two = G.the_result(1), G.the_result(2)
    assert list(one) == ["tests_frozen_in", "bars", "rules"] and (one["rules"]["L9-1"]["cases"], one["rules"]["L9-1"]["holds"]) == (12, 6)
    assert list(two) == ["tests_frozen_in", "bars", "words", "rules"] and two["words"] == 6
    assert (two["rules"]["M9-1"]["cases"], two["rules"]["M9-1"]["holds"]) == (6, 0)                  # no funerary word reached the function
    assert G.ROUNDS[2]["table"] == "tuning_nf.tsv" and G.ROUNDS[1]["table"] == "tuning.tsv"


# ------------------------------------------------------------------------------------- the rules' tests, as frozen

def test_no_test_function_reads_a_file_or_names_a_text():
    """The frozen tests are pure counts on the rows they are given: only a few modules of the standard library, no
    file, no call that could reach one, no text of the corpus named. One function a rule of the figures."""
    allowed, banned = {"random", "re", "collections", "itertools", "math"}, {"open", "exec", "eval", "compile", "__import__", "input", "print"}
    outside = {"os", "sys", "pathlib", "subprocess", "io", "json", "csv", "glob", "shutil", "importlib", "urllib", "socket"}
    names, found = re.compile(r"\b(REM ?\d{3}|GA \d|AWE\.|AWK\.|QI\d|MI \d|Kar\. ?\d|Sh\. ?\d)"), {}
    for f in sorted(G.TESTS.glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        docs = {id(n.body[0].value) for n in ast.walk(tree) if isinstance(n, (ast.Module, ast.FunctionDef)) and n.body
                and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}       # a docstring is no data
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert {a.name.split(".")[0] for a in node.names} <= allowed, (f.name, [a.name for a in node.names])
            elif isinstance(node, ast.ImportFrom):
                assert (node.module or "").split(".")[0] in allowed, (f.name, node.module)
            elif isinstance(node, ast.Name):
                assert node.id not in banned | outside, (f.name, node.id)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs:
                assert not names.search(node.value) and ".tsv" not in node.value and "data/" not in node.value, (f.name, node.value[:60])
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                assert re.fullmatch(rf"test_{f.stem}_\d+", node.name) and [a.arg for a in node.args.args] == ["rows"], (f.name, node.name)
                found[node.name[5:].replace("_", "-", 1)] = f.stem
    assert sorted(f.stem for f in G.TESTS.glob("*.py")) == [f"L{k}" for k in range(1, 9)] + [f"M{k}" for k in range(1, 7)]
    f = figs()
    for rnd in ("1", "2"):
        ids = [x["id"] for x in f["rounds"][rnd]["the_rules"]]
        assert sorted(ids) == sorted(k for k in found if k[0] == G.ROUNDS[int(rnd)]["letter"]) == sorted(G.tests(int(rnd))), rnd
        assert all(found[i] == i.split("-")[0] for i in ids)


def test_the_tests_are_the_files_that_were_frozen():
    """Each round's test files are, byte for byte, those of the commit that froze them; that commit has the time the
    page gives and holds nothing but tests; no test file has been touched since."""
    for rnd, R in G.ROUNDS.items():
        fz, files = R["frozen"], sorted(G.TESTS.glob(f"{R['letter']}*.py"))
        assert len(files) == R["finders"] and G.frozen(rnd) == f"{fz['first']} {fz['at']}"
        assert git("log", "-1", "--format=%aI", fz["here"]) == f"2026-11-16T{fz['at']}-08:00"          # the author's time: when it was first committed
        assert set(git("show", "--format=", "--name-only", fz["here"]).split()) == {str(f.relative_to(ROOT)) for f in files}
        for f in files:
            assert git("log", "--format=%h", "--", str(f.relative_to(ROOT))).split() == [fz["here"]], f.name
        with set_to(fz, here=G.WHEN[rnd]["set_in"]):                                                   # a commit that does not hold the tests
            assert stops(lambda: G.frozen(rnd), "is not the file committed in")
    assert figs()["rounds"]["1"]["tests_frozen_in"] == "604c379 19:15:35" and figs()["rounds"]["2"]["tests_frozen_in"] == "6c974f3 19:30:39"


# ---------------------------------------------------------------------------------- what the agents were given

def test_what_the_finders_and_the_readers_were_given_is_public():
    first = (ROOT / "runs/prompts/GRAMMAR_finders.md").read_text(encoding="utf-8")
    block = textwrap.dedent(first[first.index("    # Find rules of Meroitic grammar"):]).replace("{{", "{").replace("}}", "}")
    assert block.replace("<the finder's angle>", "<<ANGLE>>").replace("<answers>", "data/sources/grammar/rules/L<<K>>.jsonl") \
        .replace('"id": "L3-2"', '"id": "L<<K>>-1"') == G.BRIEF
    second = (ROOT / "runs/prompts/GRAMMAR_round2.md").read_text(encoding="utf-8")
    ind = lambda s: textwrap.indent(s, "    ", lambda line: bool(line.strip()))                        # noqa: E731
    assert ind(G.BRIEF2) in second and ind(G.READERS_BRIEF) in second and all(f"{k}. {a}" in second for k, a in G.ANGLES2.items())
    assert len(G.ANGLES) == G.ROUNDS[1]["finders"] == 8 and len(G.ANGLES2) == G.ROUNDS[2]["finders"] == 6
    for rnd, angles in ((1, G.ANGLES), (2, G.ANGLES2)):
        for k, a in angles.items():
            b = G.brief_of(rnd, k)
            assert "<<ANGLE>>" not in b and "<<K>>" not in b and f"**Your angle: {a}.**" in b and f"{G.ROUNDS[rnd]['rules']}/{G.ROUNDS[rnd]['letter']}{k}.jsonl" in b
    two = G.brief_of(2, 4)
    assert "runs/grammar/M4.py" in two and "def test_M4_1(rows):" in two and "tuning_nf.tsv" in two and "No epitaph is among them." in two
    assert "**Not wanted:** the grammar of the epitaph" in two and "At most 6 rules" in two and "At most 8 rules" in G.BRIEF
    for b in (" ".join(G.BRIEF.split()), " ".join(G.BRIEF2.split())):
        assert "do not open any other file of the repository" in b and "at least 20 cases there" in b and "80%" in b and "30 points" in b
    assert "A quote is needed for \"stated\" and for \"partly\". What you know of Meroitic from elsewhere does not count." in G.READERS_BRIEF


# ---------------------------------------------------------------------------------------------------- the figures

def test_the_long_texts_and_the_kinds_are_counted_rule_by_rule():
    rows = [{"text": "A", "kind": "funerary", "level": "unknown" if n % 2 else "meaning"} for n in range(G.LONG)]
    rows += [{"text": "B", "kind": "graffito", "level": "kind"} for _ in range(G.LONG + 20)] + [{"text": "C", "kind": "graffito", "level": "lost"}] * 5
    fns = [lambda rs: (len(rs), len(rs) // 2, 0.0), lambda rs: (0, 0, 0.0), lambda rs: (sum(r["kind"] == "funerary" for r in rs),) * 2 + (0.0,)]
    out = G.long_texts(rows[:G.LONG], rows[G.LONG:], fns)
    assert out == [{"text": "B", "kind": "graffito", "set": "held back", "words": 120, "open_words": 120, "rules_with_a_case": 1, "cases": 120, "holds": 60},
                   {"text": "A", "kind": "funerary", "set": "tuning", "words": 100, "open_words": 50, "rules_with_a_case": 2, "cases": 200, "holds": 150}]
    by = G.cases_by_kind(rows, fns)
    assert by["cases"] == {"funerary": 200, "graffito": 125} and by["all"] == 325 and by["share"]["funerary"] == round(200 / 325, 4)
    s = G.set_of(rows)
    assert (s["texts"], s["words"], s["long_texts"], s["not_funerary"]) == (3, 225, 2, {"texts": 2, "words": 125})
    assert s["by_kind"] == {"funerary": {"texts": 1, "words": 100}, "graffito": {"texts": 2, "words": 125}}


def test_the_figures_add_up():
    f = figs()
    sp, both = f["split"], f["both"]
    assert sp["tuning"]["texts"] + sp["held"]["texts"] == 548 and sp["seed"] == G.SEED and sp["held_share"] == G.HELD and sp["layers"] == list(G.LAYERS)
    for s in (sp["tuning"], sp["held"]):
        assert s["texts"] == sum(k["texts"] for k in s["by_kind"].values()) and s["words"] == sum(k["words"] for k in s["by_kind"].values())
        assert s["not_funerary"]["words"] == s["words"] - s["by_kind"]["funerary"]["words"]
    assert 0.39 < sp["held"]["texts"] / 548 < 0.41 and sp["tuning"]["long_texts"] + sp["held"]["long_texts"] == len(f["long_texts"]) == 7
    assert f["bars"] == G.BARS and f["ours_needed"] == G.OURS_NEEDED == 3
    for rnd, r in f["rounds"].items():
        rows, R = r["the_rules"], G.ROUNDS[int(rnd)]
        assert r["rules"] == len(rows) == sum(r["by_finder"].values()) == r["tests_with_the_finders_counts"] and len(r["by_finder"]) == r["finders"] == R["finders"]
        assert all(set(x) == {"id", "finder", "statement", "tuning", "held", "verdict", "readers", "works", "ours"} for x in rows)
        for x in rows:                                                                     # each verdict is the bars' verdict on the counts given
            h = x["held"]
            assert x["verdict"] == G.verdict_of(h) and h["rate"] == round(h["holds"] / h["cases"], 4) and x["id"].startswith(x["finder"] + "-")
            assert (x["readers"] is None) == (x["verdict"] != "passed") and x["ours"] == (x["readers"] == ["not found", "not found"])
            assert x["verdict"] != "passed" or all(v in G.VERDICTS for v in x["readers"])
        ok = [x for x in rows if x["verdict"] == "passed"]
        assert r["passed"] == len(ok) == r["readers"]["rules"] == r["readers"]["answered_by_both"] == sum(r["readers"][k] for k in G.PAIRS.values())
        assert r["passed"] + sum(r["not_passed"].values()) == r["rules"] and r["ours"] == sorted(x["id"] for x in rows if x["ours"])
        assert r["readers"]["not found by both"] == len(r["ours"]) and all(not x["works"] for x in ok if x["ours"])
        assert r["works"] == {w: sum(w in x["works"] for x in ok) for w in r["works"]} and set(r["works"]) <= {name for _, name in G.WORKS}
        assert r["held_words"] == (sp["held"]["words"] if rnd == "1" else sp["held"]["not_funerary"]["words"])
    assert both["rules"] == sum(r["rules"] for r in f["rounds"].values()) and both["passed"] == sum(r["passed"] for r in f["rounds"].values())
    assert both["ours"] == sum(len(r["ours"]) for r in f["rounds"].values()) and both["stated_or_partly_stated"] == both["passed"] - both["ours"]
    assert both["bar_met"] == (both["ours"] >= f["ours_needed"]) and both["bar_met"] is False
    assert both["partly_stated_by_both"] == sum(r["readers"]["partly stated by both"] for r in f["rounds"].values())
    longs = f["long_texts"]
    assert [t["words"] for t in longs] == sorted((t["words"] for t in longs), reverse=True) and all(t["words"] >= G.LONG for t in longs)
    assert all(t["holds"] <= t["cases"] and t["rules_with_a_case"] <= f["rounds"]["1"]["passed"] and t["open_words"] <= t["words"] for t in longs)
    assert sum(t["set"] == "held back" for t in longs) == sp["held"]["long_texts"]
    l2 = f["long_texts_round_2"]                                                   # the second round's rules in the same texts
    assert [(t["text"], t["words"], t["open_words"], t["set"]) for t in l2] == [(t["text"], t["words"], t["open_words"], t["set"]) for t in longs]
    assert all(t["holds"] <= t["cases"] and t["rules_with_a_case"] <= f["rounds"]["2"]["passed"] for t in l2)
    for rnd, r in f["rounds"].items():
        assert r["tests_frozen_in_this_history"] == G.ROUNDS[int(rnd)]["frozen"]["here"] and r["tests_frozen_in"].split()[0] == G.ROUNDS[int(rnd)]["frozen"]["first"]
    by = f["cases_by_kind"]
    assert by["all"] == sum(by["cases"].values()) and all(by["share"][k] == round(v / by["all"], 4) for k, v in by["cases"].items())
    cost = f["cost"]
    assert cost["all"] == {"agents": sum(v["agents"] for k, v in cost.items() if k != "all"), "tokens": sum(v["tokens"] for k, v in cost.items() if k != "all")}
    assert [cost[f"round {rnd}, the finders"]["agents"] for rnd in (1, 2)] == [8, 6] and [cost[f"round {rnd}, the readers"]["agents"] for rnd in (1, 2)] == [4, 2]
    assert f["when"] == {"split_drawn": G.WHEN["split_drawn"], "1": G.WHEN[1], "2": G.WHEN[2]}


def test_the_figures_hold_no_wording_of_a_source():
    """No string of the figures follows the lexicon of 2003, Rilly 2016 or 2021, Millet 2005 or Lipinski 2011 for
    four words in a row; no reader's quote or note is in them; a reworded statement is one the finder's wording
    needed."""
    def strings(o):
        if isinstance(o, str):
            yield o
        elif isinstance(o, dict):
            for k, v in o.items():
                yield k
                yield from strings(v)
        elif isinstance(o, list):
            for v in o:
                yield from strings(v)
    f = figs()
    every = set(strings(f))
    assert not any(k in every for k in ("quote", "note", "file", "cases_wording", "why_grammar", "known", "comparison"))
    ids = {x["id"]: x["statement"] for r in f["rounds"].values() for x in r["the_rules"]}
    assert set(G.STATEMENTS) <= set(ids) and all(ids[k] == v for k, v in G.STATEMENTS.items())
    needs("data/rilly2003", "data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt", "data/sources/jssea-text/pages.txt",
          "data/sources/lipinski2011-text/pages.txt", "data/sources/grammar/rules")
    import lexicon as X
    import lexique as Q

    def runs(text):
        w = X.words_of(re.sub(r"ffi|ffl|ff|fi|fl|\x00", "ꜰ", text.lower()))
        return {tuple(w[i: i + X.COPIED]) for i in range(len(w) - X.COPIED + 1)}
    grams = set()
    for e in Q.load():
        for t in [v for v in e.values() if isinstance(v, str)] + [p.get("proposal") or "" for p in e.get("proposals") or []]:
            grams |= runs(t)
    for path in ("data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt", "data/sources/jssea-text/pages.txt",
                 "data/sources/lipinski2011-text/pages.txt"):
        text = re.sub(r"(?m)^\f?=== page \d+ ===$", " ", (ROOT / path).read_text(encoding="utf-8", errors="replace"))
        grams |= runs(text) | runs(re.sub(r"(?<=[^\W\d_])-[ \t]*\n\s*(?=[^\W\d_])", "", text))
    assert sorted(s for s in every if runs(s) & grams) == []
    # the finders' own wording of the reworded statements does share such a run: none is reworded without need
    mine = {**G.rules(1), **G.rules(2)}
    assert all(runs(mine[k]["statement"]) & grams for k in G.STATEMENTS) and all(mine[k]["statement"] != v for k, v in G.STATEMENTS.items())
    assert all(ids[k] == r["statement"] for k, r in mine.items() if k not in G.STATEMENTS)


def test_the_page_says_what_the_figures_say():
    f, text, raw = figs(), page(), PAGE.read_text(encoding="utf-8")
    sp, both, one, two, w = f["split"], f["both"], f["rounds"]["1"], f["rounds"]["2"], f["when"]
    rule = {x["id"]: x for r in f["rounds"].values() for x in r["the_rules"]}
    of = lambda rid: f"{rule[rid]['held']['holds']} of {rule[rid]['held']['cases']}"                    # noqa: E731
    pct = lambda x: f"{100 * x:.1f}%"                                                                   # noqa: E731
    t, h = sp["tuning"], sp["held"]
    nf = t["not_funerary"]["words"] + h["not_funerary"]["words"]
    rem1003 = next(x for x in f["long_texts"] if x["text"] == "REM 1003")
    phrases = [
        # the status and the verdict
        f"Over two rounds {both['rules']} rules were proposed, {both['passed']} passed on held-back texts, and {both['ours']} is a finding of ours "
        f"where {f['ours_needed']} were needed",
        "`src/grammar.py` (checks: `tests/test_grammar.py`)", "[`grammar_pilot_figures.json`](grammar_pilot_figures.json)",
        f"first committed at {G.ROUNDS[1]['frozen']['at']} and {G.ROUNDS[2]['frozen']['at']} on a branch of their own, `grammar`, as "
        f"{G.ROUNDS[1]['frozen']['first']} and {G.ROUNDS[2]['frozen']['first']}; in this history they are {G.ROUNDS[1]['frozen']['here']} and "
        f"{G.ROUNDS[2]['frozen']['here']}, copies of the same files made at {git('log', '-1', '--format=%cd', '--date=format:%H:%M', G.ROUNDS[2]['frozen']['here'])} "
        "that keep the first commits' author times",
        f"| Proposed | {both['rules']} |", f"| Passed on held-back texts | {both['passed']} |",
        f"| Stated or partly stated in a source in hand | {both['stated_or_partly_stated']} |", f"| A finding of ours | {both['ours']} |",
        f"**The bar set beforehand was {f['ours_needed']}. It is not met, and the pilot ends here,**",
        f"{both['passed']} rules that hold out of sample", f"{both['partly_stated_by_both']} points where the count is sharper",
        f"(the {one['readers']['partly stated by both']} of section 8 and {two['readers']['partly stated by both']} of this round)",
        f"Cost of the pilot: {f['cost']['all']['agents']} agents, {f['cost']['all']['tokens']:,} tokens.",
        f"there are about {round(nf, -3):,} words",
        # the split
        f"The {t['texts'] + h['texts']} texts were dealt by lot (seed {sp['seed']}) into two sets, {round(100 * sp['held_share'])}% held back within each kind of text",
        f"long texts ({sp['long_from_words']} words or more) apart from short ones",
        f"| Tuning: the rule finders see these | {t['texts']} | {t['words']:,} | {t['long_texts']} |",
        f"| Held back: only the frozen tests see these | {h['texts']} | {h['words']:,} | {h['long_texts']} |",
        "The words are those of the map with its six reviewed layers",
        # the bars
        f"at least {f['bars']['cases']} cases, holds in at least {round(100 * f['bars']['rate'])}% of them, and stands at least "
        f"{round(100 * f['bars']['margin'])} points above its comparison rate on those texts",
        f"grammar first is worth going on with if at least {f['ours_needed']} rules are findings of ours",
        # the first round
        f"({w['1']['set']}), and proposed {one['rules']} rules", f"all {one['tests_with_the_finders_counts']} give the finder's own counts",
        f"The tests were committed at {w['1']['tests_frozen']}, the table of the held-back texts was written after that ({w['1']['held_table_written']})",
        f"| Passed (at least 20 cases, 80% holding, 30 points above the comparison) | {one['passed']} |",
        f"| Fewer than 20 cases | {one['not_passed']['fewer than 20 cases']} |", f"| Holding in under 80% | {one['not_passed']['holds in under 80%']} |",
        f"| Under 30 points above the comparison | {one['not_passed']['under 30 points above its comparison']} |",
        f"searched the sources in hand for each of the {one['passed']} rules between {w['1']['readers_started']} and {w['1']['last_answer'][:5]}",
        f"| Stated by a source | {one['readers']['stated by both']} |",
        f"| Stated by one reader's source, partly by the other's | {one['readers']['stated by one, partly by the other']} |",
        f"| Partly stated | {one['readers']['partly stated by both']} |", f"| Not found | {one['readers']['not found by both']} |",
        f"**No rule is a finding of ours.** The pilot's bar of {f['ours_needed']} is not met by this round.",
        f"**What the {one['passed']} rules are.** They describe the epitaph: {round(100 * f['cases_by_kind']['share']['funerary'])}% of their cases stand in funerary texts.",
        f"(Griffith's Karanòg and Rilly 2021, {one['works']['Rilly 2021']} rules each)",
        f"({of('L2-3')} held-back cases)", f"not `ps-` ({of('L2-4')})", f"often does not ({of('L2-5')})", f"only after l, q or t ({of('L8-4')})",
        f"the glide is y ({of('L8-2')})",
        f"Cost: {f['cost']['round 1, the finders']['agents']} finders, {f['cost']['round 1, the finders']['tokens']:,} tokens; "
        f"{f['cost']['round 1, the readers']['agents']} readers, {f['cost']['round 1, the readers']['tokens']:,} tokens",
        # the second round
        f"{t['not_funerary']['words']:,} words of the tuning set for the finders, {h['not_funerary']['words']:,} words of the held-back set for the tests",
        f"after the commit that set the round ({w['2']['set']}), and proposed {two['rules']} rules",
        f"All {two['tests_with_the_finders_counts']} tests give their finder's counts on the tuning texts. They were committed at {w['2']['tests_frozen']} "
        f"and then run once on the {two['held_words']:,} held-back words that are not funerary.",
        f"| Passed | {two['passed']} |",
        f"| Holding in under 80% ({WORDS[two['not_passed_also_under_the_margin']]} of them also under the margin) | {two['not_passed']['holds in under 80%']} |",
        f"searched the sources in hand for each of the {two['passed']} between {w['2']['readers_started']} and {w['2']['last_answer'][:5]}",
        f"| Stated by a source | {two['readers']['stated by both']} |",
        f"| Stated by one reader's source, partly by the other's | {two['readers']['stated by one, partly by the other']} |",
        f"| Partly stated | {two['readers']['partly stated by both']} |", f"| Not found | {two['readers']['not found by both']} |",
        f"({of('M2-3')} held-back cases, {pct(rule['M2-3']['held']['rate'])}, against {pct(rule['M2-3']['held']['comparison_rate'])})",
        f"Cost: {f['cost']['round 2, the finders']['agents']} finders, {f['cost']['round 2, the finders']['tokens']:,} tokens; "
        f"{f['cost']['round 2, the readers']['agents']} readers, {f['cost']['round 2, the readers']['tokens']:,} tokens",
    ]
    for p in phrases:
        assert p in text, p
    assert two["ours"] == ["M2-3"] and one["ours"] == [] and set(two["not_passed"]) == {"holds in under 80%"}
    assert f"finders were started at {w['1']['finders_started'][:5]}, after the commit with the bars" in text
    assert f"The six finders were started at {w['2']['finders_started']}" in text and round(nf / rem1003["words"]) == 8 and "one in eight of them in one stela" in text
    # the long texts, a row each, in the figures' order
    rows = [l for l in raw.splitlines() if l.startswith("| REM ")]
    assert [l.split(" | ")[0][2:] for l in rows] == [x["text"] for x in f["long_texts"]]
    for l, x in zip(rows, f["long_texts"]):
        assert l.endswith(f" | {x['words']} | {x['open_words']} | {x['rules_with_a_case']} | {x['cases']} | {x['holds']} |"), l
    three = f["long_texts"][:3]
    assert 0.55 < sum(x["holds"] for x in three) / sum(x["cases"] for x in three) < 0.65 and "they hold in about six cases of ten" in text
    assert round(h["not_funerary"]["words"] / f["bars"]["cases"], -1) == 90 and "comes about once in 90 words to reach 20 cases" in text
    # the last part of the request, the parse of the long texts, is said plainly to be not done: only the rules' reach is counted
    assert "| R3 | \"Then parse the long royal texts with them.\" | **Not done as section 6 set it.**" in text
    assert "| R4 | \"A two-day pilot.\" | Ended on 2026-11-16, its first evening, by the verdict set beforehand (section 11). |" in text
    assert "This counts each rule's reach; it is not the parse that section 6 set out." in text and "No word without a meaning gets a kind" not in text
    l2 = f["long_texts_round_2"]
    hold = [x["holds"] / x["cases"] for x in l2]
    assert (f"the {two['passed']} rules that passed have cases in each of them ({min(x['rules_with_a_case'] for x in l2)} to "
            f"{max(x['rules_with_a_case'] for x in l2)} of the {two['passed']} rules a text), and their cases hold there {round(100 * min(hold))}% to "
            f"{round(100 * max(hold))}% of the time") in text and all(x["cases"] for x in l2)


def test_the_summaries_name_the_pilot():
    f = figs()
    both, m_ = f["both"], json.loads(M.PUBLIC.read_text(encoding="utf-8"))
    says = (f"Over two rounds {both['rules']} rules were proposed, {both['passed']} passed on held-back texts and {both['ours']} is a finding of ours, "
            f"where the bar set beforehand was {f['ours_needed']}")
    for name in ("README.md", "NEXT_STEPS.md", "REPORT.md"):
        text = " ".join((ROOT / name).read_text(encoding="utf-8").split())
        assert "grammar_pilot.md" in text and says in text, name
        assert f"{f['cost']['all']['agents']} agents" in text or name != "REPORT.md", name
        assert "Its last part, parsing the long royal texts with the rules, was not done" in text, name   # the cut said where the step is told
    readme, report = (ROOT / "README.md").read_text(encoding="utf-8"), " ".join((ROOT / "REPORT.md").read_text(encoding="utf-8").split())
    assert "python3 -I tests/test_grammar.py" in readme and "- `python3 -I src/grammar.py public`" in readme and "(`src/grammar.py`)" in readme
    assert '"how can we make more structural strategic moves. I am a bit pissed we\'ve been working on "assembling some data" for the last week"' in report
    assert '"Yes, start it"' in report and f"{f['cost']['all']['agents']} agents, {f['cost']['all']['tokens']:,} subagent tokens" in report
    index = (ROOT / "data/INDEX.md").read_text(encoding="utf-8")
    assert "`data/sources/grammar/`" in index and "grammar_pilot" in index
    assert len(m_["layers"]) == 7                                              # the pilot lays nothing: the map stays as it was


# ------------------------------------------------------------------------------------------- with the local files

LOCAL = ("data/sources/grammar/split.json", "data/sources/grammar/tuning.tsv", "data/sources/grammar/.held/held.tsv",
         "data/sources/grammar/result.json", "data/sources/grammar/result2.json", "data/sources/grammar/novelty/result.json",
         "data/sources/grammar/novelty2/result.json", "data/sources/grammar/rules", "data/sources/grammar/rules2")
THE_MAP = ("data/sources/v6/analysts/glosses.jsonl", "data/corpus_v6.jsonl", "data/sources/recurring/overlay.jsonl", "data/sources/rare/g2/overlay.jsonl",
           "data/sources/rare/g4/overlay.jsonl", "data/sources/g3/overlay.jsonl", "data/sources/rare/g4m/overlay.jsonl", "data/sources/g8b/overlay.jsonl")


def test_the_figures_are_the_count_of_the_local_files():
    needs(*LOCAL, "data/sources/grammar/tokens.json", "data/sources/grammar/tokens2.json")
    assert G.figures() == figs()


def test_the_second_rounds_tables_hold_no_epitaph():
    needs(*LOCAL, "data/sources/grammar/tuning_nf.tsv")
    f = figs()["split"]
    held, tuning = G.held_rows(2), G.rows_of(G.HOME / "tuning_nf.tsv")
    assert all(r["kind"] != "funerary" for r in held + tuning)
    assert (len(held), len(tuning)) == (f["held"]["not_funerary"]["words"], f["tuning"]["not_funerary"]["words"])
    sp = G.the_split()
    assert {r["text"] for r in G.rows_of(G.HOME / "tuning.tsv")} == set(sp["tuning"]) and {r["text"] for r in G.held_rows(1)} == set(sp["held"])
    assert not set(sp["tuning"]) & set(sp["held"])
    # no test names a text of the corpus
    names = {t for t in sp["tuning"] + sp["held"] if len(t) >= 4}
    for path in sorted(G.TESTS.glob("*.py")):
        consts = {n.value for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        assert not consts & names, (path.name, sorted(consts & names)[:3])


def test_the_script_writes_everything_again():
    """The pilot again in a folder of its own, with the finders' rules and the readers' answers copied in at their
    turn: the split, the tables, the briefs, the held-back table, both results, the readers' packs and their count
    come out byte for byte; each test gives its finder's counts on the tuning texts."""
    needs(*LOCAL, *THE_MAP, "data/rilly2003", "data/sources/grammar/briefs", "data/sources/grammar/briefs2", "data/sources/grammar/novelty/packs",
          "data/sources/grammar/novelty2/packs")
    live = G.HOME

    def differ(d, *names):
        return [n for n in names if (d / n).read_bytes() != (live / n).read_bytes()]
    with a_home() as d:
        quiet(G.split)
        quiet(G.dump)
        quiet(G.briefs, 1)
        quiet(G.briefs, 2)
        assert differ(d, "split.json", "tuning.tsv", "tuning_nf.tsv", "tuning_texts.md", *[f"briefs/L{k}.md" for k in range(1, 9)],
                      *[f"briefs2/M{k}.md" for k in range(1, 7)]) == []
        assert not (d / ".held").exists()                                       # nothing of the held-back texts yet
        for folder in ("rules", "rules2"):
            shutil.copytree(live / folder, d / folder)
        assert quiet(G.tuning, 1) == len(G.rules(1)) == 54 and quiet(G.tuning, 2) == len(G.rules(2)) == 19
        quiet(G.held_dump)
        quiet(G.held, 1)
        quiet(G.held, 2)
        assert differ(d, ".held/held.tsv", "result.json", "result2.json") == []
        quiet(G.packs, 1)
        quiet(G.packs, 2)
        assert differ(d, "novelty/groups.json", "novelty2/groups.json", *[f"novelty/packs/N{n}_r{c}.md" for n in (1, 2) for c in (1, 2)],
                      *[f"novelty2/packs/P1_r{c}.md" for c in (1, 2)]) == []
        for folder in ("novelty", "novelty2"):
            for c in (1, 2):
                shutil.copytree(live / folder / f"answers{c}", d / folder / f"answers{c}", dirs_exist_ok=True)
        quiet(G.count, 1)
        quiet(G.count, 2)
        assert differ(d, "novelty/result.json", "novelty2/result.json") == []
    assert stops(G.split, "the split is drawn: not drawn again") and stops(lambda: G.packs(1), "answers exist: the packs are not written again")


def test_the_rules_were_in_git_before_the_finders_and_the_tests_before_the_held_back_texts():
    """Each round's commit is git's, at its time, and holds the bars the page names; the finders were started after
    it, the tests were frozen after the last rule and before the held-back texts were read, the readers came last."""
    w = G.WHEN
    for rnd in (1, 2):
        x = w[rnd]
        assert git("log", "-1", "--format=%cI", x["set_in"]) == f"2026-11-16T{x['set']}-08:00", rnd
        assert x["set"] < x["finders_started"] < x["first_rules"] <= x["last_rules"] < x["tests_frozen"] <= x["tested"] < x["readers_started"] \
            < x["first_answer"] <= x["last_answer"], rnd
        assert x["tests_frozen"] == G.ROUNDS[rnd]["frozen"]["at"]
    assert w["split_drawn"] < w[1]["set"] and w[1]["tests_frozen"] < w[1]["held_table_written"] <= w[1]["tested"] and w[1]["last_answer"] < w[2]["set"]
    raw = PAGE.read_text(encoding="utf-8")
    for phrase, rnd in (("## 5. The bars, set before any finder is started", 1),
                        ("2. **On the held-back texts** a rule passes when it has at least 20 cases, holds in at least 80% of them, and", 1),
                        ("5. **The pilot's verdict, set now:** grammar first is worth going on with if at least 3 rules are findings of", 1),
                        ("1. **A frozen test.** Each rule's test is a function over the map's columns, written from the rule's wording and", 1),
                        ("## 9. A second round, outside the epitaphs (set before its finders are started)", 2),
                        ("- **Not wanted:** a rule about the invocation, the naming, the filiation or the offering formulas of an epitaph.", 2),
                        ("  is worth going on with if, over both rounds, at least 3 rules are findings of ours.", 2)):
        out = git("log", "--reverse", "--format=%cI", f"-S{phrase}", "--", str(PAGE.relative_to(ROOT))).split()
        assert out and out[0][11:19] <= w[rnd]["set"], phrase
        assert phrase in raw, phrase


def test_the_times_are_the_local_files():
    """The split, the rules and the readers' answers have the times the script records (Pacific time); the held-back
    table was written after the first round's tests were frozen."""
    needs(*LOCAL, "data/sources/grammar/novelty/answers1", "data/sources/grammar/novelty2/answers1")
    import datetime
    import zoneinfo
    pacific = zoneinfo.ZoneInfo("America/Los_Angeles")
    at = lambda f: datetime.datetime.fromtimestamp(f.stat().st_mtime, pacific).strftime("%H:%M:%S")       # noqa: E731
    w = G.WHEN
    assert at(G.HOME / "split.json") == w["split_drawn"] and at(G.HOME / ".held/held.tsv") >= w[1]["held_table_written"] > w[1]["tests_frozen"]
    for rnd, R in G.ROUNDS.items():
        rules = sorted(at(f) for f in (G.HOME / R["rules"]).glob("*.jsonl"))
        assert len(rules) == R["finders"] and (rules[0], rules[-1]) == (w[rnd]["first_rules"], w[rnd]["last_rules"]), (rnd, rules[0], rules[-1])
        answers = sorted(at(f) for f in (G.HOME / R["novelty"]).glob("answers*/*.jsonl"))
        assert len(answers) == 2 * R["packs"] and (answers[0], answers[-1]) == (w[rnd]["first_answer"], w[rnd]["last_answer"]), (rnd, answers[0], answers[-1])


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
