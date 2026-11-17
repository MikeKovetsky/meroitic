"""Checks for the rounds of F4, ways of translating whole texts compared (src/f4r.py).

  python3 -I tests/test_f4r.py

Millet 2005, Rilly's lexicon, the map's gloss file, the handbook and the agents' answers are local only: the
checks of the method run on made-up texts, units and answers; the checks of the reported numbers read the public
figures file and compare it with a count from the local files where those are present.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import f4 as F                       # noqa: E402
import f4r as R                      # noqa: E402
from local_only import needs, run    # noqa: E402

NAMES = list(R.ROUNDS["r1"]["readings"])


def g(form, level, gloss="", **more):
    return {"form": form, "level": level, "gloss": gloss, **more}


def lines(path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in items), encoding="utf-8")


def test_the_glosses_show_what_the_analyst_read_of_an_unknown_word():
    # the pilot's baseline gave "?" here; the translators' packs showed the gloss
    assert F.word_reading(g("Sklte", "unknown", "in Skl")) == "[Sklte: ?]"
    assert R.word_reading(g("Sklte", "unknown", "in Skl")) == "[Sklte: in Skl (?)]"
    assert R.word_reading(g("abc", "unknown", "")) == "[abc: ?]"
    assert R.word_reading(g("abc", "unknown", "?")) == "[abc: ?]"
    # every other level reads as in the pilot
    for w in (g("wos", "meaning", "Isis"), g("x.y", "lost", "<x.y>"), g("pqr", "kind", "[a title]"),
              g("yetmde", "hypothesis", "nephew")):
        assert R.word_reading(w) == F.word_reading(w)
    # a gloss withheld from the translators is withheld here too, also on an unknown word
    held = g("bqol", "unknown", "a made-up gloss cut short", parts=[{"entry": "bqo"}])
    assert R.word_reading(held, frozenset({"bqo"})) == "[bqol: ?]"
    assert R.word_reading(g("abc", "unknown", "as Millet reads it")) == "[abc: ?]"
    assert R.glosses([g("wos", "meaning", "Isis"), g("Sklte", "unknown", "in Skl")]) == "Isis · [Sklte: in Skl (?)]"


def test_the_status_of_a_word_by_script():
    lex = {"a": {"status": "established"}, "b": {"status": "hypothesis"}, "c": {"status": "probable"}}
    st = {"a": "agreed by two scholars", "d": "disputed", "e": "stated by one"}
    assert R.f2_status("a", st, lex) == "agreed" and R.f2_status("d", st, lex) == "disputed"
    assert R.f2_status("c", st, lex) == "stated by one"        # not rated by F2, probable for Rilly
    assert R.f2_status("b", st, lex) == "proposed" and R.f2_status("zz", st, lex) == "proposed"
    assert R.weakest(["agreed", "stated by one"]) == "stated by one"
    assert R.weakest(["agreed", "disputed", "stated by one"]) == "disputed"
    assert R.weakest(["agreed", "proposed", "disputed"]) == "proposed"
    assert R.weakest([]) == "proposed" and R.weakest(["something else"]) == "proposed"
    word = lambda level, *heads, gloss="x": g("w", level, gloss, parts=[{"entry": h} for h in heads])   # noqa: E731
    assert R.map_status(word("meaning", "a"), st, lex) == "agreed"
    assert R.map_status(word("meaning", "a", "e"), st, lex) == "stated by one"
    assert R.map_status(word("grammar", "a", "d"), st, lex) == "disputed"
    assert R.map_status(word("hypothesis", "a"), st, lex) == "proposed"
    for level in ("lost", "name", "number"):
        assert R.map_status(word(level), st, lex) == level
    assert R.map_status(word("unknown"), st, lex) == "open" and R.map_status(word("kind"), st, lex) == "open"
    assert R.map_status(word("meaning", "a"), st, lex, frozenset({"a"})) == "open"      # its gloss is withheld
    assert all(R.map_status(word(l, "a"), st, lex) in F.STATUSES for l in
               ("meaning", "grammar", "hypothesis", "kind", "unknown", "lost", "name", "number"))


def test_the_parallels():
    gl = {"T1": [g("wos", "meaning", "Isis"), g("smlo", "kind", "[a title]"), g("12", "number", "12"),
                 g("ab", "meaning", "x"), g("x.y", "lost", "<x.y>")],
          "T2": [g("a1", "name", "A"), g("a2", "name", "B"), g("a3", "name", "C"), g("a4", "name", "D"),
                 g("smlo", "kind", "[a title]"), g("b1", "name", "E"), g("b2", "name", "F"), g("b3", "name", "G"),
                 g("b4", "name", "H"), g("smlo", "kind", "[a title]")],
          "T3": [g("smlo", "kind", "[a title]"), g("12", "number", "12"), g("ab", "meaning", "x"), g("x.y", "lost", "")]}
    for i in range(R.COMMON + 1):
        gl[f"W{i:02d}"] = [g("wos", "meaning", "Isis")]
    rows = {t: {"site": "Somewhere"} for t in gl}
    out = R.parallels("T1", gl, rows)
    text = "\n".join(out)
    # a word of the formulae gets its count only
    assert f"- `wos`: in {R.COMMON + 1} other texts (a word of the formulae)." in out
    # smlo: two other texts, one place each (the first of a text), WIDTH words on each side, its own text left out
    assert "- `smlo`: in 2 other texts." in out
    assert "  - T2 (Somewhere): a2 a3 a4 **smlo** b1 b2 b3 = B · C · D · [smlo: a title] · E · F · G" in out
    assert "  - T3 (Somewhere): **smlo** 12 ab x.y = [smlo: a title] · 12 · x · [x.y: signs lost]" in out
    assert sum(l.startswith("  - T2") for l in out) == 1 and sum(l.startswith("  - T3") for l in out) == 1
    assert not any(l.startswith("  - T1") for l in out)
    # a number, a word with lost signs and a word of two letters get none
    assert "`12`" not in text and "`x.y`" not in text and "`ab`" not in text
    # at most PARALLELS places for a word
    many = {"T": [g("zzz", "unknown")], **{f"P{i}": [g("zzz", "unknown")] for i in range(R.PARALLELS + 2)}}
    assert sum(l.startswith("  - ") for l in R.parallels("T", many, {t: {"site": "S"} for t in many})) == R.PARALLELS
    # a row of the corpus that names Millet (a phrase his thesis quotes) is shown without his name
    named = {"T": [g("zzz", "unknown")], "Millet 1968 p. 362 (MilletExamples.txt line 4)": [g("zzz", "unknown")],
             "S": [g("zzz", "unknown")]}
    out = R.parallels("T", named, {"T": {"site": "x"}, "S": {"site": "after Millet"},
                                   "Millet 1968 p. 362 (MilletExamples.txt line 4)": {"site": ""}})
    assert not F.MILLET.search("\n".join(out)) and "  - a phrase quoted in a study of 1968: **zzz** = [zzz: ?]" in out
    assert "  - S: **zzz** = [zzz: ?]" in out
    # a word that stands nowhere else gets no line
    assert R.parallels("T", {"T": [g("only", "unknown")]}, {"T": {"site": "S"}}) == []


def test_the_splitter_cuts_a_unit_open_in_part():
    assert "true only when Millet leaves ALL of the unit untranslated" in R.SPLIT
    assert "true when Millet leaves the Meroitic untranslated" not in R.SPLIT
    assert "true when Millet leaves the Meroitic untranslated" in F.SPLIT          # the pilot's rule, unchanged
    pack = R.splitter_pack("GA 99", {("GA99",): "GA99: a stela\nTEXT\n1: wos\nRENDERING\nO Isis\n"},
                           "answers/GA99.jsonl")
    assert "## GA99" in pack and "1: wos" in pack and "O Isis" in pack and "`answers/GA99.jsonl`" in pack
    assert "{" not in pack.split("---")[0].replace('{"text"', "").replace('false}', "")       # every field filled


def test_the_judges_packs_hold_at_most_twenty_units():
    units = [{"unit": f"U{i:02d}", "open": i % 5 == 0} for i in range(1, 51)]          # 40 to judge
    cs = R.chunks(units)
    assert [len(c) for c in cs] == [20, 20] and [u for c in cs for u in c] == [u["unit"] for u in units if not u["open"]]
    assert [len(c) for c in R.chunks([{"unit": f"U{i}", "open": False} for i in range(45)])] == [15, 15, 15]
    assert [len(c) for c in R.chunks([{"unit": f"U{i}", "open": False} for i in range(21)])] == [11, 10]
    assert [len(c) for c in R.chunks([{"unit": "U1", "open": False}])] == [1]
    assert R.chunks([{"unit": "U1", "open": True}]) == [] and R.chunks([]) == []
    assert all(len(c) <= R.CHUNK for n in range(1, 130) for c in R.chunks([{"unit": str(i), "open": False} for i in range(n)]))


def test_each_judge_has_an_order_of_their_own():
    a = R.order_of("r1", 1, "GA 28", NAMES)
    assert sorted(a.values()) == sorted(NAMES) and list(a) == list(R.LETTERS[:len(NAMES)])
    assert a == R.order_of("r1", 1, "GA 28", NAMES)                       # the same on every call
    orders = {tuple(R.order_of("r1", j, t, NAMES).values()) for j in (1, 2) for t in ("GA 28", "GA 41", "GA 53")}
    assert len(orders) > 1
    assert R.order_of("r1", 1, "GA 28", NAMES) != R.order_of("r2", 1, "GA 28", NAMES) or \
        R.order_of("r1", 2, "GA 28", NAMES) != R.order_of("r2", 2, "GA 28", NAMES)


def test_a_judges_pack():
    units = [{"unit": "U01", "kind": "name", "english": "the deceased is X", "open": False},
             {"unit": "U02", "kind": "title", "english": "arebetke", "open": True},
             {"unit": "U03", "kind": "place", "english": "in Faras", "open": False}]
    order = {"A": "panel", "B": "decoy", "C": "glosses"}
    pack = R.judge_pack("GA 99", "The deceased is X.", units, ["U01"], order,
                        {"panel": "PANEL TEXT", "decoy": "DECOY TEXT", "glosses": "GLOSS TEXT"}, "answers/judge1/GA99_1.jsonl")
    assert "| U01 | name | the deceased is X |" in pack and "U03" not in pack and "arebetke" not in pack
    assert pack.index("### Reading A\n\nPANEL TEXT") < pack.index("### Reading B\n\nDECOY TEXT") < pack.index("### Reading C\n\nGLOSS TEXT")
    assert "panel" not in pack and "decoy" not in pack.lower().replace("decoy text", "")       # no name of a reading
    assert '"Reading A" to "Reading C"' in pack and "exactly 3 lines" in pack and '"text": "GA99"' in pack
    assert "whether two names are the\n   same place" in pack and "judge the first" in pack


def test_the_second_judging_has_one_rule_more():
    assert "4. Kinship." not in R.JUDGE_RULES[1] and R.JUDGE_RULES[1] == R.JUDGE
    two = R.JUDGE_RULES[2]
    assert two.replace(R.KIN, "").replace("Four rules:", "Three rules:") == R.JUDGE          # nothing else differs
    assert two.index("3. Judge only by") < two.index("4. Kinship.") < two.index("Write to the file")
    units = [{"unit": "U01", "kind": "name", "english": "she was related to X", "open": False}]
    args = ("GA 99", "She was related to X.", units, ["U01"], {"A": "glosses", "B": "decoy"}, {"glosses": "g", "decoy": "d"}, "a.jsonl")
    assert "4. Kinship." not in R.judge_pack(*args) and "4. Kinship." in R.judge_pack(*args, rules=2)
    assert "the verdict is\n   \"partly\": one of them says more than the other" in R.judge_pack(*args, rules=2)
    # the second judging reads the first round's readings, has an order of its own, and no packs but the judges'
    assert R.source("r1") == "r1" and R.source("r1b") == "r1" and R.ROUNDS["r1b"]["judging"] == 2
    assert R.ROUNDS["r1b"]["readings"] == R.ROUNDS["r1"]["readings"] and R.ROUNDS["r1b"]["texts"] == R.ROUNDS["r1"]["texts"]
    orders = [(R.order_of("r1", j, t, NAMES), R.order_of("r1b", j, t, NAMES)) for j in (1, 2) for t in ("GA 28", "GA 41", "GA 53")]
    assert any(a != b for a, b in orders)
    for fn in (R.packs, R.editors):
        try:
            fn("r1b")
            raise AssertionError(f"{fn.__name__} wrote packs for a round that judges another's readings")
        except SystemExit as e:
            assert "judges the readings of r1" in str(e)


def test_the_packs_keep_millet_out_and_say_the_rules():
    m = {"rows": {"T 1": {"site": "Faras", "kind": "funerary"}},
         "gl": {"T 1": [g("wos", "meaning", "Isis", parts=[{"entry": "Wos"}]),
                        g("bqol", "meaning", "a made-up gloss cut short", parts=[{"entry": "bqo"}]),
                        g("abc", "unknown", "as Millet reads it", by="analyst", evidence="Millet 1973 has it")]},
         "lex": {"Wos": {"headword": "Wos", "kind": "god name", "page": 259, "status": "established", "meaning": "Isis",
                         "proposals": [{"author": "Millet 1973", "proposal": "a goddess"},
                                       {"author": "Griffith 1911", "proposal": "Isis"}]},
                 "bqo": {"headword": "bqo", "kind": "verb", "page": 60, "status": "hypothesis",
                         "meaning": "a made-up gloss (Millet)", "proposals": []}},
         "st": {"Wos": "agreed by two scholars"}, "ours": {"Wos": "the goddess Isis", "bqo": "our made-up wording"},
         "withheld": frozenset({"bqo"})}
    for pack in (R.translator_pack("T 1", m, "THE BOOK", "a.jsonl"), R.writer_pack("T 1", m, "THE BOOK", "a.jsonl"),
                 R.editor_pack("T 1", m, "THE BOOK", [{"words": [], "translation": "x"}] * 3, "a.jsonl")):
        assert not F.MILLET.search(pack), pack
        assert "THE BOOK" in pack and "`a.jsonl`" in pack and "Lose nothing the materials hold" in pack
        assert "made-up gloss" not in pack and "made-up wording" not in pack
    t = R.translator_pack("T 1", m, "THE BOOK", "a.jsonl")
    assert "| 1 | wos | meaning | Isis | Wos (agreed by two scholars) |" in t and "Griffith 1911: Isis" in t
    assert "## Other places in the corpus where these words stand\n\nNone." in t
    w = R.writer_pack("T 1", m, "THE BOOK", "a.jsonl")
    assert "| 1 | wos | Isis | agreed |" in w and "| 2 | bqol | [bqol: ?] | open |" in w and "| 3 | abc | [abc: ?] | open |" in w
    assert "The entries of the lexicon" not in w                      # the writer sees the map's readings only
    e = R.editor_pack("T 1", m, "THE BOOK", [{"words": [{"n": 1, "form": "wos", "reading": "Isis", "status": "agreed"}],
                                               "translation": f"reading {k}"} for k in (1, 2, 3)], "a.jsonl")
    assert e.index("## Translator T1") < e.index("## Translator T2") < e.index("## Translator T3") < e.index("## T 1")
    assert "Translation: reading 2" in e and "Do not add a meaning that none of the three gives" in e


def test_the_checkers_verdicts_on_the_handbook():
    book = "\n".join(["# Title", "- one [A, p. 1, established]", "- two [A, p. 2, probable]", "- three [A, p. 3, proposal]",
                      "a line without a source", "- four [A, p. 4, established]", "- five [A, p. 5, established]",
                      "- six [A, p. 6, established]"])
    verdicts = [{"line": 2, "verdict": "confirmed"}, {"line": 2, "verdict": "unsupported"},          # the first counts
                {"line": 3, "verdict": "corrected", "text": "- two, as the source has it [A, p. 2, proposal]"},
                {"line": 4, "verdict": "unsupported"},
                {"line": 5, "verdict": "unsupported"},                                             # not a sourced line
                {"line": 6, "verdict": "corrected", "text": "- four, without a source"},            # no source: dropped
                {"line": 7, "verdict": "corrected", "text": "- five, as Millet has it [A, p. 5, established]"},
                {"line": 99, "verdict": "confirmed"}, {"line": "8", "verdict": "unsupported"}, {"line": 8, "verdict": "fine"}]
    text, counts = R.apply_check(book, verdicts)
    assert text.split("\n") == ["# Title", "- one [A, p. 1, established]", "- two, as the source has it [A, p. 2, proposal]",
                                "a line without a source", "- six [A, p. 6, established]"]
    assert counts == {"sourced": 6, "confirmed": 1, "corrected": 1, "unsupported": 1, "corrected_without_a_line": 2,
                      "unchecked": 1}
    assert R.apply_check(book, []) == (book, {"sourced": 6, "unchecked": 6})


def test_the_handbook_may_not_name_millet():
    with tempfile.TemporaryDirectory() as d:
        old, check = R.HANDBOOK, R.CHECK
        try:
            R.HANDBOOK, R.CHECK = Path(d) / "handbook.md", Path(d) / "handbook_check"
            R.HANDBOOK.write_text("The copula is -o [Rilly 2003, p. 117].\n", encoding="utf-8")
            try:
                R.handbook()
                raise AssertionError("a handbook that was not checked was read")
            except SystemExit as e:
                assert "has not been checked" in str(e)
            R.HANDBOOK.unlink()
            lines(R.CHECK / "counts.json", [{"sourced": 1}])
            try:
                R.handbook()
                raise AssertionError("a missing handbook was read")
            except SystemExit:
                pass
            R.HANDBOOK.write_text("The copula is -o [Rilly 2003, p. 117].\n", encoding="utf-8")
            assert R.handbook() == "The copula is -o [Rilly 2003, p. 117]."
            R.HANDBOOK.write_text("As Millet (2005) reads it.\n", encoding="utf-8")
            try:
                R.handbook()
                raise AssertionError("a handbook that names Millet was read")
            except SystemExit:
                pass
        finally:
            R.HANDBOOK, R.CHECK = old, check


def test_one_reading_against_another_unit_by_unit():
    v = {("T", "U1", "panel"): "given", ("T", "U1", "glosses"): "partly",
         ("T", "U2", "panel"): "wrong", ("T", "U2", "glosses"): "missing",       # an open word beats a wrong one
         ("T", "U3", "panel"): "partly", ("T", "U3", "glosses"): "partly",
         ("T", "U4", "panel"): "given"}                                          # no verdict on the glosses: not counted
    assert R.compare(v, [("T", f"U{i}") for i in range(1, 5)], "panel") == {"better": 1, "worse": 1, "same": 1}


def test_the_rule_for_what_is_carried_on():
    wrong = {n: 0.05 for n in NAMES}
    s = {"pilot": 0.9, "glosses": 0.60, "writer": 0.58, "translator": 0.66, "panel": 0.65, "decoy": 0.0}
    assert R.carried(s, wrong, NAMES) == "translator"                      # the best of the two, 5 points or more ahead
    assert R.carried({**s, "panel": 0.70}, wrong, NAMES) == "panel"
    assert R.carried({**s, "translator": 0.66, "panel": 0.66}, wrong, NAMES) == "translator"   # a tie: the simpler
    # too many wrong units: left out, however good its score
    assert R.carried({**s, "panel": 0.80}, {**wrong, "panel": 0.08}, NAMES) == "translator"
    assert R.carried({**s, "panel": 0.80}, {**wrong, "panel": 0.07}, NAMES) == "panel"         # 2 points over is allowed
    # a lead under 5 points is no lead: the writer if it keeps the glosses' meaning, else the glosses
    assert R.carried({**s, "translator": 0.64, "panel": 0.649}, wrong, NAMES) == "writer"
    assert R.carried({**s, "translator": 0.64, "panel": 0.64, "writer": 0.56}, wrong, NAMES) == "glosses"
    assert R.carried({**s, "translator": 0.64, "panel": 0.64, "writer": 0.57}, wrong, NAMES) == "writer"
    # the pilot's translator is never carried, and without the glosses' score nothing is
    assert R.carried({**s, "translator": 0.5, "panel": 0.5, "writer": 0.4}, wrong, NAMES) == "glosses"
    assert R.carried({**s, "glosses": None}, wrong, NAMES) is None
    # a judging that misses a bar carries nothing: the judging is changed first
    met = {"kappa": True, "decoys_accepted": True}
    assert R.carried(s, wrong, NAMES, met) == "translator"
    assert R.carried(s, wrong, NAMES, {**met, "kappa": False}) is None
    assert R.carried(s, wrong, NAMES, {**met, "decoys_accepted": False}) is None


def made_up_round(base, verdicts2=None):
    """A round of one text, three units judged (one of them not in our copy) and one open, two judges."""
    rnd = "r1"
    units = [{"text": "GA99", "unit": "U01", "english": "the deceased is Malo", "meroitic": "mlo", "kind": "name", "open": False},
             {"text": "GA99", "unit": "U02", "english": "arebetke", "meroitic": "arebetke", "kind": "title", "open": True},
             {"text": "GA99", "unit": "U03", "english": "in Faras", "meroitic": "phrste", "kind": "place", "open": False},
             {"text": "GA99", "unit": "U04", "english": "a priest", "meroitic": "zzzzzz", "kind": "title", "open": False}]
    lines(base / "split" / "answers" / "GA99.jsonl", units)
    order = {str(j): {"GA 99": R.order_of(rnd, j, "GA 99", NAMES)} for j in (1, 2)}
    key = {"round": rnd, "texts": ["GA 99"], "readings": NAMES, "decoys": {}, "decoy_shared_words": {}, "order": order,
           "chunks": {"GA 99": [["U01", "U03", "U04"]]},
           "units": {"GA 99": {"U01": {"kind": "name", "open": False, "doubt": False, "in_copy": True, "clean": True},
                               "U02": {"kind": "title", "open": True, "doubt": False, "in_copy": True, "clean": True},
                               "U03": {"kind": "place", "open": False, "doubt": False, "in_copy": True, "clean": False},
                               "U04": {"kind": "title", "open": False, "doubt": False, "in_copy": False, "clean": True}}}}
    (base / rnd).mkdir(parents=True, exist_ok=True)
    (base / rnd / "key.json").write_text(json.dumps(key), encoding="utf-8")
    one = {"U01": {"pilot": "partly", "glosses": "partly", "writer": "partly", "translator": "given", "panel": "given",
                   "decoy": "wrong"},
           "U03": {"pilot": "missing", "glosses": "wrong", "writer": "wrong", "translator": "given", "panel": "partly",
                   "decoy": "given"},
           "U04": {"pilot": "given", "glosses": "given", "writer": "given", "translator": "wrong", "panel": "wrong",
                   "decoy": "wrong"}}
    for j, verdicts in ((1, one), (2, verdicts2 or one)):
        letter = {name: l for l, name in order[str(j)]["GA 99"].items()}
        rows = [{"text": "GA99", "unit": u, "reading": letter[n], "verdict": v} for u in verdicts for n, v in verdicts[u].items()]
        rows.append({"text": "GA99", "unit": "U02", "reading": "A", "verdict": "given"})        # an open unit: not read
        rows.append({"text": "GA99", "unit": "U01", "reading": "Z", "verdict": "given"})        # no such reading
        lines(base / rnd / "answers" / f"judge{j}" / "GA99_1.jsonl", rows)
    return rnd


def test_the_count_of_a_made_up_round():
    with tempfile.TemporaryDirectory() as d:
        old = R.OUT
        try:
            R.OUT = Path(d)
            rnd = made_up_round(R.OUT)
            f = R.count(rnd)
        finally:
            R.OUT = old
    assert f["units"] == {"all": 4, "open": 1, "judged": 3, "not_in_copy": 1, "scored": 2,
                          "not_in_copy_per_text": {"GA 99": 1}, "open_with_a_translated_part": 0,
                          "by_kind": {"name": 1, "place": 1}, "per_text": {"GA 99": 2}}
    # U04 is not in our copy and is not scored: translator 2 given of 2, panel 1.5, glosses and writer 0.5 of 2
    assert f["score"] == {"pilot": 0.25, "glosses": 0.25, "writer": 0.25, "translator": 1.0, "panel": 0.75, "decoy": 0.5}
    assert f["wrong"]["glosses"] == 0.5 and f["wrong"]["translator"] == 0.0 and f["given"]["panel"] == 0.5
    assert f["lead"] == {"pilot": 0.0, "writer": 0.0, "translator": 0.75, "panel": 0.5}
    assert f["unit_by_unit"]["1"]["translator"] == {"better": 2} and f["unit_by_unit"]["1"]["writer"] == {"same": 2}
    assert f["unit_by_unit"]["1"]["pilot"] == {"same": 1, "better": 1}             # missing is better than wrong
    assert f["panel_against_translator"] == {"1": {"same": 1, "worse": 1}, "2": {"same": 1, "worse": 1}}
    assert f["per_text"]["GA 99"]["panel"] == 0.75 and f["by_kind"]["place"]["translator"] == 1.0
    assert f["agreement"]["pairs"] == 10 and f["agreement"]["same"] == 10          # five real readings, two units
    # the decoy counts on clean units only: U01 (wrong); U03's decoy shares a word with it and is left out
    assert f["decoys_measure"]["1"] == {"clean_units": 1, "accepted": 0, "verdicts": {"wrong": 1}}
    assert f["bars"] == {"kappa": True, "decoys_accepted": True}
    assert f["carried"] == "translator"                # the best score, and no more wrong units than the glosses
    assert f["rule"] == {"lead": R.LEAD, "wrong_over": R.WRONG_OVER, "writer_loss": R.WRITER_LOSS}
    assert f["agreement"]["kappa_credited_or_not"] == 1.0 and f["agreement"]["units_judged_differently"] == 0
    assert f["agreement"]["per_text"] == {"GA 99": {"pairs": 10, "same": 10, "kappa": None}}       # under 20 lines
    assert f["agreement"]["differing_pairs"] == {}
    assert f["of"] == "r1" and f["judging"] == 1


def test_two_judges_who_differ():
    two = {"U01": {"pilot": "given", "glosses": "given", "writer": "given", "translator": "partly", "panel": "partly",
                   "decoy": "partly"},
           "U03": {"pilot": "wrong", "glosses": "missing", "writer": "missing", "translator": "wrong", "panel": "wrong",
                   "decoy": "wrong"}}
    with tempfile.TemporaryDirectory() as d:
        old = R.OUT
        try:
            R.OUT = Path(d)
            f = R.count(made_up_round(R.OUT, two))
        finally:
            R.OUT = old
    assert f["scores"]["2"]["translator"]["score"] == 0.25 and f["score"]["translator"] == 0.625   # the judges' mean
    assert f["agreement"]["same"] == 0 and f["bars"]["kappa"] is False
    assert f["decoys_measure"]["2"]["accepted"] == 1 and f["bars"]["decoys_accepted"] is False     # 1 of 1 clean unit
    assert f["carried"] is None                        # a bar missed: nothing is carried, the judging is changed first
    # where the judges part, each pair in the order of the alphabet: U01 given against partly for all five readings;
    # U03 missing against wrong for the pilot, the glosses and the writer, the translator given against wrong, the
    # panel partly against wrong
    assert f["agreement"]["differing_pairs"] == {"given / partly": 5, "given / wrong": 1, "missing / wrong": 3,
                                                 "partly / wrong": 1}
    assert list(f["agreement"]["differing_pairs"]) == sorted(f["agreement"]["differing_pairs"])


def test_a_judges_line_counts_only_for_the_units_of_its_pack():
    with tempfile.TemporaryDirectory() as d:
        old = R.OUT
        try:
            R.OUT = Path(d)
            rnd = made_up_round(R.OUT)
            key = json.loads((R.OUT / rnd / "key.json").read_text(encoding="utf-8"))
            key["chunks"]["GA 99"] = [["U01"], ["U03", "U04"]]                 # the same units, in two packs
            (R.OUT / rnd / "key.json").write_text(json.dumps(key), encoding="utf-8")
            letter = {name: l for l, name in key["order"]["1"]["GA 99"].items()}
            one = R.OUT / rnd / "answers" / "judge1"
            rows = [json.loads(l) for l in (one / "GA99_1.jsonl").read_text(encoding="utf-8").splitlines()]
            glosses = {"text": "GA99", "unit": "U01", "reading": letter["glosses"]}
            # pack 1 held U01 only: its lines for U03 (here "wrong" for every reading, where pack 2, which held U03,
            # gives the translator "given") are not read, and its line for U01's glosses stands in a file of no pack
            lines(one / "GA99_2.jsonl", [r for r in rows if r["unit"] in ("U03", "U04")])
            lines(one / "GA99_1.jsonl", [{**r, "verdict": "wrong"} if r["unit"] == "U03" else r for r in rows
                                         if {k: r[k] for k in glosses} != glosses])
            lines(one / "GA99_3.jsonl", [{**glosses, "verdict": "given"}])
            v = R.verdicts_of(rnd, key, 1)
            f = R.count(rnd)
        finally:
            R.OUT = old
    assert v[("GA 99", "U03", "translator")] == "given" and ("GA 99", "U01", "glosses") not in v
    assert {u for _, u, _ in v} == {"U01", "U03", "U04"} and len(v) == 3 * len(NAMES) - 1
    assert f["score"]["translator"] == 1.0 and f["scores"]["1"]["glosses"]["unanswered"] == 1


def test_the_packs_are_not_written_again():
    with tempfile.TemporaryDirectory() as d:
        old = R.OUT
        try:
            R.OUT = Path(d)
            lines(R.OUT / "split" / "answers" / "GA99.jsonl", [{"text": "GA99"}])
            lines(R.OUT / "r1" / "answers" / "writer" / "GA99.jsonl", [{"text": "GA99"}])
            lines(R.OUT / "r1" / "answers" / "editor" / "GA99.jsonl", [{"text": "GA99"}])
            lines(R.OUT / "r1" / "answers" / "judge1" / "GA99_1.jsonl", [{"text": "GA99"}])
            for fn, args in ((R.split, ()), (R.packs, ("r1",)), (R.judges, ("r1",))):
                try:
                    fn(*args)
                    raise AssertionError(f"{fn.__name__} wrote its packs again")
                except SystemExit as e:
                    assert "not writing" in str(e), e
        finally:
            R.OUT = old


def test_the_decoys_of_the_held_texts():
    import itertools
    import random
    # assign() finds the least total, as trying every order does
    rnd = random.Random(7)
    for n, m in ((1, 1), (2, 3), (4, 4), (5, 7)):
        cost = {f"r{i}": {f"c{j}": rnd.randint(0, 6) for j in range(m)} for i in range(n)}
        got = R.assign(cost)
        assert sorted(got) == sorted(cost) and len(set(got.values())) == n
        best = min(sum(cost[r][c] for r, c in zip(sorted(cost), perm))
                   for perm in itertools.permutations([f"c{j}" for j in range(m)], n))
        assert sum(cost[r][got[r]] for r in cost) == best
    assert R.assign({"a": {"x": 1, "y": 0}, "b": {"x": 0, "y": 0}}) == {"a": "y", "b": "x"}
    assert R.assign({"a": {"x": 3}, "b": {"y": 2, "x": 0}}) == {"a": "x", "b": "y"}       # a column a row lacks
    try:
        R.assign({"a": {"x": 1}, "b": {"x": 1}})
        raise AssertionError("two rows got one column")
    except ValueError:
        pass
    # the sample: open rows of the right size and kind, not from Gebel Adda, not taken
    def row(kind, site="Karanog", open_=True):
        return {"kind": kind, "site": site, "open": open_}
    kinds = list(R.PAGES2)
    rows, gl = {}, {}
    for k in kinds:
        for i in range(12):
            rows[f"{k[:3]}{i:02d}"] = row(k)
    rows.update({"GA 99": row(kinds[0]), "adda1": row(kinds[0], "Gebel Adda, cemetery 3"), "closed": row(kinds[0], open_=False),
                 "short": row(kinds[0]), "lost": row(kinds[0]), "taken": row(kinds[0])})
    gl = {i: [g("w", "meaning", "x")] * 10 for i in rows}
    gl["short"] = [g("w", "meaning", "x")] * (F.MIN_WORDS - 1)
    gl["lost"] = [g("w", "lost", "")] * 5 + [g("w", "meaning", "x")] * 5
    out = R.pages2(rows, gl, {"taken"})
    assert len(out) == sum(R.PAGES2.values()) == len(set(out)) and out == R.pages2(rows, gl, {"taken"})
    assert not set(out) & {"GA 99", "adda1", "closed", "short", "lost", "taken"}
    assert [sum(rows[i]["kind"] == k for i in out) for k in kinds] == list(R.PAGES2.values())
    assert R.file_of("REM 0091c") == "REM0091c" and R.file_of("Meroe 27") == "Meroe27" and R.file_of("Kar. 4/a") == "Kar4a"
    # the held round: the panel's design beside the glosses, judged by the second judging's rules, decoys of its own
    h = R.ROUNDS["held"]
    assert h["texts"] == "held" and h["judging"] == 2 and h["decoys"] == "pages2" and R.source("held") == "held"
    assert h["readings"] == ("glosses", "writer", "translator", "panel", "decoy")


def test_the_texts_held_back():
    needs("data/sources/f4/texts.json")
    s = R.sets()
    assert s["dev"] == ["GA 47", "GA 41", "GA 28", "GA 53", "GA 37"] and len(s["held"]) == 13
    assert not set(s["dev"]) & set(s["held"]) and s["held"] == sorted(s["held"])
    made = R.sets({"pilot": ["B"], "pages": ["P"], "candidates": [{"id": "C"}, {"id": "B"}, {"id": "A"}]})
    assert made == {"dev": ["B"], "held": ["A", "C"], "pages": ["P"]}


def between(text, start, end):
    i = text.index(start)
    return text[i: text.index(end, i + len(start))]


def pct(x):
    return f"{100 * x:.1f}%"


PAGE = ROOT / "data/discovery/f4_rounds.md"
SECTIONS = {"r1": ("## 5. Round one, first judging", "## 6. "), "r1b": ("## 6. Round one, second judging", "## 7. "),
            "held": ("## 8. The result on the held texts", "## 9. ")}


def test_the_public_figures_are_the_count():
    needs("data/sources/f4r/held/key.json", "data/sources/f4r/r1/key.json", "data/sources/f4r/r1b/key.json",
          "data/sources/f4/texts.json", "data/sources/v6/analysts/glosses.jsonl")
    public = json.loads(R.PUBLIC.read_text(encoding="utf-8"))
    assert sorted(public) == ["held", "r1", "r1b"]
    for rnd in public:
        assert public[rnd] == json.loads(json.dumps(R.count(rnd))), rnd


def test_the_page_quotes_the_figures():
    public = json.loads(R.PUBLIC.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    for rnd, (start, end) in SECTIONS.items():
        f, part = public[rnd], " ".join(between(page, start, end).split())
        s = f["scores"]
        for n in f["readings"]:
            row = next(l for l in between(page, start, end).splitlines() if l.startswith(f"| {n} |"))
            assert f"| {pct(s['1'][n]['score'])} | {pct(s['2'][n]['score'])} | {pct(f['score'][n])} | {pct(f['given'][n])} |" in row, (rnd, n)
            if n != "decoy":
                assert f"| {pct(f['wrong'][n])} |" in row, (rnd, n)
            if n in f["lead"]:
                assert row.rstrip().endswith(f"| +{100 * f['lead'][n]:.1f} |"), (rnd, n)
        u, a = f["units"], f["agreement"]
        if rnd != "r1b":                 # the second judging has the first's units, and its section does not repeat them
            assert f"into {u['all']} units" in part and f"{u['scored']} are scored" in part, rnd
        else:
            assert u == public["r1"]["units"] and "The same readings and units" in part
        assert f"{a['same']} of {a['pairs']} lines" in part, rnd
        assert f"kappa {a['kappa']:.2f}" in part or f"is {a['kappa']:.2f}" in part, rnd
        d = f["decoys_measure"]
        assert d["1"]["clean_units"] == d["2"]["clean_units"] and f"{d['1']['clean_units']} clean decoy units" in part, rnd
        assert f["bars"]["decoys_accepted"] is True
    # what each section says of its bars
    assert public["r1"]["bars"]["kappa"] is False and "The agreement's bar is missed" in page
    assert public["r1b"]["bars"]["kappa"] is True and public["r1b"]["carried"] == "panel" and "the panel is carried on" in page
    h = public["held"]
    assert h["bars"] == {"kappa": True, "decoys_accepted": True}
    assert h["decoys_measure"]["1"]["accepted"] == h["decoys_measure"]["2"]["accepted"] == 1
    assert round(h["lead"]["panel"], 4) >= R.EXPECTED_HELD["panel_lead_bar"]
    held = " ".join(between(page, *SECTIONS["held"]).split())
    one, two = h["unit_by_unit"]["1"], h["unit_by_unit"]["2"]
    assert f"the panel is better on {one['panel']['better']} and {two['panel']['better']} of the {h['units']['scored']} units and worse on {one['panel']['worse']} and {two['panel']['worse']}" in held
    assert f"the translator better on {one['translator']['better']} and {two['translator']['better']}, worse on {one['translator']['worse']} and {two['translator']['worse']}" in held
    assert f"the writer better on {one['writer']['better']} and {two['writer']['better']}, worse on {one['writer']['worse']} and {two['writer']['worse']}" in held
    k, n = h["by_kind"], h["units"]["by_kind"]
    assert f"places ({n['place']} units: glosses {pct(k['place']['glosses'])}, panel {pct(k['place']['panel'])})" in held
    for kind, name in (("other", "other statements"), ("name", "persons in a role"), ("title", "titles"),
                       ("formula", "formulae"), ("relation", "Relations gain least")):
        assert f"{name} ({n[kind]}: {pct(k[kind]['glosses'])} and {pct(k[kind]['panel'])})" in held, kind
    assert set(k["god"].values()) == {1.0} and "the invocations of gods are given by every reading" in held
    m = h["per_text_mean"]
    assert f"glosses {pct(m['glosses'])}, writer {pct(m['writer'])}, translator {pct(m['translator'])}, panel {pct(m['panel'])}" in held
    assert all(d["panel"] >= d["glosses"] for d in h["per_text"].values()) and "at or above the glosses in each of the 13 texts" in held
    # the cost: every figure of section 9 is in the script's TOKENS, and the total is their sum
    cost = " ".join(between(page, "## 9. Cost", "## 10. ").split())
    for key, n in R.TOKENS.items():
        assert f"{n:,}" in cost, key
    assert f"In all {sum(R.TOKENS.values()):,}." in cost
    for rnd in ("r1", "held"):
        total = sum(n for key, n in R.TOKENS.items() if key.startswith(rnd + ":"))
        assert f"{total:,}" in cost, rnd


def pair(c, key):
    """A count of both judges as the pages write it: "6 and 2", or "none" when both are 0."""
    a, b = c["1"].get(key, 0), c["2"].get(key, 0)
    return "none" if a == b == 0 else f"{a} and {b}"


def test_the_page_quotes_the_rest_of_its_counts():
    """The numbers of sections 5, 6 and 8 that are not in their tables: where the judges part, the units outside
    our copy, the gain by kind, the panel against the translator, and the rule's verdict on each judging."""
    public = json.loads(R.PUBLIC.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    r1, r1b, h = public["r1"], public["r1b"], public["held"]
    first, second, held = (" ".join(between(page, *SECTIONS[r]).split()) for r in ("r1", "r1b", "held"))
    # round one, first judging: the bar missed, so nothing is carried; where the judges part
    a = r1["agreement"]
    assert r1["bars"]["kappa"] is False and r1["carried"] is None and "nothing is carried on from this judging" in first
    ga28 = a["per_text"]["GA 28"]
    rest = [x for t, x in a["per_text"].items() if t != "GA 28"]
    assert f"GA28 has {ga28['pairs']} of the {a['pairs']} lines and a kappa of {ga28['kappa']:.2f}" in first
    assert f"the other four texts agree on {sum(x['same'] for x in rest)} of {sum(x['pairs'] for x in rest)} lines" in first
    assert (f"Of the {a['pairs'] - a['same']} lines judged differently, {a['differing_pairs']['given / partly']} are "
            f"given against partly") in first and f"the judges' kappa is {a['kappa_credited_or_not']:.2f}" in first
    assert f"75 are scored ({r1['units']['not_in_copy']} render" in first and r1["units"]["scored"] == 75
    # round one, second judging
    one, two = r1b["unit_by_unit"]["1"], r1b["unit_by_unit"]["2"]
    for name, words in (("panel", "the panel is better on"), ("translator", "the translator better on"),
                        ("writer", "the writer better on")):
        c = {"1": one[name], "2": two[name]}
        assert f"{words} {pair(c, 'better')}" in second and f"worse on {pair(c, 'worse')}" in second, name
    k, n = r1b["by_kind"], r1b["units"]["by_kind"]
    assert f"titles ({n['title']} units: glosses {pct(k['title']['glosses'])}, panel {pct(k['title']['panel'])})" in second
    names = [k["name"][x] for x in ("pilot", "glosses", "writer", "translator", "panel")]
    assert f"On the {n['name']} units that name a person in a role the readings are close ({pct(min(names))} to {pct(max(names))})" in second
    assert r1b["carried"] == "panel" and all(r1b["bars"].values())
    assert (f"{100 * r1b['lead']['panel']:.1f} points over the glosses, with fewer wrong units "
            f"({pct(r1b['wrong']['panel'])} against {pct(r1b['wrong']['glosses'])})") in second
    pt = r1b["panel_against_translator"]
    assert (f"The panel's lead over one translator, {100 * (r1b['score']['panel'] - r1b['score']['translator']):.1f} "
            f"points, rests on few units: unit by unit the panel is better than the translator on {pair(pt, 'better')} of "
            f"the {r1b['units']['scored']} (first and second judge) and worse on {pair(pt, 'worse')}") in second
    assert f"GA28 holds {r1b['units']['per_text']['GA 28']} of the 75 units" in second
    assert f"GA47 scores 0 for every reading ({r1b['units']['per_text']['GA 47']} units" in second
    assert all(x == 0.0 for x in r1b["per_text"]["GA 47"].values())
    # the held texts
    u = h["units"]
    assert (f"{u['open']} are open ({u['open_with_a_translated_part']} of them with a translated part), {u['judged']} "
            f"went to the judges and {u['scored']} are scored ({u['not_in_copy']} render Meroitic that is not in our "
            f"copy, {u['not_in_copy_per_text']['GA 19']} of them in GA19)") in held
    d = h["decoys_measure"]["1"]
    assert f"({100 * d['accepted'] / d['clean_units']:.1f}%; the bar is {100 * R.BARS['decoys_accepted']:.0f}%)" in held
    assert f"The lead on the five tuning texts was {100 * r1b['lead']['panel']:.1f}." in held
    pt = h["panel_against_translator"]
    assert (f"Its lead over the first of its three translators is "
            f"{100 * (h['score']['panel'] - h['score']['translator']):.1f} point, with four agents a text against one: "
            f"unit by unit the panel is better on {pair(pt, 'better')} of the {u['scored']} units (first and second "
            f"judge) and worse on {pair(pt, 'worse')}.") in held
    assert f"gets {100 * h['lead']['writer']:.1f} of the {100 * h['lead']['panel']:.1f} points" in held
    lo, hi = R.EXPECTED_HELD["writer_lead"]
    assert not lo <= h["lead"]["writer"] <= hi and f"a little more than the {100 * lo:.0f} to {100 * hi:.0f} expected" in held
    # the handbook's check, as section 5 gives it
    book = h["handbook"]
    assert (f"The handbook: {book['sourced']} sourced lines; its four checkers") in first
    assert f"confirmed {book['confirmed']}, corrected {book['corrected']}, dropped none" in first
    assert book.get("unsupported", 0) == 0 and book["unchecked"] == 1 and "and one (the opening sentence)" in first


def test_what_is_not_built_is_said_plainly():
    """Step 25 asks for a page per text and for Griffith's own translations as a second rendering; neither is
    built, and every page and summary of the rounds says so."""
    read = lambda name: " ".join((ROOT / name).read_text(encoding="utf-8").split())        # noqa: E731
    page = read("data/discovery/f4_rounds.md")
    parts = {"page, top": between(page, "**Not built yet**", "## 1. "),
             "page, section 8": between(page, "7. **Not done:**", "## 9. "),
             "README": between(read("README.md"), "16. **A translator with a handbook", "## The question"),
             "REPORT": read("REPORT.md")[read("REPORT.md").index("## Day six (2026-11-13)"):],
             "NEXT_STEPS": between(read("NEXT_STEPS.md"), "17. **F4, the rounds", "Next, in this order"),
             "NEXT_STEPS, F4": between(read("NEXT_STEPS.md"), "- **Next in this step now:**", "The order: F1")}
    for name, text in parts.items():
        assert "Griffith's own translations" in text and ("not built" in text.lower() or "not done" in text.lower()
                                                          or "neither is built" in text.lower()), name
        assert "304" in text or "the pages themselves" in text, name
    # the next step follows the rule set before the held texts, and cuts no design to save tokens
    f4 = parts["NEXT_STEPS, F4"]
    assert "built with the panel" in f4 and "several texts to an agent" not in f4
    # what the handbook's compiler and checkers were told is public, as the page says
    for name in ("F4R_handbook_compile.md", "F4R_handbook_check.md"):
        text = (ROOT / "runs" / "prompts" / name).read_text(encoding="utf-8")
        assert "Do NOT open anything under `data/sources/jssea`" in text, name


def test_the_readme_counts_the_rounds_among_the_local_commands():
    """The README's list of what needs local files names the rounds' script, and its count of the list is right."""
    words = ("Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty", "Twenty-one",
             "Twenty-two", "Twenty-three")
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    head = next(l for l in text.splitlines() if l.endswith("things need files that are kept locally (Data, above), so "
                                                           "they don't run from a clone:"))
    items = [l for l in between(text, head, "## Layout").splitlines() if l.startswith("- `python3 -I ")]
    assert any(l.startswith("- `python3 -I src/f4r.py ") for l in items)
    assert head.split()[0] == words[len(items) - 11], (head, len(items))


def test_the_summaries_quote_the_figures():
    """README, REPORT and NEXT_STEPS say of the rounds what the figures file says."""
    public = json.loads(R.PUBLIC.read_text(encoding="utf-8"))
    read = lambda name: " ".join((ROOT / name).read_text(encoding="utf-8").split())        # noqa: E731
    parts = {"README": between(read("README.md"), "16. **A translator with a handbook", "## The question"),
             "REPORT": read("REPORT.md")[read("REPORT.md").index("## Day six (2026-11-13)"):],
             "NEXT_STEPS": between(read("NEXT_STEPS.md"), "17. **F4, the rounds", "Next, in this order"),
             "NEXT_STEPS, F4": between(read("NEXT_STEPS.md"), "- **The rounds, 13 November**", "The order: F1")}
    h, b, one = public["held"], public["r1b"], public["r1"]
    score, wrong = h["score"], h["wrong"]
    for name in ("README", "REPORT", "NEXT_STEPS"):
        text = parts[name]
        for n in ("glosses", "writer", "translator", "panel"):
            assert pct(score[n]) in text, (name, n)
        assert f"{pct(wrong['glosses'])}, {pct(wrong['writer'])}, {pct(wrong['translator'])} and {pct(wrong['panel'])}" in text, name
        assert f"{h['units']['scored']} units" in text and f"kappa {h['agreement']['kappa']:.2f}" in text, name
        d = h["decoys_measure"]["1"]
        assert f"{d['accepted']} of {d['clean_units']} clean decoy units" in text, name
        assert f"{100 * h['lead']['panel']:.1f} points" in text, name
    for name in ("README", "REPORT"):
        text = parts[name]
        assert f"kappa {one['agreement']['kappa']:.2f}" in text or f"kappa was {one['agreement']['kappa']:.2f}" in text, name
        assert f"kappa {b['agreement']['kappa']:.2f}" in text, name
        assert f"{100 * h['lead']['writer']:.1f} of the {100 * h['lead']['panel']:.1f} points" in text, name
    # the headline gives each number to its own reading
    assert (f"also on texts it was not tuned on: {pct(score['translator'])} of a scholar's units of meaning against "
            f"{pct(score['glosses'])}, and a panel of three with an editor {pct(score['panel'])}") in parts["README"]
    report = parts["REPORT"]
    for n in ("glosses", "pilot", "writer", "translator", "panel"):
        assert f"{n} {pct(b['score'][n])}" in report, n
    pt = h["panel_against_translator"]
    assert (f"The panel leads one translator by {100 * (score['panel'] - score['translator']):.1f} point: unit by unit "
            f"it is better on {pair(pt, 'better')} of the {h['units']['scored']} units and worse on "
            f"{pair(pt, 'worse')}") in report
    c = json.loads(json.dumps(R.TOKENS))
    total = sum(c.values())
    assert f"{total:,} subagent tokens" in report and f"{total:,}" in parts["NEXT_STEPS, F4"]
    for key in ("all:splitters", "all:handbook", "all:handbook_check", "r1b:judges"):
        assert f"{c[key]:,}" in report, key
    for rnd in ("r1", "held"):
        assert f"{sum(n for k, n in c.items() if k.startswith(rnd + ':')):,}" in report, rnd
    f4 = parts["NEXT_STEPS, F4"]
    for n in ("glosses", "writer", "translator", "panel"):
        assert pct(score[n]) in f4, n
    book = public["held"]["handbook"]
    assert f"{book['sourced']} lines with a source" in report and f"{book['confirmed']} confirmed, {book['corrected']} corrected" in report
    assert book.get("unsupported", 0) == 0 and "none dropped" in report and f"{book['unchecked']} outside their ranges" in report


if __name__ == "__main__":
    run([(name, fn) for name, fn in globals().items() if name.startswith("test_")])
