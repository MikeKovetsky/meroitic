"""Build data/corpus.jsonl: the de-augmented funerary corpus plus the three
royal narratives, in one normalized ASCII spelling.

Spelling: o for Millet's E-hat; x = h (3rd h), X = h (4th h), N = n-tilde,
S = s-hat. Capitals that only mark an uncertain reading (dotted letters) are
lowered. Stars (doubtful signs), question marks, brackets and parentheses are
dropped and the letters they mark kept, so tk*k stays one word, tkk. A lost
sign or gap ([.], …) and the separators : , end a word. Where the editor gives
two readings, as in "lbr tbr (EITHER LBR OR TBR)", the first is kept.

Otten's mero-corpus.txt already holds the three narratives; those copies are
dropped, so each narrative is in the corpus once, from its own file.
"""
import difflib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/otten/Data"
NARRATIVES = {
    "hamadab": "HamadabStelaOfAmanirenasNarrative.txt",
    "tanyidamani": "TanyidamaniNarrative.txt",
    "kharamadoye": "KalabshaMeroiticInscriptionOfKharamadoyeNarrative.txt",
}
KEEP_CAPS = set("SXNE")
EITHER = re.compile(r"(\S+) (\S+) \(EIT[HX]ER-(\S+?)-OR-(\S+?)\)")


def first_reading(mo):
    """'lbr tbr (EITXER-LBR-OR-TBR)' is one word read two ways: keep the first."""
    a, b, x, y = mo.groups()
    return a if (a.lower(), b.lower()) == (x.lower(), y.lower()) else f"{a} {b}"


def norm(text):
    text = EITHER.sub(first_reading, text)
    text = re.sub(r"[*?\[\]()]", "", text)
    text = re.sub(r"[.,…:]", " ", text)
    text = "".join(c if (not c.isupper() or c in KEEP_CAPS) else c.lower() for c in text)
    text = text.replace("E", "o")
    return re.sub(r"\s+", " ", text).strip()


def same_text(a, b):
    """Two editions of one inscription: far more shared word order than any two texts share (< 0.06 here)."""
    return difflib.SequenceMatcher(None, a.split(), b.split(), autojunk=False).ratio() >= 0.3


def main():
    narratives = {}
    for key, fn in NARRATIVES.items():
        body = [l for l in (DATA / fn).read_text().split("\n") if l.strip() and not l.startswith("#")]
        narratives[key] = norm(" ".join(body))
    rows, dropped = [], []
    for r in map(json.loads, open(ROOT / "data/texts.jsonl")):
        t = norm(r["text"].replace("NAME", "\0").replace("R\0", "\1"))
        t = t.replace("\0", "NAME").replace("\1", "RNAME")
        if any(same_text(t, n) for n in narratives.values()):
            dropped.append(r["id"])
        elif t:
            rows.append({"id": r["id"], "src": "funerary", "copies": r["copies"], "text": t})
    rows += [{"id": key, "src": "narrative", "copies": 1, "text": t} for key, t in narratives.items()]
    with open(ROOT / "data/corpus.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    words = [w for r in rows for w in r["text"].split()]
    print(f"texts {len(rows)}; tokens {len(words)}; types {len(set(words))}; narrative copies dropped {dropped}")
    print("letters", "".join(sorted({c for w in words for c in w if not w.endswith('NAME')})))


if __name__ == "__main__":
    main()
