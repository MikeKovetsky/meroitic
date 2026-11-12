"""The meanings the experts give in entries we do not hold (answers/extractor.jsonl), set beside our map.

  python3 -I src/experts/missing.py

Each word is put into our corpus spelling and looked up the way the coverage map looks a word up (src/coverage.py,
lookup with the corrections' rule for stems of two signs), then among the words of the corrected map. Writes
extractor_checked.tsv, and missing_grouped.tsv: the words of the held texts that our map does not translate and
the expert gives a meaning (from tally.py's missing_meanings.tsv: "new", and "agree", "partly" or "differ" on a
word the map holds only as a hypothesis or a kind), one line per word. Local only; the reader's list is untrusted
data: only its six fields are read.
"""
import collections
import csv
import itertools
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import coverage as C                                   # noqa: E402

FOLDER = ROOT / "data/sources/expert"
GLOSSES = ROOT / "data/sources/coverage/corrected/glosses.jsonl"
TRANSLATED = C.TRANSLATED


def spellings(word, source=""):
    """The corpus spellings an expert's word may stand for. Both editions write the sign se as "se", the sign ne
    as "ne" or ñ, and Millet writes ḫ as x and ẖ as h; the OCR of FHN has lost the marks on h, so each h may be
    either. Our corpus writes ẖ as X, ḫ as x, and in a few words ẖ as a plain h."""
    w = re.sub(r"[^a-zñ]", "", word.lower().replace("fi", "ñ"))
    w = w.replace("se", "\x01").replace("s", "S").replace("\x01", "s").replace("ne", "N").replace("ñ", "N")
    spots = [i for i, c in enumerate(w) if c == "h"]
    out = []
    signs = "Xh" if source.startswith("Millet") else "Xxh"
    for choice in itertools.product(signs, repeat=min(len(spots), 4)):
        v = list(w)
        for i, c in zip(spots, choice):
            v[i] = c
        out.append("".join(v))
    return out or [w]


def status(word, words, affixes, in_map, source=""):
    """(how our map holds the word, its reading there): looked up as the map does, else found among the map's
    words, else not held. The best of the possible spellings counts."""
    best = ("not in the map", "")
    for tok in spellings(word, source):
        g = C.lookup(tok, None, words, affixes, two_signs=True) if tok else None
        if g is None and tok in in_map:
            g = in_map[tok]
        if g is None:
            continue
        if g["level"] in TRANSLATED:
            return ("translated", g["gloss"])
        if best[0] == "not in the map":
            best = (f"held without an accepted meaning ({g['level']})", g.get("gloss") or "")
    return best


KINDS = (                              # the first that fits the expert's meaning, as the judge wrote it
    ("a piece of another word", r"\b(part of|end of|ending of|beginning of|first letter|initial of)\b"),
    ("a personal name", r"\bnames?\b|\ba king\b"),   # "of the king" is a word
    ("a place or a people", r"^(in|of|from) [A-Z]|\bplace\b|\bethnic\b|-land\b|^[A-Z]\w+ \([A-Z]"),
)
STOP = {"with", "from", "that", "this", "them", "they", "their", "having", "been", "some", "while", "perhaps",
        "probably", "person", "title", "word", "part", "name", "personal", "expression", "being", "were", "what"}


def kind_of(meaning):
    """The kind of thing the expert takes the word for: the first of KINDS whose pattern fits the meaning, else a
    word."""
    return next((kind for kind, pattern in KINDS if re.search(pattern, meaning)), "a word")


def alike(meaning, by_word):
    """Translated words of our map whose reading shares a word of four letters or more with the expert's
    meaning: where to look for the same meaning under another spelling. At most four, the most frequent first."""
    keys = {w for w in re.findall(r"[a-z]{4,}", meaning.lower()) if w not in STOP}
    found = [(n, form, gloss) for form, (gloss, n) in by_word.items()
             if keys & set(re.findall(r"[a-z]{4,}", gloss.lower()))]
    return "; ".join(f"{form} = {gloss[:40]}" for _, form, gloss in sorted(found, reverse=True)[:4])


def judged(by_word, path=None):
    """The words our map does not translate to which a judge found the expert giving a meaning (every row of
    missing_meanings.tsv), one line per word, with the judges' verdicts and the kind of thing the expert takes it
    for."""
    path = path or FOLDER / "missing_meanings.tsv"
    rows = list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))
    groups = {}
    for r in rows:
        groups.setdefault(r["word"], []).append(r)
    out = []
    for word, rs in groups.items():
        seconds = [x.partition(": ")[2] for r in rs for x in r.get("second judge", "").split("; ")
                   if x.partition(": ")[0] in ("agree", "partly", "differ", "new")]
        meanings = sorted({m for m in [r["the expert's meaning"] for r in rs] + seconds if m})
        verdicts = collections.Counter(r["verdict"] for r in rs if r["verdict"])
        meaning = "; ".join(meanings)
        kind = kind_of(meaning)
        out.append({"word": word, "kind": kind, "verdicts": ", ".join(f"{v} {n}" for v, n in sorted(verdicts.items())),
                    "the expert's meaning": meaning[:160],
                    "expert unsure": "yes" if any(r["expert unsure"] for r in rs) else "",
                    "places": len(rs), "entries": ", ".join(sorted({f"{r['source']} {r['entry']}" for r in rs})),
                    "our map": ", ".join(sorted({r["level"] for r in rs})),
                    "our reading": " / ".join(sorted({r["our reading"] for r in rs}))[:80],
                    "translated words of our map with a like meaning": alike(meaning, by_word) if kind == "a word" else ""})
    return sorted(out, key=lambda r: (r["kind"] != "a word", r["kind"], -r["places"], r["word"]))


def worst_of(states):
    """How the map holds a phrase of several words: not in the map if a part is not, else the first part held
    without an accepted meaning, else translated. A phrase without letters is not in the map."""
    if not states or "not in the map" in states:
        return "not in the map"
    return next((h for h in states if h != "translated"), "translated")


def held(word, source, m):
    """(how our map holds a word or a phrase, our reading of it): each part looked up by status(), the phrase
    held as worst_of() its parts, the readings with " / " between them. m = (words, affixes, in_map)."""
    parts = [p for p in re.split(r"\s+", word.strip()) if re.sub(r"[^A-Za-zñ]", "", p)]
    states = [status(p.strip("-"), *m, source) for p in parts]
    return worst_of([s[0] for s in states]), " / ".join(s[1] for s in states)[:160]


def our_map(path=GLOSSES):
    """(words, affixes, in_map, seen): the lexicon's index as src/coverage.py builds it, the corrected map's words
    (each form with a translated reading where the map has one) and how often the map translates each form."""
    words, affixes, _ = C.index(C.lexicon())
    in_map, seen = {}, collections.Counter()
    for line in path.open(encoding="utf-8"):
        for g in json.loads(line)["glosses"]:
            if g["form"] not in in_map or g["level"] in TRANSLATED:
                in_map[g["form"]] = g
            seen[g["form"]] += g["level"] in TRANSLATED
    return words, affixes, in_map, seen


def main():
    words, affixes, in_map, seen = our_map()
    out = []
    for line in (FOLDER / "answers/extractor.jsonl").read_text(encoding="utf-8").splitlines():
        try:
            a = json.loads(line)
            word, meaning = str(a["word"]), str(a["meaning"])
        except (ValueError, KeyError, TypeError):
            continue
        state, reading = held(word, str(a.get("source", "")), (words, affixes, in_map))
        out.append({"source": str(a.get("source", "")), "entry": str(a.get("entry", "")), "word": word,
                    "the expert's meaning": meaning[:120], "expert unsure": "yes" if a.get("doubt") is True else "",
                    "our map": state, "our reading": reading})
    with (FOLDER / "extractor_checked.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    by_word = {}
    for form, g in in_map.items():
        if g["level"] in TRANSLATED and g.get("gloss"):
            by_word[form] = (g["gloss"], seen[form])          # how often the map translates the form
    grouped = judged(by_word)
    with (FOLDER / "missing_grouped.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(grouped[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(grouped)
    tally = {}
    for r in grouped:
        tally[r["kind"]] = tally.get(r["kind"], 0) + 1
    print(len(grouped), "words of the held texts with a meaning from the expert and none in our map;", tally,
          "| of them judged new:", sum("new" in r["verdicts"] for r in grouped))
    for r in grouped:
        if r["kind"] == "a word":
            meaning, like = r["the expert's meaning"][:48], r["translated words of our map with a like meaning"][:70]
            print(f"  {r['word'][:22]:22} {'?' if r['expert unsure'] else ' '} {meaning:48} | "
                  f"{r['entries'][:24]:24} | like: {like}")
    print()
    kinds = {}
    for r in out:
        kinds[r["our map"]] = kinds.get(r["our map"], 0) + 1
    print(len(out), "meanings;", kinds)
    for r in out:
        if r["our map"] != "translated":
            meaning = r["the expert's meaning"][:44]
            print(f"  {r['source'][:6]} {r['entry'][:9]:9} {r['word'][:24]:24} {'?' if r['expert unsure'] else ' '} "
                  f"{meaning:44} | {r['our map'][:40]} | {r['our reading'][:50]}")


if __name__ == "__main__":
    main()
