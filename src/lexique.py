"""Rilly's 2003 lexicon (thesis vol. II, HAL tel-04793700) as a test set.

The extraction agents wrote data/rilly2003/lexique_*.jsonl, one entry per line.
This module merges them, maps Rilly's transliteration to the corpus spelling,
finds which glossed words occur in the corpus, and builds two blind tasks:

  R2_recall   open recall of every testable word, no corpus, no options
  N2_open_*   the words recall missed, to be worked out from the corpus

  python3 src/lexique.py stats            # merged counts, testable words
  python3 src/lexique.py build-recall     # writes the recall task (new folder only)
  python3 src/lexique.py build-open FILE  # writes the corpus tasks for the misses listed in FILE
  python3 src/lexique.py judged           # the judged run's totals, as judged and without the words it should not have had

The judged run of 2026-11-09 (runs/tasks/R2_recall.md, N2_open_*.md, local-only) was built by this file as of
commit 364d792. Fixed since: three of its 68 words are not test words (yer and nobo occur in one text each once
another entry's words are not counted as theirs; qoleb is a demonstrative), two were wrongly left out (ntki, qor),
and the corpus tasks' glossary gave six targets away (mk "very probably goddess" for mkdi; qore for qorise, qor-o,
qorene, qorode; mlo for smlo). `judged` prints the totals both ways. The builders refuse to replace a task or a
key that a run is scored against.

Rilly's lexicon is not in the public repo (README, Data): without data/rilly2003/ every command stops.
"""
import collections, itertools, json, random, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEX = ROOT / "data/rilly2003"
CORPUS = ROOT / "data/corpus_v2.jsonl"
BLIND = Path("/private/tmp/claude-501/blind")
SEED = 31
NAMES = ("nom propre", "anthroponyme", "toponyme", "théonyme", "theonyme", "ethnonyme", "nom de personne",
         "nom de lieu", "nom divin", "divinité", "divinite")
GOOD = ("established", "probable")
REJECTED_FROM = 280     # PDF page where the appendix of rejected glosses starts
# grammatical words whose spelling a content word can't own (wi 'brother' vs the copula wi)
FUNCTION = {"wi", "lo", "li", "qo", "qe", "te", "se", "lw", "leb", "ke", "ye", "yi", "lis", "tel"}
GRAMMAR = ("suffixe", "préfixe", "prefixe", "morphème", "morpheme", "particule", "déterminant", "copule",
           "pronom", "postposition", "infixe", "démonstratif", "demonstratif", "conjonction", "prédicatif",
           "predicatif", "possessif")
# a meaning that only sends to another entry ("variant of ato", "see peseto"); "not a mere variant" is not one
XREF = re.compile(r"^(see\b|cf\.)|(?<!not a )(?<!mere )\bvariants?\b|\bvar\.")
SUFFIXES = ["", "l", "li", "lo", "lowi", "wi", "s", "se", "lis", "te", "tel", "teli", "leb", "lebkwi", "qo",
            "qowi", "i", "yi", "ye", "b", "bx", "ke", "kete", "kes", "lw", "w"]
# a letter with a mark that the corpus spells as another letter, as NFD decomposes it: ḫ (and the look-alike
# h̭), ẖ (precomposed only in lowercase), ḥ, š, ŝ, ñ, ê. Any other mark goes: a dotted letter is an uncertain
# reading of that letter.
MARKS = {"ḫ": "x", "h̭": "x", "ẖ": "X", "ḥ": "X", "š": "S", "ŝ": "s",
         "ñ": "N", "ê": "o"}


def load():
    files = sorted(LEX.glob("lexique_*.jsonl"))
    if not files:
        sys.exit(f"no lexique_*.jsonl in {LEX}: Rilly's lexicon is kept locally, not in the public repo (README, Data)")
    seen, out = set(), []
    for p in files:
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
    A dotted letter (an uncertain reading) is that letter. Brackets after a
    space hold a note ("(2)", "(?)", "(arch.)"); letters in brackets inside a
    word are optional (ḫbḫl(i)). A spelling with lost signs ([.], [ca. 2], a
    dot) has none.
    """
    w = re.sub(r"\s+\([^)]*\)", " ", unicodedata.normalize("NFD", word)).lower()
    if re.search(r"[.…]", w):
        return set()
    for mark, letter in MARKS.items():
        w = w.replace(mark, letter)
    w = "".join(c for c in w if not unicodedata.combining(c))
    parts = re.split(r"\(([a-z]+)\)", w)
    out = set()
    for keep in itertools.product((False, True), repeat=len(parts) // 2):
        out |= signs("".join(p for k, p in enumerate(parts) if k % 2 == 0 or keep[k // 2]))
    return out


def signs(w):
    """The corpus spellings of one reading: se and ne as their signs or as s+e and n+e."""
    choices = []
    for p in re.split(r"(se|ne|s)", re.sub(r"[^a-zA-Z]", "", w)):
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
    rows = [json.loads(l) for l in CORPUS.read_text().splitlines()]
    texts_with = collections.defaultdict(set)
    for r in rows:
        for tok in set(r["text"].split()):
            texts_with[tok].add(r["id"])
    return rows, texts_with


def occurrences(forms, texts_with, taken=frozenset()):
    """Texts where a form occurs as a whole word, or (3+ letters) with a known ending.

    A word in taken (another entry's own spelling) counts for that entry, not as
    the form plus an ending: yeri + ke is yerike 'begotten', not yer 'milk'.
    """
    hits = set()
    for f in forms:
        hits |= texts_with.get(f, set())
        if len(f) >= 3:
            for suf in SUFFIXES[1:]:
                if f + suf not in taken:
                    hits |= texts_with.get(f + suf, set())
    return hits


def testable(entries, texts_with, min_texts=2):
    """Glossed (established or probable) content words that occur in 2+ texts.

    Left out: names (Rilly capitalises them), gods, endings, particles and other
    grammatical words, the rejected-glosses appendix, entries that only send to
    another (a variant, "see ..."), one-letter spellings, and homonyms whose
    corpus spellings collide with another testable word (the key would be
    ambiguous). Occurrences: see occurrences(); a word is taken when another
    entry of the lexicon proper has it as a spelling.
    """
    forms_of = [set().union(*(corpus_spellings(h) for h in [e["headword"]] + list(e.get("variants") or [])))
                for e in entries]
    owner = collections.defaultdict(set)
    for k, e in enumerate(entries):
        if (e.get("page_pdf") or 0) < REJECTED_FROM:
            for f in forms_of[k]:
                owner[f].add(k)
    out = []
    for k, e in enumerate(entries):
        if e["headword"].lstrip("*-– ")[:1].isupper():
            continue
        cat = (e.get("category") or "").lower()
        if not e.get("meaning_en") or e.get("status") not in GOOD or any(n in cat for n in NAMES):
            continue
        if e["headword"].lstrip().startswith(("-", "–")) or any(g in cat for g in GRAMMAR):
            continue    # endings and particles: a grammar question, tested separately
        if (e.get("page_pdf") or 0) >= REJECTED_FROM:
            continue    # the appendix of glosses Rilly rejects ("Gloses non retenues")
        forms = {f for f in forms_of[k] if len(f) >= 2 and f not in FUNCTION}
        if not forms or XREF.search(e["meaning_en"].strip().lower()):
            continue    # a cross-reference is not a meaning
        ends = {f + s for f in forms if len(f) >= 3 for s in SUFFIXES[1:]}
        hits = occurrences(forms, texts_with, {w for w in ends if owner.get(w, set()) - {k}})
        if len(hits) >= min_texts:
            out.append({"word": e["headword"], "meaning": e["meaning_en"], "status": e["status"],
                        "category": e.get("category", ""), "forms": sorted(forms), "texts": len(hits),
                        "page": e.get("page_pdf")})
    owners = collections.Counter(f for i in out for f in i["forms"])
    return [i for i in out if all(owners[f] == 1 for f in i["forms"])]


def related(known, target):
    """A glossary word that gives a target away: one's corpus spelling begins the
    other's (mk, mkdi; qore, qorise), the glossary's meaning names the target
    (nobo "qore nobo 'Nubian king'" gives qore away), or the target's meaning,
    which the task does not show, names the glossary word and their spellings
    share three letters (qore, qor-o; mlo, smlo; not qore, nobo "slave of the qore")."""
    def names(x, y):
        return re.sub(r"\s*\(\d+\)$", "", y["word"]).lower() in re.findall(r"[\w-]+", x["meaning"].lower())
    pairs = [(f, g) for f in known["forms"] for g in target["forms"]]
    if any(f.startswith(g) or g.startswith(f) for f, g in pairs) or names(known, target):
        return True
    return names(target, known) and any(f[i:i + 3] in g for f, g in pairs for i in range(len(f) - 2))


def shown(item, texts_with, n):
    """The spellings a task shows for a word: those in the corpus first, in most texts first."""
    return sorted(item["forms"], key=lambda f: -len(occurrences({f}, texts_with)))[:n]


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


def fresh(dirs, key, data):
    """Refuse, before writing anything, a folder that holds a task or a saved key with other contents: a run is
    scored against both, and the blind folders go when /private/tmp is emptied, the keys in runs/keys/ don't."""
    taken = [str(d) for d in dirs if (d / "task.md").exists()]
    if taken:
        sys.exit(f"{', '.join(taken)} already holds a task; refusing to overwrite a run")
    if key.exists() and json.loads(key.read_text()) != data:
        sys.exit(f"{key} differs from this build; refusing to overwrite the key a run is scored against")
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def build_recall(items):
    d, key = BLIND / "R2_recall", ROOT / "runs/keys/lexique_items.json"
    fresh([d], key, items)
    words = [i["word"] for i in items]
    random.Random(SEED).shuffle(words)
    (d / "task.md").write_text(RECALL.format(n=len(words), out=d / "answer.json",
                                             words="\n".join(f"- {w}" for w in words)))
    json.dump(items, open(key, "w"), indent=1, ensure_ascii=False)
    print("wrote", d / "task.md", len(words), "words")


def build_open(items, missed, parts=2):
    rows, texts_with = corpus_index()
    rng = random.Random(SEED)
    rng.shuffle(rows)
    corpus = "\n".join(f"L{i:04d}: {r['text']}" for i, r in enumerate(rows))
    targets = [i for i in items if i["word"] in missed]
    known = [i for i in items if i["word"] not in missed]
    gave = sorted({k["word"] for k in known for t in targets if related(k, t)})
    glossary = "\n".join(f"- {i['word']} ({', '.join(shown(i, texts_with, 3))}): {i['meaning']}"
                         for i in known if i["word"] not in gave)
    rng.shuffle(targets)
    chunks = [targets[k::parts] for k in range(parts)]
    dirs, key = [BLIND / f"N2_open_{k + 1}" for k in range(parts)], ROOT / "runs/keys/lexique_open.json"
    answers = {t["word"]: t["meaning"] for t in targets}
    fresh(dirs, key, answers)
    for d, chunk in zip(dirs, chunks):
        tl = "\n".join(f"- {t['word']} (look for: {', '.join(shown(t, texts_with, 4))})" for t in chunk)
        (d / "task.md").write_text(OPEN.format(n=len(chunk), out=d / "answer.json", targets=tl,
                                               glossary=glossary, corpus=corpus))
        print("wrote", d / "task.md", len(chunk), "targets")
    print("left out of the glossary, as they give a target away:", ", ".join(gave) or "none")
    json.dump(answers, open(key, "w"), indent=1, ensure_ascii=False)


ALT = re.compile(r"\b(SAME|TYPE|WRONG)(?: \([^)]*\))? if\b")


def alt(r):
    """The verdict a borderline judge row names for the other reading ("TYPE if ..."), or None."""
    m = ALT.search(r["why"]) if r["why"].startswith("Borderline") else None
    return m[1] if m else None


def totals(judge, drop=()):
    """The totals block of runs/lexique_judge.json, recomputed from its rows, without the words in drop.

    Borderline rows (their why starts "Borderline") set the ranges: a SAME that
    names another verdict can go down, a non-SAME that names SAME can go up, and
    "Borderline any_same" doubts any_same only. Word lists come back sorted.
    """
    rec = [r for r in judge["recall"] if r["word"] not in drop]
    cor = [r for r in judge["corpus"] if r["word"] not in drop]
    v = collections.Counter(r["verdict"] for r in rec)
    f = collections.Counter(r["verdict_first"] for r in cor)
    anys = sum(r["any_same"] for r in cor)
    rb = [r for r in rec if r["why"].startswith("Borderline")]
    cb = [r for r in cor if r["why"].startswith("Borderline")]
    down = lambda rows, key: sum(r[key] == "SAME" and alt(r) not in (None, "SAME") for r in rows)
    up = lambda rows, key: sum(r[key] != "SAME" and alt(r) == "SAME" for r in rows)
    any_down = down(cb, "verdict_first") + sum(r["any_same"] and r["why"].startswith("Borderline any_same")
                                               for r in cb)
    any_up = sum(not r["any_same"] and alt(r) == "SAME" for r in cb)
    hi, lo = [r for r in rec if r["confidence"] >= 4], [r for r in rec if r["confidence"] <= 3]
    by = {"4-5": [r for r in cor if r["confidence"] >= 4], "3": [r for r in cor if r["confidence"] == 3],
          "1-2": [r for r in cor if r["confidence"] <= 2]}
    return {
        "recall": {"n": len(rec), **{k: v[k] for k in ("SAME", "TYPE", "WRONG", "UNKNOWN")}},
        "recall_same_by_confidence": {
            "4-5": {"SAME": sum(r["verdict"] == "SAME" for r in hi),
                    "answers": sum(r["verdict"] != "UNKNOWN" for r in hi)},
            "1-3": {"SAME": sum(r["verdict"] == "SAME" for r in lo),
                    "answers": sum(r["verdict"] != "UNKNOWN" for r in lo), "answers_with_unknown": len(lo)}},
        "corpus_first": {"n": len(cor), **{k: f[k] for k in ("SAME", "TYPE", "WRONG")}},
        "corpus_any_same": {"count": anys, "n": len(cor)},
        "corpus_same_by_confidence": {k: {"SAME": sum(r["verdict_first"] == "SAME" for r in rows),
                                          "answers": len(rows)} for k, rows in by.items()},
        "borderline": {"recall_words": sorted(r["word"] for r in rb),
                       "corpus_words": sorted(r["word"] for r in cb),
                       "recall_SAME_range": [v["SAME"] - down(rb, "verdict"), v["SAME"] + up(rb, "verdict")],
                       "corpus_first_SAME_range": [f["SAME"] - down(cb, "verdict_first"),
                                                   f["SAME"] + up(cb, "verdict_first")],
                       "corpus_any_same_range": [anys - any_down, anys + any_up]}}


def judged(entries, texts_with):
    """The judged run's totals, and without the words it should not have had.

    Not test words: the run's words that testable() leaves out now. Given away:
    the corpus targets related() to a word the run's glossary showed.
    """
    judge = json.load(open(ROOT / "runs/lexique_judge.json"))
    ran = json.load(open(ROOT / "runs/keys/lexique_items.json"))
    missed = set(json.load(open(ROOT / "runs/keys/lexique_missed.json")))
    now = {i["word"] for i in testable(entries, texts_with)}
    wrong = sorted({i["word"] for i in ran} - now)
    known = [i for i in ran if i["word"] not in missed]
    gave = sorted({t["word"] for t in ran if t["word"] in missed for k in known if related(k, t)})
    added = sorted(now - {i["word"] for i in ran})
    for name, rt, ct in [("as judged", totals(judge), totals(judge)),
                         ("fair", totals(judge, wrong), totals(judge, set(wrong) | set(gave)))]:
        r, b = rt["recall"], rt["borderline"]
        cf, ca, cb = ct["corpus_first"], ct["corpus_any_same"], ct["borderline"]
        print(f"{name:10} recall SAME {r['SAME']}/{r['n']} (borderline {b['recall_SAME_range'][0]}-"
              f"{b['recall_SAME_range'][1]}); corpus first SAME {cf['SAME']}/{cf['n']} "
              f"({cb['corpus_first_SAME_range'][0]}-{cb['corpus_first_SAME_range'][1]}), any SAME "
              f"{ca['count']}/{ca['n']} ({cb['corpus_any_same_range'][0]}-{cb['corpus_any_same_range'][1]})")
    print("not test words:", ", ".join(wrong) or "none")
    print("corpus targets the glossary gave away:", ", ".join(gave) or "none")
    print("test words the run left out:", ", ".join(added) or "none")
    return wrong, gave, added


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    entries = load()
    _, texts_with = corpus_index()
    if cmd == "judged":
        judged(entries, texts_with)
        sys.exit()
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
