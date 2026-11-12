"""Checks for the analysts on the spellings of corpus_v6 that none had read (src/v6/readers.py).

  python3 -I tests/test_v6_readers.py

The lexicon, corpus_v6 and the analysts' answers are local only: the checks of the method run on made-up rows,
the checks of the reported numbers read the public figures file and compare it with the local files where those
are present.
"""
import json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src" / "v6"), str(ROOT / "src"), str(ROOT / "tests")]

import readers as X    # noqa: E402
from local_only import needs, run   # noqa: E402

PAGE = ROOT / "data/discovery/v6_readers.md"
FIGURES = ROOT / "data/discovery/corpus_v6_readers.json"
LOCAL = ("data/rilly2003", "data/corpus_v6.jsonl", "data/sources/coverage/packs", "data/sources/v6/packs")


def test_a_tagged_name_is_masked_and_not_sent():
    rows = [{"id": "REM 1", "text": "woSi tmeye qowi 12 xyz", "names": [1, 3]},
            {"id": "REM 2", "text": "tmeye abc", "names": []}, {"id": "REM 3", "text": "abc"}]
    masked = X.masked(rows)
    assert [r["text"] for r in masked] == ["woSi NAME qowi 12 xyz", "tmeye abc", "abc"]      # a numeral stays
    assert rows[0]["text"] == "woSi tmeye qowi 12 xyz"                                       # the rows are not changed
    new = X.unread(rows, {}, {}, have={"qowi"})                    # an empty lexicon: the lookup leaves every word
    words = {w["word"]: w for w in new}
    assert set(words) == {"woSi", "xyz", "tmeye", "abc"}           # not NAME, not the numeral, not a held word
    assert words["abc"]["count"] == 2 and words["tmeye"]["count"] == 1     # tmeye counts where it is not tagged
    assert [w["word"] for w in new][0] == "abc"                    # the most frequent first


def test_packs_are_numbered_after_the_old_ones_and_written_once():
    with tempfile.TemporaryDirectory() as d:
        old, out = Path(d) / "old", Path(d) / "new"
        for name, words in (("A001", ["a"]), ("A017", ["b"]), ("B002", ["a"])):
            (old / name).mkdir(parents=True)
            (old / name / "words.jsonl").write_text("".join(json.dumps({"word": w}) + "\n" for w in words))
        assert X.held(old, out) == {"a", "b"}
        new = [{"word": f"w{i}", "count": 9 - i, "texts": 1, "contexts": [], "griffith": []} for i in range(5)]
        made = X.write_packs(new, [], old=old, out=out, per=2, twice=3)
        assert made == ["A018", "A019", "A020", "B003", "B004"]
        read = lambda name: [json.loads(l)["word"] for l in (out / name / "words.jsonl").read_text().splitlines()]
        assert read("A018") + read("A019") + read("A020") == ["w0", "w1", "w2", "w3", "w4"]
        assert read("B003") + read("B004") == ["w0", "w1", "w2"]                 # the most frequent again
        assert (out / "A018" / "BRIEF.md").read_text() == X.C.BRIEF.read_text()
        assert X.held(old, out) == {"a", "b", "w0", "w1", "w2", "w3", "w4"}
        try:
            X.write_packs(new, [], old=old, out=out, per=2, twice=3)
        except SystemExit as e:
            assert "holds packs already" in str(e)
        else:
            raise AssertionError("the packs were written a second time")


def page():
    return re.sub(r"\s+", " ", PAGE.read_text(encoding="utf-8"))


def test_reported_numbers():
    f, text = json.loads(FIGURES.read_text(encoding="utf-8")), page()
    b, a, n, x = f["before"], f["after"], f["newly_translated"], f["answers"]
    assert f"| `corpus_v6` before | {b['words']:,} | {b['translated']:,} | {b['share']:.1%} |" in text
    assert f"| `corpus_v6` with the new answers | {a['words']:,} | {a['translated']:,} | {a['share']:.1%} |" in text
    part = "the Meroitic Newsletter"
    pb, pa = f["by_part"]["before"][part], f["by_part"]["after"][part]
    assert (f"| {pb['words']:,} | {pb['translated']:,} and {pa['translated']:,} | {pb['translated'] / pb['words']:.1%} and "
            f"{pa['translated'] / pa['words']:.1%} |") in text
    assert a["translated"] - b["translated"] == n["words"] == n["meaning"] + n["grammar"] + n["name"] + n["number"]
    assert (f"**{n['words']} words more are translated:** {n['name']} are names that the analysts recognised, "
            f"{n['meaning']} are words with a meaning and {n['grammar']} are grammar words") in text
    lv = x["levels"]
    assert (f"Of the {x['spellings']} spellings, {x['translated']} got a translated level** ({lv['name']} names, "
            f"{lv['meaning']} meanings, {lv['grammar']} grammar words), {lv['hypothesis']} a proposal of the lexicon, "
            f"{lv['kind']} only their kind, and {lv['unknown']} nothing") in text
    assert x["translated"] == lv["name"] + lv["meaning"] + lv["grammar"] and x["dropped"] == x["missing"] == 0
    assert (f"for {x['same_translated_or_not']} of {x['read_twice']} ({x['same_translated_or_not'] / x['read_twice']:.1%}), "
            f"and give {x['same_level']} the same level") in text
    assert x["same_translated_or_not"] / x["read_twice"] >= 0.85                 # the bar of the run
    assert f"the {x['spellings']} spellings (" in text and f"it is {n['words']}, about half the lower figure" in text
    assert f["still_not_analysed"] == 0


def test_public_figures_are_what_the_local_files_give():
    needs(*LOCAL)
    corpus = [json.loads(l) for l in X.R.CORPUS.read_text().splitlines() if l.strip()]
    _, figs = X.count(corpus)
    assert figs == json.loads(FIGURES.read_text(encoding="utf-8"))
    recount = json.loads((ROOT / "data/sources/v6/recount.json").read_text())["coverage"]["all"]
    assert (figs["before"]["words"], figs["before"]["translated"]) == (recount["words"], recount["translated"])
    words, affixes, _ = X.C.index(X.C.lexicon())
    assert X.unread(X.R.rows_for_map(corpus), words, affixes, X.held(X.R.PACKS, X.NEW)) == []   # nothing left unread
    sent = sum(1 for p in sorted(X.NEW.iterdir()) if p.name.startswith("A")
               for l in (p / "words.jsonl").read_text().splitlines() if l.strip())
    assert sent == figs["answers"]["spellings"]


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
