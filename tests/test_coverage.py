"""Checks for the translation coverage map (src/coverage.py).

  python3 -I tests/test_coverage.py

The lexicon and the corpus are local only, so the checks of the method run on a made-up lexicon and made-up
texts; the checks of the reported numbers need the local files and are skipped without them.
"""
import collections, json, shutil, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import coverage as C   # noqa: E402
from local_only import needs, run   # noqa: E402

PAGE = ROOT / "data/discovery/coverage.md"


def raw(headword, meaning="", status="unknown", category="", variants=(), page=10):
    return {"headword": headword, "variants": list(variants), "category": category, "meaning_en": meaning,
            "status": status, "page_pdf": page, "page_printed": page - 2}


RAW = [
    raw("ato", "water; perhaps 'river'", "established", "substantif"),
    raw("mẖe", "abundant", "established", "adjectif"),
    raw("mḫe", "variant of mẖe", "unknown", "adjectif"),
    raw("pqr", "prince", "hypothesis", "titre"),
    raw("aribet", "", "unknown", "titre"),
    raw("Wos", "Isis", "established", "théonyme"),
    raw("-erike-", "begotten by (the father)", "established", "verbe ou substantif"),
    raw("t- (1)", "", "hypothesis", "préfixe verbal (?)"),
    raw("-lo", "a mis-segmentation: the copula -o", "established"),
    raw("-lowi", "a mis-segmentation: the copula -o and -wi", "established"),
    raw("qowi", "'this one is'", "probable", "prédicatif"),
    raw("wi (1)", "brother", "established", "substantif"),
    raw("-wi (5)", "optional particle after the copula", "hypothesis", "particule"),
    raw("yetmde", "nephew, niece", "established", "substantif"),
    raw("old", "a gloss Rilly rejects", "established", "substantif", page=C.L.REJECTED_FROM),
]


def made_up():
    es = C.lexicon(RAW)
    return (es,) + C.index(es)


def answer(word, parts, kind="unknown", confidence=4, gloss=""):
    return {"word": word, "parts": [{"form": f, "entry": e} for f, e in parts], "kind": kind, "gloss": gloss,
            "confidence": confidence, "evidence": "", "recalled": ""}


def test_an_entry_gets_its_level_from_rilly():
    es, words, affixes, heads = made_up()
    level = {h: e["level"] for h, e in heads.items()}
    assert level["ato"] == "meaning" and level["Wos"] == "name" and level["-lo"] == "grammar"
    assert level["pqr"] == "hypothesis"                    # a proposal only
    assert level["aribet"] == "kind" and heads["aribet"]["kind"] == "title"   # no meaning, but a title
    assert level["t- (1)"] == "kind" and heads["t- (1)"]["kind"] == "function word"
    assert heads["-erike-"]["affix"] == "infix" and heads["-erike-"]["kind"] == "verb"
    assert "old" not in heads                              # the appendix of rejected glosses is left out
    assert heads["ato"]["confidence"] == 5 and heads["qowi"]["confidence"] == 4 and heads["pqr"]["confidence"] == 2


def test_an_entry_that_sends_to_another_takes_its_level():
    es, words, affixes, heads = made_up()
    e = heads["mḫe"]
    assert e["level"] == "meaning" and e["meaning"].startswith("abundant") and e["kind"] == "adjective"
    two = C.lexicon(RAW + [raw("mẖe (2)", "a second word", "hypothesis", "substantif")])
    assert {x["headword"]: x for x in two}["mḫe"]["level"] == "kind"     # two entries of that name: no guess


def test_the_lookup():
    es, words, affixes, heads = made_up()
    look = lambda tok, prev="": C.lookup(tok, prev, words, affixes)
    assert look("NAME")["level"] == "name" and look("12")["level"] == "number" and look("at.o")["level"] == "lost"
    g = look("ato")
    assert (g["level"], g["confidence"], g["gloss"]) == ("meaning", 5, "water") and "Rilly 2003, p. 8" in g["source"]
    g = look("yetmdelowi")                                  # a stem of three letters or more with a known ending
    assert g["level"] == "meaning" and [p["form"] for p in g["parts"]] == ["yetmde", "lowi"]
    assert look("atolo")["level"] == "meaning"
    assert look("mxe")["level"] == "meaning"                # x is ḫ: the variant entry
    assert look("pqr")["level"] == "hypothesis" and look("aribet")["level"] == "kind"
    assert look("pqrlo")["level"] == "hypothesis"           # a stem with a proposal takes an ending
    assert look("aribetlo") is None                         # a stem without a meaning does not: the match proves nothing
    assert look("zzz") is None and look("2w") is None       # left to the analysts
    two = C.lexicon(RAW + [raw("ato (2)", "'bread'", "established", "substantif")])
    g = C.lookup("ato", "", *C.index(two)[:2])
    assert (g["gloss"], g["senses"], g["open"]) == ("water / bread", 2, False)      # both entries are named
    # wi alone is the particle, not "brother"; after a word in -lo it is the wi of -lowi
    assert look("wi")["level"] == "hypothesis"
    assert look("wi", "yetmdelo")["level"] == "grammar" and look("wi", "at.lo")["level"] == "hypothesis"
    # an ending of open function does not lower the level, and the gloss says so; an accepted one is not open
    g = look("yetmdewi")
    assert g["level"] == "meaning" and g["open_grammar"] and not look("yetmdelo")["open_grammar"]
    figs = C.figures(C.gloss_texts([{"id": "T1", "text": "yetmdewi yetmdelo ato"}], words, affixes))
    assert figs["all"]["with_open_grammar"] == {"lookup": 1} and figs["all"]["translated"] == 3


def test_a_name_in_griffiths_tables_is_a_name():
    es, words, affixes, heads = made_up()
    printed = [(["tbitolye"], "names table, column A (person 12)", ""), (["mlN"], "Index C", "n. B."),
               (["pelmoS"], "Index C", "title of A"), (["ato", "mXe"], "formula A (table)", "")]
    look = lambda tok: C.lookup(tok, "", words, affixes, printed)
    assert look("tbitolye")["level"] == "name" and "names table" in look("tbitolye")["source"]
    printed.append((["yiboyeqowi"], "names table, column A (person 13)", ""))
    assert (look("tbitolye")["gloss"], look("yiboyeqowi")["gloss"]) == ("Tbitolye", "this is Yiboye")
    assert look("mlN")["level"] == "name" and look("pelmoS") is None       # a title is not a name
    assert look("ato")["level"] == "meaning"                               # the lexicon comes first
    assert C.hints("tbitolyeqowi", printed) == ["names table, column A (person 12): tbitolye"]


def test_an_answer_that_cannot_be_used():
    es, words, affixes, heads = made_up()
    ok = answer("terikelowi", [("t", "t- (1)"), ("erike", "-erike-"), ("lowi", "-lowi")], "filiation word", 5)
    assert C.check(ok, "terikelowi", heads) == ""
    assert "spell" in C.check(answer("terikelowi", [("terike", "-erike-")]), "terikelowi", heads)
    assert "not an entry" in C.check(answer("abc", [("abc", "abc (9)")]), "abc", heads)
    assert "kind" in C.check(answer("abc", [("abc", "?")], kind="thing"), "abc", heads)
    assert "confidence" in C.check(answer("abc", [("abc", "?")], confidence=6), "abc", heads)
    assert C.check(answer("abc", [("abc", "?")]), "abd", heads) and C.check({"word": "abc", "parts": []}, "abc", heads)
    # an answer of the wrong shape is dropped with a reason, not a crash further on
    assert "entry" in C.check(answer("abc", [("abc", ["?"])]), "abc", heads)
    assert "confidence" in C.check(answer("abc", [("abc", "?")], confidence=4.0), "abc", heads)
    assert "confidence" in C.check(answer("abc", [("abc", "?")], confidence=True), "abc", heads)
    assert "kind" in C.check(answer("abc", [("abc", "?")], kind=["title"]), "abc", heads)
    assert "text" in C.check(answer("abc", [("abc", "?")], gloss=5), "abc", heads)
    assert C.check(dict(answer("abc", [("abc", "?")]), gloss=None, recalled=None), "abc", heads) == ""


def test_the_level_of_an_analysed_word():
    es, words, affixes, heads = made_up()
    level = lambda *a, **k: C.settle(answer(*a, **k), heads)
    g = level("terikelowi", [("t", "t- (1)"), ("erike", "-erike-"), ("lowi", "-lowi")], "filiation word", 5)
    assert g["level"] == "meaning" and g["open_grammar"]         # t- of unknown function does not hide "begotten"
    assert level("terikelowi", [("t", "t- (1)"), ("erike", "-erike-"), ("lowi", "-lowi")], "filiation word", 3)["level"] == "hypothesis"
    assert level("tbitolyeqowi", [("tbitolye", "NAME"), ("qowi", "qowi")], "person name")["level"] == "name"
    assert level("zzzlowi", [("zzz", "?"), ("lowi", "-lowi")], "title")["level"] == "kind"
    assert level("zzzlowi", [("zzz", "?"), ("lowi", "-lowi")], "title", 3)["level"] == "unknown"   # an unsure kind
    assert level("zzz", [("zzz", "?")])["level"] == "unknown"
    assert level("pqrlo", [("pqr", "pqr"), ("lo", "-lo")], "title", 5)["level"] == "hypothesis"
    assert level("aribetato", [("aribet", "aribet"), ("ato", "ato")], "two words written as one", 5)["level"] == "kind"
    assert level("etolo", [("eto", "ato"), ("lo", "-lo")], "noun")["variant"]                  # eto is not a spelling of ato
    assert level("lo", [("lo", "-lo")], "function word", 5)["level"] == "grammar"


def packs(folder, a=None, b=None):
    for name, lines in (("A001", a), ("B001", b)):
        if lines is not None:
            d = Path(folder) / name
            d.mkdir()
            (d / "words.jsonl").write_text("".join(json.dumps({"word": w}) + "\n" for w in ("zzzlowi", "tbilo", "qqq")))
            (d / "analysis.jsonl").write_text("".join((l if isinstance(l, str) else json.dumps(l)) + "\n" for l in lines))


def test_two_analysts_and_dropped_answers():
    es, words, affixes, heads = made_up()
    with tempfile.TemporaryDirectory() as d:
        packs(d,
              a=[answer("zzzlowi", [("zzz", "?"), ("lowi", "-lowi")], "title"),
                 answer("tbilo", [("tbi", "NAME"), ("lo", "-lo")], "person name"),
                 "not json", answer("other", [("other", "?")])],
              b=[answer("zzzlowi", [("zzz", "?"), ("lowi", "-lowi")], "title"),
                 answer("tbilo", [("tbilo", "?")]),
                 answer("qqq", [("qq", "?")])])
        got, report = C.analyses(d, heads)
    assert got["zzzlowi"]["level"] == "kind" and "differ" not in got["zzzlowi"] and got["zzzlowi"]["twice"]
    assert got["tbilo"]["level"] == "unknown" and got["tbilo"]["differ"]        # the lower of the two stands
    assert "qqq" not in got                                                     # no usable answer from either
    assert (report["analysed"], report["twice"], report["same_level"], report["differ"]) == (2, 2, 1, ["tbilo"])
    assert report["same_level_and_cut"] == 1 and report["translated_by"] == {"first": 1}
    assert report["same_translated_or_not"] == 1
    assert sorted(why for _, _, why in report["dropped"]) == ["not JSON", "not a word of this pack", "the parts do not spell the word"]
    assert sorted(report["missing"]) == [("A001", "qqq"), ("B001", "qqq")]


def test_what_blocks_a_word():
    es, words, affixes, heads = made_up()
    block = lambda *a, **k: [(b, e is not None) for b, e in C.blockers(C.settle(answer(*a, **k), heads), heads)]
    # a stem without an accepted meaning blocks under its headword, an unknown piece under its letters
    assert block("pqrzzz", [("pqr", "pqr"), ("zzz", "?")], "title", 4) == [("pqr", True), ("zzz", False)]
    # an ending of open function does not lower the level of a word with a known stem (settle), so it blocks
    # nothing there: an unsure cut of known stems blocks under the word's own letters
    assert block("yetmdewi", [("yetmde", "yetmde"), ("wi", "-wi (5)")], "kin term", 4) == []
    assert block("yetmdewi", [("yetmde", "yetmde"), ("wi", "-wi (5)")], "kin term", 3) == [("yetmdewi", False)]
    assert block("tbiwi", [("tbi", "NAME"), ("wi", "-wi (5)")], "person name", 2) == [("tbiwi", False)]
    # a word made of a beginning and an ending only is blocked by the one without an accepted function
    assert block("tlo", [("t", "t- (1)"), ("lo", "-lo")], "function word", 5) == [("t- (1)", True)]
    assert C.blockers(C.lookup("wi", "", words, affixes), heads)[0][0] == "-wi (5)"     # a function word alone
    # the lookup's ending is no word of its own: a function word with a proposal only blocks under its headword
    words, affixes, heads = C.index(C.lexicon(RAW + [raw("eqe", "perhaps 'this'", "hypothesis", "démonstratif")]))
    g = C.lookup("eqelo", "", words, affixes)
    assert g["level"] == "hypothesis" and [(b, e is not None) for b, e in C.blockers(g, heads)] == [("eqe", True)]


def test_the_ranked_list_counts_the_texts_a_piece_blocks():
    es, words, affixes, heads = made_up()
    rows = [{"id": "T1", "text": "ato pqr NAME"}, {"id": "T2", "text": "ato aribet zzz"},
            {"id": "T3", "text": "ato pqrlo at.o"}, {"id": "T4", "text": "ato NAME 12"}, {"id": "T6", "text": "a.b .."}]
    glossed = C.gloss_texts(rows, words, affixes, {"zzz": C.settle(answer("zzz", [("zzz", "?")], "title", 2), heads)})
    ranked, texts_by = C.ranking(glossed, heads)
    by = {r["piece"]: r for r in ranked}
    assert (by["pqr"]["texts"], by["pqr"]["alone"], by["pqr"]["words"], by["pqr"]["kind"]) == (2, 2, 2, "title")
    assert (by["aribet"]["texts"], by["aribet"]["alone"]) == (1, 0) and by["zzz"]["level"] == "unknown"
    assert (by["pqr"]["is"], by["zzz"]["is"]) == ("headword", "letters")
    assert ranked[0]["piece"] == "pqr" and by["pqr"]["forms"] == ["pqr", "pqrlo"]
    # the lost word of T3 is no blocker; T6, all lost, has nothing to read and is not counted complete; the median
    # is that of T2, T3, T1 and T4: 1/3, 1/2, 2/3 and 1 of their legible words translated
    assert abs(texts_by.pop("median") - (1 / 2 + 2 / 3) / 2) < 1e-12
    assert texts_by == {"texts": 5, "legible": 4, "no_blocker": 1, "one_blocker": 2}
    copies = rows + [{"id": "T5", "text": "ato pqr NAME"}]                       # a copy of T1 counts for words only
    again, texts_again = C.ranking(C.gloss_texts(copies, words, affixes), heads)
    pqr = {r["piece"]: r for r in again}["pqr"]
    assert (pqr["texts"], pqr["alone"], pqr["all_texts"], pqr["words"]) == (2, 2, 3, 3) and texts_again["texts"] == 5
    assert C.draft(glossed[1][1]) == "water [title] <zzz>"
    figs = C.figures(glossed)
    assert figs["all"]["words"] == 14 and figs["all"]["translated"] == 7
    assert figs["all"]["levels"]["lost"] == 3 and sum(figs["all"]["levels"].values()) == 14
    assert figs["different words"]["words"] == 10


def test_a_piece_keeps_its_kind_and_its_own_level():
    # a headword without a category takes the kind the analysts named for its words; a headword whose words stand
    # lower than its entry (another piece of them is unknown) keeps its entry's level; letters spelled like a
    # headword are another piece (Rilly's sb is the corpus's Sb, not the se sign's sb)
    es = C.lexicon(RAW + [raw("moke", "", "unknown"), raw("sb", "", "unknown", "substantif")])
    words, affixes, heads = C.index(es)
    analysed = {w: C.settle(a, heads) for w, a in (
        ("mokelowi", answer("mokelowi", [("moke", "moke"), ("lowi", "-lowi")], "kin term", 3)),
        ("pqrzzz", answer("pqrzzz", [("pqr", "pqr"), ("zzz", "?")], "title", 3)),
        ("sb", answer("sb", [("sb", "?")], "noun", 2)),
        ("Sbzz", answer("Sbzz", [("Sb", "sb"), ("zz", "?")], "noun", 2)))}
    rows = [{"id": "T1", "text": "mokelowi pqrzzz"}, {"id": "T2", "text": "sb Sbzz ato"}]
    ranked, _ = C.ranking(C.gloss_texts(rows, words, affixes, analysed), heads)
    by = {(r["piece"], r["is"]): r for r in ranked}
    assert by["moke", "headword"]["kind"] == "kin term" and by["moke", "headword"]["level"] == "unknown"
    assert by["pqr", "headword"]["level"] == "hypothesis" and by["zzz", "letters"]["level"] == "unknown"
    assert by["sb", "headword"]["forms"] == ["Sbzz"] and by["sb", "letters"]["forms"] == ["sb"]
    assert len(ranked) == 6 and C.public_list(ranked).splitlines()[0].split("\t") == list(C.COLUMNS)


def test_near_copies_are_counted_once():
    rows = [{"id": "long", "text": "a b c d e f g h"}, {"id": "copy", "text": "a b c d e f g"},
            {"id": "other", "text": "a b c x y z w"}, {"id": "short", "text": "a b"}, {"id": "same", "text": "a b"}]
    assert [r["id"] for r in C.distinct(rows)] == ["long", "other", "short"]


def test_packs_and_public_list():
    es, words, affixes, heads = made_up()
    rows = [{"id": "T1", "text": "ato zzz qqq"}, {"id": "T2", "text": "zzz pqr"}]
    residue = C.left(rows, words, affixes)
    assert [(w["word"], w["count"], w["texts"]) for w in residue] == [("zzz", 2, 2), ("qqq", 1, 1)]
    assert residue[0]["contexts"] == ["T1: ato [zzz] qqq", "T2: [zzz] pqr"]
    with tempfile.TemporaryDirectory() as d:
        made = C.write_packs(Path(d), residue, es, per=1, again=1)
        assert made == ["A001", "A002", "B001"]
        more = residue + [{"word": "new", "count": 1, "texts": 1, "contexts": [], "griffith": []}]
        assert C.write_packs(Path(d), more, es, per=5, again=1, more=True) == ["A003"]      # only the new word
        assert json.loads((Path(d) / "A003/words.jsonl").read_text())["word"] == "new"
        assert C.write_packs(Path(d), more, es, more=True) == []
        assert (Path(d) / "B001/words.jsonl").read_text() == (Path(d) / "A001/words.jsonl").read_text()
        # a new pack is numbered after the highest one, so a gap in the numbers does not overwrite a pack
        shutil.rmtree(Path(d) / "A002")
        assert C.write_packs(Path(d), more + [dict(more[-1], word="newer")], es, per=5, more=True) == ["A004"]
        assert json.loads((Path(d) / "A003/words.jsonl").read_text())["word"] == "new"
        table = (Path(d) / "A001/lexicon.tsv").read_text().splitlines()
        assert table[0].startswith("headword\t") and len(table) == len(es) + 1
        glossed = C.gloss_texts(rows, words, affixes)
        ranked, texts_by = C.ranking(glossed, heads)
        C.write(glossed, ranked, C.figures(glossed), texts_by, {}, out=Path(d) / "out", public=Path(d) / "public.tsv")
        public = (Path(d) / "public.tsv").read_text()
        assert "prince" not in public and "water" not in public          # no gloss of Rilly's in the public list
        assert public.splitlines()[1].split("\t")[:6] == ["zzz", "letters", "unknown", "unknown", "2", "0"]
        assert all(len(l.split("\t")) == len(C.COLUMNS) for l in public.splitlines())
        first = json.loads((Path(d) / "out/glosses.jsonl").read_text().splitlines()[0])
        assert first["draft"] == "water <zzz> <qqq>" and first["glosses"][0]["source"].startswith("Rilly 2003")


def test_the_gloss_line_is_the_first_clause():
    assert C.short("'ruler', 'sovereign'; can apply to ruling women") == "ruler, sovereign"
    assert C.short("water, and perhaps 'river' or 'Nile'") == "water"
    assert C.short('"abundant" (the supposed meaning)') == "abundant"
    assert C.short("a mis-segmentation: the copula -o in -l-o") == "the copula -o in -l-o"
    assert C.short("'viceroy', probably borrowed from Egyptian") == "viceroy"
    assert C.short("the viceroy's office") == "the viceroy's office" and C.short("") == ""
    assert C.short("ḫ(re) + lẖ + l 'a great meal', in benediction formula D1") == "a great meal"
    # 48 letters at most, cut at a word's end
    assert C.short("administrative title tied to the viceroy's office in the north") == "administrative title tied to the viceroy's"


# Rilly's own list of words with a translation, in his 2016 overview ("Meroitic", UCLA Encyclopedia of Egyptology,
# section Lexicon, https://escholarship.org/uc/item/3128r3sw): a source later than the lexicon and independent of our
# typing of it. The five that the lexicon does not hold at an accepted level are what the page reports.
RILLY_2016 = ["abr", "asr", "at", "ato", "kdi", "kdise", "kdite", "ked", "l", "lẖ", "mẖe", "mlo", "mte", "sem", "ste",
              "st", "tre", "wide", "ar", "are", "dm", "dime", "ḫre", "ḫlbi", "pwrite", "tke", "wle", "yer", "qore",
              "ktke", "pqr", "nob", "teneke", "ant", "apote", "pelmos", "ssor", "tewiseti", "nbr"]
NOT_ACCEPTED_IN_THE_LEXICON = ["asr", "wide", "ḫre", "pqr", "nbr"]
LOCAL = ("data/rilly2003", "data/corpus_v5.jsonl", "data/sources")


def test_the_lexicons_levels_agree_with_rillys_2016_list():
    needs("data/rilly2003")
    words, affixes, heads = C.index(C.lexicon())
    low = []
    for w in RILLY_2016:
        owners = [e for f in C.L.corpus_spellings(w) for e in words.get(f, []) + affixes.get(f, [])]
        if not any(e["level"] in C.TRANSLATED for e in owners):
            low.append(w)
    assert low == NOT_ACCEPTED_IN_THE_LEXICON and len(RILLY_2016) == 39


def built(heads_up=()):
    """The lexicon, the corpus and the analysts' answers, glossed; heads_up names entries to count as accepted."""
    needs(*LOCAL)
    if not (C.OUT / "packs").is_dir():
        from local_only import Skip
        raise Skip("needs the analysts' answers in data/sources/coverage/packs")
    es = C.lexicon()
    for e in es:
        if e["headword"] in heads_up:
            e.update(level="meaning", confidence=4)
    words, affixes, heads = C.index(sorted(es, key=lambda e: (C.RANK[e["level"]], -e["confidence"])))
    rows = C.texts()
    analysed, report = C.analyses(C.OUT / "packs", heads)
    glossed = C.gloss_texts(rows, words, affixes, analysed)
    return rows, words, affixes, heads, report, glossed


def page_tables():
    """The tables of data/discovery/coverage.md, {header: [rows]}, each row its cells without marks of emphasis."""
    tables, rows = {}, None
    for line in PAGE.read_text().splitlines() + [""]:
        if line.startswith("|"):
            cells = tuple(c.strip().strip("*`").strip() for c in line.strip().strip("|").split("|"))
            if rows is None:
                head, rows = cells, []
            elif not all(set(c) <= set("-:") for c in cells):
                rows.append(cells)
        elif rows is not None:
            tables[head], rows = rows, None
    return tables


def share(n, total):
    return f"{n:,} ({n / total:.1%})"


def test_reported_coverage():
    rows, words, affixes, heads, report, glossed = built()
    first = C.figures(C.gloss_texts(rows, words, affixes))["all"]
    assert (first["words"], first["translated"]) == (21977, 11374)                 # the lookup alone: 51.8%
    assert len(C.left(rows, words, affixes)) == 1887
    f = C.figures(glossed)
    a, once = f["all"], f["near-copies counted once"]
    assert (a["texts"], a["words"], a["translated"]) == (899, 21977, 13292)        # 60.5%
    assert a["levels"] == {"meaning": 6955, "grammar": 1968, "name": 4106, "number": 263, "hypothesis": 3704,
                           "kind": 2099, "unknown": 2620, "lost": 262}
    assert a["by"] == {"lookup": 11374, "analyst": 1918}
    assert (a["translated_on_a_choice"], a["title_or_epithet_only"], a["by_one_analyst"], a["by_a_spelling_variant"],
            a["with_open_grammar"]) == (1376, 995, 464, 694, {"analyst": 840, "lookup": 70})
    assert (once["texts"], once["words"], once["translated"]) == (608, 8786, 5266)  # 59.9%
    assert once["levels"] == {"meaning": 2720, "grammar": 1013, "name": 1390, "number": 143, "hypothesis": 1424,
                              "kind": 669, "unknown": 1165, "lost": 262}
    part = lambda name: (f[name]["texts"], f[name]["words"], f[name]["translated"])
    assert part("the older corpus (names masked)") == (662, 18075, 10719)
    assert part("Karanog and Shablul (Griffith 1911)") == (151, 2911, 2158)
    assert part("Griffith's other volumes") == (86, 991, 415)
    assert (f["different words"]["words"], f["different words"]["translated"]) == (3160, 1105)
    assert (report["analysed"], report["twice"], report["same_level"], report["same_level_and_cut"]) == (1887, 230, 194, 178)
    assert report["translated_by"] == {"first": 66, "second": 62, "both": 58} and report["same_translated_or_not"] == 218
    assert report["dropped"] == [] and report["missing"] == []
    # the page's two tables of section 1 are these figures
    t = page_tables()
    levels = {r[0]: r[2:] for r in t["Level", "What it means", "All 899 texts", "Near-copies counted once"]}
    for l in C.LEVELS:
        assert levels[l] == (share(a["levels"][l], a["words"]), share(once["levels"][l], once["words"])), l
    assert levels["translated"] == (share(a["translated"], a["words"]), share(once["translated"], once["words"]))
    assert levels[""] == (f"{a['words']:,}", f"{once['words']:,}")
    groups = {"The older corpus (Otten's, names masked)": "the older corpus (names masked)",
              "Karanòg and Shablûl (Griffith 1911)": "Karanog and Shablul (Griffith 1911)",
              "Griffith's other volumes": "Griffith's other volumes"}
    shown = t["Part", "Texts", "Words", "Translated"]
    assert [r[0] for r in shown] == list(groups)
    for r in shown:
        g = f[groups[r[0]]]
        assert r[1:] == (f"{g['texts']:,}", f"{g['words']:,}", share(g["translated"], g["words"])), r
    # one family of near-copies in the older corpus: 86 texts and 6,284 of its 18,075 words (section 3)
    family = [r for r in rows if "aribet yete kemxr yetmdelowi" in r["text"]]
    assert (len(family), sum(len(r["text"].split()) for r in family)) == (86, 6284)


def test_reported_ranking():
    rows, words, affixes, heads, report, glossed = built()
    ranked, texts_by = C.ranking(glossed, heads)
    assert f"{texts_by.pop('median'):.1%}" == "68.8%"
    assert texts_by == {"texts": 608, "legible": 605, "no_blocker": 82, "one_blocker": 124}
    assert len(ranked) == 1336 and sum(r["is"] == "headword" for r in ranked) == 302
    assert [r["piece"] for r in ranked[:5]] == ["ḫr", "ẖol", "ye- (2)", "pqr", "-wi (5)"]
    level = lambda is_, l: sum(r["is"] == is_ and r["level"] == l for r in ranked)
    assert [level("headword", l) for l in ("hypothesis", "kind", "unknown")] == [126, 157, 19]
    assert [level("letters", l) for l in ("hypothesis", "kind", "unknown")] == [257, 0, 777]
    kinds = [r for r in ranked if r["kind"] != "unknown"]
    assert (len(kinds), sum(r["level"] == "unknown" for r in kinds), sum(r["kind"] != "unknown" for r in ranked[:30])) == (670, 144, 29)
    assert (sum(r["texts"] >= 5 for r in ranked), sum(r["texts"] <= 1 for r in ranked), min(r["texts"] for r in ranked)) == (96, 995, 1)
    # the pieces without a kind stand mostly in a single text, about half of those in the three royal texts
    where = collections.defaultdict(set)
    for t, gs in glossed:
        for g in gs:
            for b, e in C.blockers(g, heads):
                where[b, "headword" if e is not None else "letters"].add(t["id"])
    royal = {r["id"] for r in rows if r["src"] == "narrative"}
    assert royal == {"tanyidamani", "hamadab", "kharamadoye"}
    no_kind = [r for r in ranked if r["kind"] == "unknown"]
    one = [r for r in no_kind if r["all_texts"] == 1]
    assert all(len(where[r["piece"], r["is"]]) == r["all_texts"] for r in ranked)
    assert (len(no_kind), len(one), sum(where[r["piece"], r["is"]] <= royal for r in one)) == (666, 539, 256)
    by = {(r["piece"], r["is"]): r for r in ranked}
    assert (by["ḫr", "headword"]["texts"], by["ḫr", "headword"]["alone"], by["ḫr", "headword"]["words"]) == (116, 11, 183)
    assert by["moke", "headword"]["kind"] == "kin term" and by["moke", "headword"]["alone"] == 11
    # section 2's table: the first twenty pieces that are not names or function words, as the list has them
    table = page_tables()["Piece", "Headword or letters", "Kind", "Level", "Texts", "Alone", "Words", "Spellings"]
    first = [r for r in ranked if r["kind"] not in C.NAME_KINDS + ("function word",)][:len(table)]
    assert len(table) == 20 and [tuple(row) for row in table] == [
        (r["piece"], r["is"], r["kind"], r["level"], str(r["texts"]), str(r["alone"]), str(r["words"]), " ".join(r["forms"][:3]))
        for r in first]
    # the public list is the ranked list as the script writes it, and holds no gloss
    assert C.PUBLIC.read_text() == C.public_list(ranked)
    # every word of every text has a gloss, a level, a confidence and a source in the local file, and a draft line
    needs("data/sources/coverage/glosses.jsonl")
    lines = (C.OUT / "glosses.jsonl").read_text().splitlines()
    assert len(lines) == 899
    for l in lines:
        t = json.loads(l)
        assert len(t["glosses"]) == len(t["text"].split()) and t["draft"]
        assert all(g["level"] in C.LEVELS and g["source"] and g["gloss"] and type(g["confidence"]) is int for g in t["glosses"])
    # the example of section 3 is the gloss file's Kar. 12
    kar12 = next(json.loads(l) for l in lines if json.loads(l)["id"] == "G-karanog-12")
    example = page_tables()["Word", "Level", "Gloss"]
    assert [tuple(r) for r in example] == [(g["form"], g["level"], g["gloss"]) for g in kar12["glosses"][:len(example)]]
    assert f"({kar12['translated']} of its {kar12['words']} words are translated)" in PAGE.read_text()


def test_reported_check_against_rillys_2016_list():
    # section 4: counting as accepted the four entries the lexicon holds as proposals and Rilly's 2016 list
    # translates (pqr, wide, nbr, and sr with asr, both spelled aSr) moves 186 words, to 61.3%
    f = C.figures(built()[-1])["all"]
    up = C.figures(built(heads_up=("pqr", "wide", "nbr", "sr", "asr"))[-1])["all"]
    assert (up["translated"] - f["translated"], f"{up['translated'] / up['words']:.1%}") == (186, "61.3%")


def test_the_brief_names_every_kind():
    brief = C.BRIEF.read_text()
    assert all(f"`{k}`" in brief for k in C.KINDS)


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
