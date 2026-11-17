"""Checks for track A, the two Nubian dictionaries (src/nubian.py, data/discovery/outside_evidence.md section 2).

  python3 -I tests/test_nubian.py

The typed pages are local only, and this file was written before any of them was seen: the checks of `merge`,
`agree` and `gate` run on made-up pages and words. The list of known words is public and is checked as it stands,
and against a count from the local files where those are present.
"""
import collections
import contextlib
import io
import json
import random
import sys
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import cognates_rules as cr          # noqa: E402
import nubian as N                   # noqa: E402
from local_only import NES_LISTS, needs, run    # noqa: E402

THE_MAP = ("data/sources/v6/analysts/glosses.jsonl", "data/sources/lexicon", "data/sources/expert", "data/sources/egyptian/loans_both.jsonl",
           "data/sources/recurring/overlay.jsonl", "data/sources/rare/g2/overlay.jsonl", "data/sources/rare/g4/overlay.jsonl",
           "data/sources/g3/overlay.jsonl", "data/sources/rare/g4m/overlay.jsonl", "data/sources/g8b/overlay.jsonl", "data/sources/g9/overlay.jsonl")
SMALL = {"R": {"first": 333, "last": 336, "page": 332, "list": "reinisch1879"}, "L": {"first": 410, "last": 411, "page": 147, "list": "lepsius1880"}}
MEANINGS = ("water fire stone tree bird fish house moon star milk bread salt meat bone skin horn tail feather root leaf seed sand cloud "
            "rain smoke ash road mountain river night tooth tongue knee belly neck heart liver blood egg louse").split()


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
    """A folder of its own in the place of data/sources/nubian/, with the two folders of typed pages."""
    with tempfile.TemporaryDirectory() as d:
        home = Path(d)
        (home / "typed").mkdir()
        (home / "typed2").mkdir()
        with set_to(N, HOME=home):
            yield home


def line(book, index, n, headword, de="", en="", dialect="", loan="", parent="", note="", books=SMALL):
    return "\t".join([book, str(index), str(index - books[book]["page"]), str(n), headword, dialect, loan, "", "n", de, en, "", parent, note])


def typed(folder, book, index, rows, count=None, blank=False, header=None):
    """One typed file: rows are dicts of line()'s arguments after n. The count line is right unless `count` is given."""
    body = [line(book, index, n, **r) for n, r in enumerate(rows, 1)]
    entries = sum(not r.get("parent") for r in rows)
    lines = [header or "\t".join(N.HEADER)] + body + (["# blank"] if blank else []) + [count or f"# entries={entries} subrows={len(rows) - entries}"]
    (folder / f"{book}{index:04d}.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_pages(folder):
    """Six made-up pages that pass every check: a sub-row, a page that begins inside an entry, a blank page."""
    typed(folder, "R", 333, [dict(headword="Āb", de="vater", en="father", dialect="KD"),
                             dict(headword="āb-kiñ", de="waise", en="orphan", parent="Āb"),
                             dict(headword="Agar", de="ort; stelle", en="place; spot", dialect="FM", note="runs on")])
    typed(folder, "R", 334, [dict(headword="agar-ti", de="örtlich", en="local", parent=N.CONTINUED),
                             dict(headword="Ai", de="ich", en="I", dialect="K"),
                             dict(headword="Aman", de="wasser", en="water", note="unsure: the second a")])
    typed(folder, "R", 335, [], blank=True)
    typed(folder, "R", 336, [dict(headword="aman-dō", de="am wasser", en="at the water", parent=N.CONTINUED),
                             dict(headword="Bāb", de="tür", en="door", loan="Ar")])
    typed(folder, "L", 410, [dict(headword="ā", de="herz", en="heart", dialect="M")])
    typed(folder, "L", 411, [dict(headword="kitāb", de="buch", en="book", dialect="MKD", loan="*", note="[kitāb]"),
                             dict(headword="kitāb-kā", de="das buch (obj.)", en="the book (object)", parent="kitāb")])


# ------------------------------------------------------------------------------------------- the known words

def the_list():
    return json.loads(N.LIST.read_text(encoding="utf-8"))


def test_the_list_has_the_pages_counts():
    f = the_list()
    c, ws = f["counts"], f["words"]
    assert (c["with_a_meaning"], c["loans_by_both_readers"], c["rule_words"], c["left"]) == (160, 15, 18, 127)
    assert {k: c[k] for k in N.COUNTS} == N.COUNTS and len(ws) == 160 == len({w["headword"] for w in ws})
    by_rule = lambda start: [w for w in ws if w["rule"].startswith(start)]       # noqa: E731
    assert len(by_rule("a loan into Meroitic")) == 15 and len(by_rule("a word the correspondences")) == 18
    assert all(len(by_rule(start)) == c[k] for k, start in N.REDUCED.items())
    kept = [w for w in ws if w["kept"]]
    assert len(kept) == c["kept"] == 127 - sum(c[k] for k in N.REDUCED) == 83
    assert all(w["rule"] == "kept" for w in kept) and not any(w["rule"].startswith("kept") for w in ws if not w["kept"])
    assert c["kept_by_the_lexicon"] + c["kept_by_a_layer"] == c["kept"] == sum(c["kept_wording_from"].values())
    assert sum(w["meaning_from"] == "the lexicon" for w in kept) == c["kept_by_the_lexicon"]
    assert dict(collections.Counter(w["wording_from"] for w in kept)) == c["kept_wording_from"]
    assert c["kept_with_a_same_meaning_row_in_the_short_lists"] <= c["kept"] - c["kept_without_a_key"]
    assert f["map_layers"] == list(N.MAP_LAYERS) and len(N.MAP_LAYERS) == 7 and f["function_words"] == sorted(N.FUNCTION_WORDS)
    named = {w["headword"]: w["rule"] for w in ws if w["headword"] in N.BY_NAME}
    assert set(named) == set(N.BY_NAME) and all(r.startswith("by name, ") for r in named.values())    # each check holds on the lexicon
    families = {w["rule"].split(", ")[1][len("in the family of "):] for w in by_rule("counted once, in the family of")}
    assert families == {"tk (1)", "ns", "qo", "qe (1)", "mk", "at (2)", "pl (2)"}                    # tk, ns, qo, and the others found


def test_the_list_has_no_meaning():
    f = the_list()
    assert all(set(w) == {"headword", "kind", "meaning_from", "wording_from", "kept", "rule"} for w in f["words"])   # the lexicon is in copyright
    assert all(w["meaning_from"] == "the lexicon" or w["meaning_from"].split()[1] in N.MAP_LAYERS for w in f["words"])
    assert {w["wording_from"] for w in f["words"]} <= {"the public table", "the layers' lines", "the lexicon"}
    assert "meaning" not in f and "meaning" not in f["counts"]


def test_the_list_keeps_the_pages_rules():
    ws = the_list()["words"]
    rule = [w["headword"] for w in ws if w["rule"].startswith("a word the correspondences")]
    assert {N.bare(h) for h in rule} <= set(N.RULE_WORDS) and len(N.RULE_WORDS) == 22
    assert not any(N.bare(w["headword"]) in N.RULE_WORDS for w in ws if w not in rule and not w["rule"].startswith("a word the corr")
                   and not w["rule"].startswith("a loan"))
    stems = [N.bare(h) for h in rule if len(N.bare(h)) >= 3]
    assert len(stems) == 15                                            # dm, l and lẖ have fewer than three letters
    kept = [N.bare(w["headword"]) for w in ws if w["kept"]]
    assert not any(k.startswith(s) or k.endswith(s) for k in kept for s in stems)
    assert not any(a != b and b.startswith(a) for a in kept for b in kept) and len(kept) == len(set(kept))   # one word a stem, of any length
    assert not set(N.BY_NAME) & {w["headword"] for w in ws if w["kept"]}
    for w in ws:                                                       # a dropped word names what dropped it
        if w["rule"].startswith("counted once, under "):
            stem = w["rule"][len("counted once, under "):]
            assert stem in {x["headword"] for x in ws if x["kept"]} and N.bare(w["headword"]).startswith(N.bare(stem)) and len(N.bare(stem)) >= 3
        if w["rule"].startswith("counted once, in the family of "):
            stem = w["rule"][len("counted once, in the family of "):].split(", a stem")[0]
            assert stem in {x["headword"] for x in ws if x["kept"]} and N.bare(w["headword"]).startswith(N.bare(stem)) and len(N.bare(stem)) < 3
        if w["rule"].startswith("built on the rule word "):
            on = w["rule"][len("built on the rule word "):].split(" and ")
            assert set(on) <= set(stems) and all(N.bare(w["headword"]).startswith(s) or N.bare(w["headword"]).endswith(s) for s in on)
        if w["rule"].startswith("by name, "):
            what, base, entry, *_ = N.BY_NAME[w["headword"]]
            assert f" {base}, " in w["rule"] and w["rule"].endswith(f"(the lexicon's entry {entry})")


def test_reductions_on_made_up_headwords():
    left = ["kdise", "mkdi", "ptare", "slẖ", "qor", "qor-o", "qorise", "mlo", "mlowi", "tk (1)", "tk (2)", "tkk", "abc (2)", "abc (1)", "ns per", "kb"]
    out = N.reductions(left, ["kdi", "qore", "l (2)", "lẖ", "are (3)"])
    assert out["kdise"] == out["mkdi"] == (False, "built on the rule word kdi")           # begins with it, ends with it
    assert out["ptare"] == (False, "built on the rule word are")                          # the sense number is no letter
    assert out["slẖ"] == (True, "kept")                                                   # lẖ and l have under three letters
    assert out["qor"][0] and "the lexicon's entry qor does not name qore" in out["qor"][1]   # named, but no lexicon here: kept
    assert out["qor-o"] == out["qorise"] == (False, "counted once, under qor")            # the hyphen is no letter
    assert out["mlo"] == (True, "kept") and out["mlowi"] == (False, "counted once, under mlo")
    assert out["tk (1)"] == (True, "kept")                                                # a family under three letters: the shortest alone
    assert out["tk (2)"] == out["tkk"] == (False, "counted once, in the family of tk (1), a stem under three letters")
    assert out["abc (1)"] == (True, "kept") and out["abc (2)"] == (False, "counted once, under abc (1)")
    assert out["ns per"] == out["kb"] == (True, "kept")                                   # a stem that stands once
    assert N.bare("ns per") == "nsper" and N.bare("t-erike-l") == "terikel" and N.bare("ḫ- (1)") == "ḫ"
    assert set(out) == set(left)
    chain = N.reductions(["abcde", "abcd", "abc"], [])
    assert chain["abcde"] == chain["abcd"] == (False, "counted once, under abc")          # the shortest stands
    short = N.reductions(["ns", "ns per", "nse doke", "qo", "qoli", "qor-o"], [])
    assert [short[h][0] for h in ("ns", "ns per", "nse doke", "qo", "qoli", "qor-o")] == [True, False, False, True, False, False]


def entry(h, meaning, *proposals):
    return {"headword": h, "meaning": meaning, "proposals": [{"proposal": p} for p in proposals]}


def test_the_third_reduction_by_name_is_checked_against_the_lexicon():
    lex = {"qor": entry("qor", "determined form of qore 'ruler'"), "yeto": entry("yeto", "water, a very rare variant of ato"),
           "mse": entry("mse", "variant (?) of mte"), "ḫlẖl": entry("ḫlẖl", "ḫ(re) + lẖ + l 'a great *ḫre' (meal)"),
           "ḫ- (1)": entry("ḫ- (1)", "meal"), "ḫmlol": entry("ḫmlol", "doubtless 'a good meal'"),
           "apote-lẖ": entry("apote-lẖ", "great envoy, chief envoy"), "pesto": entry("pesto", "viceroy (see peseto)"),
           "pqr": entry("pqr", "'prince' or 'vizier'"), "p- (2)": entry("p- (2)", "a prefix p- in some nouns (pwide / wide, pqr / qr)"),
           "at (1)": entry("at (1)", "priest", "a variant of ant 'priest' in three texts")}
    loans = {"apote", "peseto", "ant"}
    out = N.reductions(sorted(N.BY_NAME), [], lex, loans)
    assert all(not out[h][0] and out[h][1].startswith("by name, ") for h in N.BY_NAME)
    assert out["qor"][1] == "by name, a form of qore, a word the correspondences were built from: qore with the article (the lexicon's entry qor)"
    assert out["ḫ- (1)"][1].endswith("(the lexicon's entry ḫlẖl)")                         # its own entry does not name ḫre: ḫlẖl's does
    assert out["at (1)"][1].startswith("by name, built on ant, a loan by both readers")      # a proposal of the entry names it
    assert out["pqr"][1].endswith("p- + qr, qr a form of qore (the lexicon's entry p- (2))")   # p- (2) names pqr and qr
    no_qr = N.reductions(["pqr"], [], {**lex, "p- (2)": entry("p- (2)", "a prefix p- in some nouns (pwide / wide)")}, loans)
    assert no_qr["pqr"][0] and "does not name pqr and qr" in no_qr["pqr"][1]                 # an entry that does not analyse it: kept
    assert N.named_in("ḫre", lex["ḫlẖl"]) and N.named_in("apote", lex["apote-lẖ"]) and not N.named_in("ḫre", lex["ḫ- (1)"])
    assert not N.named_in("ato", entry("x", "a variant of atom")) and not N.named_in("ant", entry("x", "a plant"))   # a word of its own
    wrong = N.reductions(["mse", "pesto", "apote-lẖ"], [], {**lex, "mse": entry("mse", "a variant of mde")}, {"apote"})
    assert wrong["mse"][0] and "mse does not name mte" in wrong["mse"][1]                  # the entry does not say so: kept
    assert wrong["pesto"][0] and "or peseto is not a loan" in wrong["pesto"][1]             # not a loan by both readers: kept
    assert not wrong["apote-lẖ"][0]
    assert N.reductions(["ḫ- (1)", "ḫbḫne", "ḫr"], [], {}, set())["ḫbḫne"] == (False, "counted once, in the family of ḫ- (1), a stem under three letters")


def test_function_words_are_taken_out_before_the_keys():
    assert N.keys_of("their (plural possessive pronoun)") == {"plural", "possessive", "pronoun"}
    assert N.keys_of("before; in someone's presence") == {"presence"} and N.keys_of("this, this one (variant of qo)") == frozenset()
    assert N.keys_of("god; very likely also goddess") == {"god", "goddess"} and N.keys_of("another form of yesebe") == {"yesebe"}
    assert N.keys_of("to go out with them and with him") == frozenset() and N.keys_of("") == frozenset()
    assert N.keys_of("probably a form of mlowi (noun)") == {"mlowi"} and N.keys_of("verb stem 'eat'; with the causative prefix") == {"stem", "eat", "causative"}
    assert N.keys_of("a blessing or favour (positive sense)") == {"blessing", "favour", "positive"}    # words that speak of words (23:15)
    meta = "noun verb adjective adverb particle suffix prefix ending word meaning sense".split()
    assert {w for m in meta for w in (m, m + ("es" if m.endswith("x") else "s"))} <= N.FUNCTION_WORDS
    for text in ("water, and perhaps 'river' or 'Nile'", "a kind of sacrifice; per unclear", "to take, to receive", "Kandake, Candace"):
        assert N.keys_of(text) == N.cr.cognates.keys(text) - N.FUNCTION_WORDS                 # the engine's keys, less the list
    content = "water king ruler give take kill god goddess man woman child mother father brother sister bread meal milk cow dog bull " \
              "great good small young old new south north west east name title priest land sun foot hand eye head house day".split()
    assert not N.FUNCTION_WORDS & set(content) and {"perhaps", "probably", "see", "also", "variant", "form", "cf", "kind", "sort", "type"} <= N.FUNCTION_WORDS


def test_the_meanings_are_taken_in_the_pages_order():
    lex = {"a": {"meaning": "the lexicon's a"}, "b": {"meaning": "the lexicon's b"}, "c": {"meaning": "the lexicon's c"}, "d": {"meaning": ""}}
    table = {"a": "our a"}
    layers = [("recurring", [{"item": "b", "why": "stated", "level": "meaning", "gloss": "b by a layer"},
                             {"item": "b", "why": "stated", "level": "meaning", "gloss": "b by a layer"},
                             {"item": "b", "why": "form", "level": "meaning", "gloss": "not stated"}]),
              ("rare_later", [{"item": "b", "why": "stated", "level": "meaning", "gloss": "b once"}])]
    by = {"a": "layer recurring", "b": "layer recurring", "c": "the lexicon", "d": "the lexicon"}
    assert N.wording("a", lex, table, layers, by) == ("our a", "the public table")            # the table first, even for a layer's word
    assert N.wording("b", lex, table, layers, by) == ("b by a layer", "the layers' lines")    # the wording stated most often
    assert N.wording("c", lex, table, layers, by) == ("the lexicon's c", "the lexicon")
    assert N.wording("d", lex, table, layers, by) == ("", "the lexicon")
    assert all(v.strip() == v and v for v in N.the_table().values()) and N.the_table()["mẖe"] == "abundant, plentiful"


def test_the_engines_lists_against_the_pages():
    assert {N.bare(w) for w in cr.RULE_WORDS} == set(N.RULE_WORDS)                        # the same 22 words
    e = the_list()["engine"]
    assert e["rule_words_only_in_the_engine"] == e["rule_words_only_on_the_page"] == []
    assert e["loans_only_in_the_engine"] == ["ssor"]                                      # the page's list decides: ssor stays
    kept = {w["headword"] for w in the_list()["words"] if w["kept"]}
    assert "ssor" in kept and not kept & set(e["loans_only_on_the_page"])
    d = N.engine_differences({"ssor", "ant", "adb", "mlo"}, {"ant", "adb"})
    assert d["loans_only_in_the_engine"] == ["ssor"] and d["loans_only_on_the_page"] == ["adb"]


def test_words_of_leaves_out_a_word_without_a_key():
    words, left = N.words_of([("ato", "water"), ("x (1)", ""), ("y", "to be"), ("tk (2)", "to love, to revere"), ("qe (1)", "this, this one")])
    assert [w[0] for w in words] == ["ato", "tk (2)"] and left == ["x (1)", "y", "qe (1)"]
    assert words[1][1] == frozenset({"love", "revere"})                                   # the engine's own keys


def test_the_list_is_the_count_of_the_local_files():
    needs(*THE_MAP, *NES_LISTS, "data/sources/nubian/known_words_local.json")
    public, local = N.word_list()
    assert public == the_list() and local == N.read("known_words_local.json")
    assert [w["headword"] for w in local["words"]] == sorted(w["headword"] for w in public["words"] if w["kept"])
    words, no_key = N.known_words()
    assert len(words) + len(no_key) == public["counts"]["kept"] and len(no_key) == public["counts"]["kept_without_a_key"]
    assert len({f for f, _, _ in words}) == len(words)                                    # one row of scores a word
    assert all(cr.pattern(f) for f, _, _ in words)                                        # the engine reads every headword
    table = N.the_table()
    for w in local["words"]:                                                              # the meaning in the page's order
        assert (w["meaning"] == table[w["headword"]]) if w["wording_from"] == "the public table" else w["headword"] not in table
        assert w["meaning"] == w["lexicon_meaning"].strip() or w["wording_from"] != "the lexicon"
        assert w["wording_from"] != "the layers' lines" or w["meaning_from"] != "the lexicon"
        assert w["keys"] == sorted(N.keys_of(w["meaning"]))
    assert {w["headword"] for w in local["words"] if not w["keys"]} == {"dḫno", "qe (1)"}  # 'another form of ydḫno', 'this, this one'
    with set_to(N, COUNTS=N.COUNTS | {"left": 126}):
        assert stops(N.word_list, "nothing is written")


def test_the_second_pages_are_the_lot():
    rng = random.Random(N.SEED_SECOND)
    assert tuple(sorted(rng.sample(range(333, 521), 19))) == N.SECOND["R"]
    assert tuple(sorted(rng.sample(range(410, 562), 15))) == N.SECOND["L"]
    assert sum(map(len, N.SECOND.values())) == 34
    assert len(N.indexes("R")) == 188 and len(N.indexes("L")) == 152
    assert all(i in N.indexes(b) for b, idx in N.SECOND.items() for i in idx)


# ------------------------------------------------------------------------------------------------- merge

def test_merge_joins_clean_pages():
    with a_home() as home:
        clean_pages(home / "typed")
        rows, rep = N.merge_of(home / "typed", SMALL)
        assert rep["pages"] == {"expected": 6, "merged": 6, "failed": 0, "missing": 0} and not rep["failed"] and not rep["other_files"]
        assert (rep["entries"], rep["subrows"]) == (7, 4) == (sum(not r["parent"] for r in rows), sum(bool(r["parent"]) for r in rows))
        assert rep["by_book"]["R"] == {"pages": 4, "pages_without_a_row": 1, "entries": 5, "subrows": 3, "marked_as_loans": 1, "continued": 2, "unsure": 1}
        assert rep["by_book"]["L"]["marked_as_loans"] == 1 and rep["loan_marks"] == {"Ar": 1, "*": 1} and rep["dialect_parts_not_of_the_books"] == {}
        typed(home / "typed", "R", 335, [dict(headword="Bad", de="x", en="x", loan="-", dialect="Derr"), dict(headword="Bal", de="y", en="y", loan="none")])
        assert N.merge_of(home / "typed", SMALL)[1]["loan_marks"] == {"Ar": 1, "*": 1, "-": 1, "none": 1}   # each shows before the gate drops it
        assert N.merge_of(home / "typed", SMALL)[1]["dialect_parts_not_of_the_books"] == {"DERR": 1}
        clean_pages(home / "typed")
        assert [r["headword"] for r in rows][:4] == ["Āb", "āb-kiñ", "Agar", "agar-ti"]                 # the order of the pages
        assert all(list(r) == N.COLUMNS for r in rows)
        assert rows[0] == {"book": "R", "page": "1", "headword": "Āb", "dialect": "KD", "loan": "", "pos": "n", "gloss_de": "vater", "gloss_en": "father", "parent": ""}
        assert rows[-1]["page"] == str(411 - 147) and rows[-1]["parent"] == "kitāb"
        cells = line("L", 410, 1, "ā", "herz", "heart", "M").split("\t")
        (home / "typed" / "L0410.tsv").write_text("\n".join(["\t".join(N.HEADER), "\t".join(cells[:2] + ["xii"] + cells[3:]), "# entries=1 subrows=0"]), encoding="utf-8")
        rows, rep = N.merge_of(home / "typed", SMALL)
        assert not rep["failed"] and [r["page"] for r in rows if r["book"] == "L"] == ["263", "264", "264"]     # counted from the index


def test_merge_attaches_a_continued_subrow():
    with a_home() as home:
        clean_pages(home / "typed")
        rows, rep = N.merge_of(home / "typed", SMALL)
        by = {r["headword"]: r for r in rows}
        assert by["agar-ti"]["parent"] == "Agar" and by["agar-ti"]["page"] == "2"         # the last entry of the page before
        assert by["aman-dō"]["parent"] == "Aman"                                          # across a page without an entry
        assert rep["continued_not_attached"] == []
        typed(home / "typed", "R", 333, [dict(headword="ab-ki", de="x", en="x", parent=N.CONTINUED), dict(headword="Agar", de="ort", en="place")])
        rows, rep = N.merge_of(home / "typed", SMALL)
        assert rep["continued_not_attached"] == ["R0333 row 1"] and rows[0]["parent"] == N.CONTINUED    # no page before the first
        typed(home / "typed", "R", 334, [dict(headword="Ai", de="ich", en="I"), dict(headword="agar-ti", de="örtlich", en="local", parent=N.CONTINUED)])
        rows, rep = N.merge_of(home / "typed", SMALL)
        assert {r["headword"]: r for r in rows}["agar-ti"]["parent"] == "Agar"            # the page before, wherever the row stands
        (home / "typed" / "R0335.tsv").unlink()
        rows, rep = N.merge_of(home / "typed", SMALL)
        assert "R0336 row 1" in rep["continued_not_attached"]                             # not across a missing page
        assert {r["headword"]: r for r in rows}["aman-dō"]["parent"] == N.CONTINUED


def test_merge_lists_a_wrong_count_and_does_not_repair_it():
    with a_home() as home:
        clean_pages(home / "typed")
        typed(home / "typed", "R", 334, [dict(headword="Ai", de="ich", en="I"), dict(headword="Aman", de="wasser", en="water")],
              count="# entries=3 subrows=0")
        before = (home / "typed" / "R0334.tsv").read_text(encoding="utf-8")
        rows, rep = N.merge_of(home / "typed", SMALL)
        assert rep["pages"] == {"expected": 6, "merged": 5, "failed": 1, "missing": 0}
        assert rep["failed"] == {"R0334": ["the count line says entries=3 subrows=0, the rows are entries=2 subrows=0"]}
        assert not any(r["headword"] in ("Ai", "Aman") for r in rows)                     # the page is left out
        assert (home / "typed" / "R0334.tsv").read_text(encoding="utf-8") == before       # and the file is as it was
        assert {r["headword"]: r for r in rows}["aman-dō"]["parent"] == N.CONTINUED       # nothing is attached across it


def test_merge_lists_a_missing_index_and_a_stray_file():
    with a_home() as home:
        clean_pages(home / "typed")
        (home / "typed" / "L0411.tsv").unlink()
        (home / "typed" / "R0337.tsv").write_text("x\n", encoding="utf-8")
        (home / "typed" / "notes.txt").write_text("x\n", encoding="utf-8")
        rows, rep = N.merge_of(home / "typed", SMALL)
        assert rep["missing"] == ["L0411"] and rep["pages"]["missing"] == 1 and rep["pages"]["merged"] == 5
        assert rep["other_files"] == ["R0337.tsv", "notes.txt"] and not any(r["headword"] == "kitāb" for r in rows)
        assert N.merge_of(home / "none", SMALL)[1]["pages"] == {"expected": 6, "merged": 0, "failed": 0, "missing": 6}


def test_a_page_is_checked_line_by_line():
    with a_home() as home:
        f = home / "typed"
        good = [dict(headword="Ai", de="ich", en="I"), dict(headword="ai-gi", de="mich", en="me", parent="Ai")]

        def fails(text=None, **kw):
            if text is None:
                typed(f, "R", 333, kw.pop("rows", good), **kw)
            else:
                (f / "R0333.tsv").write_text(text, encoding="utf-8")
            rows, why = N.read_page(f / "R0333.tsv", "R", 333)
            assert (rows is None) == bool(why)
            return why

        head, a, b = "\t".join(N.HEADER), line("R", 333, 1, "Ai", "ich", "I"), line("R", 333, 2, "ai-gi", "mich", "me", parent="Ai")
        end = "# entries=1 subrows=1\n"
        assert fails() == [] and len(N.read_page(f / "R0333.tsv", "R", 333)[0]) == 2
        assert fails("\ufeff" + "\r\n".join([head, a, b, end.strip(), "", ""])) == []     # a mark of the file, not of the page
        assert fails(header="\t".join(N.HEADER[:-1])) == ["the first line is not the header"]
        assert fails("\n".join([head, a, b]) + "\n") == ["the last line is not the count line"]
        assert fails("\n".join([head, a, b, "# entries=1 subrows=1 "]) + "\n") == []     # a space after the count is no letter
        assert fails("\n".join([head, a, b, "# entries=1"]) + "\n") == ["the last line is not the count line"]
        assert fails("\n".join([head, a, b, "# entries=one subrows=1"]) + "\n") == ["the last line is not the count line"]
        assert fails(head + "\n") == ["the last line is not the count line"]
        assert fails("\n".join([head, a, line("R", 333, 3, "ai-gi", "mich", "me", parent="Ai"), end])) == ["n does not run from 1: row 2 has n=3"]
        assert fails("\n".join([head, a, b.rsplit("\t", 1)[0], end])) == ["line 3 has 13 cells, not 14", "the count line says entries=1 subrows=1, the rows are entries=1 subrows=0"]
        assert fails("\n".join([head, a, line("R", 334, 2, "ai-gi", "mich", "me", parent="Ai"), end])) == ["row 2 names another book or index"]
        assert fails("\n".join([head, a, line("L", 333, 2, "ai-gi", "mich", "me", parent="Ai"), end])) == ["row 2 names another book or index"]
        assert fails("\n".join([head, a, line("R", 333, 2, "", "mich", "me", parent="Ai"), end])) == ["row 2 has no headword"]
        assert fails("\n".join([head, a, "# seite 2", b, end])) == ["line 3 is a comment the brief does not have"]
        assert fails("\n".join([head, a, "", b, end])) == ["line 3 has 1 cells, not 14"]
        assert fails(blank=True) == ["`# blank` in a page with rows"]
        assert fails(rows=[], blank=True) == [] and N.read_page(f / "R0333.tsv", "R", 333)[0] == []
        assert fails(rows=[]) == []                                                        # no row, and the count says so
        (f / "R0333.tsv").write_bytes("\t".join(N.HEADER).encode() + b"\n\xff\xfe\n")
        assert N.read_page(f / "R0333.tsv", "R", 333) == (None, ["the file is not UTF-8"])


def test_the_dictionary_is_read_as_written():
    with a_home() as home:
        rows = [{"book": "R", "page": "1", "headword": "Āb", "dialect": "KD", "loan": "", "pos": "n", "gloss_de": 'vater; "alter"', "gloss_en": "father", "parent": ""},
                {"book": "R", "page": "1", "headword": "āb-kiñ", "dialect": "", "loan": "", "pos": "", "gloss_de": "waise", "gloss_en": "", "parent": "Āb"}]
        N.write_dictionary(rows, home / "dictionary.tsv")
        assert N.read_dictionary(home / "dictionary.tsv") == rows                          # a quote mark is a letter like any other
        (home / "dictionary.tsv").write_text("book\tpage\n", encoding="utf-8")
        assert stops(lambda: N.read_dictionary(home / "dictionary.tsv"), "header")


# ---------------------------------------------------------------------------------------------- agree

def twenty(change=None):
    """Twenty made-up entries of one page; `change(n, row)` may alter the second typist's copy of row n."""
    rows = [dict(headword=f"tā{c}ar", de=f"das {c}-wort und sein gebrauch", en=f"the {c} word") for c in "bdfgklmnprstwxyzhjcv"]
    if change is None:
        return rows
    return [r for r in (change(n, dict(r)) for n, r in enumerate(rows, 1)) if r is not None]


def agreed(second, first=None, subs=((), ())):
    with a_home() as home:
        typed(home / "typed", "R", 334, (first or twenty()) + list(subs[0]))
        typed(home / "typed2", "R", 334, second + list(subs[1]))
        return N.agree_of(home / "typed", home / "typed2", {"R": (334,)})


def test_agree_meets_the_bar():
    def other_marks(n, r):
        if n <= 4:
            r["headword"] = r["headword"].replace("ā", "a").capitalize()                # the length mark and the case
        if n == 5:
            r["headword"] = r["headword"].replace("ar", "ár")                           # an accent
        if n == 6:
            r["de"] = r["de"].replace("gebrauch", "Gebrauche")                          # nearly the same meaning
        return r
    res = agreed(twenty(other_marks))
    e = res["entries"]
    assert res["verdict"] == "met" and res["pages"] == {"drawn": 1, "compared": 1, "not_compared": 0}
    assert (e["first"], e["second"], e["found"], e["same_meaning"], e["mark_for_mark"]) == (20, 20, 20, 20, 15)
    assert (e["found_share"], e["same_meaning_share"], e["mark_for_mark_share"]) == (1.0, 1.0, 0.75)
    assert res["bars"] == {"found": 0.95, "same_meaning": 0.90, "likeness": 0.8}
    one_gone = agreed(twenty(lambda n, r: None if n == 20 else r))
    assert one_gone["entries"]["found_share"] == 0.95 and one_gone["verdict"] == "met"   # 19 of 20 is at the bar
    two_other = agreed(twenty(lambda n, r: r | {"de": "etwas ganz anderes"} if n <= 2 else r))
    assert two_other["entries"]["same_meaning_share"] == 0.9 and two_other["verdict"] == "met"    # 18 of 20 is at the bar


def test_agree_misses_on_the_headwords():
    res = agreed(twenty(lambda n, r: r | {"headword": r["headword"].replace("t", "d")} if n <= 2 else r))
    e = res["entries"]
    assert (e["found"], e["found_share"], e["same_meaning_share"]) == (18, 0.9, 1.0) and res["verdict"] == "missed"
    page = res["by_page"]["R0334"]["entries"]
    assert page["not_found"] == ["tābar", "tādar"] and page["only_in_the_second"] == ["dābar", "dādar"] and page["other_meaning"] == []
    assert agreed(twenty(lambda n, r: None if n >= 19 else r))["verdict"] == "missed"    # two of twenty not typed


def test_agree_misses_on_the_meanings():
    res = agreed(twenty(lambda n, r: r | {"de": "etwas ganz anderes"} if n <= 3 else r))
    e = res["entries"]
    assert (e["found"], e["same_meaning"], e["same_meaning_share"]) == (20, 17, 0.85) and res["verdict"] == "missed"
    other = res["by_page"]["R0334"]["entries"]["other_meaning"]
    assert len(other) == 3 and other[0]["headword"] == "tābar" and other[0]["likeness"] < 0.8
    assert N.likeness("Der Vater", "der vater ") == 1.0 and N.likeness("vater", "mutter") < 0.8
    assert abs(N.likeness("abcde", "abcdx") - 0.8) < 1e-12                               # 0.8 is the same meaning
    senses = ("feuer; eine; haut; wasser; strom; gehen; salz; mond; kommen; milch; gehen; vogel; ein; mond; milch; kommen; wasser; eine; milch; "
              "und; strom; stern; haut; machen; fleisch; fisch; fleisch; vogel; nemen; milch; knochen")
    assert len(senses) > 200 and N.likeness(senses, senses.split("; ", 1)[1]) > 0.95     # a long meaning is compared letter by letter


def test_what_the_bar_sets_aside():
    same = [("Āb", "ab"), ("tā́r", "tar"), ("kídē", "KIDE"), ("àgar", "agár"), ("ûr", "ur"), (" aman ", "aman"),
            ("ǵer", "ġer"), ("ǧer", "ǵer"), ("ñog", "ńog")]                                  # one printed mark rendered two ways
    assert all(N.letters(a) == N.letters(b) for a, b in same)                            # length, accent, any mark on a vowel, case
    other = [("šā", "sā"), ("ža", "za"), ("ñog", "nog"), ("aṅ", "an"), ("ǵer", "ger"), ("ńog", "nog"), ("ǧer", "ger"), ("ṅog", "ńog"),
             ("ǰa", "ja"), ("au-tir", "autir"), ("au tir", "autir"), ("tar", "tarr"), ("taar", "tār")]
    assert all(N.letters(a) != N.letters(b) for a, b in other)                           # a mark that makes another consonant; a hyphen
    assert N.letters("Šā́ñ") == "šań" and N.letters(unicodedata.normalize("NFD", "ṅā")) == N.letters("ṅa") == "ṅa"
    for a, b in same[-3:] + [("ṅog", "ńog")]:                                          # the gate reads them as the bar counts them
        assert (N.sounds(a, "L") == N.sounds(b, "L")) == (N.letters(a) == N.letters(b))
    res = agreed(twenty(lambda n, r: r | {"headword": r["headword"].replace("g", "ġ")}), first=twenty(lambda n, r: r | {"headword": r["headword"].replace("g", "ǵ")}))
    e = res["entries"]
    assert (e["found"], e["mark_for_mark"], e["same_sounds"]) == (20, 19, 20)            # ǵ and ġ: one printed mark, one sound for the gate
    dot = agreed(twenty(lambda n, r: r | {"headword": r["headword"].replace("n", "ṅ")}), first=twenty(lambda n, r: r | {"headword": r["headword"].replace("n", "ń")}))
    assert (dot["entries"]["found"], dot["entries"]["same_sounds"]) == (19, 19)          # ṅ and ń: two letters of the print, two sounds


def test_agree_reports_the_subrows_apart():
    subs1 = [dict(headword="tāb-kā", de="x-wort", en="x", parent="tābar"), dict(headword="tāb-lā", de="y-wort", en="y", parent="tābar")]
    subs2 = [dict(headword="tāb-kā", de="x-wort", en="x", parent="tābar"), dict(headword="tāb-la", de="ganz anders", en="y", parent="tabar")]
    res = agreed(twenty(), subs=(subs1, subs2))
    s = res["subrows"]
    assert (s["first"], s["found"], s["same_meaning"], s["mark_for_mark"]) == (2, 2, 1, 1) and s["same_meaning_share"] == 0.5
    assert res["entries"]["found"] == 20 and res["verdict"] == "met"                     # the bar is on the entries
    none = agreed(twenty(), subs=(subs1, []))
    assert none["subrows"]["found_share"] == 0.0 and none["verdict"] == "met"


def test_agree_pairs_headwords_written_alike_by_their_meanings():
    first = [dict(headword="ār", de="nehmen, ergreifen", en="to take"), dict(headword="ar", de="wir", en="we")]
    second = [dict(headword="ar", de="wir", en="we"), dict(headword="ār", de="nemen, ergreifen", en="to take")]
    with a_home() as home:
        typed(home / "typed", "L", 411, first)
        typed(home / "typed2", "L", 411, second)
        res = N.agree_of(home / "typed", home / "typed2", {"L": (411,)})
    e = res["entries"]
    assert (e["found"], e["same_meaning"], e["mark_for_mark"]) == (2, 2, 2)
    one = N.compare([dict(headword="ar", gloss_de="wir", parent="")] * 2, [dict(headword="ār", gloss_de="wir", parent="")], "L")
    assert (one["found"], one["not_found"]) == (1, ["ar"])                               # a row of the second reading is used once


def test_agree_does_not_decide_without_every_page():
    with a_home() as home:
        typed(home / "typed", "R", 334, twenty())
        typed(home / "typed2", "R", 334, twenty())
        typed(home / "typed", "R", 336, twenty())
        res = N.agree_of(home / "typed", home / "typed2", {"R": (334, 336)})
        assert res["verdict"] == "not decided" and res["not_compared"] == {"R0336": {"first": [], "second": ["the file is missing"]}}
        assert res["pages"] == {"drawn": 2, "compared": 1, "not_compared": 1} and res["entries"]["found_share"] == 1.0
        typed(home / "typed2", "R", 336, twenty(), count="# entries=19 subrows=0")
        res = N.agree_of(home / "typed", home / "typed2", {"R": (334, 336)})
        assert res["verdict"] == "not decided" and "count line" in res["not_compared"]["R0336"]["second"][0]
        typed(home / "typed2", "R", 336, twenty())
        both = N.agree_of(home / "typed", home / "typed2", {"R": (334, 336)})
        assert both["verdict"] == "met" and both["entries"]["first"] == 40 and both["by_book"]["R"]["entries"]["found"] == 40
    assert N.typing_verdict({"first": 0, "found": 0, "same_meaning": 0}, {}) == "not decided"


# ------------------------------------------------------------------------------------- the letters for the engine

def seg(s):
    return tuple(s)


def test_typed_headwords_become_the_engines_segments():
    for typed_as, book, segs in [
            ("kā́b", "R", "kab"), ("Tā", "L", "ta"),                                      # the macron of length, the acute, the case
            ("wíssi", "R", "wisi"), ("kidē", "R", "kide"),                                # a doubled consonant is one, as in the engine
            ("yā", "R", "ya"), ("zibir", "R", "zibir"), ("jug", "R", "jug"),              # y, z and j are the engine's own
            ("ǰer", "R", "jer"), ("j́er", "R", "jer"),                                    # a j with a mark
            ("ǵēr", "L", "jer"), ("ġēr", "L", "jer"), ("ǧēr", "R", "jer"), ("burǵ", "L", "burj"),    # a g with any mark is the palatal
            ("gorǵo", "L", "gorjo"),                                                      # and a plain g stays g
            ("taq", "L", "tak")]:                                                         # q outside Reinisch: as the engine reads it
        assert N.sounds(typed_as, book) == seg(segs), typed_as
    assert N.sounds("šoñ", "R") == ("ʃ", "o", "ɲ") and N.sounds("Šā", "R") == ("ʃ", "a")
    assert N.sounds("žuk", "R") == seg("juk")                                             # ž: the engine's j, like ʒ
    assert N.sounds("aṅissi", "L") == ("a", "ŋ", "i", "s", "i") == N.sounds("AṄISSI", "L")
    assert N.sounds("diṅ", "L") == ("d", "i", "ŋ") and N.sounds("ńog", "L") == ("ɲ", "o", "g") == N.sounds("ñog", "R")
    assert N.sounds("taq", "R") == seg("tac") and N.sounds("iqi", "R") == seg("ici")      # Reinisch's q is a palatal
    assert N.sounds(unicodedata.normalize("NFD", "ṅā"), "R") == N.sounds("ṅā", "R") == ("ŋ", "a")
    assert cr.segments("aṅ") == seg("an") and cr.segments("ǵer") == seg("ger")            # what the engine alone would read
    assert N.spelling("Āb-kiñ", "R") == "āb-kiñ" and N.spelling("áṅ-ǵi") == "áŋ-ɟi"       # the rest is left as typed
    rows, _ = N.engine_rows([dict(book="R", page="1", headword="au-tir", dialect="K", loan="", pos="v", gloss_de="x", gloss_en="to serve", parent="")])
    assert [v for v, _ in rows[0].variants] == ["autir", "au", "tir"]                     # a hyphen: the engine's own pieces


def test_dialect_marks_become_the_engines_languages():
    assert N.languages("K") == (("kenzi",), "") and N.languages("D") == (("dongolawi",), "")
    assert N.languages("F") == N.languages("M") == N.languages("FM") == (("nobiin",), "")
    assert N.languages("KD") == (("kenzi", "dongolawi"), "") and N.languages("MKD") == (("nobiin", "kenzi", "dongolawi"), "")
    assert N.languages("") == ((), "") and N.languages("K. D.") == (("kenzi", "dongolawi"), "")
    assert N.languages("KX") == ((), "KX") and N.languages("Ar") == ((), "AR")              # no dialect mark of the books: no language
    assert {cr.group(l) for l in N.DIALECTS.values()} == {"nubian"} == {cr.group(N.UNMARKED)}      # one set of correspondences
    assert cr.align("kdi", seg("kari"), "kenzi") == cr.align("kdi", seg("kari"), "dongolawi") == cr.align("kdi", seg("kari"), "nobiin")


def d(headword, en, dialect="", loan="", parent="", book="R"):
    return {"book": book, "page": "1", "headword": headword, "dialect": dialect, "loan": loan, "pos": "n", "gloss_de": "x", "gloss_en": en, "parent": parent}


def test_dictionary_rows_for_the_engine():
    rows, c = N.engine_rows([
        d("Āb", "father", "KD"), d("āb-kiñ", "orphan", parent="Āb"),                      # two languages; the sub-row takes them
        d("Agar", "place", "FM"), d("Aman", "water"),                                     # one language; no mark
        d("Bāb", "door", "K", loan="Ar"), d("bāb-ki", "of the door", parent="Bāb"),       # a loan and its sub-row
        d("Dū", "", "K"), d("---", "nothing", "K"),                                       # no English meaning; no letter
        d("ar-kā", "us", "D", parent="Arr"),                                              # the parent is typed otherwise
        d("ā", "heart", "M", book="L"), d("kitāb", "book", "MKD", loan="*", book="L"), d("xoǵ", "odd", "KZ", book="L")])
    got = [(r.lang, r.form, r.dataset) for r in rows]
    assert got == [("kenzi", "Āb", "reinisch1879"), ("dongolawi", "Āb", "reinisch1879"), ("kenzi", "āb-kiñ", "reinisch1879"),
                   ("dongolawi", "āb-kiñ", "reinisch1879"), ("nobiin", "Agar", "reinisch1879"), ("nobiin", "Aman", "reinisch1879"),
                   ("dongolawi", "ar-kā", "reinisch1879"), ("nobiin", "ā", "lepsius1880"), ("nobiin", "xoǵ", "lepsius1880")]
    assert c["entries_read"] == 9 and c["subrows_read"] == 3 and c["loans_left_out"] == 2 and c["subrows_of_loans_left_out"] == 1
    assert c["without_an_english_meaning"] == 1 and c["without_a_letter_the_engine_reads"] == 1 and c["without_a_key"] == 1   # "us"
    assert c["compared"] == 7 and c["rows"] == 9 and c["without_a_dialect"] == 2 and c["subrows_under_the_entry_before"] == 1
    assert c["rows_by_list"] == {"reinisch1879": 7, "lepsius1880": 2} and c["rows_by_language"] == {"kenzi": 2, "dongolawi": 3, "nobiin": 4}
    assert c["dialect_marks_not_of_the_books"] == {"KZ": 1} and c["letters_the_engine_does_not_read"] == {}
    water = rows[5]
    assert water.keys == frozenset({"water"}) and water.gloss == "water" and water.variants == (("aman", seg("aman")),)
    assert rows[2].keys == frozenset({"orphan"}) and rows[2].variety == "KD"
    homonym, _ = N.engine_rows([d("ar", "we", "K", loan="Ar"), d("ar", "to take", "D"), d("ar-ki", "taken", parent="ar")])
    assert [(r.lang, r.form) for r in homonym] == [("dongolawi", "ar"), ("dongolawi", "ar-ki")]      # the nearest entry before it
    over, c = N.engine_rows([d("Bāb", "door", "K", loan="Ar"), d("bāb-ki", "of the door", parent="Bāb") | {"page": "2"},    # begun on the page before
                             d("ar", "we", "K", loan="Ar") | {"page": "2"}, d("ār", "to take", "D") | {"page": "3"},
                             d("ār-ki", "taken", parent="ar") | {"page": "3"}])            # not the `ar` of another page
    assert [(r.lang, r.form) for r in over] == [("dongolawi", "ār"), ("dongolawi", "ār-ki")]
    assert c["subrows_of_loans_left_out"] == 1 and c["subrows_under_the_entry_before"] == 2
    alone, c = N.engine_rows([d("ab-ki", "orphan", parent=N.CONTINUED)])                   # no entry before it at all
    assert [(r.lang, r.form) for r in alone] == [("nobiin", "ab-ki")] and c["without_a_dialect"] == 1


def test_the_cells_as_the_typists_filled_them():
    """The shapes the typists' notes name (data/sources/nubian/typists_notes.json), each read without a guess."""
    # 1. A dialect cell: letters run together, groups split by commas, a place in the dialect's place.
    assert N.languages("K, D") == N.languages("KD") == (("kenzi", "dongolawi"), "")
    assert N.languages("K, DF, M") == N.languages("KDFM") == N.languages("KDF, FM") == (("kenzi", "dongolawi", "nobiin"), "")
    assert N.languages("D, K, FM") == (("dongolawi", "kenzi", "nobiin"), "") and N.languages("MK.") == (("nobiin", "kenzi"), "")
    assert N.languages("Derr") == ((), "DERR") and N.languages("M (Burckh.)") == (("nobiin",), "BURCKH")    # not D for Dongola
    # 2. Two or three forms in one headword cell; the first is the headword.
    for cell, fs in [("Bīr, bírri", ["Bīr", "bírri"]), ("Ard, árid", ["Ard", "árid"]), ("Kúsu und kússu", ["Kúsu", "kússu"]),
                     ("Dalū, auch dallū", ["Dalū", "dallū"]), ("Kull meist kúlli", ["Kull", "kúlli"]), ("Un, unni, unn", ["Un", "unni", "unn"]),
                     ("Nebs, nébis, seltener nefs", ["Nebs", "nébis", "nefs"]), ("Hilgē (D), halgē (K), hálig (FM)", ["Hilgē", "halgē", "hálig"]),
                     ("Kāše M. kašere D.", ["Kāše", "kašere"]), ("Kīdire MK. kīdere D.", ["Kīdire", "kīdere"]), ("Doin (doṅ?)", ["Doin", "doṅ?"]),
                     ("Mūr, -kā", ["Mūr", "-kā"]), ("-in, -n", ["-in", "-n"]), ("Rāī und ógij rāī", ["Rāī", "ógij rāī"]),
                     ("ói-n fóki", ["ói-n fóki"]), ("kúl(l)i", ["kúl(l)i"]), ("Fart (?)", ["Fart"]), ("Iā!", ["Iā!"])]:
        assert N.forms(cell) == fs and N.headword_of(cell) == fs[0], (cell, N.forms(cell))
    assert [v for v, _ in N.variants_of("Bīr, bírri", "R")] == ["bīr", "bírri"]                # every form a variant of the row
    assert [v for v, _ in N.variants_of("Ingir, ingira, ingir-rā", "L")] == ["ingir", "ingira", "ingirrā"]
    assert [v for v, _ in N.variants_of("Mūr, -kā", "L")] == ["mūr"] and [v for v, _ in N.variants_of("jom-bay, -bai, -bä", "R")] == ["jombay", "jom"]
    assert [v for v, _ in N.variants_of("-in, -n", "L")] == ["in", "n"]                         # a suffix entry keeps its forms
    assert [v for v, _ in N.variants_of("kúl(l)i", "R")] == ["kúli", "kúl", "kúlli"]            # the engine's own reading of brackets
    # A sub-row's parent repeats the whole cell, or names its first form.
    rows, c = N.engine_rows([d("Bīr, bírri", "well", "KD"), d("bīr-ti", "small well", parent="Bīr, bírri"), d("bīr-kā", "the well", parent="Bīr"),
                             d("Bīr, bírri", "well", "FM") | {"page": "2"}, d("bir-ri", "spring", parent=N.CONTINUED) | {"page": "3"}])
    assert c["subrows_under_the_entry_before"] == 1 and [r.lang for r in rows if r.form == "bīr-kā"] == ["kenzi", "dongolawi"]
    assert [r.lang for r in rows if r.form == "bir-ri"] == ["nobiin"]                          # a page begun inside an entry: the entry before
    rows, c = N.engine_rows([d("Kúsu", "laziness", "M"), d("Ard", "earth", "K"), d("kúsu-ti", "lazy", parent="Kúsu, kússu")])
    assert c["subrows_under_the_entry_before"] == 0 and [r.lang for r in rows if r.form == "kúsu-ti"] == ["nobiin"]   # its first form names it
    # 3. Any loan mark drops the entry and its sub-rows, and nothing else does.
    marks = ["Ar", "*", "Kopt", "Tigré", "Amh.", "Altegypt.", "Aeg.", "Aeg, Kopt, Ar", "Sudan-Ar.", "vulg. Ar.", "vgl. Ar.", "Ar?", "Gr",
             "aus τράπεζα", "identisch mit دروش", "Ar; spanisch", "* türkisch"]
    rows, c = N.engine_rows([d(f"Ka{n}", "word", "K", loan=m) for n, m in enumerate(marks)] + [d("ka0-ti", "of the word", parent="Ka0"),
                             d("Asāia", "a plant", "M", book="L") | {"note": "[ʿašāʾ] no star printed"}, d("Gobel", "a loan", "M", loan="*", book="L")])
    assert c["loans_left_out"] == len(marks) + 1 and c["subrows_of_loans_left_out"] == 1 and [r.form for r in rows] == ["Asāia"]
    # 4. An entry that runs over a page: its next page's derived words hang on it; a page begun inside an entry may have none.
    with a_home() as home:
        typed(home / "typed", "R", 333, [dict(headword="Bīr, bírri", de="brunnen", en="well", dialect="K, D", note="runs on")])
        typed(home / "typed", "R", 334, [dict(headword="bīr-ti", de="kleiner brunnen", en="small well", parent=N.CONTINUED),
                                         dict(headword="Bot", de="loch", en="hole", dialect="KDFM", note="runs on")])
        typed(home / "typed", "R", 335, [dict(headword="Dalū", de="eimer", en="bucket")])                 # no (continued) row
        typed(home / "typed", "R", 336, [], blank=True)
        rows, rep = N.merge_of(home / "typed", {"R": SMALL["R"]})
        assert not rep["failed"] and rep["continued_not_attached"] == [] and {r["headword"]: r for r in rows}["bīr-ti"]["parent"] == "Bīr, bírri"
        engine, _ = N.engine_rows(rows)
        assert [(r.lang, r.form) for r in engine if r.form == "bīr-ti"] == [("kenzi", "bīr-ti"), ("dongolawi", "bīr-ti")]
    # 5. Forms put in `see` or `note` are not scored: the row is its headword cell alone.
    see, _ = N.engine_rows([d("Defē", "boat", "KD") | {"see": "= FM defai", "note": "also printed: defai"}])
    assert [v for v, _ in see[0].variants] == ["defē"]


def test_the_german_meanings_are_compared_as_typed_but_for_the_long_s():
    assert N.likeness("weiſse farbe", "weiße farbe") == 1.0 == N.likeness("Geheimniß", "geheimniſs") == N.likeness("groſser", "großer")
    assert N.likeness("aus-ser", "außer") < 1.0 and N.german(unicodedata.normalize("NFD", "Mädchen ")) == "mädchen"
    first = [dict(headword="Bīr, bírri", de="der brunnen, weiſse", en="well"), dict(headword="Gōz", de="sand", en="sand")]
    second = [dict(headword="Bīr", de="der Brunnen, weiße", en="well", note="also printed: bírri"), dict(headword="Gōz", de="sand", en="sand")]
    with a_home() as home:
        typed(home / "typed", "L", 411, first)
        typed(home / "typed2", "L", 411, second)
        e = N.agree_of(home / "typed", home / "typed2", {"L": (411,)})["entries"]
    assert (e["found"], e["same_meaning"], e["mark_for_mark"]) == (2, 2, 2)                     # the first form of a cell is its headword


def test_a_later_form_can_carry_the_match():
    words = made_up(36)
    rows = N.engine_rows([d(f"Zuzuzu{n}, {regular(f)}", g, "K") for n, (f, _, g) in enumerate(words)])[0]
    alone = N.engine_rows([d(regular(f), g, "K") for f, _, g in words])[0]
    assert all(cr.rule_score(f, a) == cr.rule_score(f, b) for (f, _, _), a, b in zip(words, rows, alone))


# --------------------------------------------------------------------------------------------------- the gate

def made_up(n=36, seed=7):
    """n made-up Meroitic words of four consonants, each with a meaning of its own."""
    rng, forms = random.Random(seed), []
    while len(forms) < n:
        f = "".join(rng.choice("kdtrlnsbw") for _ in range(4))
        if f not in forms and len(set(f)) == 4:
            forms.append(f)
    return N.words_of(list(zip(forms, MEANINGS)))[0]


def regular(form):
    """The Nubian word the correspondences give a made-up form: initial l is d, initial d is t, medial d is r."""
    out = [("d" if c == "l" else "t" if c == "d" else c) if i == 0 else ("r" if c == "d" and i < len(form) - 1 else c) for i, c in enumerate(form)]
    return "ā".join(out) + "a"


def dictionary_of(words, turn=0):
    """A made-up dictionary: for each word the regular Nubian word, under its own meaning (turn=0) or under the
    meaning of the word `turn` places on; and rows of other meanings."""
    marks = ("K", "D", "FM", "KD", "")
    rows = [d(regular(f), words[(i + turn) % len(words)][2], marks[i % 5], book="RL"[i % 2]) for i, (f, _, _) in enumerate(words)]
    rows += [d(regular(f)[::-1], f"chair number {i}", "K") for i, (f, _, _) in enumerate(words[:12])]
    rows += [d("Bāb", words[0][2], "K", loan="Ar")]
    return N.engine_rows(rows)[0]


def short_of(words):
    return [cr.Row("midob", "x", g, frozenset(cr.cognates.keys(g)), "gld", "", ((v, seg(v)),))
            for g, v in [("table", "pim"), ("spoon", "fom"), (words[0][2], "pum"), (words[1][2], "mop")]]


def test_the_gate_passes_planted_regular_words():
    words = made_up()
    res = N.gate_of(words, short_of(words), dictionary_of(words))
    bar = res["all"]["rule"]["shuffle"]
    assert res["verdict"] == "met" and (bar["n"], bar["of"], bar["sims"], bar["seed"]) == (36, 36, 2000, 3)
    assert bar["p"] < 0.05 and bar["p"] == (bar["ge"] + 1) / 2001 and bar["stat"] > 0.9
    alone = res["dictionaries"]["rule"]["shuffle"]
    assert alone["n"] == 36 and alone["p"] < 0.05                                        # beside it: the dictionaries alone
    assert res["rows"] == {"short_lists": 4, "dictionaries": len(dictionary_of(words))} and res["words"] == 36
    assert res["all"]["rule"]["top1"]["precision"] > res["all"]["rule"]["top1"]["chance"] and res["all"]["rule"]["top1"]["words_with_a_hit"] >= 30
    assert res["all"]["rule"]["ranks"]["of_rows"] == sum(res["rows"].values()) and res["all"]["rule"]["ranks"]["in_the_top_10"] == 36
    assert set(res["all"]["raw"]) == set(res["all"]["rule"]) == {"shuffle", "by_length", "top1", "top10", "ranks"} == set(res["dictionaries"]["raw"])
    lengths = res["all"]["rule"]["by_length"]
    assert lengths["n"] == 36 and lengths["p"] < 0.05 and lengths["stat"] == bar["stat"] and sum(lengths["groups"].values()) == 36   # beside the bar
    assert len(res["pairs"]) == 36 and res["pairs"][0]["best"]["score"] >= res["pairs"][-1]["best"]["score"] > 0.9
    first = next(p for p in res["pairs"] if p["headword"] == words[0][0])
    assert first["best"]["form"] == regular(words[0][0]) and first["rows_of_the_same_meaning"] == first["of_them_in_the_dictionaries"] + 1
    assert first["best"]["list"] in ("reinisch1879", "lepsius1880") and "Bāb" not in {p["best"]["form"] for p in res["pairs"]}
    json.dumps(res)                                                                      # everything can be written


def test_the_bar_is_on_all_rows():
    words = made_up()
    short = [cr.Row("midob", regular(f), g, k, "gld", "", ((regular(f), cr.segments(regular(f))),)) for f, k, g in words]
    chairs = N.engine_rows([d(regular(f)[::-1], f"chair number {i}", "K") for i, (f, _, _) in enumerate(words)])[0]
    res = N.gate_of(words, short, chairs)                                                # the regular words stand in the short lists only
    assert res["verdict"] == "met" and res["all"]["rule"]["shuffle"]["n"] == 36
    assert res["dictionaries"]["rule"]["shuffle"]["n"] == 0 == res["dictionaries"]["raw"]["shuffle"]["n"]
    assert set(res["dictionaries"]["rule"]) == {"shuffle", "by_length"} and all(p["of_them_in_the_dictionaries"] == 0 for p in res["pairs"])


def test_the_shuffle_by_length_keeps_each_meaning_among_words_of_its_length():
    """A made-up case of the bias by_length() is beside the bar for: short words with broad meanings that match
    many rows, long words with narrow ones; no row is a cognate of any word. The engine's shuffle passes it; the
    shuffle within one length does not."""
    rng, cons = random.Random(0), "kdtrlnsbw"
    short = []
    while len(short) < 12:
        f = rng.choice(cons) + rng.choice(cons)
        short += [f] if f not in short else []
    long = ["".join(rng.choice(cons) for _ in range(6)) for _ in range(24)]
    words = [(f, frozenset({f"broad{i}"}), "") for i, f in enumerate(short)] + [(f, frozenset({f"narrow{i}"}), "") for i, f in enumerate(long)]
    rows = []
    for key, n in [(f"broad{i}", 150) for i in range(12)] + [(f"narrow{i}", 2) for i in range(24)]:
        for _ in range(n):
            v = "".join(rng.choice("kdtrlnsbwgmaeiou") for _ in range(rng.randint(3, 7)))
            rows.append(cr.Row("nobiin", v, "", frozenset({key}), "x", "", ((v, cr.segments(v)),)))
    t = cr.shuffle_test(words, rows, cr.matrix(words, rows, cr.rule_score), 500, 3)
    lengths = N.by_length(words, t, 500, 3)
    assert t["p"] < 0.05 < 0.2 < lengths["p"] and lengths["groups"] == {"2": 12, "4": 24} and lengths["stat"] == t["stat"]


def test_the_gate_is_the_engines_own_test():
    words = made_up()
    short, rows = short_of(words), dictionary_of(words)
    res = N.gate_of(words, short, rows)
    S = cr.matrix(words, short + rows, cr.rule_score)
    t = cr.shuffle_test(words, short + rows, S, 2000, 3)
    assert {k: t[k] for k in ("n", "of", "stat", "ge", "sims", "p")} == {k: v for k, v in res["all"]["rule"]["shuffle"].items() if k != "seed"}
    top = cr.top_test(words, short + rows, S, 2000, 3, 10)
    assert res["all"]["rule"]["top10"]["precision"] == top["prec"] and res["all"]["rule"]["top10"]["p"] == top["p"]
    raw = cr.shuffle_test(words, short + rows, cr.matrix(words, short + rows, cr.raw_score), 2000, 3)
    assert res["all"]["raw"]["shuffle"]["p"] == raw["p"] and res["all"]["raw"]["shuffle"]["stat"] == raw["stat"]
    alone = cr.shuffle_test(words, rows, cr.matrix(words, rows, cr.rule_score), 2000, 3)
    assert res["dictionaries"]["rule"]["shuffle"]["stat"] == alone["stat"] and res["dictionaries"]["rule"]["shuffle"]["ge"] == alone["ge"]


def test_the_gate_misses_when_the_words_are_not_regular():
    words = made_up()
    res = N.gate_of(words, short_of(words), dictionary_of(words, turn=5))
    bar = res["all"]["rule"]["shuffle"]
    assert bar["n"] == 36 and bar["p"] > 0.05 and res["verdict"] == "missed"
    assert bar["stat"] < 0.5 and res["dictionaries"]["rule"]["shuffle"]["p"] > 0.05 and res["all"]["rule"]["by_length"]["p"] > 0.05


def test_the_gate_does_not_decide_on_fewer_than_30_words():
    words = made_up(29)
    for turn in (0, 5):
        res = N.gate_of(words, short_of(words), dictionary_of(words, turn))
        assert res["all"]["rule"]["shuffle"]["n"] == 29 and res["verdict"] == "too small to decide"
    assert N.gate_of(words, short_of(words), dictionary_of(words))["all"]["rule"]["shuffle"]["p"] < 0.05       # though p is small
    some = made_up(36)
    few = N.gate_of(some, [], dictionary_of(some[:20]))                                  # 36 words, 20 with a row
    assert few["all"]["rule"]["shuffle"]["of"] == 36 and few["all"]["rule"]["shuffle"]["n"] == 20 and few["verdict"] == "too small to decide"
    assert N.verdict(29, 0.0005) == "too small to decide" == N.verdict(0, 1.0)
    assert N.verdict(30, 0.0499) == "met" and N.verdict(30, 0.05) == "missed" and N.verdict(107, 0.49) == "missed"
    none = N.gate_of(some, short_of(some)[:2], [])                                       # no row of the same meaning at all
    assert none["verdict"] == "too small to decide" and none["pairs"] == [] and set(none["all"]["rule"]) == {"shuffle", "by_length"}
    assert none["all"]["rule"]["by_length"] | {"seed": 0} == {"n": 0, "groups": {}, "stat": 0.0, "ge": 2000, "sims": 2000, "p": 1.0, "seed": 0}
    assert (N.GATE["p"], N.GATE["words"], N.GATE["sims"], N.GATE["seed"], N.GATE["short_rows"]) == (0.05, 30, 2000, 3, 5442)


def as_it_should_be(home):
    """What the gate asks for before it runs, written into a made-up home."""
    N.write("merge_report.json", {"pages": {"expected": 6, "merged": 6, "failed": 0, "missing": 0}})
    N.write("agree.json", {"verdict": "met"})
    N.write("known_words_local.json", {"words": []})
    (home / "dictionary.tsv").write_text("\t".join(N.COLUMNS) + "\n", encoding="utf-8")


def fake_git(*args):
    """git as the gate asks it: the commit the checkout stands on, and one text for the engine here and in its commit."""
    return "0123456789abcdef0123456789abcdef01234567" if args == ("rev-parse", "HEAD") else "the engine's text"


def test_the_gate_runs_once_on_a_committed_script_and_whole_dictionaries():
    with a_home() as home, set_to(N, git=fake_git, not_as_committed=lambda: []):
        as_it_should_be(home)
        assert N.ready() is None
        with set_to(N, not_as_committed=lambda: ["src/nubian.py"]):
            assert stops(N.ready, "not as committed: src/nubian.py")
        with set_to(N, git=lambda *a: "another text" if a[0] == "hash-object" else fake_git(*a)):
            assert stops(N.ready, "src/cognates_rules.py is not the file of 1b4f0ff")
        with set_to(N, git=lambda *a: ""):
            assert stops(N.ready, "src/cognates_rules.py is not the file of 1b4f0ff")          # no git, no run
        N.write("merge_report.json", {"pages": {"expected": 6, "merged": 5, "failed": 1, "missing": 0}})
        assert stops(N.ready, "1 pages fail a check and 0 are missing")
        N.write("merge_report.json", {"pages": {"expected": 6, "merged": 5, "failed": 0, "missing": 1}})
        assert stops(N.ready, "0 pages fail a check and 1 are missing")
        as_it_should_be(home)
        for v in ("missed", "not decided"):
            N.write("agree.json", {"verdict": v})
            assert stops(N.ready, f"the typing's bar is {v}")
        as_it_should_be(home)
        (home / "agree.json").unlink()
        assert stops(N.ready, "agree.json is missing")
        as_it_should_be(home)
        N.write("gate.json", {})
        assert stops(N.ready, "the gate is run once")


def test_what_is_committed_is_told_from_what_is_not():
    assert N.not_as_committed(("src/cognates_rules.py", "src/cognates.py")) == []          # the engine, as it stands
    assert N.not_as_committed(("runs/nubian/no_such_file.json",)) == ["runs/nubian/no_such_file.json"]
    assert N.git("hash-object", N.ENGINE) == N.git("rev-parse", f"{N.GATE['engine']}:{N.ENGINE}") != "" and N.GATE["engine"] == "1b4f0ff"
    assert set(N.FRAMEWORK) == {"src/nubian.py", "src/cognates_rules.py", "src/cognates.py", "runs/nubian/known_words.json"}


def test_the_commands_run_from_the_typed_pages_to_the_figures():
    words = made_up()
    with a_home() as home, tempfile.TemporaryDirectory() as out:
        f = home / "typed"
        pages = [("R", 333), ("R", 334), ("R", 335), ("R", 336), ("L", 410), ("L", 411)]
        for k, (book, index) in enumerate(pages):
            mine = [dict(headword=regular(w[0]).capitalize(), de=f"wort {i}", en=w[2], dialect=("K", "D", "FM", "KD", "")[i % 5])
                    for i, w in enumerate(words) if i % 6 == k]
            if k == 1:
                mine = [dict(headword="āb-kiñ", de="waise", en="orphan", parent=N.CONTINUED)] + mine + [dict(headword="Bāb", de="tür", en=words[0][2], loan="Ar")]
            typed(f, book, index, mine)
            if (book, index) in (("R", 334), ("L", 411)):
                typed(home / "typed2", book, index, [m | {"headword": m["headword"].lower()} for m in mine])
        listed = Path(out) / "known_words.json"
        listed.write_text(json.dumps({"counts": {"kept": 36}, "words": [{"headword": w[0], "kept": True} for w in words] + [{"headword": "zz", "kept": False}]}), encoding="utf-8")
        N.write("known_words_local.json", {"words": [{"headword": w[0], "meaning": w[2]} for w in words]})
        short = short_of(words)
        with set_to(N, BOOKS=SMALL, SECOND={"R": (334,), "L": (411,)}, LIST=listed, PUBLIC=Path(out) / "figures.json", git=fake_git,
                    not_as_committed=lambda: []), set_to(N.GATE, short_rows=len(short)), set_to(cr, load_nes=lambda: short):
            assert stops(N.gate, "merge_report.json is missing")
            quiet(N.merge)
            rep = N.read("merge_report.json")
            assert rep["pages"] == {"expected": 6, "merged": 6, "failed": 0, "missing": 0} and (rep["entries"], rep["subrows"]) == (37, 1)
            assert stops(N.gate, "agree.json is missing")
            quiet(N.agree)
            assert N.read("agree.json")["verdict"] == "met" and N.read("agree.json")["entries"]["mark_for_mark"] == 0
            quiet(N.gate)
            g = N.read("gate.json")
            assert g["verdict"] == "met" and g["commit"] == fake_git("rev-parse", "HEAD") and g["typing"] == "met"
            assert g["known_words"] == {"kept": 36, "compared": 36, "without_a_key": []} and g["all"]["rule"]["shuffle"]["n"] == 36
            assert g["dictionary"]["loans_left_out"] == 1 and g["dictionary"]["entries_read"] == 37 and g["dictionary"]["subrows_read"] == 1
            assert g["rows"]["short_lists"] == 4 and g["rows"]["dictionaries"] == g["dictionary"]["rows"] > 36
            assert stops(N.gate, "the gate is run once")
            quiet(N.public)
            figs = json.loads((Path(out) / "figures.json").read_text(encoding="utf-8"))
            assert figs == N.figures() and figs["gate_a1"]["verdict"] == "met" and figs["typed_twice"]["verdict"] == "met"
            assert figs["typed"]["pages"]["merged"] == 6 and figs["known_words"] == {"kept": 36}
            with set_to(N.GATE, short_rows=5):
                (home / "gate.json").unlink()
                assert stops(N.gate, "the short lists have 4 rows")
            N.write("known_words_local.json", {"words": [{"headword": w[0], "meaning": w[2]} for w in words[:35]]})
            assert stops(N.gate, "is not the list of runs/nubian/known_words.json")
        text = (Path(out) / "figures.json").read_text(encoding="utf-8")
        assert not any(w[0] in text or regular(w[0]) in text.lower() for w in words) and "orphan" not in text       # counts only


def test_the_figures_are_counts_only():
    def leaves(x, path=""):
        if isinstance(x, dict):
            for k, v in x.items():
                yield from leaves(v, f"{path}/{k}")
        elif isinstance(x, list):
            for v in x:
                yield from leaves(v, path + "[]")
        else:
            yield path, x

    with a_home() as home:
        bare_figs = N.figures()
        assert bare_figs["known_words"] == the_list()["counts"] and bare_figs["typed"] is bare_figs["typed_twice"] is bare_figs["gate_a1"] is None
        clean_pages(home / "typed")
        typed(home / "typed2", "R", 334, [dict(headword="Ai", de="ich", en="I")])
        with set_to(N, BOOKS=SMALL, SECOND={"R": (334,)}):
            quiet(N.merge)
            quiet(N.agree)
            figs = N.figures()
        assert figs["typed"]["pages"] == {"expected": 6, "merged": 6, "failed": 0, "missing": 0} and figs["typed"]["continued_not_attached"] == 0
        assert figs["typed_twice"]["verdict"] == "missed" and figs["typed_twice"]["entries"]["first"] == 2
        texts = {v for p, v in leaves(figs) if isinstance(v, str)}
        assert texts <= {"missed", f"{N.PAGE}, section 2"}, texts                         # no headword, no meaning
        assert "by_page" not in figs["typed_twice"] and "failed" not in figs["typed"]


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
