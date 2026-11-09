"""Add the Griffith transcriptions to the corpus: data/corpus_v3.jsonl.

data/expansion/griffith_*.jsonl hold texts read from Griffith's printed type
(Meroitic Inscriptions I-II, 1911-12; Meroe, 1911), in the corpus spelling.
Only whole texts are added: a row is left out when Griffith printed just part
of the text (its notes start "Partial", or it is in PARTIAL).

A Griffith text is dropped as already present when it matches a corpus_v2 text
or a Griffith text added before it. Both are first spelled alike (skeleton()),
so that the two spelling conventions in the corpus, word division, numerals
and lost signs don't hide a copy. They match when half or more of the text's
letter 6-grams occur in the other, or when the other, each masked name or lost
stretch standing for any letters, spells all of it with at least half of its
letters. Griffith's names are not masked (no name list exists for them), so
each added row says src "griffith".

  python3 src/expand.py          # writes corpus_v3.jsonl and prints the gain
"""
import fnmatch, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N = 6
# rows whose notes say in other words that Griffith printed only part of the text: 50 one row of a formula
# table, 58 the cartouche of (a) only, 59 and 60 their opening words or the parents' names in English only,
# 128 only the groups his commentary quotes
PARTIAL = {"mi1b": {50, 58, 59, 60}, "mi2b": {128}}


def words(text):
    text = re.sub(r"\(\d+\)|\|", " ", text)          # Griffith's line numbers and type-line marks
    text = re.sub(r"[#?]", "", text)
    return [w for w in text.split() if w.strip(".")]


def skeleton(text):
    """The letters of a text, spelled alike whichever corpus convention wrote it; '#' where letters are
    unknown (a masked name, lost signs).

    FHN lines write the s and se signs s and se, Millet's S and s, so s+e and the
    se sign both become s, and likewise n; x and X fold, and o and e (Millet's o
    is often typed e), first, so that so and se fold alike. Word division and
    numerals go.
    """
    t = re.sub(r"\bR?NAME\b|[.…]+", "#", text).lower()
    t = t.replace("o", "e").replace("se", "s").replace("ne", "n")
    return re.sub(r"#+", "#", re.sub(r"[^a-z#]", "", t))


def stretches(s):
    return [p for p in s.split("#") if p]


def grams(s):
    """Letter 6-grams within the known stretches; a text with none has its stretches whole."""
    g = {p[i:i + N] for p in stretches(s) for i in range(len(p) - N + 1)}
    return g or set(stretches(s))


def share(s, ref):
    """Share of s's grams that occur in the skeleton ref."""
    gs, parts = grams(s), stretches(ref)
    if not gs:
        return 0.0
    rg = {p[i:i + N] for p in parts for i in range(len(p) - N + 1)}
    return sum(g in rg if len(g) == N else any(g in p for p in parts) for g in gs) / len(gs)


def spelled(s, ref):
    """ref, each '#' standing for one or more letters, spells all of s, with at least half its letters."""
    own = len(ref) - ref.count("#")
    return "#" in ref and own * 2 >= len(s) - s.count("#") and fnmatch.fnmatchcase(s, ref.replace("#", "?*"))


def present(s, ref):
    return share(s, ref) >= 0.5 or spelled(s, ref)


def load_griffith():
    rows = []
    for p in sorted((ROOT / "data/expansion").glob("griffith_*.jsonl")):
        part = p.stem.split("_", 1)[1]
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            ws = words(r.get("text_corpus", ""))
            if not ws:
                continue
            letter = re.sub(r"^\d*", "", str(r.get("rem") or ""))     # REM 0091a, 0091b: one Griffith number
            partial = (r.get("notes") or "").lstrip().lower().startswith("partial") \
                or r.get("griffith_no") in PARTIAL.get(part, ())
            rows.append({"id": f"G-{part}-{r.get('griffith_no')}{letter}", "src": "griffith", "rem": r.get("rem", ""),
                         "copies": 1, "text": " ".join(ws), "partial": partial})
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        raise ValueError(f"repeated ids: {sorted({i for i in ids if ids.count(i) > 1})}")
    return rows


def merge(base, griffith):
    """(added, already present as (row, id of the text it matches), partial): what corpus_v3 takes."""
    refs = [(r["id"], skeleton(r["text"])) for r in base]
    added, dupes, partial = [], [], []
    for g in griffith:
        g = dict(g)
        if g.pop("partial"):
            partial.append(g)
            continue
        s = skeleton(g["text"])
        hit = next((rid for rid, ref in refs if present(s, ref)), None)
        if hit:
            dupes.append((g, hit))
        else:
            added.append(g)
            refs.append((g["id"], s))
    return added, dupes, partial


def main():
    base = [json.loads(l) for l in (ROOT / "data/corpus_v2.jsonl").read_text().splitlines()]
    griffith = load_griffith()
    added, dupes, partial = merge(base, griffith)
    with open(ROOT / "data/corpus_v3.jsonl", "w") as f:
        for r in base + added:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tok = lambda rows: sum(len(r["text"].split()) for r in rows)
    print(f"griffith texts {len(griffith)}: partial {len(partial)} ({tok(partial)} words, left out); "
          f"already present {len(dupes)} ({tok([g for g, _ in dupes])} words); new {len(added)} ({tok(added)} words)")
    print("already present:", " ".join(f"{g['id']}={b}" for g, b in dupes))
    print(f"corpus_v2 {len(base)} texts {tok(base)} words -> corpus_v3 {len(base) + len(added)} texts "
          f"{tok(base) + tok(added)} words (+{tok(added) / tok(base):.0%})")


if __name__ == "__main__":
    main()
