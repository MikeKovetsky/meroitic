"""The blind test again (step G6, data/discovery/blind_test_2.md): the choice test of src/recurring.py with what
the first one taught. Five fresh readers a pack choose among four meanings for a hidden word shown only by the
words around it; a choice needs all five. The accepted words are the first test's and five more; the fillers are
drawn from one pool of accepted meanings and proposals, and near meanings are kept apart.

The test was run twice. The first run took 43 accepted words (the first test's 38 and five more) and left 40 of
the plan's 83 out; the second (data/discovery/blind_test_83.md) took all 83, the 40 with the meaning the lexicon
gives them, however coarse. `run_83()` gives the script the second run's settings.

Everything is read and written under data/sources/g6/ and, for the run with 83, data/sources/g6b/ (local only:
the packs show the map), except `public`. Four meanings of the run with 83 stood in the packs in a wording that
follows the lexicon's English; that wording is read from the local file pack_wording.json.

  python3 -I src/blind2.py words       the words of the test and their four options, printed
  python3 -I src/blind2.py packs       the packs for five readers each (packs/, key.json)
  python3 -I src/blind2.py count       the readers' choices, the bars, each open word's verdict (result.json)
  python3 -I src/blind2.py words-83    the same three steps for the run with all 83 accepted words
  python3 -I src/blind2.py packs-83
  python3 -I src/blind2.py count-83
  python3 -I src/blind2.py public      data/discovery/blind_test_2_figures.json and blind_test_83_figures.json

What the readers were given is in runs/prompts/G6_choice.md and G6_choice_83.md.
"""
import collections
import contextlib
import copy
import itertools
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import recurring as W                                   # noqa: E402
import themap as M                                      # noqa: E402

HOME = ROOT / "data/sources/g6"
ANSWERS = "data/sources/g6"                             # the folder the packs name for the readers' answers
PUBLIC = ROOT / "data/discovery/blind_test_2_figures.json"
FIRST = ROOT / "data/discovery/recurring_words_figures.json"     # the first test's public figures
TOKENS = "tokens.json"                                   # from the task notifications, typed by hand (local)
LAYERS = ("recurring", "rare_sure", "rare_later", "unnamed")   # the layers of the map when the test was set
SEED = 20261116 + 6
READERS, PACKS, NEEDED = 5, 5, 5                         # a choice: all five readers pick the same option
BARS = W.BARS                                            # the bars of the first test, unchanged
# When the rules were set against the readers (2026-11-16, Pacific time), as src/leftover.py records it.
WHEN = {"set_in": "ff4a0ba", "set": "15:41:41", "started": "15:42:03", "first_answer": "15:42:33", "last_answer": "15:43:36",
        "counted": "15:44:04"}

# The entries the base map translates in three texts or more, alone in their word, that the lexicon calls
# established or probable and that the first test did not have: the five with a meaning of their own, of one of
# the four kinds, and why each of the others stays out.
NEW = {"ste": ("mother", "noun"), "ktke": ("queen (Candace)", "title"), "qoresem": ("the ruler's spouse", "title"),
       "te-dḫe-l": ("to bear (a child)", "verb"), "t-erike-l": ("to beget (a child)", "verb")}
# (`kroro` is filed here as a form or a variant of a word of the test. The lexicon calls it a variant of `akroro`,
# which is not in the test and which the lexicon data in hand does not hold. The table stands as it was committed
# before the readers; the entry stayed out either way.)
OFFICE = "a title of which only the kind of office is known"
FORM = "a form or a variant of a word of the test, or the same meaning"
NONE = "no meaning of its own, or not of the four kinds"
ALSO = "also an open word of the test"
OUT = {
    "beliloke": OFFICE, "beloloke": OFFICE, "deseke": OFFICE, "mkesḫe": OFFICE, "qorene": OFFICE, "siremroke": OFFICE,
    "sleqene": OFFICE, "slẖ": OFFICE, "slẖs": OFFICE, "snte": OFFICE, "soni": OFFICE, "ssimete": OFFICE,
    "stmdese": OFFICE, "tbqo": OFFICE, "teter": OFFICE, "tqi": OFFICE, "trtekese": OFFICE, "ttne": OFFICE,
    "ḫbḫne": OFFICE, "ḫlbine": OFFICE,
    "apote-lẖ": FORM, "dḫe": FORM, "kroro": FORM, "mẖe": FORM, "nse doke": FORM, "ntke (1)": FORM, "pesto": FORM,
    "qetneyineqeli": FORM, "qetrri": FORM, "qor": FORM, "qor-o": FORM, "qorise": FORM, "sqo": FORM, "t-dḫe": FORM,
    "ḫlẖl": FORM,
    "dik": NONE, "dot": NONE, "pke": NONE,
    "l (2)": ALSO, "wi (1)": ALSO,
}
ACCEPTED = W.ACCEPTED | NEW
COARSE = frozenset()                                     # meanings that are never drawn as a filler (the run with 83)
SORTS = None                                             # entry -> its sort, for a count by sort (the run with 83)


@contextlib.contextmanager
def settings():
    """src/recurring.py's choice test with this test's readers, packs, rule of choice and accepted words."""
    old = W.READERS, W.PACKS, W.NEEDED, W.ACCEPTED
    W.READERS, W.PACKS, W.NEEDED, W.ACCEPTED = READERS, PACKS, NEEDED, ACCEPTED
    try:
        yield
    finally:
        W.READERS, W.PACKS, W.NEEDED, W.ACCEPTED = old

# Meanings too near one another to be told apart by a context: a filler is never put beside a meaning of its group
# (the true meaning of an accepted word, a candidate of an open word, or another filler). A word's own candidates
# stay together as the sources give them.
GROUPS = [
    {"ruler", "great prince", "lord of", "master", "lord of eternity", "the ruler's spouse", "queen (Candace)"},
    {"water", "beneficial water offering"},
    {"to give", "given", "to present", "to grant", "to serve"},
    {"to make", "made by"},
    {"to praise", "to be praised", "adoration, praise", "to love, to revere"},
    {"life", "life-giver", "health"},
    {"god", "good god"},
    {"priest", "priest of Amun", "Amun's first priest"},
    {"land, province", "country", "of the country", "village"},
    {"child", "direct descendant", "to bear (a child)", "to beget (a child)"},
    {"nephew, niece", "mother's brother", "mother's kin"},
    {"good", "abundant", "beneficent", "good of repute"},
    {"great, elder", "powerful", "strength", "protection"},
    {"majordomo", "estate steward", "temple administrator", "temple bread administrator"},
    {"notable", "citizen", "good of repute"},
    {"wife", "the ruler's spouse"},
    {"bull", "cow"},
]


def read(path):
    return json.loads((HOME / path).read_text(encoding="utf-8"))


def write(path, data):
    (HOME / path).parent.mkdir(parents=True, exist_ok=True)
    (HOME / path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def further(gl, lex):
    """The lexicon's sure entries that the base map translates in three texts or more, alone in their word, and
    that the first test did not have."""
    out = collections.defaultdict(set)
    for t in sorted(gl):
        for g in gl[t]:
            if g["level"] == "meaning":
                s = [h for h in W.heads_of(g) if h in lex and not W.affix(h)]
                if len(s) == 1:
                    out[s[0]].add(t)
    return sorted(h for h, ts in out.items() if len(ts) >= W.MIN_TEXTS and (h not in ACCEPTED or h in NEW) and (lex[h].get("status") or "") in W.SURE)


def near(a, b):
    """Whether the filler `a` may not stand beside the meaning `b`: they share a content word or a group, or `a`
    is a coarse meaning, which is never a filler."""
    return a in COARSE or bool(W.content(a) & W.content(b)) or any(a in g and b in g for g in GROUPS)


def fill(have, kind, rng, pool, avoid=()):
    """Four options: those given, filled up from the pool with meanings of the same kind (of another kind only when
    the kind has too few), none of them near an option or a meaning of `avoid`."""
    opts = list(have)
    same = sorted(m for m, k in pool if k == kind)
    rest = sorted({m for m, k in pool if k != kind} - set(same))
    rng.shuffle(same)
    rng.shuffle(rest)
    for m in same + rest:
        if len(opts) == 4:
            break
        if m not in opts and not any(near(m, o) for o in opts + list(avoid)):
            opts.append(m)
    return opts


def ours(entry, cand):
    """A word's candidates in the public wording (W.CANDIDATES_IN_OUR_WORDS, by the candidate's place among those
    kept), each with its own kind."""
    kind = {x["meaning"]: x["kind"] for x in reversed(cand["candidates"])}
    keep = W.distinct([x["meaning"] for x in cand["candidates"]])
    return [(W.CANDIDATES_IN_OUR_WORDS.get((entry, n), m), kind[m]) for n, m in enumerate(keep, 1)]


def open_words(cur, its, cands, opened):
    """The open words: those of the first test, with the places the map with its layers still holds open; three
    such places at least."""
    out = {}
    for k in sorted(cands):
        if W.left_out(cands[k]) or k not in opened:
            continue
        places = [(its[k]["places"][n - 1]["text"], its[k]["places"][n - 1]["n"] - 1) for n in opened[k]]
        places = [p for p in places if cur[p[0]][p[1]]["level"] in W.OPEN]
        if len(places) >= 3:
            out[k] = {"kind": cands[k]["candidates"][0]["kind"], "candidates": ours(k, cands[k]), "places": places}
    return out


def the_map():
    """The map with the layers it had when the test was set."""
    names = tuple(l["name"] for l in M.LAYERS)
    if names[:len(LAYERS)] != LAYERS:
        raise SystemExit(f"the layers of the test are no longer {LAYERS}")
    return M.current(upto=len(LAYERS))


def the_words():
    with settings():
        return words_of(W.lexicon(), M.base(), the_map())


def words_of(lex, base, cur):
    its, cands = W.the_items(), W.read("choice/candidates.json")
    opened = W.open_places(W.taken_places()["rows"])
    more = further(base, lex)
    if set(more) != set(NEW) | set(OUT):
        raise SystemExit(f"the further entries have changed: {sorted(set(more) ^ (set(NEW) | set(OUT)))}")
    op = open_words(cur, its, cands, opened)
    pool = {(m, k) for m, k in ACCEPTED.values()} | {(m, k) for w in op.values() for m, k in w["candidates"] if k in W.KINDS}
    rng = random.Random(SEED)
    out = []
    for k, w in op.items():
        meanings = [m for m, _ in w["candidates"]]
        out.append({"sort": "open", "entry": k, "kind": w["kind"], "candidates": meanings, "true": None,
                    "places": W.sample(w["places"], rng), "options": fill(meanings, w["kind"], rng, pool)})
    acc = W.accepted_places(base, lex)
    by_kind = collections.defaultdict(list)
    for h in sorted(ACCEPTED):
        if len({t for t, _ in acc.get(h, [])}) >= W.MIN_TEXTS:
            by_kind[ACCEPTED[h][1]].append(h)
    for kind in sorted(by_kind):
        hs = by_kind[kind]
        rng.shuffle(hs)
        for n, h in enumerate(hs):
            true = ACCEPTED[h][0]
            absent = n % 3 == 2
            opts = fill([], kind, rng, pool, avoid=[true]) if absent else fill([true], kind, rng, pool)
            out.append({"sort": "absent" if absent else "offered", "entry": h, "kind": kind, "candidates": [], "true": true,
                        "places": W.sample(acc[h], rng), "options": opts, "new": h in NEW})
    rng.shuffle(out)
    for n, w in enumerate(out, 1):
        w["code"] = f"W{n:03d}"
        w["pack"] = (n - 1) % PACKS + 1
    if any(len(w["options"]) != 4 for w in out):
        raise SystemExit("a word has fewer than four options")
    return out, cur


def shown_map(cur):
    """The map with its layers as the readers see it: a piece's reading without the spelling of its whole word."""
    gl = copy.deepcopy(cur)
    for gs in gl.values():
        for g in gs:
            if g.get("why") == "piece":
                g["gloss"] = re.sub(r"^part of [^:]+:\s*", "", g.get("gloss") or "")
    return gl


COUNTED = ("This pack lists {n} words: your file must have {n} lines, one for each word, none left out. When the file is "
           "written, count its lines against that number, then reply in one line: how many words, and how many of each pick.")
REPLY = "When the file is written, reply in one line: how many words, and how many of each pick."
assert W.CHOICE_BRIEF.count(REPLY) == 1


def words():
    ws, _ = the_words()
    print(len(ws), "words:", dict(collections.Counter(w["sort"] for w in ws)), "new accepted:", sum(1 for w in ws if w.get("new")),
          "by kind:", dict(collections.Counter((w["sort"], w["kind"]) for w in ws)))
    for w in ws:
        print(w["code"], w["pack"], f"{w['sort']:8}", f"{w['entry']:14}", len(w["places"]), w["true"], w["candidates"], "|", w["options"])


def packs():
    if any(HOME.glob("reader*/K*.jsonl")):
        raise SystemExit("the readers have answered: the packs are not written again")
    ws, cur = the_words()
    gl, rows = shown_map(cur), W.corpus_rows()
    (HOME / "packs").mkdir(parents=True, exist_ok=True)
    key = {"words": {w["code"]: {k: w[k] for k in ("sort", "entry", "kind", "candidates", "true", "options", "pack")}
                     | {"new": bool(w.get("new")), "places": [list(p) for p in w["places"]]} for w in ws}, "letters": {}}
    for n in range(1, PACKS + 1):
        mine = [w for w in ws if w["pack"] == n]
        hidden, tokens, lg = {w["entry"] for w in mine}, W.tokens_of(mine, gl), W.legend(mine, gl)
        for r in range(1, READERS + 1):
            (HOME / f"reader{r}").mkdir(exist_ok=True)
            rng = random.Random(f"{SEED}/{n}/{r}")
            order = list(mine)
            rng.shuffle(order)
            body = []
            for w in order:
                letters = list(w["options"])
                rng.shuffle(letters)
                key["letters"][f"{w['code']}/{r}"] = letters
                body.append(W.choice_block(w, gl, rows, hidden, letters, tokens))
            brief = W.CHOICE_BRIEF.replace(REPLY, COUNTED.format(n=len(mine)))
            text = brief.format(n=len(mine), legend=lg, answers=f"{ANSWERS}/reader{r}/K{n}.jsonl") + "\n---\n\n" + "\n".join(body)
            (HOME / "packs" / f"K{n}_r{r}.md").write_text(text, encoding="utf-8")
    write("key.json", key)
    print(len(ws), "words:", dict(collections.Counter(w["sort"] for w in ws)), "in", PACKS, "packs for", READERS, "readers each")


def count():
    key = read("key.json")
    with settings():
        rows = W.choice_rows(key, HOME)
        for r in rows:
            r["new"] = key["words"][r["code"]]["new"]
        figs = W.choice_figures(rows)
    res = {"figures": figs | {"bars": BARS, "readers": READERS, "needed": NEEDED, "packs": PACKS}, "rows": rows}
    if SORTS is not None:
        res["by_sort"] = by_sort(rows)
    write("result.json", res)
    print(json.dumps(figs, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------------------------------------------- the figures

def outcome(r):
    """What the five readers made of an accepted word: right, wrong, none, or no choice."""
    c = r["choice"]
    return "no choice" if c is None else "none" if c == "none" else "right" if c == r["true"] else "wrong"


def by_sort(rows):
    """The accepted words' outcomes by the sort of word (SORTS; a word of the first test where it names none)."""
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["sort"] != "open":
            by[SORTS.get(r["entry"], OF_THE_FIRST)][f"{r['sort']}: {outcome(r)}"] += 1
    return {k: dict(sorted(v.items())) for k, v in sorted(by.items())}


def options_of(rows):
    """What the words' four options hold: how many words have both sorts of meaning among them (an accepted meaning
    of the test and a proposal on record for one of its open words), and the open words two of whose own proposals
    are near one another (they stay together, as the sources give them)."""
    accepted = {m for m, _ in ACCEPTED.values()}
    proposals = {m for r in rows if r["sort"] == "open" for m in r["candidates"]}
    return {"words": len(rows),
            "of_both_sorts": sum(bool(set(r["options"]) & accepted) and bool(set(r["options"]) & proposals) for r in rows),
            "open_words_with_near_proposals": sorted(r["entry"] for r in rows if r["sort"] == "open"
                                                     and any(near(a, b) for a, b in itertools.combinations(r["candidates"], 2)))}


def figures():
    """What the page reports, from the local results: counts, and each word's row in the wording of the packs
    (the accepted meanings and the proposals as the first test's public figures have them)."""
    res, key = read("result.json"), read("key.json")
    rows, first = res["rows"], json.loads(FIRST.read_text(encoding="utf-8"))["choice"]
    t = next(v for v in read(TOKENS).values() if isinstance(v, dict))
    acc = [r for r in rows if r["sort"] != "open"]
    return {
        "words": len(rows), "sorts": dict(collections.Counter(r["sort"] for r in rows).most_common()),
        "accepted": {"all": len(acc), "of_the_first_test": sum(not r["new"] for r in acc), "new": sum(r["new"] for r in acc)},
        "further_entries": {"all": len(NEW) + len(OUT), "taken": len(NEW), "left_out": dict(collections.Counter(OUT.values()).most_common()),
                            "by_entry": {k: "taken" for k in sorted(NEW)} | dict(sorted(OUT.items()))},
        "groups_of_near_meanings": len(GROUPS), "options": options_of(rows), "seed": SEED, "places_shown_at_most": W.SHOWN,
        "words_each_side": W.CHOICE_WIDTH,
        "answers": sum(r["answered"] for r in rows), "answers_expected": len(rows) * READERS,
        "choice": res["figures"],
        "accepted_by_outcome": {s: dict(collections.Counter(outcome(r) for r in acc if r["sort"] == s).most_common()) for s in ("offered", "absent")},
        "wrong_choices": [{"entry": r["entry"], "sort": r["sort"], "true": r["true"], "chosen": r["choice"]} for r in acc if outcome(r) == "wrong"],
        "new_words": [{"entry": r["entry"], "sort": r["sort"], "true": r["true"], "outcome": outcome(r)} for r in acc if r["new"]],
        "open_chosen": {r["entry"]: r["choice"] for r in rows if r["sort"] == "open" and r["choice"] in r["candidates"]},
        "first_test": {"needed": first["needed"], "all_agree": first["all_agree"], "absent": first["absent"]},
        "rows": [{k: r[k] for k in ("sort", "entry", "kind", "true", "candidates", "options", "picks", "choice")}
                 | ({"verdict": r["verdict"]} if r["sort"] == "open" else {"new": r["new"]}) for r in rows],
        "packs_of": {str(n): c for n, c in sorted(collections.Counter(w["pack"] for w in key["words"].values()).items())},
        "cost": {"agents": len(t), "tokens": sum(t.values())}, "when": WHEN,
    }


# ------------------------------------------------------------------------- the run with all 83 accepted words

HOME_83 = ROOT / "data/sources/g6b"
PUBLIC_83 = ROOT / "data/discovery/blind_test_83_figures.json"
SEED_83, PACKS_83 = 20261116 + 10, 8
LAYERS_83 = LAYERS + ("rare_millet", "leftover")         # the six layers of the map when this run was set
PRIEST, ADMIN, VICEROY = "a priestly title", "an administrative title", "an official under the viceroy"
HOUSE, TITLE, BEAR = "a household official of the ruler", "a title, the office not known", "to bear (a child)"
# The 40 entries the first run left out, by why it left them out, each with the meaning the lexicon gives it in a
# few words of our own. Four of them (HOUSE, the two bynames and the predicate of `qor-o`) stood in the packs in a
# wording that follows the project's English of the lexicon for four words in a row (the rule of src/lexicon.py,
# COPIED): here, in the figures and on the page they are in other words, and the packs' wording is read from the
# local file PACK_WORDING, without which the packs cannot be written again as they were.
MORE = {
    OFFICE: {"beliloke": (PRIEST, "title"), "beloloke": (PRIEST, "title"), "deseke": (PRIEST, "title"), "mkesḫe": (PRIEST, "title"),
             "slẖ": (PRIEST, "title"), "slẖs": (PRIEST, "title"), "snte": (PRIEST, "title"), "soni": (PRIEST, "title"),
             "ssimete": (PRIEST, "title"), "teter": (PRIEST, "title"), "tqi": (PRIEST, "title"), "trtekese": (PRIEST, "title"),
             "siremroke": (ADMIN, "title"), "sleqene": (ADMIN, "title"), "tbqo": (ADMIN, "title"),
             "stmdese": (VICEROY, "title"), "ḫlbine": (VICEROY, "title"), "ttne": (HOUSE, "title"), "ḫbḫne": (HOUSE, "title"),
             "qorene": (TITLE, "title")},
    FORM: {"apote-lẖ": ("chief envoy", "title"), "pesto": ("viceroy", "title"), "kroro": (TITLE, "title"),
           "dḫe": (BEAR, "verb"), "t-dḫe": (BEAR, "verb"), "mẖe": ("abundant", "adjective"),
           "nse doke": ("a favourable sacrifice", "noun"), "ntke (1)": ("strength", "noun"),
           "qetneyineqeli": ("a byname of Isis", "adjective"), "qetrri": ("a byname of Osiris", "adjective"),
           "qor": ("the ruler", "noun"), "qor-o": ("the ruler, as a predicate", "noun"), "qorise": ("of the ruler", "noun"),
           "sqo": ("this man", "noun"), "ḫlẖl": ("a great meal", "noun")},
    NONE: {"dik": ("all the way, from one place to another", "verb"), "dot": ("favourable", "adjective"), "pke": ("a blessing", "noun")},
    ALSO: {"l (2)": ("to give", "verb"), "wi (1)": ("brother", "noun")},
}
OF_THE_FIVE, OF_THE_FIRST = "one of the five that G6 added", "one of the 38 of the first test"
SORT = {h: why for why, hs in MORE.items() for h in hs} | {h: OF_THE_FIVE for h in NEW}
if {h: SORT[h] for h in OUT} != OUT:
    raise SystemExit("the entries the first run left out are no longer those of MORE")
NEW_83 = NEW | {h: v for hs in MORE.values() for h, v in hs.items()}
ACCEPTED_83 = W.ACCEPTED | NEW_83
GROUPS_83 = GROUPS + [
    {PRIEST, TITLE, "priest", "priest of Amun", "Amun's first priest"},
    {ADMIN, TITLE, HOUSE, VICEROY, "temple administrator", "temple bread administrator", "estate steward", "majordomo"},
    {"favourable", "a favourable sacrifice", "good", "abundant", "beneficent", "good of repute"},
    {"a blessing", "life", "health", "protection", "adoration, praise"},
    {"a byname of Isis", "a byname of Osiris", "life-giver", "powerful", "beneficent"},
]
# A coarse meaning ("a priestly title") is the true meaning of its own words only: it is never drawn as a filler,
# since it would be true of any title of its sort it stood beside.
COARSE_83 = frozenset({PRIEST, ADMIN, HOUSE, VICEROY, TITLE})
# The times of the run (2026-11-16, Pacific time): the commit of the rules and its time in git; the packs' files;
# the first and the last launch of each of the two batches (the session's log: the usage limit of the session
# stopped the launch after 32 readers, and the last 8 were started when it was lifted); the answer files; the count.
WHEN_83 = {"set_in": "bb57217", "set": "16:49:38", "packs_written": "16:49:40", "started": "16:49:46", "first_answer": "16:50:22",
           "last_launch_before_the_limit": "16:51:18", "last_answer_before_the_limit": "16:51:53", "readers_before_the_limit": 32,
           "resumed": "18:01:14", "first_answer_after": "18:01:54", "last_answer": "18:01:59", "readers_after_the_limit": 8,
           "counted": "18:02:17"}


PACK_WORDING = HOME_83 / "pack_wording.json"             # local: {a meaning as it stands here: as the packs had it}


def pack_wording():
    return json.loads(PACK_WORDING.read_text(encoding="utf-8")) if PACK_WORDING.exists() else {}


@contextlib.contextmanager
def run_83():
    """The script with the settings of the run with all 83 accepted words, the meanings in the packs' wording where
    the local file has one; the first run's settings are back afterwards."""
    global HOME, ANSWERS, PUBLIC, SEED, PACKS, LAYERS, NEW, OUT, ACCEPTED, GROUPS, COARSE, SORTS, WHEN
    old = HOME, ANSWERS, PUBLIC, SEED, PACKS, LAYERS, NEW, OUT, ACCEPTED, GROUPS, COARSE, SORTS, WHEN
    shown = pack_wording()
    HOME, ANSWERS, PUBLIC, SEED, PACKS, LAYERS = HOME_83, "data/sources/g6b", PUBLIC_83, SEED_83, PACKS_83, LAYERS_83
    NEW = {h: (shown.get(m, m), k) for h, (m, k) in NEW_83.items()}
    OUT, ACCEPTED, SORTS, WHEN = {}, ACCEPTED_83 | NEW, SORT, WHEN_83
    GROUPS, COARSE = [{shown.get(m, m) for m in g} for g in GROUPS_83], frozenset(shown.get(m, m) for m in COARSE_83)
    try:
        yield
    finally:
        HOME, ANSWERS, PUBLIC, SEED, PACKS, LAYERS, NEW, OUT, ACCEPTED, GROUPS, COARSE, SORTS, WHEN = old


def in_run_83(step):
    def run():
        with run_83():
            return step()
    return run


def figures_83():
    """The figures of the run with all 83 accepted words: those of figures() under its settings, the result by
    sort of word, the 40 entries with their sort and meaning, the first run's bars beside it, and the cost as far
    as it was reported. Without the local file of the packs' wording the figures would carry that wording, which
    follows the lexicon's for four words in a row, so they are not counted."""
    if not PACK_WORDING.exists():
        raise SystemExit(f"{PACK_WORDING} is missing: the figures would carry the packs' wording of four meanings")
    first_run = read("result.json")["figures"]
    with run_83():
        f, res = figures(), read("result.json")
        t = next(v for v in read(TOKENS).values() if isinstance(v, dict))
        readers = {f"K{n}_r{r}" for n in range(1, PACKS + 1) for r in range(1, READERS + 1)}
    rows = {r["entry"]: r for r in res["rows"] if r["sort"] != "open"}
    ours = {theirs: m for m, theirs in pack_wording().items()}             # the packs' wording -> the wording here
    f = in_our_words(f, ours)
    return f | {
        "by_sort": res["by_sort"],
        "the_40": {h: {"sort": why, "meaning": m, "kind": k, "shown": rows[h]["sort"], "outcome": outcome(rows[h])}
                   for why, hs in MORE.items() for h, (m, k) in sorted(hs.items())},
        "coarse_meanings": {m: sum(v[0] == m for v in NEW_83.values()) for m in sorted(COARSE_83)},
        "groups_added": len(GROUPS_83) - len(GROUPS), "layers": list(LAYERS_83),
        "run_with_43": {k: first_run[k] for k in ("offered", "offered_chosen", "offered_right", "right_when_chosen", "absent", "absent_wrong",
                                                    "wrong_when_absent", "bar1", "bar2")},
        "cost": {"agents": len(readers), "with_a_count": len(t), "tokens_counted": sum(t.values()), "without_a_count": sorted(readers - set(t))},
    }


def in_our_words(x, ours):
    """Figures with every meaning in the wording of this file: `ours` maps the packs' wording to it."""
    if isinstance(x, dict):
        return {ours.get(k, k): in_our_words(v, ours) for k, v in x.items()}
    if isinstance(x, list):
        return [in_our_words(v, ours) for v in x]
    return ours.get(x, x) if isinstance(x, str) else x


def public():
    PUBLIC.write_text(json.dumps(figures(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    PUBLIC_83.write_text(json.dumps(figures_83(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", PUBLIC.relative_to(ROOT), "and", PUBLIC_83.relative_to(ROOT))


COMMANDS = {"words": words, "packs": packs, "count": count, "words-83": in_run_83(words), "packs-83": in_run_83(packs),
            "count-83": in_run_83(count), "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
