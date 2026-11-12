"""Checks for the same people in Demotic, Greek and Meroitic (src/demotic.py).

  python3 -I tests/test_demotic.py

FHN III, the readers' lists and the judges' answers are local only: the checks of the method run on made-up
lists, the checks of the reported numbers read the public figures file and compare it with the local files where
those are present.
"""
import json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import demotic as D    # noqa: E402
from local_only import needs, run   # noqa: E402

PAGE = ROOT / "data/discovery/demotic.md"
FIGURES = ROOT / "data/discovery/demotic_figures.json"
LOCAL = ("data/sources/fhn-text/pages.txt", "data/sources/demotic/answers/other_reader1.jsonl",
         "data/sources/demotic/meanings_rows.jsonl", "data/sources/expert/meanings_rows.jsonl", "data/rilly2003",
         "data/sources/coverage/corrected/glosses.jsonl")


def person(entry, name, language="Demotic", titles=(), same_as=(), reader="r1"):
    return {"entry": entry, "language": language, "person": name, "name_in_text": "", "role": "",
            "titles": [{"title": t, "original": o} for t, o in titles], "same_as": list(same_as), "reader": reader}


def test_plain_and_bare():
    assert D.plain("Wayekiye (A)") == "wayekiyea" and D.plain("qoreñ") == "qoren" and D.plain("Paêse") == "paese"
    assert D.bare("Wygy3") == "wg" and D.bare("Wyekiye") == "wk"
    assert D.bare("Abratoeis") == "brts" and D.bare("Brtoye") == "brt"


def test_a_readers_file_is_read_with_care():
    with tempfile.TemporaryDirectory() as d:
        folder = Path(d)
        (folder / "answers").mkdir()
        (folder / "answers" / "r1.jsonl").write_text("﻿" + "\n".join([
            json.dumps({"type": "person", "entry": "245", "language": "Demotic", "person": "Wayekiye (A)",
                        "titles": [{"title": "qeren of Isis", "original": "qrny"}, {"title": ""}, "junk"],
                        "same_as": ["246 Wyekiye", {"x": 1}], "kin": ["son of X"]}),
            json.dumps({"type": "person", "entry": "(246)", "person": "Taese", "titles": None}),
            json.dumps({"type": "person", "entry": "247", "person": ""}),                     # no name
            json.dumps({"type": "equation", "entry": 245, "meroitic": "qoreñ", "other": "qrny (Demotic)",
                        "meaning": "a title", "doubt": "yes"}),
            json.dumps({"type": "equation", "entry": "245", "meroitic": "perite", "meaning": ""}),   # no meaning
            json.dumps({"type": "note", "entry": "245"}), json.dumps(["a"]), "not json",
        ]) + "\n", encoding="utf-8")
        persons, equations = D.load("r1", folder)
    assert [(p["entry"], p["person"], p["titles"], p["same_as"]) for p in persons] == [
        ("245", "Wayekiye (A)", [{"title": "qeren of Isis", "original": "qrny"}], ["246 Wyekiye"]),
        ("246", "Taese", [], [])]
    assert equations == [{"entry": "245", "meroitic": "qoreñ", "other": "qrny (Demotic)", "meaning": "a title",
                          "doubt": False, "reader": "r1"}]


def test_what_two_readers_share():
    a = [person("245", "Wayekiye (A)"), person("245", "Hornakhtyotef"), person("260", "Pasan")]
    b = [person("245", "Wayekiye A"), person("260", "Pasan"), person("260", "Abratoye"), person("261", "Tami")]
    assert D.listed_by_both(a, b) == {"first": 3, "second": 4, "both": 2, "share_of_first": 0.6667, "share_of_second": 0.5}
    assert D.listed_by_both([], b)["share_of_first"] is None
    eq = lambda w: {"meroitic": w}
    assert D.known_found([eq("pelmos"), eq("Perite"), eq("qoreñ"), eq("antiye"), eq("pesetolo")]) == ["ant", "pelmos", "perite", "peseto", "qoren"]
    assert D.known_found([eq("plmos"), eq("wos")]) == []


def test_people_are_joined_by_name_and_by_the_editors():
    lines = [person("245", "Wayekiye (A)", titles=[("qeren of Isis", "qrny")], same_as=["246 Wyekiye", "999 Nobody"]),
             person("246", "Wayekiye (A)", "Meroitic", titles=[("agent", "perite")]),
             person("246", "Makaltami", "Meroitic", titles=[("strategus", "pelmos")]),
             person("243", "Mqoltemoye", same_as=["246 Mkltmy"]),                       # another spelling there
             person("252", "Wayekiye (B)", titles=[("agent of Isis", "rt")]),             # a namesake stays apart
             person("260", "Abratoye", titles=[("the king's son", "sy-nsw")], same_as=["265 Abratoeis"]),
             person("265", "Abratoye", "Greek", titles=[("psentes", "psentes")]),
             person("270", "Abratoye", "Meroitic", titles=[("King's Son", "peseto")])]
    folk = D.people(lines)
    by = {p["names"][0]: p for p in folk}
    assert len(folk) == 4
    assert by["Wayekiye (A)"]["entries"] == ["245", "246"] and set(by["Wayekiye (A)"]["titles"]) == {"Demotic or Egyptian", "Meroitic"}
    assert by["Makaltami"]["entries"] == ["243", "246"] and by["Makaltami"]["names"] == ["Makaltami", "Mqoltemoye"]
    assert by["Wayekiye (B)"]["entries"] == ["252"]
    assert set(by["Abratoye"]["titles"]) == {"Demotic or Egyptian", "Greek", "Meroitic"}
    two = D.in_two(folk)
    assert sorted(p["names"][0] for p in two) == ["Abratoye", "Wayekiye (A)"]             # Makaltami has one language
    assert by["Abratoye"]["titles"]["Meroitic"] == [("270", "King's Son", "peseto")]


def test_names_are_left_out_of_the_judges_lines():
    eqs = [{"entry": "245", "meroitic": "qoreñ", "other": "qrny", "meaning": "a title", "doubt": True, "reader": "r1"},
           {"entry": "232", "meroitic": "Wyekiye", "other": "Wygy3", "meaning": "personal name Wayekiye", "doubt": False, "reader": "r1"}]
    assert D.is_name(eqs[1]) and not D.is_name(eqs[0])
    assert D.found(eqs) == [{"source": "FHN III", "entries": ["245"], "word": "qoreñ", "meaning": "a title", "doubt": True, "from": "r1"}]


def page():
    return re.sub(r"\s+", " ", PAGE.read_text(encoding="utf-8"))


def test_reported_numbers():
    f, text = json.loads(FIGURES.read_text(encoding="utf-8")), page()
    r = f["readers"]
    for label, name in (("Demotic and Greek entries, first", "other_reader1"), ("Demotic and Greek entries, second", "other_reader2"),
                        ("Meroitic entries", "meroitic_reader1")):
        assert f"| {label} | {r[name]['persons']} | {r[name]['equations']} |" in text, label
    b = f["persons_listed_by_both"]
    assert b["share_of_first"] >= 0.8 and b["share_of_second"] >= 0.8                       # the first bar
    assert f"they do in {b['both']} of {b['first']} ({b['share_of_first']:.1%})" in text and b["first"] == b["second"]
    k = f["known_equations"]
    assert k["first"] == k["second"] and len(k["first"]) == 4 >= 4 and "ant" in k["meroitic_reader"]   # the second bar
    assert f"That gives {f['people']} people, {f['people_in_two_entries_or_more']} of them in two entries or more" in text
    assert f["people_with_titles_in_two_languages"] == 4 and "Four have a title in a Meroitic text" in text
    e, t = f["equations"], f["table"]
    assert f"list {e['all']} equations; {e['of_names']} only set two spellings" in text
    assert f"The other {e['all'] - e['of_names']} are {t['lines']} different lines" in text
    for label, key in (("translated", "translated"), ("a proposal only (hypothesis)", "held without an accepted meaning (hypothesis)"),
                       ("the kind only", "held without an accepted meaning (kind)"), ("not in the map", "not in the map")):
        assert f"| {label} | {t['our map'][key]} |" in text, label
    d = t["decoys"]
    assert f"For the {t['judged']} lines" in text and f"({d['first judge']} and {d['second judge']})" in text
    assert t["decoys, first judge"]["agree"] == t["decoys, second judge"]["agree"] == 0 and "Neither accepted a decoy" in text
    j1, j2, both = t["translated, first judge"], t["translated, second judge"], t["two judges, translated"]
    assert f"on {j1['agree']} of {j1['rows']} and the second on {j2['agree']} of {j2['rows']}" in text
    assert f"on the {both['rows']} both saw with our reading they gave the same verdict on {both['same_verdict']} (Cohen's kappa {both['kappa']:.2f})" in text
    assert f"{f['lines_on_words_not_listed_before']['lines']} of the {t['lines']} lines are on a word or phrase" in text
    lack, sure = t["lacking"], t["lacking, stated as sure"]
    for label, key in (("no accepted meaning for the word", "our map has no accepted meaning for the word"),
                       ("both judges say the editors read it otherwise", "our map reads the word otherwise (both judges)"),
                       ("the one judge who saw our reading", "our map reads the word otherwise (the one judge who saw our reading)"),
                       ("one judge of two", "our map may read the word otherwise (one judge of two)")):
        assert f"{label} | {lack[key]} | {sure[key]} |" in text, label
    assert f"| all | {sum(lack.values())} | {sum(sure.values())} |" in text
    n = f["not_in_the_map"]
    assert f"{n['held_once_the_ocr_is_mended']} of the {n['lines']} lines \"not in the map\"" in text
    assert f"**The editors set {e['all'] - e['of_names']} Meroitic words or phrases" in text
    assert f"For the {t['our map']['translated']} different lines whose word our map translates" in text


def test_the_volume_is_cut_at_its_headings():
    needs("data/sources/fhn-text/pages.txt")
    text = D.entries()
    wanted = D.OTHER["Demotic"] + D.OTHER["Greek"] + D.MEROITIC
    assert all(n in text for n in wanted) and len(D.OTHER["Demotic"]) == 22 and len(D.OTHER["Greek"]) == 2
    assert text[243].startswith("243 Philae. Demotic graffito of Makaltami") and "244 Dakka" not in text[243]
    assert "Makheye" in text[271].splitlines()[0] and text[272].startswith("272 Philae")


def test_public_figures_are_what_the_local_files_give():
    needs(*LOCAL)
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        figs = D.count()
    assert figs == json.loads(FIGURES.read_text(encoding="utf-8"))
    folk, lines, _ = D.merge()
    assert len(D.in_two(folk)) == figs["people_with_titles_in_two_languages"]
    assert sorted(p["names"][0] for p in D.in_two(folk)) == ["Abratoye", "Beke", "Bekemete", "Manitawawi"]


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
