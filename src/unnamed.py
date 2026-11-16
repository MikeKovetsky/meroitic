"""The open spellings the lexicon does not hold (step G3, data/discovery/unnamed_spellings.md): is each place a
name, a piece of a word beside it, a word of its own, or unclear? Two checkers decide every place from the place
alone; places whose answer the map holds are mixed in as controls, and a reading counts only if the controls and
the checkers' agreement meet bars set beforehand.

Everything is read and written under data/sources/g3/ (local only: the packs show the map's readings), except
`public`, which writes the figures of the page.

  python3 -I src/unnamed.py pilot-packs     the first pilot: 100 places and 50 controls for two checkers
  python3 -I src/unnamed.py pilot           its count (it missed two bars and is not taken)
  python3 -I src/unnamed.py pilot2-packs    the second pilot: 100 other places, corrected controls, the script's joins
  python3 -I src/unnamed.py pilot2          its count
  python3 -I src/unnamed.py full-packs      every place the second pilot did not judge, a tenth more as controls
  python3 -I src/unnamed.py full            its count
  python3 -I src/unnamed.py layer           the lines the step lays in the map (src/themap.py)
  python3 -I src/unnamed.py public          data/discovery/unnamed_spellings_figures.json

What the checkers were given is in runs/prompts/G3_places.md. A command that writes packs refuses once a checker
of that reading has answered.
"""
import collections
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import lexicon as X                                    # noqa: E402
import recurring as W                                  # noqa: E402
import themap as M                                     # noqa: E402

HOME = ROOT / "data/sources/g3"
PUBLIC = ROOT / "data/discovery/unnamed_spellings_figures.json"
LAYER = "unnamed"                                      # this step's layer in src/themap.py
SEED, PILOT, PACK, WIDTH = 20261116, 100, 50, 5
CONTROLS = {"word": 20, "name": 15, "cut": 15}         # the first pilot's controls
CASES = ("name", "piece", "word", "unclear")
BARS = {"kappa": 0.6, "words_called_name_or_piece": 0.10, "names_called_name": 0.70, "cuts_called_piece_of_the_whole": 0.70}
READINGS = ("pilot", "pilot2", "full")                 # in the order they were made
TAKEN = ("pilot2", "full")                             # the readings whose verdicts count: together every place, once
TOKENS = {r: f"tokens_{r}.json" for r in READINGS}     # from the task notifications, typed by hand (local)
# When the rules were set against the checkers they bind (2026-11-16, Pacific time), as src/rare.py records it:
# "set_in" is the commit of the rules a reading's checkers worked under and "set" its time in git; "started" is the
# reading's first launch and "counted" the command that first counted its answers, both in the session's log, by
# hand; "first_answer" and "last_answer" are the earliest and the latest times of its answer files under HOME.
WHEN = [
    {"reading": "pilot", "set_in": "7395a7f", "set": "13:59:53", "started": "14:00:00",
     "first_answer": "14:00:49", "last_answer": "14:01:04", "counted": "14:01:19"},
    {"reading": "pilot2", "set_in": "1ba8a90", "set": "14:03:42", "started": "14:03:47",
     "first_answer": "14:04:43", "last_answer": "14:04:55", "counted": "14:05:09"},
    {"reading": "full", "set_in": "7f2cddb", "set": "14:05:38", "started": "14:05:45",
     "first_answer": "14:06:23", "last_answer": "14:09:17", "counted": "14:09:27"},
]
NORTH_STAR_RULE = {"set_in": "47e77e3", "set": "14:09:13"}  # how the north star is counted after the step (section 9
#                                                            of the page): set before the full pass was counted

BRIEF = """# Decide, place by place, what {places} Meroitic spellings are

The project's word-by-word map of the Meroitic corpus has no accepted meaning for the spellings below, and the
dictionary of Meroitic does not hold them. Many such "words" are not words of their own: the edition's word
division has cut a longer word or a name in two, or the spelling is a personal, place or divine name, which needs
no meaning. Your task is to decide, for every place listed, what the spelling in bold is **in that place**.

For every place give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

    {{"place": "Q017", "case": "piece", "whole": "woSi", "why": "<at most twenty words>"}}

- "case" is one of:
  - "name": a personal name, a place name or a god's name (or a part of one that is itself only a name). Say so
    only when the place shows it: it stands where the formulae of this kind of text put a name (the deceased
    after the opening invocation of an epitaph, a parent before a word of filiation, a person after a title or
    before a title in a list of relatives, a place before a locative ending, a god in an invocation), or the words
    around it are names of the same kind.
  - "piece": no word of its own: a part of a longer word (or name) whose other part stands right before or right
    after it, cut off by the word division. Put the whole word, joined, in the project's letters, in "whole" (for
    `wo` before `Si`: "woSi").
  - "word": a word of its own (a noun, a verb, a title, an epithet, a particle) whose meaning nobody has. This is
    the case when nothing in the place shows a name or a cut.
  - "unclear": signs are lost in or around it, or the context shown is too thin to decide.
- Decide each place on what is shown for it: the words around it and the map's reading of each. A reading in
  square brackets is a word the map has no accepted meaning for: `[form: ?]` when it knows nothing of it,
  `[form: a guess (?)]` when an analyst made a guess. The word to judge is always shown as `[form: ?]`. Do not open any file, do not look the spelling up, do
  not use what you may know of Meroitic beyond what is shown, and do not search the web.
- Some places are put in on purpose: their answer is known. They look like the others.
- "whole" is empty unless the case is "piece".

Letters: the project writes `S` for the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ.

This pack lists {places} places: your file must have {places} lines, one for each place, none left out. When the
file is written, count its lines against that number, then reply in one line: how many places, and how many of
each case.
"""


NOTE = """- Under some places a script's note says that the word, joined with the word before or after it, gives a
  spelling the map holds. The note is a fact about letters, not a judgment: say "piece" only if the place fits it.
"""
BRIEF2 = BRIEF.replace("- Some places are put in on purpose:", NOTE + "- Some places are put in on purpose:")
assert BRIEF2 != BRIEF
BARS2 = {"kappa": 0.6, "words_called_name": 0.10, "names_called_name": 0.70}
CONTROLS2 = {"word": 20, "name": 15, "particle": 15}


def read(name):
    return json.loads((HOME / name).read_text(encoding="utf-8"))


def write(name, data):
    (HOME / name).parent.mkdir(parents=True, exist_ok=True)
    (HOME / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def before():
    """The map this step works on: the analysts' map with the layers laid before this step's own."""
    return M.current(upto=[l["name"] for l in M.LAYERS].index(LAYER))


def holds(gl):
    """The spellings the map holds as translated or named."""
    return {f for f, c in W.spellings_of(gl)[0].items() if c.most_common(1)[0][0] in W.READ + W.NAMED}


def population(gl, lex):
    """The places of kind c: the open spellings that stand in one or two texts and that the lexicon does not hold."""
    level, texts, heads = W.spellings_of(gl)
    forms = {f for f, c in level.items() if c.most_common(1)[0][0] in W.OPEN and len(texts[f]) <= 2
             and W.key_of(f, [h for h in heads[f].most_common(1)[0][0] if h not in X.PSEUDO], lex)[1] == "not in the lexicon"}
    return sorted((t, i + 1) for t, gs in gl.items() for i, g in enumerate(gs) if g["form"] in forms and g["level"] in W.OPEN)


def shown(gs, i, hide, rows, t):
    """One place for a pack: the word at index i of the words gs, WIDTH words on each side, the map's reading of
    each; the words at the indexes `hide` (the word judged, and for a cut its other half) are shown as the map
    shows a word it knows nothing of, `[form: ?]`, so that a real place and a control look alike."""
    lo, hi = max(0, i - WIDTH), min(len(gs), i + WIDTH + 1)
    words = " ".join(f"**{g['form']}**" if j == i else g["form"] for j, g in enumerate(gs[lo:hi], lo))
    readings = " · ".join(f"[{g['form']}: ?]" if j in hide else W.R.word_reading(g) for j, g in enumerate(gs[lo:hi], lo))
    r = rows.get(t) or {}
    return {"text": t, "kind": r.get("kind") or "", "site": (r.get("site") or "").split(":")[0][:40], "n": i + 1, "of": len(gs),
            "form": gs[i]["form"], "words": words, "readings": readings}


def pick(rnd, texts, cands, k):
    """k of the candidate places, drawn by lot from those in the texts of the real places where there are enough."""
    near = [c for c in cands if c[0] in texts]
    return rnd.sample(near if len(near) >= k else cands, k)


def names_of(gl):
    """The places of the names the analysts recognised that are no entry of the lexicon (no layer's)."""
    return sorted((t, i) for t, gs in gl.items() for i, g in enumerate(gs)
                  if g["level"] == "name" and "layer" not in g and [p.get("entry") for p in g.get("parts") or []] == ["NAME"])


def controls(gl, rnd, texts, n):
    """Places whose answer the map holds, shown as open: n["word"] translated words (the answer: a word of its own),
    n["name"] names the analysts recognised that are no entry of the lexicon, n["cut"] translated or named
    spellings of six letters or more cut in two at a place drawn by lot (the answer: a piece of that spelling).
    The words are taken from the texts of the real places where there are enough."""
    words = sorted((t, i) for t, gs in gl.items() for i, g in enumerate(gs) if g["level"] in W.READ and len(g["form"]) >= 3 and "layer" not in g)
    longs = sorted((t, i) for t, gs in gl.items() for i, g in enumerate(gs) if g["level"] in W.READ + W.NAMED and len(g["form"]) >= 6 and "layer" not in g)
    out = [{"control": "word", "text": t, "i": i, "answer": "word"} for t, i in pick(rnd, texts, words, n["word"])]
    out += [{"control": "name", "text": t, "i": i, "answer": "name"} for t, i in pick(rnd, texts, names_of(gl), n["name"])]
    for t, i in pick(rnd, texts, longs, n["cut"]):
        form = gl[t][i]["form"]
        at = rnd.randrange(2, len(form) - 1)
        out.append({"control": "cut", "text": t, "i": i, "answer": "piece", "whole": form, "at": at, "half": rnd.randrange(2)})
    return out


def controls2(gl, lex, rnd, texts, n):
    """The second pilot's controls, shown as open: n["word"] translated words built on a stem of the lexicon that
    is no function word (the answer: a word of its own; what is measured is how often a checker calls one a
    name), n["name"] names the analysts recognised that are no entry of the lexicon, n["particle"] endings or
    particles written as a word of their own (by the project's rule a piece of the word beside them; reported,
    under no bar)."""
    def what(g):
        ents = [p.get("entry") for p in g.get("parts") or []]
        if g["level"] not in W.READ or "layer" in g or not ents or any(e not in lex for e in ents):
            return None
        stems = [e for e in ents if not W.affix(e) and (lex[e].get("kind") or "") not in ("function word", "")]
        return "word" if stems and len(g["form"]) >= 3 else "particle" if not stems and len(g["form"]) >= 2 else None
    words = sorted((t, i) for t, gs in gl.items() for i, g in enumerate(gs) if what(g) == "word")
    parts = sorted((t, i) for t, gs in gl.items() for i, g in enumerate(gs) if what(g) == "particle")
    return ([{"control": "word", "text": t, "i": i, "answer": "word"} for t, i in pick(rnd, texts, words, n["word"])]
            + [{"control": "name", "text": t, "i": i, "answer": "name"} for t, i in pick(rnd, texts, names_of(gl), n["name"])]
            + [{"control": "particle", "text": t, "i": i, "answer": "piece"} for t, i in pick(rnd, texts, parts, n["particle"])])


def joins(gl, t, i, good):
    """What a script finds: the joins of the word with the word before it, after it, or both that give a spelling
    the map holds as translated or named."""
    gs = gl[t]
    f, a, b = gs[i]["form"], gs[i - 1]["form"] if i else None, gs[i + 1]["form"] if i + 1 < len(gs) else None
    return [j for j in ((a + f) if a else None, (f + b) if b else None, (a + f + b) if a and b else None) if j in good]


def place_of(c, gl, rows):
    gs = gl[c["text"]]
    if c.get("control") == "cut":
        form = gs[c["i"]]["form"]
        two = [{"form": form[:c["at"]], "level": "unknown"}, {"form": form[c["at"]:], "level": "unknown"}]
        gs = gs[:c["i"]] + two + gs[c["i"] + 1:]
        return shown(gs, c["i"] + c["half"], {c["i"], c["i"] + 1}, rows, c["text"])
    return shown(gs, c["i"], {c["i"]}, rows, c["text"])


def packs_of(folder, real, ctrl, gl, rows, rnd, brief, good=None):
    """Write a reading's packs: the real places and the controls, shuffled, PACK to a pack, for two checkers."""
    if any((HOME / folder).glob("answers*/*.jsonl")):
        raise SystemExit(f"{folder}: answers exist, the packs are not written again")
    items = [{"control": None, "text": t, "i": n - 1} for t, n in real] + ctrl
    rnd.shuffle(items)
    key = []
    for q, c in enumerate(items, 1):
        key.append({"place": f"Q{q:04d}", **c, **place_of(c, gl, rows),
                    **({} if good is None else {"joins": joins(gl, c["text"], c["i"], good)})})
    groups = [key[i: i + PACK] for i in range(0, len(key), PACK)]
    (HOME / folder / "packs").mkdir(parents=True, exist_ok=True)
    for n, g in enumerate(groups, 1):
        body = "\n".join(f"### {p['place']} — {p['text']} ({p['kind'] or 'kind not given'}{', ' + p['site'] if p['site'] else ''}), word {p['n']} of {p['of']}\n\n"
                         f"- Words: {p['words']}\n- Readings: {p['readings']}\n"
                         + "".join(f"- A script's note: joined with a word beside it, this gives `{j}`, a spelling the map holds.\n" for j in p.get("joins", [])) for p in g)
        for c in (1, 2):
            (HOME / folder / f"answers{c}").mkdir(exist_ok=True)
            text = brief.format(places=len(g), answers=f"data/sources/g3/{folder}/answers{c}/P{n:02d}.jsonl") + "\n---\n\n" + body
            (HOME / folder / "packs" / f"P{n:02d}_c{c}.md").write_text(text, encoding="utf-8")
    write(f"{folder}/key.json", key)
    write(f"{folder}/groups.json", [[p["place"] for p in g] for g in groups])
    print(folder, len(groups), "packs;", len(real), "places;", dict(collections.Counter(c["control"] for c in ctrl)), "controls")


def pilot_packs():
    gl, lex, rows = before(), W.lexicon(), W.corpus_rows()
    rnd = random.Random(SEED)
    pop = population(gl, lex)
    real = sorted(rnd.sample(pop, PILOT))
    write("population.json", {"places": len(pop), "spellings": len({gl[t][n - 1]["form"] for t, n in pop}), "pilot": real})
    packs_of("pilot", real, controls(gl, rnd, {t for t, _ in real}, CONTROLS), gl, rows, rnd, BRIEF)


def pilot2_packs():
    """The second pilot: 100 other places, the controls of controls2, the script's joins shown as a note."""
    gl, lex, rows = before(), W.lexicon(), W.corpus_rows()
    rnd = random.Random(SEED + 2)
    done = {tuple(p) for p in read("population.json")["pilot"]}
    real = sorted(rnd.sample([p for p in population(gl, lex) if p not in done], PILOT))
    write("pilot2/real.json", real)
    packs_of("pilot2", real, controls2(gl, lex, rnd, {t for t, _ in real}, CONTROLS2), gl, rows, rnd, BRIEF2, holds(gl))


def full_packs():
    """The full pass: every place the second pilot did not judge (the first pilot's among them: its verdicts were
    not taken), with controls that make up a tenth of the places, two thirds of them words and one third names."""
    gl, lex, rows = before(), W.lexicon(), W.corpus_rows()
    rnd = random.Random(SEED + 3)
    done = {tuple(p) for p in read("pilot2/real.json")}
    real = [p for p in population(gl, lex) if p not in done]
    k = len(real) // 10
    packs_of("full", real, controls2(gl, lex, rnd, {t for t, _ in real}, {"word": k - k // 3, "name": k // 3, "particle": 0}), gl, rows, rnd, BRIEF2, holds(gl))


def answers(folder, c):
    """A checker's lines, kept only for the places of the pack the file is named after, with a known case."""
    groups = read(f"{folder}/groups.json")
    return W.own_lines(HOME / folder / f"answers{c}", groups, "P{n:02d}", "place",
                       lambda r, n: r.get("place") if r.get("place") in groups[n - 1] and r.get("case") in CASES else None)


def right(p, a):
    """Whether a checker's answer to a control is the known one; for a cut, the piece of the right whole."""
    if p["control"] == "cut":
        return a["case"] == "piece" and W.joined(a.get("whole")) == p["whole"]
    return a["case"] == p["answer"]


def verdict(a, b):
    """A real place from its two checkers' answers: their case when they agree (for a piece, also on the whole)."""
    if not (a and b):
        return "not answered by both"
    if a["case"] != b["case"]:
        return "not agreed"
    if a["case"] == "piece" and W.joined(a.get("whole")) != W.joined(b.get("whole")):
        return "piece, the wholes differ"
    return a["case"]


def result_of(key, one, two, second):
    """A reading's figures and its bars. `second`: the bars of the second pilot and the full pass (a control word
    may not be called a name) in the place of the first pilot's (nor a piece; and the cut spellings found)."""
    real = [p for p in key if p["control"] is None]
    both = [(one[p["place"]]["case"], two[p["place"]]["case"]) for p in real if p["place"] in one and p["place"] in two]
    kp = W.kappa(both)
    ctrl = {}
    for j, ans in (("1", one), ("2", two)):
        c = {}
        for kind in sorted({p["control"] for p in key if p["control"]}):
            mine = [p for p in key if p["control"] == kind]
            c[kind] = {"shown": len(mine), "right": sum(right(p, ans[p["place"]]) for p in mine if p["place"] in ans),
                       **{f"called_{case}": n for case, n in sorted(collections.Counter(ans[p["place"]]["case"] for p in mine if p["place"] in ans).items())}}
        ctrl[j] = c
    def rate(kind, *cases):
        return [sum(c[kind].get(f"called_{x}", 0) for x in cases) / c[kind]["shown"] for c in ctrl.values()]
    bar = BARS2 if second else BARS
    bars = {"every_place_answered_by_both": all(p["place"] in one and p["place"] in two for p in key),
            "kappa": kp is not None and kp >= bar["kappa"],
            "names_called_name": all(r >= bar["names_called_name"] for r in rate("name", "name"))}
    if second:
        bars["words_called_name"] = all(r <= bar["words_called_name"] for r in rate("word", "name"))
    else:
        bars["words_called_name_or_piece"] = all(r <= bar["words_called_name_or_piece"] for r in rate("word", "name", "piece"))
        bars["cuts_called_piece_of_the_whole"] = all(c["cut"]["right"] >= bar["cuts_called_piece_of_the_whole"] * c["cut"]["shown"] for c in ctrl.values())
    rows = []
    for p in real:
        a, b = one.get(p["place"]), two.get(p["place"])
        v = verdict(a, b)
        rows.append({"place": p["place"], "text": p["text"], "n": p["n"], "form": p["form"], "verdict": v, "whole": W.joined(a.get("whole")) if v == "piece" else ""})
    return {"places": len(real), "answered_by_both": len(both), "kappa": None if kp is None else round(kp, 4), "controls": ctrl, "bars": bars,
            "taken": all(bars.values()), "verdicts": dict(collections.Counter(r["verdict"] for r in rows).most_common()),
            "pairs": dict(collections.Counter(f"{a} / {b}" for a, b in both).most_common()), "rows": rows}


def count(folder):
    out = result_of(read(f"{folder}/key.json"), answers(folder, 1), answers(folder, 2), second=folder != "pilot")
    write(f"{folder}/result.json", out)
    print(folder, {k: v for k, v in out.items() if k != "rows"})


# ----------------------------------------------------------------------------------------- what is laid in the map

def rows():
    """Every real place with its verdict, from the readings that count; a reading that missed a bar stops this."""
    out = []
    for folder in TAKEN:
        res = read(f"{folder}/result.json")
        if not res["taken"]:
            raise SystemExit(f"{folder} missed a bar: nothing is taken from it")
        out += res["rows"]
    return out


def lines_of(gl, rs):
    """(the lines the step lays in the map, the pieces it leaves out and why). A place both checkers call a name is
    laid as a name; a piece only where both name the same whole and gl holds that whole as translated or named."""
    level, gloss = W.form_levels(gl)
    out, apart = [], collections.Counter()
    for r in rs:
        g = gl[r["text"]][r["n"] - 1]
        if g["form"] != r["form"]:
            raise SystemExit(f"the map has {g['form']!r} at {(r['text'], r['n'])}, the reading {r['form']!r}")
        base = {"text": r["text"], "n": r["n"], "form": r["form"], "item": r["form"], "was": g["level"]}
        if r["verdict"] == "name":
            out.append(base | {"level": "name", "gloss": "a name, by its place in the text", "why": "name", "source": "two checkers, from the place"})
        elif r["verdict"] == "piece":
            lv = level[r["whole"]].most_common(1)[0][0] if r["whole"] in level else None
            if lv in W.READ + W.NAMED:
                out.append(base | {"level": lv, "gloss": f"part of {r['whole']}: {gloss[r['whole']]}", "why": "piece", "source": "the map's reading of the whole word"})
            else:
                apart["piece, the whole word " + ("open in the map" if lv in W.OPEN else "not a form of the map")] += 1
    return out, dict(apart)


def layer():
    lines, apart = lines_of(before(), rows())
    (HOME / "overlay.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in lines), encoding="utf-8")
    print(len(lines), "lines", dict(collections.Counter(o["why"] for o in lines)), dict(collections.Counter(o["level"] for o in lines)), "left out:", apart)


# ---------------------------------------------------------------------------------------------------- the figures

def figures():
    gl, lex = before(), W.lexicon()
    pop, rs = population(gl, lex), rows()
    lines, apart = lines_of(gl, rs)
    good = holds(gl)
    figs = {"places": len(pop), "spellings": len({gl[t][n - 1]["form"] for t, n in pop}),
            "places_where_a_script_finds_a_join": sum(bool(joins(gl, t, n - 1, good)) for t, n in pop),
            "readings": {f: {k: v for k, v in read(f"{f}/result.json").items() if k != "rows"} for f in READINGS},
            "taken": list(TAKEN), "verdicts": dict(collections.Counter(r["verdict"] for r in rs).most_common()),
            "laid": {"lines": len(lines), "why": dict(collections.Counter(o["why"] for o in lines).most_common()),
                     "to": dict(collections.Counter(o["level"] for o in lines).most_common()),
                     "was": dict(collections.Counter(o["was"] for o in lines).most_common())}, "left_out": apart, "cost": {}}
    for f, name in TOKENS.items():
        if (HOME / name).exists():
            t = read(name)
            figs["cost"][f] = {"agents": len(t), "tokens": sum(t.values())}
    return figs


def public():
    figs = figures()
    PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: figs[k] for k in ("places", "verdicts", "laid", "left_out", "cost")}, ensure_ascii=False))


COMMANDS = {"pilot-packs": pilot_packs, "pilot": lambda: count("pilot"), "pilot2-packs": pilot2_packs, "pilot2": lambda: count("pilot2"),
            "full-packs": full_packs, "full": lambda: count("full"), "layer": layer, "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
