"""Build data/corpus.jsonl: the de-augmented funerary corpus plus the three
royal narratives, in one normalized ASCII spelling.

Spelling: o for Millet's E-hat; x = h (3rd h), X = h (4th h), N = n-tilde,
S = s-hat. Capitals that only mark an uncertain reading (dotted letters) are
lowered. Brackets, stars and question marks are dropped.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/otten/Data"
NARRATIVES = {
    "hamadab": "HamadabStelaOfAmanirenasNarrative.txt",
    "tanyidamani": "TanyidamaniNarrative.txt",
    "kharamadoye": "KalabshaMeroiticInscriptionOfKharamadoyeNarrative.txt",
}
KEEP_CAPS = set("SXNE")


def norm(text):
    text = re.sub(r"[\[\]().*?,…:]", " ", text)
    text = "".join(c if (not c.isupper() or c in KEEP_CAPS) else c.lower() for c in text)
    text = text.replace("E", "o")
    return re.sub(r"\s+", " ", text).strip()


def main():
    rows = []
    for r in map(json.loads, open(ROOT / "data/texts.jsonl")):
        t = norm(r["text"].replace("NAME", "\0").replace("R\0", "\1"))
        t = t.replace("\0", "NAME").replace("\1", "RNAME")
        if t:
            rows.append({"id": r["id"], "src": "funerary", "copies": r["copies"], "text": t})
    for key, fn in NARRATIVES.items():
        body = [l for l in (DATA / fn).read_text().split("\n") if l.strip() and not l.startswith("#")]
        rows.append({"id": key, "src": "narrative", "copies": 1, "text": norm(" ".join(body))})
    with open(ROOT / "data/corpus.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    words = [w for r in rows for w in r["text"].split()]
    print(f"texts {len(rows)}; tokens {len(words)}; types {len(set(words))}")
    print("letters", "".join(sorted({c for w in words for c in w if not w.endswith('NAME')})))


if __name__ == "__main__":
    main()
