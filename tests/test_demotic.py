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


def person(entry, name, language="Demotic", titles=(), same_as=(), reader="r1", in_text=""):
    return {"entry": entry, "language": language, "person": name, "name_in_text": in_text, "role": "",
            "titles": [{"title": t, "original": o} for t, o in titles], "same_as": list(same_as), "reader": reader}


def test_plain_and_bare():
    assert D.plain("Wayekiye (A)") == "wayekiyea" and D.plain("qoreñ") == "qoren" and D.plain("Paêse") == "paese"
    assert D.bare("Wygy3") == "wg" and D.bare("Wyekiye") == "wk"
    assert D.bare("Abratoeis") == "brts" and D.bare("Brtoye") == "brt"
    assert [D.namesake(n) for n in ("Wayekiye (A)", "Hornakhtyotef II", "Hornakhtyotef (I)", "Wayekiye A")] == \
        ["A", "II", "I", "A"]
    assert [D.namesake(n) for n in ("Mtewwi (Manitawawi)", "Tsône the elder", "Taêse", "Wygy3", "NN")] == [""] * 5
    assert D.alike("Hornakhtyotef I", "Hornakhtyotef (II)") == 1.0          # the letter is weighed apart, not here
    assert D.alike("P3-šr-n-t3-snt", "Sosen") < D.SAME_NAME <= D.alike("Harendotes", "Hr-nd-it=f")


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


def test_the_editors_identification_is_not_stretched():
    folk = D.people([
        person("232", "Hornakhtyotef (I)", same_as=["249 Hornakhtyotef I"]),   # (I) is not in 249: no line to join
        person("249", "Hornakhtyotef (II)"),
        person("231", "Pshentsône", same_as=["232 P3-šr-n-t3-snt"]),             # named in 232's comments only
        person("232", "Sosen", in_text="Ssn"),
        person("250", "Weyegeye", same_as=["245 Wygy3"]),                         # the spelling of the ancient text
        person("245", "Wayekiye (A)", in_text="Wygy3"),
        person("252", "Wayekiye (B)", same_as=["245 Wayekiye"])])               # a namesake of another letter
    entries = sorted(p["entries"] for p in folk)
    assert entries == [["231"], ["232"], ["232"], ["245", "250"], ["249"], ["252"]], entries
    one = D.people([person("245", "Wayekiye (A)"), person("246", "Wyekiye", "Meroitic", same_as=["245 Wayekiye A"])])
    assert [p["entries"] for p in one] == [["245", "246"]]                    # the same letter, written otherwise


def test_the_ocr_and_a_readers_two_spellings_in_one():
    assert D.mended("Akiri") == ["Akiñ"] and D.mended("mete") == []
    assert D.mended("ttri qorise") == ["ttñ qorise", "ttri qoñse", "ttñ qoñse"]           # each place on its own
    assert D.apart("mete/mte") == ["mete", "mte"] and D.apart("st(e)mdese") == ["stemdese", "stmdese"]
    assert D.apart("pesto/peseto Akiri-te") == ["pesto Akiri-te", "peseto Akiri-te"] and D.apart("qore") == []
    held = {"meaning": {"level": "meaning", "gloss": "an office"}, "hypothesis": {"level": "hypothesis", "gloss": "?"}}
    in_map = {D.K.M.spellings(w)[0]: held[level] for w, level in (("ttñ", "meaning"), ("qorise", "meaning"),
                                                                   ("mte", "meaning"), ("Akiñ-te", "hypothesis"),
                                                                   ("pesto", "meaning"))}
    m = ({}, {}, in_map)                                       # an empty lexicon: only the map's own words are held
    assert D.misread("ttri qorise", "FHN III", m) and not D.two_in_one("ttri qorise", "FHN III", m)
    assert not D.misread("ttñ qorise", "FHN III", m)                         # held as written: not an artefact
    both = ({}, {}, {**in_map, D.K.M.spellings("ttri")[0]: held["meaning"]})
    assert not D.misread("ttri", "FHN III", both) and D.misread("ttri", "FHN III", m)   # held as written, and mended
    either = ({}, {}, {**in_map, D.K.M.spellings("ñ/qe")[0]: held["meaning"], D.K.M.spellings("qe")[0]: held["meaning"]})
    assert D.misread("ri/qe", "FHN III", either) and not D.two_in_one("ri/qe", "FHN III", either)   # counted once
    assert D.two_in_one("mete/mte", "FHN III", m) and not D.misread("mete/mte", "FHN III", m)
    assert D.two_in_one("pesto/peseto Akiri-te", "FHN III", m)             # two spellings, and the OCR's ñ
    assert not D.misread("hbhri", "FHN III", m) and not D.two_in_one("mreperi/mrepero", "FHN III", m)
    assert D.corrected("hbhri qorises", ["267"]) == "hbhri qorise"                # FHN IV's corrigenda
    assert D.corrected("hbhri qorises", ["268"]) == "hbhri qorises"               # only in the entry it corrects
    assert D.corrected("stemedese pesetolis", ["270", "271"]) == "stemdese pesetolise"
    titles = ({}, {}, {**in_map, D.K.M.spellings("hbhñ")[0]: held["meaning"]})
    assert D.misprinted("hbhri qorises", ["267"], "FHN III", titles)              # corrected, then the OCR's ñ
    assert not D.misread("hbhri qorises", "FHN III", titles)                      # the OCR alone does not do it
    assert not D.misprinted("hbhri qorises", ["268"], "FHN III", titles)
    assert not D.misprinted("hbhri qorises", ["267"], "Millet 2005", titles)      # FHN's misprints, FHN's lines
    assert D.misread("hbhri qorise", "FHN III", titles)                           # no misprint: counted once,
    assert not D.misprinted("hbhri qorise", ["267"], "FHN III", titles)           #   for the OCR
    assert not D.misprinted("stemedese pesetolis", ["271"], "FHN III", titles)    # corrected, still not held
    assert D.corrected("ant boqhw dik", ["268"]) == "ant Boqhw dik"              # a capital letter only:
    assert not D.misprinted("ant boqhw dik", ["268"], "FHN III", titles)          #   the lookup is the same
    assert D.cut_short("a loan from Demotic t") and D.cut_short("Isis / title related to Demotic p")
    assert not D.cut_short("Isis +i") and not D.cut_short("great envoy, chief envoy / ") and not D.cut_short("")


def test_packs_and_the_table_are_never_written_again():
    for make, answer in ((D.packs, "other_reader1.jsonl"), (D.table, "meanings_judge1.jsonl")):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "answers").mkdir()
            (Path(d) / "answers" / answer).write_text("{}\n")
            try:
                make(Path(d))
            except SystemExit as e:
                assert "not writing" in str(e)
            else:
                raise AssertionError(f"{make.__name__} wrote its packs over answers")


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
    assert f"list {e['all']} equations; {e['of_names']} are left out as names" in text
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
    ocr, two, typo = (n["held_once_the_ocr_is_mended"], n["held_once_two_spellings_are_read_apart"],
                      n["held_once_a_misprint_is_corrected"])
    assert (f"{ocr + two + typo} of the {n['lines']} lines \"not in the map\" are words the map holds: {ocr} misread "
            f"by the OCR") in text and f", {two} that a reader wrote as two spellings in one" in text
    assert f"and {typo} misprinted in FHN III itself and corrected in its index volume" in text
    assert f"The index volume corrects {f['misprints_corrected_by_fhn_iv']} of our lines in all" in text
    assert f"And {f['readings_cut_short']} of our readings reached the judges cut short" in text
    assert f"**The editors set {e['all'] - e['of_names']} Meroitic words or phrases" in text
    assert f"For the {t['our map']['translated']} different lines whose word our map translates" in text
    assert f"so {f['people'] - 2} people became {f['people']}" in text           # what the review changed
    assert "the example line of the readers' brief" in text and '"meroitic": "qoreñ"' in D.BRIEF   # the bar's caveat
    readers, judges = (136380, 138439, 109839), (62952, 63312)                   # the cost, by hand
    assert (f"three readers {sum(readers):,} subagent tokens ({readers[0]:,}, {readers[1]:,} and {readers[2]:,}), two "
            f"judges {sum(judges):,} ({judges[0]:,} and {judges[1]:,})") in text
    assert numbers(PAGE.read_text(encoding="utf-8"), PAGE_STATED) <= known(f), \
        sorted(numbers(PAGE.read_text(encoding="utf-8"), PAGE_STATED) - known(f))


# numbers a text may state without a figure behind them: entries and dates it names, the bar and its quote, the
# cost by hand, and the figures the review replaced
ENTRIES = {"229", "231", "244", "246", "247", "249", "252", "253", "254", "260", "261", "264", "265", "267", "270",
           "271", "291", "306"}
PAGE_STATED = ENTRIES | {"2026-11-12", "17", "80%", "5.5", "2000", "1234", "136,380", "138,439", "109,839", "384,658", "62,952",
                         "63,312", "126,264", "97"}
NUMBER = re.compile(r"\d{4}-\d\d-\d\d|\d[\d,]*(?:\.\d+)?%?")


def numbers(text, stated=()):
    """The numbers of a text, outside its code blocks, that are neither below 10 nor stated."""
    found = {t.rstrip(",") for t in NUMBER.findall(re.sub(r"```.*?```", " ", text, flags=re.S))}
    return {t for t in found if t not in stated and not (t.isdigit() and int(t) < 10)}


def known(f):
    """Every number the figures file holds, as a text writes it, and the sums the page draws from it."""
    out = set()

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, bool) or x is None or isinstance(x, str):
            return
        elif isinstance(x, int):
            out.update({str(x), f"{x:,}"})
        else:
            out.update({f"{x:.1%}", f"{x:.2f}"})
    walk(f)
    t, e = f["table"], f["equations"]
    n = f["not_in_the_map"]
    out.update({str(e["all"] - e["of_names"]), str(sum(t["decoys"].values())), str(sum(t["lacking"].values())),
                str(sum(t["lacking, stated as sure"].values())),
                str(len(D.OTHER["Demotic"])), str(len(D.OTHER["Demotic"]) + len(D.OTHER["Greek"])),
                str(n["held_once_the_ocr_is_mended"] + n["held_once_two_spellings_are_read_apart"]
                    + n["held_once_a_misprint_is_corrected"])})
    return out


def between(text, start, end="\n\n"):
    """The text from start (which stands once) to end, or to the text's end."""
    assert text.count(start) == 1, start
    rest = text[text.index(start):]
    return rest[:rest.index(end)] if end in rest else rest


def test_the_summaries_quote_the_figures():
    """README, REPORT, NEXT_STEPS and the summary page say of this step what the figures file says."""
    f = json.loads(FIGURES.read_text(encoding="utf-8"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
    steps = (ROOT / "NEXT_STEPS.md").read_text(encoding="utf-8")
    html = (ROOT / "docs/report.html").read_text(encoding="utf-8")
    parts = {"README, item 13": between(readme, "13. **The same people in Demotic", "14. **A second scholar"),
             "README, step 20": between(readme, "### 20. The same people in two scripts", "### 21."),
             "REPORT": between(report, "3. **The same people in Demotic, Greek and Meroitic**", "6. **Cost:**"),
             "REPORT, review": between(report, "7. **What the review changed:** the join"),
             "NEXT_STEPS, point 14": between(steps, "14. **The same people in Demotic", "15. **F2: a second scholar"),
             "NEXT_STEPS, step 17": between(steps, "    - **The people named in both the Philae graffiti",
                                            "    - **What it leaves:** the Demotic list"),
             "the summary page": between(html, "<tr><td>Read the 22 Demotic graffiti", "</tr>")}
    parts = {k: re.sub(r"\s+", " ", v) for k, v in parts.items()}
    # the numbers of items, points and steps; the bar; what the review replaced; the readers' step (test_v6_readers)
    stated = ENTRIES | {"2026-11-12", "13", "14", "17", "20", "80%", "97", "11", "12"}
    for name, text in parts.items():
        odd = numbers(text, stated) - known(f)
        assert not odd, (name, sorted(odd))
    people = f"{f['people']} people"
    assert all(people in parts[k] or f"({f['people']}, " in parts[k] for k in ("README, item 13", "REPORT",
                                                                              "the summary page"))
    t = f["table"]
    assert (f"{sum(t['lacking'].values())} lines, {t['lacking']['our map has no accepted meaning for the word']} of "
            "them on words without an accepted meaning") in parts["REPORT"]
    n = f["not_in_the_map"]
    artefacts = sum(n[k] for k in ("held_once_the_ocr_is_mended", "held_once_two_spellings_are_read_apart",
                                   "held_once_a_misprint_is_corrected"))
    assert f"; {artefacts} of those are words" \
        in parts["REPORT"]
    cost = between(report, "6. **Cost:** eight analysts", "7. **What the review changed:**")
    analysts, readers, judges = 1012556, 384658, 126264
    assert (f"eight analysts {analysts:,} subagent tokens; three readers {readers:,} and two judges {judges:,} for the "
            f"Demotic step; {analysts + readers + judges:,} together before the review") in re.sub(r"\s+", " ", cost)


def test_a_number_out_of_turn_is_not_a_heading():
    pages = {56: "190 Philae. Before the sources begin.",
             57: "186 Philae. The first entry of the sources.\nSome text.\n"
                 "260 Philae is named here, in a line of entry 186.\n972 Fontes Historiae Nubiorum III\n",
             58: "(187) Dakka. The second entry.\nMore text.\n189 Philae. A heading that skips one number.\n"
                 "188 Philae. A cross-reference that goes back.\n"}
    with tempfile.TemporaryDirectory() as d:
        layer = Path(d) / "pages.txt"
        layer.write_text("".join(f"\x0c=== page {n} ===\n{t}" for n, t in pages.items()), encoding="utf-8")
        text = D.entries(layer)
    assert sorted(text) == [186, 187, 189]
    assert "260 Philae is named here" in text[186] and "972 Fontes" in text[186] and "190 Philae" not in text[186]
    assert text[187].startswith("(187) Dakka") and "188 Philae" in text[189]


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
    assert all(len({D.namesake(n) for n in p["names"]} - {""}) <= 1 for p in folk)      # no two namesakes in one
    assert not any({"Pshentsône", "Sosen"} <= set(p["names"]) for p in folk)             # generations 1 and 4


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
