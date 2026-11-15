"""Checks for the recurring open words (src/recurring.py, data/discovery/recurring_words.md).

  python3 -I tests/test_recurring.py

The map, the lexicon of 2003, the source texts and the agents' answers are local only: the checks of the method
run on made-up items, places and answers; the checks of the reported numbers read the public figures file, compare
the page with it, and compare it with a count from the local files where those are present.
"""
import contextlib
import io
import json
import random
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import recurring as W                # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/recurring_words.md"
LOCAL = "data/sources/recurring"


def g(form, level, gloss="", parts=None):
    return {"form": form, "level": level, "gloss": gloss, "parts": parts if parts is not None else [{"form": form, "entry": form}]}


def lines(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join((r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)) + "\n" for r in rows), encoding="utf-8")


def figs():
    return json.loads(W.PUBLIC.read_text(encoding="utf-8"))


def page():
    return " ".join(PAGE.read_text(encoding="utf-8").split())


def between(text, start, end):
    assert text.count(start) == 1, start
    i = text.index(start)
    return text[i: text.index(end, i + len(start))]


# ------------------------------------------------------------------------------------------------- the items

def test_a_spelling_goes_to_its_first_unsure_stem():
    lex = {"ḫr": {"status": "hypothesis"}, "ps-": {"status": "hypothesis"}, "-kete": {"status": "established"},
           "ato": {"status": "established"}, "mlo": {"status": "probable"}}
    assert W.key_of("pSxrkete", ["ps-", "ḫr", "-kete"], lex) == ("ḫr", "stem")
    # a sure stem is passed over for an unsure one after it, and taken when there is no other
    assert W.key_of("atoxr", ["ato", "ḫr"], lex) == ("ḫr", "stem")
    assert W.key_of("atomlo", ["ato", "mlo"], lex) == ("ato", "stem, sure in the lexicon")
    # no stem: the first unsure affix, then the first affix, then the spelling itself
    assert W.key_of("pSkete", ["-kete", "ps-"], lex) == ("ps-", "affix")
    assert W.key_of("kete", ["-kete"], lex) == ("-kete", "affix, sure in the lexicon")
    assert W.key_of("al", ["not an entry"], lex) == ("al", "not in the lexicon")


def test_the_items_hold_every_place_of_an_open_spelling_in_three_texts():
    def text(*forms):
        return [g(f, "meaning" if f in ("ato", "wos") else "unknown", "water" if f == "ato" else "") for f in forms]
    gl = {"T1": text("wos", "al", "ato"), "T2": text("al", "ato"), "T3": text("ato", "al", "al"), "T4": text("bo", "ato")}
    rows = {t: {"site": "Faras", "kind": "funerary"} for t in gl}
    out = W.items_of(gl, rows, {})
    assert [it["item"] for it in out] == ["al"]                      # `bo` stands in one text, `ato` is read
    it = out[0]
    assert (it["texts"], it["uses"]) == (3, 4) and it["forms"][0]["level"] == "unknown"
    assert [(p["text"], p["n"]) for p in it["places"]] == [("T1", 2), ("T2", 1), ("T3", 2), ("T3", 3)]
    assert it["places"][0]["words"] == "wos **al** ato"
    # two words of the same spelling in one window: only the place's own word is in bold
    assert it["places"][2]["words"] == "ato **al** al" and it["places"][3]["words"] == "ato al **al**"


def test_the_dossier_shows_one_place_a_text_first():
    places = [{"text": t} for t in "AABBBCD"]
    assert [p["text"] for p in W.spread(places, 4)] == ["A", "B", "C", "D"]
    assert len(W.spread(places, 10)) == 7
    assert [p["text"] for p in W.spread(places, 6)] == ["A", "B", "C", "D", "A", "B"]


def test_every_item_is_in_one_batch_only():
    used = [k for ks in W.BATCHES.values() for k in ks]
    assert len(used) == len(set(used))


# ------------------------------------------------------------------------------------------------ the quotes

def test_a_quote_counts_only_when_it_stands_in_the_file():
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "pages.txt"
        f.write_text("=== page 7 ===\nThe verb   means\nto eat, he says at the\n=== page 8 ===\nend of the page.\n", encoding="utf-8")
        W._pages.clear()
        assert W.find("the verb means to eat", str(f)) == (False, None)            # the case differs
        assert W.find("The verb means to eat", str(f)) == (True, 7)                # line breaks and runs of spaces
        assert W.find("says at the end of the page", str(f)) == (True, 7)          # over one page break
        assert W.find("to eat", str(f)) == (False, None)                           # under three words
        assert W.find("The verb means to drink", str(f)) == (False, None)
        assert W.find("The verb means to eat", str(Path(d) / "absent.txt")) == (False, None)
        row = {"statements": [{"source": "S", "file": str(f), "page": 3, "quote": "The verb means\nto eat", "says": "x", "stance": "sure"},
                              {"source": "S", "file": str(f), "page": 7, "quote": "not in the file at all", "says": "y", "stance": "accepts"}]}
        kept, c = W.checked_of(row)
        assert [s["quote"] for s in kept["statements"]] == ["The verb means to eat"]
        # the page is the file's, not the reader's; a stance outside the list is "mentions"
        assert kept["statements"][0]["page"] == 7 and kept["statements"][0]["stance"] == "mentions"
        assert (c["statements"], c["quote_found"], c["quote_not_found"], c["page_corrected"]) == (2, 1, 1, 1)
        W._pages.clear()


def test_the_class_follows_the_checked_statements():
    def e(piece="", *st):
        return {"piece": piece, "statements": [{"source": s, "stance": x} for s, x in st]}
    assert W.class_of(e("", ("Rilly 2021", "accepts")))[0] == "A"
    assert W.class_of(e("a piece of woSi", ("Rilly 2016", "probable")))[0] == "A"
    # a proposal of the later source, or a firm statement of an older one, is not class A
    assert W.class_of(e("a piece of woSi", ("Rilly 2021", "proposes"), ("Rilly 2003", "accepts")))[0] == "B"
    assert W.class_of(e("", ("Millet 2005", "accepts")))[0] == "C"
    assert W.class_of(e())[0] == "C"


# --------------------------------------------------------------------------------------------- class A, twice

def test_class_a_needs_both_readers_firm_on_one_source():
    a = {"stance": "accepts", "source": "Rilly 2021", "meaning": "verb stem 'eat'"}
    assert W.stated(a, {"stance": "probable", "source": "Rilly 2021", "meaning": "to eat, to feed"}) == "stated"
    assert W.stated(a, {"stance": "proposes", "source": "Rilly 2021", "meaning": "to eat"}) == "not stated firmly"
    assert W.stated(a, {"stance": "accepts", "source": "Rilly 2016", "meaning": "to eat"}) == "not stated firmly"
    assert W.stated(a, {"stance": "accepts", "source": "Rilly 2021", "meaning": "to drink"}) == "stated, the meanings differ"
    assert W.stated({"stance": "none", "source": "Rilly 2021", "meaning": ""}, {"stance": "none", "source": "Rilly 2021", "meaning": ""}) == "not stated firmly"


def test_the_cover_is_the_lower_of_the_two_answers():
    forms = [{"form": "wi", "uses": 10}, {"form": "wide", "uses": 4}, {"form": "qeswi", "uses": 5}, {"form": "w", "uses": 2}]
    a = {"covers": {"wi": "all", "wide": "some", "qeswi": "all"}}
    b = {"covers": {"wi": "all", "wide": "all", "qeswi": "none", "w": "all"}}
    assert W.covered(forms, a, b) == {"all": 10, "some": 4, "none": 5, "not said": 2}


# ---------------------------------------------------------------------------------------------- the place pass

def test_packs_keep_an_item_whole_or_cut_it_into_runs():
    its = {k: {"item": k, "uses": n, "places": [None] * n} for k, n in (("big", 23), ("b", 6), ("c", 5), ("d", 4))}
    packs = W.place_groups(its, size=10)
    assert packs == [[["big", 0, 10]], [["big", 10, 20]], [["big", 20, 23]], [["b", 0, 6], ["d", 0, 4]], [["c", 0, 5]]] or \
        packs == [[["big", 0, 10]], [["big", 10, 20]], [["big", 20, 23]], [["b", 0, 6]], [["c", 0, 5], ["d", 0, 4]]]
    seen = [(k, i) for p in packs for k, lo, hi in p for i in range(lo, hi)]
    assert len(seen) == len(set(seen)) == 38 and all(sum(hi - lo for _, lo, hi in p) <= 10 for p in packs)


def test_a_place_counts_only_where_both_checkers_agree():
    def c(case, whole=""):
        return {"case": case, "whole": whole}
    assert W.place_verdict(c("stated"), c("stated"), True) == "stated"
    assert W.place_verdict(c("stated"), c("stated"), False) == "not agreed"       # the item missed class A's bar
    assert W.place_verdict(c("stated"), c("piece", "woSi"), True) == "not agreed"
    assert W.place_verdict(c("piece", "wo Si"), c("piece", "wo-Si"), True) == "piece"
    assert W.place_verdict(c("piece", "woSi"), c("piece", "woS"), True) == "not agreed"
    assert W.place_verdict(c("piece"), c("piece"), True) == "not agreed"          # no whole word named
    assert W.place_verdict(c("open"), c("open"), False) == "open"
    assert W.place_verdict(c("unclear"), c("unclear"), False) == "unclear"
    assert W.place_verdict(c("open"), None, False) == "not answered by both"


def test_kappa():
    assert W.kappa([]) is None
    assert W.kappa([("a", "a"), ("b", "b"), ("a", "a")]) == 1.0
    assert W.kappa([("a", "a")] * 4) == 1.0                              # one case only: no chance to differ
    assert abs(W.kappa([("a", "a"), ("a", "b"), ("b", "a"), ("b", "b")])) < 1e-9
    assert round(W.kappa([("a", "a")] * 8 + [("b", "b")] * 8 + [("a", "b")] * 2 + [("b", "a")] * 2), 4) == 0.6


def test_a_checkers_file_counts_only_for_its_own_pack():
    groups = [[["wi", 0, 2]], [["wi", 2, 3], ["al", 0, 1]]]
    with tempfile.TemporaryDirectory() as d:
        lines(Path(d) / "P01.jsonl", [{"item": "wi", "place": 1, "case": "open"}, "not json",
                                       {"item": "wi", "place": 1, "case": "stated"},        # a second line for a place
                                       {"item": "wi", "place": 3, "case": "open"},          # a place of pack 2
                                       {"item": "wi", "place": 2, "case": "maybe"}])        # no such case
        lines(Path(d) / "P02.jsonl", [{"item": "al", "place": 1, "case": "piece", "whole": "alo"},
                                       {"item": "wi", "place": "3", "case": "open"}])       # the place is not a number
        got = W.place_answers(Path(d), groups)
        assert {k: v["case"] for k, v in got.items()} == {("wi", 1): "open", ("al", 1): "piece"}


def test_the_pass_is_counted_place_by_place():
    its = {"wi": {"places": [{"text": "T1", "n": 1, "form": "wi"}, {"text": "T2", "n": 4, "form": "wi"}]},
           "wo-": {"places": [{"text": "T1", "n": 2, "form": "wo"}]}}
    classes = {"wi": W.CLASSES["A"], "wo-": W.CLASSES["B"]}
    verified = {"wi": {"verdict": "stated", "one": {"meaning": "emphatic particle"}}}
    one = {("wi", 1): {"case": "stated"}, ("wi", 2): {"case": "open"}, ("wo-", 1): {"case": "piece", "whole": "wo Si", "meaning": "Isis"}}
    two = {("wi", 1): {"case": "stated"}, ("wi", 2): {"case": "unclear"}, ("wo-", 1): {"case": "piece", "whole": "woSi"}}
    rows, pairs = W.place_rows(its, classes, verified, one, two)
    assert [(r["item"], r["place"], r["class"], r["verdict"], r["whole"], r["meaning"]) for r in rows] == [
        ("wi", 1, "A", "stated", "", "emphatic particle"), ("wi", 2, "A", "not agreed", "", ""), ("wo-", 1, "B", "piece", "woSi", "Isis")]
    assert len(pairs) == 3
    assert W.open_places([{"item": "al", "place": n, "verdict": "open"} for n in (1, 2, 5)] +
                         [{"item": "wi", "place": 1, "verdict": "open"}, {"item": "al", "place": 3, "verdict": "piece"}]) == {"al": [1, 2, 5]}


def test_the_pass_is_taken_only_when_both_checkers_answered_every_place():
    rows = [{"class": "A", "verdict": "open"}, {"class": "B", "verdict": "piece"}, {"class": "B", "verdict": "not answered by both"}]
    pairs = [("open", "open"), ("piece", "piece")]
    s = W.place_summary(rows, pairs)
    assert s["kappa"] == 1.0 and not s["taken"]                          # agreement is perfect, but a place lacks an answer
    assert W.place_summary(rows[:2], pairs)["taken"]
    assert not W.place_summary(rows[:2], [("open", "piece"), ("piece", "open")])["taken"]       # kappa under the bar
    assert s["by class"] == {"A": {"open": 1}, "B": {"piece": 1, "not answered by both": 1}} and s["answered by both"] == 2


def test_a_step_never_writes_its_packs_again_once_an_agent_has_answered():
    steps = {"batches": "lit/answers", "verify-packs": "lit/verify/answers2", "place-packs": "places/answers1",
             "cand-packs": "choice/cand2", "choice-packs": "choice/reader5"}
    old = W.OUT
    try:
        for step, folder in steps.items():
            for writer in (step, "items"):
                with tempfile.TemporaryDirectory() as d:
                    W.OUT = Path(d)
                    lines(W.OUT / folder / "X1.jsonl", [{"item": "x"}])
                    try:
                        W.COMMANDS[writer]()
                        raise AssertionError(f"{writer} wrote with answers in {folder}")
                    except SystemExit as e:
                        assert "not writing" in str(e) and folder in str(e), e
        with tempfile.TemporaryDirectory() as d:                         # answers of a later step do not stop an earlier one
            W.OUT = Path(d)
            lines(W.OUT / "places" / "answers1" / "P01.jsonl", [{"item": "x"}])
            W.not_again("verify-packs")
    finally:
        W.OUT = old


def test_an_answer_counts_only_in_the_file_of_its_own_pack():
    """The literature pass, class A and step 1 of the test read a line only from the file of the pack or batch that
    holds its item."""
    old = W.OUT
    try:
        with tempfile.TemporaryDirectory() as d:
            W.OUT = Path(d)
            first, second = list(W.BATCHES)[:2]
            k = W.BATCHES[first][0]
            lines(W.OUT / "lit" / "answers" / f"{second}.jsonl", [{"item": k, "statements": [], "piece": "a piece"}])
            with contextlib.redirect_stdout(io.StringIO()):
                W.quotes()
            assert k not in W.read("lit/checked.json") and W.read("lit/counts.json")["items_not_answered"] == sum(map(len, W.BATCHES.values()))
            item = {"forms": [{"form": "x", "uses": 3}], "uses": 3, "places": [{"text": "T", "n": n} for n in (1, 2, 3)]}
            W.write("items.json", [dict(item, item="x"), dict(item, item="y")])
            W.write("lit/verify/groups.json", [["x"], ["y"]])
            line = {"item": "x", "meaning": "to eat", "source": "Rilly 2021", "page": 1, "stance": "accepts", "covers": {"x": "all"}}
            for v in (1, 2):
                lines(W.OUT / "lit" / "verify" / f"answers{v}" / "A1.jsonl", [line] if v == 1 else [])
                lines(W.OUT / "lit" / "verify" / f"answers{v}" / "A2.jsonl", [line] if v == 2 else [])      # x stands in pack 1
            with contextlib.redirect_stdout(io.StringIO()):
                W.verify()
            assert W.read("lit/verify/result.json") == {}
            rows = [{"item": i, "place": n, "verdict": "open"} for i in ("x", "y") for n in (1, 2, 3)]
            W.write("places/result.json", {"taken": True, "rows": rows})
            W.write("choice/cand_groups.json", [["x"], ["y"]])
            cand = {"item": "x", "name": "no", "candidates": [{"meaning": "to eat", "kind": "verb"}]}
            lines(W.OUT / "choice" / "cand1" / "C1.jsonl", [cand])
            lines(W.OUT / "choice" / "cand2" / "C2.jsonl", [cand])
            with contextlib.redirect_stdout(io.StringIO()):
                W.cands()
            assert W.read("choice/candidates.json") == {}
    finally:
        W.OUT = old


def test_why_an_open_item_stays_out_of_the_choice():
    def c(*kinds, name="", meanings=None):
        ms = meanings or [f"m{i}" for i in range(len(kinds))]
        return {"name": name, "candidates": [{"meaning": m, "kind": k} for m, k in zip(ms, kinds)]}
    assert W.left_out(c()) == "no candidate kept"
    assert W.left_out(c("noun", name="place")) == "a name by the sources"
    assert W.left_out(c("function word", "noun")) == "first candidate a function word"
    assert W.left_out(c("numeral")) == "first candidate a numeral"
    assert W.left_out(c("title", meanings=["ate of Primis"])) == "no candidate left after the removals"
    assert W.left_out(c("noun", "function word")) is None


# ------------------------------------------------------------------------------------------ the choice, step 1

def test_a_candidate_is_kept_only_when_both_readers_list_it():
    a = {"name": "no", "name_stance": "none", "candidates": [{"meaning": "notable", "kind": "title", "source": "Rilly 2003", "stance": "proposes"},
                                                             {"meaning": "citizen", "kind": "title", "source": "Hofmann", "stance": "proposes"},
                                                             "not a candidate", {"meaning": "the", "kind": "noun"}]}
    b = {"name": "no", "name_stance": "none", "candidates": [{"meaning": "a notable person"}, {"meaning": "good of repute"}]}
    m = W.both_list(a, b)
    assert [(c["meaning"], c["source"], c["second"]) for c in m["candidates"]] == [("notable", "Rilly 2003", "a notable person")]
    assert m["name"] == "" and W.both_list(a, None) == {"candidates": [], "name": ""}
    # a name needs both readers, the same kind of name, and a firm stance from each
    n = {"name": "place", "name_stance": "accepts", "candidates": []}
    assert W.both_list(n, {"name": "place", "name_stance": "probable", "candidates": []})["name"] == "place"
    assert W.both_list(n, {"name": "god", "name_stance": "accepts", "candidates": []})["name"] == ""
    assert W.both_list(n, {"name": "place", "name_stance": "proposes", "candidates": []})["name"] == ""
    assert W.both_list({"name": "epithet", "name_stance": "accepts"}, {"name": "epithet", "name_stance": "accepts"})["name"] == ""


def test_the_candidates_are_distinct_and_translated():
    assert W.distinct(["brother", "his brother", "sister"]) == ["brother", "sister"]
    assert W.distinct(["made by", "written by", "made"]) == ["made by", "written by"]
    assert W.distinct(["mother's kin", "direct descendant", "mother's brother"]) == ["mother's kin", "direct descendant", "mother's brother"]
    assert W.distinct(["great womnise", "high priest of Amun"]) == ["high priest of Amun"]
    assert W.distinct(["ate of Primis"]) == []


# ------------------------------------------------------------------------------------------ the choice, step 2

def test_the_options_are_four_of_one_kind_without_a_shared_word():
    for seed in range(40):
        rng = random.Random(seed)
        opts = W.fill(["to give"], "verb", rng)
        assert len(opts) == len(set(opts)) == 4 and opts[0] == "to give"
        assert all(dict(W.ACCEPTED.values())[m] == "verb" for m in opts)
        for i, m in enumerate(opts):
            assert not any(W.content(m) & W.content(o) for o in opts[:i]), opts
        # the meaning not offered: neither it nor a wording that shares a word with it
        absent = W.fill([], "noun", random.Random(seed), avoid="land, province")
        assert len(absent) == 4 and not any(W.content(m) & {"land", "province"} for m in absent)
        # a kind with too few meanings is filled from the others, its own first
        adj = W.fill(["shining"], "adjective", random.Random(seed))
        assert len(adj) == 4 and all(dict(W.ACCEPTED.values())[m] == "adjective" for m in adj[1:])
        short = W.fill([], "adjective", random.Random(seed), avoid="good")
        assert len(short) == 4 and [dict(W.ACCEPTED.values())[m] == "adjective" for m in short] == [True, True, True, False]


def test_the_accepted_words_are_not_the_open_words():
    # `ato` is also the entry of a recurring item (a spelling of it the map holds open); the test takes only the
    # places the map reads, and that item's own places were all "stated", so it was no open word of the test
    assert set(W.ACCEPTED) & {k for ks in W.BATCHES.values() for k in ks} == {"ato"}
    assert not any(r["sort"] == "open" and r["entry"] in W.ACCEPTED for r in figs()["choice"]["rows"])
    kinds = {k for _, k in W.ACCEPTED.values()}
    assert kinds == set(W.KINDS)
    labels = [m for m, _ in W.ACCEPTED.values()]
    assert len(labels) == len(set(labels))


def test_a_reader_never_sees_a_spelling():
    hidden = {"qore"}
    assert W.blind_reading(g("qorelo", "meaning", "ruler (with the copula)", [{"form": "qore", "entry": "qore"}, {"form": "lo", "entry": "ending"}]), hidden) == "[a word of this test]"
    assert W.blind_reading(g("ato", "meaning", "water"), hidden) == "water"
    assert W.blind_reading(g("x..y", "lost", "<x..y>"), hidden) == "[signs lost]"
    assert W.blind_reading(g("al", "unknown", "?"), hidden) == "[?]"
    assert W.blind_reading(g("al", "unknown", ""), hidden) == "[?]"
    assert W.blind_reading(g("kttre", "kind", "[title]"), hidden) == "[title]"
    assert W.blind_reading(g("mlowi", "hypothesis", "health"), hidden) == "health (?)"
    assert W.blind_reading(g("mlowi", "hypothesis", "health (?)"), hidden) == "health (?)"
    assert W.blind_reading(g("Tneyi", "name", "NAME"), hidden) == "(a name)"
    # what stands in round brackets is cut: such remarks name spellings and guesses
    assert W.blind_reading(g("pXrs", "hypothesis", "it is (the notable) in Faras"), hidden) == "it is in Faras (?)"
    assert W.blind_reading(g("Si", "name", "(part of woSi)"), hidden) == "[?]"
    assert W.strip_remarks("may (they) give him to drink") == "may give him to drink"
    # a reading that spells out a hidden word of the pack is withheld; a longer word that holds it is not
    tokens = ["wetrri", "qore"]
    assert W.blind_reading(g("qetrri", "meaning", "dialectal variant of wetrri"), set(), tokens) == "[reading withheld]"
    assert W.blind_reading(g("qorene", "meaning", "a title of the qorene"), set(), tokens) == "a title of the qorene"
    assert W.names_one("the ruler (qore)", tokens) and not W.names_one("the qoreneḫ", tokens)


def test_the_hidden_word_is_a_code_with_what_the_map_cuts_off():
    word = g("pSixrkete", "hypothesis", "may you feed him", [{"form": "pSi", "entry": "ps-"}, {"form": "xr", "entry": "ḫr"}, {"form": "kete", "entry": "-kete"}])
    assert W.shown_as(word, "ḫr", "W007") == "pSi-W007-kete"
    assert W.shown_as(g("al", "unknown", "", [{"form": "al", "entry": "?"}]), "al", "W001") == "W001"
    gs = [g("at", "meaning", "bread"), g("mXe", "meaning", "abundant"), word, g("xrkete", "hypothesis", "may you eat", [{"form": "xr", "entry": "ḫr"}, {"form": "kete", "entry": "-kete"}]),
          g("ato", "meaning", "water")]
    line = W.blind_line(gs, 2, "ḫr", "W007", {"ḫr"})
    assert line == "bread · abundant · **pSi-W007-kete** · W007-kete · water"
    assert "xr" not in line.replace("W007", "") and "feed" not in line and "eat" not in line


def test_the_pack_does_not_show_its_own_words():
    its_words = [{"entry": "ato", "places": [("T", 0)], "code": "W001"}, {"entry": "ye- (2)", "places": [("T", 1)], "code": "W002"}]
    gl = {"T": [g("yoto", "meaning", "water"), g("ye", "unknown", "")]}
    assert W.tokens_of(its_words, gl) == ["ato", "yoto"]                 # `ye` is under three letters


def test_the_places_shown_are_twelve_at_most_one_a_text_first():
    places = [(f"T{t}", i) for t in range(8) for i in range(3)]
    got = W.sample(places, random.Random(1))
    assert len(got) == W.SHOWN == 12 and len({t for t, _ in got}) == 8 and got == sorted(got)
    assert W.sample(places[:5], random.Random(1)) == sorted(places[:5])


def test_the_choice_needs_four_of_five():
    assert W.choice_of(["a"] * 5) == "a" and W.choice_of(["a"] * 4 + ["b"]) == "a"
    assert W.choice_of(["a"] * 3 + ["b", "none"]) is None
    assert W.choice_of(["none"] * 4 + ["a"]) == "none"
    assert W.choice_of(["a"] * 4) is None                                # a reader's answer is missing
    assert W.picked({"pick": "B"}, ["w", "x", "y", "z"]) == "x" and W.picked({"pick": " none "}, ["w"]) == "none"
    assert W.picked({"pick": "E"}, ["w", "x", "y", "z"]) is None and W.picked({"pick": "D"}, ["w", "x"]) is None
    assert W.picked({}, ["w"]) is None


def key_of_test(words):
    """A made-up key: code -> (sort, true, candidates), the options in the order A to D for every reader."""
    key = {"words": {}, "letters": {}}
    for n, (code, (sort, true, cands)) in enumerate(words.items()):
        opts = ([true] if sort == "offered" else cands) + ["f1", "f2", "f3"]
        key["words"][code] = {"sort": sort, "entry": code.lower(), "kind": "noun", "true": true, "candidates": cands, "options": opts[:4],
                              "pack": n % W.PACKS + 1}
        for r in range(1, W.READERS + 1):
            key["letters"][f"{code}/{r}"] = opts[:4]
    return key


def answer(folder, key, code, picks):
    for r, p in enumerate(picks, 1):
        f = folder / f"reader{r}" / f"K{key['words'][code]['pack']}.jsonl"
        f.parent.mkdir(parents=True, exist_ok=True)
        with f.open("a", encoding="utf-8") as h:
            h.write(json.dumps({"code": code, "pick": p}) + "\n")


def test_a_label_is_given_only_when_both_bars_hold():
    words = {f"A{n:02d}": ("offered", f"true{n}", []) for n in range(10)}
    words |= {f"B{n:02d}": ("absent", f"gone{n}", []) for n in range(10)}
    words |= {"O01": ("open", None, ["cand"]), "O02": ("open", None, ["cand"]), "O03": ("open", None, ["cand"]), "O04": ("open", None, ["cand"])}
    key = key_of_test(words)

    def run_with(offered_wrong, absent_wrong, drop=None):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            for n in range(10):
                answer(folder, key, f"A{n:02d}", ["B"] * 5 if n < offered_wrong else ["A"] * 5)
                answer(folder, key, f"B{n:02d}", ["A"] * 4 + ["none"] if n < absent_wrong else ["none"] * 5)
            answer(folder, key, "O01", ["A", "A", "A", "A", "none"])
            answer(folder, key, "O02", ["B"] * 5)
            answer(folder, key, "O03", ["none"] * 5)
            answer(folder, key, "O04", ["A", "A", "A", "B", "none"][:4] if drop else ["A", "A", "A", "B", "none"])
            rows = W.choice_rows(key, folder)
            return W.choice_figures(rows), {r["code"]: r.get("verdict") for r in rows if r["sort"] == "open"}

    figs_, verdicts = run_with(2, 1)                                    # 8 of 10 right, 1 of 10 wrong: both bars held
    assert (figs_["right_when_chosen"], figs_["wrong_when_absent"], figs_["bar1"], figs_["bar2"], figs_["labels_given"]) == (0.8, 0.1, True, True, True)
    assert verdicts == {"O01": "favoured", "O02": "a filler chosen", "O03": "none of the four", "O04": "no choice"}
    figs_, verdicts = run_with(3, 0)                                    # 7 of 10 right: bar 1 missed
    assert (figs_["bar1"], figs_["bar2"], figs_["labels_given"]) == (False, True, False) and verdicts["O01"] == "chosen, no label"
    figs_, verdicts = run_with(0, 2)                                    # 2 of 10 wrong: bar 2 missed
    assert (figs_["bar1"], figs_["bar2"], figs_["labels_given"]) == (True, False, False) and verdicts["O01"] == "chosen, no label"
    figs_, verdicts = run_with(0, 0, drop=True)                         # a reader's answer missing: no label at all
    assert figs_["bar1"] and figs_["bar2"] and not figs_["complete"] and not figs_["labels_given"] and verdicts["O01"] == "chosen, no label"


def test_bar_one_needs_eight_words_with_a_choice():
    words = {f"A{n:02d}": ("offered", f"true{n}", []) for n in range(9)} | {"B00": ("absent", "gone", [])}
    key = key_of_test(words)
    with tempfile.TemporaryDirectory() as d:
        for n in range(9):
            answer(Path(d), key, f"A{n:02d}", ["A"] * 5 if n < 7 else ["A", "A", "B", "B", "none"])
        answer(Path(d), key, "B00", ["none"] * 5)
        f = W.choice_figures(W.choice_rows(key, Path(d)))
    assert (f["offered_chosen"], f["right_when_chosen"], f["bar1"], f["found"]) == (7, 1.0, False, round(7 / 9, 4))


def test_a_readers_file_counts_only_for_the_words_of_its_pack():
    key = key_of_test({"A00": ("offered", "t", []), "A01": ("offered", "u", [])})          # packs 1 and 2
    with tempfile.TemporaryDirectory() as d:
        for r in range(1, W.READERS + 1):
            lines(Path(d) / f"reader{r}" / "K1.jsonl", [{"code": "A00", "pick": "A"}, {"code": "A00", "pick": "B"}, {"code": "A01", "pick": "A"}])
        rows = {r["code"]: r for r in W.choice_rows(key, Path(d))}
    assert rows["A00"]["picks"] == {"t": 5} and rows["A00"]["choice"] == "t"
    assert rows["A01"]["answered"] == 0 and rows["A01"]["choice"] is None


# -------------------------------------------------------------------------------------------------- the recount

def test_the_overlay_resolves_only_what_the_pass_agrees_on():
    gl = {"T": [g("wo", "hypothesis", "Isis"), g("Si", "name", "part of woSi"), g("xrkete", "hypothesis", "may you eat"),
                g("akiN", "kind", "a place"), g("al", "unknown"), g("mr", "kind"), g("woSi", "name", "Isis"), g("x.", "lost"), g("ato", "meaning", "water")],
          "U": [g("woSi", "name", "Isis"), g("mlomrs", "hypothesis", "notable")]}
    its = {k: {"places": [{"text": "T", "n": n, "form": f}]} for k, n, f in (("wo-", 1, "wo"), ("ḫr", 3, "xrkete"), ("Akine", 4, "akiN"), ("al", 5, "al"), ("mr", 6, "mr"))}
    rows = [{"item": "wo-", "place": 1, "verdict": "piece", "whole": "woSi"}, {"item": "ḫr", "place": 1, "verdict": "stated", "whole": ""},
            {"item": "Akine", "place": 1, "verdict": "open", "whole": ""}, {"item": "al", "place": 1, "verdict": "open", "whole": ""},
            {"item": "mr", "place": 1, "verdict": "piece", "whole": "mlomrs"}]
    verified = {"ḫr": {"one": {"meaning": "eat", "source": "Rilly 2021", "page": 12}}}
    cands = {"Akine": {"name": "place"}, "al": {"name": ""}}
    ov, f = W.recount_of(gl, its, rows, verified, cands)
    assert [(o["item"], o["level"], o["why"], o["was"]) for o in ov] == [
        ("wo-", "name", "piece", "hypothesis"), ("ḫr", "meaning", "stated", "hypothesis"), ("Akine", "name", "name", "kind")]
    assert ov[1]["gloss"] == "eat" and ov[1]["source"] == "Rilly 2021, p. 12"
    # a piece of a word the map holds open resolves nothing, and an open word that is no name stays open
    assert f["before"] == {"read": 1, "names": 3, "open": 6, "lost": 1, "share": round(1 / 7, 4)}
    assert f["after"] == {"read": 2, "names": 5, "open": 3, "lost": 1, "share": 0.4}
    assert f["pieces"] == {"name": 1, "open": 1} and f["overlay"] == {"piece": 1, "stated": 1, "name": 1}
    assert (f["spellings"], f["spellings_all_resolved"], f["spellings_none_resolved"]) == (5, 3, 2)
    assert W.share({"read": 0, "open": 0}) is None


def test_the_formula_check_looks_three_words_back():
    gl = {"T": [g("at", "meaning"), g("mXe", "meaning"), g("pSxrkete", "hypothesis"), g("a", "unknown"), g("b", "unknown"), g("c", "unknown"), g("xrkete", "hypothesis")],
          # bread four words back is not counted; water (ato) three words back is not bread
          "U": [g("atmXe", "meaning"), g("a", "unknown"), g("b", "unknown"), g("c", "unknown"), g("pSxrkete", "hypothesis")],
          "V": [g("atomXe", "meaning"), g("pSiXekete", "hypothesis"), g("xrkete", "hypothesis")],
          # ẖol: ḫmlol is written with x (ḫ); with X (ẖ) it is another word
          "Z": [g("xmlol", "meaning"), g("Xolkete", "hypothesis"), g("a", "unknown"), g("b", "unknown"), g("c", "unknown"), g("Xmlol", "unknown"),
                g("Xolkete", "hypothesis")]}
    its = {"ḫr": {"places": [{"text": "T", "n": 3}, {"text": "T", "n": 7}, {"text": "U", "n": 5}, {"text": "V", "n": 3}]},
           "ẖol": {"places": [{"text": "Z", "n": 2}, {"text": "Z", "n": 7}]}}
    rows = [{"item": "ḫr", "place": n, "verdict": "stated"} for n in (1, 2, 3, 4)] + [{"item": "ẖol", "place": n, "verdict": "stated"} for n in (1, 2)]
    got = W.formula_check(rows, its, gl)
    assert got["ḫr"] == {"stated": 4, "what": "a form of at, bread (not ato, water)", "with": 1}
    assert (got["ẖol"]["stated"], got["ẖol"]["with"]) == (2, 1)


# ------------------------------------------------------------------------------------- the page and the figures

def test_the_figures_hold_no_text_of_a_source():
    """Counts, verdicts and short meanings only: no statement, quote or place of a local file."""
    text = W.PUBLIC.read_text(encoding="utf-8")
    for word in ('"quote"', '"says"', '"newer_than_2003"', '"readings"', '"why"', '"note"', '"one"', '"two"'):
        assert word not in text, word
    f = figs()
    assert all(len(s["meaning"].split()) <= 14 for s in f["class_a"]["stated"])
    assert all(len(m.split()) <= 4 for r in f["choice"]["rows"] for m in r["options"])
    # the meanings given in our words, where the figures have them; that the readers' wording of each follows a
    # source, and that it stands in no tracked file, test_no_public_meaning_follows_a_source_for_four_words checks
    # on the local files
    assert f["in_our_words"] == len(W.STATED_IN_OUR_WORDS) + len(W.CANDIDATES_IN_OUR_WORDS) == 9 and len(W.STATED_IN_OUR_WORDS) == 4
    assert "Nine meanings in the figures file (four of this table, five candidates of section 6) are given in our words" in page()
    stated = {s["item"]: s["meaning"] for s in f["class_a"]["stated"]}
    assert all(stated[k] == m for k, m in W.STATED_IN_OUR_WORDS.items())
    rows = {r["entry"]: r for r in f["choice"]["rows"] if r["sort"] == "open"}
    assert all(rows[e]["candidates"][n - 1] == m and m in rows[e]["options"] and m in rows[e]["given_by"]
               for (e, n), m in W.CANDIDATES_IN_OUR_WORDS.items())


def test_the_public_rows_carry_the_public_wording():
    """A candidate is reworded by its word and its place among that word's candidates, wherever it stands in the
    row, and keeps its picks and its source. The readers' wordings here are made up."""
    r = {"sort": "open", "entry": "ptroti", "kind": "noun", "true": None, "candidates": ["one wording", "another wording", "master"],
         "options": ["one wording", "another wording", "master", "west"], "picks": {"one wording": 2, "master": 1, "none": 2},
         "choice": "one wording", "verdict": "chosen, no label"}
    given = {"one wording": ["Zyhlarz", "proposes"], "another wording": ["Priese 1977a", "proposes"], "master": ["Griffith 1911", "proposes"]}
    first, second = W.CANDIDATES_IN_OUR_WORDS["ptroti", 1], W.CANDIDATES_IN_OUR_WORDS["ptroti", 2]
    row = W.public_row(r, given)
    assert row["candidates"] == [first, second, "master"] and row["options"] == [first, second, "master", "west"]
    assert row["picks"] == {first: 2, "master": 1, "none": 2} and row["choice"] == first and row["verdict"] == "chosen, no label"
    assert row["given_by"] == {first: ["Zyhlarz", "proposes"], second: ["Priese 1977a", "proposes"], "master": ["Griffith 1911", "proposes"]}
    assert W.public_row(r | {"choice": None}, given)["choice"] is None and W.public_row(r | {"choice": "none"}, given)["choice"] == "none"
    # the same wordings in a word the table does not name stay as they are
    other = W.public_row(r | {"entry": "yeso"}, given)
    assert (other["candidates"], other["picks"], other["choice"], other["given_by"]) == (r["candidates"], r["picks"], "one wording", given)
    # two options that would come out in one wording, or an option worded "none", would merge their picks
    for options in (["one wording", "another wording", second, "west"], ["one wording", "another wording", "master", "none"]):
        try:
            W.public_row(r | {"options": options}, given)
            raise AssertionError(f"wrote the row with the options {options}")
        except SystemExit as e:
            assert "would have one wording; nothing written" in str(e), e
    acc = W.public_row({"sort": "offered", "entry": "sem", "kind": "noun", "true": "wife", "candidates": [], "options": ["wife", "bull"],
                        "picks": {"wife": 5}, "choice": "wife"}, {})
    assert acc == {"sort": "offered", "entry": "sem", "kind": "noun", "true": "wife", "candidates": [], "options": ["wife", "bull"],
                   "picks": {"wife": 5}, "choice": "wife"}


def test_no_public_meaning_follows_a_source_for_four_words():
    """The rule of src/lexicon.py (COPIED) on every meaning of the figures file, against the typed lexicon of 2003
    (all its entries, not only those the map uses: the meaning in French and in English, Rilly's discussion, every
    proposal) and the text of Rilly 2016 and 2021. In those texts a word cut by a hyphen at a line's end is made
    whole, and fi, fl, ff, ffi and ffl count as one letter, which the text layer of Rilly 2021 has lost ("\\x00rst"
    for "first"). Two options stay as the script's ACCEPTED has them (public before, in runs/keys/). The tables of
    meanings in our words name exactly the readers' wordings that follow a source, and none of those wordings
    stands in a tracked file."""
    needs("data/rilly2003", "data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt",
          f"{LOCAL}/lit/verify/result.json", f"{LOCAL}/choice/result.json")
    import re
    import subprocess
    import lexicon as X
    import lexique as L

    def runs(text):
        w = X.words_of(re.sub(r"ffi|ffl|ff|fi|fl|\x00", "ꜰ", text.lower()))
        return {tuple(w[i: i + X.COPIED]) for i in range(len(w) - X.COPIED + 1)}
    grams = set()
    for e in L.load():
        for t in [v for v in e.values() if isinstance(v, str)] + [p.get("proposal") or "" for p in e.get("proposals") or []]:
            grams |= runs(t)
    for path in ("data/sources/rilly2016-text/pages.txt", "data/sources/dotawo-text/pages.txt"):
        text = re.sub(r"(?m)^\f?=== page \d+ ===$", " ", (ROOT / path).read_text(encoding="utf-8", errors="replace"))
        grams |= runs(text) | runs(re.sub(r"(?<=[^\W\d_])-[ \t]*\n\s*(?=[^\W\d_])", "", text))
    copied = lambda m: bool(runs(m) & grams)                                                   # noqa: E731
    kept = {"to love, to revere", "to order, to command"}
    assert {m for m, _ in W.ACCEPTED.values() if copied(m)} == kept
    f = figs()
    meanings = {s["meaning"] for s in f["class_a"]["stated"]}
    for r in f["choice"]["rows"]:
        meanings |= set(r["options"]) | set(r["candidates"]) | (set(r["picks"]) - {"none"}) | set(r.get("given_by", {}))
    bad = [m for m in sorted(meanings - kept) if copied(m)]
    assert not bad, bad
    # the readers' wordings, which the local results keep: the tables reword exactly those that follow a source
    verified, rows = W.read("lit/verify/result.json"), W.read("choice/result.json")["rows"]
    stated = {k: v["one"]["meaning"] for k, v in verified.items() if v["verdict"] == "stated"}
    cands = {(r["entry"], n): m for r in rows if r["sort"] == "open" for n, m in enumerate(r["candidates"], 1)}
    follow = ({k for k, m in stated.items() if copied(m)}, {k for k, m in cands.items() if copied(m)})
    assert follow == (set(W.STATED_IN_OUR_WORDS), set(W.CANDIDATES_IN_OUR_WORDS)), follow
    theirs = [stated[k] for k in W.STATED_IN_OUR_WORDS] + [cands[k] for k in W.CANDIDATES_IN_OUR_WORDS]
    found = subprocess.run(["git", "grep", "-I", "-i", "-F", "-l"] + [a for m in theirs for a in ("-e", m)], cwd=ROOT, capture_output=True, text=True)
    assert found.returncode == 1 and not found.stdout, found.stdout or found.stderr


def test_the_figures_add_up():
    f = figs()
    assert (f["spellings"], f["items"], f["running_words"]) == (154, 121, 1108)
    m = f["map"]
    assert m["in_three_texts_or_more"] == f["spellings"] and m["open_spellings"] == m["in_three_texts_or_more"] + m["in_one_or_two_texts"]
    assert m["running_words"] == f["recount"]["running_words"]
    assert sum(f["candidates"]["left_out"].values()) + f["choice"]["open_words"] == f["candidates"]["with_a_candidate"]
    assert f["candidates"]["left_out"]["a name by the sources"] <= len(f["candidates"]["names"])
    assert sum(c["items"] for c in f["classes"].values()) == f["items"]
    assert sum(c["spellings"] for c in f["classes"].values()) == f["spellings"]
    assert sum(c["running_words"] for c in f["classes"].values()) == f["running_words"]
    a = f["class_a"]
    assert a["items"] == f["classes"]["A"]["items"] == sum(a["verdicts"].values()) and len(a["stated"]) == a["verdicts"]["stated"]
    assert sum(a["covered"].values()) == a["running_words"] == sum(s["uses"] for s in a["stated"])
    p = f["places"]
    assert p["places"] == p["answered by both"] == f["running_words"] == sum(p["verdicts"].values())
    for v, n in p["verdicts"].items():
        assert sum(c.get(v, 0) for c in p["by class"].values()) == n, v
    assert p["taken"] is (p["kappa"] >= p["bar"]) and p["bar"] == W.KAPPA
    assert sum(s["places_stated"] for s in a["stated"]) == p["verdicts"]["stated"]
    c = f["candidates"]
    assert c["items"] == f["open_items"] == c["with_a_candidate"] + c["none"]
    ch = f["choice"]
    assert ch["words"] == len(ch["rows"]) == ch["offered"] + ch["absent"] + ch["open_words"] and ch["bars"] == W.BARS
    assert ch["offered"] == ch["offered_chosen"] + ch["offered_none"] + ch["offered_no_choice"] and sum(ch["open"].values()) == ch["open_words"]
    assert ch["right_when_chosen"] == round(ch["offered_right"] / ch["offered_chosen"], 4)
    assert ch["bar1"] is (ch["offered_chosen"] >= 8 and ch["right_when_chosen"] >= 0.8) and ch["bar2"] is (ch["wrong_when_absent"] <= 0.1)
    assert ch["labels_given"] is (ch["complete"] and ch["bar1"] and ch["bar2"])
    assert ("favoured" in ch["open"]) is ch["labels_given"]
    r = f["recount"]
    for side in ("before", "after"):
        assert sum(r[side][k] for k in ("read", "names", "open", "lost")) == r["running_words"]
    assert sum(r["overlay"].values()) == sum(r["overlay_levels"].values()) == sum(r["was"].values())
    assert r["overlay"]["stated"] == p["verdicts"]["stated"] and sum(r["pieces"].values()) == p["verdicts"]["piece"]
    assert r["overlay"]["piece"] == r["pieces"]["read"] + r["pieces"]["name"]
    assert r["before"]["open"] - r["after"]["open"] == sum(r["was"][k] for k in W.OPEN)
    t = f["tokens"]
    assert t["all"] == {"agents": sum(v["agents"] for k, v in t.items() if k != "all"), "tokens": sum(v["tokens"] for k, v in t.items() if k != "all")}


def test_the_page_says_what_the_figures_say():
    f, text = figs(), page()
    pct = lambda x: f"{100 * x:.1f}%"                                     # noqa: E731
    a, p, ch, r, c = f["class_a"], f["places"], f["choice"], f["recount"], f["candidates"]
    lit, m = f["literature"], f["map"]
    assert (f"The map of `corpus_v6` ({m['inscriptions']} inscriptions, {m['running_words']:,} running words) holds {m['open_spellings']:,} "
            f"distinct spellings without an accepted meaning. {m['in_three_texts_or_more']} of them stand in three texts or more and cover "
            f"{f['running_words']:,} running words") in text
    assert f"The {m['in_one_or_two_texts']:,} open spellings that stand in one or two texts were not in this work." in text
    lo = c["left_out"]
    assert (f"Of the {c['with_a_candidate']} items with a candidate, the rules added before step 2 left out {sum(lo.values())}: "
            f"{lo['first candidate a function word']} whose first candidate is a function word (an ending or a particle), "
            f"{lo['a name by the sources']} names by the sources, {lo['first candidate a numeral']} whose first candidate is a numeral, "
            f"and {lo['no candidate left after the removals']} with no candidate left after the removals") in text and len(lo) == 4
    for w in f["when"]:
        assert f"| {w['step']} | {w['set_in']} | {w['set']} | {w['started']} | {w['first_answer']} |" in text, w["step"]
    assert f"{lit['statements']} statements, {lit['quote_found']} quotes found, for {lit['items_with_a_checked_statement']} of the {f['items']} items" in text
    for letter, row in f["classes"].items():
        line = next(l for l in PAGE.read_text(encoding="utf-8").splitlines() if l.startswith(f"| {letter} | "))
        assert line.endswith(f"| {row['items']} | {row['spellings']} | {row['running_words']} |"), letter
    assert f"{a['verdicts']['stated']} of the {a['items']} items pass" in text
    assert f"of the {a['running_words']} running words of the {a['verdicts']['stated']} items: {a['covered']['all']} \"all\", {a['covered']['some']} \"some\", {a['covered']['none']} \"none\"" in text
    for k in a["not_stated"]:
        assert f"`{k}`" in between(text, "The three that do not:", "The readers also said")
    assert f"Their Cohen's kappa is {p['kappa']:.2f} (bar {p['bar']})" in text
    for v in ("stated", "piece", "open", "unclear", "not agreed"):
        cells = " | ".join(str(p["by class"][k].get(v, 0)) for k in "ABC")
        assert f"| {v} | {p['verdicts'][v]} | {cells} |" in text, v
    for s in a["stated"]:
        assert f"| `{s['item']}` | {s['meaning']} | {s['source']}, p. {s['page']} | {s['uses']} | {s['places_stated']} |" in text, s["item"]
    none = [s["item"] for s in a["stated"] if s["places_stated"] == 0]
    assert all(f"`{k}`" in between(text, "of the 26 have no place stated", "A check by script") for k in none) and f"Seven of the {len(a['stated'])}" in text and len(none) == 7
    fc = p["formula_check"]
    assert f"all {fc['ḫr']['with']} stated places of `ḫr`" in text and fc["ḫr"]["with"] == fc["ḫr"]["stated"]
    assert f"{fc['ẖol']['with']} of the {fc['ẖol']['stated']} stated places of `ẖol`" in text
    pc = r["pieces"]
    assert f"The {p['verdicts']['piece']} pieces: the whole word both checkers name is a word the map already reads for {pc['read']} places, a name the map has for {pc['name']}, a word the map holds open for {pc['open']}, and no form of the map for {pc['not a form of the map']}." in text
    assert f"{f['open_items']} items keep three or more open places ({f['open_places']} places). For {c['with_a_candidate']} of them both readers list a candidate; for {c['none']} they list none." in text
    for k in c["names"]:
        assert f"`{k}`" in between(text, "are names by the sources:", "### Result of step 2"), k
    assert f"{ch['words']} words went into five packs: {ch['open_words']} open words, {ch['offered']} accepted words with the meaning offered, {ch['absent']} with the meaning not offered" in text
    assert f"| Accepted, meaning offered | {ch['offered']} | {ch['offered_chosen']} | {ch['offered_right']} | {ch['offered_none']} | {ch['offered_no_choice']} |" in text
    assert f"| Accepted, meaning not offered | {ch['absent']} | {ch['absent_wrong']} (both wrong) | | {ch['absent_none']} | {ch['absent'] - ch['absent_wrong'] - ch['absent_none']} |" in text
    assert f"{ch['offered_right']} of {ch['offered_chosen']} ({pct(ch['right_when_chosen'])}; the bar is 80%)" in text
    assert f"{ch['absent_wrong']} of {ch['absent']} ({pct(ch['wrong_when_absent'])}; the bar is 10%)" in text
    assert f"{ch['offered_right']} of the {ch['offered']} accepted words that had it among the options ({pct(ch['found'])})" in text
    assert not ch["bar1"] and not ch["bar2"] and "**Bar 1 is missed.**" in text and "**Bar 2 is missed.**" in text
    wrong = [x for x in ch["rows"] if x["sort"] != "open" and x["choice"] not in (None, "none") and x["choice"] != x["true"]]
    assert len(wrong) == ch["offered_chosen"] - ch["offered_right"] + ch["absent_wrong"]
    for x in wrong:
        assert f"`{x['entry']}` \"{x['true']}\"" in text and f"\"{x['choice']}\"" in text, x["entry"]
    o = ch["open"]
    assert f"a candidate chosen, {o['chosen, no label']} words" in text and f"a filler chosen, {o['a filler chosen']} words" in text
    assert f"\"none of the four\", {o['none of the four']} words; no choice, {o['no choice']} words" in text
    for x in ch["rows"]:
        if x.get("verdict") == "chosen, no label":
            by = x["given_by"][x["choice"]]
            assert f"| `{x['entry']}` | {x['choice']} | {by[0]} ({by[1]}) | {x['picks'][x['choice']]} of 5 |" in text, x["entry"]
        if x.get("verdict") == "a filler chosen":
            assert f"`{x['entry']}` as \"{x['choice']}\"" in text, x["entry"]
    ag = ch["all_agree"]
    assert f"{ag['offered_right']} of {ag['offered_chosen']} accepted words were right and no wrong meaning was chosen" in text and ag["absent_wrong"] == 0
    for side, col in (("read", "have a meaning"), ("names", "names and numerals"), ("open", "open"), ("lost", "signs lost")):
        assert f"| {col} | {r['before'][side]:,} | {r['after'][side]:,} |" in text, side
    assert f"| **{pct(r['before']['share'])}** | **{pct(r['after']['share'])}** |" in text and f"Of the {r['running_words']:,} running words" in text
    assert f"from {pct(r['before']['share'])} to {pct(r['after']['share'])}" in text
    ov = r["overlay"]
    already = sum(r["was"][k] for k in ("meaning", "grammar", "name"))
    assert f"The overlay holds {sum(ov.values())} places: the {ov['stated']} stated ones, {ov['piece']} pieces of a word the map reads ({pc['read']}) or of a name ({pc['name']}), and the {ov['name']} open places of the seven names. {already} of the {sum(ov.values())} were already read or named" in text
    assert f"the count of open words falls by {r['before']['open'] - r['after']['open']}" in text and len(c["names"]) == 7
    assert (f"the overlay resolves every place of {r['spellings_all_resolved']}, more than half the places of {r['spellings_most_resolved']} "
            f"(the {r['spellings_all_resolved']} among them), and no place of {r['spellings_none_resolved']}") in text
    v = p["verdicts"]
    assert f"{v['stated']} take a meaning that Rilly states" in text and f"{v['piece']} are pieces" in text and f"{v['open']} are words of their own" in text
    assert f"{v['unclear'] + v['not agreed']} are unclear or not agreed" in text
    assert f"{v['not agreed']} places are not agreed and {v['unclear']} are unclear" in text
    t = f["tokens"]
    assert f"{t['all']['agents']} fresh agents, {t['all']['tokens']:,} subagent tokens" in text
    for k in ("literature", "verifiers", "place_checkers", "candidate_readers", "choice_readers"):
        assert f"{t[k]['tokens']:,} ({t[k]['agents']}" in text, k


def test_the_summaries_quote_the_figures():
    """README, REPORT and NEXT_STEPS say of this work what the figures file says."""
    f = figs()
    read = lambda name: " ".join((ROOT / name).read_text(encoding="utf-8").split())        # noqa: E731
    pct = lambda x: f"{100 * x:.1f}%"                                                       # noqa: E731
    parts = {"README": between(read("README.md"), "17. **Of the unread spellings that recur", "## The question"),
             "REPORT": read("REPORT.md")[read("REPORT.md").index("## Day six, afternoon (2026-11-13): the unread spellings that recur"):],
             "NEXT_STEPS": between(read("NEXT_STEPS.md"), "18. **The unread spellings that recur", "Next, in this order")}
    v, ch, r, a = f["places"]["verdicts"], f["choice"], f["recount"], f["class_a"]
    for name, text in parts.items():
        assert f"{f['running_words']:,} running words" in text and "154" in text, name
        for n in (v["stated"], v["piece"], v["open"]):
            assert str(n) in text, (name, n)
        assert f"kappa {f['places']['kappa']:.2f}" in text, name
        assert pct(r["before"]["share"]) in text and pct(r["after"]["share"]) in text, name
        assert pct(ch["right_when_chosen"]) in text and pct(ch["wrong_when_absent"]) in text and "80%" in text and "10%" in text, name
    for name in ("README", "NEXT_STEPS"):
        assert f"{v['unclear'] + v['not agreed']} are unclear or not agreed" in parts[name], name
        assert f"{ch['offered_right']} of {ch['offered_chosen']}" in parts[name] and f"{ch['absent_wrong']} of {ch['absent']}" in parts[name], name
    assert f"{f['literature']['statements']} statements" in parts["README"] and f"for {a['verdicts']['stated']} items" in parts["README"]
    assert f"from {r['before']['read']:,} to {r['after']['read']:,}, from {pct(r['before']['share'])} to {pct(r['after']['share'])}" in parts["README"]
    rep = parts["REPORT"]
    assert f"{r['before']['read']:,} ({pct(r['before']['share'])})" in rep and f"Of the {r['before']['read'] + r['before']['open']:,} running words" in rep
    assert f"into {f['items']} items" in rep and f"collected {f['literature']['statements']} statements" in rep and f"all {f['literature']['quote_found']} quotes" in rep
    assert f"For {a['items']} items" in rep and f"{a['verdicts']['stated']} items pass" in rep
    assert f"{v['unclear']} are unclear and {v['not agreed']} not agreed" in rep
    fc = f["places"]["formula_check"]["ḫr"]
    assert f"all {fc['with']} stated places of the verb" in rep and fc["with"] == fc["stated"]
    assert f"({r['after']['read']:,} read, {r['before']['open'] - r['after']['open']} fewer open)" in rep
    c = f["candidates"]
    assert (f"{f['open_items']} items keep three or more open places. For {c['with_a_candidate']} both readers list a meaning the sources "
            f"propose, and seven items are names") in rep and len(c["names"]) == 7
    assert f"{ch['words']} words shown only as a code" in rep and f"On the {ch['offered']} accepted words" in rep and f"on the {ch['absent']} whose true meaning" in rep
    assert f"chose a meaning for {ch['offered_chosen']} and were right for {ch['offered_right']} ({pct(ch['right_when_chosen'])}" in rep
    assert f"still chose one for {ch['absent_wrong']} ({pct(ch['wrong_when_absent'])}" in rep
    t = f["tokens"]
    assert f"{t['all']['agents']} fresh agents, {t['all']['tokens']:,} subagent tokens" in rep
    for k in ("literature", "verifiers", "place_checkers", "candidate_readers", "choice_readers"):
        assert f"{t[k]['tokens']:,}" in rep, k
    spellings_left = f"{f['map']['in_one_or_two_texts']:,} open spellings that stand in one or two texts"
    assert spellings_left in rep and spellings_left in parts["NEXT_STEPS"] and spellings_left in page()
    assert f"{r['before']['read'] + r['before']['open']:,} running words" in rep and r["before"]["read"] + r["before"]["open"] < f["map"]["running_words"]


def test_the_readme_lists_the_script_among_the_local_commands():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "- `python3 -I src/recurring.py public` (and " in text and "python3 -I tests/test_recurring.py" in text
    start = "- `python3 -I src/recurring.py public` (and "
    listed = between(" ".join(text.split()), start, ") reads")[len(start):]
    assert sorted([c.strip("` ") for c in listed.split(",")] + ["public"]) == sorted(W.COMMANDS)
    head = W.__doc__
    for c in W.COMMANDS:
        assert f"python3 -I src/recurring.py {c} " in head, c


def test_the_bars_on_the_page_are_the_scripts():
    text = page()
    assert f"is under {W.KAPPA}, nothing is taken" in text
    assert f"for at least {100 * W.BARS['right_when_chosen']:.0f}%, and there are at least {W.BARS['chosen_at_least']} such words" in text
    assert f"for at most {100 * W.BARS['wrong_when_absent']:.0f}%" in text
    assert "option that four or five of the five pick" in text and (W.NEEDED, W.READERS) == (4, 5)
    for m in W.UNTRANSLATED:
        assert f'"{m}"' in text, m


def test_the_prompts_are_in_the_repository():
    brief = (ROOT / "runs/prompts/RECURRING_literature.md").read_text(encoding="utf-8")
    assert "copy, do not retype from" in brief and "Do not give a meaning of" in brief
    launch = (ROOT / "runs/prompts/RECURRING_launch.md").read_text(encoding="utf-8")
    # the two batches of pieces were started with one sentence more, as the session's log records it
    assert "`pieces_a` and `pieces_b`" in launch and "so the field \"piece\" matters most" in " ".join(launch.split())
    for name in ("VERIFY_BRIEF", "PLACE_BRIEF", "CAND_BRIEF", "CHOICE_BRIEF"):
        assert name in launch and isinstance(getattr(W, name), str), name
    for brief in (W.VERIFY_BRIEF, W.PLACE_BRIEF, W.CAND_BRIEF):
        assert "Do not use your own knowledge of Meroitic" in brief
    assert "do not use what you may know of published translations" in " ".join(W.CHOICE_BRIEF.split())


def test_the_figures_are_the_count_of_the_local_files():
    needs(f"{LOCAL}/items.json", f"{LOCAL}/lit/checked.json", f"{LOCAL}/lit/verify/result.json", f"{LOCAL}/places/result.json",
          f"{LOCAL}/choice/candidates.json", f"{LOCAL}/choice/result.json", f"{LOCAL}/recount.json", "data/sources/v6")
    assert W.figures() == figs()


def test_the_local_results_are_what_the_answers_give():
    """The stored results, counted again from the agents' answer files."""
    needs(f"{LOCAL}/items.json", f"{LOCAL}/places/answers1", f"{LOCAL}/places/answers2", f"{LOCAL}/choice/key.json", f"{LOCAL}/choice/reader1",
          f"{LOCAL}/lit/verify/result.json", f"{LOCAL}/lit/classes.json")
    its, groups = W.the_items(), W.read("places/groups.json")
    rows, pairs = W.place_rows(its, W.read("lit/classes.json"), W.read("lit/verify/result.json"),
                               W.place_answers(W.OUT / "places" / "answers1", groups), W.place_answers(W.OUT / "places" / "answers2", groups))
    stored = W.read("places/result.json")
    assert rows == stored["rows"] and round(W.kappa(pairs), 4) == stored["kappa"]
    crow = W.choice_rows(W.read("choice/key.json"), W.OUT / "choice")
    cf = W.choice_figures(crow)
    assert {"figures": cf, "rows": crow} == W.read("choice/result.json")


def test_every_pack_and_result_is_what_the_steps_write():
    """Every step run again in a folder of its own, the agents' answers of a step copied in only after its packs
    are written, gives byte for byte every pack the agents read and every result the figures are counted from."""
    needs(f"{LOCAL}/items.json", f"{LOCAL}/choice/key.json", "data/sources/v6", "data/sources/lexicon", "data/corpus_v6.jsonl",
          "data/rilly2003")
    import filecmp
    import shutil
    stages = [["items", "batches"], ["lit/answers"], ["quotes", "verify-packs"], ["lit/verify/answers1", "lit/verify/answers2"],
              ["verify", "place-packs"], ["places/answers1", "places/answers2"], ["places", "cand-packs"], ["choice/cand1", "choice/cand2"],
              ["cands", "choice-packs"], [f"choice/reader{r}" for r in range(1, W.READERS + 1)], ["choice", "recount"]]
    real = W.OUT
    with tempfile.TemporaryDirectory() as d:
        try:
            W.OUT = Path(d)
            for stage in stages:
                for step in stage:
                    if step in W.COMMANDS:
                        with contextlib.redirect_stdout(io.StringIO()):
                            W.COMMANDS[step]()
                    else:
                        shutil.copytree(real / step, W.OUT / step, dirs_exist_ok=True)
            mine = {p.relative_to(W.OUT) for p in W.OUT.rglob("*") if p.is_file()}
        finally:
            W.OUT = real
        theirs = {p.relative_to(real) for p in real.rglob("*") if p.is_file() and not p.name.startswith(".")
                  and p.relative_to(real).parts[0] != "old_scripts" and p.relative_to(real) != Path("lit/BRIEF.md")}
        assert mine == theirs, (sorted(map(str, mine - theirs)), sorted(map(str, theirs - mine)))
        differ = [str(p) for p in sorted(theirs) if not filecmp.cmp(real / p, Path(d) / p, shallow=False)]
        assert not differ, differ
    assert (real / "lit/BRIEF.md").read_bytes() == (ROOT / "runs/prompts/RECURRING_literature.md").read_bytes()


def test_each_bar_was_set_before_its_agents_were_started():
    """The commits are git's and their times the page's; every bar was set before the agents it binds were started,
    and they were started before they answered. The classes sort the literature pass's answers, so they were set
    after them, and before the readers of class A were started."""
    import subprocess
    when = W.WHEN
    assert [w["step"] for w in when] == [w["step"] for w in figs()["when"]]
    for w in when:
        if w["set_in"].endswith("not committed"):
            continue
        got = subprocess.run(["git", "log", "-1", "--format=%cI", w["set_in"]], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        assert got == f"2026-11-13T{w['set']}-08:00", (w["step"], got)
    bars = when[1:]
    assert all(w["set"] < w["started"] < w["first_answer"] for w in bars), bars
    classes, class_a = when[0], when[1]
    assert classes["started"] < classes["first_answer"] < classes["set"] < class_a["started"]


def test_the_times_of_the_bars_are_the_files():
    """The first answer of each step, and the working script that held the bar of class A, as their files' times
    give them (Pacific time)."""
    needs(f"{LOCAL}/old_scripts/verify.py", f"{LOCAL}/lit/answers", f"{LOCAL}/choice/reader1")
    import datetime
    import zoneinfo
    pacific = zoneinfo.ZoneInfo("America/Los_Angeles")

    def clock(path):
        t = datetime.datetime.fromtimestamp(path.stat().st_mtime, pacific)
        assert t.date() == datetime.date(2026, 11, 13), (path, t)
        return t.strftime("%H:%M:%S")
    for w in W.WHEN:
        files = [f for folder in w["answers"] for f in (W.OUT / folder).glob("*.jsonl")]
        assert files and min(map(clock, files)) == w["first_answer"], w["step"]
    assert clock(W.OUT / "old_scripts/verify.py") == W.WHEN[1]["set"]


def test_no_pack_of_the_choice_shows_a_hidden_spelling():
    needs(f"{LOCAL}/choice/key.json", f"{LOCAL}/choice/packs", "data/sources/v6")
    import re
    key, gl = W.read("choice/key.json"), W.the_map()
    for n in range(1, W.PACKS + 1):
        mine = [w | {"code": c} for c, w in key["words"].items() if w["pack"] == n]
        tokens = W.tokens_of(mine, gl)
        for r in range(1, W.READERS + 1):
            body = (W.OUT / "choice" / "packs" / f"K{n}_r{r}.md").read_text(encoding="utf-8").split("\n---\n", 1)[1]
            for tok in tokens:
                assert not re.search(rf"(?<![A-Za-zḫẖšñ]){re.escape(tok)}(?![A-Za-zḫẖšñ])", body), (n, r, tok)
            for w in mine:
                if w["true"]:
                    block = body[body.index(f"## `{w['code']}`"):].split("\n## `", 1)[0]
                    assert (f". {w['true']}\n" in block + "\n") is (w["sort"] == "offered"), w["code"]


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
