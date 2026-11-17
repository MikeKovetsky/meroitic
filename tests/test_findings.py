"""FINDINGS.md, the write-up of the project's negative results: every number on it is the figures files' number, or
the number of the page it names where no script writes one.

  python3 -I tests/test_findings.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import themap as M                   # noqa: E402
from local_only import run           # noqa: E402

RAW = (ROOT / "FINDINGS.md").read_text(encoding="utf-8")
PAGE = " ".join(RAW.split())                                                    # the page with its line breaks undone


def figures(name):
    return json.loads((ROOT / "data/discovery" / name).read_text(encoding="utf-8"))


def flat(path):
    return " ".join((ROOT / path).read_text(encoding="utf-8").split())


def pc(a, b):
    return f"{100 * a / b:.1f}%"


def run_line(name, words, needs, c):
    return (f"| {name} | {words} | {needs} | {c['offered_right']} of {c['offered_chosen']} ({pc(c['offered_right'], c['offered_chosen'])}) "
            f"| {c['absent_wrong']} of {c['absent']} ({pc(c['absent_wrong'], c['absent'])}) |")


def test_the_corpus_and_the_map():
    first = figures("recurring_words_figures.json")["map"]
    assert f"{first['inscriptions']} inscriptions ({first['running_words']:,} running words)" in PAGE
    m = figures("map_figures.json")
    r, lk, n = m["current"]["running"], m["lookup"]["running"], m["north_star"]
    assert f"{r['need']:,} running words that need a meaning (no name, no numeral, no lost sign), {r['translated']:,} are translated: {pc(r['translated'], r['need'])}" in PAGE
    assert f"gives {pc(lk['translated'], lk['need'])}" in PAGE
    s = M.star_pct(n)                                                           # divided from the counts and rounded once
    assert f"{n['translated']} of about {n['distinct_words']['point']:,} distinct words have a meaning: {s['point']} (between {s['low']} and {s['high']}" in PAGE
    assert f"{n['translated_by_the_lexicon']} come from Rilly's lexicon of 2003 and {sum(n['translated_by_a_layer'].values())} from later works" in PAGE
    assert n["translated_by_the_lexicon"] + sum(n["translated_by_a_layer"].values()) == n["translated"]
    assert "Meanings found by the project: 0." in PAGE
    # why: the spellings without a meaning, and how few of them recur
    assert (f"Of the {first['open_spellings']:,} distinct spellings without an accepted meaning on the first map, {first['in_three_texts_or_more']} stand "
            "in three texts or more.") in PAGE


def test_the_three_runs_of_the_blind_choice():
    one = figures("recurring_words_figures.json")["choice"]
    two, three = figures("blind_test_2_figures.json")["choice"], figures("blind_test_83_figures.json")["choice"]
    assert (one["needed"], two["needed"], three["needed"]) == (4, 5, 5) and one["readers"] == two["readers"] == three["readers"] == 5
    assert run_line("First", one["offered"] + one["absent"], "four of five readers", one) in PAGE
    assert run_line("Second", two["offered"] + two["absent"], "all five", two) in PAGE
    assert run_line("Third", three["offered"] + three["absent"], "all five", three) in PAGE
    # the bars as set, and the second missed in every run
    b = one["bars"]
    assert b == two["bars"] == three["bars"]
    assert (f"at least {round(100 * b['right_when_chosen'])}% of those choices must be right, on at least {b['chosen_at_least']} words. Where it is "
            f"not offered, at most {round(100 * b['wrong_when_absent'])}% of the words may get a meaning chosen") in PAGE
    assert all(c["absent_wrong"] / c["absent"] > b["wrong_when_absent"] for c in (one, two, three)) and "The second bar was missed in every run" in PAGE
    assert all(0.15 < c["absent_wrong"] / c["absent"] < 0.25 for c in (one, two, three)) and "about one word in five whose true meaning is not offered" in PAGE
    assert all(c["right_when_chosen"] > 0.9 for c in (two, three)) and "five readers who agree are nearly always right" in PAGE
    after = one["all_agree"]
    assert after["absent_wrong"] == 0
    assert f"no wrong choice among {one['absent']} words. Set beforehand in the second run, it gave {two['absent_wrong']} of {two['absent']}" in PAGE
    # the example: "silver" chosen by all five for the word it is proposed for, and for the word for "god"
    second = figures("blind_test_2_figures.json")
    assert "silver" in second["open_chosen"].values()
    assert any(w["true"] == "god" and w["chosen"] == "silver" and w["sort"] == "absent" for w in second["wrong_choices"])
    # the earlier trial is the report's, with its reservation
    report = flat("REPORT.md")
    assert ("27 words of known meaning gave the right kind of word 26 times and the meaning 4 times, each time for a word that stands opposite a known "
            "partner (north and south, mother and father). One reader, not blind") in report
    assert ("27 words of known meaning were judged from their contexts alone, by one reader who was not blind: the kind of word came out right 26 times, "
            "the meaning 4 times") in PAGE and "It measures the method's reach, not a result" in PAGE


def test_the_grammar_pilot():
    g = figures("grammar_pilot_figures.json")
    b, s, p = g["both"], g["split"], g["parse"]["all"]
    assert f"{s['tuning']['texts']} for finding rules and {s['held']['texts']} held back" in PAGE
    assert s["tuning"]["texts"] + s["held"]["texts"] == 548
    assert (f"| Proposed | {b['rules']} | | Passed on the held-back texts | {b['passed']} | "
            f"| Stated or partly stated in a source in hand | {b['stated_or_partly_stated']} | | A finding of the project | {b['ours']} |") in PAGE
    assert f"The bar for going on was {g['ours_needed']} such findings" in PAGE and not b["bar_met"]
    assert f"at least {g['bars']['cases']} cases there, held in at least {round(100 * g['bars']['rate'])}% of them, and stood {round(100 * g['bars']['margin'])} points above" in PAGE
    assert "committed before it was run on the held-back texts" in PAGE                 # the second round's tests came after the table was written
    one = g["rounds"]["1"]
    assert f"{round(100 * g['cases_by_kind']['share']['funerary'])}% of the cases of the first round's {one['passed']} passed rules stand in epitaphs" in PAGE
    nf = s["tuning"]["not_funerary"]["words"] + s["held"]["not_funerary"]["words"]
    assert f"Outside the epitaphs there are about {round(nf, -3):,} words." in PAGE
    every = s["tuning"]["words"] + s["held"]["words"]
    assert every - nf > every / 2 and f"{every:,} running words, most of them in epitaphs" in PAGE
    assert (f"speak of {p['open_words_a_rule_speaks_of']} of the {p['open_words']} words without a meaning, and of "
            f"{p['open_words_by_what_is_said']['plural']} of those they say only that the word ends in `-eb`, like a plural") in PAGE
    assert f"{b['partly_stated_by_both']} points where the count is sharper" in PAGE
    assert (f"on {b['partly_stated_by_both'] + b['ours']} points of grammar and spelling: the {b['partly_stated_by_both']} where the project's counts "
            f"are sharper than its sources, and the {'one' if b['ours'] == 1 else b['ours']} rule those sources do not state") in PAGE


def test_the_comparison_with_the_family_is_its_pages():
    cog, readme = flat("data/discovery/cognates_rules.md"), flat("README.md")
    assert "The ten independent lists (Old Nubian, Nobiin, Kenzi, Dongolawi, Midob, Birgid, Hill Nubian, Nara, Taman, Nyima)" in cog
    assert "ten Northern East Sudanic languages, Nubian among them, against 2,000 shuffles" in PAGE and "ten Nubian-family" not in PAGE
    assert "compare with 2,000 shuffles of the Meroitic meanings" in cog and "On the 31 gold words the rules were not built from, it does no better than chance (p = 0.49)" in cog
    assert "(p = 0.49)" in PAGE and "p = 0.49 on words held out" in PAGE
    assert "Rilly's 82 sound correspondences" in readme and "Rilly's 82 sound correspondences" in PAGE
    # gate A1, the two whole dictionaries of Nile Nubian: its bar's p, as the figures file of track A gives it
    a1 = figures("outside_nubian_figures.json")["gate_a1"]
    p = f"p = {a1['all']['rule']['by_length']['p']:.3f}"
    assert a1["verdict"] == "missed" and f"did no better ({p} against a shuffle within words of one length" in PAGE
    assert f"missed its bar ({p})" in PAGE and "has not been run" not in PAGE and "not yet counted" not in PAGE


def test_what_went_wrong_is_the_figures():
    one = figures("leftover_parts_figures.json")["part_1"]["lot_letters"]["explained_at"]
    names = sum(a == "name" for x in one for a in x["answers"])
    assert f"in {names} of the {2 * len(one)} answers at the {len(one)} such places of one reading" in PAGE
    stems = figures("leftover_stems_figures.json")
    laid = stems["laid"]
    assert (f"the {stems['places']} leftover places never given to checkers" in PAGE
            and f"the first laid {laid['lines']} more places in the map ({laid['to']['name']} names and {laid['to']['grammar']} word of grammar)" in PAGE)
    assert "Three times a review found" in PAGE


def test_the_page_names_what_it_rests_on():
    for page in ("map_layers.md", "distinct_words.md", "recurring_words.md", "blind_test_2.md", "blind_test_83.md", "grammar_pilot.md", "cognates_rules.md"):
        assert f"(data/discovery/{page})" in PAGE and (ROOT / "data/discovery" / page).exists(), page
    assert "[FINDINGS.md](FINDINGS.md)" in (ROOT / "README.md").read_text(encoding="utf-8") and "python3 -I tests/test_findings.py" in flat("README.md")
    assert "decipher" not in PAGE.lower().replace("undeciphered", "")
    n = json.loads((ROOT / "data/discovery/corpus_v6_figures.json").read_text(encoding="utf-8"))["inscriptions"]["with_an_open_reading"]
    assert f"the open readings of {n} inscriptions are" in PAGE and f"{n} inscriptions are now machine-readable under an open licence" in flat("README.md")


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
