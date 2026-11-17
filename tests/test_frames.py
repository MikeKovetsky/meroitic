"""Checks for track B of the evidence from outside the texts (src/frames.py, data/discovery/outside_evidence.md,
section 3): the packs of the blind test and the count of gate B.

  python3 -I tests/test_frames.py

The map, the lexicon, the packs and the answers are local only: the checks of the method run on made-up words,
answers and verdicts; the checks of the page's counts and of the packs read the local files where they are present.
"""
import collections
import contextlib
import io
import json
import random
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import frames as F                   # noqa: E402
import recurring as W                # noqa: E402
from local_only import needs, run    # noqa: E402

PAGE = ROOT / "data/discovery/outside_evidence.md"
THE_MAP = ("data/sources/v6/analysts/glosses.jsonl", "data/corpus_v6.jsonl", "data/sources/lexicon/entries.jsonl", "data/sources/expert",
           "data/sources/recurring/overlay.jsonl", "data/sources/rare/g2/overlay.jsonl", "data/sources/rare/g4/overlay.jsonl",
           "data/sources/g3/overlay.jsonl", "data/sources/rare/g4m/overlay.jsonl", "data/sources/g8b/overlay.jsonl", "data/sources/g9/overlay.jsonl")
LOCAL = ("data/sources/frames/texts.json", "data/sources/frames/folds.json", "data/sources/frames/packs/key.json")


def page():
    return " ".join(PAGE.read_text(encoding="utf-8").split())


def stops(fn, part):
    try:
        fn()
    except SystemExit as e:
        assert part in str(e), e
        return True
    raise AssertionError("did not stop")


@contextlib.contextmanager
def swapped(obj, name, value):
    """A module's value replaced for the length of a check."""
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


@contextlib.contextmanager
def home():
    """The script's folder as an empty one, for a check that writes; what the commands print is not shown."""
    old = F.HOME
    with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(io.StringIO()):
        F.HOME = Path(d)
        try:
            yield F.HOME
        finally:
            F.HOME = old


# ------------------------------------------------------------------------------------------- made-up texts

def word(form, level, *parts, gloss="", kind="", reading=None, piece=False):
    w = {"form": form, "level": level, "kind": kind, "gloss": gloss, "parts": [list(p) for p in parts], "piece": piece}
    return w | ({"reading": gloss if reading is None else reading} if level in W.READ else {})


ENTRIES = {
    "qore": {"class": "known", "kind": "noun"}, "kdi": {"class": "known", "kind": "noun"}, "lẖ": {"class": "known", "kind": "title"},
    "ked": {"class": "known", "kind": "verb"}, "wse": {"class": "stem", "kind": "noun"}, "tqe": {"class": "stem", "kind": "title"},
    "-k (4)": {"class": "stem", "kind": "verb", "bound": True},
    "-l (1)": {"class": "affix", "kind": "function word", "gloss": "postposed article"}, "-te (4)": {"class": "affix", "kind": "function word", "gloss": ""},
    "-wi (5)": {"class": "affix", "kind": "function word", "gloss": "particle (?)"},
    "Amni": {"class": "name", "kind": "god name", "god": "Amun"}, "Amnx": {"class": "name", "kind": "god name"},
    "Pedeme": {"class": "name", "kind": "place name"}, "Ntkmni": {"class": "name", "kind": "person name"},
}
KNOWN = {e: {"kind": ENTRIES[e]["kind"], "places": 1, "texts": 1, "meaning": m, "from": "made up", "taken_from": "", "own_meaning": True, "reading": m}
         for e, m in (("qore", "king, ruler"), ("kdi", "woman"), ("lẖ", "great, elder"), ("ked", "to kill"))}
TEXT = [
    word("qore", "meaning", ("qore", "qore"), gloss="ruler"),                                   # 0 a known word
    word("qorel", "meaning", ("qore", "qore"), ("l", "-l (1)"), gloss="the ruler"),             # 1 with an ending the map names
    word("qorelX", "meaning", ("qore", "qore"), ("lX", "lẖ"), gloss="great ruler"),             # 2 two known entries
    word("kdi", "meaning", ("kdi", "kdi"), gloss="woman"),                                      # 3
    word("wse", "kind", ("wse", "wse"), gloss="[noun]", kind="noun"),                           # 4 open, the map names its stem
    word("wsel", "hypothesis", ("wse", "wse"), ("l", "-l (1)"), gloss="the wse (?)", kind="noun"),   # 5 the same stem with an ending
    word("pide", "unknown", ("pide", "?"), gloss="?", kind="unknown"),                          # 6 open, no stem named
    word("pidel", "unknown", ("pide", "?"), ("l", "-l (1)"), gloss="?", kind="unknown"),        # 7 the same piece, an ending named
    word("xyzpide", "unknown", ("xyz", "?"), ("pide", "?"), gloss="?", kind="unknown"),         # 8 two unnamed pieces: the whole spelling
    word("amni", "name", ("amni", "Amni"), gloss="Amun", kind="god name"),                      # 9
    word("amnx", "name", ("amnx", "Amnx"), gloss="name of a deity", kind="god name"),           # 10 a god the map does not name
    word("ntkmni", "name", ("ntkmni", "Ntkmni"), gloss="name of the ruler", kind="person name"),   # 11
    word("pedemete", "name", ("pedeme", "Pedeme"), ("te", "-te (4)"), gloss="in Primis", kind="place name"),   # 12
    word("bertoye", "name", ("bertoye", "NAME"), gloss="NAME", kind="person name"),             # 13
    word("yeretni", "name", ("yeretni", "?"), gloss="a name, by its place in the text", kind="unknown"),   # 14
    word("25", "number", gloss="25"), word("te...", "lost", gloss="<te...>"),                   # 15, 16
    word("wi", "hypothesis", ("wi", "-wi (5)"), gloss="particle", kind="function word"),        # 17 an ending standing alone
    word("ked", "hypothesis", ("ked", "ked"), gloss="to kill (?)", kind="verb"),                # 18 a known word where the map is unsure
    word("tqewse", "kind", ("tqe", "tqe"), ("wse", "wse"), gloss="[title]", kind="title"),      # 19 two stems without a meaning
    word("tqelX", "kind", ("tqe", "tqe"), ("lX", "lẖ"), gloss="great tqe", kind="title"),       # 20 a stem and a known entry
    word("tmde", "meaning", gloss="(part of yetmde)", reading="part of a word", piece=True),    # 21 a piece written apart
    word("se", "name", ("se", "-l (1)"), gloss="part of mnotese: Amun", kind="function word", piece=True),   # 22
]


def made_up(texts=None):
    return {"texts": texts or [{"id": "T1", "kind": "royal or temple", "words": TEXT}], "entries": ENTRIES, "known": KNOWN}


def shown(hidden, fold=1, data=None):
    data = data or made_up()
    code = F.codes_of(data["texts"], data["entries"], set(hidden), fold)
    names, kin = F.names_of(data["texts"], data["entries"]), F.kin_of(set(hidden), data["entries"])
    return [F.token(w, data["entries"], data["known"], set(hidden), code, names, kin) for w in data["texts"][0]["words"]], code


# ------------------------------------------------------------------------------------------------ the method

def test_a_word_is_a_reading_or_a_code():
    toks, code = shown({"qore"})
    q, wse, pide, tqe = code["hidden", "qore"], code["entry", "wse"], code["spelling", "pide"], code["entry", "tqe"]
    assert toks[0] == q and toks[1] == f"{q}+[postposed article]"                       # every spelling of the hidden entry, its ending by its gloss
    assert toks[2] == f"{q}+[great, elder]"                                             # two known entries: each by its own rule
    assert toks[3] == "[woman]"                                                         # a known word that is not hidden: the map's gloss
    assert toks[4] == wse and toks[5] == f"{wse}+[postposed article]"                   # an open word: one code an entry
    assert toks[6] == pide and toks[7] == f"{pide}+[postposed article]"                 # one code a spelling: the piece the map could not name
    assert toks[8] == code["spelling", "xyzpide"] != pide                               # no stem to be told: the whole spelling
    assert toks[9] == "[Amun]" and toks[10] == "GOD-01"                                 # a god by the name the map gives, or a code that says god
    assert toks[11] == "PERSON-01" and toks[12] == "PLACE-01" and toks[13] == "PERSON-02" and toks[14] == "NAME-01"
    assert toks[15] == "25" and toks[16] == "[lost]"
    assert toks[17] == code["entry", "-wi (5)"]                                         # an ending standing alone, open: its own code
    assert toks[18] == code["entry", "ked"] != code.get(("hidden", "ked"))              # a known word where the map is unsure is an open word
    assert toks[19] == f"{tqe}+{wse}" and toks[20] == f"{tqe}+[great, elder]"
    assert toks[21] == "[part of a word]" and toks[22] == "[part of a name]"
    both, code2 = shown({"qore", "lẖ"})
    assert both[2] == f"{code2['hidden', 'qore']}+{code2['hidden', 'lẖ']}" and both[20] == code2["entry", "tqe"]   # a hidden entry is not shown in an open word
    none, _ = shown(set())
    assert none[:4] == ["[ruler]", "[the ruler]", "[great ruler]", "[woman]"]           # nothing hidden: the map's gloss of the whole word
    for toks in (toks, both, none):                                                     # never a spelling
        assert not any(w["form"] in re.findall(r"[^\W\d_]+", t) for w, t in zip(TEXT, toks) if w["level"] not in ("number",)), toks


def test_a_word_built_on_a_hidden_one_is_coded_and_not_counted():
    entries = ENTRIES | {"qorene": {"class": "known", "kind": "title"}, "kdise": {"class": "known", "kind": "noun"},
                         "lẖs": {"class": "known", "kind": "title"}}
    known = KNOWN | {e: KNOWN["qore"] | {"kind": entries[e]["kind"], "meaning": m, "reading": m}
                     for e, m in (("qorene", "a royal title"), ("kdise", "sister"), ("lẖs", "a title"))}
    words = [word("qorene", "meaning", ("qorene", "qorene"), gloss="a royal title"),
             word("qorenel", "meaning", ("qorene", "qorene"), ("l", "-l (1)"), gloss="the royal title"),
             word("kdise", "meaning", ("kdise", "kdise"), gloss="sister"), word("lẖs", "meaning", ("lẖs", "lẖs"), gloss="a title"), TEXT[0]]
    data = {"texts": [{"id": "T1", "kind": "royal or temple", "words": words}], "entries": entries, "known": known}
    assert F.kin_of({"qore", "lẖ"}, entries) == {"qorene"}                                        # lẖ has under three letters
    assert F.kin_of({"qorene"}, entries) == set() and F.kin_of({"kdi"}, entries) == {"kdise"}
    toks, code = shown({"qore", "lẖ"}, data=data)
    q = code["entry", "qorene"]
    assert toks[:4] == [q, f"{q}+[postposed article]", "[sister]", "[a title]"] and toks[4] == code["hidden", "qore"]
    files, key = F.build(data, {"1": ["lẖ", "qore"], "2": ["kdi", "ked"]})
    one = key["folds"]["1"]["codes"]
    assert one[q]["sort"] == "open" and one[q]["built_on_a_hidden_word"] == ["qore"] and one[q]["places"] == 2   # an open word: not counted
    assert key["folds"]["1"]["built_on_a_hidden_word"] == ["qorene"] and key["folds"]["2"]["built_on_a_hidden_word"] == ["kdise"]
    assert [h["entry"] for h in F.hidden_words(key) if h["fold"] == 1] == ["qore"]               # qorene is not counted (lẖ stands nowhere)
    assert "a royal title" not in files["f1_p01"] and "[sister]" in files["f1_p01"] and "sister" not in files["f2_p01"]


def test_a_name_has_one_code_and_says_what_it_names():
    twice = made_up([{"id": "T1", "kind": "long text", "words": [TEXT[11], TEXT[13], TEXT[11], TEXT[12], TEXT[13], TEXT[9], TEXT[10], TEXT[10]]}])
    toks, _ = shown(set(), data=twice)
    assert toks == ["PERSON-01", "PERSON-02", "PERSON-01", "PLACE-01", "PERSON-02", "[Amun]", "GOD-01", "GOD-01"]


def test_hidden_and_open_codes_are_drawn_from_one_numbering():
    data = made_up()
    hidden_first = 0
    for fold in range(1, 41):
        code = F.codes_of(data["texts"], data["entries"], {"qore", "kdi"}, fold)
        assert len(set(code.values())) == len(code) and all(re.fullmatch(r"W\d{3}", c) for c in code.values()), code
        assert sorted(code.values()) == [f"W{n:03d}" for n in range(1, len(code) + 1)]            # one run of numbers, no gap between the sorts
        hidden_first += min(code, key=code.get)[0] == "hidden"
    assert 0 < hidden_first < 40                                                                  # the lowest number is of either sort, by lot
    many = {"texts": [{"id": "T", "kind": "long text", "words": [word(f"w{n}", "unknown", (f"w{n}", "?")) for n in range(1200)]}], "entries": {}, "known": {}}
    assert all(re.fullmatch(r"W\d{4}", c) for c in F.codes_of(many["texts"], {}, set(), 1).values())   # more than 999 codes: one digit more for all


def test_the_folds_are_two_halves_that_share_nothing():
    known = [f"w{n:03d}" for n in range(102)]
    f = F.folds_of(known)
    one, two = f["halves"]["1"], f["halves"]["2"]
    assert f["seed"] == F.SEED == 20261116 and len(one) == len(two) == 51 and not set(one) & set(two) and sorted(one + two) == known
    order = sorted(known)
    random.Random(20261116).shuffle(order)
    assert one == sorted(order[:51]) and two == sorted(order[51:])                    # the sorted list, shuffled with the page's seed
    assert F.folds_of(reversed(known)) == f and F.folds_of(known, seed=1) != f
    odd = F.folds_of(known[:5])["halves"]
    assert (len(odd["1"]), len(odd["2"])) == (3, 2)


def test_the_folds_are_drawn_once():
    with home() as d:
        F.write("texts.json", {"known": {f"w{n}": {} for n in range(10)}})
        F.folds()
        first = (d / "folds.json").read_text(encoding="utf-8")
        assert stops(F.folds, "not drawn again") and (d / "folds.json").read_text(encoding="utf-8") == first


def test_a_text_is_never_split_and_a_long_text_is_a_pack_of_its_own():
    sizes = [5, 120, 40, 90, 99, 100, 60, 30, 708, 80, 70, 4, 96]
    texts = [{"words": [None] * n} for n in sizes]
    packs = F.packs_of(texts)
    assert sorted(i for p in packs for i in p) == list(range(len(sizes)))                         # every text in one pack
    long = [i for i, n in enumerate(sizes) if n >= 100]
    assert [p for p in packs if len(p) == 1 and p[0] in long] == [[i] for i in long]             # 100 words or more: a pack of its own
    short = [p for p in packs if p[0] not in long]
    assert [i for p in short for i in p] == [i for i in range(len(sizes)) if i not in long]      # the others in the corpus's order
    assert len(short) == 2 and all(200 <= sum(sizes[i] for i in p) <= 400 for p in short), short  # 574 words: two packs of about 300
    assert F.packs_of([{"words": [None] * 3}]) == [[0]] and F.packs_of([{"words": [None] * 150}]) == [[0]]


def test_a_gloss_is_shown_without_meroitic_letters():
    mero = {"qore", "lw", "xlbi", "ked", "pke", "to", "a", "at", "s", "nd", "d"}
    assert F.clean("ruler, sovereign +lw") == "ruler, sovereign" and F.clean("part of xlbi: bull") == "bull" and F.clean("(part of ato)") == ""
    assert F.clean("it is (the general) of the province") == "it is of the province"             # a remark may name the word beside it
    assert F.clean("to kill, to slaughter (a form of ked)") == "to kill, to slaughter" and F.clean("water (?)") == "water (?)"
    assert F.clean("'agent'; borrowed from Egyptian p3 rwḏ") == "'agent'" and F.clean("child; page (?) as title", cut=False) == "child; page (?) as title"
    assert F.clean("'I took': ye- 1sg + er 'take hold of' + pluractional -k + -i") == "'I took'"
    assert F.clean("optative ending, 2nd person plural (-ke plural + -te)") == "optative ending, 2nd person plural"
    assert F.clean("first piece of pe-stolis 'of the viceroy'") == "'of the viceroy'" and F.clean("[high priest]") == "high priest"
    assert [m.group() for m in F.suspects("predicated form of qore, with -lw and ye- at a place to be", mero)] == ["qore", "-lw", "ye-"]
    assert [m.group() for m in F.suspects("variant of akroro", mero)] == ["akroro"] and not F.suspects("a form of the article", mero)
    assert not F.suspects("Amun's 2nd formula A, whom X begot; I gave, O god", mero)             # English, labels, and no word beside a digit
    assert F.shown("the pke (a good gift)", mero) == "" and F.shown("to kill", mero) == "to kill" and F.shown("?", mero) == ""
    assert F.blank("a title formed on qore, 'king'", mero) == "a title formed on …, 'king'"
    assert F.ENGLISH <= {"a", "are", "as", "at", "be", "on", "so", "to"} and F.ENGLISH_AS_WRITTEN == {"I", "O"}


def test_a_reading_falls_back_on_the_known_entries_meaning():
    mero = {"qore", "akroro", "pke"}
    known = {"mlo": {"reading": "good; a worthy person"}, "qor-o": {"reading": "he is the ruler"}}
    g = lambda gloss, *entries, **more: {"level": "meaning", "gloss": gloss, "parts": [{"form": "x", "entry": e} for e in entries]} | more   # noqa: E731
    assert F.reading_of(g("abundant +li", "mlo"), known, {}, mero) == "abundant"                  # the map's gloss, where it reads
    assert F.reading_of(g("adjective +l", "mlo"), known, {}, mero) == "good; a worthy person"     # only the kind of word
    assert F.reading_of(g("predicated form of qore", "qor-o"), known, {}, mero) == "he is the ruler"   # names a Meroitic word
    assert F.reading_of(g("part of xlbi: bull", "?", why="piece"), known, {}, mero) == "part of a word"   # never the whole word's meaning
    assert F.reading_of(g("part of mlo: good", "mlo", why="piece"), known, {}, mero) == "good"    # a piece that names a known entry is that word
    entries = {"-lo": {"class": "affix", "gloss": "article and copula"}}
    assert F.reading_of(g("the singular copula -o in -l-o", "-lo"), known, entries, mero) == "article and copula"
    assert F.reading_of(g("emphatic particle after the copula -o", "-lo", layer="x"), known, entries, mero) == "emphatic particle after the copula"


def test_a_decoy_is_another_hidden_word_of_the_kind_with_another_meaning():
    known = {"l": {"kind": "verb", "meaning": "to give"}, "tre": {"kind": "verb", "meaning": "to give"}, "ked": {"kind": "verb", "meaning": "to kill"},
             "qore": {"kind": "noun", "meaning": "king, ruler"}, "qor": {"kind": "noun", "meaning": "the ruler"}, "kdi": {"kind": "noun", "meaning": "woman"},
             "kroro": {"kind": "noun", "meaning": "another form of akroro", "own_meaning": False}, "mlo": {"kind": "adjective", "meaning": "good"}}
    known = {e: {"own_meaning": True} | k for e, k in known.items()}
    for seed in range(30):
        d = F.decoys_of(set(known), known, random.Random(seed))
        assert d["l"] == d["tre"] == "ked" and d["qore"] == d["qor"] == "kdi"       # never the other word for "to give" or for "ruler"
        assert d["kdi"] in ("qore", "qor") and "kroro" not in d and "kroro" not in d.values()   # a word without a meaning of its own: none
        assert d["mlo"] != "mlo" and d["ked"] in ("l", "tre")                         # no other adjective: of another kind


def test_the_meaning_to_judge_is_taken_as_in_track_a():
    said = {"qore": ("king, ruler", "the public table"), "mleyi": ("probably a form of mlowi (noun)", "the public table"),
            "mlowi": ("health", "the layers' lines"), "kroro": ("another form of akroro", "the public table"),
            "esebe": ("another form of yesebe", "the public table"), "yesebe": ("", "the lexicon"),
            "asr": ("variant of sr", "the lexicon"), "sr": ("variant (?) of asr", "the lexicon"), "beliloke": ("senior title (variant of beloloke)", "the public table")}
    by = {h: "the lexicon" for h in ("qore", "mleyi", "mlowi", "kroro", "esebe", "asr", "sr", "beliloke")}
    m = lambda e: F.meaning_to_judge(e, said.get, by)                                  # noqa: E731
    assert m("qore") == ("king, ruler", "the public table", "", True)
    assert m("mleyi") == ("health", "the layers' lines, of mlowi", "mlowi", True)        # replaced by the meaning of the word it names
    assert m("kroro") == ("another form of akroro", "the public table", "", False)       # akroro has no meaning on the map
    assert m("esebe")[3] is False and m("asr")[3] is False                               # yesebe is not on the map; sr only names asr
    assert m("beliloke") == ("senior title (variant of beloloke)", "the public table", "", True)   # it says more than a name
    assert [F.only_names(x) for x in ("variant of sr", "another form of akroro", "probably a form of mlowi (noun)", "variant (?) of mte",
                                      "a form of qore, 'king'", "south; a form of yireqe", "senior title (variant of beloloke)")] == \
        ["sr", "akroro", "mlowi", "mte", None, None, None]


def test_the_key_says_what_each_code_is():
    data = made_up([{"id": "T1", "kind": "royal or temple", "words": TEXT[:9]}, {"id": "T2", "kind": "long text", "words": TEXT[:4] * 30}])
    files, key = F.build(data, {"1": ["kdi", "qore"], "2": ["ked", "lẖ"]})
    assert sorted(files) == ["f1_p01", "f1_p02", "f2_p01", "f2_p02"] and key["packs"]["p02"] == {"texts": {"Text 02": "T2"}, "words": 120}
    one = key["folds"]["1"]["codes"]
    hid = {k["entry"]: (c, k) for c, k in one.items() if k["sort"] == "hidden"}
    assert set(hid) == {"qore", "kdi"} and hid["qore"][1]["packs"] == ["f1_p01", "f1_p02"] and hid["qore"][1]["places"] == 3 + 90
    assert hid["qore"][1] | {"packs": 0, "places": 0} == {"fold": 1, "sort": "hidden", "entry": "qore", "kind": "noun", "packs": 0, "places": 0,
                                                         "meaning": "king, ruler", "from": "made up", "taken_from": "", "own_meaning": True,
                                                         "decoy": "kdi", "decoy_meaning": "woman"}
    opened = {k.get("entry") or k["spelling"]: k for k in one.values() if k["sort"] == "open"}
    assert set(opened) == {"wse", "pide", "xyzpide"} and opened["wse"]["kind"] == "noun" and "spelling" in opened["pide"] and "meaning" not in opened["wse"]
    assert all(k["fold"] == 1 and k["packs"] for k in one.values())
    text = files["f1_p01"]
    assert text.startswith("# Pack f1_p01: 1 Meroitic text, 9 words, 5 codes") and "## Text 01 (royal or temple, 9 words)" in text and "T1" not in text
    listed = text.split("## The codes of this pack: 5")[1]
    assert sorted(re.findall(r"W\d{3}", listed)) == key["folds"]["1"]["packs"]["f1_p01"] == sorted(c for c, k in one.items() if "f1_p01" in k["packs"])
    assert "Give each of these 5 codes one line" in listed
    two = {k.get("entry"): k for k in key["folds"]["2"]["codes"].values() if k["sort"] == "hidden"}
    assert set(two) == {"lẖ"}                                         # `ked` stands in none of these texts: no code, and nothing to answer


def test_an_answer_file_is_checked_against_its_pack():
    codes = ["W001", "W002", "W003"]
    line = lambda c, m="none", **more: json.dumps({"code": c, "meaning": m, "why": ""} | more)     # noqa: E731
    got, wrong = F.check_answers("\n".join([line("W001"), line("W002", "a king"), "", line("W003", "None.")]), codes)
    assert not wrong and list(got) == codes and [F.meaning_given(got[c]) for c in codes] == [None, "a king", None]
    assert F.check_answers(line("W001") + "\n" + line("W002"), codes)[1] == ["1 codes without a valid line: W003"]
    _, wrong = F.check_answers("\n".join([line("W001"), line("W001"), "not json", line("W009"), json.dumps({"code": "W002"}), json.dumps(["W003"])]), codes)
    assert wrong == ["W001 is answered twice", "line 3 is no JSON", "line 4: 'W009' is no code of the pack", 'W002 has no meaning ("none" is one)',
                     "line 6: None is no code of the pack", "2 codes without a valid line: W002, W003"]
    with_frames = "\n".join([line("W001", frame=None, slot=None), line("W002", "a king", frame="K3", slot=2), line("W003", "a god")])
    got, wrong = F.check_answers(with_frames, codes)
    assert not wrong                                                                              # a meaning without a frame is no fault of the file
    known_frames = {"K3": {1, 2, 3}, "W1": {1}}
    assert [F.counted(got[c], "frames", known_frames) for c in codes] == [None, "a king", None]   # ... it counts as "none" with the frames
    assert [F.counted(got[c], "plain", known_frames) for c in codes] == [None, "a king", "a god"]  # and as given without them
    cites = lambda frame, slot: {"code": "W002", "meaning": "a king", "frame": frame, "slot": slot}   # noqa: E731
    assert F.counted(cites("K3", 2), "frames", known_frames) == "a king" == F.counted(cites("W1", "1"), "frames", known_frames)   # "1" is slot 1
    for frame, slot in (("K9", 2), ("K3", 4), ("W1", 2), ("K3", "second"), ("K3", None), (None, 2), (["K3"], 2)):
        assert F.counted(cites(frame, slot), "frames", known_frames) is None, (frame, slot)       # no frame and slot of the digest
    assert F.counted(cites("K3", 2), "frames", {}) is None
    with home() as d:
        assert F.frame_slots() == {} and stops(F.slots_in_hand, "the six files of frames are not all there")   # until the six files are there
        for k in F.FRAMES:
            F.write(f"frames_{k}.json", {"angle": k, "frames": [{"id": f"{k}1", "slots": [{"n": 1}, {"n": 2}]}]})
        assert F.frame_slots() == {f"{k}1": {1, 2} for k in "KGDWOP"} == F.slots_in_hand()
    assert [F.meaning_given({"meaning": m}) for m in ("none", " None ", "", "\"none\"", "no meaning", "a  great\tking")] == [None] * 5 + ["a great king"]
    assert F.meaning_given(None) is None and F.meaning_given({"meaning": 3}) is None


def test_the_digest_holds_the_frames_without_their_passages_and_notes():
    frame = {"id": "K1", "name": "Dated titulary", "where": "opening", "monuments": "royal stelae (Kawa)",
             "sources": [{"fhn": "I 17", "page": 128, "passage": "PASSAGE OF THE SOURCE"}], "notes": "A NOTE OF THE BUILDER",
             "slots": [{"n": 1, "meaning": "the date", "wording": ["Regnal year 6", "Year 3"], "egyptian": "EGYPTIAN WORDS", "optional": False, "repeats": False},
                       {"n": 2, "meaning": "praise of the king", "wording": ["the good god"], "egyptian": "", "optional": True, "repeats": True}]}
    files = {k: {"angle": "x", "frames": [frame | {"id": f"{k}1"}], "read": ["I 17"], "rejected": [{"why": "A REJECTED ONE"}]} for k in F.FRAMES}
    text = F.digest_of(files)
    for k, what in F.FRAMES.items():
        assert f"## {k}: {what} (1 frames)" in text and f"### {k}1. Dated titulary" in text
    assert "Where: opening. Monuments: royal stelae (Kawa)." in text
    assert '1. the date. Wording: "Regnal year 6"; "Year 3".\n' in text and '2. praise of the king. Wording: "the good god". (may be left out; may repeat)' in text
    assert not re.search(r"PASSAGE|NOTE OF|EGYPTIAN|REJECTED|I 17|128", text)                     # no passage, note, Egyptian, page
    with home() as d:
        F.write("texts.json", {"known": {}})
        assert stops(F.packs, "the six files of frames are not all there") and not (d / F.DIGEST).exists()


def test_the_texts_are_written_again_only_while_the_folds_stay_and_no_aligner_has_answered():
    data = {"counts": dict(F.PAGE), "known": {f"w{n}": {} for n in range(10)}, "texts": []}
    with home() as d, contextlib.ExitStack() as stack:
        for name, value in (("texts_of", lambda *a: data), ("the_map", lambda: {}), ("the_table", lambda: {})):
            stack.enter_context(swapped(F, name, value))
        stack.enter_context(swapped(F.W, "corpus_rows", lambda: {}))
        stack.enter_context(swapped(F.W, "lexicon", lambda: {}))
        F.texts()
        F.folds()
        data["texts"] = ["a new reading"]                                                        # the same known words: the folds stay
        F.texts()
        assert F.read("texts.json")["texts"] == ["a new reading"]
        data["known"] = {f"w{n}": {} for n in range(1, 11)}                                      # other known words: other folds
        assert stops(F.texts, "the folds are drawn from other known words") and F.read("texts.json")["texts"] == ["a new reading"]
        data["known"] = {f"w{n}": {} for n in range(10)}
        F.write_text("answers/plain/f1_p01_a.jsonl", "")
        assert stops(F.texts, "aligners have answered")
        data["counts"] = dict(F.PAGE, open=1369)
        assert stops(F.texts, "the counts are not the page's")


# ------------------------------------------------------------------------------------------------ gate B

def a_test(right, wrong, decoys=0, none=0, one=0):
    """Made-up hidden words in one pack, answers and verdicts: `right` words whose two answers both judges call the
    same, `wrong` words they do not (the first `decoys` of all the given words fit their decoy), `none` words both
    aligners leave without a meaning, `one` words only one aligner gives a meaning."""
    hidden, given, said = [], {}, {}
    for n in range(right + wrong + none + one):
        h = {"fold": 1, "code": f"W{n:03d}", "entry": f"e{n}", "packs": ["f1_p01"], "meaning": f"meaning {n}", "decoy_meaning": f"decoy {n}"}
        hidden.append(h)
        if n < right + wrong:
            for a in F.ALIGNERS:
                given[1, "f1_p01", a, h["code"]] = f"answer {n} {a}"
                said[f"answer {n} {a}", h["meaning"]] = ("same", "same") if n < right else ("same", "partly")
                said[f"answer {n} {a}", h["decoy_meaning"]] = ("same", "same") if n < decoys else ("another", "another")
        elif n >= right + wrong + none:
            given[1, "f1_p01", "a", h["code"]] = f"answer {n} a"
    return F.arm_figures(hidden, given, lambda ans, meaning: said[ans, meaning])


def test_gate_b_is_counted_as_the_page_states_it():
    assert F.BARS == {"given_at_least": 10, "right": 0.80, "margin": 0.30, "kappa": 0.6}
    f = a_test(right=9, wrong=2, decoys=1, none=5, one=3)
    assert (f["hidden"], f["given"], f["right"], f["decoys_same"]) == (19, 11, 9, 1)             # given: both aligners; right: both judges, both answers
    assert (f["share_right"], f["share_decoys"], f["margin"]) == (0.8182, 0.0909, 0.7273)
    met = F.gate(f, 0.7)
    assert met == {"bars": {"given_at_least_10": True, "right_80": True, "above_decoys_30": True, "kappa_0.6": True}, "complete": True, "met": True}
    assert F.gate(a_test(8, 2), 0.6)["met"] and F.gate(a_test(8, 2, decoys=5), 0.6)["met"]       # 80% on ten words; 30 points above 50%
    low = F.gate(a_test(7, 3), 0.9)                                                               # 70% right
    assert not low["met"] and low["bars"] == {"given_at_least_10": True, "right_80": False, "above_decoys_30": True, "kappa_0.6": True}
    near = F.gate(a_test(9, 1, decoys=7), 0.9)                                                    # 90% right, 70% of the decoys fit too
    assert not near["met"] and near["bars"] == {"given_at_least_10": True, "right_80": True, "above_decoys_30": False, "kappa_0.6": True}
    apart = F.gate(a_test(10, 0), 0.59)                                                           # the judges do not agree
    assert not apart["met"] and apart["bars"] == {"given_at_least_10": True, "right_80": True, "above_decoys_30": True, "kappa_0.6": False}
    assert not F.gate(a_test(10, 0), None)["met"]
    few = F.gate(a_test(9, 0, none=40), 0.9)                                                      # nine given words, all right
    assert not few["met"] and few["bars"] == {"given_at_least_10": False, "right_80": True, "above_decoys_30": True, "kappa_0.6": True}
    empty = a_test(0, 0, none=4)
    assert empty["given"] == 0 and empty["share_right"] is None and not any(v for k, v in F.gate(empty, 0.9)["bars"].items() if k != "kappa_0.6")
    assert not F.gate(a_test(10, 0), 0.9, complete=False)["met"]                                  # an answer or a verdict is missing


def test_a_word_without_a_meaning_of_its_own_is_left_out_of_the_count():
    key = {"folds": {"1": {"codes": {"W001": {"sort": "hidden", "entry": "qore", "packs": ["f1_p01"], "meaning": "king", "decoy_meaning": "woman", "own_meaning": True},
                                     "W002": {"sort": "hidden", "entry": "kroro", "packs": ["f1_p01"], "meaning": "another form of akroro", "decoy_meaning": "",
                                              "own_meaning": False},
                                     "W003": {"sort": "open", "spelling": "x", "packs": ["f1_p01"]}}}}}
    assert [h["entry"] for h in F.hidden_words(key)] == ["qore"]
    given = {(1, "f1_p01", a, c): "a king" for a in F.ALIGNERS for c in ("W001", "W002")}
    f = F.arm_figures(F.hidden_words(key), given, lambda ans, meaning: ("same", "same"))
    assert (f["hidden"], f["given"], f["right"]) == (1, 1, 1)


def test_a_word_in_several_packs_is_right_only_where_it_is_right_in_each():
    h = {"fold": 1, "code": "W001", "entry": "qore", "packs": ["f1_p01", "f1_p02", "f1_p03"], "meaning": "king", "decoy_meaning": "woman"}
    given = {(1, p, a, "W001"): f"{p} {a}" for p in ("f1_p01", "f1_p02") for a in F.ALIGNERS} | {(1, "f1_p03", "a", "W001"): "f1_p03 a"}
    good = lambda ans, meaning: ("same", "same") if meaning == "king" else ("another", "partly")     # noqa: E731
    f = F.arm_figures([h], given, good)
    assert (f["given"], f["right"], f["decoys_same"]) == (1, 1, 0) and f["words"] == [{"fold": 1, "entry": "qore", "packs": 3, "given_in": 2, "right": True, "decoy_same": False}]
    assert f["by_word_and_pack"] == {"given": 2, "right": 2, "decoy_same": 0}                    # the third pack has one answer: not given there
    one_off = lambda ans, meaning: ("same", "partly") if ans == "f1_p02 b" else good(ans, meaning)   # noqa: E731
    f = F.arm_figures([h], given, one_off)
    assert (f["given"], f["right"]) == (1, 0) and f["by_word_and_pack"] == {"given": 2, "right": 1, "decoy_same": 0}
    other_fold = F.arm_figures([h | {"fold": 2}], given, good)
    assert other_fold["given"] == 0                                                              # a code counts in its own fold only


def test_the_judges_rows_pair_each_answer_with_its_meaning_and_with_a_decoy():
    key = {"folds": {"1": {"codes": {"W001": {"sort": "hidden", "meaning": "king", "decoy_meaning": "woman", "own_meaning": True},
                                     "W002": {"sort": "hidden", "meaning": "woman", "decoy_meaning": "king", "own_meaning": True}, "W003": {"sort": "open"},
                                     "W004": {"sort": "hidden", "meaning": "another form of akroro", "decoy_meaning": "", "own_meaning": False}}}}}
    line = lambda m, frame="K1": {"meaning": m, "frame": frame, "slot": 1}                       # noqa: E731
    got = {("frames", "f1_p01", "a"): {"W001": line("a ruler"), "W002": line("none"), "W003": line("a house"), "W004": line("a god")},
           ("frames", "f1_p01", "b"): {"W001": line("A ruler"), "W002": line("a queen"), "W003": line("a house"), "W004": line("a god")},
           ("frames", "f1_p02", "a"): {"W001": line("a priest", frame="K9")},
           ("plain", "f1_p01", "a"): {"W001": line("a ruler"), "W002": line("a ruler"), "W003": line("none"), "W004": line("a god")}}
    given = F.hidden_answers(key, got, {"K1": {1}})
    assert set(given) == {("frames", 1, "f1_p01", "a", "W001"), ("frames", 1, "f1_p01", "b", "W001"), ("frames", 1, "f1_p01", "b", "W002"),
                          ("plain", 1, "f1_p01", "a", "W001"), ("plain", 1, "f1_p01", "a", "W002")}       # no "none", no open word, no K9,
    #                                                                                               and no word without a meaning of its own
    rows = F.judge_rows(key, given)
    assert sorted(rows) == ["R0001", "R0002", "R0003", "R0004"]                                  # a pair of texts stands once, whoever gave it
    assert sorted(map(tuple, rows.values())) == [("a queen", "king"), ("a queen", "woman"), ("a ruler", "king"), ("a ruler", "woman")]
    assert rows == F.judge_rows(key, given) and list(rows.values()) != [rows[r] for r in sorted(rows, key=lambda r: rows[r])]   # by lot, and the same each time
    text = F.rows_text(F.JUDGE_BRIEF, list(rows.items()), "data/sources/frames/judge/answers1/J01.jsonl")
    body = text.split("\n---\n")[1]
    assert body.count("- `R") == 4 and "4 rows" in text and not re.search(r"plain|frames|f1_p01|W00\d|aligner|decoy", body)   # no arm, no pack, no code
    assert "you are not told which rows" in F.JUDGE_BRIEF and all(f'"{v}"' in F.JUDGE_BRIEF for v in F.VERDICTS)


def test_the_count_reads_the_answers_and_the_verdicts_and_the_open_words_wait_for_the_gate():
    """The whole path on made-up files: ten hidden words that both aligners with the frames read right, the judges'
    packs, the count, and the open words' packs, which are not written until the count says the gate is met."""
    ws = [word(f"k{n}", "meaning", (f"k{n}", f"k{n}"), gloss=f"gloss {n}") for n in range(12)] + [word(f"o{n}", "unknown", (f"o{n}", "?")) for n in range(3)]
    entries = {f"k{n}": {"class": "known", "kind": "noun"} for n in range(12)}
    things = ["king", "woman", "water", "bread", "bull", "cow", "god", "life", "west", "north", "south", "milk"]
    known = {f"k{n}": {"kind": "noun", "places": 1, "texts": 1, "meaning": things[n], "from": "made up", "taken_from": "", "own_meaning": True,
                       "reading": things[n]} for n in range(12)}
    data = {"texts": [{"id": "T1", "kind": "long text", "words": ws}], "entries": entries, "known": known}
    with home() as d:
        files, key = F.build(data, {"1": [f"k{n}" for n in range(10)], "2": ["k10", "k11"]})
        F.write("packs/key.json", key)
        assert stops(F.judge_packs, "the six files of frames are not all there")
        for k in F.FRAMES:
            F.write(f"frames_{k}.json", {"frames": [{"id": f"{k}1", "slots": [{"n": 1}]}]})
        assert stops(F.judge_packs, "missing or not valid") and stops(F.open_packs, "does not say that gate B is met")
        for arm in F.ARMS:
            for fold in ("1", "2"):
                codes = key["folds"][fold]["codes"]
                for a in F.ALIGNERS:
                    lines = []
                    for c in key["folds"][fold]["packs"][f"f{fold}_p01"]:
                        k = codes[c]
                        m = (k["meaning"] if arm == "frames" else "none") if k["sort"] == "hidden" else "a house" if k["spelling"] != "o2" else "none"
                        slot = 1 if (k["sort"], k.get("spelling"), a) != ("open", "o1", "b") or fold == "1" else 7   # one answer without a slot
                        lines.append(json.dumps({"code": c, "meaning": m} | ({"frame": "K1", "slot": slot} if arm == "frames" else {})))
                    F.write_text(f"answers/{arm}/f{fold}_p01_{a}.jsonl", "\n".join(lines) + "\n")
        assert stops(F.packs, "aligners have answered")
        F.answers_check()
        F.judge_packs()
        rows = F.read("judge/key.json")["rows"]
        assert len(rows) == 24 and sorted(F.read("judge/key.json")["packs"]) == ["J01"] and (d / "judge/packs/J01_j2.md").exists()   # 12 answers, each with its decoy
        F.count()
        res = F.read("result.json")
        assert not res["complete"] and res["pairs_without_two_verdicts"] == 24 and not res["gate_met"] and stops(F.open_packs, "does not say")
        truth = {(t, t) for t in things}
        for j in F.JUDGES:
            F.write_text(f"judge/answers{j}/J01.jsonl", "\n".join(json.dumps({"row": r, "verdict": "same" if tuple(p) in truth else "another"})
                                                                   for r, p in rows.items()) + "\n")
        assert stops(F.judge_packs, "the judges have answered")
        F.count()
        res = F.read("result.json")
        fr, pl = res["frames"], res["plain"]
        assert res["complete"] and res["judges"]["kappa"] == 1.0 and res["judges"]["judged_by_both"] == 24
        assert (fr["hidden"], fr["given"], fr["right"], fr["decoys_same"]) == (12, 12, 12, 0) and fr["gate"]["met"] and res["gate_met"]
        assert (pl["given"], pl["right"]) == (0, 0) and not pl["gate"]["met"]                    # the arm without frames, counted the same way
        assert res["frames_meanings_without_a_frame_and_slot"] == 1 and res["hidden_without_a_meaning_of_their_own"] == 0   # o1 in fold 2, by b
        F.open_packs()
        o = F.read("open/key.json")
        assert list(o["rows"].values()) == [["a house", "a house"]] and (d / "open/packs/O01_j1.md").exists()   # one pair of texts, judged once
        for j in F.JUDGES:
            F.write_text(f"open/answers{j}/O01.jsonl", json.dumps({"row": "P0001", "verdict": "same"}) + "\n")
        F.count()
        op = F.read("result.json")["open"]
        assert (op["open_words"], op["pairs_with_two_meanings"], op["words_agreed"]) == (3, 3, 2)   # o0 in both folds, o1 in fold 1 only
        assert [(x["spelling"], x["stands_in_packs"], len(x["agreed_in"])) for x in op["agreed"]] == [("o0", 2, 2), ("o1", 2, 1)]   # o2: "none"
        assert op["agreed"][0]["agreed_in"][0]["frames"] == [["K1", 1], ["K1", 1]]


# ------------------------------------------------------------------------------------------ what the agents are given

def indented(text):
    return " ".join(("\n".join("    " + l if l else "" for l in text.splitlines())).split())


def test_what_the_aligners_and_the_judges_are_given_is_public():
    aligners = " ".join((ROOT / "runs/prompts/FRAMES_aligners.md").read_text(encoding="utf-8").split())
    marks = {"given": "<<what the aligner is given>>", "reason": "<<what a reason is>>", "line": "<<the line>>", "fields": "<<the frame and the slot>>\n",
             "only": "<<what it may use>>"}
    one = F.ALIGNER_BRIEF.format(repo=F.REPO, folder=F.FOLDER, pack="<pack>", code="W012", n="<n>", answers=f"{F.FOLDER}/answers/<arm>/<pack>_<a|b>.jsonl", **marks)
    assert indented(one) in aligners                                                    # one brief, word for word, its two variants marked
    assert "held back" not in F.ALIGNER_BRIEF and "known" not in F.ALIGNER_BRIEF and "check" not in F.ALIGNER_BRIEF   # no word of the known codes
    given = {arm: F.GIVEN[arm].format(repo=F.REPO, folder=F.FOLDER, digest=F.DIGEST) for arm in F.ARMS}
    for arm in F.ARMS:
        for piece in (given[arm], F.REASON[arm], F.LINE[arm].format(code="W012"), F.FIELDS[arm], F.ONLY[arm]):
            assert indented(piece) in aligners, (arm, piece)
        brief = F.brief_of(arm, "f1_p03", "b", 151, "W012")
        assert brief == one.replace(marks["given"], given[arm]).replace(marks["reason"], F.REASON[arm]) \
            .replace(marks["line"], F.LINE[arm].format(code="W012")).replace(marks["fields"], F.FIELDS[arm]).replace(marks["only"], F.ONLY[arm]) \
            .replace("<arm>", arm).replace("<pack>", "f1_p03").replace("<a|b>", "b").replace("<n>", "151")
        flat = " ".join(brief.split())
        assert 'or "none"' in flat and "Never guess for the sake of an answer" in flat and '"none" is a full answer' in flat
        assert "exactly 151 lines" in flat and "A code may be any kind of word" in flat and "packs/f1_p03.md" in flat
        assert "Do not open any other file of the repository, do not search the web" in flat and "You may not look up the inscription" in flat
        assert f"{F.FOLDER}/answers/{arm}/f1_p03_b.jsonl" in flat and "key.json" not in flat
    with_frames, alone = F.brief_of("frames", "p", "a", 3), F.brief_of("plain", "p", "a", 3)
    assert f"{F.REPO}/{F.FOLDER}/frames_digest.md" in with_frames and "frames_K" not in with_frames and '"slot": 2' in with_frames
    assert "digest" not in alone and "frames_" not in alone and '"frame"' not in alone
    assert 'a meaning without a frame and a slot of the digest counts as "none"' in " ".join(with_frames.split())
    assert list(F.FRAMES) == list("KGDWOP") and "data/sources/frames/briefs/<arm>/<pack>_<a|b>.md" in aligners
    judges = " ".join((ROOT / "runs/prompts/FRAMES_judges.md").read_text(encoding="utf-8").split())
    for brief in (F.JUDGE_BRIEF, F.OPEN_BRIEF):
        assert indented(brief.format(n="<n>", answers="<answers>", repo=F.REPO)) in judges


# ------------------------------------------------------------------------------- the page's counts and the packs

def test_the_texts_have_the_counts_of_the_page():
    text = page()
    assert F.PAGE == {"texts": 99, "words": 2945, "open": 1370, "known": 102, "places": 624}
    assert "99 texts and 2,945 words" in text and "1,370 of those words are open, and 102 dictionary words with a meaning stand in them, at 624 places" in text
    assert "(seed 20261116)" in text and "kappa of at least 0.6" in text and "At least 80% of the given words are right, on at least 10 given words" in text
    assert "at least 30 points above the share of decoys that both judges call the same" in text
    needs(*THE_MAP)
    gl, rows, lex = F.the_map(), W.corpus_rows(), W.lexicon()
    ids = F.chosen(gl, rows)
    texts = [(t, gl[t]) for t in ids]
    places = F.places_of(texts, F.with_a_meaning(gl, lex))
    assert F.counts_of(texts, places) == F.PAGE
    kinds = collections.Counter(F.kind_shown(rows[t]["kind"]) for t in ids)
    assert kinds == {"royal or temple": 87, "oracular decree": 7, "long text": 5} and sum(len(gl[t]) >= F.LONG for t in ids) == 7


def test_the_texts_file_is_the_map_as_the_test_was_set():
    needs(*THE_MAP, *LOCAL)
    data = F.read("texts.json")
    assert data == F.texts_of(F.the_map(), W.corpus_rows(), W.lexicon(), F.the_table()) and data["counts"] == F.PAGE
    known = data["known"]
    assert len(known) == 102 and sum(k["places"] for k in known.values()) == 624 and all(k["meaning"] and k["reading"] for k in known.values())
    assert collections.Counter(k["from"] for k in known.values()) == {"the public table": 77, "the layers' lines": 23, "the lexicon": 1,
                                                                      "the layers' lines, of mlowi": 1}
    table = F.the_table()
    assert all((k["meaning"] == table[e]) == (k["from"] == "the public table") for e, k in known.items() if table.get(e) and not k["taken_from"])
    assert {e: (k["taken_from"], k["meaning"]) for e, k in known.items() if k["taken_from"]} == {"mleyi": ("mlowi", "health")}   # the page's answer 3
    assert sorted(e for e, k in known.items() if not k["own_meaning"]) == ["esebe", "kroro"]   # left out of the count, hidden all the same
    assert F.read("folds.json") == F.folds_of(known)


def local():
    needs(*LOCAL)
    data, halves, key = F.read("texts.json"), F.read("folds.json")["halves"], F.read("packs/key.json")
    return data, halves, key


def tokens_of(data, hidden, fold):
    """Every word of the test with what a pack of the fold shows of it: (text, word, token, its units' codes)."""
    code, names = F.codes_of(data["texts"], data["entries"], hidden, fold), F.names_of(data["texts"], data["entries"])
    kin = F.kin_of(hidden, data["entries"])
    return [(t["id"], w, F.token(w, data["entries"], data["known"], hidden, code, names, kin), [code[u] for u in F.units_of(w, data["entries"], hidden, kin)])
            for t in data["texts"] for w in t["words"]], code


def test_the_folds_are_two_halves_of_the_102_known_words():
    data, halves, key = local()
    one, two = halves["1"], halves["2"]
    assert len(one) == len(two) == 51 and not set(one) & set(two) and sorted(one + two) == sorted(data["known"])
    assert [key["folds"][f]["hidden"] for f in ("1", "2")] == [one, two] and key["seed"] == F.SEED


def test_the_packs_are_what_the_script_builds_and_the_same_in_both_folds():
    data, halves, key = local()
    files, built = F.build(data, halves)
    assert built == key and len(files) == 20
    for name, text in files.items():
        assert (F.HOME / "packs" / f"{name}.md").read_text(encoding="utf-8") == text, name
    assert sorted(f.name for f in (F.HOME / "packs").iterdir()) == sorted([f"{n}.md" for n in files] + ["key.json"])
    assert (F.HOME / F.DIGEST).read_text(encoding="utf-8") == F.digest_of(F.the_frames())        # the digest the arm with the frames reads
    assert len(key["packs"]) == 10 and sum(len(p["texts"]) for p in key["packs"].values()) == 99 and sum(p["words"] for p in key["packs"].values()) == 2945
    sizes = {len(t["words"]) for t in data["texts"] if len(t["words"]) >= F.LONG}
    alone = [p["words"] for p in key["packs"].values() if len(p["texts"]) == 1]
    assert sorted(alone) == sorted(sizes) and len(alone) == 7                                    # a text of 100 words or more is a pack of its own
    assert all(250 <= p["words"] <= 350 for p in key["packs"].values() if len(p["texts"]) > 1)   # the others: about 300 words
    for p in key["packs"]:
        heads = [re.findall(r"^## (Text \d+) \((royal or temple|oracular decree|long text), \d+ words?\)$", files[f"f{f}_{p}"], re.M) for f in (1, 2)]
        assert heads[0] == heads[1] and [h for h, _ in heads[0]] == list(key["packs"][p]["texts"])   # the same texts under the same labels
    for name, text in files.items():
        body = text.split("## Text", 1)[1]
        assert not re.search(r"\bREM\b", body) and not any(t in body for t in key["packs"][name[3:]]["texts"].values()), name   # no number of an inscription
        n = len(key["folds"][name[1]]["packs"][name])
        assert f"## The codes of this pack: {n}" in text and f"Give each of these {n} codes one line" in text
        assert sorted(set(re.findall(r"\bW\d+\b", text.split("## Text", 1)[1]))) == key["folds"][name[1]]["packs"][name]   # every code is listed, once
        assert (F.HOME / "briefs" / "frames" / f"{name}_a.md").read_text(encoding="utf-8") == F.brief_of("frames", name, "a", n, F.example(key["folds"][name[1]]["packs"][name]))


def test_no_pack_holds_the_spelling_of_a_coded_word_or_the_gloss_of_a_hidden_one():
    data, halves, key = local()
    for fold in F.FOLDS:
        hidden = set(halves[str(fold)])
        toks, code = tokens_of(data, hidden, fold)
        coded = [(w, tok) for _, w, tok, units in toks if units]
        spellings = {f for w, _ in coded for f in [w["form"]] + [p[0] for p in w["parts"]]}
        heads = {re.sub(r"[-()]", "", re.sub(r"\s*\(\d+\)$", "", e)) for (sort, e) in code if sort != "spelling"}
        banned = {s.lower() for s in spellings | heads | {h.replace("ẖ", "X").replace("ḫ", "x") for h in heads} if s} - F.ENGLISH
        assert len(banned) > 900 and {e.lower() for e in hidden if e.isalpha()} <= banned
        gods = set(F.GODS.values())                                                              # a god's English name is a reading (Aritene is written as its entry)
        for _, w, tok, units in toks:
            text = re.sub(r"\b(?:W\d+|(?:PERSON|PLACE|NAME|GOD)-\d+)\b", " ", tok)
            found = [m.group() for m in F.suspects(text, banned) if m.group() not in gods]
            assert not found, (fold, w["form"], tok, found)                                      # no Meroitic letters of a coded word, anywhere
            if units:
                assert re.fullmatch(r"(?:\[[^\]]*\]\+)*W\d+(?:\+(?:W\d+|\[[^\]]*\]))*", tok), tok   # a coded word: codes, and readings of what is cut off it
        kin = F.kin_of(hidden, data["entries"])
        assert kin == set(key["folds"][str(fold)]["built_on_a_hidden_word"]) and kin and not kin & hidden
        for _, w, tok, units in toks:
            mine = [e for _, e in w["parts"] if e in hidden]
            built = [e for _, e in w["parts"] if e in kin]
            if w["level"] in W.READ and built:                                                   # a word built on a hidden one: a code, not its reading
                assert all(code["entry", e] in units for e in built) and not any(f"[{data['known'][e]['reading']}]" in tok for e in built), (w["form"], tok)
            if w["level"] in W.READ and mine:                                                    # a place where a hidden word stands
                assert units == [code["hidden", e] if e in hidden else code["entry", e] for e in dict.fromkeys(e for _, e in w["parts"] if e in hidden or e in kin)]
                shown = re.findall(r"\[([^\]]*)\]", tok)
                kept = {data["known"][e]["reading"] for _, e in w["parts"] if e in data["known"] and e not in hidden}
                glosses = {data["entries"][e]["gloss"] for _, e in w["parts"] if data["entries"].get(e, {}).get("gloss")}
                assert set(shown) <= kept | glosses, (w["form"], tok)                             # beside the code: only other entries' readings
                for e in mine:
                    for told in (w["gloss"], F.clean(w["gloss"]), w["reading"], data["known"][e]["meaning"], data["known"][e]["reading"]):
                        assert told not in shown and f"[{told}]" not in tok, (w["form"], tok)    # never its gloss, never its meaning
        for t in data["texts"]:                                                                  # a piece beside a hidden word does not tell the whole word
            ws = t["words"]
            for i, w in enumerate(ws):
                if w["level"] in W.READ and w["piece"] and not any(e in data["known"] for _, e in w["parts"]):
                    assert w["reading"] == "part of a word", w
    for name in sorted(F.build(data, halves)[0]):
        body = (F.HOME / "packs" / f"{name}.md").read_text(encoding="utf-8").split("## Text", 1)[1]
        assert not re.search(r"[ḫẖšñ]|\+[a-zSNX]", body), name                                   # none of the lexicon's letters, no "+lw"


def test_hidden_and_open_codes_cannot_be_told_apart_by_their_shape():
    data, halves, key = local()
    for fold in F.FOLDS:
        codes = key["folds"][str(fold)]["codes"]
        widths = {len(c) for c in codes}
        assert len(widths) == 1 and all(re.fullmatch(r"W\d+", c) for c in codes)                 # one shape
        assert sorted(codes) == [f"W{n:0{max(widths) - 1}d}" for n in range(1, len(codes) + 1)]  # one numbering, no gap
        sorts = [codes[c]["sort"] for c in sorted(codes)]
        hid = [n for n, s in enumerate(sorts) if s == "hidden"]
        assert len(hid) == 51 and sorts.count("open") == len(sorts) - 51
        thirds = collections.Counter(3 * n // len(sorts) for n in hid)
        assert all(thirds[k] >= 8 for k in range(3)), thirds                                     # the hidden words' numbers lie all over the run
        toks, code = tokens_of(data, set(halves[str(fold)]), fold)
        shape = lambda tok: re.sub(r"\[[^\]]*\]", "R", re.sub(r"W\d+", "W", tok))                 # noqa: E731
        of = {"hidden": collections.Counter(), "open": collections.Counter()}
        for _, w, tok, units in toks:
            if units:
                of["hidden" if any(codes[c]["sort"] == "hidden" for c in units) else "open"][shape(tok)] += 1
        assert set(of["hidden"]) <= set(of["open"]), set(of["hidden"]) - set(of["open"])         # every shape a hidden word takes, open words take too
        assert of["hidden"]["W"] > 0.75 * sum(of["hidden"].values()) and of["open"]["W"] > 0.75 * sum(of["open"].values())


def test_a_hidden_entry_has_one_code_in_a_fold_and_a_code_one_word():
    data, halves, key = local()
    for fold in F.FOLDS:
        hidden = set(halves[str(fold)])
        codes = key["folds"][str(fold)]["codes"]
        of = {k["entry"]: c for c, k in codes.items() if k["sort"] == "hidden"}
        assert set(of) == hidden and len(set(of.values())) == 51
        toks, code = tokens_of(data, hidden, fold)
        places, spellings = collections.Counter(), collections.defaultdict(set)
        for _, w, tok, units in toks:
            for e in dict.fromkeys(e for _, e in w["parts"] if e in hidden):
                if w["level"] in W.READ:
                    assert of[e] in re.findall(r"W\d+", tok), (e, tok)                           # every spelling of the entry, in every pack
                    places[e] += 1
                    spellings[e].add(w["form"])
        assert {e: codes[of[e]]["places"] for e in hidden} == dict(places) and max(len(s) for s in spellings.values()) >= 5
        meant = sum(data["known"][e]["places"] for e in hidden)
        assert meant <= sum(places.values()) <= meant + 2                                        # the 624 places, and where the map reads the entry as grammar
        for c, k in codes.items():
            if k["sort"] == "hidden" and not k["own_meaning"]:
                assert k["decoy"] == k["decoy_meaning"] == "" and k["entry"] in ("esebe", "kroro") and fold == 1
            elif k["sort"] == "hidden":
                d = codes[of[k["decoy"]]]
                assert k["decoy"] in hidden and k["decoy"] != k["entry"] and k["decoy_meaning"] == d["meaning"] != k["meaning"]
                assert not W.content(k["meaning"]) & W.content(d["meaning"]) and d["own_meaning"]
                assert k["meaning"] == data["known"][k["entry"]]["meaning"] and k["from"] and k["kind"] == data["known"][k["entry"]]["kind"]
            else:
                assert ("entry" in k) != ("spelling" in k) and "meaning" not in k and k["packs"] and k["places"] >= 1
    built = set(key["folds"]["1"]["built_on_a_hidden_word"]) | set(key["folds"]["2"]["built_on_a_hidden_word"])
    opened = [{(k.get("entry"), k.get("spelling")) for k in key["folds"][f]["codes"].values() if k["sort"] == "open" and k.get("entry") not in built}
              for f in ("1", "2")]
    assert opened[0] == opened[1] and len(opened[0]) == 851                                    # the open words are the same in both folds
    for f in ("1", "2"):                                                                         # and each fold codes its own built words besides
        mine = {k["entry"] for k in key["folds"][f]["codes"].values() if k["sort"] == "open" and k.get("entry") in built}
        assert set(key["folds"][f]["built_on_a_hidden_word"]) <= mine


def test_the_figures_are_counts_only():
    data, halves, key = local()
    f = F.figures()
    assert f["counts"] == F.PAGE and f["aligners"] == 80 and f["folds"]["1"]["hidden_words"] == f["folds"]["2"]["hidden_words"] == 51
    k = f["known_words"]
    assert (k["meaning_taken_from_another_word"], k["without_a_meaning_of_their_own"], k["in_more_than_one_pack"]) == (1, 2, 59)   # the page's 59 of 102
    assert [f["folds"][x]["coded_as_built_on_a_hidden_word"] for x in ("1", "2")] == [4, 3]     # qore, qor-o, qorise, qorbse; nobo, qorene, qoresem
    assert sum(f["known_words"]["by_packs_they_stand_in"].values()) == 102 and len(f["packs"]) == 10
    assert sum(p["words"] for p in f["packs"]) == 2945 and all(abs(p["fold_1"]["open"] - p["fold_2"]["open"]) <= 4 for p in f["packs"])

    def leaves(x):
        if isinstance(x, dict):
            for k, v in x.items():
                yield k
                yield from leaves(v)
        elif isinstance(x, list):
            for v in x:
                yield from leaves(v)
        else:
            yield x
    words = set(data["known"]) | set(data["entries"]) | {w["form"] for t in data["texts"] for w in t["words"] if w["level"] != "number"}
    told = {k["meaning"] for k in data["known"].values()} | {k["reading"] for k in data["known"].values()}
    for leaf in leaves(f):
        assert not isinstance(leaf, str) or (leaf not in words and leaf not in told), leaf       # no word, no meaning


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
