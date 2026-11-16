"""Distinct words: how many different words the clean corpus holds and how many of them have a meaning, the
project's north star (data/discovery/distinct_words.md).

A running word of the map is a dictionary word (its spelling is built on an entry of the lexicon of 2003 that is
no name), a name, or a stem the map could not name. The dictionary words can be counted. The unnamed stems cannot
be counted as they stand: some are names, pieces of longer words, forms of dictionary words the map missed, or
the same word twice. So two checkers judge a sample of them, drawn by a fixed seed, and the count of distinct
words is an estimate with a range.

Every command reads and writes under data/sources/words/ (local only: the packs quote the lexicon), except
`public`, which writes the figures of the page.

  python3 -I src/words.py population   the words of the map, by what they are (population.json)
  python3 -I src/words.py packs r2     the sample of unnamed stems for two checkers (packs/, sample.json)
  python3 -I src/words.py count r2     the two checkers compared, the estimate and its range (result.json)
  python3 -I src/words.py public       data/discovery/distinct_words_figures.json

Two readings of the same sample: `r1`, whose checkers missed the bar, and `r2`, with the brief corrected as the
bar says (fresh checkers; the rules of RULES2). The line each checker was started with is in
runs/prompts/WORDS_launch.md; the briefs are BRIEF and BRIEF2 below.
"""
import collections
import json
import math
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import coverage as C                                   # noqa: E402
import f4r as R                                        # noqa: E402
import recurring as W                                  # noqa: E402

OUT = ROOT / "data/sources/words"
PUBLIC = ROOT / "data/discovery/distinct_words_figures.json"
RECURRING = ROOT / "data/discovery/recurring_words_figures.json"
NAME_KINDS = ("person name", "place name", "god name")
SEED = 20261116
SAMPLE = 240
PACK = 24
SHOWN = 6                       # places shown for a stem at most
WIDTH = 6                       # words on each side of a place
ALIKE = 5                       # look-alikes listed at most, of each sort
CASES = ("word", "known", "same", "name", "piece", "unclear")
# The bar, set and committed before any checker was started (the page gives the commit).
KAPPA = 0.6                     # Cohen's kappa of the two checkers over the sampled stems; under it nothing is taken
Z = 1.96                        # the range is a 95% interval
# Subagent tokens of the checkers of each reading, from the task notifications, by hand after the runs.
TOKENS = {"r1": (20, 1504282), "r2": (0, 0)}

BRIEF = """# What are these {n} stems? A sample of what the map of Meroitic could not name

The project's word-by-word map of the Meroitic corpus cuts each written word into pieces it knows from the lexicon
of 2003 (stems, endings, prefixes). For the words below it found no stem it knows: what is left, the piece shown as
the item's stem, has no entry. The project wants to count how many different words the corpus holds, so for each
stem it has to know what the stem really is. Your task is to say that, for each item, from what is shown.

For each item give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

    {{"n": 17, "stem": "<the stem as given here>", "case": "word", "of": "", "why": "<at most twenty words>"}}

- "case" is one of:
  - "word": a word of the language in its own right (a noun, a verb, a title, an adjective, a particle) that no
    entry of the lexicon covers. Its meaning need not be known.
  - "known": a form of a word the lexicon has: a variant spelling, or a stem with endings the map did not cut
    off. Put the lexicon's headword in "of".
  - "same": the same word as another stem in the list "Look-alikes among the other unnamed stems" of this item (a
    variant spelling or another form of it). Put that stem in "of".
  - "name": a proper name of a person, a place or a god, or part of one.
  - "piece": no stem at all: a piece of a longer word that the edition's word division or the map's cutting has
    separated from the rest (the words beside it show the rest), or an ending or a sign standing alone.
  - "unclear": signs are lost in or around it, or what is shown is too thin to decide between the cases above.
- Decide on what is shown: the spellings the stem was cut from, the places with the words around them and the
  map's reading of each, and the look-alikes. A look-alike is only a similar spelling: it is the same word only
  if the places support it.
- You may search the lexicon of 2003 (`data/rilly2003/`, JSON lines) for a spelling. Do not use your own knowledge
  of Meroitic, do not search the web, do not run the project's scripts, and write no other file.
- "of" is empty unless the case is "known" or "same".

Letters: the project writes `S` for the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ; a dot is a lost
sign. In a place the word that holds the stem is in bold; `[...]` in the readings marks a word the map has no
accepted meaning for. The repository's root is /Users/mike/repos/mike/meroitic.

When the file is written, reply in one line: how many items, and how many of each case.
"""


# The second reading: the first missed the bar, mostly on "word" against "unclear" for a stem that stands once
# (42 of its 71 stems not agreed) and on "word" against "name" (13). These rules were added and committed before
# any checker of the second reading was started.
RULES2 = """
Rules for the cases (read them before you start; a first reading without them did not agree):

- A stem with no lost sign is a **"word"** unless something shown marks it as one of the other cases. That it
  stands once, or among words nobody understands, is no reason for "unclear": the edition wrote it as a word, and
  it counts as one until something shows otherwise.
- **"unclear"** only when a sign is lost (a dot) in the stem's own word or in the word right before or right after
  it, or when the text has fewer than three words. Too little context alone is not "unclear".
- **"name"** only when the place gives a reason: the stem stands where names stand (beside a word of filiation
  such as "born of" or "begotten of", before "this one is", or with a title and "it is"), or the map reads the
  word beside it as part of the same name.
- **"piece"** only when the word beside it completes it to a spelling the lexicon has, or when the stem is one or
  two signs. A stem of three signs or more that nothing completes is a "word".
- **"known"** and **"same"** only when the places support it, not on the look of the spelling alone.
"""
BRIEF2 = BRIEF.replace("\nLetters: the project writes", RULES2 + "\nLetters: the project writes")
assert BRIEF2 != BRIEF
ROUNDS = {"r1": {"folder": "", "brief": BRIEF}, "r2": {"folder": "r2/", "brief": BRIEF2}}
LAST = "r2"


def read(path):
    return json.loads((OUT / path).read_text(encoding="utf-8"))


def write(path, data):
    (OUT / path).parent.mkdir(parents=True, exist_ok=True)
    (OUT / path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ----------------------------------------------------------------------------------------- what each word is

def identity(g, lex):
    """What a running word of the map is, for counting distinct words:
    ("none", ())             a name or a numeral by the map's own level, or a word with lost signs: not counted;
    ("dictionary", entries)  built on entries of the lexicon that are no names: its stems, or, for a word made of
                             endings and particles only, those;
    ("name", ())             built on a name (an entry that is a name, or a piece the map marks as one) and on no stem;
    ("stem", (piece,))       no stem the lexicon has: the longest piece the map could not name, or the whole spelling."""
    if g["level"] in W.NAMED or g["level"] == "lost":
        return "none", ()
    parts = g.get("parts") or []
    entries = [p.get("entry") for p in parts]
    words = [e for e in entries if e in lex and (lex[e].get("kind") or "") not in NAME_KINDS]
    stems = [e for e in words if not W.affix(e)]
    if stems:
        return "dictionary", tuple(stems)
    if any(e == "NAME" or (e in lex and (lex[e].get("kind") or "") in NAME_KINDS) for e in entries):
        return "name", ()
    unnamed = [p["form"] for p in parts if p.get("entry") == "?"]
    if unnamed:
        return "stem", (max(unnamed, key=len),)
    return ("dictionary", tuple(words)) if words else ("stem", (g["form"],))


def population_of(gl, lex):
    """The running words that need a meaning, by what they are: the dictionary words in use (entry -> uses), the
    count of names, and the unnamed stems, each with its spellings and places."""
    known, stems, c = collections.Counter(), {}, collections.Counter()
    for t in sorted(gl):
        for i, g in enumerate(gl[t]):
            what, ids = identity(g, lex)
            c[what] += 1
            if what == "dictionary":
                known.update(set(ids))
            elif what == "stem":
                s = stems.setdefault(ids[0], {"stem": ids[0], "uses": 0, "texts": set(), "forms": collections.Counter(), "places": []})
                s["uses"] += 1
                s["texts"].add(t)
                s["forms"][g["form"]] += 1
                s["places"].append([t, i])
    for s in stems.values():
        s["texts"] = len(s["texts"])
        s["forms"] = dict(s["forms"].most_common())
    return known, stems, dict(c)


def translated(known, lex):
    """The dictionary words in use whose meaning the lexicon calls established or probable."""
    return sorted(h for h in known if (lex[h].get("status") or "") in W.SURE)


def lookup_only():
    """The map as the lexicon alone gives it on the same corpus: looked up word by word, none of the project's
    analysts or corrections ("before us")."""
    es = C.lexicon()
    words, affixes, _ = C.index(es)
    import recount as V
    corpus = [json.loads(l) for l in V.CORPUS.read_text(encoding="utf-8").splitlines() if l.strip()]
    return {r["id"]: gs for r, gs in C.gloss_texts(V.rows_for_map(corpus), words, affixes, {})}


def population():
    gl, lex = W.the_map(), W.lexicon()
    known, stems, c = population_of(gl, lex)
    before, _, cb = population_of(lookup_only(), lex)
    out = {"running": c, "dictionary_words": len(known), "translated": len(translated(known, lex)),
           "unnamed_stems": len(stems), "unnamed_in_one_place": sum(s["uses"] == 1 for s in stems.values()),
           "unnamed_running_words": sum(s["uses"] for s in stems.values()),
           "before": {"running": cb, "dictionary_words": len(before), "translated": len(translated(before, lex))},
           "known": dict(known.most_common()), "stems": stems}
    write("population.json", out)
    print({k: v for k, v in out.items() if k not in ("known", "stems")})


# --------------------------------------------------------------------------------------------------- the sample

def distance(a, b, cap=2):
    """The edit distance of two spellings, or cap + 1 when it is more than cap."""
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    row = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        new = [i]
        for j, y in enumerate(b, 1):
            new.append(min(row[j] + 1, new[j - 1] + 1, row[j - 1] + (x != y)))
        if min(new) > cap:
            return cap + 1
        row = new
    return min(row[-1], cap + 1)


def reach(stem):
    """How far a look-alike may be: none for a stem under three signs, one sign under seven, two from seven."""
    return 0 if len(stem) < 3 else 1 if len(stem) < 7 else 2


def alikes(stem, pool, most=ALIKE):
    """The spellings of a pool within reach of a stem, the closest first, the stem itself left out."""
    far = reach(stem)
    near = sorted((distance(stem, o, far), o) for o in pool if o != stem and far and abs(len(o) - len(stem)) <= far)
    return [o for d, o in near if d <= far][:most]


def sample_of(stems, n=SAMPLE, seed=SEED):
    """n of the unnamed stems, drawn by a fixed seed from their sorted list: every stem has the same chance."""
    keys = sorted(stems)
    return sorted(random.Random(seed).sample(keys, min(n, len(keys))))


def context(gl, t, i):
    gs = gl[t]
    span = range(max(0, i - WIDTH), min(len(gs), i + WIDTH + 1))
    return (" ".join(f"**{gs[j]['form']}**" if j == i else gs[j]["form"] for j in span),
            " · ".join(R.word_reading(gs[j]) for j in span))


def cut(g):
    return " + ".join(f"{p['form']} ({p.get('entry')})" for p in g.get("parts") or []) or "not cut"


def item_block(n, s, gl, rows, words, others):
    lines = [f"## Item {n}: stem `{s['stem']}`", "",
             f"Stands in {s['uses']} place{'s' if s['uses'] != 1 else ''}, in {s['texts']} text{'s' if s['texts'] != 1 else ''}. "
             "Cut from: " + "; ".join(f"`{f}` ({k})" for f, k in s["forms"].items()) + ".", "",
             "Places (text, kind of text; the words; the map's reading of each; how the map cut the word):", ""]
    for t, i in s["places"][:SHOWN]:
        ws, rs = context(gl, t, i)
        lines.append(f"- {t} ({rows[t].get('kind') or 'kind not known'}): {ws}\n  = {rs}\n  cut: {cut(gl[t][i])}")
    near = alikes(s["stem"], words)
    lines.append("\nLook-alikes among the lexicon's spellings (spelling: headword, kind, status, meaning):\n")
    lines += [f"- `{o}`: " + " / ".join(f"{e['headword']}, {e['kind'] or 'kind not given'}, {e['status'] or 'no status'}, {(e['meaning'] or 'no meaning')[:90]}"
                                      for e in words[o][:2]) for o in near] or ["- none"]
    lines.append("\nLook-alikes among the other unnamed stems (stem, places):\n")
    lines += [f"- `{o}` ({others[o]['uses']})" for o in alikes(s["stem"], others)] or ["- none"]
    return "\n".join(lines) + "\n"


def answered(folder):
    return folder.is_dir() and any(folder.glob("*.jsonl"))


def packs(rnd=LAST):
    """The packs of one reading: the same sample for every reading, the reading's own brief."""
    sub = ROUNDS[rnd]["folder"]
    if answered(OUT / f"{sub}answers1") or answered(OUT / f"{sub}answers2"):
        raise SystemExit("the packs are answered: they are not written again")
    gl, rows, pop = W.the_map(), W.corpus_rows(), read("population.json")
    words, _, _ = C.index(C.lexicon())
    stems = pop["stems"]
    chosen = sample_of(stems)
    groups = [chosen[i: i + PACK] for i in range(0, len(chosen), PACK)]
    if (OUT / "sample.json").exists() and read("sample.json") != groups:
        raise SystemExit("the sample is not the one already drawn")
    (OUT / f"{sub}packs").mkdir(parents=True, exist_ok=True)
    n = 0
    for k, group in enumerate(groups, 1):
        body = []
        for stem in group:
            n += 1
            body.append(item_block(n, stems[stem], gl, rows, words, stems))
        for c in (1, 2):
            (OUT / f"{sub}answers{c}").mkdir(exist_ok=True)
            text = ROUNDS[rnd]["brief"].format(n=len(group), answers=f"data/sources/words/{sub}answers{c}/S{k:02d}.jsonl") + "\n---\n\n" + "\n".join(body)
            (OUT / f"{sub}packs" / f"S{k:02d}_c{c}.md").write_text(text, encoding="utf-8")
    write("sample.json", groups)
    print(rnd, len(groups), "packs,", len(chosen), "stems of", len(stems))


# ---------------------------------------------------------------------------------------------------- the count

def sample_answers(folder, groups):
    """A checker's lines, kept only for the stems of the pack the file is named after, with a known case."""
    return W.own_lines(folder, groups, "S{n:02d}", "stem",
                       lambda r, n: r.get("stem") if r.get("stem") in groups[n - 1] and r.get("case") in CASES else None)


def verdict(a, b):
    """The bar for one sampled stem: it has a case only when both checkers give that case."""
    if not a or not b:
        return "not answered by both"
    return a["case"] if a["case"] == b["case"] else "not agreed"


def wilson(x, n, z=Z):
    """The Wilson interval of a share x / n (x may be a half count)."""
    if not n:
        return 0.0, 1.0
    p = x / n
    mid, half = p + z * z / (2 * n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (mid - half) / (1 + z * z / n)), min(1.0, (mid + half) / (1 + z * z / n))


def estimate(stems, verdicts):
    """How many of `stems` unnamed stems are distinct words of their own, from the sample's verdicts
    (verdict -> count). A stem that is the same word as another counts a half. The point takes the stems both
    checkers agree on and can decide; the low end takes every stem that is unclear or not agreed as no word, the
    high end takes every one of them as a word, each with the sample's 95% interval."""
    n = sum(verdicts.values())
    words = verdicts.get("word", 0) + verdicts.get("same", 0) / 2
    open_ = verdicts.get("unclear", 0) + verdicts.get("not agreed", 0)
    decided = n - open_
    return {"point": round(stems * words / decided) if decided else None,
            "low": round(stems * wilson(words, n)[0]), "high": round(stems * wilson(words + open_, n)[1])}


def star(translated_, dictionary, unnamed):
    """The north star: the share of distinct words that have a meaning. `unnamed` is estimate()'s result."""
    share = lambda u: round(translated_ / (dictionary + u), 4)          # noqa: E731
    return {"point": None if unnamed["point"] is None else share(unnamed["point"]), "low": share(unnamed["high"]), "high": share(unnamed["low"])}


def results(pop, groups, one, two):
    rows, pairs = [], []
    for stem in [s for g in groups for s in g]:
        a, b = one.get(stem), two.get(stem)
        if a and b:
            pairs.append((a["case"], b["case"]))
        rows.append({"stem": stem, "uses": pop["stems"][stem]["uses"], "verdict": verdict(a, b), "one": a, "two": b})
    kp = W.kappa(pairs)
    verdicts = dict(collections.Counter(r["verdict"] for r in rows))
    taken = bool(kp is not None and kp >= KAPPA and len(pairs) == len(rows))
    out = {"sampled": len(rows), "answered by both": len(pairs), "kappa": None if kp is None else round(kp, 4), "bar": KAPPA,
           "taken": taken, "verdicts": verdicts, "rows": rows}
    if taken:
        unnamed = estimate(pop["unnamed_stems"], verdicts)
        out |= {"unnamed_words": unnamed,
                "distinct_words": {k: None if v is None else pop["dictionary_words"] + v for k, v in unnamed.items()},
                "star": star(pop["translated"], pop["dictionary_words"], unnamed),
                "star_before": star(pop["before"]["translated"], pop["dictionary_words"], unnamed)}
    return out


def count(rnd=LAST):
    pop, groups, sub = read("population.json"), read("sample.json"), ROUNDS[rnd]["folder"]
    out = results(pop, groups, sample_answers(OUT / f"{sub}answers1", groups), sample_answers(OUT / f"{sub}answers2", groups))
    write(f"{sub}result.json", out)
    print(rnd, {k: v for k, v in out.items() if k != "rows"})


# ---------------------------------------------------------------------------------------------- the public figures

def stated_later(lex):
    """The dictionary words that the recurring-words work found stated by a later source in at least one place and
    that the lexicon of 2003 does not call established or probable: translated once that work is in the map."""
    f = json.loads(RECURRING.read_text(encoding="utf-8"))
    return sorted(s["item"] for s in f["class_a"]["stated"]
                  if s["places_stated"] and s["item"] in lex and (lex[s["item"]].get("status") or "") not in W.SURE)


def figures():
    """What the page reports, from the local results: counts only, with a few stems as examples."""
    pop, lex = read("population.json"), W.lexicon()
    by_round = {r: read(f"{ROUNDS[r]['folder']}result.json") for r in ROUNDS}
    res = by_round[LAST]
    if not res["taken"]:
        raise SystemExit("the last reading missed its bar: nothing is taken from it")
    later = stated_later(lex)
    nxt = pop["translated"] + len(later)
    return {"running": pop["running"], "dictionary_words": pop["dictionary_words"], "translated": pop["translated"],
            "unnamed_stems": pop["unnamed_stems"], "unnamed_in_one_place": pop["unnamed_in_one_place"],
            "unnamed_running_words": pop["unnamed_running_words"], "before": pop["before"],
            "sample": {k: res[k] for k in ("sampled", "answered by both", "kappa", "bar", "taken", "verdicts")} | {"seed": SEED, "reading": LAST},
            "readings": {r: {k: v[k] for k in ("sampled", "answered by both", "kappa", "bar", "taken", "verdicts")} for r, v in by_round.items()},
            "unnamed_words": res["unnamed_words"], "distinct_words": res["distinct_words"],
            "star": res["star"], "star_before": res["star_before"],
            "next": {"stated_later": len(later), "translated": nxt, "star": star(nxt, pop["dictionary_words"], res["unnamed_words"])},
            "tokens": {k: {"agents": a, "tokens": t} for k, (a, t) in TOKENS.items()}}


def public():
    PUBLIC.write_text(json.dumps(figures(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", PUBLIC.relative_to(ROOT))


COMMANDS = {"population": population, "packs": packs, "count": count, "public": public}

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3) or sys.argv[1] not in COMMANDS or (sys.argv[2:] and (sys.argv[1] not in ("packs", "count") or sys.argv[2] not in ROUNDS)):
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]](*sys.argv[2:])
