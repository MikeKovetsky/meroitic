"""Rilly's 2003 lexicon (thesis vol. II, HAL tel-04793700) as a test set.

The extraction agents wrote data/rilly2003/lexique_*.jsonl, one entry per line.
This module merges them, maps Rilly's transliteration to the corpus spelling,
finds which glossed words occur in the corpus, and builds two blind tasks:

  R2_recall   open recall of every testable word, no corpus, no options
  N2_open_*   the words recall missed, to be worked out from the corpus

  python3 src/lexique.py stats            # merged counts, testable words
  python3 src/lexique.py build-recall     # writes the recall task (new folder only)
  python3 src/lexique.py build-open FILE  # writes the corpus tasks for the misses listed in FILE
"""
import collections, itertools, json, random, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEX = ROOT / "data/rilly2003"
CORPUS = ROOT / "data/corpus_v2.jsonl"
BLIND = Path("/private/tmp/claude-501/blind")
SEED = 31
NAMES = ("nom propre", "anthroponyme", "toponyme", "théonyme", "theonyme", "ethnonyme", "nom de personne",
         "nom de lieu", "nom divin", "divinité", "divinite")
GOOD = ("established", "probable")
REJECTED_FROM = 280
# grammatical words whose spelling a content word can't own (wi 'brother' vs the copula wi)
FUNCTION = {"wi", "lo", "li", "qo", "qe", "te", "se", "lw", "leb", "ke", "ye", "yi", "lis", "tel"}     # PDF page where the appendix of rejected glosses starts
GRAMMAR = ("suffixe", "préfixe", "prefixe", "morphème", "morpheme", "particule", "déterminant", "copule",
           "pronom", "postposition", "infixe")
SUFFIXES = ["", "l", "li", "lo", "lowi", "wi", "s", "se", "lis", "te", "tel", "teli", "leb", "lebkwi", "qo",
            "qowi", "i", "yi", "ye", "b", "bx", "ke", "kete", "kes", "lw", "w"]


def load():
    seen, out = set(), []
    for p in sorted(LEX.glob("lexique_*.jsonl")):
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            key = (e.get("headword", "").strip(), e.get("page_pdf"))
            if key in seen or not key[0]:
                continue
            seen.add(key)
            out.append(e)
    return out


def corpus_spellings(word):
    """Every corpus spelling a word in Rilly's transliteration could have.

    Corpus: o for o, x and X for the two h signs (ḫ, ẖ), S for the s sign,
    lowercase s for the se sign, N for the ne sign. Rilly writes se and ne for
    those signs, which can't be told from s+e and n+e, so both are tried.
    """
    w = word.lower()
    w = re.sub(r"[()?\[\]*.\s]", "", w).strip("-–:")
    w = w.replace("ḫ", "x").replace("h̭", "x").replace("ẖ", "X").replace("ḥ", "X")
    w = w.replace("ñ", "N").replace("š", "S").replace("ŝ", "s").replace("ê", "o").replace("ē", "e")
    w = re.sub(r"[^a-zA-Z]", "", w)
    if not w:
        return set()
    parts = re.split(r"(se|ne|s)", w)
    choices = []
    for p in parts:
        if p == "se":
            choices.append(["s", "Se"])
        elif p == "ne":
            choices.append(["N", "ne"])
        elif p == "s":
            choices.append(["S"])
        elif p:
            choices.append([p])
    return {"".join(c) for c in itertools.product(*choices)} if choices else set()


def corpus_index():
    rows = [json.loads(l) for l in open(CORPUS)]
    texts_with = collections.defaultdict(set)
    for r in rows:
        for tok in set(r["text"].split()):
            texts_with[tok].add(r["id"])
    return rows, texts_with


def occurrences(forms, texts_with):
    """Texts where a form occurs as a whole word, or (3+ letters) with a known ending."""
    hits = set()
    for f in forms:
        hits |= texts_with.get(f, set())
        if len(f) >= 3:
            for suf in SUFFIXES[1:]:
                hits |= texts_with.get(f + suf, set())
    return hits


def testable(entries, texts_with, min_texts=2):
    """Glossed (established or probable) content words that occur in 2+ texts.

    Left out: names (Rilly capitalises them), gods, endings and particles, the
    rejected-glosses appendix, one-letter spellings, and homonyms whose corpus
    spellings collide with another testable word (the key would be ambiguous).
    """
    out = []
    for e in entries:
        if e["headword"].lstrip("*-– ")[:1].isupper():
            continue
        cat = (e.get("category") or "").lower()
        if not e.get("meaning_en") or e.get("status") not in GOOD or any(n in cat for n in NAMES):
            continue
        if e["headword"].lstrip().startswith(("-", "–")) or any(g in cat for g in GRAMMAR):
            continue    # endings and particles: a grammar question, tested separately
        if (e.get("page_pdf") or 0) >= REJECTED_FROM:
            continue    # the appendix of glosses Rilly rejects ("Gloses non retenues")
        forms = set()
        for hw in [e["headword"]] + list(e.get("variants") or []):
            forms |= corpus_spellings(hw)
        forms = {f for f in forms if len(f) >= 2 and f not in FUNCTION}
        if not forms or re.search(r"\b(variant|var\.|see |cf\.)", e["meaning_en"].strip().lower()):
            continue    # a cross-reference is not a meaning
        hits = occurrences(forms, texts_with)
        if len(hits) >= min_texts:
            out.append({"word": e["headword"], "meaning": e["meaning_en"], "status": e["status"],
                        "category": e.get("category", ""), "forms": sorted(forms), "texts": len(hits),
                        "page": e.get("page_pdf")})
    owners = collections.Counter(f for i in out for f in i["forms"])
    return [i for i in out if all(owners[f] == 1 for f in i["forms"])]


RECALL = """# Task: Meroitic vocabulary from memory

Below are {n} words of Meroitic, the language of ancient Kush (Sudan), in the standard scholarly transliteration (Hintze/Rilly).

For each word, write what it means, from your own knowledge only. If you do not know, write "unknown". A confident wrong answer is worse than "unknown". Work only from this file and your memory: do not use web search or fetch any page, and do not read any other file.

Write JSON to `{out}` (and repeat a short summary in your final message):

{{"answers": [{{"word": "...", "meaning": "... or unknown", "confidence": 1}}]}}

confidence is 1 (vague) to 5 (sure).

Words:
{words}
"""

OPEN = """# Task: work out what these Meroitic words mean, from the texts

Below is a corpus of Meroitic inscriptions (ancient Kush), one text per line, in an ASCII transliteration: o for o, x and X for the two h signs, S for the s sign, lowercase s for the se sign, N for the ne sign. Person names are masked as NAME (royal names as RNAME). Digits are numerals. Some texts are near-copies of one inscription; count texts, not tokens.

The glossary gives words whose meanings are known. For each of the {n} target words (given in the standard transliteration, with the spellings to look for in the corpus), propose what it means from the evidence in the corpus: where it occurs, what it occurs with, its endings, the glossary words around it, parallel passages. Give your three best candidate meanings, best first, each a short English gloss, with the evidence for the first one and a confidence 1 to 5 (5: the texts force it; 4: strong evidence, one clear reading; 3: plausible; 2: weak; 1: guess). Also say, separately, whether you remember a published meaning for the word (field "recalled").

Work only from this file and your own reasoning: do not use web search or fetch any page, and do not read any other file. You may run code (for example Python) that reads only this file.

Write JSON to `{out}` (and repeat a short summary in your final message):

{{"answers": [{{"word": "...", "candidates": ["best", "second", "third"], "confidence": 1, "evidence": "...", "recalled": "..."}}]}}

## Target words

{targets}

## Glossary (known words)

{glossary}

## Corpus

{corpus}
"""


def fresh(d):
    if (d / "task.md").exists():
        sys.exit(f"{d} already holds a task; refusing to overwrite a run")
    d.mkdir(parents=True, exist_ok=True)


def build_recall(items):
    d = BLIND / "R2_recall"
    fresh(d)
    words = [i["word"] for i in items]
    random.Random(SEED).shuffle(words)
    (d / "task.md").write_text(RECALL.format(n=len(words), out=d / "answer.json",
                                             words="\n".join(f"- {w}" for w in words)))
    json.dump(items, open(ROOT / "runs/keys/lexique_items.json", "w"), indent=1, ensure_ascii=False)
    print("wrote", d / "task.md", len(words), "words")


def build_open(items, missed, parts=2):
    rows, _ = corpus_index()
    rng = random.Random(SEED)
    rng.shuffle(rows)
    corpus = "\n".join(f"L{i:04d}: {r['text']}" for i, r in enumerate(rows))
    targets = [i for i in items if i["word"] in missed]
    known = [i for i in items if i["word"] not in missed]
    glossary = "\n".join(f"- {i['word']} ({', '.join(i['forms'][:3])}): {i['meaning']}" for i in known)
    rng.shuffle(targets)
    chunks = [targets[k::parts] for k in range(parts)]
    for k, chunk in enumerate(chunks):
        d = BLIND / f"N2_open_{k + 1}"
        fresh(d)
        tl = "\n".join(f"- {t['word']} (look for: {', '.join(t['forms'][:4])})" for t in chunk)
        (d / "task.md").write_text(OPEN.format(n=len(chunk), out=d / "answer.json", targets=tl,
                                               glossary=glossary, corpus=corpus))
        print("wrote", d / "task.md", len(chunk), "targets")
    json.dump({t["word"]: t["meaning"] for t in targets}, open(ROOT / "runs/keys/lexique_open.json", "w"),
              indent=1, ensure_ascii=False)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    entries = load()
    _, texts_with = corpus_index()
    items = testable(entries, texts_with)
    if cmd == "stats":
        c = collections.Counter(e.get("status") for e in entries)
        print(f"entries {len(entries)}; status {dict(c)}; testable (glossed, not a name, in 2+ texts) {len(items)}")
        for i in items[:15]:
            print(f"  {i['word']:14} {i['texts']:3} texts  {i['meaning'][:60]}")
    elif cmd == "build-recall":
        build_recall(items)
    elif cmd == "build-open":
        missed = set(json.load(open(sys.argv[2])))
        build_open(items, missed)
