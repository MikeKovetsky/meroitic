"""Second cleanup, found by the blind grammar run: 21 short frames still came
in 21 copies each, because some swapped-in names were several words long.
Those multi-word names are masked in short texts (8 words or fewer) and exact
duplicates dropped. Writes data/corpus_v2.jsonl."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILLERS = ["pte oye", "apN blye", "mh witr", "mlitr ide", "mli tewen", "tNlxe aror", "msxte trobit",
           "Swe ibr", "x lonk", "dteqox qo", "beke mete", "kdi qebts", "a kye", "S qo ye", "qo eye",
           "li ye", "tqo mete l"]


# multi-word names that cannot be ordinary phrases: masked in every text
SAFE = FILLERS[:10]


def main():
    rows, seen = [], set()
    for r in map(json.loads, open(ROOT / "data/corpus.jsonl")):
        t = r["text"]
        if r["src"] == "funerary":
            padded = f" {t} "
            for f in sorted(SAFE, key=len, reverse=True):
                while f" {f} " in padded:
                    padded = padded.replace(f" {f} ", " NAME ")
            t = padded.strip()
        if r["src"] == "funerary" and len(t.split()) <= 8:
            padded = f" {t} "
            for f in sorted(FILLERS, key=len, reverse=True):
                padded = padded.replace(f" {f} ", " NAME ")
            t = padded.strip()
        if t in seen:
            continue
        seen.add(t)
        rows.append({**r, "text": t})
    with open(ROOT / "data/corpus_v2.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    words = [w for r in rows for w in r["text"].split()]
    print(f"texts {len(rows)}; tokens {len(words)}; types {len(set(words))}")


if __name__ == "__main__":
    main()
