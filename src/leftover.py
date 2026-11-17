"""The leftover parts, and the meanings Millet and Lipinski state (a follow-up to G2 and G4,
data/discovery/leftover_parts.md).

Part 1: the places of the rare spellings (src/rare.py) that both checkers called a form of a stem's entry and that
were not laid because the map leaves a part of the spelling unnamed. Two checkers say what the unnamed part is;
places of known answer are mixed in. Part 2: the entries of G4 without a meaning from Rilly's later work for which
Millet 2005 or Lipinski 2011 states one: the rule of G4 again, with the source changed.

Part 1 was read twice (data/discovery/leftover_parts_2.md): the first reading missed a bar and is not taken; the
second, by fresh checkers on controls drawn anew, has a bar for each verdict and lays only what both checkers call
an ending or a known word, never a name.

Part 1 is read and written under data/sources/g8/ (the first reading) and data/sources/g8b/ (the second), part 2
under data/sources/rare/g4m/ (local only: the packs and the answers quote the sources), except `public`.

  python3 -I src/leftover.py packs          part 1: the places and the controls for two checkers (packs/, key.json)
  python3 -I src/leftover.py count          part 1: the checkers compared, the bars (result.json)
  python3 -I src/leftover.py packs-again    part 1, the second reading: the same places, controls drawn anew
  python3 -I src/leftover.py count-again    part 1, the second reading: the checkers compared, its own bars
  python3 -I src/leftover.py layer-again    part 1, the second reading: the lines for the map (overlay.jsonl)
  python3 -I src/leftover.py setup          part 2: the entries (items.json, lit/)
  python3 -I src/leftover.py verify-packs   part 2: the statements for two readers
  python3 -I src/leftover.py verify         part 2: what the source states, and what it gives (a word, a name)
  python3 -I src/leftover.py place-packs    part 2: the places for two checkers
  python3 -I src/leftover.py places         part 2: the checkers compared, the bar
  python3 -I src/leftover.py layer          part 2: the lines for the map (overlay.jsonl; src/themap.py lays them)
  python3 -I src/leftover.py public         data/discovery/leftover_parts_figures.json

What the checkers of part 1 were given is in runs/prompts/G8_parts.md and G8_parts_2.md.
"""
import collections
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import lexicon as X                                    # noqa: E402
import rare as R                                       # noqa: E402
import recurring as W                                  # noqa: E402
import themap as M                                     # noqa: E402
import unnamed as U                                    # noqa: E402
import words as D                                      # noqa: E402

HOME = ROOT / "data/sources/g8"                        # part 1, the first reading
HOME_AGAIN = ROOT / "data/sources/g8b"                 # part 1, the second reading
PUBLIC = ROOT / "data/discovery/leftover_parts_figures.json"
LAYER = "rare_millet"                                  # part 2's layer in src/themap.py
LAYER_AGAIN = "leftover"                               # the layer of part 1's second reading, laid after part 2's
BEFORE = ("recurring", "rare_sure", "rare_later", "unnamed")   # the layers laid when the step was set
TOKENS = {"part 1, the checkers": HOME / "tokens.json",                 # from the task notifications, typed by hand
          "part 2, the readers": R.HOME / "g4m" / "tokens_verify.json",   # (local); each holds {"note", <who>: {pack: n}}
          "part 2, the checkers": R.HOME / "g4m" / "tokens_places.json",
          "part 1 again, the checkers": HOME_AGAIN / "tokens.json"}
# When the rules were set against the agents (2026-11-16, Pacific time): the commit of the rules and its time in
# git; the first launch and the count (the session's log, by hand: the launch is the earliest answer's time less
# its agent's run time; for the second reading of part 1 it is the clock read in the message that launched it);
# the earliest and the latest times of the answer files.
WHEN = [
    {"step": "part 1, the unnamed parts", "set_in": "1c86898", "set": "15:23:46", "started": "15:27:11", "first_answer": "15:28:06",
     "last_answer": "15:29:31", "counted": "15:30:41", "answers": ["g8/answers1", "g8/answers2"]},
    {"step": "part 2, the statements read twice", "set_in": "4b0c763", "set": "15:35:28", "started": "15:35:38", "first_answer": "15:36:13",
     "last_answer": "15:37:16", "counted": "15:38:26", "answers": ["rare/g4m/lit/verify/answers1", "rare/g4m/lit/verify/answers2"]},
    {"step": "part 2, the places", "set_in": "4b0c763", "set": "15:35:28", "started": "15:38:47", "first_answer": "15:39:08",
     "last_answer": "15:40:08", "counted": "15:40:35", "answers": ["rare/g4m/places/answers1", "rare/g4m/places/answers2"]},
    {"step": "part 1 again, the unnamed parts", "set_in": "ebfa9e3", "set": "15:51:18", "started": "15:51:35", "first_answer": "15:52:36",
     "last_answer": "15:53:01", "counted": "15:53:14", "answers": ["g8b/answers1", "g8b/answers2"]},
]
# The meanings Lipinski 2011 gives the two words of the dictionary that part 2 lays, in a few words of our own
# (the readers' wordings follow their source and stay local); tests/test_leftover.py holds each to the rule of
# src/lexicon.py: no four words in a row of the lexicon of 2003 or of Rilly 2016 and 2021.
MEANINGS = {"mse": "child", "kdimdḫe": "women who have not borne a child"}
# The same for the two words of the dictionary that the second reading of part 1 is the first to lay as translated
# words: Rilly 2016 gives the first its meaning, Rilly 2021 the second.
MEANINGS_AGAIN = {"nbr": "gold", "yiroẖe": "to take control"}

# ------------------------------------------------------------------------------- part 1: the unnamed parts

SEED, PACK = 20261116 + 8, 46
CONTROLS = {"ending": 20, "junk": 20}
CASES = ("ending", "known", "name", "unknown", "unclear")
BARS = {"kappa": 0.6, "junk_explained": 0.10, "endings_called_ending": 0.70}
LETTERS = "abdeiklmnoqrstwyxXSN"
# The second reading: a seed of its own, and a bar for each verdict. The bar on the letters drawn by lot counts only
# what can still be laid, an ending or a known word (LAID); a name is not laid, so no bar rests on it.
SEED_AGAIN = 20261116 + 9
BARS_AGAIN = {"kappa": 0.6, "junk_called_ending_or_known": 0.10, "endings_called_ending": 0.70}
LAID = ("ending", "known")

BRIEF = """# Say what the unnamed part of {places} Meroitic spellings is

In each place below, the project's map of the Meroitic corpus cuts the spelling in bold into parts and ties some
of them to entries of the dictionary of Meroitic (Rilly's lexicon of 2003). One part or more is left **unnamed**.
Your task is to say, for every place, what the unnamed part is.

For every place give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

    {{"place": "Q017", "case": "ending", "entry": "", "why": "<at most twenty words>"}}

- "case" is one of:
  - "ending": the unnamed part is nothing but endings, prefixes or particles of the word (one or several), or
    letters of a variant writing of the named part. With it the spelling is still the named word and no other.
  - "known": the unnamed part is another word that the lexicon holds with a meaning it calls established or
    probable. Put that entry's headword in "entry".
  - "name": the unnamed part is a personal, place or divine name (the spelling joins a name to the named word).
  - "unknown": the unnamed part is a word or a run of letters that nothing in hand explains. Say this also when
    the part could be cut into endings only by taking it letter by letter, with nothing in the place to show it.
  - "unclear": signs are lost in it, or the place is too thin to decide.
- You may search the lexicon (`data/rilly2003/`, JSON lines) for the unnamed part or for pieces of it. The lexicon
  writes ḫ where the project writes `x`, ẖ for `X`, s for `S`, se for `s`, and ne or ñ for `N`. Open no other
  file, do not search the web, and do not use what you may know of Meroitic beyond the lexicon and what is shown.
- Some places are put in on purpose: their answer is known. They look like the others.
- "entry" is empty unless the case is "known".

This pack lists {places} places: your file must have {places} lines, one for each place, none left out. When the
file is written, count its lines against that number, then reply in one line: how many places, and how many of
each case.
"""


def rule(again=False):
    """A reading of part 1: (its folder, its seed, its bars, the name of its bar on the letters drawn by lot, the
    cases that bar counts as an explanation)."""
    if again:
        return HOME_AGAIN, SEED_AGAIN, BARS_AGAIN, "junk_called_ending_or_known", LAID
    return HOME, SEED, BARS, "junk_explained", ("ending", "known", "name")


def read(name, home=None):
    """A file of a reading of part 1: of the first one (HOME) unless another reading's folder is given."""
    return json.loads(((home or HOME) / name).read_text(encoding="utf-8"))


def write(name, data, home=None):
    f = (home or HOME) / name
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def before():
    """The map with the layers laid when this step was set (G1, G2, G4 and G3), without part 2's own."""
    names = [l["name"] for l in M.LAYERS]
    if tuple(names[:len(BEFORE)]) != BEFORE:
        raise SystemExit(f"the layers before this step are no longer {BEFORE}")
    return M.current(upto=len(BEFORE))


def real_places(gl, lex):
    """The stated places of G2 and G4 under a stem's entry that are not laid: [(run, entry, text, n)]."""
    out = []
    for run in R.LAYER:
        R.here(run)
        its = R.place_items(run)[0]
        for r in R.taken(run)[1]["rows"]:
            if r["verdict"] != "stated" or its[r["item"]]["how"].startswith("affix"):
                continue
            p = its[r["item"]]["places"][r["place"] - 1]
            if "layer" not in gl[p["text"]][p["n"] - 1]:
                out.append({"control": None, "run": run, "entry": r["item"], "text": p["text"], "i": p["n"] - 1})
    W.OUT = R.RECURRING
    return out


def parts_of(g, hide=()):
    """The word's parts as the pack shows them: (letters, the entry's headword or None for an unnamed part)."""
    return [(p.get("form") or "", None if j in hide or p.get("entry") is None or p.get("entry") in X.PSEUDO else p["entry"])
            for j, p in enumerate(g.get("parts") or [])]


def controls(gl, lex, rnd, n):
    """Places whose answer is known: translated words of one stem and endings with the endings shown as unnamed
    (the answer: ending), and translated words with letters drawn by lot put before or after them and shown as an
    unnamed part (the answer: unknown)."""
    words = sorted((t, i) for t, gs in gl.items() for i, g in enumerate(gs) if g["level"] in W.READ and "layer" not in g
                   and (ents := [p.get("entry") for p in g.get("parts") or []]) and all(e in lex for e in ents)
                   and sum(not W.affix(e) for e in ents) == 1)
    with_endings = [(t, i) for t, i in words if len(gl[t][i]["parts"]) > 1]
    holds = set(W.spellings_of(gl)[0])
    out = []
    for t, i in rnd.sample(with_endings, n["ending"]):
        hide = [j for j, p in enumerate(gl[t][i]["parts"]) if W.affix(p["entry"])]
        out.append({"control": "ending", "answer": "ending", "text": t, "i": i, "hide": hide})
    for t, i in rnd.sample(words, n["junk"]):
        while True:
            junk = "".join(rnd.choice(LETTERS) for _ in range(rnd.randrange(3, 6)))
            if junk not in holds:
                break
        out.append({"control": "junk", "answer": "unknown", "text": t, "i": i, "junk": junk, "front": rnd.random() < 0.5})
    return out


def place_of(c, gl, rows):
    gs = gl[c["text"]]
    g = gs[c["i"]]
    parts = parts_of(g, c.get("hide", ()))
    if c.get("control") == "junk":
        parts = [(c["junk"], None)] + parts if c["front"] else parts + [(c["junk"], None)]
        g = {"form": "".join(f for f, _ in parts), "level": "unknown"}
        gs = gs[:c["i"]] + [g] + gs[c["i"] + 1:]
    shown = U.shown(gs, c["i"], {c["i"]}, rows, c["text"])
    return shown | {"parts": parts}


def packs(home=None, again=False):
    """The packs of a reading of part 1 (the second one with `again`): the same places, the controls and the order
    drawn with the reading's seed. `home` is another folder to write them to."""
    folder, seed = rule(again)[:2]
    home = home or folder
    if any(home.glob("answers*/*.jsonl")):
        raise SystemExit("answers exist: the packs are not written again")
    gl, lex, rows = before(), W.lexicon(), W.corpus_rows()
    rnd = random.Random(seed)
    items = real_places(gl, lex) + controls(gl, lex, rnd, CONTROLS)
    rnd.shuffle(items)
    key = [{"place": f"Q{q:04d}", **c, **place_of(c, gl, rows)} for q, c in enumerate(items, 1)]
    groups = [key[i: i + PACK] for i in range(0, len(key), PACK)]
    (home / "packs").mkdir(parents=True, exist_ok=True)
    folder = home.relative_to(ROOT) if home.is_relative_to(ROOT) else home

    def cut(p):
        return "; ".join(f"`{f}` = unnamed" if e is None else f"`{f}` = the lexicon's entry `{e}`" + (f" ({lex[e]['meaning'][:60]})" if lex.get(e, {}).get("meaning") else "")
                         for f, e in p["parts"])
    for n, g in enumerate(groups, 1):
        body = "\n".join(f"### {p['place']} — {p['text']} ({p['kind'] or 'kind not given'}{', ' + p['site'] if p['site'] else ''}), word {p['n']} of {p['of']}\n\n"
                         f"- Words: {p['words']}\n- Readings: {p['readings']}\n- The spelling's parts: {cut(p)}\n" for p in g)
        for c in (1, 2):
            (home / f"answers{c}").mkdir(exist_ok=True)
            text = BRIEF.format(places=len(g), answers=f"{folder}/answers{c}/P{n:02d}.jsonl") + "\n---\n\n" + body
            (home / "packs" / f"P{n:02d}_c{c}.md").write_text(text, encoding="utf-8")
    write("key.json", key, home)
    write("groups.json", [[p["place"] for p in g] for g in groups], home)
    print(len(groups), "packs;", sum(p["control"] is None for p in key), "places;", dict(collections.Counter(p["control"] for p in key if p["control"])), "controls;",
          dict(collections.Counter(p["run"] for p in key if p["control"] is None)))


def answers(c, home=None):
    """A checker's lines, kept only for the places of its own pack and with a case of CASES; the first line wins."""
    home = home or HOME
    groups, out = read("groups.json", home), {}
    for n, g in enumerate(groups, 1):
        f = home / f"answers{c}" / f"P{n:02d}.jsonl"
        for line in f.read_text(encoding="utf-8").splitlines() if f.exists() else []:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(r, dict) and r.get("place") in g and r.get("case") in CASES:
                out.setdefault(r["place"], r)
    return out


def count(home=None, again=False):
    """A reading of part 1 counted against its own bars (those of the second reading with `again`)."""
    folder, _, bars_set, lot_bar, explained = rule(again)
    home = home or folder
    key, lex = read("key.json", home), W.lexicon()
    one, two = answers(1, home), answers(2, home)
    real = [p for p in key if p["control"] is None]
    both = [(one[p["place"]]["case"], two[p["place"]]["case"]) for p in real if p["place"] in one and p["place"] in two]
    kp = W.kappa(both)
    ctrl = {str(j): {kind: {"shown": sum(p["control"] == kind for p in key),
                            **{f"called_{k}": v for k, v in sorted(collections.Counter(ans[p["place"]]["case"] for p in key if p["control"] == kind and p["place"] in ans).items())}}
                     for kind in ("ending", "junk")} for j, ans in ((1, one), (2, two))}
    bars = {"every_place_answered_by_both": all(p["place"] in one and p["place"] in two for p in key),
            "kappa": kp is not None and kp >= bars_set["kappa"],
            lot_bar: all(sum(c["junk"].get(f"called_{k}", 0) for k in explained) <= bars_set[lot_bar] * c["junk"]["shown"] for c in ctrl.values()),
            "endings_called_ending": all(c["ending"].get("called_ending", 0) >= bars_set["endings_called_ending"] * c["ending"]["shown"] for c in ctrl.values())}
    rows = []
    for p in real:
        a, b = one.get(p["place"]), two.get(p["place"])
        v = "not answered by both" if not (a and b) else "not agreed" if a["case"] != b["case"] else a["case"]
        if v == "known":
            ea, eb = (a.get("entry") or "").strip(), (b.get("entry") or "").strip()
            v = "known" if ea == eb and (lex.get(ea, {}).get("status") or "") in W.SURE else "known, not the same sure entry"
        rows.append({"place": p["place"], "run": p["run"], "entry": p["entry"], "text": p["text"], "n": p["n"], "form": p["form"], "verdict": v})
    out = {"places": len(real), "answered_by_both": len(both), "kappa": None if kp is None else round(kp, 4), "controls": ctrl, "bars": bars,
           "taken": all(bars.values()), "verdicts": dict(collections.Counter(r["verdict"] for r in rows).most_common()),
           "by_run": {run: dict(collections.Counter(r["verdict"] for r in rows if r["run"] == run).most_common()) for run in R.LAYER}, "rows": rows}
    write("result.json", out, home)
    print({k: v for k, v in out.items() if k != "rows"})


OTHER_STEM = "another stem of the spelling has no meaning"


def lines_again(rows, gl, lex, stated, verified):
    """(the lines the second reading lays, the places it leaves out and why). A place both checkers call an ending,
    or a known word with the same sure entry, takes the level of its entry as in the rare spellings (src/rare.py),
    unless another stem of the spelling has no meaning. A place both call a name is not laid. `verified` is
    {run: the meanings of that run's entries}; gl is the map with the layers laid when the step was set."""
    out, apart = [], collections.Counter()
    for run in R.LAYER:
        for r in rows:
            if r["run"] != run or r["verdict"] not in LAID:
                continue
            g = gl[r["text"]][r["n"] - 1]
            if g["form"] != r["form"] or "layer" in g:
                raise SystemExit(f"{r['place']}: the map has changed at this place")
            if R.unsettled(g, lex, stated):
                apart[OTHER_STEM] += 1
                continue
            v = verified[run][r["entry"]]["one"]
            out.append({"text": r["text"], "n": r["n"], "form": r["form"], "item": r["entry"], "was": g["level"],
                        "level": R.level_of(r["entry"], lex), "gloss": v["meaning"], "why": "form" if run == "g2" else "stated",
                        "source": f"{v['source']}, p. {v['page']}"})
    return out, dict(apart)


def build_again(home=None):
    """lines_again() on the second reading's result, if its bars are met; with the meanings of each run's entries."""
    res = read("result.json", home or HOME_AGAIN)
    if not res["taken"]:
        raise SystemExit("a bar was missed: nothing is laid")
    gl, lex = before(), W.lexicon()
    stated = R.stated_entries(json.loads((R.RECURRING / "lit/verify/result.json").read_text(encoding="utf-8")),
                              json.loads((R.HOME / "g4/lit/verify/result.json").read_text(encoding="utf-8")))
    verified = {}
    for run in R.LAYER:
        R.here(run)
        verified[run] = R.place_items(run)[3]
    W.OUT = R.RECURRING
    return *lines_again(res["rows"], gl, lex, stated, verified), verified


def layer_again():
    out, apart, _ = build_again()
    (HOME_AGAIN / "overlay.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out), encoding="utf-8")
    print(len(out), "lines", dict(collections.Counter(o["why"] for o in out)), dict(collections.Counter(o["level"] for o in out)),
          "left out:", apart)


# ----------------------------------------------------------------- part 2: Millet 2005 and Lipinski 2011

RUN = "g4m"
HOME2 = R.HOME / RUN                                   # part 2
SOURCES = ("Millet 2005", "Lipinski 2011")
WHAT = ("word", "name", "partly")

OLD_SOURCE = '"source": "<Rilly 2016 or Rilly 2021, the one that states it most firmly>", "page": 12, "stance": "accepts", '
NEW_SOURCE = ('"source": "<Millet 2005 or Lipinski 2011, the one that states it most firmly>", "page": 12, "stance": "accepts", '
              '"what": "word", ')
OLD_STANCE = '- "stance": "accepts" when'
NEW_WHAT = """- Judge only what Millet 2005 or Lipinski 2011 states; the statements of other sources are shown for context.
- "what": what that source gives for the item. "name" when it states that the item is a name (of a person, a
  place, a people or a god); "word" when it gives a meaning in full, in the source's own language; "partly" when
  the meaning it gives leaves a Meroitic word as it is (for instance "chief X in Y" with X not translated). Empty
  when the stance is "none".
"""
OLD_FILES = "In the files with `=== page N ===` markers"
NEW_FILES = ("Millet 2005 is `data/sources/jssea-text/pages.txt`, Lipinski 2011 is "
             "`data/sources/lipinski2011-text/pages.txt`. In the files with `=== page N ===` markers")


def brief():
    b = W.VERIFY_BRIEF
    for old, new in ((OLD_SOURCE, NEW_SOURCE), (OLD_STANCE, NEW_WHAT + OLD_STANCE), (OLD_FILES, NEW_FILES)):
        if b.count(old) != 1:
            raise SystemExit(f"the brief of G4 has changed: {old[:40]!r} stands {b.count(old)} times in it")
        b = b.replace(old, new)
    return b


def picked():
    """The entries of G4 that did not pass the bar of class A and for which the literature pass found a statement
    of Millet 2005 or of Lipinski 2011 with the stance "accepts" or "probable"."""
    g4 = R.HOME / "g4"
    its = json.loads((g4 / "items.json").read_text(encoding="utf-8"))
    checked = json.loads((g4 / "lit/checked.json").read_text(encoding="utf-8"))
    classes = json.loads((g4 / "lit/classes.json").read_text(encoding="utf-8"))
    keep = [it for it in its if classes[it["item"]] != W.CLASSES["A"]
            and any(s["source"] in SOURCES and s["stance"] in W.FIRM for s in checked[it["item"]]["statements"])]
    return keep, checked


def setup():
    R.here(RUN)
    HOME2.mkdir(parents=True, exist_ok=True)
    R.answered(RUN, ["lit/verify/answers1", "lit/verify/answers2"] + [f"{f}/answers{c}" for f in R.FOLDER.values() for c in (1, 2)])
    keep, checked = picked()
    (HOME2 / "lit").mkdir(exist_ok=True)
    W.write("items.json", keep)
    W.write("lit/checked.json", {it["item"]: checked[it["item"]] for it in keep})
    W.write("lit/classes.json", {it["item"]: W.CLASSES["A"] for it in keep})
    print(len(keep), "entries,", sum(it["uses"] for it in keep), "places,",
          dict(collections.Counter(s["source"] for it in keep for s in checked[it["item"]]["statements"]
                                   if s["source"] in SOURCES and s["stance"] in W.FIRM)))


def verify_packs():
    old = W.VERIFY_BRIEF
    W.VERIFY_BRIEF = brief()
    try:
        R.verify_packs(RUN)
    finally:
        W.VERIFY_BRIEF = old


def verify():
    """W.verify(), then the rule of section 4: stated only when the source both readers name is Millet 2005 or
    Lipinski 2011; and what the statement gives, by both readers ("word", "name", "partly"; else "differ")."""
    R.verify(RUN)
    res = W.read("lit/verify/result.json")
    c = collections.Counter()
    for k, v in res.items():
        a, b = v["one"], v["two"]
        if v["verdict"] == "stated" and not (a.get("source") == b.get("source") and a.get("source") in SOURCES):
            v["verdict"] = "not stated by Millet 2005 or Lipinski 2011"
        wa, wb = (a.get("what") or "").strip(), (b.get("what") or "").strip()
        v["what"] = wa if wa == wb and wa in WHAT else "differ"
        c[v["verdict"], v["what"]] += 1
    W.write("lit/verify/result.json", res)
    print({f"{a} / {b}": n for (a, b), n in sorted(c.items())})


def place_packs():
    """R.place_packs with the brief of G4, and the count of lines each pack expects in the brief from the start."""
    R.place_packs(RUN)
    groups = W.read("places/groups.json")
    for n, group in enumerate(groups, 1):
        places = sum(hi - lo for _, lo, hi in group)
        for c in (1, 2):
            f = HOME2 / "places" / "packs" / f"P{n:02d}_c{c}.md"
            text = f.read_text(encoding="utf-8")
            if text.count(R.REPLY) != 1:
                raise SystemExit(f"{f.name}: the reply line stands {text.count(R.REPLY)} times")
            f.write_text(text.replace(R.REPLY, R.COUNTED.format(places=places)), encoding="utf-8")


def places():
    R.places(RUN)


def build():
    """(the lines part 2 lays, the places it leaves out and why), on the map with the layers laid before it: as in
    G4, and by the rule added before the readers were started: a translated word only when both readers say the
    source gives a meaning in full; a name when the lexicon calls the entry a name or both readers say the source
    states a name; else the place stays out."""
    lex, gl = W.lexicon(), before()
    R.here(RUN)
    stated = R.stated_entries(json.loads((R.RECURRING / "lit/verify/result.json").read_text(encoding="utf-8")),
                              json.loads((R.HOME / "g4/lit/verify/result.json").read_text(encoding="utf-8")),
                              W.read("lit/verify/result.json"))
    its, _, _, verified = R.place_items(RUN)
    res = R.taken(RUN)[1]
    laid, apart = R.lines_of("g4", gl, its, res["rows"], verified, lex, stated)
    W.OUT = R.RECURRING
    return its, verified, res, *given_as(laid, verified, apart)


LEFT = "stated, but the meaning leaves a Meroitic word as it is, or the readers differ on what is given"


def given_as(laid, verified, apart=()):
    """The lines of G4's rule by what the source gives: a line laid as a name stays; a stated place of an entry the
    source calls a name is laid as a name; one whose meaning is given in full stays a translated word; any other
    stated place is left out."""
    out, apart = [], collections.Counter(dict(apart))
    for o in laid:
        what = verified[o["item"]].get("what")
        if o["why"] != "stated" or o["level"] == "name":
            out.append(o)
        elif what == "name":
            out.append(o | {"level": "name", "why": "name"})
        elif what == "word":
            out.append(o)
        else:
            apart[LEFT] += 1
    return out, dict(apart)


def layer():
    _, _, _, out, apart = build()
    (HOME2 / "overlay.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out), encoding="utf-8")
    print(len(out), "lines", dict(collections.Counter(o["why"] for o in out)), dict(collections.Counter(o["level"] for o in out)),
          "left out:", apart)


# ---------------------------------------------------------------------------------------------------- the figures

def tokens():
    out = {}
    for step, f in TOKENS.items():
        if f.exists():
            t = next(v for v in json.loads(f.read_text(encoding="utf-8")).values() if isinstance(v, dict))
            out[step] = {"agents": len(t), "tokens": sum(t.values())}
    return out | {"all": {"agents": sum(v["agents"] for v in out.values()), "tokens": sum(v["tokens"] for v in out.values())}}


def lot_letters(key, one, two):
    """The controls with letters drawn by lot: how each checker answered them, and the places where one of the
    two explained the letters (the entry of the word they were put on, on which side, the two answers)."""
    junk = [p for p in key if p["control"] == "junk"]
    said = [(p, one[p["place"]]["case"], two[p["place"]]["case"]) for p in junk]
    return {"shown": len(junk),
            "explained": {str(j): sum(c[j] != "unknown" for c in [(None, a, b) for _, a, b in said]) for j in (1, 2)},
            "explained_as": {str(j): dict(collections.Counter(c[j] for c in [(None, a, b) for _, a, b in said] if c[j] != "unknown")) for j in (1, 2)},
            "unknown_by_both": sum(a == b == "unknown" for _, a, b in said),
            "explained_at": [{"word": next(e for _, e in p["parts"] if e), "letters": "before" if p["front"] else "after", "answers": [a, b]}
                             for p, a, b in said if (a, b) != ("unknown", "unknown")]}


def name_kind(entry, v, lex):
    """What sort of name the source gives: a place name where the lexicon files the entry so; a personal name
    where both readers' lines say so; else a name."""
    if (lex.get(entry, {}).get("kind") or "") == "place name":
        return "a place name"
    return "a personal name" if all("personal name" in (v[k].get("meaning") or "") for k in ("one", "two")) else "a name"


def reading_of(home=None, again=False):
    """The figures of a reading of part 1 (of the second one with `again`; `home` is another folder to read)."""
    folder, _, bars_set = rule(again)[:3]
    home = home or folder
    key, res = read("key.json", home), read("result.json", home)
    one, two = answers(1, home), answers(2, home)
    real = [p for p in key if p["control"] is None]
    return {"places": len(real), "places_by_run": dict(collections.Counter(p["run"] for p in real).most_common()),
            "controls": dict(collections.Counter(p["control"] for p in key if p["control"])), "packs": len(read("groups.json", home)),
            "lines_expected": len(key), "answered": {"1": len(one), "2": len(two)},
            "answered_by_both": res["answered_by_both"], "kappa": res["kappa"], "bars_set": bars_set, "bars": res["bars"], "taken": res["taken"],
            "hidden_endings": {j: c["ending"] for j, c in res["controls"].items()}, "lot_letters": lot_letters(key, one, two),
            "verdicts": res["verdicts"], "verdicts_by_run": res["by_run"]}


def part_2():
    lex = W.lexicon()
    its, verified, res, lines, apart = build()
    R.here(RUN)
    checked = W.read("lit/checked.json")
    W.OUT = R.RECURRING
    firm = {k: sorted({s["source"] for s in checked[k]["statements"] if s["source"] in SOURCES and s["stance"] in W.FIRM}) for k in its}
    stated = {k: v for k, v in verified.items() if v["verdict"] == "stated"}
    known = set(D.population_of(M.current(), lex, fix=True)[0])                 # the dictionary words in use
    words = sorted(M.given(lines, known, lex))
    if set(words) != set(MEANINGS):
        raise SystemExit(f"MEANINGS and the words part 2 lays differ: {sorted(set(words) ^ set(MEANINGS))}")

    def gives(k, v):
        return "" if v["verdict"] != "stated" else MEANINGS.get(k) or (name_kind(k, v, lex) if v["what"] == "name" else "")
    return {"entries": len(its), "places": sum(it["uses"] for it in its.values()),
            "entries_by_source": dict(collections.Counter(s for v in firm.values() for s in v).most_common()),
            "read_twice": dict(collections.Counter(v["verdict"] for v in verified.values()).most_common()),
            "gives": dict(collections.Counter(v["what"] for v in stated.values()).most_common()),
            "names": dict(collections.Counter(name_kind(k, v, lex) for k, v in stated.items() if v["what"] == "name").most_common()),
            "by_entry": [{"entry": k, "kind": lex.get(k, {}).get("kind") or "", "source": v["one"]["source"] if v["verdict"] == "stated" else "", "verdict": v["verdict"],
                          "gives": v["what"] if v["verdict"] == "stated" else "", "meaning": gives(k, v)} for k, v in verified.items()],
            "the_places": R.summary(res),
            "laid": laid_of(lines),
            "left_out": apart,
            "words": [{"entry": k, "kind": lex[k].get("kind") or "", "meaning": MEANINGS[k], "source": verified[k]["one"]["source"],
                       "places_laid": sum(o["item"] == k and o["level"] in W.READ for o in lines),
                       "texts": len({o["text"] for o in lines if o["item"] == k and o["level"] in W.READ})} for k in words]}


def laid_of(lines):
    return {"lines": len(lines), "why": dict(collections.Counter(o["why"] for o in lines).most_common()),
            "to": dict(collections.Counter(o["level"] for o in lines).most_common()),
            "to_by_why": {w: dict(collections.Counter(o["level"] for o in lines if o["why"] == w).most_common())
                          for w in sorted({o["why"] for o in lines})},
            "was": dict(collections.Counter(o["was"] for o in lines).most_common())}


def part_1_again():
    """The second reading of part 1: the figures of the first, its own bars, what it lays and leaves out, and the
    words of the dictionary it is the first layer to give a meaning."""
    lex = W.lexicon()
    lines, apart, verified = build_again()
    known = set(D.population_of(M.current(), lex, fix=True)[0])                 # the dictionary words in use
    by_layer = M.given_by_layers([(l["name"], lines if l["name"] == LAYER_AGAIN else M.lines_of(l)) for l in M.LAYERS], known, lex)
    words = by_layer[LAYER_AGAIN]
    if set(words) != set(MEANINGS_AGAIN):
        raise SystemExit(f"MEANINGS_AGAIN and the words the second reading is the first to lay differ: {sorted(set(words) ^ set(MEANINGS_AGAIN))}")
    run_of = {o["item"]: ("g2" if o["why"] == "form" else "g4") for o in lines}
    f = reading_of(again=True)
    return f | {"laid": laid_of(lines) | {"by_run": dict(collections.Counter(run_of[o["item"]] for o in lines).most_common()),
                                           "entries": len({o["item"] for o in lines})},
                "left_out": apart, "not_laid": {"name": f["verdicts"].get("name", 0)},
                "words": [{"entry": k, "kind": lex[k].get("kind") or "", "meaning": MEANINGS_AGAIN[k], "source": verified[run_of[k]][k]["one"]["source"],
                           "places_laid": sum(o["item"] == k and o["level"] in W.READ for o in lines),
                           "texts": len({o["text"] for o in lines if o["item"] == k and o["level"] in W.READ})} for k in words]}


def figures():
    return {"part_1": reading_of(), "part_1_again": part_1_again(), "part_2": part_2(), "cost": tokens(),
            "when": [{k: w[k] for k in w if k != "answers"} for w in WHEN]}


def public():
    figs = figures()
    PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", PUBLIC.relative_to(ROOT), {k: figs["part_2"][k] for k in ("read_twice", "gives", "laid", "left_out")},
          {k: figs["part_1_again"][k] for k in ("bars", "verdicts", "laid", "left_out")})


COMMANDS = {"packs": packs, "count": count, "packs-again": lambda: packs(again=True), "count-again": lambda: count(again=True),
            "layer-again": layer_again, "setup": setup, "verify-packs": verify_packs, "verify": verify,
            "place-packs": place_packs, "places": places, "layer": layer, "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
