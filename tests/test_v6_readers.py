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


def test_the_count_writes_to_a_folder_of_its_own():
    import packs as P                                  # the readers of the doubtful matches: their figures are public
    assert X.OUT not in (P.OUT, X.R.OUT, X.R.OUT / "coverage", X.NEW, X.R.PACKS, X.C.OUT, X.C.CORRECTED)
    assert X.PUBLIC != X.R.ROOT / "data/discovery/corpus_v6_figures.json"


def test_pieces_joined_without_the_limit_on_length():
    e = X.C.entry({"headword": "abcdef", "meaning_en": "a made-up thing", "status": "established",
                   "category": "substantif", "page_printed": 1})
    words, affixes, _ = X.C.index([e])
    texts = [("T1", "abc def zz"), ("T2", "abcdef zz"), ("T3", "abcdef")]
    glossed = X.C.gloss_texts([{"id": i, "text": t} for i, t in texts], words, affixes)
    assert [g["level"] for _, gs in glossed for g in gs][:2] == ["unknown", "unknown"]
    assert X.C.joins(list(glossed[0][1]), words, affixes, X.C.written_whole(glossed)) == []   # pieces of 3 letters
    assert X.longer_joins(glossed, words, affixes) == 2 and glossed[0][1][0]["level"] == "unknown"   # not applied
    one = X.C.gloss_texts([{"id": "T1", "text": "abc def"}, {"id": "T2", "text": "abcdef"}], words, affixes)
    assert X.longer_joins(one, words, affixes) == 0          # the word stands written as one in one text only


def page():
    return re.sub(r"\s+", " ", PAGE.read_text(encoding="utf-8"))


# numbers a text may state without a figure behind them: dates, the REM numbers it names, the bar and the gain
# expected beforehand, the cost by hand, and what the review replaced
STATED = {"2026-11-12", "1039", "1333", "1361", "85%", "265", "385", "1,012,556", "133,497", "125,907", "130,241",
          "119,048", "126,556", "127,513", "121,712", "128,082", "12"}
ANALYSTS = (133497, 125907, 130241, 119048, 126556, 127513, 121712, 128082)   # the cost, by hand
EXPECTED = (265, 385)                                                         # the gain told beforehand
NUMBER = re.compile(r"\d{4}-\d\d-\d\d|\d[\d,]*(?:\.\d+)?%?")


def numbers(text, stated=()):
    """The numbers of a text, outside its code blocks, that are neither below 10 nor stated."""
    found = {t.rstrip(",") for t in NUMBER.findall(re.sub(r"```.*?```", " ", text, flags=re.S))}
    return {t for t in found if t not in stated and not (t.isdigit() and int(t) < 10)}


def known(f):
    """Every number of the figures file and of the clean corpus's unread words, as a text writes it, and what the
    pages draw from them."""
    out = set()

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, int) and not isinstance(x, bool):
            out.update({str(x), f"{x:,}"})
        elif isinstance(x, float):
            out.add(f"{x:.1%}")
    walk(f)
    v6 = json.loads((ROOT / "data/discovery/corpus_v6_figures.json").read_text())["coverage"]["not_analysed"]
    walk({k: v6[k] for k in ("words", "spellings")})
    a, n = f["answers"], f["newly_translated"]
    for part in f["by_part"].values():
        walk({k: v["translated"] / v["words"] for k, v in part.items()})
    walk({"same side": a["same_translated_or_not"] / a["read_twice"]})
    out.add(f"{n['words'] / f['after']['words'] * 100:.1f}")                    # the points gained
    return out


def between(text, start, end="\n\n"):
    """The text from start (which stands once) to end, or to the text's end, its spaces as one."""
    assert text.count(start) == 1, start
    rest = text[text.index(start):]
    return re.sub(r"\s+", " ", rest[:rest.index(end)] if end in rest else rest)


def test_the_summaries_quote_the_figures():
    """README, REPORT, NEXT_STEPS and the summary page say of this step what the figures file says."""
    f = json.loads(FIGURES.read_text(encoding="utf-8"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
    steps = (ROOT / "NEXT_STEPS.md").read_text(encoding="utf-8")
    html = (ROOT / "docs/report.html").read_text(encoding="utf-8")
    parts = {"README, item 12": between(readme, "12. **Analysts on the spellings nobody had read", "13. **The same"),
             "README, step 19": between(readme, "### 19. Analysts on the unread spellings", "### 20."),
             "REPORT": between(report, "## Day five, evening", "3. **The same people in Demotic"),
             "REPORT, cost": between(report, "6. **Cost:** eight analysts", "7. **What the review changed:** the join"),
             "NEXT_STEPS, point 13": between(steps, "13. **Analysts on the unread spellings", "14. **The same"),
             "the summary page": between(html, "<tr><td>Have eight analysts read", "</tr>")}
    stated = STATED | {"12", "13", "14", "18", "19", "1.5", "0.5", "2.0", "384,658", "126,264",
                       "1,523,478"}                             # items and steps; the quote; the other step's cost
    for name, text in parts.items():
        odd = numbers(text, stated) - known(f)
        assert not odd, (name, sorted(odd))
    a, b, n = f["answers"], f["before"], f["newly_translated"]
    words = f"{a['spellings']} spellings ({a['running_words']:,} running words)"
    assert words in parts["README, item 12"] and words in parts["REPORT"]
    assert f"{b['translated'] + n['words']:,} of {b['words']:,}" in parts["REPORT"]
    assert f"{n['words']} running words more" in parts["NEXT_STEPS, point 13"]
    assert f"expected beforehand was {EXPECTED[0]} to {EXPECTED[1]} words" in parts["README, item 12"]
    assert f"eight analysts {sum(ANALYSTS):,} subagent tokens" in parts["REPORT, cost"]
    review = between(report, "7. **What the review changed:** the join")
    assert f"gives {f['longer_joins']} words, not the 12 counted by hand" in review


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
    assert f"the {x['spellings']} spellings ({x['running_words']:,} running words)" in text
    assert f"was {EXPECTED[0]} to {EXPECTED[1]} words; it is {n['words']}, about half the lower figure" in text
    assert 0.45 <= n["words"] / EXPECTED[0] <= 0.55
    assert f["still_not_analysed"] == 0
    v6 = json.loads((ROOT / "data/discovery/corpus_v6_figures.json").read_text())["coverage"]["not_analysed"]
    assert f"built with {v6['words']:,} of its words, in {v6['spellings']} spellings, that no analyst had seen" in text
    assert f"({v6['spellings']} and {v6['words']:,} are counted after the map's corrections)" in text
    assert f"without its limit on length, would translate {f['longer_joins']} words more" in text
    assert (f"eight analysts, {sum(ANALYSTS):,} subagent tokens (" + ", ".join(f"{t:,}" for t in ANALYSTS[:6]) +
            f" and {ANALYSTS[6]:,} on the seven packs, {ANALYSTS[7]:,} on the second reading)") in text
    assert f"is counted by `src/v6/readers.py` and gives {f['longer_joins']}" in text
    assert numbers(PAGE.read_text(encoding="utf-8"), STATED) <= known(f), \
        sorted(numbers(PAGE.read_text(encoding="utf-8"), STATED) - known(f))


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
