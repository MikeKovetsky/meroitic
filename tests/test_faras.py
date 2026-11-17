"""Checks for the Faras texts of Griffith 1922 as open readings (src/faras.py).

  python3 -I tests/test_faras.py

The readers' files, the rows, the measure and the counts of the comparison are public; the closed readings the
comparison reads are local only, so the check that recomputes it is skipped where the v6 build is absent.
"""
import json, pathlib, random, re, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src" / "v6"), str(ROOT / "src" / "experts"), str(ROOT / "src"), str(ROOT / "tests")]

import faras as F       # noqa: E402
import expand as E      # noqa: E402
import readings as R    # noqa: E402
from local_only import needs, run   # noqa: E402


def rows_file():
    return [json.loads(l) for l in F.ROW.read_text(encoding="utf-8").splitlines() if l.strip()]


def made_up(n, first, final, **more):
    return dict({"text": f"Faras {n}", "pages": ["p603"], "object": "Altar", "first": first, "final": final,
                 "rendering": "", "pack": "T"}, **more)


# --- numbers and the lot ---
def test_numbers():
    assert F.number("Faras 7") == 7 and F.number(" Faras 46 ") == 46
    assert F.number("Kar. 7") is None and F.number("Faras 7a") is None and F.number(None) is None
    assert F.rem(1) == "0501" and F.rem(44) == "0544" and F.rem(46) == "0546"


def test_the_drawn_texts_are_the_lot_of_the_bar():
    assert tuple(sorted(random.Random(F.SEED).sample(range(1, 47), 5))) == F.DRAWN == (2, 10, 13, 14, 15)
    assert "`[2, 10, 13, 14, 15]`" in (F.FARAS / "BAR.md").read_text(encoding="utf-8")


def test_page():
    assert F.page({"pages": ["p603"]}) == "p. 567 (PDF p. 603)"
    assert F.page({"pages": ["p604", "p603"]}) == "pp. 567-568 (PDF pp. 603-604)"
    assert F.page({"pages": []}) == ""
    # each plate and its blank back carry no printed number (the running heads of the PDF's pages: 609 is 571,
    # 619 is 579, 623 is 581, 647 is 599)
    assert F.page({"pages": ["p609"]}) == "p. 571 (PDF p. 609)" and F.page({"pages": ["p619"]}) == "p. 579 (PDF p. 619)"
    assert F.page({"pages": ["p623"]}) == "p. 581 (PDF p. 623)"
    assert F.page({"pages": ["p604", "p607"]}) == "pp. 568-569 (PDF pp. 604-607)"
    assert [F.printed(p) for p in (601, 647, 648)] == [565, 599, 600]       # the article is pp. 565-600
    try:
        F.printed(615)
    except ValueError:
        pass
    else:
        raise AssertionError("a plate has no printed page number")


# --- the measure ---
def test_distance():
    assert F.distance(list("abc"), list("abc")) == 0
    assert F.distance(list("abc"), list("abd")) == 1
    assert F.distance(list("abc"), list("ac")) == 1 and F.distance([], list("ab")) == 2


def test_agreement_counts_signs_not_letters_and_leaves_lost_signs_out():
    # se and te are one sign each; [.] and a restoration are lost signs; (3) and ? are marks
    assert F.bare("(1)wos : se[.]te? [k]") == ["w", "o", "s", "se", "te"]
    assert F.agreement([("wos : asori", "wos : asori")]) == (8, 8)
    assert F.agreement([("wos : asori", "wos : sori")]) == (7, 8)          # a sign only one typing has
    assert F.agreement([("wos", "wosi")]) == (2, 3)                        # counts against, either way
    assert F.agreement([("wo[.]s", "wos")]) == (3, 3)                      # a lost sign is left out
    assert F.agreement([("a", "bcdef")]) == (0, 1)                         # never below nothing


def test_places_are_the_stretches_that_differ():
    assert F.places("wos : ato", "wos : ato") == []
    assert F.places("wos : ato mẖe", "wos : at mḫe") == [("to", "t", "wosa", "mẖe"), ("ẖ", "ḫ", "satom", "e")]       # four signs either side: s a to m


# --- the comparison ---
def test_a_quoted_passage_is_scored_against_its_best_stretch_of_the_text():
    assert F.within("abcdefgh", "cdef") == (4, 4) and F.within("abcdefgh", "cdxf") == (3, 4)
    assert F.within("ab", "abcd") == (2, 4) and F.within("", "ab") == (0, 2) and F.within("ab", "") == (0, 0)
    # folded, x and X and s and S are one letter (fold()); strict, they are two and only word division goes
    assert F.within("woSi SSor lxlowi", "SSor lXlowi") == (9, 9)
    assert F.within("woSi SSor lxlowi", "SSor lXlowi", folded=False) == (9, 10)
    assert F.within("aXrr. amodteli", "aXrrb amodteli", folded=False) == (12, 13)    # a lost sign counts against


# --- the rows ---
def test_formula_pairs_are_the_karanog_rows():
    pairs = {("".join(a), "".join(b)) for a, b in F.formula_pairs()}
    assert len(pairs) == 17 and ("ato", "mẖe") in pairs and ("at", "mẖe") in pairs


def test_rows_from_made_up_readings():
    first = {1: made_up(1, "(1)wos : asori : ḫrpḫñ", "(1)wos : asori : ḫrpḫñ : pẖrs(2)se? : atomẖe [.][.]"),
             2: made_up(2, "wos", "wos : ẖol", kept=[{"copy": "ẖol", "latin": "khêl"}], notes="a note"),
             10: made_up(10, "abe", "abe")}
    second = {2: made_up(2, "wos", "wos : ẖl", pack="X")}
    decided = {2: {"text": "Faras 2", "final": "wos : ẖol", "places": [{"first": "o", "second": ""}]}}
    rows = F.rows(first, second, decided, F.formula_pairs())
    assert [r["rem"] for r in rows] == ["0501", "0502", "0510"] and rows[0]["label"] == "Faras 1"
    r = rows[0]
    assert r["text_corpus"] == "woS aSori xrpxN pXrSs ato mXe .."       # s S, se s, ḫ x, ẖ X, ñ N; formula parted
    assert r["words"] == 6 and r["signs"] == 23 and r["uncertain"] == 1     # to and se are one sign each
    assert r["griffith_no"] is None and r["site"] == "Faras" and r["page"] == "p. 567 (PDF p. 603)"
    assert "1 formula word" in r["notes"] and "0 signs changed" not in r["notes"]
    assert "changed by the check" in r["notes"]
    r2 = rows[1]
    assert r2["text_std"] == "wos : ẖol" and "agree on 5 of 6 signs" in r2["notes"] and "(1 place;" in r2["notes"]
    assert "ẖol (his Latin: khêl)" in r2["notes"] and r2["notes"].endswith("a note")


def test_a_gap_of_the_copy_inside_a_known_word_is_closed():
    """The readers write a space at each gap of the copy; text_corpus closes it where the parts spell a word the other
    Griffith rows hold in three texts or more, never across a divider, longest join first."""
    known = {"Soreyi", "at", "pSoXte", "tedxelowi"}
    words, closed = F.joined(F.K.runs("wosi : so (2) reyi : a(6) t mẖe : p soẖ te"), known)
    assert F.K.spell(words).split() == ["woSi", "Soreyi", "at", "mXe", "pSoXte"] and closed == 4
    words, closed = F.joined(F.K.runs("so : reyi tedḫe lowi"), known)                   # the divider stays
    assert F.K.spell(words).split() == ["So", "reyi", "tedxelowi"] and closed == 1
    first = {24: made_up(24, "wosi", "(1) wosi : so (2) reyi : ato mẖe : p (7) soẖte")}
    r = F.rows(first, {}, {}, F.formula_pairs(), {"Soreyi", "pSoXte"})[0]
    assert r["text_corpus"] == "woSi Soreyi ato mXe pSoXte" and "closes 2 gaps" in r["notes"]
    assert r["text_std"] == "(1) wosi : so (2) reyi : ato mẖe : p (7) soẖte"            # the reading as written
    # three of the other rows write atomẖe, but the pair (ato, mẖe) parts it again: the reader's word end stands, and
    # only the gap inside m ẖe is closed (Faras 29's "ato m (6) ẖe")
    words, closed = F.joined(F.K.runs("ato mẖe : ato m ẖe : at mẖe"), {"atomXe", "atmXe", "mXe"}, F.formula_pairs())
    assert F.K.spell(words).split() == ["ato", "mXe", "ato", "mXe", "at", "mXe"] and closed == 1
    assert F.joined(F.K.runs("ato mẖe"), {"atomXe"})[1] == 1                             # without the pairs it would join
    first = {2: made_up(2, "wosi", "wosi : ato mẖe : at m ẖe")}
    r = F.rows(first, {}, {}, F.formula_pairs(), {"atomXe", "mXe"})[0]
    assert r["text_corpus"] == "woSi ato mXe at mXe" and "closes 1 gap " in r["notes"] and "text_corpus parts" not in r["notes"]


def test_a_numeral_is_a_word_of_its_own_and_a_line_number_is_not():
    """Faras 44 writes the numeral 1 after each prince's name; "(13)" is a line number of the copy."""
    words, _, _ = F.words_of("pese(2)to : krinkror 1 peseto (13) 13 mto", {"pesto"}, [])
    assert F.K.spell(words).split() == ["pesto", "krinkror", "1", "pesto", "13", "mto"]
    first = {44: made_up(44, "x", "peseto 1 krinkror 13")}
    r = F.rows(first, {}, {}, [], set())[0]
    assert r["text_corpus"] == "pesto 1 krinkror 13" and r["words"] == 4 and r["signs"] == 4 + 8   # p e se to; k r i n k r o r
    with tempfile.TemporaryDirectory() as d:                                  # the check of a final reading lets them be
        (pathlib.Path(d) / "A").mkdir()
        (pathlib.Path(d) / "A" / "readings.jsonl").write_text(json.dumps(first[44]) + "\n")
        assert list(F.readings(pathlib.Path(d))) == [44]
        (pathlib.Path(d) / "settled.jsonl").write_text(json.dumps(first[44]) + "\n")    # and so does the settling's
        assert list(F.settled(pathlib.Path(d) / "settled.jsonl")) == [44]


def test_the_known_words_are_the_other_griffith_rows():
    kw = F.known_words()
    assert {"woSi", "Soreyi", "tedxelowi", "terikelowi", "at", "ato", "mXe"} <= kw
    assert all(w.isalpha() for w in kw) and F.known_words(least=10_000) == set()
    # a word counts once a text; a word with a lost sign is none; the Faras rows, a sub-folder, are not read
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        (d / "faras").mkdir()
        row = lambda text: json.dumps({"text_corpus": text}) + "\n"
        (d / "griffith_a.jsonl").write_text(row("woSi woSi qore.") + row("woSi Soreyi qore.") + row("Soreyi qore."))
        (d / "griffith_b.jsonl").write_text(row("woSi") + row("Soreyi"))
        (d / "other.jsonl").write_text(row("ato") * 3)
        (d / "faras" / "griffith_faras.jsonl").write_text(row("mXe") * 3)
        assert F.known_words((d,)) == {"woSi", "Soreyi"} and F.known_words((d,), least=4) == set()


def test_a_restoration_over_a_word_end_keeps_the_two_words():
    """Faras 5: "terike[li teri](6)kelowi" is terikeli terikelowi, its middle restored; the bracket's lost signs
    stay in both words and the reading as written is untouched."""
    assert F.restored("keyñ terike[li teri](6)kelowi") == "keyñ terike[li] [teri](6)kelowi"
    assert F.restored("so[re](2)yi [:] ye") == "so[re](2)yi [:] ye"                   # nothing to part
    first = {5: made_up(5, "keyñ", "(5)keyñ terike[li teri](6)kelowi")}
    r = F.rows(first, {}, {}, F.formula_pairs())[0]
    assert r["text_corpus"] == "keyN terike.. ...kelowi" and r["words"] == 3
    assert r["text_std"] == "(5)keyñ terike[li teri](6)kelowi" and r["signs"] == 4 + 5 + 6    # restored: lost


def test_readings_stops_on_what_is_not_a_reading():
    with tempfile.TemporaryDirectory() as d:
        pack = pathlib.Path(d) / "A"
        pack.mkdir()
        f = pack / "readings.jsonl"
        f.write_text(json.dumps(made_up(1, "wos", "wos")) + "\n")
        assert list(F.readings(pathlib.Path(d))) == [1]
        for bad in (made_up(47, "wos", "wos"), {"text": "Kar. 1", "first": "", "final": ""},
                    made_up(1, "wos", "wos 3"), made_up(2, "wos", "w(o)s")):
            f.write_text(json.dumps(made_up(1, "wos", "wos")) + "\n" + json.dumps(bad) + "\n")
            try:
                F.readings(pathlib.Path(d))
            except ValueError:
                continue
            raise AssertionError(f"accepted {bad}")


# --- the files ---
def test_rows_file_is_current():
    assert rows_file() == F.rows()


def test_rows_hold_every_text_typed_once_in_the_corpus_spelling():
    rows, typed = rows_file(), sorted(F.readings())
    assert typed == list(range(1, len(typed) + 1)) and set(F.DRAWN) <= set(typed)   # Faras 1 to N, the drawn five in
    assert [r["label"] for r in rows] == [f"Faras {n}" for n in typed]
    for r in rows:
        assert all(re.fullmatch(r"[abdeiklmnopqrstwxySNX.]+|\d+", w) for w in r["text_corpus"].split()), r["label"]
        assert r["words"] == sum(bool(re.search("[a-zA-Z0-9]", w)) for w in r["text_corpus"].split())   # numerals count
        assert r["signs"] == len(F.bare(r["text_std"])) and r["source"] == F.SOURCE


def test_the_corpus_reads_them_as_open_readings_of_rem_0501_to_0546():
    rows = [R.finish(r) for r in R.griffith_rows("data/expansion/faras", "griffith")]
    assert len(rows) == len(F.readings()) and ("data/expansion/faras", "griffith") in R.GRIFFITH
    for n, g in zip(sorted(F.readings()), rows):
        assert g["key"] == f"griffith:G-faras-{F.rem(n)}" and g["numbers"] == {"rem": [F.rem(n)]}
        assert g["v5"] is None and g["open"] and g["typed"] and g["number"] == f"Faras {n}" and g["site"] == "Faras"


def test_corpus_v5_does_not_take_them():
    """src/expand.py reads data/expansion and not its sub-folders: corpus_v3 and corpus_v5 stay as they were."""
    assert not any(r["id"].startswith("G-faras") for r in E.load_griffith())


def test_published_measure():
    m = json.loads(F.MEASURE.read_text())
    assert m == F.measure()
    assert m["texts"] == [f"Faras {n}" for n in F.DRAWN] and m["bar"] == 0.95
    assert m["met"] == (m["final"]["agree"] / m["final"]["signs"] >= 0.95)


def test_the_bar_is_met_on_the_counts():
    """95 of 100 signs meets the bar and 94 do not; 37,999 of 40,000, whose share rounds to 0.95, do not."""
    real, texts = F.agreement, {n: made_up(n, "", "") for n in F.DRAWN}
    try:
        for agree, total, met in ((95, 100, True), (94, 100, False), (37999, 40000, False), (38000, 40000, True)):
            F.agreement = lambda pairs, a=agree, t=total: (a, t)
            m = F.measure(texts, texts)
            assert m["met"] is met and m["final"]["share"] == round(agree / total, 4), (agree, total)
    finally:
        F.agreement = real


def test_published_comparison_has_counts_only():
    figs = json.loads(F.COMPARISON.read_text())
    keys = set()
    def walk(x, at=()):
        if isinstance(x, dict):
            for k, v in x.items():
                keys.add(k)
                walk(v, at + (k,))
        elif isinstance(x, list):
            for v in x:
                walk(v, at)
        elif isinstance(x, str):
            assert at[:1] == ("how",) or at[-1] in ("verdict", "key", "rem", "class", "by"), at   # no text
    walk(figs)
    assert "text" not in keys


def test_comparison_recomputed():
    needs("data/sources/v6/inscriptions.jsonl", "data/sources/v6/lines.jsonl", "data/otten")
    assert json.loads(F.COMPARISON.read_text()) == F.comparison(F.rows())


def test_the_page_quotes_the_comparison():
    """What the page says of Millet's quotations is what comparison.json counts."""
    texts = json.loads(F.COMPARISON.read_text())["texts"]
    page = " ".join((F.FARAS / "README.md").read_text(encoding="utf-8").split())
    parts = [l for t, e in texts.items() if t != "Faras 38" for l in e.get("lines", []) if l["class"] == "phrase"]
    agree, letters = (sum(l["folded"][k] for l in parts) for k in ("agree", "letters"))
    assert len(parts) == 11 and f"on {agree} of {letters} letters" in page                  # the quotations of parts
    assert len(texts["Faras 21"]["lines"]) == 7                                              # seven of them of Faras 21
    for text, key in (("Faras 43", "otten:MilletExamples.txt:286"), ("Faras 44", "mnl:REM 0544|MeroNews28"),
                      ("Faras 44", "otten:MilletExamples.txt:629")):                      # the whole texts
        a = texts[text]["against"][key]
        assert f"| {a['letters']} | {a['agree']} ({a['agree'] / a['letters']:.1%}) |" in page, (text, key)


def test_the_page_quotes_the_rows():
    """Section 3's table, the counts of sections 1 and 2 and the gaps closed are what the rows and the readers' files
    give."""
    rows, first, decided = rows_file(), F.readings(), F.settled()
    page = " ".join((F.FARAS / "README.md").read_text(encoding="utf-8").split())
    lost = lambda r: F.K.signs(r["text_std"]).count(".")                       # noqa: E731
    for r in rows:
        o = first[int(r["label"].split()[1])]
        line = re.escape(f"| {r['label']} | {r['rem']} | {o['pack']} |") + r" [^|]* \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|"
        m = re.search(line, page)
        assert m and tuple(map(int, m.groups())) == (o["rows"], r["signs"], r["words"], lost(r),
                                                      F.K.changed(o["first"], o["final"])), r["label"]
    changed = sum(F.K.changed(o["first"], o["final"]) for o in first.values())
    read = sum(len(F.bare(o["first"])) for o in first.values())
    assert (f"with {sum(map(lost, rows))} lost signs and {sum(r['uncertain'] for r in rows)} query marks), in "
            f"{sum(o['rows'] for o in first.values())} rows of the copies" in page)
    assert f"**{changed} ({changed / read:.1%})**" in page and f"over the {read:,} signs first read" in page
    assert f"(`kept`, {sum(len(o.get('kept', [])) for o in first.values())} places)" in page
    assert f"(`unsure`, {sum(len(o.get('unsure', [])) for o in first.values())} places)" in page
    known, pairs = F.known_words(), F.formula_pairs()
    gaps = [F.words_of(decided[n]["final"] if n in decided else o["final"], known, pairs)[1] for n, o in first.items()]
    assert f"{sum(gaps)} gaps in {sum(g > 0 for g in gaps)} texts" in page


def test_settled_readings_differ_from_the_first_only_where_listed():
    """The settled reading is the first reader's with each listed place put right, and nothing else changed (line
    numbers stand inside words, so the places are compared without them)."""
    bare_ = lambda t: re.sub(r"\(\d+\)", "", t)
    # each line number with the signs before it: no place settled here adds or drops a sign, so they stand alike
    at = lambda t: [(m.group(0), len(F.K.signs(t[:m.start()]))) for m in re.finditer(r"\(\d+\)", t)]
    first, decided = F.readings(), F.settled()
    assert sorted(decided) == list(F.DRAWN)
    for n, o in decided.items():
        assert at(o["final"]) == at(first[n]["final"]), n
        for p in o["places"]:
            assert p["why"] and bare_(p["settled"]) in bare_(o["final"]), (n, p)
            assert p["first"] == p["settled"] or len(F.K.signs(p["first"])) == len(F.K.signs(p["settled"])), (n, p)
        # a place where the first reading stands changes nothing; two places can lie on one stretch (Faras 13's
        # psiḫ r, parted, and psiḫr with or without lost signs after it), so each is put right once its stretch is
        # found, in whatever order
        text, todo = bare_(first[n]["final"]), [p for p in o["places"] if p["first"] != p["settled"]]
        while todo:
            p = next((p for p in todo if bare_(p["first"]) in text), None)
            assert p is not None, (n, todo)
            text = text.replace(bare_(p["first"]), bare_(p["settled"]), 1)
            todo.remove(p)
        assert text == bare_(o["final"]), n


def test_the_verdicts_go_into_the_builds_file_in_place_of_the_old_ones():
    with tempfile.TemporaryDirectory() as d:
        ours, build = pathlib.Path(d) / "ours.jsonl", pathlib.Path(d) / "verdicts.jsonl"
        line = lambda o: json.dumps(o) + "\n"                                    # noqa: E731
        ours.write_text(line({"line": "L2", "same_as": "k2", "part": False, "readers": "two"}) +
                        line({"line": "L9", "same_as": "k9", "part": True, "readers": "two"}))
        build.write_text(line({"line": "L1", "same_as": "k1", "part": True}) + line({"line": "L2", "same_as": "", "part": False}))
        want = [{"line": "L1", "same_as": "k1", "part": True}, {"line": "L2", "same_as": "k2", "part": False},
                {"line": "L9", "same_as": "k9", "part": True}]
        assert F.merge_verdicts(ours, build) == (1, 1) and F.load(build) == want
        assert F.merge_verdicts(ours, build) == (2, 0) and F.load(build) == want            # run again: the same file


def test_the_verdicts_are_what_both_readers_answered():
    """verdicts.jsonl holds the line, the text and the part that both readers named, each on its own pack (local)."""
    folder = "data/sources/faras/v6readers"
    needs(f"{folder}/key.json", f"{folder}/r1/answers.jsonl", f"{folder}/r2/answers.jsonl")
    key = json.loads((ROOT / folder / "key.json").read_text(encoding="utf-8"))
    said = {}
    for r in ("1", "2"):
        for a in F.load(ROOT / folder / f"r{r}" / "answers.jsonl"):
            item = key[r][a["item"]]
            said.setdefault(item["line"], []).append((item.get(a["same_as"], ""), a["part"]))
    agreed = {line: v[0] for line, v in said.items() if len(v) == 2 and v[0] == v[1]}
    assert {o["line"]: (o["same_as"], o["part"]) for o in F.load(F.VERDICTS)} == agreed and len(agreed) == 2


def test_published_recur():
    needs("data/sources/v6/analysts/glosses.jsonl", "data/corpus_v6.jsonl")
    r = json.loads(F.RECUR.read_text())
    assert r == F.recur()
    assert r["in_one_text_now_in_a_faras_text"] <= r["map"]["in_one_text"] <= r["map"]["in_one_text_on_the_map"]
    # Faras 44 is REM 0544, on the map before; Faras 43 was on it as Millet's line 286, whose reading REM 0543 prefers
    assert r["new_texts"] == len([n for n in F.readings() if F.rem(n) not in ("0543", "0544")])
    s = r["new_spellings"]
    assert s["on_the_map"] + s["new_to_the_map"] == s["distinct"] and s["open_on_the_map"] <= s["on_the_map"]


def test_the_page_quotes_the_recount():
    """What the page says recurs is what recur.json counts (public)."""
    r = json.loads(F.RECUR.read_text())
    s, m = r["new_spellings"], r["map"]
    page = " ".join((F.FARAS / "README.md").read_text(encoding="utf-8").split())
    assert f"{m['in_one_text_on_the_map']:,} open spellings that stand in one of its texts" in page
    assert f"{r['in_one_text_now_in_a_faras_text']} of them now stand in a new Faras text too" in page
    assert f"{r['reach_three_texts']} open spellings reach three texts" in page
    assert (f"Of the {s['distinct']} distinct spellings of the {r['new_texts']} texts new to the map" in page and
            f"{s['on_the_map']} are on the map already, {s['open_on_the_map']} of them open; {s['new_to_the_map']} are "
            f"new to it, and {s['new_to_the_map_in_two_faras_texts']} of those stand in two Faras texts" in page)
    rows = rows_file()
    assert f"All {len(rows)} texts are typed" in page
    assert f"{sum(r['signs'] for r in rows):,} signs and {sum(r['words'] for r in rows)} words" in page


def test_the_studies_of_the_map_read_the_texts_of_the_map():
    """corpus_v6 grows (the Faras texts) and can lose a text found to be part of another (Millet's line 414 is part of
    Faras 21); the map does not. Its studies read lexicon.MAPPED, the corpus as the analysts glossed it."""
    import lexicon as X
    import recurring as W
    import f4
    import words as D
    assert f4.CORPUS == X.MAPPED and f4.INSCRIPTIONS == X.MAPPED_TABLE
    needs("data/sources/v6/analysts/corpus.jsonl", "data/sources/v6/analysts/glosses.jsonl", "data/rilly2003")
    mapped = [json.loads(l)["id"] for l in X.MAPPED.read_text(encoding="utf-8").splitlines() if l.strip()]
    glossed = [json.loads(l)["id"] for l in X.GLOSSES.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert mapped == glossed and len(mapped) == 548
    assert not ({f"REM {F.rem(n)}" for n in F.readings()} - {"REM 0544"}) & set(mapped)    # the new texts are not on it
    assert list(W.corpus_rows()) == mapped and set(D.lookup_only()) == set(mapped)          # the studies and "before us"


if __name__ == "__main__":
    run([(n, f) for n, f in globals().items() if n.startswith("test_")])
