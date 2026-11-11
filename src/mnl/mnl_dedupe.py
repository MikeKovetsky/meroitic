"""Mark which Newsletter texts are already in the corpus, and which are a second edition of another row.

  python3 -I mnl_dedupe.py <repo root> <mnl_texts.jsonl> [--show]      (rewrites the file with the new fields)

Both sides are first spelled alike (src/expand.py skeleton()). The test uses a text's distinctive letter
6-grams only: 6-grams inside unbroken stretches, leaving out those that 4 or more lines of Millet's examples
share, or 20 or more corpus texts (the funerary formulae). A text with fewer than 6 such 6-grams cannot
be tested. Two Newsletter rows are compared without the 6-grams that 4 or more Newsletter rows share as
well: the formulae as the Newsletter spells them, which the corpus spells otherwise.

References: every text of data/corpus_v3.jsonl, and every line of Otten's file of Millet's examples
(data/otten/Data/MilletExamples.txt), where names are not masked.

Fields added to each row:
  tested      false when the text is too short or too formulaic to test
  in_corpus   the corpus text or Millet line that holds half or more of its distinctive 6-grams, or that holds
              another edition of the same inscription ("<corpus id> (as <row id>, <source>)"), or ""
  share       the row's own share
  same_as     the row kept for this inscription when it is printed more than once, or "". Two rows whose
              pages give two different REM numbers are two inscriptions, however alike their texts, and so
              are the pairs in TWO_INSCRIPTIONS.
  new         true when in_corpus and same_as are empty and the row has at least one whole word
"""
import json, re, sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mnl_signs as S  # noqa: E402

N, COMMON, COMMON_CORPUS, MIN = 6, 4, 20, 6


def grams(s):
    return {p[i:i + N] for p in s.split("#") for i in range(len(p) - N + 1)}


def year(r):
    return int(re.search(r"\((\d{4})\)", r["source"]).group(1))


def page_rem(r):
    """The REM number the page gives (its four digits), or "": a printout row numbered only by working the
    number out from the order of the printout (~ or ? on every line) has none."""
    if r["kind"] == "printout" and all(l.split("|")[0].strip()[:1] in "~?" for l in r["lines"]):
        return ""
    return r["rem"][:4]


# An inscription that a later issue edits again under another REM number, so that the two rows share no number
# and too little text to be matched. The Obelisk of Meroe: the printout's REM 1041 (Hintze's fragments) is the
# text that Newsletter 29 edits as REM 1041A-B and REM 1361A-D.
RENUMBERED = {"1041": "1361"}

# Texts that the tests below take for one and that are not. Each was looked at in the collation of 2026-11-10
# (data/expansion/newsletter_reading.md, section 4): two objects that open with the same Apedemak formula (REM 1051
# and 1054), two epitaphs with the same invocation and benedictions, ten pages apart in the printout (REM 1059 and
# 1073), and a short epitaph whose benedictions, in the same spelling, end a long corpus text of other people
# (REM 1085 and corpus text T0792, which is line 1213 of Millet's examples).
TWO_INSCRIPTIONS = {frozenset(("1051", "1054")), frozenset(("1059", "1073"))}
NOT_THE_CORPUS_TEXT = {"1085": {"T0792", "Millet's examples, line 1213"}}     # the corpus text and its source line


def best_match(r, refs):
    """(share, id) of the reference that holds most of the row's distinctive 6-grams ("_g"); a corpus text the row
    is known not to be is passed over."""
    apart = NOT_THE_CORPUS_TEXT.get(r["rem"][:4], ())
    return max(((len(r["_g"] & gs) / len(r["_g"]), rid) for rid, gs in refs if rid not in apart), default=(0.0, ""))


def editions(rows, skeletons, formulae=frozenset()):
    """Mark each row printed more than once (same_as): keep the later issue, then the longer text, except where
    the later issue reprints only a part of an earlier, fuller text (it holds less than half of that text, which
    holds most of it): then the fuller text is kept. Rows carry their distinctive 6-grams in "_g"; skeletons[i]
    is row i's skeleton; formulae are 6-grams left out of the comparison. A kept row whose other edition is in
    the corpus is in the corpus too."""
    own = [r["_g"] - formulae for r in rows]
    order = sorted(range(len(rows)), key=lambda i: ("reconstruction" in rows[i]["id"].lower(), -year(rows[i]), -rows[i]["words"]))
    name = lambda r: f"{r['id']} ({r['source']})"
    kept, of = [], {}
    for i in order:
        r = rows[i]
        r["same_as"] = ""
        again = [o for o in rows if r["kind"] == "printout" and o is not r and o["rem"][:4] == RENUMBERED.get(r["rem"][:4])]
        if again:                                          # edited again under another number: the later edition is kept
            r["same_as"] = f"{again[0]['id']} and the rest of that edition ({again[0]['source']})"
            continue
        for n, k in enumerate(kept):
            o = rows[k]
            if page_rem(r) and page_rem(o) and page_rem(r) != page_rem(o):
                continue                                   # two numbers on the pages: two inscriptions
            if frozenset((r["rem"][:4], o["rem"][:4])) in TWO_INSCRIPTIONS:
                continue                                   # looked at: two inscriptions
            shared = len(own[i] & own[k])
            a = shared / len(own[i]) if own[i] else 0
            b = shared / len(own[k]) if own[k] else 0
            tested = len(own[i]) >= MIN and len(own[k]) >= MIN
            same_rem = bool(r["rem"]) and r["rem"] == o["rem"] and r["file"] != o["file"]
            twin = same_rem and skeletons[i][:12] == skeletons[k][:12]
            if (tested and max(a, b) >= 0.5) or (same_rem and max(a, b) >= 0.2) or twin:
                if tested and b >= 0.5 > a:                # the kept row is a part of this fuller one: keep this one
                    kept[n] = i
                    for j in [j for j, m in of.items() if m == k] + [k]:
                        of[j] = i
                        rows[j]["same_as"] = name(r)
                else:
                    r["same_as"] = name(o)
                    of[i] = k
                break
        else:
            kept.append(i)
    for i, k in of.items():
        if rows[i]["in_corpus"] and not rows[k]["in_corpus"]:
            rows[k]["in_corpus"] = f"{rows[i]['in_corpus']} (as {rows[i]['id']}, {rows[i]['source']})"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ROOT, PATH = Path(sys.argv[1]), Path(sys.argv[2])
    S.need(ROOT / "data/corpus_v3.jsonl", ROOT / "data/otten/Data/MilletExamples.txt", PATH)
    sys.path.insert(0, str(ROOT / "src"))
    import expand as E
    corpus = [json.loads(l) for l in (ROOT / "data/corpus_v3.jsonl").read_text().splitlines()]
    refs = [(c["id"], grams(E.skeleton(c["text"]))) for c in corpus]
    millet = []
    for k, line in enumerate((ROOT / "data/otten/Data/MilletExamples.txt").read_text(errors="replace").splitlines(), 1):
        if line.startswith("#") or not line.strip():
            continue
        gs = grams(E.skeleton(line.split("\t")[0]))
        if len(gs) >= MIN:
            millet.append((f"Millet's examples, line {k}", gs))
    rows = [json.loads(l) for l in PATH.read_text().splitlines()]
    skeletons = [E.skeleton(r["text_corpus"]) for r in rows]
    # the formulae: 6-grams that COMMON or more of Millet's lines share, or COMMON_CORPUS corpus texts: the corpus
    # holds some texts several times over (name-swapped copies), so that a lower count there would make a text's
    # own letters look common.
    common = {g for g, n in Counter(g for _, gs in millet for g in gs).items() if n >= COMMON}
    common |= {g for g, n in Counter(g for _, gs in refs for g in gs).items() if n >= COMMON_CORPUS}
    spelled_here = {g for g, n in Counter(g for s in skeletons for g in grams(s)).items() if n >= COMMON}
    refs += millet
    for r, s in zip(rows, skeletons):
        r["_g"] = grams(s) - common
        r["tested"] = len(r["_g"]) >= MIN
        r["in_corpus"], r["share"] = "", 0.0
        if r["tested"]:
            share, rid = best_match(r, refs)
            r["share"] = round(share, 2)
            if share >= 0.5:
                r["in_corpus"] = rid
    editions(rows, skeletons, spelled_here)
    for r in rows:
        r["new"] = not r["in_corpus"] and not r["same_as"] and r["words"] > 0
        del r["_g"]
    PATH.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    new = [r for r in rows if r["new"]]
    count = lambda rs: sum(len(E.words(r["text_corpus"])) for r in rs)
    print(f"rows {len(rows)}: already in the corpus {sum(bool(r['in_corpus']) for r in rows)}, "
          f"second editions {sum(bool(r['same_as']) and not r['in_corpus'] for r in rows)}, "
          f"no whole word {sum(1 for r in rows if not r['in_corpus'] and not r['same_as'] and r['words'] == 0)}, new {len(new)}")
    print(f"NEW: {len(new)} texts ({sum(r['tested'] for r in new)} tested, {sum(not r['tested'] for r in new)} too short or formulaic to test), "
          f"{sum(r['words'] for r in new)} whole words, {sum(r['broken_words'] for r in new)} broken words; "
          f"{count(new)} words by the corpus's own count (numerals and broken words included)")
    print(f"  of which tested texts: {sum(r['words'] for r in new if r['tested'])} whole words")
    by = Counter()
    for r in new:
        by[r["file"]] += r["words"]
    print("  whole words by issue:", dict(sorted(by.items())))
    if "--show" in sys.argv:
        print("  in corpus:")
        for r in rows:
            if r["in_corpus"]:
                print(f"    {r['id']} ({r['file']}, {r['words']} words) = {r['in_corpus']}, share {r['share']}")
        print("  second editions:")
        for r in rows:
            if r["same_as"] and not r["in_corpus"]:
                print(f"    {r['id']} ({r['file']}) = {r['same_as']}")
        print("  shares of the new tested texts:", sorted(r["share"] for r in new if r["tested"])[-25:])


if __name__ == "__main__":
    main()
