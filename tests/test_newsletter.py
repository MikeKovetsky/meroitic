"""Checks for the Meroitic Newsletter reading (data/expansion/newsletter_reading.md, src/mnl/) that need the typed
texts, which stay on the author's machine (README, Data): the rebuild gives the files the page counts, the page's
counts and accuracy figures come out of them, and no typed line is in a file that git tracks. The scripts
themselves are tested on made-up lines by src/mnl/test_mnl.py.

  python3 -I tests/test_newsletter.py
"""
import json, re, subprocess, sys, tempfile, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tests")]

from local_only import needs, run   # noqa: E402

MNL = "data/sources/mnl"
RESULTS = ("mnl_texts.jsonl", "dedupe_report.txt", "corpus_v4.jsonl")
TYPEWRITTEN = {"MeroNews18", "MeroNews21", "MeroNews22", "MeroNews25b", "MeroNews26a"}   # the issues not tested


def rows():
    return [json.loads(l) for l in (ROOT / MNL / "mnl_texts.jsonl").read_text().splitlines()]


def test_rebuild_gives_the_local_files():
    needs(f"{MNL}/readings/raw", f"{MNL}/readings/inventory", *(f"{MNL}/{f}" for f in RESULTS), "data/corpus_v3.jsonl",
          "data/otten/Data/MilletExamples.txt")
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["bash", str(ROOT / "src/mnl/rebuild.sh"), str(ROOT), d], check=True, capture_output=True)
        for f in RESULTS:
            assert (Path(d) / f).read_bytes() == (ROOT / MNL / f).read_bytes(), f


def test_reported_newsletter_numbers():
    needs(f"{MNL}/mnl_texts.jsonl", f"{MNL}/corpus_v4.jsonl", "data/corpus_v3.jsonl")
    rs = rows()
    new = [r for r in rs if r["new"]]
    words = lambda path: [len(json.loads(l)["text"].split()) for l in (ROOT / path).read_text().splitlines()]
    v3, v4 = words("data/corpus_v3.jsonl"), words(f"{MNL}/corpus_v4.jsonl")
    # the page, section 1
    assert (len(rs), Counter(r["kind"] for r in rs)) == (256, {"printout": 110, "print": 146})
    assert (len(new), sum(r["words"] for r in new)) == (185, 2690)
    assert (sum(bool(r["in_corpus"]) for r in rs), sum(bool(r["same_as"]) and not r["in_corpus"] for r in rs),
            sum(not r["in_corpus"] and not r["same_as"] and r["words"] == 0 for r in rs)) == (9, 11, 51)
    assert (len(v4), sum(v4), len(v3), sum(v3)) == (933, 22531, 748, 19066)
    assert sum(bool(r["rem"]) for r in rs) == 218
    # sections 3 and 6
    assert sum(r["file"] in TYPEWRITTEN for r in new) == 36
    assert sum("worked out from the order" in r["notes"] for r in rs if r["kind"] == "printout") == 59
    quick = [r for r in rs if "first test without enlarging" in r["notes"]]
    assert [r["rem"] for r in quick] == [str(n) for n in range(1042, 1049)]
    assert ([r["rem"] for r in quick if r["new"]], sum(r["words"] for r in quick if r["new"])) == (["1042", "1043", "1046"], 19)


def test_reported_accuracy_numbers():
    test, otten = f"{MNL}/readings/test", "data/otten/Data"
    akinidad, tanyidamani = f"{otten}/HamadabStelaOfAmanirenasNarrative.txt", f"{otten}/TanyidamaniNarrative.txt"
    needs(*(f"{test}/r{k}.txt" for k in "1234"), akinidad, tanyidamani, f"{otten}/Kalabsha_Millet.txt",
          f"{otten}/KalabshaMeroiticInscriptionOfKharamadoyeNarrative.txt", "data/corpus_v3.jsonl")
    tool = lambda script, *args: subprocess.run([sys.executable, "-I", str(ROOT / "src/mnl" / script), *map(str, args)],
                                                capture_output=True, text=True, check=True, cwd=ROOT).stdout
    pages = lambda a, b: ",".join(f"p{k:02d}" for k in range(a, b + 1))
    out = tool("mnl_score.py", "millet", f"{test}/r4.txt", f"{otten}/KalabshaMeroiticInscriptionOfKharamadoyeNarrative.txt",
               f"{otten}/Kalabsha_Millet.txt")                                       # the page, section 3, the table
    assert "covered 1031," in out and "agreement 97.6%" in out and "covered 1018," in out and "agreement 98.5%" in out
    for reading, ref, pp, extra, said in [
            ("r1", akinidad, pages(5, 10), [], ("95.4% of 1634 reference", "only in reading 51,", "207 (95%)")),
            ("r3", akinidad, "p07,p09", [], ("94.1% of 625 reference", "only in reading 6,", "78 (96%)")),
            ("r3", tanyidamani, "p25,p27,p29", [], ("97.0% of 900 reference", "only in reading 32,", "118 (91%)")),
            ("r2", tanyidamani, pages(23, 30), ["--quick"], ("93.7% of 2172 reference", "only in reading 158,", "317 (76%)"))]:
        out = tool("mnl_round.py", "test", ROOT, f"{test}/{reading}.txt", ref, pp, *extra)
        assert all(s in out for s in said), (reading, pp, out)
    assert "agree on 97.4% of 623 signs" in tool("mnl_score.py", "pair", f"{test}/r1.txt", f"{test}/r3.txt")


def test_reported_abratoye_double_typing():
    needs(f"{MNL}/readings/abratoye_stela_mnl28_p24.txt", f"{MNL}/mnl_texts.jsonl")
    nfc = lambda s: unicodedata.normalize("NFC", s)
    first = nfc((ROOT / MNL / "readings/abratoye_stela_mnl28_p24.txt").read_text())
    first = "".join(l for l in first.splitlines() if not l.startswith("#"))
    second = nfc("".join(next(r for r in rows() if r["rem"] == "1333")["lines"]))
    plain = lambda s: re.sub(r"[①-⑳㉑-㉟\s]", "", s).replace("ẖ", "H")       # the stone's line numbers, spaces
    assert len(plain(first)) == 1293 and plain(first) == plain(second).replace("ḫ", "H") != plain(second)
    assert Counter(c for c in second if c in "ḫẖ") == {"ḫ": 25, "ẖ": 33} and set("ḫẖ").isdisjoint(first)


def test_no_typed_line_is_in_a_tracked_file():
    needs(f"{MNL}/mnl_texts.jsonl")
    nfc = lambda s: unicodedata.normalize("NFC", s)
    typed = set()
    for r in rows():
        for line in r["lines"]:
            body = nfc((line.split("|")[-1] if r["kind"] == "printout" else line).strip())
            if len(body.split()) >= 2 and len(re.findall(r"[^\W\d_]", body)) >= 10:
                typed.add(body)
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True, check=True).stdout
    found = []
    for f in tracked.splitlines():
        if (ROOT / f).is_file():
            text = nfc((ROOT / f).read_text(errors="replace"))
            found += [(f, t) for t in typed if t in text]
    assert len(typed) > 500 and not found, found[:5]


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")])
