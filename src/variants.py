"""Spellings and forms of known words among the pieces without a meaning: a search inside the lexicon.

  python3 -I src/variants.py first     the pool, the listed variants and the endings as the search sees them
  python3 -I src/variants.py build     the test on the hidden variants, the comparison words and the search; writes
                                       the local result files and the public list
  python3 -I src/variants.py sample    the check on the test's one shortcut: for 30 hidden variants, the made-up
                                       words searched as the variant itself was (about six minutes)
  python3 -I src/variants.py check     the checkers' packs: every match that beats the bar, and unmarked items
                                       whose answer is known
  python3 -I src/variants.py merge     the checkers' answers against the key; the confirmed list, and the words
                                       it would move in the coverage map

The question (NEXT_STEPS.md, E 21): which pieces of the coverage map's list of words without a meaning
(data/discovery/coverage_unknown.tsv) are a spelling, or a form with an ending, of a word that Rilly's 2003 lexicon
already has? The search knows letters only, as the search for Egyptian words did (src/egyptian.py), and uses its
model, its trie search, its made-up words and its checkers' pack (data/discovery/variants.md).

1. The pool. The entries of the lexicon proper that are words, not endings or prefixes: an ending is too short
   to search for, and a word's level does not hang on its endings. Entries whose headwords have the same letters
   (tk (1) to tk (4)) are one match, since letters cannot tell them apart. A match holds the letter strings of
   its headwords and of the variants Rilly lists under them, vowels included.
2. The model. An entry's spelling becomes another spelling letter by letter: a letter stays, changes or drops,
   and a letter may be added. The starting table is flat (flat()): it holds no groups of like letters and no
   weak letters, so which letters alternate comes from the counts alone, taken from the variants that the
   lexicon lists (the 307 not spelled like their headword, those of endings included) aligned with their
   headwords.
3. Endings. A piece may be an entry with one of the endings of lexique.SUFFIXES. Every word is read from its
   end, so that an ending comes first and is taken as the Egyptian search takes an article. How often each ending
   stands is counted on the corpus words that the coverage map's lookup explains, not on the variants, which the
   lexicon lists bare.
4. The test. Each listed variant of a word is hidden in turn: struck from every variant list, and every entry
   that has it as its headword goes (the lexicon often gives a variant an entry of its own). The model is
   trained on the rest, and the search should bring the variant back to an entry that lists it, as its single
   best match. The bar (FOUND, STANDS_OUT) was set before the first run.
5. Chance. A best match counts only as far as it beats the best matches of made-up words of the same length. The
   words with an accepted meaning that the lexicon calls a variant of nothing go through the same search, to see
   what the made-up words are worth as a yardstick.
6. The check. Every piece whose best match beats the bar goes to two checkers, mixed with two kinds of unmarked
   items whose answer is known. Both are listed variants shown as if they were pieces, with the candidates the
   search gave when they were hidden: a control keeps them all, a decoy has the entry that lists it taken out,
   so that only look-alikes are left.

The lexicon, the gloss file and the result files are local (data/sources/variants/). The public files are the
page, the brief, the list of every searched piece with its best match (forms, no gloss) and the confirmed list.
"""
import collections, csv, hashlib, json, math, random, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import lexique as L    # noqa: E402
import coverage as C   # noqa: E402
import egyptian as E   # noqa: E402

HERE = ROOT / "data/sources/variants"                       # local only
OUT = HERE / "out"
CHECK = HERE / "check"
KEYFILE = HERE / "check_key.json"
PUBLIC = ROOT / "data/discovery/variants_candidates.tsv"
CONFIRMED = ROOT / "data/discovery/variants_confirmed.tsv"
BRIEF = ROOT / "data/discovery/variants_brief.md"

LETTERS = E.MER + E.VOWELS_M  # both sides are Meroitic: the consonants, 0 for a vowel at the start, and e, i, o
SHORTEST = E.SHORTEST         # a word with fewer letters is not searched: anything fits it
LONGEST = E.VOWEL_LONGEST     # made-up words of this many letters or more are compared together
MADE_UP = 1000                # made-up words of each length
SEED = E.SEED
BAR, FDR = E.BAR, E.FDR       # a best match beats the bar when at most BAR of the made-up words do as well
# The bar of the test, set before its first run (data/discovery/variants.md, section 2): the share of the hidden
# variants that must come back to their own entry as the single best match, and the share that must do so with a
# match that beats the bar against the made-up words. The test succeeds when both are reached.
FOUND = 2 / 3
STANDS_OUT = 1 / 2
UNSURE = re.compile(r"\?|peut")       # a variant that Rilly marks as uncertain: "mle (?)", "Mn (peut-être)"
TOP = 3                       # the best matches kept for each piece
CONTROLS = 12                 # listed variants shown as pieces, with the candidates they got when hidden
DECOYS = 12                   # listed variants shown as pieces, their own entry taken out of the candidates
PER_PACK = 45                 # items a checker reads in one pack, at most
VERDICTS = ("same", "other", "no")


# ------------------------------------------------------------------------------------------------ letters

def back(word):
    """A letter string read from its end: the search compares words that way, so that an ending comes first."""
    return word[::-1]


def strings(spelling):
    """Every letter string a spelling of Rilly's can have, vowels included (the signs se and ne read both ways,
    letters in brackets with and without); none for a spelling with lost signs."""
    return {E.meroitic(s, True) for s in L.corpus_spellings(spelling)} - {""}


def flat(e, mer=LETTERS):
    """The starting chances for one letter of an entry: it stays, it drops, or it becomes another letter, any other
    letter as likely as the next. Nothing about Meroitic spelling is assumed here."""
    p = {m: 0.10 / (len(mer) - 1) for m in mer}
    p[e], p[""] = 0.80, 0.10
    return p


# ------------------------------------------------------------------------------------------------ the pool

def words(raw=None):
    """The entries of the lexicon proper as the search needs them: the letters of the headword (`key`, and `head`
    for every reading of it), the variants listed under it that are not spelled like it (`listed`), whether it is
    an ending or a prefix (`affix`), and its level, kind and corpus spellings as the coverage map has them.

    `accepted`: would a piece that is this word count as translated? (accept())"""
    raw = L.load() if raw is None else raw
    level = {e["headword"]: e for e in C.lexicon(raw)}
    out = []
    for e in raw:
        if (e.get("page_pdf") or 0) >= L.REJECTED_FROM:
            continue
        c, head = level[e["headword"].strip()], strings(e["headword"])
        listed = []
        for v in e.get("variants") or []:
            q = E.headword(v, True)
            if q and head and q not in head:
                listed.append({"variant": v, "letters": q, "strings": strings(v) - head,
                               "uncertain": bool(UNSURE.search(v))})
        text = " ".join(str(e.get(k) or "") for k in ("meaning_en", "rilly_view", "proposals"))
        meaning = (e.get("meaning_en") or "").strip()
        sends = bool(L.XREF.search(meaning.lower())) and c["meaning"] == meaning    # the map did not follow it
        out.append({"headword": c["headword"], "key": E.headword(e["headword"], True), "head": head,
                    "listed": listed, "affix": c["affix"], "kind": c["kind"], "level": c["level"],
                    "status": c["status"], "spellings": c["forms"], "meaning": meaning, "text": text,
                    "sends": sends})
    accept(out)
    return out


def accept(entries):
    """Set `accepted` on each entry: would a piece that is this word count as translated? The map's level of the
    entry must be a translated one. An entry whose meaning sends to another ("variant of ...", "see ...") and that
    the map did not follow there (coverage.lexicon follows only to an entry with an accepted meaning) counts when
    an entry it is a variant of does: one that lists its spelling, or that its meaning names (names()). So `Wis`,
    a variant of `Wos`, counts, and `qetneyineqeli` does not: it is "established" as a variant of an epithet whose
    own meaning is a proposal. An entry that sends nowhere the lexicon has keeps its level's answer."""
    def ok(a, depth=0):
        if a["level"] not in C.TRANSLATED or depth > 3:
            return False
        to = [b for b in entries if b is not a and a["sends"]
              and (a["head"] & {s for v in b["listed"] for s in v["strings"]} or names(a["meaning"], b["headword"]))]
        return any(ok(b, depth + 1) for b in to) if to else True

    for e in entries:
        e["accepted"] = ok(e)


def units(entries, hidden=frozenset(), alone=frozenset()):
    """The pool: one match for each headword spelling among the words, with the letter strings of its headwords and
    their listed variants, read from the end (`codes`).

    `hidden` are letter strings to strike: an entry that has one as its headword goes, and no other entry keeps
    one among its variants. `alone` are headwords that keep none of their variants (the stricter test)."""
    by = {}
    for e in entries:
        if e["affix"] or not e["key"] or e["head"] & hidden:
            continue
        own = set() if e["headword"] in alone else {s for v in e["listed"] for s in v["strings"]}
        u = by.setdefault(e["key"], {"key": e["key"], "entries": [], "codes": set()})
        u["entries"].append(e["headword"])
        u["codes"] |= (e["head"] | own) - hidden
    return [dict(u, codes=sorted(back(c) for c in u["codes"])) for u in by.values()]


def cases(entries):
    """(the training pairs, the hidden variants of the test).

    A pair is one listed variant with its headword, endings' variants included: {"letters", "head", "entry"}. A
    hidden variant is one letter string that words list as a variant, three letters or more: {"letters", "variants"
    (as printed), "owners" (the headwords that list it), "hidden" (the strings struck with it), "uncertain" (every
    listing is marked so)}."""
    pairs, by = [], {}
    for e in entries:
        for v in e["listed"]:
            pairs.append({"letters": v["letters"], "head": sorted(e["head"]), "entry": e["headword"]})
            if e["affix"] or not e["key"] or len(v["letters"]) < SHORTEST:
                continue
            it = by.setdefault(v["letters"], {"letters": v["letters"], "variants": [], "owners": [], "hidden": set(),
                                              "uncertain": True})
            it["variants"].append(v["variant"])
            it["owners"].append(e["headword"])
            it["hidden"] |= v["strings"]
            it["uncertain"] = it["uncertain"] and v["uncertain"]
    heads = {e["headword"]: e["head"] for e in entries}
    for it in by.values():
        it["hidden"] -= set().union(*(heads[h] for h in it["owners"]))    # an owner's own headword is never hidden
    return pairs, list(by.values())


def without(pairs, item, owners=False):
    """The pairs left to train on when an item is hidden: none whose variant or headword is a hidden spelling, and
    with `owners`, none of the entries that list it."""
    return [p for p in pairs if p["letters"] not in item["hidden"] and not set(p["head"]) & item["hidden"]
            and not (owners and p["entry"] in item["owners"])]


# ------------------------------------------------------------------------------------------------ the model

def ending_counts(raw=None, rows=None):
    """How often a word of the lexicon stands bare ("") and with each ending of lexique.SUFFIXES, counted on the
    different words of the corpus that the coverage map's lookup explains as an entry or as an entry and an ending."""
    es = C.lexicon(raw)
    known, affixes, heads = C.index(es)
    rows = C.texts() if rows is None else rows
    counts = collections.Counter()
    for tok in sorted({t for r in rows for t in r["text"].split() if C.PLAIN.fullmatch(t)}):
        parts = (C.lookup(tok, "", known, affixes) or {}).get("parts") or []
        if len(parts) == 2 and parts[1]["entry"] == "ending":
            counts[parts[1]["form"]] += 1
        elif len(parts) == 1 and parts[0]["entry"] in heads and not heads[parts[0]["entry"]]["affix"]:
            counts[""] += 1
    return {s: counts[s] for s in L.SUFFIXES}


def ending_chances(counts):
    """The log chance of each ending, read from its end as the search reads it, the bare word ("") first."""
    n = sum(counts.values())
    return {back(s): math.log((counts[s] + 1.0) / (n + len(counts))) for s in L.SUFFIXES}


def trained(pairs, endings):
    """The model counted from the pairs, with the endings a pool entry may carry."""
    md = E.train([(back(p["letters"]), [back(c) for c in p["head"]]) for p in pairs], mer=LETTERS, egy=LETTERS,
                 articles=("",), start=flat)
    return dict(md, article=endings)


def counted(pairs, md):
    """What the model's last round counts on the pairs: ({(entry's letter, variant's letter or ""): times},
    {letter added: times}, {entry's letter: times it was aligned})."""
    bare = dict(md, article={"": 0.0})
    out, add = collections.Counter(), collections.Counter()
    for p in pairs:
        w = back(p["letters"])
        code = max((back(c) for c in p["head"]), key=lambda c: (E.score(w, c, bare), c))
        for e, m in E.align(w, code, bare)[1]:
            if e:
                out[e, m] += 1
            else:
                add[m] += 1
    seen = collections.Counter()
    for (e, _), k in out.items():
        seen[e] += k
    return out, add, seen


# ----------------------------------------------------------------------------------------------- the search

def how(word, unit, md):
    """How a match gives a word: the spelling of the match that fits best, the ending, the score, and the letters
    that differ as (the match's letter or "", the word's letter or ""), in the word's order."""
    w = back(word)
    code = max(unit["codes"], key=lambda c: (E.score(w, c, md), c))
    a, ops = E.align(w, code, md)
    return {"spelling": back(code), "ending": back(a), "score": E.score(w, code, md),
            "differences": [[e, m] for e, m in reversed(ops) if e != m]}


def found(word, us, trie, md, top=TOP, skip=()):
    """The best matches of a word: [{"entries", "key", "spelling", "ending", "score", "differences"}], best first.
    `skip` are headwords whose match is left out (a piece that is a headword is not compared with itself)."""
    hits = E.search(back(word), trie, md, top=top + 1 if skip else top)
    hits = [(s, k) for s, k in hits if not set(us[k]["entries"]) & set(skip)][:top]
    return [dict(how(word, us[k], md), entries=us[k]["entries"], key=us[k]["key"]) for _, k in hits]


def yardstick(trie, md, fake):
    """The best score of every made-up word in a pool: {length: [scores]}."""
    return {k: [E.search(back(w), trie, md)[0][0] for w in ws] for k, ws in fake.items()}


def kept_yardstick(us, trie, md, fake, path=None):
    """yardstick(), read from the result file when that was made with this pool, this model and these made-up words
    (it keeps their fingerprint), and searched and written otherwise: the search of the made-up words is most of a
    build's eight minutes."""
    path = OUT / "yardstick.json" if path is None else path
    mark = hashlib.sha256(json.dumps([[[u["key"], u["codes"]] for u in us], md, fake], sort_keys=True).encode()).hexdigest()
    if path.exists():
        kept = json.loads(path.read_text(encoding="utf-8"))
        if kept["fingerprint"] == mark:
            return {int(k): v for k, v in kept["scores"].items()}
    scores = yardstick(trie, md, fake)
    path.write_text(json.dumps({"fingerprint": mark, "scores": scores}) + "\n", encoding="utf-8")
    return scores


def letter_for_letter(us, fake):
    """How many of the made-up words of each length are an entry's spelling letter for letter, and how many are
    one with or without an ending: {length: [the first, the second, of how many]}. A piece of that length cannot
    beat the bar when more than BAR of the made-up words do: no match is better than a letter for letter one."""
    bare = {back(c) for u in us for c in u["codes"]}
    whole = {b + s for b in bare for s in L.SUFFIXES}
    return {k: [sum(w in bare for w in ws), sum(w in whole for w in ws), len(ws)] for k, ws in fake.items()}


def as_many(k, n, p=BAR):
    """The chance that k or more of n words beat a bar that each beats with chance p (egyptian.as_many, summed
    in logarithms: with more than a thousand words its terms no longer fit a float)."""
    def term(i):
        return math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
                        + i * math.log(p) + (n - i) * math.log(1 - p))
    return min(1.0, sum(term(i) for i in range(k, n + 1)))


def chance(score, word, scores):
    """The share of the made-up words of a word's length (the longest together) whose best match is as good."""
    return E.chance(score, scores[min(len(word), max(scores))])


def placed(item, us, md):
    """Where the search puts a hidden variant: `place` is one more than the number of matches that score as well
    as the best match that holds an entry listing the variant, so a tie with another match is a miss; `score` is
    the score of the best match of all, whose entries are `best`."""
    trie, w = E.Trie(list(enumerate(us))), back(item["letters"])
    own = {k for k, u in enumerate(us) if set(u["entries"]) & set(item["owners"])}
    top = E.search(w, trie, md)[0]
    mine = max(E.score(w, c, md) for k in own for c in us[k]["codes"])
    as_good = E.search(w, trie, md, floor=mine - 1e-9)
    return {"place": 1 + sum(k not in own for _, k in as_good), "of": len(us), "score": top[0],
            "best": us[top[1]]["entries"]}


def made_up(us):
    """MADE_UP made-up words of each length, built letter by letter as letters follow one another in the pool's
    headwords: {length: [words]}."""
    return E.made_up(sorted(u["key"] for u in us), n=MADE_UP, seed=SEED, longest=LONGEST)


def hidden_test(entries, endings, scores):
    """Each listed variant hidden in turn (cases()), searched with a model trained on the rest. `strict` is the
    same with the other variants of its entries hidden too and their pairs left out of the training. The chance
    compares the best match with `scores`, the made-up words' best scores in the whole pool (yardstick())."""
    pairs, items = cases(entries)
    rows = []
    for it in items:
        row = {"letters": it["letters"], "variants": it["variants"], "owners": it["owners"],
               "uncertain": it["uncertain"]}
        for name, strict in (("listed", False), ("strict", True)):
            got = placed(it, units(entries, it["hidden"], set(it["owners"]) if strict else frozenset()),
                         trained(without(pairs, it, strict), endings))
            row[name] = dict(got, chance=chance(got["score"], it["letters"], scores))
        rows.append(row)
    return rows


def own_chance(item, entries, pairs, endings, fake):
    """A hidden variant's chance with the made-up words searched as the variant itself is: in the pool without it
    and with the model trained without it. hidden_test() compares with the made-up words' scores in the whole pool
    instead (one search of the made-up words, not one for each hidden variant); this is the check on that."""
    us, md = units(entries, item["hidden"]), trained(without(pairs, item), endings)
    trie, k = E.Trie(list(enumerate(us))), min(len(item["letters"]), max(fake))
    return E.chance(placed(item, us, md)["score"], [E.search(back(w), trie, md)[0][0] for w in fake[k]])


def real_words(entries, us, trie, md, scores):
    """The comparison with real words: every word with an accepted meaning that the lexicon calls a variant of
    nothing (its meaning sends to no other entry, it lists no variant, and no other entry has its spelling),
    searched among the other matches. `linked`: the lexicon links it with its best match all the same (linked()),
    so the two may be one word. [{"headword", "key", "chance", "best", "ending", "differences", "linked"}]"""
    owners = collections.Counter(c for u in us for c in u["codes"])
    by_key, by_head = {u["key"]: u for u in us}, {e["headword"]: e for e in entries}
    out = []
    for e in entries:
        u = by_key.get(e["key"])
        if (e["affix"] or u is None or len(e["key"]) < SHORTEST or e["status"] not in L.GOOD or not e["meaning"]
                or L.XREF.search(e["meaning"].lower()) or e["listed"] or any(owners[c] > 1 for c in u["codes"])
                or any(x["key"] == e["key"] for x in out)):
            continue
        hit = found(e["key"], us, trie, md, top=1, skip=u["entries"])[0]
        out.append({"headword": e["headword"], "key": e["key"], "chance": chance(hit["score"], e["key"], scores),
                    "best": hit["entries"], "ending": hit["ending"], "differences": hit["differences"],
                    "linked": linked(e["headword"], hit, by_head)})
    return out


def pieces():
    """The pieces of the coverage map's list: [{"piece", "headword" (it is one), "kind", "level", "texts",
    "words", "letters"}]. A piece that is letters and holds a digit or a lost sign has no letters to search."""
    out = []
    for r in csv.DictReader(E.UNKNOWN.open(encoding="utf-8"), delimiter="\t"):
        head = r["headword or letters"] == "headword"
        if head:
            word = E.headword(r["piece"], True)
        else:
            word = E.meroitic(r["piece"], True) if re.fullmatch(r"[a-zA-Z]+", r["piece"]) else ""
        out.append({"piece": r["piece"], "headword": head, "kind": r["kind"], "level": r["level"],
                    "texts": int(r["texts (near-copies once)"]), "words": int(r["words"]), "letters": word})
    return out


# the words by which an entry's text sends to another entry, with up to four plain words before its headword
# ("variant of the full name Apedemk", "see pẖo", "the same lexeme as the adjective mẖe")
SENDS_ON = (r"(?:variants?(?:\s*\(\?\))?\s+(?:in\s+REM[\s\d,and]+)?of|\bsee(?:\s+also)?|\bcf\.?|\bforms?\s+of|"
            r"\bspelling\s+of|\b(?:same|equivalent)\s+(?:\w+\s+)?(?:as|of|to))\s+(?:[a-z]+\s+){0,4}?['‘\"“*]?")


def names(text, headword):
    """Does an entry's text send to a headword? Yes when it names it right after words that send on (SENDS_ON):
    a headword such as `are` or `at` is also an English word, so its mere presence says nothing. A headword that
    only begins a longer word with a letter in brackets (`w` in "variant of w(e)tneyiqeli") is not named."""
    return bool(re.search(SENDS_ON + re.escape(C.bare(headword)) + r"(?![\w-]|\(\w+\)\w)", text))


def linked(piece, hit, by_head):
    """Does the lexicon itself link a piece that is a headword with its match? Yes when one's entry lists a
    spelling of the other, or sends to the other's headword in its text (names())."""
    e = by_head.get(piece)
    if e is None:
        return False
    mine = e["head"] | {s for v in e["listed"] for s in v["strings"]}
    for h in hit["entries"]:
        o = by_head[h]
        theirs = o["head"] | {s for v in o["listed"] for s in v["strings"]}
        if mine & theirs or names(e["text"], h) or names(o["text"], piece):
            return True
    return False


# ----------------------------------------------------------------------------------------------- commands

def first():
    entries = words()
    us = units(entries)
    pairs, items = cases(entries)
    counts = ending_counts()
    print(f"lexicon proper: {len(entries)} entries, {sum(not e['affix'] for e in entries)} words; "
          f"pool: {len(us)} matches, {sum(len(u['codes']) for u in us)} letter strings")
    of_words = sum(len(e["listed"]) for e in entries if not e["affix"])
    print(f"listed variants not spelled like their headword: {len(pairs)} ({of_words} of words); hidden in the "
          f"test: {len(items)}, {sum(i['uncertain'] for i in items)} of them marked uncertain")
    print("lengths of the hidden variants:", dict(sorted(collections.Counter(len(i["letters"]) for i in items).items())))
    print("endings:", counts)
    ps = pieces()
    print(f"pieces: {len(ps)}; with {SHORTEST} letters or more: {sum(len(p['letters']) >= SHORTEST for p in ps)}")


def build():
    raw = L.load()
    entries = words(raw)
    by_head = {e["headword"]: e for e in entries}
    us = units(entries)
    trie = E.Trie(list(enumerate(us)))
    pairs, items = cases(entries)
    counts = ending_counts(raw)
    endings = ending_chances(counts)
    md = trained(pairs, endings)
    fake = made_up(us)
    OUT.mkdir(parents=True, exist_ok=True)
    scores = kept_yardstick(us, trie, md, fake)

    # the test: each listed variant hidden in turn
    test = hidden_test(entries, endings, scores)
    (OUT / "test.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in test))

    # what the model counted from all the variants
    out, add, seen = counted(pairs, md)
    (OUT / "model.json").write_text(json.dumps(
        {"pairs": len(pairs), "letters": sum(seen.values()), "added": sum(add.values()),
         "seen": dict(sorted(seen.items())), "endings": counts,
         "out": [[e, m, k] for (e, m), k in sorted(out.items(), key=lambda x: (-x[1], x[0])) if e != m],
         "add": [[m, k] for m, k in sorted(add.items(), key=lambda x: (-x[1], x[0]))]}, ensure_ascii=False, indent=1))

    # the yardstick of real words
    real = real_words(entries, us, trie, md, scores)
    (OUT / "real.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in real))

    # the pieces without a meaning
    rows = []
    for p in pieces():
        row = dict(p)
        if len(p["letters"]) >= SHORTEST:
            skip = [h for u in us if p["headword"] and p["piece"] in u["entries"] for h in u["entries"]]
            row["hits"] = found(p["letters"], us, trie, md, skip=skip)
            row["chance"] = chance(row["hits"][0]["score"], p["letters"], scores)
            row["linked"] = p["headword"] and linked(p["piece"], row["hits"][0], by_head)
            # a match that scores as well as the best one is as good a match: two entries can hold one spelling
            level = [h for hit in row["hits"] if hit["score"] >= row["hits"][0]["score"] - 1e-9 for h in hit["entries"]]
            row["accepted"] = any(by_head[h]["accepted"] for h in level)
        rows.append(row)
    (OUT / "candidates.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))

    fig = figures(entries, us, pairs, test, real, rows)
    fig["made_up"] = {"of_each_length": MADE_UP, "letter_for_letter": letter_for_letter(us, fake)}
    fig["coverage_map"] = rest_on_a_variant(entries, glossed())
    (OUT / "figures.json").write_text(json.dumps(fig, ensure_ascii=False, indent=1) + "\n")
    PUBLIC.write_text(public_list(rows), encoding="utf-8")
    print(json.dumps(fig, ensure_ascii=False, indent=1))


def rest_on_a_variant(entries, texts):
    """A by-product for the coverage map, which this file does not change: the entries at a translated level that
    accept() does not accept (their meaning makes them a variant of an entry without an accepted meaning, or sends
    to one, though it may say more, as for `mloyose`), and the running words the map counts as translated through
    one of them. {"entries": [headwords], "words": n}"""
    weak = {e["headword"] for e in entries if e["level"] in C.TRANSLATED and not e["accepted"]}
    words_ = sum(g["level"] in C.TRANSLATED and any(p["entry"] in weak for p in g["parts"])
                 for t in texts for g in t["glosses"])
    return {"entries": sorted(weak), "words": words_}


SAMPLE = 30                   # hidden variants whose chance is computed a second time, in their own pool


def sample():
    """own_chance() for SAMPLE hidden variants drawn with the seed, beside the chance the test reports."""
    raw = L.load()
    entries = words(raw)
    pairs, items = cases(entries)
    endings = ending_chances(ending_counts(raw))
    fake = made_up(units(entries))
    reported = {r["letters"]: r["listed"]["chance"] for r in
                (json.loads(l) for l in (OUT / "test.jsonl").read_text(encoding="utf-8").splitlines())}
    rows = [{"letters": it["letters"], "reported": reported[it["letters"]],
             "own": own_chance(it, entries, pairs, endings, fake)}
            for it in random.Random(SEED).sample(sorted(items, key=lambda i: i["letters"]), SAMPLE)]
    out = {"sample": len(rows), "same": sum(r["own"] == r["reported"] for r in rows),
           "largest_difference": max(abs(r["own"] - r["reported"]) for r in rows),
           "on_the_other_side_of_the_bar": sum((r["own"] <= BAR) != (r["reported"] <= BAR) for r in rows), "rows": rows}
    (OUT / "sample.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))


def tally(rows, name):
    """The test's counts for some of its rows, with the entry's other variants in the pool ("listed") or hidden
    too ("strict")."""
    got = [r[name] for r in rows]
    under = [g for g in got if g["chance"] <= BAR]
    return {"hidden": len(got), "best_match": sum(g["place"] == 1 for g in got),
            "among_three": sum(g["place"] <= 3 for g in got),
            "beats_the_bar": len(under), "best_match_and_beats_the_bar": sum(g["place"] == 1 for g in under)}


LENGTHS = ("3 or 4 letters", "5 or 6 letters", "7 letters or more")


def lengths(n):
    return LENGTHS[0] if n <= 4 else LENGTHS[1] if n <= 6 else LENGTHS[2]


def near(row, by_head):
    """Did a hidden variant that missed go to an entry that the lexicon itself links with one that lists it
    (linked()), or tie with its own entry at the top? Counted after the run; no part of the bar."""
    got = row["listed"]
    return got["place"] > 1 and any(o in got["best"] or linked(o, {"entries": got["best"]}, by_head)
                                    for o in row["owners"])


def figures(entries, us, pairs, test, real, rows):
    by_head = {e["headword"]: e for e in entries}
    searched = [r for r in rows if "hits" in r]
    new = [r for r in searched if not r["linked"]]
    under = [r for r in new if r["chance"] <= BAR]
    whole = tally(test, "listed")
    apart = [r for r in real if not r["linked"]]
    return {
        "pool": {"entries": len(entries), "words": sum(not e["affix"] for e in entries), "matches": len(us),
                 "letter_strings": sum(len(u["codes"]) for u in us)},
        "pairs": len(pairs),
        "bar": {"found": round(FOUND, 4), "stands_out": STANDS_OUT,
                "found_reached": whole["best_match"] >= FOUND * whole["hidden"],
                "stands_out_reached": whole["best_match_and_beats_the_bar"] >= STANDS_OUT * whole["hidden"]},
        "test": {"all": whole, "strict": tally(test, "strict"),
                 "misses": {"all": sum(r["listed"]["place"] > 1 for r in test),
                            "to_a_linked_entry_or_a_tie": sum(near(r, by_head) for r in test),
                            "beat_the_bar": sum(r["listed"]["place"] > 1 and r["listed"]["chance"] <= BAR for r in test),
                            "beat_the_bar_to_a_linked_entry_or_a_tie": sum(near(r, by_head) for r in test
                                                                           if r["listed"]["chance"] <= BAR)},
                 "sure": tally([r for r in test if not r["uncertain"]], "listed"),
                 "uncertain": tally([r for r in test if r["uncertain"]], "listed"),
                 "by_length": {k: tally([r for r in test if lengths(len(r["letters"])) == k], "listed")
                               for k in LENGTHS}},
        "real_words": {"words": len(real), "linked_by_the_lexicon": len(real) - len(apart), "not_linked": len(apart),
                       "at_most_0.05": sum(r["chance"] <= BAR for r in apart),
                       "expected_by_chance": round(BAR * len(apart), 1),
                       "by_length": {k: {"words": sum(lengths(len(r["key"])) == k for r in apart),
                                         "at_most_0.05": sum(r["chance"] <= BAR for r in apart
                                                             if lengths(len(r["key"])) == k)}
                                     for k in LENGTHS}},
        "unknown": {"pieces": len(rows), "searched": len(searched), "too_short": len(rows) - len(searched),
                    "linked_by_the_lexicon": len(searched) - len(new), "new": len(new),
                    "at_most_0.05": len(under), "expected_by_chance": round(BAR * len(new), 1),
                    "as_many_by_chance": as_many(len(under), len(new)),
                    "passing_q_0.2": E.passing([r["chance"] for r in new]),
                    "smallest_chance": round(1 / (MADE_UP + 1), 6),
                    "fewest_at_the_smallest_chance_to_pass": E.fewest_to_pass(len(new), made=MADE_UP),
                    "by_length": {k: {"searched": sum(lengths(len(r["letters"])) == k for r in new),
                                      "at_most_0.05": sum(lengths(len(r["letters"])) == k for r in under)}
                                  for k in LENGTHS},
                    "words_they_stand_in": sum(r["words"] for r in under),
                    "under_the_bar": {"headwords": sum(r["headword"] for r in under),
                                      "letters": sum(not r["headword"] for r in under),
                                      "match_has_an_accepted_meaning": sum(r["accepted"] for r in under),
                                      "with_an_ending": sum(bool(r["hits"][0]["ending"]) for r in under),
                                      "linked_and_under_the_bar": sum(r["chance"] <= BAR for r in searched
                                                                      if r["linked"])}},
    }


def differs(diff):
    """The letters that differ, in words: "r for l", "i dropped", "e added"."""
    return ", ".join(f"{m} for {e}" if e and m else f"{e} dropped" if e else f"{m} added" for e, m in diff)


HEAD = ["piece", "headword or letters", "kind", "texts (near-copies once)", "letters compared", "chance",
        "best match", "its spelling", "ending", "letters that differ", "the match has an accepted meaning",
        "the lexicon links the two itself"]


def public_list(rows):
    """The public list: each searched piece with its best match in the lexicon. It holds headwords and spellings
    and no gloss of the lexicon."""
    lines = ["\t".join(HEAD)]
    for r in sorted((r for r in rows if "hits" in r), key=lambda r: (r["chance"], -r["texts"], r["piece"], r["headword"])):
        h = r["hits"][0]
        lines.append("\t".join([r["piece"], "headword" if r["headword"] else "letters", r["kind"], str(r["texts"]),
                                r["letters"], f'{r["chance"]:.4f}', " / ".join(h["entries"]), h["spelling"],
                                "-" + h["ending"] if h["ending"] else "", differs(h["differences"]),
                                "yes" if r["accepted"] else "no", "yes" if r["linked"] else "no"]))
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------------------------------------ the check

def glossed():
    """The coverage map's gloss file, text by text (local)."""
    if not E.GLOSSES.exists():
        sys.exit(f"no {E.where(E.GLOSSES)}: the gloss file is built by src/coverage.py and kept locally")
    return [json.loads(l) for l in E.GLOSSES.read_text(encoding="utf-8").splitlines()]


def places(texts, heads):
    """Where each piece of the map's list stands: {(piece, it is a headword): [(text number, word number)]}."""
    out = collections.defaultdict(list)
    for i, t in enumerate(texts):
        for j, g in enumerate(t["glosses"]):
            for b, e in C.blockers(g, heads):
                out[b, e is not None].append((i, j))
    return out


def said(g):
    """What a pack shows under a word of a context: the map's gloss when the map counts the word as translated or
    the lookup gave it (the lexicon's own meaning, proposal or kind), and "?" for an analyst's reading that the
    map does not count as translated. A checker must not read another reader's guess: the first packs showed
    those, and with them the analyst's guess for the very piece under another item's words."""
    if g["level"] not in C.TRANSLATED and g.get("by") != "lookup":
        return "?"
    return str(g.get("gloss") or "").replace(" / ", "; ")[:26].strip(" /") or "?"


def secret(g, forms):
    """Is a word one of `forms`, bare or as the first part of a word the map cuts? A form that stands later in a
    cut word (`ateqi` in `yetmdelowiateqi`) is not caught, nor a word that holds a form's letters but that the map
    cuts otherwise (`mXeyotowi`, cut mXeyo-to-wi, holds `mXeyot`): the packs were read so, and three of their items
    show such a word with its gloss (data/discovery/variants.md, section 5)."""
    return g["form"] in forms or bool(g.get("parts")) and g["parts"][0]["form"] in forms


def contexts(spots, texts, n=3, side=4, hide=frozenset(), masked=True):
    """Up to n places with different words around them, each from another text: the words, and under them what
    is known of each (said()), word for word (a gloss that names two senses with " / " between them has "; "
    there). The words of `hide` show no gloss, and with `masked` the word itself shows none."""
    out, seen = [], set()
    for i, j in spots:
        t = texts[i]
        near = list(enumerate(t["glosses"]))[max(0, j - side):j + side + 1]
        words_ = " ".join(f"[{g['form']}]" if k == j else g["form"] for k, g in near)
        if t["id"] in seen or words_ in seen:
            continue
        seen |= {t["id"], words_}
        out.append({"text": t["id"], "words": words_,
                    "glosses": " / ".join("?" if masked and k == j or secret(g, hide) else said(g) for k, g in near)})
        if len(out) == n:
            break
    return out


def stands(spellings, texts, hide=frozenset()):
    """Where a word of the lexicon stands in the texts by the lookup's own account: the words that are one of its
    spellings, bare or with an ending. A word of `hide` is no such place. [(text number, word number)]"""
    return [(i, j) for i, t in enumerate(texts) for j, g in enumerate(t["glosses"])
            if g.get("by") == "lookup" and secret(g, spellings) and not secret(g, hide)]


def shown(hit, by_head, md_counts, texts, hide=frozenset()):
    """A candidate as a checker sees it: the entries of the match, the spelling that fits, the ending, each letter
    that differs with how often the listed variants show it, and two places where the word stands. `hide` are
    the words that show no gloss anywhere in the item and are no place of a candidate: the item's own."""
    out, add, seen = md_counts
    diff = [{"what": differs([d]), "in the listed variants": f"{out[d[0], d[1]]} of {seen[d[0]]} {d[0]}" if d[0]
             else f"{add[d[1]]} added"} for d in hit["differences"]]
    spellings = set().union(*(by_head[h]["spellings"] for h in hit["entries"]))
    return {"entries": [{"headword": h, "kind": by_head[h]["kind"], "status": by_head[h]["status"],
                         "accepted": by_head[h]["accepted"], "meaning": by_head[h]["meaning"][:260]}
                        for h in hit["entries"]],
            "spelling": hit["spelling"], "ending": "-" + hit["ending"] if hit["ending"] else "", "differences": diff,
            "contexts": contexts(stands(spellings, texts, hide), texts, n=2, hide=hide, masked=False)}


def pack_draw(rows, test):
    """What the packs draw from, out of the result files: (every searched piece whose best match beats the bar,
    the hidden variants of the test in an order shuffled with the seed, the random source for the shuffle of the
    whole). check_pack() takes the controls and the decoys from the hidden variants in that order."""
    best = sorted((r for r in rows if "hits" in r and r["chance"] <= BAR), key=lambda r: (r["piece"], r["headword"]))
    rnd = random.Random(SEED)
    known = sorted(test, key=lambda r: r["letters"])
    rnd.shuffle(known)
    return best, known, rnd


def known_items(known, items, entries, pairs, endings, texts):
    """The items of the packs whose answer is known, each a listed variant that stands in the texts, shown as if
    it were a piece with the candidates of the search that hid it.

    A control (CONTROLS of them) is one whose best match beat the bar: the entry that lists it is among its
    candidates if the search found it, and `same` with that entry is the right answer. A decoy (DECOYS of them)
    has five letters or more, like nearly every match under the bar, and its candidates are the best matches left
    when every entry that lists it, and every entry the lexicon links with one of those, is taken out: whatever
    candidate a checker accepts for it is a look-alike."""
    by_head = {e["headword"]: e for e in entries}
    hidden = {it["letters"]: it for it in items}
    made = []
    for row in known:
        what = ("control" if row["listed"]["chance"] <= BAR and sum(m["what"] == "control" for m in made) < CONTROLS
                else "decoy" if len(row["letters"]) >= 5 and sum(m["what"] == "decoy" for m in made) < DECOYS else "")
        it = hidden[row["letters"]]
        spellings = set().union(*(L.corpus_spellings(v) for v in it["variants"]))
        spots = [(i, j) for i, t in enumerate(texts) for j, g in enumerate(t["glosses"]) if g["form"] in spellings]
        if not what or not spots:
            continue
        us, md = units(entries, it["hidden"]), trained(without(pairs, it), endings)
        hits = found(it["letters"], us, E.Trie(list(enumerate(us))), md, top=TOP + 12 if what == "decoy" else TOP)
        if what == "decoy":
            hits = [h for h in hits if not set(h["entries"]) & set(it["owners"])
                    and not any(linked(o, h, by_head) for o in it["owners"])][:TOP]
        made.append({"what": what, "piece": texts[spots[0][0]]["glosses"][spots[0][1]]["form"],
                     "letters": it["letters"],
                     "texts": len({texts[i]["id"] for i, _ in spots}), "spots": spots, "hits": hits,
                     "counts": counted(without(pairs, it), md), "owners": it["owners"],
                     "chance": row["listed"]["chance"], "hide": spellings})
    return made


def check_pack():
    """Write the checkers' packs: every piece whose best match beats the bar, the controls and the decoys
    (known_items()), in one shuffled list cut into packs of at most PER_PACK items; and the key (local).

    An item holds the piece, the number of texts it stands in, its contexts, the lexicon's entry when the piece
    is a headword, and its candidates. It does not say what kind of word the piece is: for a piece that is the
    map's analysts' label, and a control or a decoy would have to borrow its true word's. No context of the item
    shows a gloss under a word that the map finds the piece in, nor under a word of a control or a decoy, a spelling
    of it bare or as the first part of a cut word (said(), secret(), which says what that leaves)."""
    raw = L.load()
    entries = words(raw)
    by_head = {e["headword"]: e for e in entries}
    heads = C.index(C.lexicon(raw))[2]
    pairs, items = cases(entries)
    endings = ending_chances(ending_counts(raw))
    md = trained(pairs, endings)
    rows = [json.loads(l) for l in (OUT / "candidates.jsonl").read_text(encoding="utf-8").splitlines()]
    test = [json.loads(l) for l in (OUT / "test.jsonl").read_text(encoding="utf-8").splitlines()]
    texts = glossed()
    at = places(texts, heads)
    best, known, rnd = pack_draw(rows, test)
    made = known_items(known, items, entries, pairs, endings, texts)
    # the words of the items whose answer is known show no gloss in any item: the map has them translated
    known_words = set().union(*(m["hide"] for m in made))
    counts = counted(pairs, md)
    for r in best:
        spots = at.get((r["piece"], r["headword"]), [])
        made.append({"what": "best", "piece": r["piece"], "letters": r["letters"],
                     "texts": r["texts"], "spots": spots, "hits": r["hits"],
                     "hide": {texts[i]["glosses"][j]["form"] for i, j in spots},
                     "counts": counts, "headword": r["headword"], "chance": r["chance"], "linked": r["linked"]})
    made.sort(key=lambda m: (m["what"], m["piece"], m["letters"]))
    rnd.shuffle(made)

    pack, answer = [], {}
    for k, m in enumerate(made, 1):
        ident = f"V{k:03d}"
        e = by_head.get(m["piece"]) if m.get("headword") else None
        answer[ident] = {"piece": m["piece"], "headword": bool(m.get("headword")), "what": m["what"],
                         "chance": m["chance"], "best": m["hits"][0]["entries"], "owners": m.get("owners", []),
                         "linked": bool(m.get("linked"))}
        hide = m["hide"] | known_words
        pack.append({"id": ident, "piece": m["piece"], "texts": m["texts"],
                     "contexts": contexts(m["spots"], texts, hide=hide),
                     "lexicon": {"headword": e["headword"], "status": e["status"], "text": e["text"][:500]} if e else None,
                     "candidates": [shown(h, by_head, m["counts"], texts, hide) for h in m["hits"]]})
    files = {KEYFILE: json.dumps(answer, ensure_ascii=False, indent=1)}
    n = math.ceil(len(pack) / PER_PACK)
    for k in range(n):
        files[CHECK / f"pack{k + 1:02d}" / "pack.jsonl"] = "".join(
            json.dumps(x, ensure_ascii=False) + "\n" for x in pack[k::n])
    written = write_packs(files, BRIEF.read_text(encoding="utf-8"))
    kinds = collections.Counter(a["what"] for a in answer.values())
    print(f"{len(pack)} items in {n} packs in {E.where(CHECK)}: {kinds['best']} best matches, {kinds['decoy']} "
          f"decoys, {kinds['control']} controls" + ("" if written else
                                                   "; the packs hold answers and are as this build gives them"))


def write_packs(files, brief):
    """Write the key and the packs ({path: text}), the brief beside each pack.jsonl; True when written.

    While a pack's folder holds the checkers' answers (reader*.jsonl) nothing is written: the files must be what
    this build gives, or the build stops, so that answers never stand beside another pack or another key, and the
    BRIEF.md beside them stays the brief those checkers read. A pack folder that this build would not write stops
    it too, since check_merge() reads every pack folder."""
    answered = sorted(E.where(q) for q in CHECK.glob("pack*/reader*.jsonl"))
    changed = [E.where(q) for q, text in files.items() if not q.exists() or q.read_text(encoding="utf-8") != text]
    if answered and changed:
        sys.exit(f"{E.where(CHECK)} holds the checkers' answers ({len(answered)} files), and this build would change "
                 f"{', '.join(changed)}: move the answers away before new packs are built")
    stale = sorted(E.where(q) for q in CHECK.glob("pack*") if q / "pack.jsonl" not in files)
    if stale:
        sys.exit(f"{', '.join(stale)} would stand beside the packs of this build: move them away first")
    if answered:
        return False
    for q, text in files.items():
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_text(text, encoding="utf-8")
        if q.name == "pack.jsonl":
            (q.parent / "BRIEF.md").write_text(brief, encoding="utf-8")
    return True


def which(name, candidates):
    """The candidate of an item that a checker's answer names, as (its number, the entries named), or (None, []).
    The answer gives a headword as the pack prints it (`tk (2)`); one given without its number or its capital
    (`tk`) names every entry of the candidate that is spelled so, when only one candidate has such an entry."""
    name = (name or "").strip()
    for k, c in enumerate(candidates):
        if name in c:
            return k, [name]
    bare = C.bare(name).lower()
    loose = [(k, [h for h in c if C.bare(h).lower() == bare]) for k, c in enumerate(candidates)]
    loose = [(k, hs) for k, hs in loose if bare and hs]
    return loose[0] if len(loose) == 1 else (None, [])


def check_merge(raw=None):
    """Read the checkers' answers (check/pack*/reader*.jsonl) against the key; write check.json, the confirmed
    list (local, with the checkers' reasons; public, forms only) and what the confirmed list would move in the
    coverage map. A piece is confirmed when both checkers answer `same` and name entries of one candidate.
    A checker's answers count for the items of its own pack. `raw` is the lexicon (lexique.load() when None), read
    for the spellings of the decoys' true words."""
    answer = json.loads(KEYFILE.read_text(encoding="utf-8"))
    cands, shown = {}, []
    readers = collections.defaultdict(dict)
    for folder in sorted(CHECK.glob("pack*")):
        ids = []
        for line in (folder / "pack.jsonl").read_text(encoding="utf-8").splitlines():
            x = json.loads(line)
            ids.append(x["id"])
            cands[x["id"]] = [[e["headword"] for e in c["entries"]] for c in x["candidates"]]
        for name, got in E.answers(folder, set(ids), VERDICTS).items():
            readers[name].update(got)
        shown += ids
    if sorted(shown) != sorted(answer):
        sys.exit(f"the packs in {E.where(CHECK)} hold {len(shown)} items and the key {len(answer)}, or other ones: "
                 "they are not one build of `check`")
    out = {"items": len(answer), **{w: sum(a["what"] == w for a in answer.values()) for w in ("best", "decoy", "control")},
           "readers": {}}
    by_head = {e["headword"]: e for e in words(raw)} if any(a["what"] == "decoy" for a in answer.values()) else {}
    spelled = {i: set().union(*(by_head[o]["head"] | {x for v in by_head[o]["listed"] for x in v["strings"]}
                                for o in a["owners"])) for i, a in answer.items() if a["what"] == "decoy"}

    def right(i, a):
        """A control is answered right by `same` with the candidate that holds an entry listing the variant."""
        k = which(a.get("candidate"), cands[i])[0]
        return a["verdict"] == "same" and k is not None and bool(set(cands[i][k]) & set(answer[i]["owners"]))

    def recognised(i, a):
        """A decoy is recognised by `other` with the word that lists the variant, or with one of that word's
        spellings (the decoy's own among them), in the lexicon's letters or the corpus's."""
        named = re.split(r"[\s(,]", (a.get("candidate") or "").strip(), maxsplit=1)[0]
        return a["verdict"] == "other" and bool((strings(named) | {E.meroitic(named, True)}) & spelled[i])

    for name, got in sorted(readers.items()):
        out["readers"][name] = {
            "answered": len(got),
            **{w: dict(collections.Counter(got[i]["verdict"] for i, a in answer.items() if a["what"] == w and i in got))
               for w in ("best", "decoy", "control")},
            "controls_right": sum(right(i, got[i]) for i, a in answer.items() if a["what"] == "control" and i in got),
            "decoys_recognised": sum(recognised(i, got[i]) for i, a in answer.items() if a["what"] == "decoy" and i in got)}
    names = sorted(readers)
    confirmed = []
    if len(names) >= 2:
        a, b = readers[names[0]], readers[names[1]]
        both = [i for i in answer if i in a and i in b]
        out["answered_by_both"] = len(both)
        out["same_verdict"] = sum(a[i]["verdict"] == b[i]["verdict"] for i in both)
        named = {i: (which(a[i].get("candidate"), cands[i]), which(b[i].get("candidate"), cands[i])) for i in both}
        agree = [i for i in both if a[i]["verdict"] == b[i]["verdict"] == "same"
                 and named[i][0][0] is not None and named[i][0][0] == named[i][1][0]]
        out["same_for_both_but_another_candidate"] = [
            i for i in both if a[i]["verdict"] == b[i]["verdict"] == "same" and i not in agree]
        out["same_for_both"] = {w: sum(answer[i]["what"] == w for i in agree) for w in ("best", "decoy", "control")}
        out["controls_right_for_both"] = sum(right(i, a[i]) and right(i, b[i]) for i in agree
                                             if answer[i]["what"] == "control")
        out["decoys_recognised_for_both"] = sum(recognised(i, a[i]) and recognised(i, b[i]) for i in both
                                                if answer[i]["what"] == "decoy")
        out["other_for_both"] = [{"id": i, "piece": answer[i]["piece"], "what": answer[i]["what"],
                                  "candidates": [a[i].get("candidate", ""), b[i].get("candidate", "")]}
                                 for i in both if a[i]["verdict"] == b[i]["verdict"] == "other"]
        confirmed = [{"id": i, "piece": answer[i]["piece"], "headword": answer[i]["headword"],
                      "linked": answer[i]["linked"], "chance": answer[i]["chance"],
                      "entries": list(dict.fromkeys(named[i][0][1] + named[i][1][1])),
                      "confidence": [a[i].get("confidence"), b[i].get("confidence")],
                      "reasons": [a[i].get("reason", ""), b[i].get("reason", "")]}
                     for i in agree if answer[i]["what"] == "best"]
    out["confirmed"] = len(confirmed)
    if confirmed:
        out["moved"] = moved(confirmed)
    (OUT / "check.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    (OUT / "confirmed.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in confirmed))
    if len(names) >= 2:
        CONFIRMED.write_text(confirmed_list(confirmed), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


def moved(confirmed, texts=None, raw=None):
    """What the confirmed list would move in the coverage map, without changing the map: a word moves to
    translated when every piece that blocks it (coverage.blockers) is confirmed as a word that both checkers
    name with an accepted meaning. Counted on every text and with near-copies once, as the map counts."""
    raw = L.load() if raw is None else raw
    heads = C.index(C.lexicon(raw))[2]
    by_head = {e["headword"]: e for e in words(raw)}
    texts = glossed() if texts is None else texts
    for c in confirmed:
        c["accepted"] = all(h in by_head and by_head[h]["accepted"] for h in c["entries"])
    lifts = {(c["piece"], c["headword"]) for c in confirmed if c["accepted"]}
    once = {r["id"] for r in C.distinct([{"id": t["id"], "text": t["text"]} for t in texts])}
    out = {"confirmed": len(confirmed), "with_an_accepted_meaning": len(lifts), "words": 0, "words_once": 0,
           "texts_completed_once": 0, "translated_now": 0, "all_words": 0, "translated_now_once": 0,
           "all_words_once": 0, "by_piece": {}}
    for t in texts:
        left = lifted = 0
        for g in t["glosses"]:
            blocks = {(b, e is not None) for b, e in C.blockers(g, heads)}
            hit = bool(blocks) and blocks <= lifts
            for b in blocks if hit else ():
                out["by_piece"][b[0]] = out["by_piece"].get(b[0], 0) + 1
            out["words"] += hit
            out["all_words"] += 1
            out["translated_now"] += g["level"] in C.TRANSLATED
            if t["id"] in once:
                out["words_once"] += hit
                out["all_words_once"] += 1
                out["translated_now_once"] += g["level"] in C.TRANSLATED
            if g["level"] not in C.TRANSLATED and g["level"] != "lost":
                left += not hit
                lifted += hit
        out["texts_completed_once"] += t["id"] in once and lifted > 0 and left == 0
    return out


def confirmed_list(confirmed):
    """The public list of the confirmed pieces: forms and headwords, no gloss."""
    lines = ["\t".join(["piece", "headword or letters", "the word it is a spelling or a form of, for both checkers",
                        "that word has an accepted meaning", "the lexicon links the two itself", "chance"])]
    for c in sorted(confirmed, key=lambda c: (c["piece"], c["headword"])):
        lines.append("\t".join([c["piece"], "headword" if c["headword"] else "letters",
                                " / ".join(c["entries"]), "yes" if c.get("accepted") else "no",
                                "yes" if c["linked"] else "no", f'{c["chance"]:.4f}']))
    return "\n".join(lines) + "\n"


def main(argv):
    if argv == ["first"]:
        first()
    elif argv == ["build"]:
        build()
    elif argv == ["sample"]:
        sample()
    elif argv == ["check"]:
        check_pack()
    elif argv == ["merge"]:
        check_merge()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
