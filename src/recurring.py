"""The recurring open words: the spellings of corpus_v6 that have no accepted meaning and stand in three texts or
more, taken through five steps, each with two or more independent readers and a bar set before they answered
(data/discovery/recurring_words.md).

Every command reads and writes under data/sources/recurring/ (local only: the packs quote the lexicon of 2003 and
the editions), except `public`, which writes the figures of the page.

  python3 -I src/recurring.py items          the spellings in items, each with every place it stands (items.json)
  python3 -I src/recurring.py batches        the literature pass: one dossier a batch, for one reader each (lit/packs/)
  python3 -I src/recurring.py quotes         every quote looked for in the file named; the three classes (lit/checked.json)
  python3 -I src/recurring.py verify-packs   class A for two readers (lit/verify/packs/)
  python3 -I src/recurring.py verify         the two readers compared (lit/verify/result.json)
  python3 -I src/recurring.py place-packs    every place for two checkers (places/packs/)
  python3 -I src/recurring.py places         the two checkers compared (places/result.json)
  python3 -I src/recurring.py cand-packs     the choice test, step 1: packs for two readers (choice/cand_packs/)
  python3 -I src/recurring.py cands          what both readers list (choice/candidates.json)
  python3 -I src/recurring.py choice-packs   the choice test, step 2: the blind packs and their key (choice/packs/)
  python3 -I src/recurring.py choice         the readers' choices and the bars (choice/result.json)
  python3 -I src/recurring.py recount        an overlay on the map, which is not touched, and the recount (recount.json)
  python3 -I src/recurring.py public         data/discovery/recurring_words_figures.json

The brief of the literature pass and the line each agent was started with are in runs/prompts/RECURRING_*.md; the
other briefs are the constants below. A command that writes packs refuses once an agent of its step has answered
(`items`, on which every later step numbers its places, once any agent has): the answers would no longer be to the
packs they were given.
"""
import collections
import glob
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts")]
import f4r as R                                        # noqa: E402
import lexicon as X                                    # noqa: E402

OUT = ROOT / "data/sources/recurring"
PUBLIC = ROOT / "data/discovery/recurring_words_figures.json"
OPEN = ("hypothesis", "kind", "unknown")
READ = ("meaning", "grammar")
NAMED = ("name", "number")
SURE = ("established", "probable")
FIRM = ("accepts", "probable")
STOP = set("a an the of to in on for and or with by is are be as it its this that may you him her them he she they "
           "one who which from at not his".split())
SEED = 20261113

# The bars, each set before the agents of its step were started: committed for the place pass and the choice test,
# written in the working script for class A (WHEN; the page gives the commits and the times).
KAPPA = 0.6                                                 # the place pass: Cohen's kappa of the two checkers
BARS = {"right_when_chosen": 0.80, "chosen_at_least": 8,    # the choice test, on the accepted words
        "wrong_when_absent": 0.10}
# Subagent tokens of each step, from the task notifications, by hand after the runs (13 November 2026).
TOKENS = {"literature": (10, 2411497), "verifiers": (6, 613355), "place_checkers": (52, 4146199),
          "candidate_readers": (8, 780535), "choice_readers": (25, 1895080)}
# When each rule and bar was set, against when the agents of the step it applies to were started and first answered
# (2026-11-13, Pacific time): "set" is the commit's time in git, or the time of the working script's file (the
# class A bar, data/sources/recurring/old_scripts/verify.py) or of the session's command (the classes); "started" is
# the step's first launch in the session's log, by hand; "first_answer" is the earliest time of the step's answer
# files under data/sources/recurring/ (`answers`, from the root of that folder).
WHEN = [
    {"step": "the classes (section 3)", "set_in": "the working session, not committed", "set": "15:57:05",
     "started": "15:46:21", "first_answer": "15:53:08", "answers": ["lit/answers"]},
    {"step": "class A read twice (section 4)", "set_in": "the working script, not committed", "set": "15:58:05",
     "started": "15:58:10", "first_answer": "15:59:59", "answers": ["lit/verify/answers1", "lit/verify/answers2"]},
    {"step": "the place pass (section 5)", "set_in": "e3fdb9f", "set": "16:06:33",
     "started": "16:06:41", "first_answer": "16:07:27", "answers": ["places/answers1", "places/answers2"]},
    {"step": "the choice test, step 1 (section 6)", "set_in": "60f7bd8", "set": "16:14:24",
     "started": "16:15:12", "first_answer": "16:16:01", "answers": ["choice/cand1", "choice/cand2"]},
    {"step": "the choice test, step 2 (section 6)", "set_in": "fff9478", "set": "16:19:20",
     "started": "16:19:25", "first_answer": "16:20:29", "answers": [f"choice/reader{r}" for r in range(1, 6)]},
]


def read(path):
    return json.loads((OUT / path).read_text(encoding="utf-8"))


def write(path, data):
    (OUT / path).parent.mkdir(parents=True, exist_ok=True)
    (OUT / path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def content(text):
    """The content words of a short meaning, for comparing two wordings."""
    return {w for w in re.findall(r"[a-zà-ÿ]+", (text or "").lower()) if w not in STOP and len(w) > 1}


def own_lines(folder, groups, prefix, key, wanted):
    """A reader's JSON lines, kept only for what its own pack holds: file <prefix><n>.jsonl answers pack n, and
    `wanted(line, n)` gives the line's key when the line belongs to that pack, else None. The first line wins."""
    out = {}
    for n in range(1, len(groups) + 1):
        f = folder / f"{prefix.format(n=n)}.jsonl"
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            k = wanted(r, n) if isinstance(r, dict) else None
            if k is not None:
                out.setdefault(k, r)
    return out


def the_map():
    return {r["id"]: r["glosses"] for r in map(json.loads, X.GLOSSES.read_text(encoding="utf-8").splitlines())}


def heads_of(g):
    return [p.get("entry") for p in g.get("parts") or [] if p.get("entry") and p.get("entry") not in X.PSEUDO]


def affix(h):
    core = re.sub(r"\s*\(\d+\)$", "", h)
    return core.startswith("-") or core.endswith("-")


def not_again(step):
    """Stop before a command writes the packs of a step again once one of its agents has answered; `items`, whose
    places every later step is numbered on, stops once any agent has."""
    folders = {"batches": ["lit/answers"], "verify-packs": ["lit/verify/answers1", "lit/verify/answers2"],
               "place-packs": ["places/answers1", "places/answers2"], "cand-packs": ["choice/cand1", "choice/cand2"],
               "choice-packs": [f"choice/reader{r}" for r in range(1, READERS + 1)]}
    mine = [f for fs in folders.values() for f in fs] if step == "items" else folders[step]
    answered = [f for f in mine if any((OUT / f).glob("*.jsonl"))]
    if answered:
        raise SystemExit(f"{', '.join(answered)} hold answers: not writing the {step} again")


# -------------------------------------------------------------------------------------------------- the items

MIN_TEXTS = 3
WIDTH = 5


def spellings_of(gl):
    """Each spelling of the map: how often it has each level, the texts it stands in, and how often its parts are
    built on each sequence of entries."""
    level, texts = collections.defaultdict(collections.Counter), collections.defaultdict(set)
    heads = collections.defaultdict(collections.Counter)
    for t, gs in gl.items():
        for g in gs:
            level[g["form"]][g["level"]] += 1
            texts[g["form"]].add(t)
            heads[g["form"]][tuple(p.get("entry") for p in g.get("parts") or [] if p.get("entry"))] += 1
    return level, texts, heads


def map_figures(gl):
    """The map's spellings without an accepted meaning (the level they have most often is open), by the number of
    texts they stand in."""
    level, texts, _ = spellings_of(gl)
    opened = [f for f, c in level.items() if c.most_common(1)[0][0] in OPEN]
    many = sum(len(texts[f]) >= MIN_TEXTS for f in opened)
    return {"inscriptions": len(gl), "running_words": sum(map(len, gl.values())), "open_spellings": len(opened),
            "in_three_texts_or_more": many, "in_one_or_two_texts": len(opened) - many}


def key_of(form, heads, lex):
    """The item a spelling belongs to: its first stem the lexicon does not call established or probable; else its
    first stem; else its first affix; else the spelling itself."""
    real = [h for h in heads if h in lex]
    stems = [h for h in real if not affix(h)]
    for h in stems:
        if (lex[h].get("status") or "") not in SURE:
            return h, "stem"
    if stems:
        return stems[0], "stem, sure in the lexicon"
    for h in real:
        if (lex[h].get("status") or "") not in SURE:
            return h, "affix"
    if real:
        return real[0], "affix, sure in the lexicon"
    return form, "not in the lexicon"


def items_of(gl, rows, lex):
    """The open spellings that stand in MIN_TEXTS texts or more, grouped into items, each with every place: the
    word, WIDTH words on each side, and the map's reading of each."""
    level, texts, heads = spellings_of(gl)
    forms = sorted(f for f, c in level.items() if c.most_common(1)[0][0] in OPEN and len(texts[f]) >= MIN_TEXTS)
    items = collections.OrderedDict()
    for f in forms:
        hs = [h for h in heads[f].most_common(1)[0][0] if h not in X.PSEUDO]
        key, how = key_of(f, hs, lex)
        it = items.setdefault(key, {"item": key, "how": how, "forms": [], "places": []})
        it["forms"].append({"form": f, "texts": len(texts[f]), "uses": sum(level[f].values()),
                            "level": level[f].most_common(1)[0][0], "parts": hs})
    wanted = {f["form"]: k for k, it in items.items() for f in it["forms"]}
    for t in sorted(gl):
        gs = gl[t]
        for i, g in enumerate(gs):
            k = wanted.get(g["form"])
            if k is None:
                continue
            span = gs[max(0, i - WIDTH): i + WIDTH + 1]
            items[k]["places"].append({
                "text": t, "site": rows[t].get("site") or "", "kind": rows[t].get("kind") or "", "n": i + 1, "of": len(gs),
                "form": g["form"], "gloss": (g.get("gloss") or "").strip(), "note": (g.get("evidence") or "")[:200],
                "words": " ".join(f"**{x['form']}**" if x is g else x["form"] for x in span),
                "readings": " · ".join(R.word_reading(x) for x in span)})
    out = []
    for k, it in items.items():
        e = lex.get(k)
        it["texts"] = len({p["text"] for p in it["places"]})
        it["uses"] = len(it["places"])
        it["kinds_of_text"] = dict(collections.Counter(p["kind"] for p in it["places"]).most_common())
        it["sites"] = dict(collections.Counter(p["site"].split(":")[0].split(",")[0][:30] for p in it["places"]).most_common(6))
        it["lexicon"] = None if e is None else {"kind": e["kind"], "status": e["status"], "page": e["page"], "meaning": e["meaning"],
                                                "proposals": e["proposals"]}
        out.append(it)
    out.sort(key=lambda it: (-it["texts"], it["item"]))
    return out


def corpus_rows():
    return {r["id"]: r for r in map(json.loads, (ROOT / "data/corpus_v6.jsonl").read_text(encoding="utf-8").splitlines())}


def lexicon():
    return {e["headword"]: e for e in X.entries_of()}


def items():
    not_again("items")
    out = items_of(the_map(), corpus_rows(), lexicon())
    write("items.json", out)
    print(f"{sum(len(it['forms']) for it in out)} spellings in {len(out)} items; places {sum(it['uses'] for it in out)}")
    print(dict(collections.Counter(it["how"] for it in out)))


def the_items():
    return {it["item"]: it for it in read("items.json")}


# ------------------------------------------------------------------------------------------- the literature pass

LIT_PLACES = 12
BATCHES = {
    "verbs": ["ḫr", "ẖol", "d", "pl (2)", "tḫ (1)", "dotedi", "l (2)", "yiroẖe"],
    "verb_affixes": ["ps-", "-kete", "-ketese", "-kene", "ye- (2)", "a-", "p- (2)", "-m-"],
    "offerings": ["dole", "attḫ", "al", "yeto", "yed", "mlowi", "do (1)", "ato", "aḫide", "tmot", "tiso"],
    "particles": ["-wi (5)", "-w (1)", "n-", "-ni (1)", "se (4)", "-se (1)", "-bto", "no", "seb (1)", "-i (2)", "-lowi", "wi (1)"],
    "titles_a": ["pqr", "pqrtr", "mlomrse", "mr", "womnitẖ", "womnise", "mdek", "dkretri", "mreperi", "nk", "amero"],
    "titles_b": ["wetneyineqeli", "wetrri", "Aritene", "Ms", "Aqedise", "qomlise", "ptroti", "di", "qer", "mleke", "mlekye",
                 "medo", "aribet", "atepedemo", "wo-"],
    "nouns_a": ["s", "wte", "ti", "yet (2)", "ase", "sete", "tbo", "wide", "yini", "ado", "aleqese", "aḫro", "bnebeseni", "bqo"],
    "nouns_b": ["doke", "mde", "penn", "qr", "temey (2)", "tereki", "tr", "wido", "wse", "yeseboẖe", "yeso", "dete", "-tni-",
                "Akine", "Simlo", "Skl", "Atoẖe"],
    "pieces_a": ["be", "q", "teli", "mi", "reyi", "me", "Stqo", "atbe", "ble", "brtoye", "dd", "ds"],
    "pieces_b": ["dte", "ed", "ek", "et", "ki", "mo", "nlo", "re", "teqride", "ter", "tewi", "wwi", "xm"],
}
STANCES = ("accepts", "probable", "proposes", "doubts", "rejects", "mentions")
LATER = ("Rilly 2016", "Rilly 2021")
CLASSES = {"A": "A later source states a meaning", "B": "B a piece in some or all uses", "C": "C open"}


def spread(places, n):
    """At most n places, one a text first, evenly through the list."""
    seen, first, rest = set(), [], []
    for p in places:
        (rest if p["text"] in seen else first).append(p)
        seen.add(p["text"])
    pool = first + rest
    if len(pool) <= n:
        return pool
    step = len(first) / n if len(first) >= n else None
    return [first[int(i * step)] for i in range(n)] if step else pool[:n]


def lit_block(it):
    lx = it["lexicon"]
    lines = [f"### Item `{it['item']}`", "",
             "- Spellings (texts, uses): " + "; ".join(f"`{f['form']}` ({f['texts']}, {f['uses']})" for f in it["forms"]),
             f"- In {it['texts']} texts, {it['uses']} uses. Kinds of text: {it['kinds_of_text']}. Sites: {it['sites']}."]
    if lx:
        lines.append(f"- Rilly 2003, p. {lx['page']}: {lx['kind'] or 'kind not given'}; status {lx['status'] or 'none'}; meaning as typed: {lx['meaning'] or '(none)'}")
        if lx["proposals"]:
            lines.append("- Other scholars as that lexicon records them: " + "; ".join(f"{p['author']}: {p['proposal']}" for p in lx["proposals"]))
    else:
        lines.append("- Not an entry of Rilly's lexicon of 2003.")
    shown = spread(it["places"], LIT_PLACES)
    lines.append(f"- Places ({len(shown)} of {it['uses']} shown; the word in bold, five words on each side, then the map's reading of each):")
    for p in shown:
        lines.append(f"  - {p['text']} ({p['site'][:40]}; {p['kind']}; word {p['n']} of {p['of']}): {p['words']}")
        lines.append(f"    = {p['readings']}")
        if p["note"]:
            lines.append(f"    the map's note: {p['note']}")
    return "\n".join(lines) + "\n"


def batches():
    not_again("batches")
    its = the_items()
    used = [k for ks in BATCHES.values() for k in ks]
    print("items", len(its), "| in batches", len(set(used)), "| twice", sorted({k for k in used if used.count(k) > 1}),
          "| missing", sorted(set(its) - set(used)), "| unknown", sorted(set(used) - set(its)))
    (OUT / "lit" / "packs").mkdir(parents=True, exist_ok=True)
    (OUT / "lit" / "answers").mkdir(exist_ok=True)
    for name, keys in BATCHES.items():
        text = f"# Batch `{name}`: {len(keys)} items\n\n" + "\n".join(lit_block(its[k]) for k in keys if k in its)
        (OUT / "lit" / "packs" / f"{name}.md").write_text(text, encoding="utf-8")
    write("lit/batches.json", BATCHES)


def squash(text):
    return re.sub(r"\s+", " ", text or "").strip()


_pages = {}


def pages_of(path):
    """[(page number or None, squashed text)] of a file under the repository: its `=== page N ===` blocks, or the
    whole file. A path with * names several files."""
    if path not in _pages:
        files = sorted(glob.glob(str(ROOT / path))) if any(c in path for c in "*?[") else [str(ROOT / path)]
        blocks = []
        for f in files:
            p = pathlib.Path(f)
            if not p.is_file():
                continue
            parts = re.split(r"=== page (\d+) ===\n", p.read_text(encoding="utf-8", errors="replace"))
            if len(parts) > 1:
                blocks += [(int(parts[i]), squash(parts[i + 1])) for i in range(1, len(parts), 2)]
            else:
                blocks.append((None, squash(parts[0])))
        _pages[path] = blocks
    return _pages[path]


def find(quote, path):
    """(found, the page it stands on) for a quote in a file: character for character but for line breaks and runs
    of spaces; three words at least; it may run over one page break."""
    q = squash(quote)
    if len(q.split()) < 3:
        return False, None
    blocks = pages_of(path)
    for n, text in blocks:
        if q in text:
            return True, n
    for (n, a), (_, b) in zip(blocks, blocks[1:]):
        if q in a[-len(q) - 1:] + " " + b[:len(q) + 1]:
            return True, n
    return False, None


def class_of(entry):
    """The class of an item from its checked statements: A when Rilly 2016 or 2021 accepts a meaning or calls it
    probable; else B when the reader calls the spelling a piece of another word in some or all uses; else C."""
    if any(s["source"] in LATER and s["stance"] in FIRM for s in entry["statements"]):
        return CLASSES["A"]
    return CLASSES["B"] if entry["piece"] else CLASSES["C"]


def checked_of(row):
    """One reader's line for an item, with only the statements whose quote stands in the file named."""
    kept, c = [], collections.Counter()
    for s in row.get("statements") or []:
        if not isinstance(s, dict):
            continue
        c["statements"] += 1
        found, page = find(s.get("quote") or "", str(s.get("file") or ""))
        if not found:
            c["quote_not_found"] += 1
            continue
        cited = s.get("page")
        c["quote_found"] += 1
        c["page_corrected"] += bool(page is not None and isinstance(cited, int) and abs(cited - page) > 1)
        kept.append({"source": s.get("source"), "file": s.get("file"), "page": page if page is not None else cited,
                     "quote": squash(s.get("quote")), "says": s.get("says"),
                     "stance": s.get("stance") if s.get("stance") in STANCES else "mentions"})
    return {"statements": kept, "state": row.get("state") or "", "newer_than_2003": row.get("newer_than_2003") or "",
            "piece": row.get("piece") or "", "kind": row.get("kind") or "", "tests": row.get("tests") or []}, c


def quotes():
    got = {}
    for name, keys in BATCHES.items():
        f = OUT / "lit" / "answers" / f"{name}.jsonl"
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(r, dict) and r.get("item") in keys:
                got.setdefault(r["item"], (name, r))
    out, c = {}, collections.Counter()
    for k in [k for ks in BATCHES.values() for k in ks]:
        if k not in got:
            c["items_not_answered"] += 1
            continue
        name, r = got[k]
        out[k], n = checked_of(r)
        out[k] = {"batch": name} | out[k]
        c.update(n)
        c["items"] += 1
        c["items_with_a_checked_statement"] += bool(out[k]["statements"])
    write("lit/checked.json", out)
    write("lit/classes.json", {k: class_of(v) for k, v in out.items()})
    write("lit/counts.json", dict(c) | {"batches": len(BATCHES)})
    print(dict(c), dict(collections.Counter(class_of(v)[0] for v in out.values())))


# ------------------------------------------------------------------------------------------ class A, read twice

VERIFY_PACK = 10
VERIFY_PLACES = 6
VERIFY_BRIEF = """# Check what a later source states about {n} Meroitic items

Each item below is a word or an ending that the lexicon of 2003 holds without an accepted meaning. A first pass
found statements about it in later sources, with quotes that a script has found in the files. Your task is to read
each quote in its place (open the file, read the page around it) and say what the source really states.

For each item give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

    {{"item": "<its name as given here>", "meaning": "<the meaning or the function the later source states, in your own words, at most twelve words; empty if it states none>", "source": "<Rilly 2016 or Rilly 2021, the one that states it most firmly>", "page": 12, "stance": "accepts", "covers": {{"<spelling>": "all"}}, "second": "<another scholar among the statements who gives the same meaning, with the source's name; else empty>", "note": "<at most twenty-five words: any reserve the source makes, or why a spelling is not covered>"}}

- "stance": "accepts" when the source states the meaning without reserve (in running text or as a gloss in an
  analysed example); "probable" when it says probably, seems, likely; "proposes" when it is a suggestion, a
  question mark, a "perhaps"; "none" when the quotes do not state a meaning or a function for this item.
- "covers": for each spelling of the item listed here, "all", "some" or "none": in how many of the places shown is
  the spelling the word the source speaks of? A spelling that is a piece of another word in a place is not covered
  there.
- Use only the files named in the statements and the places shown. Do not use your own knowledge of Meroitic, do
  not search the web, do not run the project's scripts, and write no other file.

Letters: the project writes `S` for the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ; Rilly 2021 writes h
for ẖ and x for ḫ, and cuts words with hyphens. In the files with `=== page N ===` markers a quote's page is the
nearest marker above it. The repository's root is /Users/mike/repos/mike/meroitic.

When the file is written, reply in one line: how many items, and how many of each stance.
"""
COVER = {"all": 2, "some": 1, "none": 0}


def spellings_line(it):
    return "Spellings (texts, uses): " + "; ".join(f"`{f['form']}` ({f['texts']}, {f['uses']})" for f in it["forms"])


def statement_lines(ch):
    return [f"- {s['source']} | `{s['file']}` | p. {s['page']} | \"{s['quote']}\" | {s['says']} | {s['stance']}" for s in ch["statements"]]


def verify_block(it, ch):
    lines = [f"## Item `{it['item']}`", "", spellings_line(it), ""]
    lx = it["lexicon"]
    if lx:
        lines.append(f"The lexicon of 2003 (p. {lx['page']}): {lx['kind']}; {lx['status']}; {lx['meaning']}\n")
    lines.append("Places (the word in bold; then the map's reading of each word):\n")
    seen = set()
    for p in it["places"]:
        if p["form"] in seen and len(seen) < len(it["forms"]):
            continue
        seen.add(p["form"])
        lines.append(f"- {p['text']} ({p['kind']}): {p['words']}\n  = {p['readings']}")
        if sum(1 for l in lines if l.startswith("- ")) >= max(VERIFY_PLACES, len(it["forms"])):
            break
    lines.append("\nStatements found (source, file, page, the quote, what the first pass took it to say, its stance):\n")
    return "\n".join(lines + statement_lines(ch)) + "\n"


def class_a(its, classes):
    return sorted((k for k, c in classes.items() if c == CLASSES["A"]), key=lambda k: (-its[k]["uses"], k))


def verify_packs():
    not_again("verify-packs")
    its, checked = the_items(), read("lit/checked.json")
    keys = class_a(its, read("lit/classes.json"))
    (OUT / "lit" / "verify" / "packs").mkdir(parents=True, exist_ok=True)
    groups = [keys[i: i + VERIFY_PACK] for i in range(0, len(keys), VERIFY_PACK)]
    for n, group in enumerate(groups, 1):
        body = "\n".join(verify_block(its[k], checked[k]) for k in group)
        for v in (1, 2):
            (OUT / "lit" / "verify" / f"answers{v}").mkdir(exist_ok=True)
            text = VERIFY_BRIEF.format(n=len(group), answers=f"data/sources/recurring/lit/verify/answers{v}/A{n}.jsonl") + "\n---\n\n" + body
            (OUT / "lit" / "verify" / "packs" / f"A{n}_v{v}.md").write_text(text, encoding="utf-8")
    write("lit/verify/groups.json", groups)


def stated(a, b):
    """The bar of class A, written in the working script before the readers were started (WHEN): an item counts as
    "stated" by a later source only when both readers give the stance "accepts" or "probable" for the same source.
    That script set apart for a third reader an item whose two meanings share no content word (it counted words of
    three letters or more); here such an item is "stated, the meanings differ", not stated. No item of the 29 fell
    there, under either count of the words."""
    both = a.get("stance") in FIRM and b.get("stance") in FIRM and a.get("source") == b.get("source")
    same = bool(content(a.get("meaning")) & content(b.get("meaning")))
    return "stated" if both and same else "stated, the meanings differ" if both else "not stated firmly"


def covered(forms, a, b):
    """Running words of an item by how far the stated meaning covers the places shown: the lower of the two
    readers' answers for each spelling."""
    out = collections.Counter()
    for f in forms:
        low = min(COVER.get((a.get("covers") or {}).get(f["form"]), -1), COVER.get((b.get("covers") or {}).get(f["form"]), -1))
        out[{2: "all", 1: "some", 0: "none"}.get(low, "not said")] += f["uses"]
    return dict(out)


def verify():
    its = the_items()
    groups = read("lit/verify/groups.json")
    ans = [own_lines(OUT / "lit" / "verify" / f"answers{v}", groups, "A{n}", "item",
                     lambda r, n: r.get("item") if r.get("item") in groups[n - 1] else None) for v in (1, 2)]
    out, c = {}, collections.Counter()
    for k in [k for g in groups for k in g]:
        a, b = ans[0].get(k), ans[1].get(k)
        if not a or not b:
            c["not answered by both"] += 1
            continue
        out[k] = {"verdict": stated(a, b), "uses": its[k]["uses"], "covered": covered(its[k]["forms"], a, b), "one": a, "two": b}
        c[out[k]["verdict"]] += 1
    write("lit/verify/result.json", out)
    print(dict(c))


# ------------------------------------------------------------------------------------------------ the place pass

PLACE_PACK = 50
CASES = ("stated", "piece", "open", "unclear")
PLACE_BRIEF = """# Decide, place by place, what {n} spellings of Meroitic are

The project's word-by-word map of the Meroitic corpus holds no accepted meaning for the spellings below. Each
stands in three texts or more. A first pass collected what the sources say about each item, with quotes that a
script has found in the files. Your task is to decide, for every place listed, what the spelling is **in that
place**.

For every place give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

    {{"item": "<the item's name as given here>", "place": 3, "case": "piece", "whole": "woSi", "meaning": "Isis", "why": "<at most twenty words>"}}

- "case" is one of:
  - "stated": the spelling here is the word (or the ending) of which the later source named in the item's header
    speaks, in the use it describes. Only possible when the header has a line "A later source states". Put that
    meaning in "meaning".
  - "piece": the spelling here is no word of its own: the edition's word division has cut a longer word or a name,
    and this is a part of it. Put the whole word, joined, in the project's letters, in "whole" (for `wo` before
    `Si`: "woSi"), and in "meaning" what the map, the lexicon of 2003 or a source in the header says of the whole
    (empty if nothing).
  - "open": the spelling here is a word (or an ending) of its own, and no source in the header states a meaning
    that applies to this place. A meaning that is only proposed, doubted, or stated for another use is "open".
  - "unclear": signs are lost around it, or the context shown is too thin to decide between the cases above.
- Decide each place on what is shown for it: the words around it, the map's reading of each, the header's
  statements. The first pass's summary ("Said of it") is a claim to check, not a fact: it may be wrong for a place.
- You may open the files named in the statements, and search the lexicon of 2003 (`data/rilly2003/`, JSON lines)
  for a joined word. Do not use your own knowledge of Meroitic, do not search the web, do not run the project's
  scripts, and write no other file.
- "whole" is empty unless the case is "piece"; "meaning" is empty for "open" and "unclear".

Letters: the project writes `S` for the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ; Rilly 2021 writes h
for ẖ and x for ḫ, and cuts words with hyphens. In a place, the spelling is in bold; `[...]` in the readings marks
a word the map has no accepted meaning for. The repository's root is /Users/mike/repos/mike/meroitic.

When the file is written, reply in one line: how many places, and how many of each case.
"""


def place_header(it, ch, ver):
    lines = [f"## Item `{it['item']}`", "", spellings_line(it), ""]
    lx = it["lexicon"]
    if lx:
        lines.append(f"The lexicon of 2003 (p. {lx['page']}): {lx['kind']}; {lx['status'] or 'no status'}; {lx['meaning'] or 'no meaning'}\n")
    else:
        lines.append("The lexicon of 2003 has no entry for it.\n")
    if ver and ver["verdict"] == "stated":
        a, b = ver["one"], ver["two"]
        lines.append(f"A later source states ({a['source']}, p. {a['page']}; {a['stance']}/{b['stance']}): {a['meaning']}. "
                     f"Two readers' reserves: {a['note']} / {b['note']}\n")
    if ch.get("state"):
        lines.append(f"Said of it (first pass, to check): {ch['state']}")
    if ch.get("piece"):
        lines.append(f"Said to be a piece (first pass, to check): {ch['piece']}")
    lines.append("\nStatements found (source, file, page, the quote, what the first pass took it to say, its stance):\n")
    return "\n".join(lines + statement_lines(ch)) + "\n"


def place_lines(it, lo, hi):
    out = [f"\nPlaces {lo + 1} to {hi} of {len(it['places'])} (text, kind of text, the word's number in the text; the words; the map's reading of each):\n"]
    for k in range(lo, hi):
        p = it["places"][k]
        out.append(f"- place {k + 1}: {p['text']} ({p['kind']}; word {p['n']} of {p['of']}): {p['words']}\n  = {p['readings']}")
    return "\n".join(out) + "\n"


def place_groups(its, size=PLACE_PACK):
    """Packs of at most `size` places, as [item, from, to] runs: an item stays whole unless it is larger than a
    pack, and then it is cut into runs of `size` places, each run a pack of its own."""
    packs, cur, held = [], [], 0
    for it in sorted(its.values(), key=lambda it: (-it["uses"], it["item"])):
        n = len(it["places"])
        if n > size:
            packs += [[[it["item"], lo, min(n, lo + size)]] for lo in range(0, n, size)]
            continue
        if held + n > size and cur:
            packs.append(cur)
            cur, held = [], 0
        cur.append([it["item"], 0, n])
        held += n
    return packs + ([cur] if cur else [])


def place_packs():
    not_again("place-packs")
    its, checked, verified = the_items(), read("lit/checked.json"), read("lit/verify/result.json")
    (OUT / "places" / "packs").mkdir(parents=True, exist_ok=True)
    groups = place_groups(its)
    for n, group in enumerate(groups, 1):
        body = "\n".join(place_header(its[k], checked[k], verified.get(k)) + place_lines(its[k], lo, hi) for k, lo, hi in group)
        for c in (1, 2):
            (OUT / "places" / f"answers{c}").mkdir(exist_ok=True)
            text = PLACE_BRIEF.format(n=len({k for k, _, _ in group}), answers=f"data/sources/recurring/places/answers{c}/P{n:02d}.jsonl") + "\n---\n\n" + body
            (OUT / "places" / "packs" / f"P{n:02d}_c{c}.md").write_text(text, encoding="utf-8")
    write("places/groups.json", groups)
    print(len(groups), "packs,", sum(hi - lo for g in groups for _, lo, hi in g), "places")


def joined(whole):
    return re.sub(r"[\s\-.:]+", "", whole or "")


def kappa(pairs):
    """Cohen's kappa of two readers over (first's answer, second's answer) pairs; None without pairs."""
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = collections.Counter(a for a, _ in pairs), collections.Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def place_verdict(a, b, passed):
    """The place pass's bar, set before the checkers answered. A place is "stated" only when both say so and the
    item passed class A's bar (`passed`); a "piece" only when both say so and name the same whole word; "open" or
    "unclear" only when both say so; every other answered place is "not agreed"."""
    if not a or not b:
        return "not answered by both"
    if a["case"] != b["case"]:
        return "not agreed"
    if a["case"] == "stated":
        return "stated" if passed else "not agreed"
    if a["case"] == "piece":
        return "piece" if joined(a.get("whole")) and joined(a.get("whole")) == joined(b.get("whole")) else "not agreed"
    return a["case"]


def place_answers(folder, groups):
    """A checker's lines, kept only for the places of the pack the file is named after, with a known case."""
    def wanted(r, n):
        ok = any(r.get("item") == k and isinstance(r.get("place"), int) and lo < r["place"] <= hi for k, lo, hi in groups[n - 1])
        return (r["item"], r["place"]) if ok and r.get("case") in CASES else None
    return own_lines(folder, groups, "P{n:02d}", "item", wanted)


def place_rows(its, classes, verified, one, two):
    rows, pairs = [], []
    for k, it in its.items():
        passed = bool(verified.get(k)) and verified[k]["verdict"] == "stated"
        for i, p in enumerate(it["places"], 1):
            a, b = one.get((k, i)), two.get((k, i))
            v = place_verdict(a, b, passed)
            if a and b:
                pairs.append((a["case"], b["case"]))
            rows.append({"item": k, "class": classes[k][0], "place": i, "text": p["text"], "n": p["n"], "form": p["form"], "verdict": v,
                         "whole": joined(a.get("whole")) if v == "piece" else "",
                         "meaning": verified[k]["one"]["meaning"] if v == "stated" else a.get("meaning", "") if v == "piece" else "",
                         "one": a, "two": b})
    return rows, pairs


def place_summary(rows, pairs):
    """The pass's figures and its bar: it is taken only when both checkers answered every place and their kappa is
    KAPPA or more."""
    kp = kappa(pairs)
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        by[r["class"]][r["verdict"]] += 1
    return {"places": len(rows), "answered by both": len(pairs), "kappa": None if kp is None else round(kp, 4), "bar": KAPPA,
            "taken": bool(kp is not None and kp >= KAPPA and len(pairs) == len(rows)),
            "verdicts": dict(collections.Counter(r["verdict"] for r in rows)), "by class": {k: dict(v) for k, v in sorted(by.items())},
            "rows": rows}


def places():
    its, groups = the_items(), read("places/groups.json")
    rows, pairs = place_rows(its, read("lit/classes.json"), read("lit/verify/result.json"),
                             place_answers(OUT / "places" / "answers1", groups), place_answers(OUT / "places" / "answers2", groups))
    out = place_summary(rows, pairs)
    write("places/result.json", out)
    print({k: v for k, v in out.items() if k != "rows"})


def taken_places():
    res = read("places/result.json")
    if not res["taken"]:
        raise SystemExit("the place pass missed its bar: nothing is taken from it")
    return res


def open_places(rows, least=3):
    """item -> the numbers of its places that the place pass calls open, for the items with `least` or more."""
    out = collections.defaultdict(list)
    for r in rows:
        if r["verdict"] == "open":
            out[r["item"]].append(r["place"])
    return {k: v for k, v in out.items() if len(v) >= least}


# ------------------------------------------------------------------------------- the choice test, step 1: candidates

CAND_PACK = 17
SHOWN = 12
NAMES = ("place", "god", "person")
CAND_BRIEF = """# List the meanings on record for {n} Meroitic items

Each item below is a word or an ending of Meroitic without an accepted meaning. A first pass collected what the
sources say about it, with quotes that a script has found in the files; a second pass found the places listed here
to hold the item as a word of its own, with no source stating a meaning for them. Your task is to list, for each
item, the meanings that the sources **propose** for it, and to say whether they take it for a proper name.

For each item give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

    {{"item": "<its name as given here>", "name": "no", "name_stance": "none", "candidates": [{{"meaning": "notable", "kind": "title", "source": "Rilly 2003", "stance": "proposes"}}], "note": "<at most twenty words>"}}

- "candidates": at most three, the firmest first. A candidate is a meaning one could put in a translation of the
  open places: a word or a phrase of at most four words ("notable", "to offer", "two", "silver"). It must be given
  for the item by a source in the statements or in the lexicon's line, for the use the open places show. A kind is
  not a candidate ("a title", "a priestly title", "an offering", "an epithet of Osiris", "a verb of the
  benedictions"): leave "candidates" empty when the sources give only that.
  - "kind": noun, title, verb, adjective, numeral or function word.
  - "source": the source that gives it, as named in the statements. "stance": that source's own: accepts,
    probable, proposes or doubts.
- "name": "place", "god" or "person" when the sources take the item, in its open places, for the proper name of a
  place, a god or a person; else "no". An epithet or a title is not a name. "name_stance": "accepts" when a source
  states it without reserve, "probable", "proposes", or "none" when "name" is "no".
- Use only what is shown here and the files named in the statements. Do not use your own knowledge of Meroitic, do
  not search the web, do not run the project's scripts, and write no other file.

Letters: the project writes `S` for the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ. The repository's
root is /Users/mike/repos/mike/meroitic.

When the file is written, reply in one line: how many items, how many with a candidate, how many names.
"""


def cand_block(it, ch, places):
    lines = [f"## Item `{it['item']}`", "", spellings_line(it), ""]
    lx = it["lexicon"]
    if lx:
        lines.append(f"The lexicon of 2003 (p. {lx['page']}): {lx['kind']}; {lx['status'] or 'no status'}; {lx['meaning'] or 'no meaning'}")
        lines += [f"  - a proposal it records ({p['author']}): {p['proposal']}" for p in lx.get("proposals") or []]
        lines.append("")
    else:
        lines.append("The lexicon of 2003 has no entry for it.\n")
    lines.append("Statements found (source, file, page, the quote, what the first pass took it to say, its stance):\n")
    lines += statement_lines(ch)
    lines.append(f"\nThe open places ({len(places)}; the word in bold; then the map's reading of each word):\n")
    for k in places[:SHOWN]:
        p = it["places"][k - 1]
        lines.append(f"- {p['text']} ({p['kind']}): {p['words']}\n  = {p['readings']}")
    return "\n".join(lines) + "\n"


def cand_packs():
    not_again("cand-packs")
    its, checked = the_items(), read("lit/checked.json")
    opened = open_places(taken_places()["rows"])
    (OUT / "choice" / "cand_packs").mkdir(parents=True, exist_ok=True)
    order = sorted(opened, key=lambda k: (-len(opened[k]), k))
    groups = [order[i: i + CAND_PACK] for i in range(0, len(order), CAND_PACK)]
    for n, group in enumerate(groups, 1):
        body = "\n".join(cand_block(its[k], checked[k], opened[k]) for k in group)
        for c in (1, 2):
            (OUT / "choice" / f"cand{c}").mkdir(exist_ok=True)
            text = CAND_BRIEF.format(n=len(group), answers=f"data/sources/recurring/choice/cand{c}/C{n}.jsonl") + "\n---\n\n" + body
            (OUT / "choice" / "cand_packs" / f"C{n}_r{c}.md").write_text(text, encoding="utf-8")
    write("choice/cand_groups.json", groups)
    print(len(opened), "items,", sum(map(len, opened.values())), "open places")


def both_list(a, b):
    """What both readers list for one item, by the rule set beforehand: the candidates of the first reader that
    share a content word with one of the second's (three at most, in the first's wording), and the name both give
    with the stance "accepts" or "probable"."""
    kept = []
    for c in (a or {}).get("candidates") or []:
        if not isinstance(c, dict) or not content(c.get("meaning")):
            continue
        for d in (b or {}).get("candidates") or []:
            if isinstance(d, dict) and content(c.get("meaning")) & content(d.get("meaning")):
                kept.append({"meaning": c["meaning"].strip(), "kind": c.get("kind") or "", "source": c.get("source") or "",
                             "stance": c.get("stance") or "", "second": d["meaning"].strip()})
                break
    name = ""
    if a and b and a.get("name") in NAMES and a.get("name") == b.get("name") and a.get("name_stance") in FIRM and b.get("name_stance") in FIRM:
        name = a["name"]
    return {"candidates": kept[:3], "name": name}


def cands():
    opened = open_places(taken_places()["rows"])
    groups = read("choice/cand_groups.json")
    ans = [own_lines(OUT / "choice" / f"cand{c}", groups, "C{n}", "item",
                     lambda r, n: r.get("item") if r.get("item") in groups[n - 1] else None) for c in (1, 2)]
    out, c = {}, collections.Counter()
    for k in opened:
        a, b = ans[0].get(k), ans[1].get(k)
        if not a or not b:
            c["not answered by both"] += 1
            continue
        out[k] = both_list(a, b) | {"open": len(opened[k]), "one": a, "two": b}
        c["with a candidate kept" if out[k]["candidates"] else "no candidate kept"] += 1
        c["a name by the sources"] += bool(out[k]["name"])
    write("choice/candidates.json", out)
    print(dict(c))


# ------------------------------------------------------------------------------- the choice test, step 2: the choice

CHOICE_WIDTH = 6
READERS = 5
PACKS = 5
NEEDED = 4                     # of the five readers, for a choice
KINDS = ("noun", "title", "verb", "adjective")
# Candidates that leave a Meroitic word untranslated: not a meaning, and they would show the hidden word's spelling.
# Taken out on 2026-11-13 after the candidates were merged and before any reader of step 2 answered.
UNTRANSLATED = ("great womnise", "ate of Primis", "great paqar")
# The accepted words of the test: lexicon entry -> (the meaning as an option, its kind). Each is "established" or
# "probable" in the lexicon of 2003, and the test takes only the places where the map reads it. One, `ato`, is
# also the entry of a recurring item (a spelling of it that the map holds open).
ACCEPTED = {
    "kdi": ("woman", "noun"), "sem": ("wife", "noun"), "mk": ("god", "noun"), "kdise": ("sister", "noun"),
    "abr": ("man", "noun"), "adb": ("land, province", "noun"), "ns": ("sacrifice", "noun"),
    "pwrite (2)": ("life", "noun"), "teneke": ("west", "noun"), "dime": ("cow", "noun"), "ḫlbi": ("bull", "noun"),
    "ntki": ("strength", "noun"), "qore": ("ruler", "noun"), "ato": ("water", "noun"),
    "yetmde": ("nephew, niece", "noun"), "ḫmlol": ("a good meal", "noun"), "tewiseti": ("adoration, praise", "noun"),
    "nob": ("a Nubian", "noun"), "mdese": ("direct descendant", "noun"), "mte": ("child", "noun"),
    "pelmos": ("general", "title"), "apote": ("envoy", "title"), "ssor": ("scribe", "title"),
    "perite": ("agent", "title"), "ḫrpḫne": ("governor", "title"), "peseto": ("viceroy", "title"),
    "ant": ("priest", "title"), "plsn": ("temple administrator", "title"),
    "ked": ("to kill", "verb"), "tkk": ("to plunder", "verb"), "tk (2)": ("to love, to revere", "verb"),
    "tre": ("to give", "verb"), "ḫrpḫe": ("to order, to command", "verb"), "ẖe (1)": ("to drink", "verb"),
    "mlo": ("good", "adjective"), "mḫe": ("abundant", "adjective"), "sḫi": ("small, young", "adjective"),
    "lẖ": ("great, elder", "adjective"),
}
CHOICE_BRIEF = """# Which meaning fits? {n} Meroitic words, each shown only by the words around it

Each word below is hidden behind a code (`W017`). You do not see how it is written, nor which inscription a place
comes from. You see up to twelve places where it stands: the kind of text, then the reading of the six words
before and after it, as a word-by-word map of the Meroitic corpus has them, with the hidden word in bold.

Marks in the readings:

- `(?)` after a reading: the map is unsure of it;
- `[?]`: a word the map has no reading for; `[signs lost]`: a damaged word;
- `[title]` and the like, in square brackets: only the kind of word is known;
- `(a name)`: the name of a person; `[a word of this test]`: another hidden word; `[reading withheld]`: a reading
  that would spell out a hidden word;
- the hidden word may carry what the map cuts off it, written in Meroitic letters before or after the code
  (`W017-lowi`). What the map says of such pieces where they stand alone:
{legend}

Under each word stand four meanings, A to D. Decide from the places shown which of the four the hidden word has.
For some words the true meaning is not among the four. Pick a meaning only if the places shown give a reason for
it over the other three; otherwise answer "none".

For each word give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

    {{"code": "W017", "pick": "B", "sure": 2, "why": "<at most twenty words: what in the places decides it>"}}

- "pick": "A", "B", "C", "D" or "none".
- "sure": 3 when the places point to this meaning and against the others; 2 when it is more likely than the
  others; 1 when it is little more than a guess. For "none" give how sure you are that none of the four fits.
- Use only what is shown here. Do not try to work out which word or which inscription it is, do not use what you
  may know of published translations of Meroitic, do not open any other file, do not search the web, and write no
  file but your answers.

When the file is written, reply in one line: how many words, and how many of each pick.
"""


def strip_remarks(gloss):
    """A neighbour's gloss without what stands in round brackets (remarks that may name a spelling or a guess),
    keeping the mark "(?)"."""
    unsure = gloss.rstrip().endswith("(?)")
    text = re.sub(r"\s*\([^()]*\)", "", gloss).strip(" ,;")
    return (text + " (?)").strip() if unsure else text


def names_one(text, tokens):
    """Does a reading spell out one of the pack's hidden words (a headword or a spelling of three letters or more)?"""
    return any(re.search(rf"(?<![A-Za-zḫẖšñ]){re.escape(tok)}(?![A-Za-zḫẖšñ])", text) for tok in tokens)


def blind_reading(g, hidden, tokens=()):
    """One neighbour as a reader sees it: never its spelling; a word built on an entry of this pack is hidden, and
    a reading that spells out a hidden word is withheld."""
    if set(heads_of(g)) & hidden:
        return "[a word of this test]"
    level, gloss = g["level"], (g.get("gloss") or "").strip()
    if names_one(gloss, tokens):
        return "[reading withheld]"
    if level == "lost":
        return "[signs lost]"
    if level == "name" and gloss in ("NAME", "RNAME"):
        return "(a name)"
    text = strip_remarks(gloss)
    if level == "unknown" or text in ("", "?", "(?)"):
        return "[?]"
    if level == "kind":
        return f"[{text.strip('[]')}]"
    if level == "hypothesis":
        return text if text.endswith("(?)") else f"{text} (?)"
    return text


def shown_as(g, entry, code):
    """The hidden word: its code, with the pieces the map cuts off it in Meroitic letters."""
    parts = g.get("parts") or []
    where = [i for i, p in enumerate(parts) if p.get("entry") == entry]
    if not where:
        return code
    i = where[0]
    return "".join(p["form"] + "-" for p in parts[:i]) + code + "".join("-" + p["form"] for p in parts[i + 1:])


def blind_line(gs, i, entry, code, hidden, tokens=()):
    out = []
    for j in range(max(0, i - CHOICE_WIDTH), min(len(gs), i + CHOICE_WIDTH + 1)):
        g = gs[j]
        if j == i:
            out.append(f"**{shown_as(g, entry, code)}**")
        elif entry in heads_of(g):
            out.append(shown_as(g, entry, code))
        else:
            out.append(blind_reading(g, hidden, tokens))
    return " · ".join(out)


def accepted_places(gl, lex):
    """entry -> the (text, index) of every word the map reads (level meaning) that is built on that entry alone."""
    out = collections.defaultdict(list)
    for t in sorted(gl):
        for i, g in enumerate(gl[t]):
            if g["level"] == "meaning":
                s = [h for h in heads_of(g) if h in lex and not affix(h)]
                if len(s) == 1 and s[0] in ACCEPTED:
                    out[s[0]].append((t, i))
    return out


def sample(places, rng):
    """SHOWN places at most, one a text first, then more from the same texts."""
    places = list(places)
    rng.shuffle(places)
    first, rest, seen = [], [], set()
    for p in places:
        (rest if p[0] in seen else first).append(p)
        seen.add(p[0])
    return sorted((first + rest)[:SHOWN])


def others_of(kind, rng):
    """The accepted meanings as fillers: those of the same kind first, in a drawn order, then the rest."""
    same = sorted({m for m, k in ACCEPTED.values() if k == kind})
    rest = sorted({m for m, k in ACCEPTED.values() if k != kind})
    rng.shuffle(same)
    rng.shuffle(rest)
    return same + rest


def fill(have, kind, rng, avoid=""):
    """Four options: those given, filled up with accepted meanings of the same kind (of another kind only when
    the kind has too few) that share no content word with an option or with `avoid`."""
    opts = list(have)
    for m in others_of(kind, rng):
        if len(opts) == 4:
            break
        if not content(m) & content(avoid) and not any(content(m) & content(o) for o in opts):
            opts.append(m)
    return opts


def distinct(meanings):
    """The candidates without one whose content words another, earlier one already has, and without those that
    leave a Meroitic word untranslated (UNTRANSLATED)."""
    out = []
    for m in meanings:
        if m in UNTRANSLATED or any(content(m) <= content(o) or content(o) <= content(m) for o in out):
            continue
        out.append(m)
    return out


def left_out(cand):
    """Why an open item stays out of the test (None: it goes in), by the rules added before any reader of step 2
    answered: no candidate kept; a name by the sources; a first candidate of a kind the accepted words do not have
    (a function word, that is an ending or a particle, or a numeral); no candidate left once those that leave a
    word untranslated or repeat another are taken out."""
    c = cand["candidates"]
    if not c:
        return "no candidate kept"
    if cand["name"]:
        return "a name by the sources"
    if c[0]["kind"] not in KINDS:
        return f"first candidate a {c[0]['kind'] or 'word of no kind'}"
    if not distinct([x["meaning"] for x in c]):
        return "no candidate left after the removals"
    return None


def choice_words(gl, lex, its, cands, opened):
    """Every word of the test: the open items that left_out() lets in, and the accepted words, two in three with
    the true meaning offered and one in three without it. Codes and packs are dealt after a shuffle."""
    rng = random.Random(SEED)
    out = []
    for k in sorted(cands):
        if left_out(cands[k]):
            continue
        c = cands[k]["candidates"]
        meanings = distinct([x["meaning"] for x in c])
        places = [(its[k]["places"][n - 1]["text"], its[k]["places"][n - 1]["n"] - 1) for n in opened[k]]
        kind = c[0]["kind"]
        out.append({"sort": "open", "entry": k, "kind": kind, "candidates": meanings, "true": None,
                    "places": sample(places, rng), "options": fill(meanings, kind, rng)})
    acc = accepted_places(gl, lex)
    by_kind = collections.defaultdict(list)
    for h in sorted(ACCEPTED):
        if len({t for t, _ in acc.get(h, [])}) >= MIN_TEXTS:
            by_kind[ACCEPTED[h][1]].append(h)
    for kind in sorted(by_kind):
        hs = by_kind[kind]
        rng.shuffle(hs)
        for n, h in enumerate(hs):
            true = ACCEPTED[h][0]
            absent = n % 3 == 2
            opts = fill([], kind, rng, avoid=true) if absent else fill([true], kind, rng)     # drawn before the places
            out.append({"sort": "absent" if absent else "offered", "entry": h, "kind": kind, "candidates": [], "true": true,
                        "places": sample(acc[h], rng), "options": opts})
    rng.shuffle(out)
    for n, w in enumerate(out, 1):
        w["code"] = f"W{n:03d}"
        w["pack"] = (n - 1) % PACKS + 1
    return out


def legend(ws, gl):
    """What the map says of the cut-off pieces shown in a pack, where such a piece stands alone as a word it reads."""
    alone = collections.defaultdict(collections.Counter)
    for gs in gl.values():
        for g in gs:
            if g["level"] == "grammar":
                alone[g["form"]][strip_remarks((g.get("gloss") or "").strip())] += 1
    seen = collections.Counter()
    for w in ws:
        for t, i in w["places"]:
            for p in gl[t][i].get("parts") or []:
                if p.get("entry") != w["entry"]:
                    seen[p["form"]] += 1
    lines = [f"  - `{f}`: {alone[f].most_common(1)[0][0]}" for f, _ in seen.most_common() if f in alone]
    return "\n".join(lines) if lines else "  - (none of the pieces shown stands alone in the map)"


def tokens_of(ws, gl):
    """The spellings a pack must not show: each hidden word's headword and the forms it has in its places."""
    out = set()
    for w in ws:
        out.add(re.sub(r"\s*\(\d+\)$", "", w["entry"]).strip("-"))
        out.update(gl[t][i]["form"] for t, i in w["places"])
    return sorted(x for x in out if len(x) >= 3)


def choice_block(w, gl, rows, hidden, letters, tokens=()):
    lines = [f"## `{w['code']}`", ""]
    for t, i in w["places"]:
        lines.append(f"- ({rows[t].get('kind') or 'kind of text not known'}) {blind_line(gl[t], i, w['entry'], w['code'], hidden, tokens)}")
    lines.append("")
    lines += [f"{letter}. {m}" for letter, m in zip("ABCD", letters)]
    return "\n".join(lines) + "\n"


def choice_packs():
    not_again("choice-packs")
    gl, rows = the_map(), corpus_rows()
    ws = choice_words(gl, lexicon(), the_items(), read("choice/candidates.json"), open_places(taken_places()["rows"]))
    (OUT / "choice" / "packs").mkdir(parents=True, exist_ok=True)
    key = {"words": {w["code"]: {k: w[k] for k in ("sort", "entry", "kind", "candidates", "true", "options", "pack")}
                     | {"places": [list(p) for p in w["places"]]} for w in ws}, "letters": {}}
    for n in range(1, PACKS + 1):
        mine = [w for w in ws if w["pack"] == n]
        hidden, tokens, lg = {w["entry"] for w in mine}, tokens_of(mine, gl), legend(mine, gl)
        for r in range(1, READERS + 1):
            (OUT / "choice" / f"reader{r}").mkdir(exist_ok=True)
            rng = random.Random(f"{SEED}/{n}/{r}")
            order = list(mine)
            rng.shuffle(order)
            body = []
            for w in order:
                letters = list(w["options"])
                rng.shuffle(letters)
                key["letters"][f"{w['code']}/{r}"] = letters
                body.append(choice_block(w, gl, rows, hidden, letters, tokens))
            text = CHOICE_BRIEF.format(n=len(mine), legend=lg, answers=f"data/sources/recurring/choice/reader{r}/K{n}.jsonl") + "\n---\n\n" + "\n".join(body)
            (OUT / "choice" / "packs" / f"K{n}_r{r}.md").write_text(text, encoding="utf-8")
    write("choice/key.json", key)
    print(len(ws), "words:", dict(collections.Counter(w["sort"] for w in ws)))


def choice_of(picks):
    """The readers' choice: the option that NEEDED or more of the READERS pick ("none" is one); None when fewer
    agree or when a reader's answer is missing."""
    if len(picks) != READERS:
        return None
    m, n = collections.Counter(picks).most_common(1)[0]
    return m if n >= NEEDED else None


def picked(answer, letters):
    """The meaning a reader's line picks: one of the four by its letter, "none", or None when it is neither."""
    p = str(answer.get("pick") or "").strip()
    if p.lower() == "none":
        return "none"
    return letters["ABCD".index(p)] if p in tuple("ABCD") and "ABCD".index(p) < len(letters) else None


def choice_rows(key, folder):
    """One row a word: what each reader picked (a reader's file counts only for the words of its own pack, the
    first line a word) and the readers' choice."""
    ws = key["words"]
    groups = [[c for c, w in ws.items() if w["pack"] == n] for n in range(1, PACKS + 1)]
    picks = collections.defaultdict(list)
    for r in range(1, READERS + 1):
        got = own_lines(folder / f"reader{r}", groups, "K{n}", "code", lambda a, n: a.get("code") if a.get("code") in groups[n - 1] else None)
        for c, a in got.items():
            m = picked(a, key["letters"][f"{c}/{r}"])
            if m is not None:
                picks[c].append(m)
    return [{"code": c, "sort": w["sort"], "entry": w["entry"], "kind": w["kind"], "true": w["true"], "candidates": w["candidates"],
             "options": w["options"], "picks": dict(collections.Counter(picks[c])), "answered": len(picks[c]), "choice": choice_of(picks[c])}
            for c, w in sorted(ws.items())]


def choice_figures(rows):
    """The test's figures and bars, and each open word's verdict (set in place on its row). A candidate is
    "favoured" only when both bars hold and every reader answered every word; otherwise it is "chosen, no label"."""
    offered = [r for r in rows if r["sort"] == "offered"]
    absent = [r for r in rows if r["sort"] == "absent"]
    chosen = [r for r in offered if r["choice"] not in (None, "none")]
    right = [r for r in chosen if r["choice"] == r["true"]]
    wrong = [r for r in absent if r["choice"] not in (None, "none")]
    figs = {"words": len(rows), "complete": all(r["answered"] == READERS for r in rows),
            "offered": len(offered), "offered_chosen": len(chosen), "offered_right": len(right),
            "right_when_chosen": round(len(right) / len(chosen), 4) if chosen else None,
            "found": round(len(right) / len(offered), 4) if offered else None,
            "offered_none": sum(r["choice"] == "none" for r in offered), "offered_no_choice": sum(r["choice"] is None for r in offered),
            "absent": len(absent), "absent_wrong": len(wrong),
            "wrong_when_absent": round(len(wrong) / len(absent), 4) if absent else None,
            "absent_none": sum(r["choice"] == "none" for r in absent)}
    figs["bar1"] = len(chosen) >= BARS["chosen_at_least"] and figs["right_when_chosen"] >= BARS["right_when_chosen"]
    figs["bar2"] = bool(absent) and figs["wrong_when_absent"] <= BARS["wrong_when_absent"]
    figs["labels_given"] = bool(figs["complete"] and figs["bar1"] and figs["bar2"])
    opened = [r for r in rows if r["sort"] == "open"]
    for r in opened:
        r["verdict"] = ("favoured" if figs["labels_given"] else "chosen, no label") if r["choice"] in r["candidates"] else \
            "none of the four" if r["choice"] == "none" else "a filler chosen" if r["choice"] else "no choice"
    figs["open_words"] = len(opened)
    figs["open"] = dict(collections.Counter(r["verdict"] for r in opened))
    return figs


def choice():
    rows = choice_rows(read("choice/key.json"), OUT / "choice")
    figs = choice_figures(rows)
    write("choice/result.json", {"figures": figs, "rows": rows})
    print(figs)


# -------------------------------------------------------------------------------------------------- the recount

def groups_of(levels):
    c = collections.Counter(levels)
    return {"read": sum(c[k] for k in READ), "names": sum(c[k] for k in NAMED), "open": sum(c[k] for k in OPEN), "lost": c["lost"]}


def share(g):
    """Of the words that need a meaning (read or open; not names, numerals or lost), the share that has one."""
    need = g["read"] + g["open"]
    return round(g["read"] / need, 4) if need else None


def form_levels(gl):
    """Each spelling's levels (spellings_of) and the map's first gloss of it."""
    gloss = {}
    for gs in gl.values():
        for g in gs:
            gloss.setdefault(g["form"], (g.get("gloss") or "").strip())
    return spellings_of(gl)[0], gloss


def overlay(gl, its, rows, verified, cands):
    """One line for each place the work resolves: a meaning a later source states; a piece of a word the map
    reads (it takes that word's level); an open place of an item that is a name by the sources."""
    level, gloss = form_levels(gl)
    out = []
    for r in rows:
        p = its[r["item"]]["places"][r["place"] - 1]
        base = {"text": p["text"], "n": p["n"], "form": p["form"], "item": r["item"], "was": gl[p["text"]][p["n"] - 1]["level"]}
        if r["verdict"] == "stated":
            v = verified[r["item"]]["one"]
            out.append(base | {"level": "meaning", "gloss": v["meaning"], "why": "stated", "source": f"{v['source']}, p. {v['page']}"})
        elif r["verdict"] == "piece" and r["whole"] in level:
            lv = level[r["whole"]].most_common(1)[0][0]
            if lv in READ + NAMED:
                out.append(base | {"level": lv, "gloss": f"part of {r['whole']}: {gloss[r['whole']]}", "why": "piece",
                                   "source": "the map's reading of the whole word"})
        elif r["verdict"] == "open" and (cands.get(r["item"]) or {}).get("name"):
            out.append(base | {"level": "name", "gloss": f"a name ({cands[r['item']]['name']})", "why": "name", "source": "the sources, read by two"})
    return out


def pieces_of(rows, gl):
    """The places both checkers call a piece, by what the whole word they name is in the map."""
    level, _ = form_levels(gl)
    out = collections.Counter()
    for r in rows:
        if r["verdict"] == "piece":
            lv = level[r["whole"]].most_common(1)[0][0] if r["whole"] in level else None
            out["read" if lv in READ else "name" if lv in NAMED else "open" if lv in OPEN else "not a form of the map"] += 1
    return dict(out)


def recount_of(gl, its, rows, verified, cands):
    ov = overlay(gl, its, rows, verified, cands)
    new = {(o["text"], o["n"]): o["level"] for o in ov}
    before = groups_of(g["level"] for gs in gl.values() for g in gs)
    after = groups_of(new.get((t, i + 1), g["level"]) for t, gs in gl.items() for i, g in enumerate(gs))
    forms = collections.defaultdict(lambda: [0, 0])
    for it in its.values():
        for p in it["places"]:
            forms[p["form"]][0] += 1
            forms[p["form"]][1] += (p["text"], p["n"]) in new
    return ov, {"running_words": sum(before.values()), "before": before | {"share": share(before)}, "after": after | {"share": share(after)},
                "overlay": dict(collections.Counter(o["why"] for o in ov)), "overlay_levels": dict(collections.Counter(o["level"] for o in ov)),
                "was": dict(collections.Counter(o["was"] for o in ov)), "pieces": pieces_of(rows, gl),
                "spellings": len(forms), "spellings_all_resolved": sum(1 for a, b in forms.values() if a == b),
                "spellings_most_resolved": sum(1 for a, b in forms.values() if 2 * b > a),
                "spellings_none_resolved": sum(1 for a, b in forms.values() if b == 0)}


def recount():
    ov, figs = recount_of(the_map(), the_items(), taken_places()["rows"], read("lit/verify/result.json"), read("choice/candidates.json"))
    (OUT / "overlay.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in ov), encoding="utf-8")
    write("recount.json", figs)
    print(json.dumps(figs, ensure_ascii=False, indent=1))


# A check by script, apart from the checkers: the two largest groups of stated places stand in a fixed phrase.
# item -> (what one of the three words before it must be, in the project's letters, where case matters: x is ḫ and
# X is ẖ; what that is). `at` (bread) starts the joined forms atmXe, atXe...; `ato` (water) is not bread.
FORMULA = {"ḫr": (lambda f: f.startswith("at") and not f.startswith("ato"), "a form of at, bread (not ato, water)"),
           "ẖol": (lambda f: "xmlo" in f, "a form of ḫmlol, a good meal")}


def formula_check(rows, its, gl):
    """For the items of FORMULA: of the places the pass calls stated, how many have the expected word among the
    three words before them."""
    out = {}
    for k, (test, what) in FORMULA.items():
        mine = [its[k]["places"][r["place"] - 1] for r in rows if r["item"] == k and r["verdict"] == "stated"]
        out[k] = {"stated": len(mine), "what": what,
                  "with": sum(any(test(g["form"]) for g in gl[p["text"]][max(0, p["n"] - 4): p["n"] - 1]) for p in mine)}
    return out


def all_agree(rows):
    """Seen after the count, not a bar: the words on which all the readers pick the same option."""
    full = [r for r in rows if r["picks"] and max(r["picks"].values()) == READERS and r["choice"] != "none"]
    offered = [r for r in full if r["sort"] == "offered"]
    return {"offered_chosen": len(offered), "offered_right": sum(r["choice"] == r["true"] for r in offered),
            "absent_wrong": sum(r["sort"] == "absent" for r in full),
            "open_candidates": sorted(r["entry"] for r in full if r["sort"] == "open" and r["choice"] in r["candidates"])}


# -------------------------------------------------------------------------------------------- the public figures

# Meanings that the readers wrote or saw in words that follow the lexicon of 2003 or Rilly 2016 and 2021 for four
# words in a row (the rule of src/lexicon.py, COPIED): the public figures and the page give them in ours. Each is
# found by where it stands, not by its wording, so that the readers' wording stands in no tracked file: a stated
# meaning of class A by its item, a candidate of the choice test by its word and its place among that word's
# candidates (1 for the first). The packs, the key and the answers, all local, keep the readers' wording. Two
# options that follow the lexicon too ("to love, to revere", "to order, to command") stay: they stand in ACCEPTED
# above, which rebuilds the packs, and were public before in runs/keys/.
STATED_IN_OUR_WORDS = {
    "-wi (5)": "particle of emphasis, optional, that follows the copula -o of the singular",
    "ps-": "prefix that makes a benediction verb causative ('make' drink, eat)",
    "wse": "'his/her', a possessive (singular, third person), another form of qo-se",
    "wi (1)": "brother (wide, which becomes wi- when the article follows)",
}
CANDIDATES_IN_OUR_WORDS = {("penn", 2): "a star's rising", ("womnitẖ", 1): "Amun's first priest", ("mreperi", 2): "estate steward",
                           ("ptroti", 1): "the southern one (feminine)", ("ptroti", 2): "to be praised"}


def public_row(r, given):
    """One word of the choice test for the figures file, every meaning in the public wording: a candidate that
    CANDIDATES_IN_OUR_WORDS rewords is reworded wherever it stands in the row. Refuses a row in which two options,
    or an option and "none", would come out in one wording: their picks would be added together."""
    mine = {m: CANDIDATES_IN_OUR_WORDS[r["entry"], n] for n, m in enumerate(r["candidates"], 1) if (r["entry"], n) in CANDIDATES_IN_OUR_WORDS}
    ours = lambda m: mine.get(m, m)                                                            # noqa: E731
    if len({ours(m) for m in r["options"]} | {"none"}) != len(r["options"]) + 1:
        raise SystemExit(f"{r['entry']}: two of its options, or an option and \"none\", would have one wording; nothing written")
    row = {k: r[k] for k in ("sort", "entry", "kind")} | {
        "true": r["true"] and ours(r["true"]), "candidates": [ours(m) for m in r["candidates"]], "options": [ours(m) for m in r["options"]],
        "picks": {ours(m): n for m, n in r["picks"].items()}, "choice": r["choice"] and ours(r["choice"])}
    if r["sort"] == "open":
        row |= {"verdict": r["verdict"], "given_by": {ours(m): given[m] for m in r["candidates"]}}
    return row


def figures():
    """What the page reports, from the local results: counts, verdicts and short meanings, no text of a source."""
    its, checked, classes = the_items(), read("lit/checked.json"), read("lit/classes.json")
    verified, pl, cd, ch = read("lit/verify/result.json"), taken_places(), read("choice/candidates.json"), read("choice/result.json")
    by_class = {}
    for letter in "ABC":
        ks = [k for k, c in classes.items() if c[0] == letter]
        by_class[letter] = {"items": len(ks), "spellings": sum(len(its[k]["forms"]) for k in ks), "running_words": sum(its[k]["uses"] for k in ks)}
    cover = collections.Counter()
    for v in verified.values():
        if v["verdict"] == "stated":
            cover.update(v["covered"])
    opened = open_places(pl["rows"])
    given = {k: {c["meaning"]: [c["source"], c["stance"]] for c in v["candidates"]} for k, v in cd.items()}
    gl = the_map()
    return {
        "map": map_figures(gl),
        "spellings": sum(len(it["forms"]) for it in its.values()), "items": len(its), "running_words": sum(it["uses"] for it in its.values()),
        "literature": read("lit/counts.json") | {"sources": dict(collections.Counter(s["source"] for v in checked.values() for s in v["statements"]).most_common())},
        "classes": by_class,
        "class_a": {"items": len(verified), "verdicts": dict(collections.Counter(v["verdict"] for v in verified.values())),
                    "not_stated": sorted(k for k, v in verified.items() if v["verdict"] != "stated"),
                    "running_words": sum(v["uses"] for v in verified.values() if v["verdict"] == "stated"), "covered": dict(cover),
                    "stated": [{"item": k, "uses": v["uses"], "meaning": STATED_IN_OUR_WORDS.get(k, v["one"]["meaning"]), "source": v["one"]["source"], "page": v["one"]["page"],
                                "stances": [v["one"]["stance"], v["two"]["stance"]], "covered": v["covered"],
                                "places_stated": sum(1 for r in pl["rows"] if r["item"] == k and r["verdict"] == "stated")}
                               for k, v in verified.items() if v["verdict"] == "stated"]},
        "places": {k: pl[k] for k in ("places", "answered by both", "kappa", "bar", "taken", "verdicts", "by class")}
        | {"formula_check": formula_check(pl["rows"], its, gl)},
        "open_items": len(opened), "open_places": sum(map(len, opened.values())),
        "candidates": {"items": len(cd), "with_a_candidate": sum(bool(v["candidates"]) for v in cd.values()),
                       "none": sum(not v["candidates"] for v in cd.values()), "names": {k: v["name"] for k, v in sorted(cd.items()) if v["name"]},
                       "left_out": dict(collections.Counter(left_out(v) for v in cd.values() if v["candidates"] and left_out(v)).most_common())},
        "choice": ch["figures"] | {"bars": BARS, "readers": READERS, "needed": NEEDED, "packs": PACKS, "all_agree": all_agree(ch["rows"]),
                                   "rows": [public_row(r, given.get(r["entry"], {})) for r in ch["rows"]]},
        "in_our_words": len(STATED_IN_OUR_WORDS) + len(CANDIDATES_IN_OUR_WORDS),
        "recount": read("recount.json"),
        "tokens": {k: {"agents": a, "tokens": t} for k, (a, t) in TOKENS.items()} | {"all": {"agents": sum(a for a, _ in TOKENS.values()),
                                                                                              "tokens": sum(t for _, t in TOKENS.values())}},
        "when": [{k: w[k] for k in ("step", "set_in", "set", "started", "first_answer")} for w in WHEN],
    }


def public():
    PUBLIC.write_text(json.dumps(figures(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", PUBLIC.relative_to(ROOT))


COMMANDS = {"items": items, "batches": batches, "quotes": quotes, "verify-packs": verify_packs, "verify": verify,
            "place-packs": place_packs, "places": places, "cand-packs": cand_packs, "cands": cands,
            "choice-packs": choice_packs, "choice": choice, "recount": recount, "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
