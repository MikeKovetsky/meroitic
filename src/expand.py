"""Add the Griffith transcriptions to the corpus: data/corpus_v3.jsonl.

data/expansion/griffith_*.jsonl hold texts read from Griffith's printed type
(Meroitic Inscriptions I-II, 1911-12; Meroe, 1911), in the corpus spelling.
A Griffith text is dropped as already present when half or more of its word
trigrams occur in one corpus_v2 text. Griffith's names are not masked (no name
list exists for them), so each added row says src "griffith".

  python3 src/expand.py          # writes corpus_v3.jsonl and prints the gain
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def words(text):
    text = re.sub(r"\(\d+\)|\|", " ", text)          # Griffith's line numbers and type-line marks
    text = re.sub(r"[#?]", "", text)
    return [w for w in text.split() if w.strip(".")]


def trigrams(ws):
    return {tuple(ws[i:i + 3]) for i in range(len(ws) - 2)} or {tuple(ws)}


def load_griffith():
    rows = []
    for p in sorted((ROOT / "data/expansion").glob("griffith_*.jsonl")):
        for line in p.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                ws = words(r.get("text_corpus", ""))
                if ws:
                    rows.append({"id": f"G-{p.stem.split('_', 1)[1]}-{r.get('griffith_no')}", "src": "griffith",
                                 "rem": r.get("rem", ""), "copies": 1, "text": " ".join(ws)})
    return rows


def main():
    base = [json.loads(l) for l in open(ROOT / "data/corpus_v2.jsonl")]
    base_grams = [trigrams(r["text"].split()) for r in base]
    added, dupes = [], []
    for g in load_griffith():
        gg = trigrams(g["text"].split())
        best = max((len(gg & b) / len(gg) for b in base_grams), default=0)
        (dupes if best >= 0.5 else added).append(g)
    with open(ROOT / "data/corpus_v3.jsonl", "w") as f:
        for r in base + added:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tok = lambda rows: sum(len(r["text"].split()) for r in rows)
    print(f"griffith texts {len(added) + len(dupes)}: new {len(added)} ({tok(added)} words), "
          f"already present {len(dupes)} {[d['id'] for d in dupes]}")
    print(f"corpus_v2 {len(base)} texts {tok(base)} words -> corpus_v3 {len(base) + len(added)} texts "
          f"{tok(base) + tok(added)} words (+{tok(added) / tok(base):.0%})")


if __name__ == "__main__":
    main()
