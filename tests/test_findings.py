"""FINDINGS.md, the write-up of the project's negative results: every number on it is the figures files' number.

  python3 -I tests/test_findings.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = (ROOT / "FINDINGS.md").read_text(encoding="utf-8")


def figures(name):
    return json.loads((ROOT / "data/discovery" / name).read_text(encoding="utf-8"))


def pc(a, b):
    return f"{100 * a / b:.1f}%"


def run_line(name, words, needs, c):
    return (f"| {name} | {words} | {needs} | {c['offered_right']} of {c['offered_chosen']} ({pc(c['offered_right'], c['offered_chosen'])}) "
            f"| {c['absent_wrong']} of {c['absent']} ({pc(c['absent_wrong'], c['absent'])}) |")


def test_the_map():
    m = figures("map_figures.json")
    r, lk, n = m["current"]["running"], m["lookup"]["running"], m["north_star"]
    assert f"{r['need']:,} running words that need a meaning (no name, no numeral, no lost sign), {r['translated']:,}\n  are translated: {pc(r['translated'], r['need'])}" in PAGE
    assert f"gives {pc(lk['translated'], lk['need'])}" in PAGE
    assert (f"{n['translated']} of about {n['distinct_words']['point']:,} distinct words have a meaning: "
            f"{pc(n['translated'], n['distinct_words']['point'])} (between {100 * n['star']['low']:.1f}% and {100 * n['star']['high']:.1f}%") in PAGE
    assert f"{n['translated_by_the_lexicon']} come from Rilly's lexicon of 2003 and\n  {sum(n['translated_by_a_layer'].values())} from later works" in PAGE
    assert n["translated_by_the_lexicon"] + sum(n["translated_by_a_layer"].values()) == n["translated"]


def test_the_three_runs_of_the_blind_choice():
    one = figures("recurring_words_figures.json")["choice"]
    two, three = figures("blind_test_2_figures.json")["choice"], figures("blind_test_83_figures.json")["choice"]
    assert (one["needed"], two["needed"], three["needed"]) == (4, 5, 5) and one["readers"] == two["readers"] == three["readers"] == 5
    assert run_line("First", one["offered"] + one["absent"], "four of five readers", one) in PAGE
    assert run_line("Second", two["offered"] + two["absent"], "all five", two) in PAGE
    assert run_line("Third", three["offered"] + three["absent"], "all five", three) in PAGE
    # the second bar (at most 10% wrongly chosen) was missed in every run, as the page says
    assert all(c["absent_wrong"] / c["absent"] > c["bars"]["wrong_when_absent"] for c in (one, two, three))
    assert "The second bar was missed in every run" in PAGE
    after = figures("recurring_words_figures.json")["choice"]["all_agree"]
    assert after["absent_wrong"] == 0
    assert f"no wrong choice among {one['absent']} words. Set beforehand in the second run, it gave {two['absent_wrong']} of {two['absent']}" in PAGE
    # the example: "silver" chosen by all five for the word it is proposed for, and for the word for "god"
    second = figures("blind_test_2_figures.json")
    assert "silver" in second["open_chosen"].values()
    assert any(w["true"] == "god" and w["chosen"] == "silver" and w["sort"] == "absent" for w in second["wrong_choices"])


def test_the_grammar_pilot():
    g = figures("grammar_pilot_figures.json")
    b, s, p = g["both"], g["split"], g["parse"]["all"]
    assert f"{s['tuning']['texts']} for finding rules and {s['held']['texts']} held back" in PAGE
    assert s["tuning"]["texts"] + s["held"]["texts"] == 548
    assert (f"| Proposed | {b['rules']} |\n| Passed on the held-back texts | {b['passed']} |\n"
            f"| Stated or partly stated in a source in hand | {b['stated_or_partly_stated']} |\n| A finding of the project | {b['ours']} |") in PAGE
    assert f"The\nbar for going on was {g['ours_needed']} such findings" in PAGE and not b["bar_met"]
    assert f"at least {g['bars']['cases']} cases there, held in at least {round(100 * g['bars']['rate'])}% of\nthem, and stood {round(100 * g['bars']['margin'])} points above" in PAGE
    assert f"{round(100 * g['cases_by_kind']['share']['funerary'])}% of the passed rules' cases stand in" in PAGE
    assert (f"speak of {p['open_words_a_rule_speaks_of']} of the {p['open_words']} words without a meaning, and of "
            f"{p['open_words_by_what_is_said']['plural']} of those") in PAGE
    assert f"{b['partly_stated_by_both']} points where the count is sharper" in PAGE
    assert f"the {b['partly_stated_by_both'] + b['ours']} points of grammar and spelling" in PAGE


def test_the_page_names_what_it_rests_on():
    for page in ("map_layers.md", "distinct_words.md", "recurring_words.md", "blind_test_2.md", "blind_test_83.md", "grammar_pilot.md", "cognates_rules.md"):
        assert f"(data/discovery/{page})" in PAGE and (ROOT / "data/discovery" / page).exists(), page
    assert "[FINDINGS.md](FINDINGS.md)" in (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Meanings found by the project: 0." in PAGE and "decipher" not in PAGE.lower().replace("undeciphered", "")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"{len(tests)} checks passed")
    sys.exit(0)
