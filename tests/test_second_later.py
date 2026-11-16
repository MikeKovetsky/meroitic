"""Checks for the second scholar of Rilly's later meanings (src/second_later.py, data/discovery/second_scholar_later.md).

  python3 -I tests/test_second_later.py

The sources and the judges' answers are local only: the checks of the method run on made-up rows; the checks of
the reported numbers read the public figures file, compare the page with it, and compare it with a count from the
local files where those are present.
"""
import filecmp
import io
import contextlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import second_later as S             # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/second_scholar_later.md"


def figs():
    return json.loads(S.PUBLIC.read_text(encoding="utf-8"))


def page():
    return " ".join(PAGE.read_text(encoding="utf-8").split())


def stops(fn, part):
    try:
        fn()
    except SystemExit as e:
        assert part in str(e), e
        return True
    raise AssertionError("did not stop")


def in_a_folder(fn):
    """Run fn with the module's folder set to an empty one."""
    home = S.HOME
    with tempfile.TemporaryDirectory() as d:
        S.HOME = Path(d)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                return fn(Path(d))
        finally:
            S.HOME = home


def made_up(n=20):
    return {f"w{i}": {"entry": f"w{i}", "meaning": f"meaning {i}", "source": "Rilly 2021", "page": i, "runs": ["g4"],
                      "others": [{"scholar": "Griffith", "how": "own work", "page": 1, "quote": f"quote {i} {j}", "says": f"says {i}"} for j in range(i % 3)]}
            for i in range(n)}


# ------------------------------------------------------------------------------------------------- the method

def test_a_meaning_is_agreed_disputed_or_stated_by_one():
    st = S.status
    assert st([("same", "same"), ("other", "partly")]) == "agreed by two scholars"
    assert st([("same", "same"), ("other", "other")]) == "agreed by two scholars, with a dissent"
    assert st([("other", "other"), ("same", "partly")]) == "disputed"           # no row both call the same
    assert st([("same", "partly"), ("partly", "partly"), ("no meaning", "no meaning"), ("other", "same")]) == "stated by one"
    assert st([]) == "stated by one"                                             # no other scholar speaks of it


def test_the_rows_pair_every_statement_and_a_tenth_more_as_decoys():
    def go(d):
        entries = S.entries
        S.entries = lambda: made_up()
        try:
            S.rows()
            first = S.read(S.HOME / "rows.json")
            S.rows()
            return first, S.read(S.HOME / "rows.json")
        finally:
            S.entries = entries
    table, again = in_a_folder(go)
    real, decoys = [r for r in table if not r["decoy"]], [r for r in table if r["decoy"]]
    assert table == again                                                        # drawn by a fixed seed
    assert len(real) == sum(i % 3 for i in range(20)) == 19 and len(decoys) == round(S.DECOYS * len(real)) == 2
    assert [r["row"] for r in table] == [f"R{i:04d}" for i in range(1, 22)]
    for r in decoys:                                                             # a decoy is a statement about another entry
        assert r["from"] != r["entry"] and r["quote"].startswith(f"quote {r['from'][1:]} ") and r["meaning"] == f"meaning {r['entry'][1:]}"
    for r in real:
        assert r["quote"].startswith(f"quote {r['entry'][1:]} ")
    assert S.OWN == ("Rilly 2003", "Rilly 2016", "Rilly 2021", "Project") and "mentions" not in S.SAYS


def test_the_packs_and_the_count_and_its_bars():
    def go(d):
        entries = S.entries
        S.entries = lambda: made_up()
        try:
            S.rows()
            S.packs()
            table = S.read(S.HOME / "rows.json")
            pack = (S.HOME / "packs" / "J01_j2.md").read_text(encoding="utf-8")
            assert "data/sources/g5/answers2/J01.jsonl" in pack and "This pack has 21 rows" in pack and pack.count("- **R00") == 21
            truth = {r["row"]: ("other" if r["decoy"] else "same" if int(r["entry"][1:]) % 2 else "other") for r in table}
            for j in (1, 2):
                lines = [json.dumps({"row": k, "verdict": v}) for k, v in truth.items()] + [json.dumps({"row": "R9999", "verdict": "same"}), "not json"]
                (S.HOME / f"answers{j}" / "J01.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
            assert stops(S.rows, "answers exist") and stops(S.packs, "answers exist")
            S.count()
            good = S.read(S.HOME / "result.json")
            # the second judge calls every decoy the same, and leaves one row out
            lines = [json.dumps({"row": k, "verdict": "same" if next(r for r in table if r["row"] == k)["decoy"] else v}) for k, v in truth.items()][1:]
            (S.HOME / "answers2" / "J01.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
            S.count()
            return good, S.read(S.HOME / "result.json")
        finally:
            S.entries = entries
    good, bad = in_a_folder(go)
    assert good["taken"] and good["kappa_same_or_not"] == 1.0 and good["answered_by_both"] == good["rows"] == 19 and all(good["bars"].values())
    assert good["decoys"] == {"1": {"shown": 2, "called_same": 0, "called_partly": 0}, "2": {"shown": 2, "called_same": 0, "called_partly": 0}}
    assert good["without_the_proposals_of_no_named_scholar"] == {}                # every made-up statement names its scholar
    odd = sum(i % 3 > 0 for i in range(1, 20, 2))                                # the odd entries with a statement are agreed
    assert good["statuses"]["agreed by two scholars"] == odd and good["with_no_other_scholar"] == sum(i % 3 == 0 for i in range(20))
    assert good["statuses"]["stated by one"] == good["with_no_other_scholar"] and good["statuses"]["disputed"] == 20 - odd - good["with_no_other_scholar"]
    assert not bad["taken"] and bad["bars"] == {"every_row_answered_by_both": False, "kappa_same_or_not": True, "decoys_called_same": False}
    assert bad["decoys"]["2"]["called_same"] == 2 and S.BARS == {"kappa_same_or_not": 0.6, "decoys_called_same": 0.10}


def test_a_judges_file_counts_only_for_its_own_pack_and_a_status_without_a_named_scholar_is_reported():
    def go(d):
        rows = [{"row": "R0001", "entry": "a", "scholar": "Griffith", "decoy": False}, {"row": "R0002", "entry": "b", "scholar": "Hintze", "decoy": False},
                {"row": "R0003", "entry": "b", "scholar": "unattributed ('earlier view')", "decoy": False},
                {"row": "R0004", "entry": "a", "scholar": "Millet", "decoy": True}]
        S.write("rows.json", rows)
        S.write("entries.json", {"a": {"others": [1]}, "b": {"others": [1, 2]}})
        S.write("groups.json", [["R0001", "R0002"], ["R0003", "R0004"]])
        for j in (1, 2):
            (d / f"answers{j}").mkdir()
            (d / f"answers{j}" / "J01.jsonl").write_text("\n".join(json.dumps(x) for x in (
                {"row": "R0001", "verdict": "same"}, {"row": "R0001", "verdict": "other"},     # the first line wins
                {"row": "R0003", "verdict": "same"},                                           # a row of the other pack
                {"row": "R0002", "verdict": "partly"})) + "\n", encoding="utf-8")
            (d / f"answers{j}" / "J02.jsonl").write_text("\n".join(json.dumps(x) for x in (
                {"row": "R0003", "verdict": "other"}, {"row": "R0004", "verdict": "partly" if j == 1 else "no meaning"})) + "\n", encoding="utf-8")
        assert S.answers(1) == {"R0001": "same", "R0002": "partly", "R0003": "other", "R0004": "partly"}
        S.count()
        return S.read(d / "result.json")
    r = in_a_folder(go)
    assert r["by_entry"] == {"a": "agreed by two scholars", "b": "disputed"}
    # b is disputed only through the proposal without a scholar's name: reported, and counted as the rule has it
    assert r["without_the_proposals_of_no_named_scholar"] == {"b": "stated by one"}
    assert r["decoys"] == {"1": {"shown": 1, "called_same": 0, "called_partly": 1}, "2": {"shown": 1, "called_same": 0, "called_partly": 0}}


def test_what_the_judges_were_given_is_public():
    prompts = (ROOT / "runs/prompts/G5_judges.md").read_text(encoding="utf-8")
    assert "\n".join(("    " + l).rstrip() for l in S.BRIEF.strip("\n").splitlines()) in prompts
    assert "do not look anything up and open no other file" in S.BRIEF and "Some\nrows are wrong on purpose" in S.BRIEF


# ------------------------------------------------------------------------------------ the figures and the pages

def test_the_figures_add_up():
    f = figs()
    assert f["taken"] and all(f["bars"].values()) and f["answered_by_both"] == f["rows"] == sum(f["pairs"].values()) == sum(f["rows_by"].values())
    assert f["kappa_same_or_not"] >= S.BARS["kappa_same_or_not"] and all(d["called_same"] <= S.BARS["decoys_called_same"] * d["shown"] for d in f["decoys"].values())
    assert f["decoys"]["1"]["shown"] == round(S.DECOYS * f["rows"])
    assert sum(f["statuses"].values()) == len(f["by_entry"]) == f["entries"] and set(f["statuses"]) <= {
        "agreed by two scholars", "agreed by two scholars, with a dissent", "disputed", "stated by one"}
    for status, n in f["statuses"].items():
        assert sum(v == status for v in f["by_entry"].values()) == n, status
    assert f["with_no_other_scholar"] <= f["statuses"]["stated by one"] and f["cost"]["agents"] == 10
    rare = json.loads(S.RARE.read_text(encoding="utf-8"))["g4"]["words"]
    assert sum(f["words_given_a_meaning_by_g4"].values()) == len(rare) and all(w["entry"] in f["by_entry"] for w in rare)


def test_the_figures_hold_no_wording_of_a_source():
    def strings(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from strings(v, k)
        elif isinstance(o, str):
            yield key, o
    f = figs()
    for key, v in strings(f):
        assert key in f["by_entry"] and v in f["statuses"], (key, v)            # an entry's headword and its status, nothing else


def test_the_page_says_what_the_figures_say():
    f, text = figs(), page()
    st, d = f["statuses"], f["decoys"]
    agreed = st["agreed by two scholars"] + st["agreed by two scholars, with a dissent"]
    assert f"{f['cost']['agents']} judges answered all {f['rows'] + d['1']['shown']} rows" in text and f"Cohen's kappa is {f['kappa_same_or_not']:.2f} (bar 0.6)" in text
    assert f"called {d['1']['called_same']} of the {d['1']['shown']} decoys \"same\"" in text and d["1"]["called_same"] == d["2"]["called_same"]
    for label, key in (("Agreed by two scholars", "agreed by two scholars"), ("Agreed by two scholars, with a dissent", "agreed by two scholars, with a dissent"),
                       ("Disputed", "disputed"), ("Stated by one", "stated by one")):
        assert f"| {label} | {st[key]} |" in text, key
    assert f"{agreed} of the {f['entries']} meanings are also stated by another scholar" in text and f"{f['with_no_other_scholar']} of them because no other scholar" in text
    assert f"the {f['entries']} entries of the lexicon for which two readers found a meaning stated by Rilly" in text
    assert f"{f['rows']} statements about these entries by someone other than Rilly. {f['rows_by']['own work']} are from" in text
    assert f"{f['rows_by']['reported by the lexicon of 2003']} are proposals that the lexicon of 2003 reports" in text
    w = f["words_given_a_meaning_by_g4"]
    assert (f"Of the {sum(w.values())} words of the dictionary that step G4 laid with a meaning, "
            f"{w.get('agreed by two scholars', 0) + w.get('agreed by two scholars, with a dissent', 0)} are agreed by two scholars, {w.get('disputed', 0)} disputed and "
            f"{w.get('stated by one', 0)} stated by one") in text
    for status, label in (("agreed by two scholars", "Agreed by two scholars:"), ("agreed by two scholars, with a dissent", "Agreed, with a dissent:"),
                          ("disputed", "Disputed:"), ("stated by one", "Stated by one:")):
        names = ", ".join(f"`{k}`" for k in sorted(k for k, v in f["by_entry"].items() if v == status))
        assert f"**{label}** {names}." in text, status
    assert f"Cost: {f['cost']['tokens']:,} subagent tokens" in text
    # F2's bar on the decoys counted "partly" with "same"
    assert d["1"]["called_partly"] == d["2"]["called_partly"] == 0 and 'is met too: neither judge called a decoy "partly"' in text
    for k, v in f["without_the_proposals_of_no_named_scholar"].items():
        assert f"`{k}` is {f['by_entry'][k]} only through it, and would be {v} without it" in text, k
    assert len(f["without_the_proposals_of_no_named_scholar"]) == 1 and "**One status rests on a proposal the lexicon gives without a scholar's name,**" in text
    rep = f["reported_by_the_lexicon_most_often"]
    assert rep["Priese"] == rep["Zyhlarz"] and (f"Griffith ({rep['Griffith']} rows), Hintze ({rep['Hintze']}), Millet ({rep['Millet']}), "
                                                f"Hofmann ({rep['Hofmann']}), Priese and Zyhlarz ({rep['Priese']} each)") in text
    assert "MET: sections 2, 3 and 5." in text and "the judges saw each statement's scholar, where F2's did not" in text


def test_the_summaries_name_the_step():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python3 -I tests/test_second_later.py" in readme and "- `python3 -I src/second_later.py public` (and " in readme
    f = figs()
    st = f["statuses"]
    agreed = st["agreed by two scholars"] + st["agreed by two scholars, with a dissent"]
    for text in (" ".join(readme.split()), " ".join((ROOT / "NEXT_STEPS.md").read_text(encoding="utf-8").split())):
        assert "second_scholar_later.md" in text and f"{agreed} of the {f['entries']}" in text and f"{st['disputed']} are disputed" in text


# ------------------------------------------------------------------------------------------- with the local files

def test_the_figures_are_the_count_of_the_local_files():
    needs("data/sources/g5/result.json", "data/sources/g5/rows.json", "data/sources/g5/tokens.json")
    assert S.figures() == figs()


def test_the_script_writes_the_rows_and_packs_the_judges_were_given():
    """The rows and the packs again in a folder of its own, the judges' answers copied in afterwards: byte for
    byte the packs of the run, and its result."""
    needs("data/rilly2003", "data/sources/g5/rows.json", "data/sources/g5/packs", *[str(p.relative_to(ROOT) / "lit/checked.json") for p in S.RUNS.values()])
    live = S.HOME

    def go(d):
        S.rows()
        S.packs()
        for name in ("rows.json", "entries.json", "groups.json"):
            assert S.read(d / name) == S.read(live / name), name
        names = sorted(p.name for p in (live / "packs").iterdir())
        assert names == sorted(p.name for p in (d / "packs").iterdir()) and all(filecmp.cmp(d / "packs" / n, live / "packs" / n, shallow=False) for n in names)
        for j in (1, 2):
            shutil.copytree(live / f"answers{j}", d / f"answers{j}", dirs_exist_ok=True)
        S.count()
        assert S.read(d / "result.json") == S.read(live / "result.json")
    in_a_folder(go)


def test_the_rules_were_in_git_before_the_judges_were_started():
    """WHEN's commit is git's, at its time; the judges were started after it (the session's log, by hand), answered
    after that and were counted after their last answer; the rules the page names stand in that commit."""
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout
    w = S.WHEN
    assert git("log", "-1", "--format=%cI", w["set_in"]).strip() == f"2026-11-16T{w['set']}-08:00"
    assert w["set"] < w["started"] < w["first_answer"] <= w["last_answer"] < w["counted"]
    for phrase in ("## 3. The bars and the rule, set before any judge is started", "**The status of a meaning:**"):
        out = git("log", "--reverse", "--format=%cI", f"-S{phrase}", "--", "data/discovery/second_scholar_later.md").split()
        assert out and out[0][11:19] <= w["set"], phrase
    assert f"the rules were committed at {w['set']} and the first judge was started at {w['started']}" in page()


def test_the_times_of_the_answers_are_the_files():
    """WHEN's first and last answer are the times of the judges' answer files (Pacific time)."""
    needs("data/sources/g5/answers1", "data/sources/g5/answers2")
    import datetime
    import zoneinfo
    pacific = zoneinfo.ZoneInfo("America/Los_Angeles")
    times = sorted(datetime.datetime.fromtimestamp(f.stat().st_mtime, pacific).strftime("%H:%M:%S")
                   for j in (1, 2) for f in (S.HOME / f"answers{j}").glob("*.jsonl"))
    assert times and (times[0], times[-1]) == (S.WHEN["first_answer"], S.WHEN["last_answer"]), (times[0], times[-1])


def test_the_rules_were_in_git_before_the_judges_answered():
    needs("data/sources/g5/answers1", "data/sources/g5/answers2")
    out = subprocess.run(["git", "-C", str(ROOT), "log", "--reverse", "--format=%ct", "-S## 3. The bars and the rule, set before any judge is started", "--",
                          "data/discovery/second_scholar_later.md"], capture_output=True, text=True).stdout.split()
    first = min(os.path.getmtime(f) for j in (1, 2) for f in (S.HOME / f"answers{j}").glob("*.jsonl"))
    assert out and int(out[0]) < first


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
