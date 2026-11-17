"""Checks for track C of the evidence from outside the texts (src/names.py, data/discovery/outside_evidence.md,
section 4): personal names cut into the parts that come back.

  python3 -I tests/test_names.py

The map, the lexicon and the names are local only: the checks of the method run on made-up names, written in
Greek letters so that nothing of them can be mistaken for Meroitic or for the English of a pack. The checks that
read the local files look at the page's totals for all texts and, beyond those, at the tuning texts alone. Two
checks read what `packs` and `public` write, which is counted on the held-back names too: they are skipped until
those files stand, that is until the script is in git and the gate has been run.
"""
import ast
import collections
import contextlib
import io
import json
import math
import random
import re
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import names as N                    # noqa: E402
import recurring as W                # noqa: E402
import themap as M                   # noqa: E402
from local_only import Skip, needs, run    # noqa: E402

THE_MAP = ["data/sources/v6/analysts/glosses.jsonl", "data/sources/lexicon/entries.jsonl", "data/corpus_v6.jsonl",
           "data/sources/grammar/split.json", *[l["file"] for l in M.LAYERS]]
GREEK = re.compile(r"[α-ω]")
STEMS = ["βακ", "τυν", "μιρ", "σολ", "δεπ", "γαφ", "λυξ", "νορ", "πιδ", "ραζ", "ζεμ", "χοθ"]     # the parts the made-up names are built from


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
    """Module values replaced for the length of a check."""
    old = {k: getattr(obj, k) for k in values}
    for k, v in values.items():
        setattr(obj, k, v)
    try:
        yield
    finally:
        for k, v in old.items():
            setattr(obj, k, v)


@contextlib.contextmanager
def a_home(**more):
    """A folder of its own in the place of data/sources/names/, with the script taken as frozen in git."""
    with tempfile.TemporaryDirectory() as d:
        with set_to(N, HOME=Path(d), PUBLIC=Path(d) / "figures.json", frozen=lambda: "abc1234 2026-11-16T22:00:00-08:00", **more):
            yield Path(d)


def made_up(n, seed, stems=STEMS):
    """n different made-up names, each of two or three of the stems, by a fixed seed."""
    rng, out = random.Random(seed), []
    while len(out) < n:
        name = "".join(rng.sample(stems, rng.choice((2, 3))))
        if name not in out:
            out.append(name)
    return out


def row(form, which, name=None, role=None, site="Karanog", lost=False, text="T"):
    return {"text": text, "n": 1, "set": which, "form": form, "lost": lost, "name": form if name is None else name, "cut": "whole", "off": "",
            "role": role, "site": site, "kind": "funerary"}


def word(form, level="unknown", kind="", gloss="", parts=None):
    return {"form": form, "level": level, "kind": kind, "gloss": gloss,
            "parts": [{"form": f, "entry": e} for f, e in ([(form, "?")] if parts is None else parts)]}


def person(form, gloss="NAME", parts=None, kind="person name"):
    return word(form, "name", kind, gloss, [(form, "NAME")] if parts is None else parts)


LEX = {
    "ζοϝι": {"kind": "function word", "status": "probable", "meaning": "'this one is'"},
    "-ζο": {"kind": "function word", "status": "probable", "meaning": "a predicate"},
    "-κυ": {"kind": "function word", "status": "established", "meaning": "a predicate"},
    "-λι": {"kind": "function word", "status": "established", "meaning": "the determiner"},
    "τεδ": {"kind": "verb", "status": "established", "meaning": "'whom X bore', 'child (of such a mother)'"},
    "τερ": {"kind": "verb", "status": "established", "meaning": "'whom X begot', 'child (of such a father)'"},
    "μλο": {"kind": "adjective", "status": "established", "meaning": 'adjective: "good"; noun: "a person of worth"'},
    "Αμν": {"kind": "god name", "status": "established", "meaning": "Amun"},
}


def greek(h):
    """letters() for the made-up lexicon, whose headwords are in Greek letters: the headword without its hyphens."""
    return h.strip("-")


def a_map():
    """A made-up map: four tuning texts and three held-back ones."""
    this = lambda form, end, entry, name: person(form + end, f"this is {name}", [(form, "NAME"), (end, entry)])      # noqa: E731
    gl = {
        "T1": [this("βακ", "ζοϝι", "ζοϝι", "Bak"), person("τυν"), word("τεδλοϝι", "meaning", gloss="it is the one born of (mother)"),
               person("μιρ"), word("τερλοϝι", "meaning", parts=[("τερ", "τερ"), ("λοϝι", "ending")])],
        "T2": [this("σολ", "ζοϝι", "ending", "Sol"), person("δεπλι", "Dep", [("δεπ", "NAME"), ("λι", "-λι")]), word("σμλοϝι", "meaning", gloss="wife +lowi")],
        "T3": [this("γαφ", "ζοϝι", "ζοϝι", "Gaf"), person("λυξζο", "this is Lux", [("λυξ", "NAME"), ("ζο", "-ζο")]), person("νορ.πιδ")],
        "T4": [person("ραζζοϝι", "this is Raz"), person("ζεμζοϝι", "Zemzowi"), word("ζο", "grammar", gloss="this one"),
               person("χοθ", "Khoth (the mother)"), person("βακτυν", "", kind=""), word("Αμν", "name", "god name", "Amun", [("Αμν", "Αμν")])],
        "H1": [person("πιδζοϝι", "this is Pid"), person("νορκυ", "this is Nor", [("νορ", "NAME"), ("κυ", "-κυ")]), person("βακκυ", "this is Bak")],
        "H2": [person("βακ", "Bak"), word("ζοϝι", "grammar", gloss="this one is")],
        "H3": [person("τυν", kind="name"), word("ζο", "grammar", gloss="this one")],
    }
    corpus = {"T1": {"kind": "funerary", "site": "Karanog: grave 12"}, "T2": {"kind": "funerary", "site": "Tômâs (north), cemetery"},
              "T3": {"kind": "funerary", "site": "Purchased by a traveller at a market"}, "T4": {"kind": None, "site": "Provenance not stated"},
              "H1": {"kind": "funerary", "site": ""}, "H2": {"kind": "funerary", "site": "Wad Ben Naga, palace"},
              "H3": {"kind": "royal or temple (stela, wall, cartouche, label)", "site": "Naga"}}
    return gl, corpus, {"tuning": ["T1", "T2", "T3", "T4"], "held": ["H1", "H2", "H3"]}


# ------------------------------------------------------------------------------------------------------ the names

def test_the_names_are_the_705_places_of_the_page():
    """On the map as it stands: the page's counts for all texts, and nothing else of the held-back texts."""
    needs(*THE_MAP)
    rows = N.the_rows()
    assert N.totals_of(rows) == N.TOTALS == {"places": 705, "without_a_lost_sign": 701, "spellings": 624, "tuning": 350, "held": 305, "both": 31}
    assert tuple(l["name"] for l in M.LAYERS)[:len(N.LAYERS)] == N.LAYERS and N.NAME_KINDS == ("person name", "name", "")
    split = N.the_split()
    assert (len(split["tuning"]), len(split["held"])) == (329, 219) and not set(split["tuning"]) & set(split["held"])
    t = N.tuning_figures(rows)                                                     # the tuning texts alone
    assert (t["places"], t["spellings"], t["names"]) == (378, 350, 342) and t["cut"] == {"whole": 287, "reading": 52, "parts": 39}
    assert sum(t["roles"].values()) == sum(t["kinds_of_text"].values()) == sum(t["sites"].values()) == t["places"]
    with set_to(M, LAYERS=M.LAYERS[:3]):
        assert stops(N.the_map, "the layers are no longer")
    with set_to(N, TOTALS=N.TOTALS | {"places": 704}):
        assert stops(N.the_rows, "the names are no longer those of the page")


def test_a_name_loses_what_the_map_names_as_an_ending_and_nothing_else():
    with set_to(N, letters=greek):
        names_lose_their_endings()


def names_lose_their_endings():
    gl, corpus, split = a_map()
    rows = N.rows_of(gl, corpus, LEX, split)
    by = {(r["text"], r["form"]): r for r in rows}
    cut = lambda t, f: (by[(t, f)]["name"], by[(t, f)]["cut"], by[(t, f)]["off"])                                       # noqa: E731
    # the map's parts take the ending off: a function word of the lexicon, the mark `ending`, an ending of the lexicon
    assert cut("T1", "βακζοϝι") == ("βακ", "parts", "ζοϝι") and cut("T2", "σολζοϝι") == ("σολ", "parts", "ζοϝι")
    assert cut("T2", "δεπλι") == ("δεπ", "parts", "λι") and cut("T3", "λυξζο") == ("λυξ", "parts", "ζο")
    # the map gives the word in one piece but reads it "this is ...": the end it takes off three tuning names is taken off, and the row says so
    assert cut("T4", "ραζζοϝι") == ("ραζ", "reading", "ζοϝι") and cut("H1", "πιδζοϝι") == ("πιδ", "reading", "ζοϝι")
    # ... but not where the map reads the whole word as the name, and never an end the map takes off in one name only or in a held-back text only
    assert cut("T4", "ζεμζοϝι") == ("ζεμζοϝι", "whole", "") and cut("H1", "βακκυ") == ("βακκυ", "whole", "") and cut("H1", "νορκυ") == ("νορ", "parts", "κυ")
    joined = N.joined_entries(LEX)
    assert joined == {"ζοϝι", "-ζο", "-κυ", "-λι"} and N.ends_read(gl, split["tuning"], LEX, joined) == ["ζοϝι"]
    assert N.ends_read(gl, split["tuning"] + split["held"], LEX, joined) == ["ζοϝι"]                 # -κυ: one name; -ζο: one name
    assert N.name_of(person("ζοϝι", "this is"), joined, ["ζοϝι"]) == ("ζοϝι", "whole", "")          # an end is no name
    # the reading takes an end off only where the map does not cut the word: in one piece, or in pieces that do not spell
    # it; where the map cuts it into parts, none of them an ending, nothing is taken off
    assert N.name_of(person("πιδζοϝι", "this is Pid"), joined, ["ζοϝι"]) == ("πιδ", "reading", "ζοϝι")
    assert N.name_of(person("πιδζοϝι", "this is Pid", [("πιδ", "NAME"), ("ζο", "NAME")]), joined, ["ζοϝι"]) == ("πιδ", "reading", "ζοϝι")
    assert N.name_of(person("πιδζοϝι", "this is Pid", [("πιδζο", "NAME"), ("ϝι", "NAME")]), joined, ["ζοϝι"]) == ("πιδζοϝι", "whole", "")
    assert N.by_parts(person("ζοβακζο", parts=[("ζο", "-ζο"), ("βακ", "NAME"), ("ζο", "-ζο")]), joined) == ("ζο", "βακ", "ζο")
    assert N.by_parts(person("ζοζο", parts=[("ζο", "-ζο"), ("ζο", "-ζο")]), joined) == ("", "ζο", "ζο")                # one piece at least is left
    assert N.by_parts(person("βακζο", parts=[("βα", "NAME"), ("ζο", "-ζο")]), joined) is None                         # the pieces do not spell it
    # a lost sign: the place is counted, the name is not used
    lost = by[("T3", "νορ.πιδ")]
    assert lost["lost"] and N.names_of(rows, "tuning") == sorted(["βακ", "τυν", "μιρ", "σολ", "δεπ", "γαφ", "λυξ", "ραζ", "ζεμζοϝι", "χοθ", "βακτυν"])
    assert N.totals_of(rows) == {"places": 17, "without_a_lost_sign": 16, "spellings": 15, "tuning": 11, "held": 5, "both": 1}
    assert N.spellings_of(rows, "held") == {"βακ": "βακ", "βακκυ": "βακκυ", "νορκυ": "νορ", "πιδζοϝι": "πιδ", "τυν": "τυν"}
    assert [r["set"] for r in rows] == ["held"] * 5 + ["tuning"] * 12 and set(by[("T1", "τυν")]) == {
        "text", "n", "set", "form", "lost", "name", "cut", "off", "role", "site", "kind"}
    # the ends are learned from the tuning texts alone: an end the held-back texts take off three names is not taken off
    more = {"T9": [person("ραζκυ", "this is Raz")], "H7": [person(n + "κυ", f"this is {n}", [(n, "NAME"), ("κυ", "-κυ")]) for n in ("τυν", "σολ", "δεπ")]}
    nine = N.rows_of(more, {"T9": {"kind": "funerary", "site": ""}, "H7": {"kind": "funerary", "site": ""}}, LEX, {"tuning": ["T9"], "held": ["H7"]})
    assert [(r["form"], r["name"], r["cut"]) for r in nine if r["set"] == "tuning"] == [("ραζκυ", "ραζκυ", "whole")]
    assert N.ends_read(more, ["H7"], LEX, joined) == ["κυ"]                      # learned from those texts, it would be one


def test_the_role_the_site_and_the_kind_come_from_the_map_and_the_corpus():
    gl, corpus, split = a_map()
    by = {(r["text"], r["form"]): r for r in N.rows_of(gl, corpus, LEX, split)}
    role = lambda t, f: by[(t, f)]["role"]                                                                              # noqa: E731
    assert role("T1", "βακζοϝι") == "dead" and role("T1", "τυν") == "mother"                       # the next word's gloss: "born of"
    assert role("T1", "μιρ") == "father"                                                            # the next word's entry in the lexicon: "begot"
    assert role("T2", "δεπλι") == "other" and role("T2", "σολζοϝι") == "dead"                      # the next word: "wife"
    assert role("T4", "ζεμζοϝι") == "dead" and role("T4", "χοθ") == "mother"                       # the next word "this one"; the name's own reading
    assert role("T4", "βακτυν") is None and role("T3", "νορ.πιδ") is None
    assert role("H2", "βακ") == "dead" and role("H3", "τυν") == "other"                           # "this one" in a text that is no epitaph
    assert [by[k]["site"] for k in (("T1", "τυν"), ("T2", "δεπλι"), ("T3", "λυξζο"), ("T4", "χοθ"), ("H1", "βακκυ"), ("H2", "βακ"))] == [
        "Karanog", "Tomas", N.NO_SITE, N.NO_SITE, N.NO_SITE, "Wad Ben Naga"]
    assert by[("T4", "χοθ")]["kind"] == "not known" and by[("H3", "τυν")]["kind"].startswith("royal")
    assert N.ROLES == ("dead", "mother", "father", "other") and {r["role"] for r in by.values()} <= set(N.ROLES) | {None}


def test_a_headword_is_written_in_the_corpuss_letters():
    assert [N.letters(h) for h in ("Wos", "lẖ", "te-dḫe-l", "-se (1)", "qorene", "H̱lẖili", "Ḫs", "wi (1)", "nse doke", "-id(e)")] == [
        "woS", "lX", "tedxel", "s", "qoreN", "XlXili", "xS", "wi", "nsdoke", "id"]


# ------------------------------------------------------------------------------------------------------ the cutter

def test_a_part_stands_in_three_names_and_is_not_carried_by_a_longer_string():
    names = ["βακτυν", "βακμιρ", "σολβακ", "τυνμιρ", "τυνσολ", "λυξ"]
    parts = N.learn_parts(names)
    assert parts == {"βακ": 3, "τυν": 3}                                    # "βα" and "ακ" stand in the same three names as "βακ": carried
    assert N.learn_parts(names + ["βακτυν"] * 5) == parts                  # a name counts once
    assert N.learn_parts(names, least=2) == {"βακ": 3, "τυν": 3, "μιρ": 2, "σολ": 2}
    assert set(N.learn_parts(names, carried=9)) == {"βακ", "βα", "ακ", "τυν", "τυ", "υν"}        # without the rule, every piece of a part
    assert "βα" in N.learn_parts(names + ["ξβαξ"]) and "ακ" not in N.learn_parts(names + ["ξβαξ"])   # "βα" now stands where "βακ" does not
    assert N.learn_parts(names, floor=4) == {} and N.learn_parts(["αβ", "αβ", "αβ"]) == {} and N.learn_parts([]) == {}
    assert N.learn_parts(["αβγ", "αβδ", "αβε"]) == {"αβ": 3} and N.learn_parts(["α", "α", "α"]) == {}                # two letters at least
    assert (N.MIN_LETTERS, N.MIN_NAMES, N.CARRIED) == (2, 3, 1.0) and N.learned_thresholds() == {"MIN_LETTERS": 2, "MIN_NAMES": 3, "CARRIED": 1.0}


def test_a_name_is_cut_with_the_fewest_letters_left_over():
    parts = {"βακ": 9, "τυν": 5, "βα": 3, "κτυν": 3, "μι": 4}
    assert N.cut("βακτυν", parts) == [("βακ", True), ("τυν", True)]                    # not βα + κτυν: its parts stand in fewer names
    assert N.cut("βακτυν", parts | {"βα": 30}) == [("βα", True), ("κτυν", True)]
    assert N.cut("βακξξτυν", parts) == [("βακ", True), ("ξξ", False), ("τυν", True)]   # a run of left-over letters is one piece
    assert N.cut("ξβακ", parts) == [("ξ", False), ("βακ", True)] and N.cut("βακρ", parts) == [("βακ", True), ("ρ", False)]
    assert N.cut("μιρ", parts) == [("μι", True), ("ρ", False)] and N.cut("ξρ", parts) == [("ξρ", False)] and N.cut("", parts) == []
    assert N.cut("βακτυν", parts | {"βακτυν": 3}) == [("βακτυν", True)]                # the fewest pieces
    assert N.cut("βαβακ", parts) == [("βα", True), ("βακ", True)]
    assert N.whole("βακτυν", parts) and N.whole("βακ", parts) and not N.whole("βακρ", parts) and not N.whole("", parts) and not N.whole("β", parts)
    rng = random.Random(4)
    for name in made_up(40, 2) + ["".join(rng.sample("βακτυνμιρξ", 6)) for _ in range(200)]:
        pieces = N.cut(name, parts)
        assert "".join(p for p, _ in pieces) == name and N.whole(name, parts) == all(ok for _, ok in pieces)
        assert all(p in parts for p, ok in pieces if ok) and not any(a[1] is False and b[1] is False for a, b in zip(pieces, pieces[1:]))


def test_the_cutter_finds_the_parts_of_made_up_names_and_splits_shuffled_letters_far_less_often():
    names = made_up(150, 1)
    learn, unseen = names[:100], names[100:]
    parts = N.learn_parts(learn)
    assert set(STEMS) <= set(parts) and not any(s[:2] in parts or s[1:] in parts for s in STEMS)       # the stems, and no piece of a stem
    c = N.compare(unseen, parts, random.Random(1), random.Random(2), draws=50)
    assert c["names"] == 50 and c["wholly_split"] == 50 and c["share"] == 1.0 and c["made_up"] < 0.05 and c["margin"] > 0.95
    assert c["margin"] == round(c["share"] - c["made_up"], 4) and 0 <= c["syllables_kept"] <= 1
    # names of letters drawn by lot hold no part: nothing is found, nothing is split
    rng = random.Random(3)
    noise = ["".join(rng.choice("αβγδεζηθικλμνξοπρστυφχψω") for _ in range(6)) for _ in range(100)]
    assert max(map(len, N.learn_parts(noise)), default=0) <= 2 and sum(N.whole(n, N.learn_parts(noise[:50])) for n in noise[50:]) <= 3
    assert N.compare([], parts, rng, rng)["share"] is None


def test_the_cutter_knows_nothing_but_the_names_it_is_given():
    """The same names in other letters give the same parts in those letters: no part, no letter and no sign of
    the script is built in. And the three functions of the cutter read nothing of the script but its thresholds."""
    names = made_up(120, 5)
    other = str.maketrans("βακτυνμιρσολδεπγφλξζχθ", "0123456789ABCDEFGHIJKL")
    plain = N.learn_parts(names)
    assert {p.translate(other): c for p, c in plain.items()} == N.learn_parts([n.translate(other) for n in names])
    assert all(N.whole(n, plain) == N.whole(n.translate(other), {p.translate(other): c for p, c in plain.items()}) for n in made_up(60, 6))
    tree = ast.parse((ROOT / "src/names.py").read_text(encoding="utf-8"))
    for fn in (n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ("learn_parts", "cut", "whole")):
        loaded = {n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        local = {a.arg for f in ast.walk(fn) if isinstance(f, (ast.FunctionDef, ast.Lambda)) for a in f.args.args} \
            | {n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)} | {f.name for f in ast.walk(fn) if isinstance(f, ast.FunctionDef)}
        assert loaded - local <= {"collections", "math", "set", "range", "len", "sorted", "min", "max", "round", "any", "bool",
                                  "MIN_NAMES", "MIN_LETTERS", "CARRIED"}, (fn.name, sorted(loaded - local))
        assert not [n for n in ast.walk(fn) if isinstance(n, ast.Constant) and isinstance(n.value, str) and n is not fn.body[0].value]


def test_the_script_holds_no_hand_typed_list_of_parts():
    """No string of the script (its docstrings set aside) is made of Meroitic letters: none of its words is a part
    the cutter learned, a tuning name, a god's name of the map or a headword of the lexicon, but for a few English
    words that happen to be spelled like one. Read against the tuning names and the lexicon; no held-back name."""
    needs(*THE_MAP, "data/sources/names/parts.json")
    tree = ast.parse((ROOT / "src/names.py").read_text(encoding="utf-8"))
    docs = {id(n.body[0].value) for n in ast.walk(tree) if isinstance(n, (ast.Module, ast.FunctionDef)) and n.body
            and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
    strings = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs]
    lex, rows = W.lexicon(), [r for r in N.the_rows() if r["set"] == "tuning"]
    meroitic = set(N.read("parts.json")["parts"]) | {N.letters(h) for h in lex} | set(N.gods_of(N.the_map(), lex)) \
        | {r["name"] for r in rows} | {r["form"] for r in rows}
    english = {"So", "an", "are", "as", "be", "do", "it", "met", "no", "on", "or", "to", "yet"}
    words = lambda s: [w for w in re.findall(r"[A-Za-z]+", s) if len(w) >= N.MIN_LETTERS]                             # noqa: E731
    assert sorted({w for s in strings for w in words(s) if w in meroitic} - english) == []
    # and where such an English word stands, it stands in a sentence: no string is made of such words alone, but the bar's "met"
    assert {s for s in strings if words(s) and all(w in meroitic for w in words(s))} == {"met"}
    assert len(strings) > 150 and len(meroitic) > 1000


# ------------------------------------------------------------------------------------------------------ the tuning

def test_the_cutter_is_compared_on_names_it_has_not_learned_from():
    names = made_up(160, 7)
    rows = [row(n, "tuning") for n in names] + [row("ωωωωωω", "held")]
    with set_to(N, RUNS=3, DRAWS_LEARN=10):
        out = N.learned(rows)
        again = N.learned(rows)
    assert out == again and out["names"] == 160 and out["thresholds"] == N.learned_thresholds() and set(STEMS) <= set(out["parts"])
    assert out["parts_in_three_names"] == len(out["parts"]) == sum(out["by_length"].values()) and out["names_wholly_split_in_sample"] == 160
    assert out["strings_in_three_names_carried_ones_too"] == len(N.learn_parts(names, carried=math.inf)) > out["parts_in_three_names"]
    half, fifth = out["unseen_half"], out["unseen_fifth"]
    assert (half["learned_from"], half["names_cut"], fifth["learned_from"], fifth["names_cut"]) == (0.5, 3 * 80, 0.8, 3 * 32)
    for u in (half, fifth):
        assert u["share"] > 0.9 and u["made_up"] < 0.1 and abs(u["margin"] - (u["share"] - u["made_up"])) < 0.0002
        assert abs(u["margin_syllables_kept"] - (u["share"] - u["syllables_kept"])) < 0.0002
    assert not any("ω" in p for p in out["parts"])                                    # nothing of a held-back name is learned
    # the names are dealt the same way whatever the made-up names: other draws, the same halves
    with set_to(N, RUNS=3, DRAWS_LEARN=20):
        assert N.learned(rows)["unseen_half"]["share"] == half["share"]
    assert (N.RUNS, N.DRAWS_LEARN) == (50, 50)
    # in every run the cutter learns from one share of the names and cuts the others: never a name it learned from
    learned_from, cut_ = [], []
    real = N.learn_parts
    with set_to(N, learn_parts=lambda ns, **kw: learned_from.append(list(ns)) or real(ns, **kw),
                tally=lambda ns, parts, *a: cut_.append(list(ns)) or (0, 0.0, 0.0)):
        N.unseen(names, 0.8, 4, 1, 1)
    assert len(learned_from) == len(cut_) == 4 and [(len(a), len(b)) for a, b in zip(learned_from, cut_)] == [(128, 32)] * 4
    assert all(not set(a) & set(b) and sorted(a + b) == sorted(names) for a, b in zip(learned_from, cut_))


def test_the_parts_file_is_what_the_cutter_learns_from_the_tuning_names():
    needs(*THE_MAP, "data/sources/names/parts.json")
    saved = N.read("parts.json")
    rows = [r for r in N.the_rows() if r["set"] == "tuning"]                          # the tuning texts alone
    assert saved["parts"] == N.learn_parts(N.names_of(rows, "tuning")) and saved["thresholds"] == N.learned_thresholds()
    assert (saved["names"], saved["parts_in_three_names"]) == (342, 328) and saved["by_length"] == {"2": 151, "3": 129, "4": 38, "5": 9, "6": 1}
    assert saved["strings_in_three_names_carried_ones_too"] == len(N.learn_parts(N.names_of(rows, "tuning"), carried=math.inf)) == 358   # the page, rule 3
    for u, share in ((saved["unseen_half"], 0.5), (saved["unseen_fifth"], 0.8)):
        assert (u["learned_from"], u["runs"], u["draws"]) == (share, N.RUNS, N.DRAWS_LEARN) and abs(u["margin"] - (u["share"] - u["made_up"])) < 0.0002
    assert saved["unseen_half"]["names_cut"] == N.RUNS * 171 and saved["unseen_fifth"]["names_cut"] == N.RUNS * 68


def test_a_made_up_name_has_the_letters_or_the_syllables_of_its_name():
    rng = random.Random(1)
    assert sorted(N.shuffled("βακτυν", rng)) == sorted("βακτυν") and len({N.shuffled("βακτυν", rng) for _ in range(50)}) > 20
    assert N.syllables("kdiye") == ["k", "di", "ye"] and N.syllables("apeloye") == ["a", "pe", "lo", "ye"] and N.syllables("eio") == ["e", "i", "o"]
    assert N.syllables("") == [] and N.VOWELS == "eio"
    for _ in range(30):
        assert sorted(N.syllables(N.reordered("apeloye", rng))) == sorted(["a", "pe", "lo", "ye"])


# ------------------------------------------------------------------------------------------------------- gate C1

def held_rows(held_names, seed=8):
    return [row(n, "tuning") for n in made_up(120, seed)] + [row(n, "held") for n in held_names]


def test_gate_c1_is_met_at_thirty_points_and_missed_under_them():
    assert N.BAR_C1 == 0.30 and N.DRAWS == 200 and N.SEED == 20261116
    # the bar on the counts themselves, before any rounding: 30 points are met, 29.996 are not (they would round to 30.0)
    assert N.verdict_c1(100, 50, 20.0) == "met" and N.verdict_c1(100, 50, 20.004) == "missed" and N.verdict_c1(305, 100, 8.5) == "met"
    assert N.verdict_c1(305, 100, 8.6) == "missed" and N.verdict_c1(100, 0, 0.0) == "missed" and N.verdict_c1(0, 0, 0.0) == "missed"
    assert N.shares(100, 50, 20.004, 30.0) == {"names": 100, "wholly_split": 50, "share": 0.5, "made_up": 0.2, "margin": 0.3,
                                               "syllables_kept": 0.3, "margin_syllables_kept": 0.2}
    tuning = made_up(120, 8)
    fresh = [n for n in made_up(400, 9) if n not in tuning][:40]
    # met: held-back names built of the parts of the tuning names
    met = N.gate_c1(held_rows(fresh), "abc1234")
    g = met["gate"]
    assert (g["names"], g["wholly_split"], g["share"], g["verdict"]) == (40, 40, 1.0, "met") and g["margin"] >= 0.30
    assert met["frozen_in"] == "abc1234" and met["bar"] == 0.30 and met["draws"] == 200 and met["seed"] == 20261116 and met["tuning_names"] == 120
    assert met["parts_in_three_tuning_names"] == len(N.learn_parts(tuning)) and met["thresholds"] == N.learned_thresholds()
    # the made-up names are 200 shuffles of each name's letters by random.Random(20261116), the names in the order of their spellings
    parts, rng = N.learn_parts(tuning), random.Random(20261116)
    made = sum(sum(N.whole(N.shuffled(n, rng), parts) for _ in range(200)) / 200 for n in sorted(fresh))
    assert g["made_up"] == round(made / 40, 4) and g["margin"] == round((40 - made) / 40, 4)
    assert [r["form"] for r in met["rows"]] == sorted(fresh) and all(r["wholly_split"] and not r["in_tuning"] for r in met["rows"])
    # missed: names of other letters, of which the cutter splits none; and names half of which it splits, 25 points over the made-up ones
    other = ["".join(random.Random(n).sample("ωψηιοκ", 5)) for n in range(40)]
    missed = N.gate_c1(held_rows(other), "abc1234")["gate"]
    assert (missed["wholly_split"], missed["share"], missed["made_up"], missed["margin"], missed["verdict"]) == (0, 0.0, 0.0, 0.0, "missed")
    quarter = N.gate_c1(held_rows(fresh[:10] + other[:30]), "abc1234")["gate"]
    assert quarter["wholly_split"] == 10 and 0.2 < quarter["margin"] < 0.30 and quarter["verdict"] == "missed"
    # the gate's made-up names shuffle letters, not syllables: on names with the script's vowel signs the two differ
    vowelled = ["βe", "κiτ", "μo", "σoλ", "δeπ", "γi", "ζoρ", "λeκ"]
    t2 = made_up(120, 12, vowelled)
    f2 = [n for n in made_up(300, 13, vowelled) if n not in t2][:30]
    g2 = N.gate_c1([row(n, "tuning") for n in t2] + [row(n, "held") for n in f2], "abc1234")["gate"]
    p2 = N.learn_parts(t2)

    def made_by(how):
        rng = random.Random(20261116)
        return sum(sum(N.whole(how(n, rng), p2) for _ in range(200)) / 200 for n in sorted(f2))

    assert len(f2) == 30 and g2["made_up"] == round(made_by(N.shuffled) / 30, 4) != round(made_by(N.reordered) / 30, 4)


def test_a_held_back_spelling_that_also_stands_in_a_tuning_text_is_still_a_held_back_name():
    tuning = made_up(120, 8)
    fresh = [n for n in made_up(400, 9) if n not in tuning][:20]
    other = ["".join(random.Random(n).sample("ωψηιοκ", 5)) for n in range(10)]
    # 20 new names, 10 that the cutter cannot split, 5 spellings that also stand in a tuning text, and 5 spellings of tuning names with an ending
    rows = held_rows(fresh + other + tuning[:5]) + [row(n + "ζο", "held", name=n) for n in tuning[5:10]] + [row("ωω.ωω", "held", lost=True)]
    out = N.gate_c1(rows, "abc1234")
    assert out["gate"]["names"] == 40 and out["gate"]["wholly_split"] == 30                          # the gate: every held-back spelling
    assert out["without_the_spellings_also_in_tuning"]["names"] == 35 and out["without_the_spellings_also_in_tuning"]["wholly_split"] == 25
    assert out["without_the_names_also_in_tuning"]["names"] == 30 and out["without_the_names_also_in_tuning"]["wholly_split"] == 20
    assert out["by_different_names"]["names"] == 40 and sum(r["in_tuning"] for r in out["rows"]) == 5
    twice = N.gate_c1(rows + [row(fresh[0] + "ζο", "held", name=fresh[0])], "abc1234")
    assert twice["gate"]["names"] == 41 and twice["by_different_names"]["names"] == 40               # two spellings of one name: two in the gate
    assert twice["gate"]["wholly_split"] == 31 and twice["by_different_names"]["wholly_split"] == 30
    assert set(out) == {"frozen_in", "bar", "draws", "seed", "thresholds", "tuning_names", "parts_in_three_tuning_names", "gate",
                        "without_the_spellings_also_in_tuning", "without_the_names_also_in_tuning", "by_different_names", "rows"}
    assert "syllables_kept" in out["gate"] and "verdict" not in out["by_different_names"]            # one bar, on the gate alone


def test_the_gate_runs_once_and_only_with_the_script_in_git():
    tuning = made_up(120, 8)
    rows = held_rows([n for n in made_up(400, 9) if n not in tuning][:12])
    never = lambda *a: (_ for _ in ()).throw(AssertionError("the names were read"))                                     # noqa: E731
    with a_home(the_rows=lambda: rows) as d:
        quiet(N.held)
        out = N.read("held.json")
        assert out["frozen_in"].startswith("abc1234") and out["gate"]["names"] == 12 and out == N.gate_c1(rows, out["frozen_in"])
        assert stops(N.held, "the gate has been run: it is not run again")
        (d / "held.json").unlink()
        # not in git, or changed since: nothing is read, nothing is written
        for git in (lambda *a: "", lambda *a: "1111" if a[0] == "hash-object" else "2222"):
            with set_to(N, frozen=FROZEN, git=git, the_rows=never, read=never):
                assert stops(N.held, "is not in git as it stands") and stops(N.packs, "is not in git as it stands")
                assert stops(N.count, "is not in git as it stands")
        assert not (d / "held.json").exists() and not (d / "packs").exists() and not (d / "count.json").exists()
        with set_to(N, frozen=FROZEN, git=lambda *a: "3333" if a[0] in ("hash-object", "rev-parse") else "abc1234 2026-11-16T22:30:00-08:00"):
            assert N.frozen() == "abc1234 2026-11-16T22:30:00-08:00"
    assert N.FROZEN == ("src/names.py", "tests/test_names.py")


FROZEN = N.frozen                     # the script's own check, kept while a_home() puts a made-up one in its place


# ------------------------------------------------------------------------------------------------------- gate C2

def people(*names, site="Karanog", roles=()):
    return {n: {"sites": {site}, "roles": set(roles)} for n in names}


def test_a_parts_statistics_count_the_names_it_stands_in():
    ppl = people("βακτυν", "βακμιρ", "βακσολ", roles=["mother"]) | people("τυνβακ", "μιρβακτυν", site="Shablul", roles=["dead", "father"]) \
        | people("βακ", "αμνβακ", site="Faras") | people("τυνσολ", "σολτυν", "λυξτυν", "τυντυν", "βακαμν", "αμν")
    parts = {"βακ": 9, "τυν": 8, "αμν": 3, "σολ": 3, "ξξ": 3}
    stats = N.statistics(ppl, parts, {"αμν": "Amun", "ωω": "Horus"})
    assert sorted(stats) == ["βακ", "τυν"]                                                # the parts in five names or more
    b = stats["βακ"]
    assert b["names"] == 8 and dict(b["place"]) == {"first": 4, "middle": 1, "last": 2, "whole name": 1}
    assert dict(b["gods"]) == {"Amun": 2} and dict(b["roles"]) == {"mother": 3, "dead": 2, "father": 2}
    assert dict(b["sites"]) == {"Karanog": 4, "Shablul": 2, "Faras": 2} and dict(b["beside"]) == {"τυν": 3}
    t = stats["τυν"]
    assert t["names"] == 7 and dict(t["place"]) == {"first": 3, "last": 5} and dict(t["beside"]) == {"βακ": 3}       # τυντυν: first and last, one name each
    assert dict(t["gods"]) == {} and N.stands_at("τυντυν", "τυν") == [0, 3] and N.stands_at("ααα", "αα") == [0, 1] and N.stands_at("α", "αα") == []
    # a god's name counts only as a part of its own, clear of the part: not the part itself, not letters that overlap it
    g = N.statistics(people("αμνβακ", "αμνβ", "αμντυν", "ξαμν", "αμναμν"), {"αμν": 5, "μνβ": 5}, {"αμν": "Amun", "μνβ": "Mash"})
    assert dict(g["αμν"]["gods"]) == {} and N.MIN_CODED == 5
    assert N.people_of([row("βακζο", "held", name="βακ", role="dead", site="Faras"), row("βακ", "tuning", role="mother"), row("βακ", "tuning"),
                        row("τυ.ν", "tuning", lost=True)]) == {"βακ": {"sites": {"Faras", "Karanog"}, "roles": {"dead", "mother"}}}


def a_key_and_packs(seed=N.SEED_PACKS):
    names = made_up(150, 11, STEMS + ["αμν", "μλο"])
    rows = [row(n, "tuning", role=("mother", "father", "dead", None)[i % 4], site=("Karanog", "Faras", "Shablul")[i % 3]) for i, n in enumerate(names[:90])]
    rows += [row(n + "ζο", "held", name=n, role="dead", site=N.NO_SITE) for n in names[90:]]
    words = {"μλο": [{"entry": "μλο", "kinds": ["quality", "thing or person"], "meaning": "good"}], "ωω": [{"entry": "ωω", "kinds": ["deed"], "meaning": "to give"}]}
    return rows, N.packs_of(rows, {"αμν": "Amun", "ωψ": "Horus"}, words, seed)


def test_the_packs_show_codes_and_numbers_and_no_letter_of_a_part_or_a_name():
    rows, (key, texts) = a_key_and_packs()
    codes = key["codes"]
    parts = N.learn_parts(N.names_of(rows, "tuning"))
    coded = {c["part"] for c in codes.values()}
    assert coded == set(N.statistics(N.people_of(rows), parts, {})) and set(STEMS) | {"αμν", "μλο"} <= coded and coded <= set(parts)
    assert sorted(codes) == [f"P{n:03d}" for n in range(1, len(codes) + 1)] and all(c["names"] >= 5 for c in codes.values())
    # the numbering is drawn by lot: it is not the order of the letters, and another seed gives another
    assert [codes[c]["part"] for c in sorted(codes)] != sorted(coded) and a_key_and_packs(1)[1][0]["codes"] != codes
    assert a_key_and_packs()[1] == (key, texts)
    # packs of about 40, every code in one pack
    sizes = [len(v) for v in key["packs"].values()]
    assert sorted(c for v in key["packs"].values() for c in v) == sorted(codes) and len(sizes) == max(1, round(len(codes) / 40))
    assert max(sizes) - min(sizes) <= 1 and list(key["packs"]) == [f"N{i}" for i in range(1, len(sizes) + 1)]
    assert all(codes[c]["pack"] == name for name, v in key["packs"].items() for c in v)
    # the key says what is known: a god's name of the map, a dictionary word with a meaning
    by = {c["part"]: c for c in codes.values()}
    assert by["αμν"]["known"] and by["αμν"]["kinds"] == ["god"] and by["αμν"]["is"] == [{"entry": None, "kinds": ["god"], "meaning": "the god Amun"}]
    assert by["μλο"]["known"] and by["μλο"]["kinds"] == ["quality", "thing or person"] and by["μλο"]["is"][0]["meaning"] == "good"
    assert sum(c["known"] for c in codes.values()) == 2 and not by["βακ"]["known"] and by["βακ"]["kinds"] == [] and by["βακ"]["is"] == []
    # ... and which kind each known part has for the bar: title and quality as one
    assert (by["αμν"]["kinds_for_the_bar"], by["μλο"]["kinds_for_the_bar"], by["βακ"]["kinds_for_the_bar"]) == (["god"], ["thing or person", "title or quality"], [])
    for name, text in texts.items():
        head, body = text.split("\n---\n\n")
        assert head == N.BRIEF.replace("<<N>>", str(len(key["packs"][name]))) and "<<N>>" not in text and text.count("<<ANSWERS>>") == 1
        assert re.findall(r"(?m)^## (P\d{3})$", body) == key["packs"][name]
        assert not GREEK.search(text) and not shown(body, {"Amun"}, {"Karanog", "Faras", "Shablul"})
        for block in re.split(r"(?m)^## ", body)[1:]:
            assert [l.split(":")[0] for l in block.splitlines() if l.startswith("- ")] == ["- names", "- place", "- with gods", "- whose names", "- sites", "- beside"]
    one = texts[codes[next(c for c in codes if codes[c]["part"] == "αμν")]["pack"]]
    assert "- with gods: Amun " in "\n".join(texts.values()) and "- place: first " in one and "the dead " in one


def test_the_known_parts_are_dealt_evenly_and_a_pack_keeps_its_codes_in_order():
    rows, _ = a_key_and_packs()
    words = {s: [{"entry": s, "kinds": ["thing or person"], "meaning": f"meaning of {n}"}] for n, s in enumerate(STEMS[:5])}
    with set_to(N, PACK=4):
        key, texts = N.packs_of(rows, {"αμν": "Amun"}, words)
    codes, packs = key["codes"], key["packs"]
    known = [sum(codes[c]["known"] for c in v) for v in packs.values()]
    sizes = [len(v) for v in packs.values()]
    assert len(packs) == round(len(codes) / 4) >= 4 and sum(known) == 6 and max(known) - min(known) <= 1 and max(sizes) - min(sizes) <= 1
    assert all(v == sorted(v) for v in packs.values()) and sorted(c for v in packs.values() for c in v) == sorted(codes)
    assert all(re.findall(r"(?m)^## (P\d{3})$", texts[name]) == v for name, v in packs.items())
    # the known parts do not take the first codes: the numbering is drawn before the deal
    assert sorted(c for c in codes if codes[c]["known"]) != sorted(codes)[:6]


def test_the_numbers_of_a_packs_codes_do_not_tell_which_are_known():
    """The deal is drawn by lot apart from the numbering. Dealt in the order of the codes, every pack would hold
    the codes at even steps among the unknown ones (and among the known ones), and a known code would stand off the
    steps of the unknown codes around it: the gaps between the numbers would show it."""
    stats = {f"π{i:03d}": {"names": 5, "place": collections.Counter(), "gods": collections.Counter(), "roles": collections.Counter(),
                           "sites": collections.Counter(), "beside": collections.Counter()} for i in range(240)}
    known = set(sorted(stats)[::8])
    with set_to(N, learn_parts=lambda names: stats, statistics=lambda people, parts, gods: stats,
                known_of=lambda p, gods, words: [{"entry": p, "kinds": ["deed"], "meaning": "a deed"}] if p in known else None):
        key, _ = N.packs_of([], {}, {})
    codes, packs = key["codes"], key["packs"]
    assert len(packs) == 6 and sum(c["known"] for c in codes.values()) == 30 and {sum(codes[c]["known"] for c in v) for v in packs.values()} == {5}
    for which in (True, False):
        group = sorted(c for c in codes if codes[c]["known"] == which)
        steps = [{group.index(c) % len(packs) for c in v if codes[c]["known"] == which} for v in packs.values()]
        assert all(len(s) > 1 for s in steps), (which, steps)


def shown(body, gods, sites):
    """The words of a pack's codes that are no label of the pack, no god's English name and no site."""
    labels = set("names place first middle last whole name with gods whose mothers fathers the dead sites beside none site not known".split())
    allowed = labels | {w for g in gods for w in g.split()} | {w for s in sites for w in re.findall(r"[^\W\d_]+", s)}
    return sorted({w for w in re.findall(r"[^\W\d_]+", re.sub(r"\bP\d{3}\b", "", body))} - allowed)


def test_the_packs_are_written_for_two_readers_and_not_again_once_one_has_answered():
    rows, (key, texts) = a_key_and_packs()
    with a_home(the_rows=lambda: rows, the_map=lambda: {}, gods_of=lambda gl, lex: {"αμν": "Amun"}, words_of=lambda gl, lex, lines: {}), \
            set_to(W, lexicon=lambda: {}), set_to(M, lines_of=lambda layer: []):
        # not before gate C1: the packs count the held-back names
        assert stops(N.packs, "gate C1 has not been run") and not (N.HOME / "packs").exists() and not (N.HOME / "key.json").exists()
        quiet(N.held)
        quiet(N.packs)
        saved = N.read("key.json")
        assert saved["packs"] == key["packs"] and sum(c["known"] for c in saved["codes"].values()) == 1 and saved["frozen_in"].startswith("abc1234 ")
        for name in saved["packs"]:
            a, b = [(N.HOME / "packs" / f"{name}_{r}.md").read_text(encoding="utf-8") for r in "ab"]
            assert f"in the file `data/sources/names/answers/{name}_a.jsonl`" in a and b == a.replace(f"{name}_a.jsonl", f"{name}_b.jsonl")
            assert "<<" not in a and not GREEK.search(a) and a.count("## P") == len(saved["packs"][name])
        assert sorted(p.name for p in (N.HOME / "packs").iterdir()) == sorted(f"{n}_{r}.md" for n in saved["packs"] for r in "ab")
        (N.HOME / "answers" / "N1_a.jsonl").write_text("{}\n", encoding="utf-8")
        assert stops(N.packs, "answers exist: the packs are not written again")


def test_the_real_packs_hold_no_meroitic_letters():
    """Once the packs are written: the brief, and under each code only numbers, other codes, the gods' English
    names and the sites."""
    needs(*THE_MAP, "data/sources/names/key.json", "data/sources/names/packs")
    key, lex = N.read("key.json"), W.lexicon()
    gods, sites = set(N.gods_of(N.the_map(), lex).values()), {N.site_of(r) for r in W.corpus_rows().values()}
    for name, codes in key["packs"].items():
        for reader in "ab":
            head, body = (N.HOME / "packs" / f"{name}_{reader}.md").read_text(encoding="utf-8").split("\n---\n\n")
            assert head == N.BRIEF.replace("<<N>>", str(len(codes))).replace("<<ANSWERS>>", f"{N.ANSWERS}/{name}_{reader}.jsonl")
            assert shown(body, gods, sites) == [] and re.findall(r"(?m)^## (P\d{3})$", body) == codes


def test_a_god_is_named_in_english_and_a_half_of_a_gods_name_is_no_god():
    lex = {"Αμν": {"kind": "god name", "meaning": "Amun"}, "Μν": {"kind": "god name", "meaning": "probably a variant of Αμν (Amun)"},
           "Ασ": {"kind": "god name", "meaning": 'the god "Makedeke"; probably a compound'}, "Wos": {"kind": "god name", "meaning": "Isis (variant of Wis)"},
           "Wis": {"kind": "god name", "meaning": "see Wos"}, "Amnp": {"kind": "god name", "meaning": "name of a deity; see Mnp (Amanap)"},
           "Mnp": {"kind": "god name", "meaning": '"Amanap"; very probably from Egyptian'}, "Mnpte": {"kind": "god name", "meaning": 'probably "Amun of Napata"'},
           "Aritene": {"kind": "god name", "meaning": "Aritene; the royal texts show the word"}, "Xx": {"kind": "god name", "meaning": "a divine name"},
           "Aa": {"kind": "god name", "meaning": "see Bb"}, "Bb": {"kind": "god name", "meaning": "see Aa"}}
    assert [N.english_name(h, lex) for h in ("Αμν", "Ασ", "Wos", "Wis", "Amnp", "Mnp", "Mnpte", "Aritene")] == [
        "Amun", "Makedeke", "Isis", "Isis", "Amanap", "Amanap", "Amun of Napata", "Aritene"]
    assert N.english_name("Xx", lex) == N.NOT_NAMED == N.english_name("Aa", lex) == N.english_name("nothing", lex)
    lex = {"amn": {"kind": "god name", "meaning": "Amun"}, "hor": {"kind": "god name", "meaning": "Horus"}, "-i": {"kind": "function word", "meaning": ""},
           "kdi": {"kind": "noun", "meaning": "woman"}}
    god = lambda form, parts, gloss="": word(form, "name", "god name", gloss, parts)                                # noqa: E731
    gl = {"T1": [god("amni", [("amn", "amn"), ("i", "-i")]), god("mn", [("mn", "amn")], "second half of Amun"), god("hr", [("hr", "hor")]),
                 god("ar", [("ar", "hor")]), god("ar", [("ar", "hor")]), god("ar", [("ar", "hor")]),
                 god("are", [("are", "hor")]), god("are", [("are", "hor")]), god("are", [("are", "amn")]), god("are", [("are", "hor")]),
                 god("ame", [("am", "amn")]), god("kdi", [("kdi", "kdi")]), person("amn", parts=[("amn", "amn")]), god("ere", [("ere", "hor")])]}
    # the entry's own letters; three letters or more given to a god in three places; no piece, no word the pieces do not spell, no person
    assert N.gods_of(gl, lex) == {"amn": "Amun", "are": "Horus"}


def test_a_known_word_has_the_kinds_the_lexicon_gives_it():
    k = N.kinds_of
    assert k("adjective", "good") == ["quality"] and k("verb", "") == ["deed"] and k("title", "") == ["title"] and k("epithet", "") == ["quality"]
    assert k("noun", "woman") == ["thing or person"] and k("noun", "brother (of a male person)") == ["kin word"]
    assert k("function word", "") == ["ending"] and k("", "") == [] and k("place name", "") == [] and k("verb", "'whom X bore', 'child (of such a mother)'") == ["deed"]
    # a word without a kind in the lexicon counts for the meanings only, even where its meaning is a kin term
    assert k("", "the child (of a mother)") == []
    # the kind is the lexicon's kind of the word by the table: a label in its meaning is no kind of it
    assert k("adjective", 'adjective: "good"; noun: "man of worth"') == ["quality"]
    assert k("title", '(1) noun: "child"; (2) title: "page (?)"; (3) adjective: "small"') == ["title"]
    assert set(N.KIND_OF.values()) | {"kin word"} == set(N.KINDS) - {"unclear"}
    # title and quality are one kind for the bar; no other two kinds are
    assert N.bar_kinds(["title"]) == N.bar_kinds(["quality"]) == N.bar_kinds(["quality", "title"]) == ["title or quality"]
    assert N.bar_kinds(["god", "kin word"]) == ["god", "kin word"] and N.bar_kinds([]) == [] and N.bar_kinds(["unclear"]) == ["unclear"]
    assert len({N.bar_kinds([x])[0] for x in N.KINDS}) == len(N.KINDS) - 1
    lex = {h: e | {"headword": h} for h, e in LEX.items()} | {h: {"headword": h, "kind": "noun", "status": "hypothesis", "meaning": "?"} for h in ("κδι", "σμ")}
    gl = {"T1": [word("μλολοϝι", "meaning", parts=[("μλο", "μλο"), ("λοϝι", "ending")]), word("κδι", "meaning", parts=[("κδι", "κδι")]),
                 word("τεδ", "meaning", parts=[("τεδ", "τεδ")]), word("ζοϝι", "grammar", parts=[("ζοϝι", "ζοϝι")]), word("Αμν", "name", "god name", parts=[("Αμν", "Αμν")]),
                 word("σμ", "meaning", parts=[("σμ", "σμ")])]}
    line = {"text": "T1", "n": 2, "form": "κδι", "item": "κδι", "why": "stated", "level": "meaning", "gloss": "woman (a later source)"}
    wife = {"text": "T1", "n": 6, "form": "σμ", "item": "σμ", "why": "stated", "level": "meaning", "gloss": "wife (a later source)"}
    with set_to(N, letters=greek):
        words = N.words_of(gl, lex, [("a layer", [line | {"why": "piece", "gloss": "a piece"}, line, wife])])
        assert set(words) == {"μλο", "τεδ", "ζοϝι", "κδι", "σμ"}                        # in use and with a meaning; no god's name, no ending
        assert words["μλο"] == [{"entry": "μλο", "kinds": ["quality"], "meaning": LEX["μλο"]["meaning"]}]
        assert words["κδι"] == [{"entry": "κδι", "kinds": ["thing or person"], "meaning": "woman (a later source)"}]       # the layer's meaning
        assert words["σμ"] == [{"entry": "σμ", "kinds": ["kin word"], "meaning": "wife (a later source)"}]          # a kin term in the meaning the key gives
        assert set(N.words_of(gl, lex, [])) == {"μλο", "τεδ", "ζοϝι"}
    assert N.known_of("αμν", {"αμν": "Amun"}, {"αμν": [{"entry": "x", "kinds": ["deed"], "meaning": "to take"}]}) == [
        {"entry": None, "kinds": ["god"], "meaning": "the god Amun"}, {"entry": "x", "kinds": ["deed"], "meaning": "to take"}]
    assert N.known_of("βακ", {"αμν": "Amun"}, {}) is None


def test_no_known_tuning_part_has_a_meaning_that_only_names_another_word():
    """The page, rule 7: a meaning that only names another word ("a variant of X") would be replaced as in track B,
    and no known part among the tuning parts needs it, so the script replaces none. The codes of gate C2 are tuning
    parts; the gods and the words are those of the map. Read on the tuning names; nothing is printed."""
    needs(*THE_MAP)
    gl, lex = N.the_map(), W.lexicon()
    gods, words = N.gods_of(gl, lex), N.words_of(gl, lex, [(l["name"], M.lines_of(l)) for l in M.LAYERS[:len(N.LAYERS)]])
    parts = N.learn_parts(N.names_of([r for r in N.the_rows() if r["set"] == "tuning"], "tuning"))
    known = [w for p in parts for w in N.known_of(p, gods, words) or []]
    only = re.compile(r"(?i)^(?:(?:probably|perhaps|possibly|rather|another|an?|the)\s+)*(?:(?:variants?|forms?)\s*(?:\(\?\))?\s+of|see)\s+\S+\s*(?:\([^)]*\))?\W*$")
    assert only.match("variant (?) of μτε") and only.match("see Ϝος") and only.match("probably a variant of Αμν (Amun)")
    assert not only.match("variant of ζο: 'this one'") and not only.match("the god Amun")
    assert len(known) > 20 and [w["entry"] for w in known if only.match(w["meaning"]) or not w["meaning"].strip()] == []


# ------------------------------------------------------------------------------------------------- gate C2: the count

def a_key(known=10, unknown=4):
    """A made-up key: `known` known parts (the first a god, the others qualities) and `unknown` others, in two packs."""
    codes = {}
    for n in range(1, known + unknown + 1):
        is_known = n <= known
        kinds = (["god"] if n == 1 else ["quality", "thing or person"] if n == 2 else ["quality"]) if is_known else []
        codes[f"P{n:03d}"] = {"part": f"part{n}", "pack": f"N{1 + n % 2}", "names": 9, "known": is_known, "kinds": kinds,
                              "is": [{"entry": f"e{n}", "kinds": kinds, "meaning": f"meaning {n}"}] if is_known else []}
    return {"codes": codes, "packs": {name: [c for c, v in codes.items() if v["pack"] == name] for name in ("N1", "N2")}}


def answers(key, kinds_a, kinds_b, meanings=None):
    """{(reader, code): its line}: the kinds each reader gives the codes, in the key's order (None: no answer)."""
    out = {}
    for reader, kinds in (("a", kinds_a), ("b", kinds_b)):
        for code, kind in zip(key["codes"], kinds):
            if kind:
                out[(reader, code)] = {"code": code, "kind": kind, "meaning": (meanings or {}).get((reader, code), "none"), "why": "the numbers"}
    return out


def test_the_kinds_bar_needs_eight_agreed_parts_and_four_fifths_of_them_right():
    assert N.BARS_C2 == {"rate": 0.80, "least": 8} and N.KINDS == ("god", "quality", "thing or person", "deed", "kin word", "title", "ending", "unclear")
    assert [N.bar_c2(r, a) for r, a in ((8, 8), (7, 8), (8, 10), (6, 8), (7, 9), (7, 7), (0, 0), (0, 7), (0, 8))] == [
        "met", "met", "met", "missed", "missed", "too small to decide", "too small to decide", "too small to decide", "missed"]
    key = a_key()
    right = ["god", "thing or person"] + ["quality"] * 8
    # met: both give the ten known parts the same kind, nine of them the key's (the second part may be either of its two kinds)
    met = N.counted(key, answers(key, right[:9] + ["deed"] + ["ending"] * 4, right[:9] + ["deed"] + ["ending", "ending", "title", "unclear"]), None)
    assert met["kinds"] == {"known_with_a_kind": 10, "agreed": 10, "right": 9, "verdict": "met"} and met["codes"] == 14 and met["known"] == 10
    assert met["answered_by_both"] == 14 and met["kappa_kinds"] == round(W.kappa([(N.bar_kinds([a])[0], N.bar_kinds([b])[0]) for a, b in zip(
        right[:9] + ["deed"] + ["ending"] * 4, right[:9] + ["deed"] + ["ending", "ending", "title", "unclear"])]), 4)     # the kinds as the bar counts them
    assert met["kappa_kinds"] != round(W.kappa(list(zip(right[:9] + ["deed"] + ["ending"] * 4, right[:9] + ["deed"] + ["ending", "ending", "title", "unclear"]))), 4)
    # the parts without a known meaning that both give the same kind are listed, with their kind and no meaning
    assert met["listed"] == [{"code": "P011", "part": "part11", "kind": "ending"}, {"code": "P012", "part": "part12", "kind": "ending"}]
    assert met["meanings"] == {"verdict": "not judged yet"}
    # missed: ten agreed, seven right
    wrong = ["deed", "thing or person", "deed", "kin word"] + ["quality"] * 6
    missed = N.counted(key, answers(key, wrong + ["ending"] * 4, wrong + ["ending"] * 4), None)
    assert missed["kinds"] == {"known_with_a_kind": 10, "agreed": 10, "right": 7, "verdict": "missed"} and missed["listed"] == []
    # too small: the readers agree on seven known parts only ("unclear" from both is no kind; a part one reader did not answer is not agreed)
    few = N.counted(key, answers(key, right[:7] + ["unclear", "title", None] + ["ending"] * 4, right[:7] + ["unclear", "deed", "quality"] + ["ending"] * 4), None)
    assert few["kinds"] == {"known_with_a_kind": 10, "agreed": 7, "right": 7, "verdict": "too small to decide"} and few["listed"] == []
    assert few["answered_by_both"] == 13 and [r["same_kind"] for r in few["rows"][7:10]] == [None, None, None]
    # title and quality are one kind for the bar: one reader's title and the other's quality agree, and either is right for a
    # part the key calls a title or a quality; an unknown part they split so is listed as "title or quality"
    tq = a_key()
    tq["codes"]["P010"]["kinds"] = ["title"]
    one = ["god", "thing or person"] + ["title"] * 4 + ["quality"] * 4 + ["title", "quality", "deed", "unclear"]
    two = ["god", "thing or person"] + ["quality"] * 4 + ["title"] * 3 + ["quality"] + ["quality", "quality", "deed", "unclear"]
    mixed = N.counted(tq, answers(tq, one, two), None)
    assert mixed["kinds"] == {"known_with_a_kind": 10, "agreed": 10, "right": 10, "verdict": "met"} and mixed["kappa_kinds"] == 1.0
    assert [(x["code"], x["kind"]) for x in mixed["listed"]] == [("P011", "title or quality"), ("P012", "quality"), ("P013", "deed")]
    assert mixed["rows"][9]["kinds_for_the_bar"] == ["title or quality"] and mixed["rows"][9]["same_kind"] == "title or quality"
    # ... but a title is not a deed, and a quality the key does not give is wrong
    off = N.counted(tq, answers(tq, one[:2] + ["deed"] + one[3:], two[:2] + ["deed"] + two[3:]), None)
    assert off["kinds"] == {"known_with_a_kind": 10, "agreed": 10, "right": 9, "verdict": "met"}
    assert N.counted(tq, answers(tq, ["quality"] + one[1:], ["title"] + two[1:]), None)["kinds"]["right"] == 9
    # a known part whose key has no kind is not counted for the kinds
    key["codes"]["P010"]["kinds"] = []
    assert N.counted(key, answers(key, right + ["ending"] * 4, right + ["ending"] * 4), None)["kinds"] == {
        "known_with_a_kind": 9, "agreed": 9, "right": 9, "verdict": "met"}


def test_the_meanings_bar_is_counted_from_the_judges_verdicts():
    key = a_key()
    kinds = ["god", "quality"] + ["quality"] * 8 + ["ending"] * 4
    said = {(r, c): f"{c} as {r} says it" for r in "ab" for c in list(key["codes"])[:9] + ["P011", "P012"]} | {("a", "P010"): "good", ("b", "P010"): " None "}
    ans = answers(key, kinds, kinds, said)
    pairs = N.pairs_of(key, ans)
    assert [p["code"] for p in pairs] == [f"P{n:03d}" for n in range(1, 10)] + ["P011", "P012"]            # P010: one reader gives none
    assert pairs[0] == {"code": "P001", "a": "P001 as a says it", "b": "P001 as b says it", "key": ["meaning 1"]} and pairs[-1]["key"] is None
    assert N.meant({"meaning": "none"}) is None and N.meant({"meaning": ""}) is None and N.meant({}) is None and N.meant({"meaning": " the  good one "}) == "the good one"
    # a meaning that gives none, however it is written, is none: it would otherwise go to the judge as a meaning both readers give
    assert all(N.meant({"meaning": m}) is None for m in ("None.", " NONE ", "unknown", "Unclear.", "not known", "-", "?", "'none'", None))
    assert N.meant({"meaning": "an unknown god"}) == "an unknown god" and N.meant({"meaning": "none of these"}) == "none of these"
    verdicts = {f"P{n:03d}": {"same": True, "right": n != 3} for n in range(1, 10)} | {"P011": {"same": True}, "P012": {"same": False}}
    met = N.counted(key, ans, verdicts)
    assert met["meanings"] == {"agreed": 9, "right": 8, "verdict": "met"} and met["kinds"]["verdict"] == "met" and met["both_give_a_meaning"] == 11
    # with both bars met a part without a known meaning is listed with the meaning both give, as a proposal; with another meaning from each, without
    assert met["listed"] == [{"code": "P011", "part": "part11", "kind": "ending", "proposal": "P011 as a says it"}, {"code": "P012", "part": "part12", "kind": "ending"}] \
        + [{"code": c, "part": key["codes"][c]["part"], "kind": "ending"} for c in ("P013", "P014")]
    # missed: nine agreed, seven right; a meaning the judge does not call the same is not agreed; no proposal is listed
    missed = N.counted(key, ans, verdicts | {"P004": {"same": True, "right": False}})
    assert missed["meanings"] == {"agreed": 9, "right": 7, "verdict": "missed"} and not any("proposal" in x for x in missed["listed"])
    small = N.counted(key, ans, verdicts | {"P001": {"same": False, "right": True}, "P002": {"same": False}})
    assert small["meanings"] == {"agreed": 7, "right": 6, "verdict": "too small to decide"} and not any("proposal" in x for x in small["listed"])
    assert [r["meaning_right"] for r in small["rows"][:3]] == [False, False, False] and small["rows"][10]["meaning_right"] is None
    # the kinds' bar missed: nothing is listed, whatever the meanings
    off = ["deed"] * 10 + ["ending"] * 4
    assert N.counted(key, answers(key, off, off, said), verdicts)["listed"] == []


def test_a_readers_file_counts_for_its_own_pack_and_the_count_waits_for_the_judge():
    key = a_key(known=10, unknown=2)
    line = lambda code, kind, meaning="none": json.dumps({"code": code, "kind": kind, "meaning": meaning, "why": "w"})    # noqa: E731
    with a_home() as d:
        N.write("key.json", key)
        (d / "answers").mkdir()
        for name, codes in key["packs"].items():
            for reader in "ab":
                lines = [line(c, "god" if c == "P001" else "quality" if int(c[1:]) <= 10 else "ending", f"{c} by {reader}" if c != "P012" else "none") for c in codes]
                # a code of the other pack, a kind that is none of the eight, a second line for a code and a broken line do not count
                lines += [line("P001" if name == "N1" else "P002", "deed"), line(codes[0], "a verb"), line(codes[0], "deed"), "{broken"]
                (d / "answers" / f"{name}_{reader}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
        ans = N.answers_of(key, d / "answers")
        assert len(ans) == 24 and ans[("a", "P001")]["kind"] == "god" and all(a["kind"] != "deed" for a in ans.values())
        # capitals and spaces in a kind are set aside
        (d / "elsewhere").mkdir()
        (d / "elsewhere" / "N2_a.jsonl").write_text(line("P001", " Kin  Word ") + "\n" + line("P003", "GOD") + "\n", encoding="utf-8")
        assert {c: a["kind"] for (_, c), a in N.answers_of(key, d / "elsewhere").items()} == {"P001": "kin word", "P003": "god"}
        quiet(N.count)
        pairs, out = N.read("count-pairs.json"), N.read("count.json")
        assert [p["code"] for p in pairs] == [f"P{n:03d}" for n in range(1, 12)] and out["meanings"] == {"verdict": "not judged yet"}
        assert out["frozen_in"].startswith("abc1234 ")                                    # the commit of the script that counted
        assert out["kinds"] == {"known_with_a_kind": 10, "agreed": 10, "right": 10, "verdict": "met"} and out["kappa_kinds"] == 1.0
        assert out["bars"] == N.BARS_C2 and len(out["rows"]) == 12 and [x["code"] for x in out["listed"]] == ["P011", "P012"]
        N.write("count-verdicts.json", {p["code"]: {"same": True, "right": True} for p in pairs[:-1]})
        assert stops(N.count, "no verdict for P011")
        # a known part whose two meanings the judge calls the same needs a word on whether it is the key's; an unknown one does not
        N.write("count-verdicts.json", {p["code"]: {"same": True} if p["code"] in ("P003", "P011") else {"same": True, "right": True} for p in pairs})
        assert stops(N.count, 'no "right" for P003')
        N.write("count-verdicts.json", {p["code"]: {"same": p["code"] != "P003"} if p["code"] in ("P003", "P011") else {"same": True, "right": True} for p in pairs})
        quiet(N.count)
        assert N.read("count.json")["meanings"] == {"agreed": 9, "right": 9, "verdict": "met"}
        # once counted with the judge's verdicts, the count is not made again, whatever the verdicts say now
        N.write("count-verdicts.json", {p["code"]: {"same": True, "right": p["code"] != "P005"} for p in pairs})
        assert stops(N.count, "it is not counted again") and N.read("count.json")["meanings"] == {"agreed": 9, "right": 9, "verdict": "met"}
        (d / "count.json").unlink()
        quiet(N.count)
        out = N.read("count.json")
        assert out["meanings"] == {"agreed": 10, "right": 9, "verdict": "met"} and out["listed"][0] == {
            "code": "P011", "part": "part11", "kind": "ending", "proposal": "P011 by a"} and "proposal" not in out["listed"][1]


# ---------------------------------------------------------------------------------------------------- the figures

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


def test_the_figures_are_counts_only():
    rows, (key, _) = a_key_and_packs()
    with a_home(the_rows=lambda: rows, RUNS=2, DRAWS_LEARN=5) as d:
        assert not GREEK.search(json.dumps(N.tuning_figures(rows) | {"taken_off": 0}, ensure_ascii=False))
        quiet(N.learn)
        assert GREEK.search((d / "parts.json").read_text(encoding="utf-8"))                       # the local file holds the parts
        quiet(N.public)
        f = json.loads(N.PUBLIC.read_text(encoding="utf-8"))
        assert sorted(f) == ["cutter", "names", "tuning"] and f["names"]["layers"] == list(N.LAYERS) and f["tuning"]["names"] == 90
        assert f["cutter"]["parts_in_three_names"] == len(N.read("parts.json")["parts"]) and "parts" not in f["cutter"]
        assert f["tuning"]["different_ends_taken_off"] == 0 and "taken_off" not in f["tuning"] and f["tuning"]["sites"] == 3
        # the gates, once their files stand
        quiet(N.held)
        N.write("key.json", key)
        kinds = [c["kinds"][0] if c["known"] else "ending" for c in key["codes"].values()]
        N.write("count.json", N.counted(key, answers(key, kinds, kinds), None))
        quiet(N.public)
        f = json.loads(N.PUBLIC.read_text(encoding="utf-8"))
        assert sorted(f) == ["cutter", "gate_c1", "gate_c2", "names", "packs", "tuning"] and "rows" not in f["gate_c1"] and "rows" not in f["gate_c2"]
        assert f["gate_c1"]["gate"]["names"] == 60 and f["gate_c1"]["gate"]["verdict"] in ("met", "missed") and f["gate_c1"]["frozen_in"].startswith("abc1234")
        assert f["packs"] == {"codes": len(key["codes"]), "packs": [len(v) for v in key["packs"].values()], "known": 2, "known_with_a_kind": 2,
                              "known_by_kind": {"god": 1, "quality": 1, "thing or person": 1}}
        assert f["gate_c2"]["kinds"]["verdict"] == "too small to decide" and f["gate_c2"]["listed"] == 0 and f["gate_c2"]["listed_by_kind"] == {}
        assert not GREEK.search(json.dumps(f, ensure_ascii=False))
        # parts.json from other thresholds is not the cutter's
        with set_to(N, MIN_LETTERS=3):
            assert stops(N.public, "parts.json is not what the cutter learns now")


def test_the_public_figures_hold_no_letter_of_a_name_or_a_part():
    """Once `public` has written them: every word of the figures is a key of the script, a kind of text, a site or
    a word of the method's own description; none is a part or a tuning name."""
    if not N.PUBLIC.exists():
        raise Skip("the figures are not written yet")
    needs(*THE_MAP, "data/sources/names/parts.json")
    f = json.loads(N.PUBLIC.read_text(encoding="utf-8"))
    rows = [r for r in N.the_rows() if r["set"] == "tuning"]
    meroitic = set(N.read("parts.json")["parts"]) | {r["name"] for r in rows} | {r["form"] for r in rows}
    english = {"So", "an", "are", "as", "be", "do", "it", "met", "no", "on", "or", "to", "yet"}
    found = {w for s in strings(f) for w in re.findall(r"[A-Za-z]+", s) if len(w) >= 2}
    assert sorted((found & meroitic) - english) == [] and f["names"] == N.TOTALS | {"layers": list(N.LAYERS)}
    assert "rows" not in f.get("gate_c1", {}) and "rows" not in f.get("gate_c2", {}) and "parts" not in f["cutter"]


# ------------------------------------------------------------------------------------------------------ the brief

def test_what_the_readers_are_given_is_public():
    text = (ROOT / "runs/prompts/NAMES_readers.md").read_text(encoding="utf-8")
    block = textwrap.dedent(text[text.index("    # What kind of part is it?"):text.index("## A code in a pack")])
    assert block.replace("<the number of codes>", "<<N>>").replace("<answers>", "<<ANSWERS>>").strip() == N.BRIEF.strip()
    brief = " ".join(N.BRIEF.split())
    assert all(f'"{k}"' in brief for k in N.KINDS) and '**"unclear" and "none" are full answers,**' in brief
    assert "Do not open any other file of the repository, do not search the web" in brief and "You are not shown its letters" in brief
    assert '{"code": "P017", "kind": "<one of the kinds below>", "meaning": "<a few English words, or none>", "why": "<one short sentence>"}' in brief
    assert brief.count("<<N>>") == 3 and brief.count("<<ANSWERS>>") == 1 and "{" not in brief.replace('{"code"', "")
    assert all(f"**{label}**" in brief for label in ("names", "place", "with gods", "whose names", "sites", "beside"))
    assert "your file must have <<N>> lines" in brief and "Egyptian names" in brief and "Nubian names" in brief
    # the example of a code in the page is a code as a pack shows it
    s = {"names": 12, "place": {"first": 9, "middle": 2, "last": 1}, "gods": {"Amun": 3, "Isis": 1}, "roles": {"mother": 4, "father": 1, "dead": 3},
         "sites": {"Karanog": 6, "Shablul": 2, N.NO_SITE: 3}, "beside": {"x": 4, "y": 2, "z": 2}}
    example = N.block("P017", s, {"x": "P003", "y": "P041", "z": "P120"})
    assert example.strip() == textwrap.dedent(
        text[text.index("    ## P017"):text.index("The numbers of this example")]).strip()


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
