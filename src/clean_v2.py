"""Second cleanup, found by the blind grammar run: 21 short frames still came
in 21 copies each, because some swapped-in names were several words long.
Those multi-word names are masked as NAME: the first ten (which cannot be
ordinary phrases) in every funerary text, all of them in short texts (8 words
or fewer). Exact duplicates are then dropped, their copies added to the one
kept. Writes data/corpus_v2.jsonl."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILLERS = ["pte oye", "apN blye", "mh witr", "mlitr ide", "mli tewen", "tNlxe aror", "msxte trobit",
           "Swe ibr", "x lonk", "dteqox qo", "beke mete", "kdi qebts", "a kye", "S qo ye", "qo eye",
           "li ye", "tqo mete l"]
SAFE = FILLERS[:10]


def mask(text, names):
    """Every whole-word occurrence of each name, longest first, becomes NAME."""
    padded = f" {text} "
    for name in sorted(names, key=len, reverse=True):
        while f" {name} " in padded:
            padded = padded.replace(f" {name} ", " NAME ")
    return padded.strip()


def main():
    rows, kept = [], {}
    for r in map(json.loads, open(ROOT / "data/corpus.jsonl")):
        t = r["text"]
        if r["src"] == "funerary":
            t = mask(t, SAFE)
            if len(t.split()) <= 8:
                t = mask(t, FILLERS)
        if t in kept:
            kept[t]["copies"] += r["copies"]
            continue
        kept[t] = {**r, "text": t}
        rows.append(kept[t])
    with open(ROOT / "data/corpus_v2.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    words = [w for r in rows for w in r["text"].split()]
    print(f"texts {len(rows)}; tokens {len(words)}; types {len(set(words))}")


if __name__ == "__main__":
    main()
