"""Checks for the lexicon test (src/lexique.py) and the corpus merge (src/expand.py).

  python3 -I tests/test_lexique.py
"""
import contextlib, io, json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import expand, lexique   # noqa: E402
from local_only import needs, run   # noqa: E402

# what `lexique.py judged` found about the run of 2026-11-09 (the module's docstring, README Methods 5)
NOT_TEST_WORDS = ["nobo", "qoleb", "yer"]
GIVEN_AWAY = ["mkdi", "qor-o", "qorene", "qorise", "qorode", "smlo (1)"]
LEFT_OUT = ["ntki", "qor"]


def quiet(fn, *args, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kw)


def entry(headword, meaning, texts=(), **kw):
    """A lexicon entry as the extraction wrote it, and the texts its headword occurs in."""
    e = {"headword": headword, "meaning_en": meaning, "status": "established", "category": "substantif",
         "page_pdf": 20, **kw}
    return e, {f: set(texts) for f in lexique.corpus_spellings(headword)} if texts else {}


def lexicon(*pairs):
    entries, texts_with = [], {}
    for e, tw in pairs:
        entries.append(e)
        for f, ts in tw.items():
            texts_with.setdefault(f, set()).update(ts)
    return entries, texts_with


def test_spellings_follow_the_corpus_convention():
    sp = lexique.corpus_spellings
    assert sp("ḫlbi") == {"xlbi"} and sp("ẖe (1)") == {"Xe"}         # the two h signs; "(1)" is a note
    assert sp("h̭r") == {"xr"}                                         # the look-alike of ḫ
    assert sp("ssor") == {"SSor"}                                     # Rilly's s is the corpus's S sign
    assert sp("qorise") == {"qoris", "qoriSe"}                        # se: the se sign, or s + e
    assert sp("ḫrpḫne") == {"xrpxN", "xrpxne"}                        # ne likewise
    assert sp("tñyi") == {"tNyi"} and sp("atê") == {"ato"} and sp("šo") == {"So"}
    assert sp("aṛe") == {"are"}                                       # a dotted letter is that letter
    assert sp("ḫbḫl(i)") == {"xbxl", "xbxli"}                         # letters in brackets are optional
    assert sp("qor-o") == {"qoro"} and sp("Ḫlbi") == {"xlbi"}
    assert sp("a[.]b") == set() and sp("a…b") == set()                # lost signs: no spelling to look for


def test_a_cross_reference_is_not_a_meaning():
    xref = lambda m: bool(lexique.XREF.search(m))
    assert xref("variant of ato") and xref("see peseto") and xref("cf. qore") and xref("var. of at")
    assert not xref("not a mere variant of qore") and not xref("ruler; see also qore") and not xref("seeds")


def test_endings_count_unless_another_word_owns_them():
    tw = {"yerike": {"T2"}, "yer": {"T3"}, "qowi": {"T1"}}
    assert lexique.occurrences({"yeri"}, tw) == {"T2"}                 # yeri + ke
    assert lexique.occurrences({"yeri"}, tw, {"yerike"}) == set()      # ... unless yerike is another entry's word
    assert lexique.occurrences({"qo"}, tw) == set()                    # two letters take no ending
    assert lexique.occurrences({"yer"}, tw) == {"T3"}


def test_testable_leaves_out_what_is_not_a_test_word():
    two = ("T1", "T2")
    entries, tw = lexicon(
        entry("abr", "man", two),
        entry("Amni", "Amun", two),                                    # a name: Rilly capitalises it
        entry("pedeme", "Qasr Ibrim", two, category="toponyme"),       # a name by its category
        entry("-lowi", "it is", two, category="suffixe"),              # an ending
        entry("kelw", "and, also", two, category="particule"),         # a grammatical word
        entry("arme", "Rome", two, page_pdf=lexique.REJECTED_FROM),    # the appendix of rejected glosses
        entry("ate", "variant of ato", two),                           # sends to another entry
        entry("wide", "", two),                                        # no gloss
        entry("tkk", "to plunder", two, status="doubtful"),
        entry("ns", "sacrifice", ("T1",)),                             # in one text only
        entry("wi", "brother", two),                                   # spelled like the copula
        entry("ar (1)", "boy", two), entry("ar (2)", "to take", two),  # one spelling, two words: no key
        entry("mk", "god", two))
    assert [i["word"] for i in lexique.testable(entries, tw)] == ["abr", "mk"]
    abr = lexique.testable(entries, tw)[0]
    assert (abr["meaning"], abr["forms"], abr["texts"], abr["page"]) == ("man", ["abr"], 2, 20)
    assert [i["word"] for i in lexique.testable(entries, tw, min_texts=3)] == []


def test_another_entrys_word_is_not_counted_as_an_ending():
    yer = entry("yer", "milk", ("T1",), variants=["yeri"])[0]
    tw = {"yer": {"T1"}, "yerike": {"T2", "T3"}}
    assert [i["texts"] for i in lexique.testable([yer], tw)] == [3]                    # yeri + ke, in T2 and T3
    yerike = entry("yerike", "begotten")[0]
    assert [i["word"] for i in lexique.testable([yer, yerike], tw)] == ["yerike"]      # yerike is its own entry
    rejected = dict(yerike, page_pdf=lexique.REJECTED_FROM)                            # the appendix owns nothing
    assert [i["word"] for i in lexique.testable([yer, rejected], tw)] == ["yer"]


def test_related_words_give_each_other_away():
    it = lambda word, meaning, *forms: {"word": word, "meaning": meaning, "forms": list(forms)}
    qore = it("qore", "ruler, king", "qore")
    assert lexique.related(it("mk", "god", "mk"), it("mkdi", "goddess", "mkdi"))        # one spelling begins the other
    assert lexique.related(it("qorise", "of the king", "qoreSe", "qores", "qoriSe", "qoris"), qore)
    assert lexique.related(qore, it("qor-o", "it is the qore (predicated form)", "qoro"))   # named, 3 letters shared
    assert lexique.related(it("smlo (1)", "title, 'good man', from mlo", "Smlo"), it("mlo", "good", "mlo"))
    assert not lexique.related(qore, it("nobo", "Nubian, slave of the qore", "nobo"))   # named, nothing shared
    assert not lexique.related(it("abr", "man", "abr"), it("kdi", "woman", "kdi"))


def test_open_task_hides_what_gives_a_target_away():
    item = lambda word, meaning, *forms: {"word": word, "meaning": meaning, "forms": list(forms)}
    items = [item("qore", "ruler", "qore"), item("abr", "man", "abr"),
             item("qorise", "royal", "qores", "qoris"), item("kdi", "woman", "kdi")]
    old = lexique.BLIND, lexique.ROOT, lexique.CORPUS
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "runs/keys").mkdir(parents=True)
        (d / "corpus.jsonl").write_text("".join(json.dumps({"id": f"T{k}", "text": t}) + "\n" for k, t in
                                                enumerate(["qore abr kdi", "qoris abr", "kdi qore"])))
        lexique.BLIND, lexique.ROOT, lexique.CORPUS = d / "blind", d, d / "corpus.jsonl"
        try:
            quiet(lexique.build_open, items, {"qorise", "kdi"}, parts=1)
            task = (d / "blind/N2_open_1/task.md").read_text()
            key = json.loads((d / "runs/keys/lexique_open.json").read_text())
            try:
                quiet(lexique.build_open, items, {"qorise", "kdi"}, parts=1)
                raise AssertionError("build_open() rebuilt a folder that holds a task")
            except SystemExit:
                pass
            assert (d / "blind/N2_open_1/task.md").read_text() == task
        finally:
            lexique.BLIND, lexique.ROOT, lexique.CORPUS = old
    targets, rest = task.split("## Target words")[1].split("## Glossary (known words)")
    glossary, corpus = rest.split("## Corpus")
    assert "- abr (abr): man" in glossary and "qore" not in glossary        # qore would give qorise away
    assert "- qorise (look for: qoris, qores)" in targets and "- kdi (look for: kdi)" in targets   # attested first
    assert "royal" not in targets + glossary and "woman" not in targets + glossary   # no target's meaning is shown
    assert key == {"qorise": "royal", "kdi": "woman"}
    assert sorted(l.split(": ")[1] for l in corpus.strip().split("\n")) == ["kdi qore", "qore abr kdi", "qoris abr"]
    assert "T0" not in corpus and "T1" not in corpus                        # lines carry no text ids


def test_borderline_rows_set_the_ranges():
    rec = lambda word, verdict, why, c=3: {"word": word, "verdict": verdict, "confidence": c, "why": why}
    cor = lambda word, first, any_same, why, c=2: {"word": word, "verdict_first": first, "any_same": any_same,
                                                   "confidence": c, "why": why}
    judge = {"recall": [rec("a", "SAME", "plain", 5),
                        rec("b", "SAME", "Borderline: generic. TYPE if the kin term must be exact."),
                        rec("c", "WRONG", "Borderline: its alternative is Rilly's. SAME if the alternative counts."),
                        rec("d", "TYPE", "A title. SAME if any title counts."),          # not marked borderline
                        rec("e", "UNKNOWN", "said unknown", 1)],
             "corpus": [cor("f", "SAME", True, "Borderline: a title. TYPE (not SAME) if the office must match.", 4),
                        cor("g", "WRONG", True, "Borderline any_same: only the 3rd candidate is the same idea."),
                        cor("h", "TYPE", False, "Borderline: right domain. SAME if the rank is left open.", 3),
                        cor("i", "WRONG", False, "plain")]}
    assert [lexique.alt(r) for r in judge["recall"]] == [None, "TYPE", "SAME", None, None]
    t = lexique.totals(judge)
    assert t["recall"] == {"n": 5, "SAME": 2, "TYPE": 1, "WRONG": 1, "UNKNOWN": 1}
    assert t["recall_same_by_confidence"] == {"4-5": {"SAME": 1, "answers": 1},
                                              "1-3": {"SAME": 1, "answers": 3, "answers_with_unknown": 4}}
    assert t["corpus_first"] == {"n": 4, "SAME": 1, "TYPE": 1, "WRONG": 2}
    assert t["corpus_any_same"] == {"count": 2, "n": 4}
    assert t["corpus_same_by_confidence"] == {"4-5": {"SAME": 1, "answers": 1}, "3": {"SAME": 0, "answers": 1},
                                              "1-2": {"SAME": 0, "answers": 2}}
    assert t["borderline"] == {"recall_words": ["b", "c"], "corpus_words": ["f", "g", "h"],
                               "recall_SAME_range": [1, 3], "corpus_first_SAME_range": [0, 2],
                               "corpus_any_same_range": [0, 3]}
    assert lexique.totals(judge, drop={"a", "f"})["recall"]["n"] == 4
    assert lexique.totals(judge, drop={"a", "f"})["corpus_any_same"] == {"count": 1, "n": 3}


def test_judge_totals_match_their_rows():
    judge = json.load(open(ROOT / "runs/lexique_judge.json"))
    saved, t = judge["totals"], lexique.totals(judge)
    for k in ("recall_words", "corpus_words"):                       # the saved lists are in the judge's order
        saved["borderline"][k] = sorted(saved["borderline"][k])
    assert saved == t
    assert (t["recall"]["SAME"], t["recall"]["n"]) == (28, 68)       # "as judged", REPORT waves 2-3, item 6
    assert (t["corpus_first"]["SAME"], t["corpus_any_same"]["count"], t["corpus_first"]["n"]) == (20, 28, 44)


def test_reported_lexicon_numbers():
    judge = json.load(open(ROOT / "runs/lexique_judge.json"))
    recall = lexique.totals(judge, NOT_TEST_WORDS)
    corpus = lexique.totals(judge, set(NOT_TEST_WORDS) | set(GIVEN_AWAY))
    assert (recall["recall"]["SAME"], recall["recall"]["n"]) == (27, 65)
    assert recall["recall_same_by_confidence"]["4-5"] == {"SAME": 19, "answers": 19}
    assert (corpus["corpus_first"]["SAME"], corpus["corpus_any_same"]["count"], corpus["corpus_first"]["n"]) == \
        (13, 20, 35)
    assert corpus["corpus_same_by_confidence"]["4-5"] == {"SAME": 2, "answers": 2}


def test_judged_names_the_words_the_run_should_not_have_had():
    needs("data/rilly2003", "data/corpus_v2.jsonl")
    wrong, gave, added = quiet(lexique.judged, lexique.load(), lexique.corpus_index()[1])
    assert (wrong, gave, added) == (NOT_TEST_WORDS, GIVEN_AWAY, LEFT_OUT)


def test_skeleton_spells_both_conventions_alike():
    sk = expand.skeleton
    assert sk("woSi Soreyi") == sk("wosi soreyi") == "wesisereyi"     # Millet's S, FHN's s
    assert sk("peseto") == sk("pesto") and sk("xrpxne") == sk("XrpXN")     # the se and ne signs; x and X
    assert sk("atE mXe") == sk("ato mxe")                             # Millet's o is often typed e
    assert sk("qo NAME 12 qowi") == sk("q o RNAME qo wi") == "qe#qewi"     # word division and numerals go
    assert sk("a ... RNAME NAME . b") == "a#b"                        # names and lost signs: one unknown stretch


def test_words_drop_line_numbers_and_marks():
    assert expand.words("(1)wos (12) a?ym tk|l # . .. qo.") == ["wos", "aym", "tk", "l", "qo."]


def test_a_copy_is_present_and_a_new_text_is_not():
    sk, present = expand.skeleton, expand.present
    ref = sk("woSi Soreyi NAME qowi NAME tedxelowi ato mXe pSoxte")
    assert present(sk("wosi soreyi NAME qo wi NAME tedxelo wi ato mxe psoxte"), ref)   # other convention, division
    assert not present(sk("apedemk qore lw amnp tNyidmni pwrite"), ref)
    assert present(sk("tedxelowi"), ref)                    # a label inside a longer text counts as present
    assert not present(sk("tedxelowi apedemk qore lw amnp"), ref)     # under half of its 6-grams
    masked = sk("qo NAME qowi")
    assert present(sk("qo aritene qowi"), masked)           # the masked name stands for any letters
    assert not present(sk("qo aritenelisye qowi"), masked)  # ... but the text must be half the other's letters
    assert not present(sk("qo aritene qowi"), sk("qo qowi"))          # nothing masked: the letters must match


def test_merge_keeps_whole_new_texts_once():
    row = lambda rid, text, partial=False: {"id": rid, "src": "griffith", "text": text, "partial": partial}
    base = [{"id": "T1", "text": "woSi Soreyi NAME qowi NAME tedxelowi ato mXe pSoxte"}]
    griffith = [row("G1", "wosi soreyi NAME qowi NAME tedxelowi ato mxe psoxte"),      # already in the corpus
                row("G2", "apedemk qore lw amnp tNyidmni pwrite"),
                row("G3", "apedemk qore lw amnp tNyidmni pwrite"),                     # repeats G2
                row("G4", "kdi mlo yetmde", partial=True)]
    added, dupes, partial = expand.merge(base, griffith)
    assert [g["id"] for g in added] == ["G2"] and [(g["id"], hit) for g, hit in dupes] == [("G1", "T1"), ("G3", "G2")]
    assert [g["id"] for g in partial] == ["G4"] and not any("partial" in g for g in added + partial)
    assert all("partial" in g for g in griffith)            # the caller's rows are left as they were


def test_griffith_rows_load_as_reported():
    rows = expand.load_griffith()
    assert len(rows) == len({r["id"] for r in rows}) == 152           # REPORT waves 2-3, item 9
    assert sum(r["partial"] for r in rows) == 29
    assert sum(len(r["text"].split()) for r in rows if r["partial"]) == 150
    assert all(r["src"] == "griffith" and r["text"] and not set("()|#?") & set(r["text"]) for r in rows)


def test_reported_expansion_numbers():
    needs("data/corpus_v2.jsonl")
    base = [json.loads(l) for l in (ROOT / "data/corpus_v2.jsonl").read_text().splitlines()]
    added, dupes, partial = expand.merge(base, expand.load_griffith())
    words = lambda rows: sum(len(r["text"].split()) for r in rows)
    assert (len(added), len(dupes), len(partial)) == (86, 37, 29)
    assert (len(base), words(base), len(base) + len(added), words(base) + words(added)) == (662, 18075, 748, 19066)


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")])
