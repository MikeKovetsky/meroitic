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
        assert all(re.fullmatch(r"[abdeiklmnopqrstwxySNX.]+", w) for w in r["text_corpus"].split()), r["label"]
        assert r["words"] == sum(bool(re.search("[a-zA-Z]", w)) for w in r["text_corpus"].split())
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
    assert m["met"] == (m["final"]["share"] >= 0.95)


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
            assert at[:1] == ("how",) or at[-1] in ("verdict", "key", "rem"), at   # no text, closed or ours
    walk(figs)
    assert "text" not in keys


def test_comparison_recomputed():
    needs("data/sources/v6/inscriptions.jsonl", "data/otten")
    assert json.loads(F.COMPARISON.read_text()) == F.comparison(F.rows())


def test_settled_readings_differ_from_the_first_only_where_listed():
    first, decided = F.readings(), F.settled()
    assert sorted(decided) == list(F.DRAWN)
    for n, o in decided.items():
        if not o["places"]:
            assert o["final"] == first[n]["final"]
        for p in o["places"]:                       # line numbers stand inside words: compare without them
            assert re.sub(r"\(\d+\)", "", p["settled"]) in re.sub(r"\(\d+\)", "", o["final"]) and p["why"]


def test_published_recur():
    needs("data/sources/v6/analysts/glosses.jsonl", "data/corpus_v6.jsonl")
    r = json.loads(F.RECUR.read_text())
    assert r == F.recur()
    assert r["in_one_text_now_in_a_faras_text"] <= r["map"]["in_one_text"]
    assert r["new_texts"] == len([n for n in F.readings() if F.rem(n) != "0544"])


def test_the_studies_of_the_map_read_the_texts_of_the_map():
    """corpus_v6 grows (the Faras texts) and can lose a text found to be part of another (Millet's line 414 is part of
    Faras 21); the map does not. Its studies read lexicon.MAPPED, the corpus as the analysts glossed it."""
    import lexicon as X
    import recurring as W
    assert W.corpus_rows.__doc__ and "MAPPED" in W.corpus_rows.__doc__
    needs("data/sources/v6/analysts/corpus.jsonl", "data/sources/v6/analysts/glosses.jsonl")
    mapped = [json.loads(l)["id"] for l in X.MAPPED.read_text(encoding="utf-8").splitlines() if l.strip()]
    glossed = [json.loads(l)["id"] for l in X.GLOSSES.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert mapped == glossed and len(mapped) == 548
    assert not ({f"REM {F.rem(n)}" for n in F.readings()} - {"REM 0544"}) & set(mapped)    # the new texts are not on it


if __name__ == "__main__":
    run([(n, f) for n, f in globals().items() if n.startswith("test_")])
