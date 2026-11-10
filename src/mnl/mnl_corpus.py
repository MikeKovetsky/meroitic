"""Write a local corpus that adds the new Newsletter texts to corpus_v3.

  python3 -I mnl_corpus.py <repo root> <mnl_texts.jsonl> <out corpus.jsonl>

Takes the rows marked new by mnl_dedupe.py (not in the corpus, not a second edition of another row, at least
one whole word). Names are not masked (no name list exists for these texts), so each row says src "mnl".
The result holds readings from articles still in copyright: it stays local, like the scans.
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mnl_signs as S  # noqa: E402


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    ROOT, TEXTS, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    S.need(ROOT / "data/corpus_v3.jsonl", TEXTS)
    sys.path.insert(0, str(ROOT / "src"))
    import expand as E
    base = [json.loads(l) for l in (ROOT / "data/corpus_v3.jsonl").read_text().splitlines()]
    rows = [json.loads(l) for l in TEXTS.read_text().splitlines()]
    if not all("new" in r for r in rows):
        sys.exit(f"{TEXTS} has rows without the field 'new': run mnl_dedupe.py on it first")
    added, seen = [], {r["id"] for r in base}
    for r in rows:
        if not r["new"]:
            continue
        ws = E.words(r["text_corpus"])
        issue = re.search(r"MeroNews(\w+)", r["file"]).group(1)
        slug = r["rem"] or re.sub(r"[^A-Za-z0-9]+", "-", r["id"]).strip("-")[:40]
        cid, k = f"N{issue}-{slug}", 2
        while cid in seen:
            cid = f"N{issue}-{slug}-{k}"
            k += 1
        seen.add(cid)
        added.append({"id": cid, "src": "mnl", "rem": r["rem"], "copies": 1, "text": " ".join(ws)})
    with open(OUT, "w") as f:
        for r in base + added:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tok = lambda rs: sum(len(r["text"].split()) for r in rs)
    print(f"corpus_v3 {len(base)} texts {tok(base)} words + {len(added)} Newsletter texts {tok(added)} words "
          f"= {len(base) + len(added)} texts {tok(base) + tok(added)} words (+{tok(added) / tok(base):.1%})")
    long = sorted(added, key=lambda r: -len(r["text"].split()))[:12]
    print("longest added:", [(r["id"], len(r["text"].split())) for r in long])


if __name__ == "__main__":
    main()
