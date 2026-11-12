"""Checks for corpus_v6: one row per inscription (src/v6/).

  python3 -I tests/test_corpus_v6.py

Otten's files, the Newsletter texts, the editions' text layers and corpus_v5 are local only, so the checks of the
method run on made-up lines and readings; the checks of the published table, map and page read the public files,
and compare them with the local ones where those are present.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src" / "v6"), str(ROOT / "src" / "experts"), str(ROOT / "src"), str(ROOT / "tests")]

import build as B       # noqa: E402
import coverage as C    # noqa: E402
import otten as O       # noqa: E402
import packs as K       # noqa: E402
import public as U      # noqa: E402
import readings as R    # noqa: E402
import recount as N     # noqa: E402
from local_only import needs, run   # noqa: E402

LOCAL = ("data/otten/Data/MilletExamples.txt", "data/corpus_v5.jsonl", "data/name_pools.json",
         "data/sources/mnl/mnl_texts.jsonl", "data/sources/jssea-text/pages.txt", "data/sources/fhn-text/pages.txt")
BUILT = ("data/sources/v6/inscriptions.jsonl", "data/sources/v6/map.jsonl", "data/sources/v6/figures.json",
         "data/corpus_v6.jsonl", "data/corpus_v5.jsonl")


# --- src/v6/otten.py ---
def line(n, mero, tag="", file="MilletExamples.txt", page="10"):
    return {"key": f"{file}:{n}", "file": file, "line": n, "page": page, "section": "", "mero": mero,
            "translation": "", "tag": tag}


def test_key_and_spellings():
    assert O.key("wESi : SEr[eyi] qE-wi (EITHER-A-OR-B)") == "wESiSEreyiqEwi"
    assert O.spellings(line(1, "amEd;mEd")) == ["amEd", "mEd"]
    assert O.spellings(line(1, "amEd; : ")) == ["amEd"]                 # a spelling without a letter is none


def test_to_corpus():
    assert O.to_corpus("wESi : SEr[eyi] : q]E") == "woSi Soreyi qo"         # dividers, brackets, E
    assert O.to_corpus("t-dxe mlEqErebr qEre-s-l") == "tdxe mloqorebr qoresl"   # an editor's hyphens join
    assert O.to_corpus("pte.Eye : SSe r....s") == "pte.oye SSe r....s"       # a lost sign stays in its word
    assert O.to_corpus("a [...] [....] b") == "a ... b"                     # two gaps in a row are one
    assert O.to_corpus("qERis : aTe") == "qoris ate"                        # capitals of doubt are lowered
    assert O.to_corpus("amEd;mEd") == "amod"                                # the first of several spellings
    assert O.to_corpus("wos-i : sorey-i : mlomrse", rilly=True) == "woSi Soreyi mlomrs"
    assert O.to_corpus("xbxne : sem", rilly=True) == "xbxN sm"


def test_derive():
    lines = [line(1, "wESi : SEreyi : qE : aplXye qEwi : tedxelEwi"), line(2, "kiSri menEtel"),
             line(3, "pelmES atE-li-s")]
    raws = ["wESi SEreyi qE aplXye qEwi tedxelEwi",            # equal
            "wESi SEreyi qE pqebete qEwi tedxelEwi",           # one name swapped
            "wESi SEreyi qE msxte trEbit qEwi tedxelEwi",      # ... for a name of two words
            "kiSri amxye",                                     # swapped at the end
            "wESi SEreyi qE aplXye qEwi tedxelEwy",            # a second small difference: no swap, but near
            "something else entirely here"]
    d = O.derive(raws, lines)
    assert d[raws[0]] == ("MilletExamples.txt:1", "equal", "", "", 1.0)
    # the stretch is what differs: letters the two names share at their ends stay outside it (aplXy-e, pqebet-e)
    assert d[raws[1]][:4] == ("MilletExamples.txt:1", "swap", "aplXy", "pqebet")
    assert d[raws[2]][:4] == ("MilletExamples.txt:1", "swap", "aplXye", "msxtetrEbit")
    assert d[raws[3]][:4] == ("MilletExamples.txt:2", "swap", "menEtel", "amxye")
    assert d[raws[4]][:4] == ("MilletExamples.txt:1", "swap", "i", "y")       # one letter typed otherwise
    assert raws[5] not in d
    two = "wESi SEreyi qE pqebete qEwi tedxelEwy and more words after it"       # two differences, far apart
    assert O.derive([two], lines).get(two, ("", ""))[1] in ("", "near")
    long = "x" * 30
    assert f"kiSri {long}" not in O.derive([f"kiSri {long}"], lines)      # a "name" of 30 letters is no swap


def test_trace_and_sources():
    private, royal = {"aplXye", "pqebete"}, {"mXeye"}
    assert O.v5_text("wESi SEreyi qE aplXye qEwi", private, royal) == "woSi Soreyi qo NAME qowi"
    assert O.v5_text("tdxe mXeye qEret pqebete", private, royal) == "tdxe RNAME qoret NAME"
    rows = [{"id": "T0001", "src": "funerary", "text": "woSi Soreyi qo NAME qowi"},
            {"id": "T0002", "src": "funerary", "text": "woSi Soreyi qo NAME mete qowi"},   # clean_v2 masks msxte trobit
            {"id": "x", "src": "narrative", "text": "woSi Soreyi qo NAME qowi"}]
    raws = ["wESi SEreyi qE aplXye qEwi", "wESi SEreyi qE pqebete qEwi", "wESi SEreyi qE msxte trEbit mete qEwi", "other"]
    traced = O.trace(rows, raws, private, royal)
    assert traced == {"T0001": raws[:2], "T0002": [raws[2]]}             # a narrative row is not a text of the older corpus
    derived = O.derive(raws, [line(1, "wESi : SEreyi : qE : aplXye qEwi")])
    src = O.sources_of(traced, derived)
    assert src["T0001"] == [("MilletExamples.txt:1", 2, 1)] and src["T0002"] == [("MilletExamples.txt:1", 1, 0)]


def test_name_words():
    text = "woSi Soreyi qo pte.oye qowi tNlxe aror terikelowi aplXye tedxelowi"
    assert O.name_words(text, ["pte.Eye", "tNlxe arEr", "aplXye", "zzz"]) == [3, 5, 6, 8]
    assert O.name_words(text, []) == []
    assert O.name_words("a b", ["a-b"]) == [0, 1]                           # a name written apart in the text
    # a lost sign inside a name is a sign: "li...ye" is not the two words "li ye", nor "are.ke" the name "areke"
    assert O.name_words("mrebqo Slotey li ye tmdelowi", ["li...ye (?)"]) == []
    assert O.name_words("ati.ye tewisti are.ke Xdil", ["areke", "Xdil"]) == [3]
    assert O.name_words("ames 1 a..kye qoleb", ["a ... kye"]) == [2]        # the same broken name
    assert O.name_words("...........amSxiye wi", ["amSxiye"]) == [0]       # lost signs before it: the name
    assert O.spelled("li ... ye") == "li.ye" and O.spelled("..tni...") == "tni"


def test_source_lines_and_their_notes():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / "MilletExamples.txt").write_text(
            "# pg. 254/255\ntdxe : qE ret l\tthe gloss\n# same as line above, but with segmentation\n"
            "t-dxe qEre-s-l l\n\n# pg. 256\nwES\n")
        lines = O.source_lines(pathlib.Path(d), ("MilletExamples.txt",))
    assert [(l["line"], l["page"], l["note"]) for l in lines] == [
        (2, "254/255", ""), (4, "254/255", "same as line above, but with segmentation"), (7, "256", "")]
    assert [O.is_analysis(l) for l in lines] == [False, True, False] and lines[0]["translation"] == "the gloss"
    rows = R.otten_rows(lines)
    assert [r["analysis"] for r in rows] == [False, True, False] and "not a reading of the stone" in rows[1]["ref"]
    assert O.label(lines[2]) == "Millet 1968 p. 256 (MilletExamples.txt line 7)"
    assert O.label(dict(lines[2], file="RillyExamples.txt", page="")) == "Rilly 2007 p. ? (RillyExamples.txt line 7)"


# --- src/v6/readings.py ---
def reading(key, text, family="otten", **more):
    r = {"key": key, "family": family, "work": more.pop("work", "Millet 1968"), "ref": "", "number": "", "numbers": {},
         "site": "", "object": "", "text": text, "whole": None, **more}
    return R.finish(r)


A = "woSi Soreyi qo tmeyeqowi adilxeyye terikelowi ameqemeteye tedxelowi pesto akiNtelo womnisl mdetowi"
B_ = "woSi Soreyi qo pXomeqowi brtoye terikelowi kditrye tedxelowi apote aromelis yetmdelowi xrpxN pXrstelo"


def test_rule():
    a, b = R.reduced(A), R.reduced(B_)
    assert R.rule(a, a)[0] == "sure" and R.rule(a, a)[1:3] == (1.0, 1.0)
    part = R.reduced("adilxeyye terikelowi ameqemeteye tedxelowi")
    v, sa, sb, n = R.rule(part, a)
    assert v == "sure" and sa == 1.0 and sb < 0.6 and n >= R.SHARED         # a part of a text is a sure match to it
    assert R.rule(a, b)[0] == ""                                             # two epitaphs of other people
    skip = R.runs(R.reduced("woSi Soreyi qo")) | R.runs(R.reduced("terikelowi")) | R.runs(R.reduced("tedxelowi"))
    assert R.rule(a, b, skip)[3] < R.rule(a, b)[3]                           # formula runs are left out of the count
    few = R.reduced("tmeyeqowi")                                             # five runs: all shared, under the floor
    assert R.rule(few, a)[0] == "" and R.rule(few, a, floor=1)[0] == "doubtful"
    seven = R.reduced("ameqemeteye")                                         # at the floor, under SHARED: doubtful
    assert R.rule(seven, a)[0] == "doubtful"
    assert R.rule("", a) == ("", 0.0, 0.0, 0)


def test_matches_and_stands_in():
    pool = [reading("ed:1", A, "griffith"), reading("ed:2", B_, "griffith")]
    x = reading("otten:1", "adilxeyye terikelowi ameqemeteye tedxelowi")
    m = R.matches(x, pool)
    assert m[0][4] == "ed:1" and m[0][0] == "sure" and all(k[0] != "sure" for k in m[1:])
    assert R.matches(x, pool, top=1) == m[:1] and all(k[4] != "ed:1" for k in R.matches(pool[0], pool))   # never itself
    assert R.stands_in(x, pool) == ["ed:1"]
    assert R.stands_in(reading("otten:2", "qo"), pool) == []                 # too short to say anything
    assert R.rem_of("0091a") == "0091a" and R.rem_of("") == "" and R.rem_of(None) == "" and R.rem_of("1254B-8") == "1254B-8"
    assert R.reduced("NAME woSi 12 RNAME smlo") == "wosisemlo"               # masks and numerals drop out


def test_formulae():
    eds = [reading(f"e{i}", "woSi Soreyi " + w, "griffith") for i, w in enumerate("abcdefgh")]
    assert R.runs("wosis") <= R.formulae(eds, common=8) and not R.formulae(eds, common=9)


def test_newsletter_rows_keep_two_printings_apart():
    import tempfile
    row = lambda page, same="": {"id": "REM 1154", "rem": "1154", "source": "Meroitic Newsletter 21 (1980)",
                                 "file": "MeroNews21", "pdf_page": int(page) - 1, "printed_page": page, "site": "Kerma",
                                 "object": "offering table", "text_corpus": "woSi Soreyi tbteli", "complete": "whole",
                                 "kind": "print", "same_as": same, "in_corpus": ""}
    printout = dict(row("5"), id="REM 1001", rem="1001", file="MeroNews6", printed_page="", kind="printout",
                    in_corpus="Millet's examples, line 629")
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "mnl.jsonl"
        p.write_text("".join(json.dumps(r) + "\n" for r in
                             (row("7"), row("17", "REM 1154 (Meroitic Newsletter 21 (1980))"), printout)))
        rs = R.mnl_rows(p)
    assert [r["key"] for r in rs] == ["mnl:REM 1154|MeroNews21|p. 7", "mnl:REM 1154|MeroNews21|p. 17", "mnl:REM 1001|MeroNews6"]
    assert [r["ref"] for r in rs] == ["p. 7", "p. 17", "PDF p. 4"]          # the printout has no printed page
    assert R.unique(rs) == rs
    try:
        R.unique(rs + rs[:1])
        raise AssertionError("a key that stands twice must stop the build")
    except SystemExit as e:
        assert "REM 1154" in str(e)
    eds = [R.finish(r) for r in rs]
    g, why = B.by_number(eds)                                                  # the second printing: one inscription
    assert g.find(rs[0]["key"]) == g.find(rs[1]["key"]) != g.find(rs[2]["key"])
    pairs = R.known_pairs(eds, [], [], {})
    assert ("Newsletter second edition", rs[1]["key"], rs[0]["key"]) in pairs
    assert ("Newsletter row in the corpus", rs[2]["key"], "otten:MilletExamples.txt:629") in pairs


FHN_267 = """267 Philae, Meroitic Chamber. The inscriptions of a Meroitic embassy.
Griffith 1912, 34 ff. REM 0097-0111.
Introduction to source
Some words.
Texts
PROCESSION I
REM 0097 (a)
(1)qo pelmos (2)atolise
REM0104 (g)
(1)qo Apmlo qo
1025
Fontes Historiae Nubiorum III
REM 0109(1)
(1)qo Ms(2)trqoye 10
Comtnents
The rooms behind the colonnade.
"""


def test_an_entry_on_several_inscriptions_gives_a_witness_for_each():
    parts = R.fhn_parts([("267", FHN_267), ("246", "246 Meroe. Text\nText\n(1)abc\nComments\n")])
    assert [(r["key"], r["ref"], r["numbers"]) for r in parts] == [
        ("fhn:267:0097", "no. 267 (a)", {"fhn": ["267"], "rem": ["0097"]}),
        ("fhn:267:0104", "no. 267 (g)", {"fhn": ["267"], "rem": ["0104"]}),
        ("fhn:267:0109", "no. 267 (1)", {"fhn": ["267"], "rem": ["0109"]})]
    assert [r["letters"] for r in parts] == ["qopelmosatolise", "qoapmloqo", "qomstrqoye"]   # page lines left out
    assert all(r["witness"] and r["text"] is None and r["site"] == "Philae, Meroitic Chamber" for r in parts)
    assert R.fhn_parts([("246", "246 Meroe.\nText\n(1)abc\nComments\n")]) == []      # one text: fhn_rows reads it


# --- src/v6/build.py ---
def test_kind():
    assert B.kind_of(["a wall"], "woSi Soreyi qo tmeye")[0] == "funerary"       # the invocation decides first
    assert B.kind_of([""], "woS wetNyiNqeli Sori wetrri")[0] == "funerary"
    assert B.kind_of(["ostracon"], "tmedoyi wteli pke liyiroXe towi")[0] == "oracular decree"
    assert B.kind_of(["ostracon (Arminna)"], "abc def")[0].startswith("document")
    assert B.kind_of(["graffito on the pylon"], "abc")[0] == "graffito"
    assert B.kind_of(["sandstone offering table"], "abc")[0] == "funerary"
    assert B.kind_of(["cartouche on the wall"], "abc")[0].startswith("royal or temple")
    assert B.kind_of(["sandstone stela"], "abc")[0] == "funerary"
    assert B.kind_of(["stela of King X"], "abc")[0].startswith("royal or temple")
    assert B.kind_of(["", "not stated"], "abc") == ("not known", "")
    assert B.words("a ... b.. …") == ["a", "b.."]


def ed(key, text, family="griffith", **numbers):
    return reading(key, text, family, numbers={k: v if isinstance(v, list) else [v] for k, v in numbers.items()})


def test_groups_by_number():
    eds = [ed("griffith:1", A, rem="0247"), ed("mnl:1", A, "mnl", rem="0247"), ed("griffith:2", A, rem="0289"),
           ed("mnl:2", B_, "mnl", ga="47"), ed("millet2005:GA47", B_, "millet2005", ga="47"),
           ed("mnl:3", B_, "mnl", mnl="Shokan 1")]
    for r in eds:
        r.setdefault("mnl_id", r["key"])
    g, why = B.by_number(eds)
    sets = sorted(sorted(v) for v in g.sets().values())
    assert sets == [["griffith:1", "mnl:1"], ["griffith:2"], ["millet2005:GA47", "mnl:2"], ["mnl:3"]]
    assert len(why) == 2 and "REM 0247" in why[0][2]                         # the same letters, another number: apart
    assert B.name_of([eds[0], eds[1]]) == "REM 0247" and B.name_of([eds[3], eds[4]]) == "GA 47"
    assert B.name_of([eds[5]]) == "Shokan 1" and B.name_of([reading("otten:1", A)]) == ""
    old = dict(ed("mnl:old", A, "mnl", rem="1041"), superseded=True)
    assert B.name_of([old, ed("mnl:new", A, "mnl", rem="1361A")]) == "REM 1361A"
    assert B.name_of([old]) == "REM 1041"


def test_same_as():
    kept = {"key": "mnl:REM 1168|MeroNews27c", "mnl_id": "Shokan 23 verso (F1964/8.148), REM 1168"}
    by = {kept["mnl_id"]: [kept]}
    row = {"key": "mnl:REM 1168|MeroNews22",
           "same_as": "Shokan 23 verso (F1964/8.148), REM 1168 (Meroitic Newsletter 27 (2000))"}
    assert B.same_as_key(row, by) == kept["key"]
    assert B.same_as_key({"key": "x", "same_as": ""}, by) is None
    assert B.same_as_key({"key": "x", "same_as": "REM 9 (Meroitic Newsletter 27 (2000))"}, by) is None


def test_prefer():
    otten = reading("otten:1", A)
    griffith = reading("griffith:1", A, "griffith", work="Meroitic Inscriptions II (Griffith 1912)")
    mnl = reading("mnl:1", A, "mnl", work="Meroitic Newsletter 28 (2001)")
    printout = reading("mnl:2", A, "mnl", work="Meroitic Newsletter 6 (1971)", printout=True)
    layer = reading("millet2005:1", None, "millet2005", letters=R.reduced(A))
    best, parts, open_ = B.prefer([mnl, griffith, otten, printout, layer])
    assert best is otten and parts == [] and open_ is griffith               # Otten's line first, the open one beside
    assert B.prefer([mnl, griffith, printout])[0] is griffith and B.prefer([printout, mnl])[0] is mnl
    assert B.prefer([layer]) == (None, [], None)                              # a text layer is not a reading to prefer
    short = reading("otten:2", "woSi Soreyi qo tmeyeqowi")                   # a part does not beat the whole text
    assert B.prefer([short, griffith])[0] is griffith
    partial = reading("griffith:2", A, "griffith", whole=False)
    assert B.prefer([partial, mnl])[0] is mnl and B.prefer([partial])[0] is partial
    recon = reading("mnl:3", A + " " + B_, "mnl", reconstruction=True)
    assert B.prefer([recon, mnl])[0] is mnl
    old = reading("mnl:4", A + " " + B_, "mnl", superseded=True)
    assert B.prefer([old, mnl])[0] is mnl and B.prefer([old])[0] is old
    analysed = reading("otten:9", A + " " + B_, analysis=True)              # longer, but Millet's analysis of a line
    assert B.prefer([analysed, otten, griffith])[0] is otten and B.prefer([analysed]) == (None, [], None)
    front, back = reading("mnl:front", "abrtoye kelw amnitore", "mnl"), reading("mnl:back", "qorpiX mdewi yotoli", "mnl")
    best, parts, _ = B.prefer([back, front])                                 # two sides that share nothing: two parts
    assert {best["key"]} | {p["key"] for p in parts} == {"mnl:front", "mnl:back"} and len(parts) == 1
    assert B.apart(front, back) and not B.apart(mnl, otten) and not B.apart(mnl, short)
    assert not B.apart(mnl, reading("mnl:b", B_, "mnl"))                     # two texts that share a formula are not parts
    assert B.year(griffith) == 1912 and B.year(mnl) == 2001 and B.year(otten) == 1968
    assert B.year(reading("otten:n", A, work="Otten's file X.txt")) == 0


def test_numerals():
    text = "pesto abdkror l pesto Nkebtror l pesto mlabN ye l pesto drtoye l qore s l"
    later = "pestoabdkror 1 pesto Nkebtror 1 pestomlabye 1"
    fixed, what = B.numerals(text, [later])
    # the list goes on: an l before "pesto" follows the confirmed ones; an l before another word is left
    assert fixed == "pesto abdkror 1 pesto Nkebtror 1 pesto mlabN ye 1 pesto drtoye l qore s l"
    assert [w[3] for w in what] == [B.ANOTHER, B.ANOTHER, "by analogy"]
    # the letters before the l are read across a short word ("tebwetel xe l"), and any other edition may show
    # the numeral, an older one too (Otten typed the numeral 1 as l); here Griffith's REM 0101, with l for 1
    rem101 = "arite wil l woS pilqetel xe l woS tebwetel xe l tdbto"
    griffith = "arite wil 1 woS pilqetel xe 1 woS tebwetel xe 1 tdbto 2"
    assert B.numerals(rem101, [griffith])[0] == "arite wil 1 woS pilqetel xe 1 woS tebwetel xe 1 tdbto"
    # two other editions that disagree: one with the letter l keeps it, two numerals that differ settle nothing
    assert B.numerals(rem101, [griffith, "arite wil l woS 2"])[0].startswith("arite wil l woS")
    assert B.numerals("ab aritewil l", ["aritewil 1 x", "aritewil 2 y"]) == ("ab aritewil l", [])
    one, what = B.numerals("pesto abdkror l pesto mlabN ye l pesto", [later])    # one confirmed: no analogy
    assert one == "pesto abdkror 1 pesto mlabN ye l pesto" and len(what) == 1
    kept, what = B.numerals(text, [later + " pestodrtoyel"])                 # the later edition keeps a letter l
    assert "mlabN ye l pesto drtoye l" in kept and len(what) == 2
    assert B.numerals(text, ["pesto abdkror pesto"]) == (text, [])           # no numeral in the other reading
    assert B.numerals("abcd 12 l", ["abcd 12 1"]) == ("abcd 12 l", [])        # an l after a numeral is left
    assert B.stream("pesto 12 smlo") == "peseto12semlo"                         # the reduced spelling writes se


def cand(verdict, sa, sb, n, key, group, ratio=0.1):
    return (verdict, sa, sb, n, key, group, ratio)


def test_decide():
    long = reading("otten:1", A)
    short = reading("otten:2", "tmeyeqowi adilxeyye terikelowi")
    sure = cand("sure", 0.9, 0.8, 40, "ed:1", "g1")
    assert B.decide(long, [sure], [])[:2] == ("reading", "g1")
    assert B.decide(long, [cand("sure", 0.9, 0.1, 40, "ed:1", "g1")], [])[:2] == ("phrase", "g1")
    assert B.decide(long, [cand("sure", 0.9, 0.1, 40, "ed:1", "g1", 0.6)], [])[0] == "reading"   # half as long: a reading
    rival = cand("doubtful", 0.5, 0.3, 30, "ed:2", "g2")
    assert B.decide(long, [sure, rival], [])[0] == "pending"                  # a second inscription close behind
    assert B.decide(long, [sure, cand("doubtful", 0.3, 0.1, 10, "ed:2", "g2")], [])[0] == "reading"
    assert B.decide(long, [sure, cand("doubtful", 0.5, 0.3, 30, "ed:1b", "g1")], [])[0] == "reading"   # the same inscription
    assert B.decide(short, [], ["g1"])[:2] == ("phrase", "g1") and B.decide(short, [], ["g1", "g2"])[:2] == ("phrase", None)
    assert B.decide(short, [], []) == ("", None, None, "")
    doubt = cand("doubtful", 0.5, 0.05, 8, "ed:1", "g1")
    assert B.decide(long, [doubt], [])[0] == "pending"                        # a long line without a home: a reader
    assert B.decide(short, [doubt], [])[0] == "phrase"                        # a phrase whichever text it is from
    assert B.decide(short, [doubt], [])[3].startswith("a doubtful match that was not read")
    rivals = [cand("sure", 0.9, 0.8, 40, "ed:1", "g1"), cand("doubtful", 0.5, 0.3, 30, "ed:2", "g2")]
    assert B.decide(reading("otten:4", "tmeye"), rivals, [])[:2] == ("phrase", None)        # too short to read
    assert B.decide(reading("otten:4", "tmeye"), rivals, [])[3].startswith("a sure match with a second inscription")
    assert B.decide(short, [cand("doubtful", 0.5, 0.4, 8, "ed:1", "g1")], [])[0] == "pending"   # it may be a reading
    tiny = reading("otten:3", "tmeyeqowi")
    assert B.decide(tiny, [cand("doubtful", 0.5, 0.4, 8, "ed:1", "g1")], [])[0] == "phrase"     # too short to read
    held = cand("", 0.2, 0.2, 3, "ed:9", "g9")
    assert B.decide(short, [sure], [], held)[:2] == ("reading", "g9") and B.decide(short, [], [], held)[3] == B.HELD_BY
    loose = [cand("", 0.2, 0.4, 4, "ed:5", "g5")]
    assert B.decide(long, [], [], None, loose)[0] == "pending" and B.decide(short, [], [], None, loose)[0] == ""
    assert B.is_reading(sure) and not B.is_reading(doubt)


def test_settle():
    group = {"ed:1": "g1", "ed:2": "g2"}.get
    c1, c2 = cand("doubtful", 0.5, 0.4, 8, "ed:1", "g1"), cand("doubtful", 0.4, 0.3, 7, "ed:2", "g2")
    pending = ("pending", None, c1, "")
    assert B.settle(pending, [c1, c2], None, group) == pending                # the readers have not settled it
    assert B.settle(pending, [c1, c2], ("ed:2", False), group) == ("reading", "g2", c2, B.READ)
    assert B.settle(pending, [c1, c2], ("ed:2", True), group) == ("phrase", "g2", c2, B.READ)
    assert B.settle(pending, [c1, c2], ("", False), group) == ("", None, None, B.READ_NONE)
    assert B.settle(pending, [c1], ("ed:2", False), group) == ("reading", "g2", None, B.READ)   # a filler they named
    sure = ("reading", "g1", c1, "the rule: a sure match to one inscription")
    assert B.settle(sure, [c1], ("ed:2", False), group) == sure               # only a pending decision is theirs


def test_candidates_one_per_inscription():
    eds = [reading("ed:1", A, "griffith"), reading("ed:1b", A, "mnl"), reading("ed:2", B_, "griffith"),
           reading("ed:r", A, "mnl", reconstruction=True)]
    group = {"ed:1": "g1", "ed:1b": "g1", "ed:2": "g2", "ed:r": "g3"}.get
    c = B.candidates(reading("otten:1", A), eds, group, frozenset())
    assert [x[5] for x in c] == ["g1"] and c[0][6] == 1.0                    # one per inscription, no reconstruction


def test_read_verdicts(tmp=None):
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "verdicts.jsonl"
        assert B.read_verdicts(p) == {}
        p.write_text('{"line": "otten:1", "same_as": "ed:1", "part": true}\n\n{"line": "otten:2", "same_as": ""}\n')
        assert B.read_verdicts(p) == {"otten:1": ("ed:1", True), "otten:2": ("", False)}


# --- src/v6/packs.py ---
KEY = {"I01": {"line": "otten:1", "kind": "known", "candidates": {"A": "ed:1", "B": "ed:2"}, "right": "B"},
       "I02": {"line": "otten:2", "kind": "decoy", "candidates": {"A": "ed:3"}, "right": "none"},
       "I03": {"line": "otten:3", "kind": "pending", "candidates": {"A": "ed:4", "B": "ed:5"}, "right": None},
       "I04": {"line": "otten:4", "kind": "pending", "candidates": {"A": "ed:6"}, "right": None},
       "I05": {"line": "otten:5", "kind": "pending", "candidates": {"A": "ed:7"}, "right": None}}


def test_readers():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "reader1.jsonl"
        p.write_text('{"item": "I01", "same_as": "B", "part": false}\nnot json\n{"item": "I01", "same_as": "A"}\n'
                     '{"item": "I03", "same_as": "C"}\n{"item": "I09", "same_as": "A"}\n{"item": "I02", "same_as": "none", "part": "yes"}\n')
        got, problems = K.load_answers(p, KEY)
        assert got == {"I01": {"same_as": "B", "part": False, "sure": 0}, "I02": {"same_as": "none", "part": False, "sure": 0}}
        assert len(problems) == 4 + 3                                          # four bad lines, three items unanswered
        assert K.load_answers(pathlib.Path(d) / "none.jsonl", KEY)[1] == ["no file none.jsonl"]
    one = {"I01": {"same_as": "B", "part": False, "sure": 5}, "I02": {"same_as": "none", "part": False, "sure": 5},
           "I03": {"same_as": "A", "part": False, "sure": 4}, "I04": {"same_as": "none", "part": False, "sure": 3},
           "I05": {"same_as": "A", "part": False, "sure": 5}}
    two = dict(one, I03={"same_as": "A", "part": True, "sure": 3}, I05={"same_as": "none", "part": False, "sure": 5})
    t = K.trust(one, KEY)
    assert (t["right"], t["none"], t["passes"]) == (1, 1, True)
    assert not K.trust(dict(one, I01={"same_as": "A", "part": False, "sure": 5}), KEY)["passes"]
    assert not K.trust({}, KEY)["passes"]
    v = K.verdicts(one, two, KEY)
    assert v == [{"line": "otten:3", "same_as": "ed:4", "part": True},        # a part for either reader is a part
                 {"line": "otten:4", "same_as": "", "part": False}]           # the readers differ on I05: not settled
    unsure = dict(two, I03={"same_as": "A", "part": True, "sure": 2})         # the same answer, one of them a guess
    assert [x["line"] for x in K.verdicts(one, unsure, KEY)] == ["otten:4"]
    assert len(K.verdicts(one, unsure, KEY, min_sure=0)) == 2
    assert K.verdicts(one, {}, KEY) == []


# --- src/v6/recount.py and the rows src/coverage.py takes ---
def test_align_and_rows():
    old = "woSi Soreyi qo NAME qowi mokelowi pesto l".split()
    new = "woSi Soreyi qo tmeye qowi pesto 1".split()
    places = N.align(old, new)
    assert places == {0: 0, 1: 1, 2: 2, 4: 4, 6: 5}
    assert N.unmatched("NAME", 3, places, new).endswith("spelled otherwise in the preferred reading")
    assert N.unmatched("mokelowi", 5, places, new).endswith("not in the preferred reading")
    split = "So ri qetrri qo".split()
    joined = "Soriqetrri qo".split()
    assert N.unmatched("ri", 1, N.align(split, joined), joined).endswith("a part of a longer word in the preferred reading")
    rows = N.rows_for_map([{"id": "REM 0247", "reading": "karanog:G-karanog-47", "text": "a b", "names": [1], "v5": ["G-karanog-47"]},
                           {"id": "GA 28", "reading": "otten:MilletExamples.txt:433", "text": "c", "names": [], "v5": []}])
    assert rows[0]["karanog"] == "G-karanog-47" and rows[0]["group"] == N.GROUPS["karanog"] and "karanog" not in rows[1]
    assert C.group(rows[1]) == N.GROUPS["otten"] and C.group({"id": "G-karanog-1"}).startswith("Karanog")
    assert C.group({"id": "T0001"}) == "the older corpus (names masked)"


def test_names_in_the_map():
    words, affixes, _ = C.index([C.entry({"headword": "qo", "variants": [], "category": "démonstratif", "meaning_en": "this one",
                                          "status": "established", "page_pdf": 10, "page_printed": 8})])
    glossed = C.gloss_texts([{"id": "GA 1", "text": "qo tmeye 12 pte.oye", "names": [1, 2, 3], "group": "g"}], words, affixes)
    gs = glossed[0][1]
    assert [g["level"] for g in gs][1:] == ["name", "number", "name"]         # a numeral is no name; a broken name is one
    assert gs[0]["level"] in C.TRANSLATED
    assert gs[1]["source"].startswith("a name, as the source") and gs[1]["parts"] == [{"form": "tmeye", "entry": "NAME"}]
    plain = C.gloss_texts([{"id": "GA 1", "text": "qo tmeye"}], words, affixes)[0][1]
    assert plain[1]["level"] == "unknown"                                    # without the mark the word is as before


# --- src/v6/public.py ---
def test_public_row_holds_no_closed_text():
    readings = [{"key": "otten:1", "work": "w", "ref": "r", "number": "", "licence": "none", "open": False, "typed": True,
                 "whole": None, "letters": 10, "words": 2, "site": "s", "object": "o", "text": "secret words", "family": "otten"},
                {"key": "griffith:G-mi2a-97", "work": "w", "ref": "r", "number": "Inscr. 97", "licence": "pd", "open": True,
                 "typed": True, "whole": True, "letters": 10, "words": 2, "site": "Philae", "object": "wall", "text": "open words",
                 "family": "griffith"}]
    i = {"id": "REM 0097", "rem": ["0097"], "numbers": {"rem": ["0097"]}, "site": "Philae", "kind": "graffito", "kind_by": "",
         "preferred": "otten:1", "parts": [], "text": "secret words", "names": [1], "numerals_set": [], "open": "griffith:G-mi2a-97",
         "open_text": "open words", "open_whole": True, "readings": readings}
    row = U.public_row(i, {"REM 0097": ["T0001"]})
    assert "secret" not in json.dumps(row) and row["text"] is None and row["open_text"] == "open words"
    assert row["in_corpus_v6"] and row["v5"] == ["T0001"] and row["words"] == 2 and row["names_marked"] == 1
    assert "text" not in row["readings"][0] and row["readings"][1]["text"] == "open words"
    mine = U.public_row(dict(i, preferred="griffith:G-mi2a-97", text="open words"), {})
    assert mine["text"] == "open words" and not mine["in_corpus_v6"]
    two = U.public_row(dict(i, preferred="griffith:G-mi2a-97", text="open words more", parts=["mnl:x"]), {})
    assert two["text"] is None                                               # a second part may be a closed reading


def test_map_table():
    t = U.map_table([{"id": "T0001", "words": 3, "what": "x", "copy": "", "inscription": None, "reading": "otten:1",
                      "share_of_text": 0.5, "share_of_text_all": 0.75, "against": "ed:1"}])
    head, row = t.splitlines()
    assert head.split("\t") == list(U.MAP_COLUMNS) and row.split("\t")[:6] == ["T0001", "3", "x", "", "", "otten:1"]
    assert len(row.split("\t")) == len(U.MAP_COLUMNS)
    cells = dict(zip(U.MAP_COLUMNS, row.split("\t")))
    assert cells["share of the text's own runs in the other"] == "0.5" and cells["compared with"] == "ed:1"
    assert cells["share of the text's runs in the other (all runs, as src/experts/prepare.py)"] == "0.75"


def test_shares_of_all_runs_are_those_of_prepare():
    a, b = R.reduced(A), R.reduced("adilxeyye terikelowi ameqemeteye tedxelowi")
    sa, sb = B.all_runs(a, b)
    ra, rb = B.P.runs(a), B.P.runs(b)                                          # src/experts/prepare.py, match()
    assert (sa, sb) == (round(len(ra & rb) / len(ra), 3), round(len(ra & rb) / len(rb), 3)) and sb == 1.0 > sa
    assert B.all_runs("", a) == (None, None)


def test_rows_alike_across_and_within_a_numbering():
    rows = [("REM 0219", R.reduced(A)), ("REM 0289", R.reduced(A)), ("Millet 1968 p. 1", R.reduced(A)),
            ("REM 0001", R.reduced(B_))]
    systems = {"REM 0219": {"rem", "karanog"}, "REM 0289": {"rem", "karanog"}, "Millet 1968 p. 1": set(), "REM 0001": {"rem"}}
    same, across = U.alike(rows, systems, frozenset())
    assert same == [("REM 0219", "REM 0289")]                                 # one numbering, two numbers
    assert across == [("REM 0219", "Millet 1968 p. 1", "sure"), ("REM 0289", "Millet 1968 p. 1", "sure")]


def test_why_a_known_pair_was_missed():
    size = {"a": 300, "b": 300, "short": 30, "long": 400}
    s = lambda **k: dict({"verdict": "doubtful", "same_text": False, "shared": 40, "best_key": "long", "b": "b"}, **k)
    assert R.why_missed(s(same_text=True), size) == R.MISSED[0]
    assert R.why_missed(s(verdict="", shared=3, best_key=""), size) == R.MISSED[1]
    assert R.why_missed(s(best_key="short"), size) == R.MISSED[2]
    assert R.why_missed(s(), size) == R.MISSED[3] and R.why_missed(s(verdict="", best_key=""), size) == R.MISSED[4]


def test_editions_of_an_inscription():
    i = {"readings": [{"work": "Meroitic Newsletter 29 (2002)"}, {"work": "Meroitic Newsletter 29 (2002)"}]}
    assert B.editions_of(i) == 1                                               # two fragments in one edition
    assert B.editions_of({"readings": i["readings"] + [{"work": "Fontes Historiae Nubiorum III (1998)"}]}) == 2


# --- the published files ---
def public_table():
    return [json.loads(l) for l in U.TABLE.read_text().splitlines() if l.strip()]


def test_published_table():
    table, figs = public_table(), json.loads(U.FIGURES.read_text())
    ids = [r["id"] for r in table]
    assert len(ids) == len(set(ids)) == figs["inscriptions"]["all"]
    assert sum(r["in_corpus_v6"] for r in table) == figs["corpus_v6"]["texts"] == figs["inscriptions"]["with_a_typed_reading"]
    assert sum(bool(r["rem"]) for r in table) == figs["inscriptions"]["with_a_rem_number"]
    assert sum(B.editions_of(r) >= 2 for r in table) == figs["inscriptions"]["with_readings_from_two_editions_or_more"]
    assert sum(not r["numbers"] for r in table) == figs["inscriptions"]["not_identified"]
    assert sum(bool(r["open_reading"]) for r in table) == figs["inscriptions"]["with_an_open_reading"]
    assert sum(r["words"] for r in table) == figs["corpus_v6"]["words"]
    open_rows = {}
    for folder in ("data/expansion", "data/expansion/karanog"):
        for p in sorted((ROOT / folder).glob("griffith_*.jsonl")):
            for l in p.read_text().splitlines():
                if l.strip():
                    open_rows[" ".join(R.E.words(json.loads(l).get("text_corpus", "")))] = p.name
    for r in table:                                    # a text in the public table is a text of the open rows
        for x in r["readings"]:
            assert ("text" in x) == x["open"], r["id"]
            assert not x["open"] or x["text"] in open_rows, r["id"]
        assert r["text"] is None or (r["preferred_is_open"] and r["text"] in open_rows), r["id"]
        assert r["open_text"] is None or r["open_text"] in open_rows, r["id"]
        assert r["in_corpus_v6"] == (r["words"] > 0), r["id"]


def test_published_map():
    lines = U.MAP.read_text().splitlines()
    figs = json.loads(U.FIGURES.read_text())
    assert lines[0].split("\t") == list(U.MAP_COLUMNS)
    rows = [l.split("\t") for l in lines[1:]]
    assert len(rows) == len({r[0] for r in rows}) == figs["corpus_v5"]["texts"] == 899
    assert sum(int(r[1]) for r in rows) == figs["corpus_v5"]["words"] == 21977
    assert all(r[2] for r in rows)                                           # every text is something
    ids = {r["id"] for r in public_table()}
    assert all(r[4] in ids for r in rows if r[4])                            # ... and its inscription is in the table
    c = figs["corpus_v5"]["classes"]
    assert sum(v["texts"] for v in c.values()) == 899 and sum(v["words"] for v in c.values()) == 21977


def test_page_tables():
    figs = json.loads(U.FIGURES.read_text())
    page = U.PAGE.read_text()
    assert U.BEGIN in page and U.END in page
    assert page[page.index(U.BEGIN):page.index(U.END) + len(U.END)] == U.tables(figs)


# numbers the page's text may state without a count behind them: dates and times, years of editions, REM numbers
# and pages it names, the thresholds of the rule and of the bars, and the numbers of steps and sections
COST = ("<!-- cost: by hand, from the task notifications -->", "<!-- end of the cost -->")
STATED = {"2026-11-12", "12:03", "1968", "2005", "1971", "0001", "2780", "0544", "0101", "362", "370",
          "60%", "30%", "90%", "12", "10", "40", "22", "28", "4.0",       # 4.0: the licence CC BY 4.0
          "16", "489"}                                                    # GA 13+16; MilletExamples.txt line 489


def test_page_text_quotes_the_tables():
    """Every number in the page's text stands in the tables that src/v6/public.py writes (or in STATED). The
    cost of the agent runs is the one part written by hand, between its own marks."""
    import re
    page = U.PAGE.read_text()
    block = page[page.index(U.BEGIN):page.index(U.END)]
    text = page[:page.index(U.BEGIN)] + page[page.index(U.END):]
    assert text.count(COST[0]) == 1 and text.count(COST[1]) == 1
    text = text[:text.index(COST[0])] + text[text.index(COST[1]):]
    text = re.sub(r"```.*?```", " ", text, flags=re.S)                        # the commands
    number = re.compile(r"\d{4}-\d\d-\d\d|\d\d:\d\d|\d[\d,]*(?:\.\d+)?%?")
    tidy = lambda t: t.rstrip(",")
    known = {tidy(t) for t in number.findall(block)} | STATED
    quoted = {tidy(t) for t in number.findall(text)}
    odd = sorted(t for t in quoted if t not in known and not (t.isdigit() and int(t) < 10))
    assert not odd, f"numbers in the text that no table holds: {odd}"


def numbers_not_in_the_tables(text, more=()):
    import re
    page = U.PAGE.read_text()
    number = re.compile(r"\d{4}-\d\d-\d\d|\d\d:\d\d|\d[\d,]*(?:\.\d+)?%?")
    tidy = lambda t: t.rstrip(",")
    known = {tidy(t) for t in number.findall(page[page.index(U.BEGIN):page.index(U.END)])} | STATED | set(more)
    known |= {tidy(t) for t in number.findall(page[page.index(COST[0]):page.index(COST[1])])}     # the cost, by hand
    return sorted(t for t in {tidy(t) for t in number.findall(text)} if t not in known and not (t.isdigit() and int(t) < 10))


def test_readme_report_and_next_steps_quote_the_tables():
    """What README, REPORT and NEXT_STEPS say about corpus_v6 is what the page's tables say."""
    readme = (ROOT / "README.md").read_text()
    item = readme[readme.index("11. **The corpus keyed by inscription"):readme.index("## The question")]
    assert not numbers_not_in_the_tables(item), numbers_not_in_the_tables(item)
    method = readme[readme.index("### 18. One inscription once"):readme.index("## Reproduce")]
    assert not numbers_not_in_the_tables(method, ["18"]), numbers_not_in_the_tables(method, ["18"])
    listed = readme[readme.index("Since 2026-11-12 the readings are also listed"):readme.index("## Methods")]
    assert not numbers_not_in_the_tables(listed), numbers_not_in_the_tables(listed)
    report = (ROOT / "REPORT.md").read_text()
    day = report[report.index("## Day five, afternoon (2026-11-12): one inscription once"):]
    assert not numbers_not_in_the_tables(day), numbers_not_in_the_tables(day)
    steps = (ROOT / "NEXT_STEPS.md").read_text()
    point = steps[steps.index("12. **The corpus keyed by inscription**"):steps.index("Next, in this order")]
    assert not numbers_not_in_the_tables(point), numbers_not_in_the_tables(point)
    status = steps[steps.index("    - **Status, 2026-11-12: built**"):steps.index("23. **F2.")]
    assert not numbers_not_in_the_tables(status), numbers_not_in_the_tables(status)


# --- the local build (skipped without the local files) ---
def test_local_build_is_what_is_published():
    needs(*BUILT)
    local = lambda name: [json.loads(l) for l in (ROOT / "data/sources/v6" / name).read_text().splitlines() if l.strip()]
    ins, mapped = local("inscriptions.jsonl"), local("map.jsonl")
    corpus = [json.loads(l) for l in (ROOT / "data/corpus_v6.jsonl").read_text().splitlines() if l.strip()]
    v5 = [json.loads(l) for l in (ROOT / "data/corpus_v5.jsonl").read_text().splitlines() if l.strip()]
    assert [m["id"] for m in mapped] == [r["id"] for r in v5]                # every text of corpus_v5, once, in order
    assert all(m.get("class") in B.WHAT for m in mapped)
    ids = [c["id"] for c in corpus]
    assert len(ids) == len(set(ids))                                         # no inscription stands twice
    assert not any(w in ("NAME", "RNAME") for c in corpus for w in c["text"].split())     # real names
    assert all(c["text"].split() and all(w.strip(".…") for w in c["text"].split()) for c in corpus)
    assert all(0 <= k < len(c["text"].split()) for c in corpus for k in c["names"])
    stands = [m for m in mapped if m["stands"]]
    assert len({m["inscription"] for m in stands}) == len(stands)            # one corpus_v5 row for an inscription
    assert {m["inscription"] for m in stands} == {c["id"] for c in corpus if c["v5"]}
    in_corpus = {c["id"]: c["v5"] for c in corpus}
    assert [U.public_row(i, in_corpus) for i in ins] == public_table()
    assert U.map_table(mapped) == U.MAP.read_text()
    figs = json.loads(U.FIGURES.read_text())
    mine = json.loads((ROOT / "data/sources/v6/figures.json").read_text())
    assert all(figs[k] == mine[k] for k in mine)
    held = {m["id"]: m for m in mapped}
    for table in B.P.HELD.values():                                          # the pairs read on 2026-11-12 are readings
        for tid in table.values():
            assert held[tid]["class"] == "reading" and held[tid]["inscription"], tid
    keys = [r["key"] for i in ins for r in i["readings"]]
    assert len(keys) == len(set(keys))                                       # every reading once, in one inscription
    assert len([k for k in keys if k.startswith("mnl:REM 1154|")]) == 2      # both printings of Newsletter 21
    for i in ins:
        assert not any(r["key"] == i["preferred"] and "not a reading of the stone" in r["ref"] for r in i["readings"]), i["id"]
        for r in i["readings"]:
            if r["key"].startswith("fhn:267:"):                               # a witness beside its own REM number
                assert r["key"].rsplit(":", 1)[1] in i["rem"], (i["id"], r["key"])


def test_local_rebuild():
    needs(*LOCAL, *BUILT)
    b = B.build()
    mapped = B.map_rows(b)
    corpus = B.corpus_rows(b, mapped)
    saved = [json.loads(l) for l in (ROOT / "data/corpus_v6.jsonl").read_text().splitlines() if l.strip()]
    assert corpus == saved                                                   # the build gives the same corpus again
    assert B.measures(b, mapped, corpus) == json.loads((ROOT / "data/sources/v6/figures.json").read_text())


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)])
