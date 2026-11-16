"""The open spellings that stand in one or two texts (data/discovery/rare_spellings.md), in two runs:

  g4   the entries the lexicon of 2003 holds without an accepted meaning: readers collect what the later sources
       state about each, two readers read the stated meanings in their place, and two checkers decide every place
       of the entries a later source speaks of or a reader calls a piece;
  g2   the spellings under a stem or an ending the lexicon calls established or probable: two checkers decide for
       every place whether it holds the lexicon's word.

Both reuse the steps of src/recurring.py in a folder of their own, data/sources/rare/<run>/ (local only: the packs
quote the lexicon and the editions). The rules and the bars are on the page, committed before the agents of each
step were started; what the agents were given is in runs/prompts/RARE_*.md.

  python3 -I src/rare.py g4 items | batches | quotes | verify-packs | verify | place-packs | places
  python3 -I src/rare.py g4 place-packs2 | places2    the second reading of the places, when the first is not taken
  python3 -I src/rare.py g2 items | place-packs | places
  python3 -I src/rare.py layers     the lines each run lays in the map (src/themap.py): g2's, then g4's
  python3 -I src/rare.py public     data/discovery/rare_spellings_figures.json

A command that writes packs refuses once an agent of its step has answered.
"""
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import coverage as C                                   # noqa: E402
import lexicon as X                                    # noqa: E402
import recurring as W                                  # noqa: E402
import words as D                                      # noqa: E402

HOME = ROOT / "data/sources/rare"
PUBLIC = ROOT / "data/discovery/rare_spellings_figures.json"
RECURRING = ROOT / "data/sources/recurring"            # the recurring open words' own folder (W.OUT, before here())
MOST_TEXTS = 2
KIND = {"g4": ("stem", "affix"), "g2": ("stem, sure in the lexicon", "affix, sure in the lexicon")}
LAYER = {"g2": "rare_sure", "g4": "rare_later"}       # the runs' layers in src/themap.py, in the order they are laid
BATCH = 12
LEADS = {"Rilly 2016": "data/sources/rilly2016-text/pages.txt", "Rilly 2021": "data/sources/dotawo-text/pages.txt"}
TOKENS = {"g4": {"literature": "tokens_g4_lit.json", "class A read twice": "tokens_g4_verify.json",
                 "places, first reading": "tokens_g4_places.json", "places, second reading": "tokens_g4_places2.json"},
          "g2": {"places": "tokens_g2_places.json"}}   # from the task notifications, typed by hand (local)


def here(run):
    """Point the steps of src/recurring.py at this run's folder."""
    W.OUT = HOME / run
    return W.OUT


def rel(run):
    return f"data/sources/rare/{run}"


# -------------------------------------------------------------------------------------------------- the items

def items_of(gl, rows, lex, hows):
    """As W.items_of, for the open spellings that stand in MOST_TEXTS texts at most and whose item is of one of
    the kinds `hows` (W.key_of's second value)."""
    level, texts, heads = W.spellings_of(gl)
    forms = sorted(f for f, c in level.items() if c.most_common(1)[0][0] in W.OPEN and len(texts[f]) <= MOST_TEXTS)
    items = collections.OrderedDict()
    for f in forms:
        hs = [h for h in heads[f].most_common(1)[0][0] if h not in X.PSEUDO]
        key, how = W.key_of(f, hs, lex)
        if how not in hows:
            continue
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
            span = gs[max(0, i - W.WIDTH): i + W.WIDTH + 1]
            items[k]["places"].append({
                "text": t, "site": rows[t].get("site") or "", "kind": rows[t].get("kind") or "", "n": i + 1, "of": len(gs),
                "form": g["form"], "gloss": (g.get("gloss") or "").strip(), "note": (g.get("evidence") or "")[:200],
                "words": " ".join(f"**{x['form']}**" if x is g else x["form"] for x in span),
                "readings": " · ".join(W.R.word_reading(x) for x in span)})
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
    out.sort(key=lambda it: ((it["lexicon"] or {}).get("kind") or "", it["item"]))
    return out


def answered(run, folders):
    done = [f for f in folders if any((HOME / run / f).glob("*.jsonl"))]
    if done:
        raise SystemExit(f"{', '.join(done)} hold answers: not written again")


def items(run):
    here(run)
    answered(run, ["lit/answers", "lit/verify/answers1", "lit/verify/answers2"] + [f"{f}/answers{c}" for f in FOLDER.values() for c in (1, 2)])
    out = items_of(W.the_map(), W.corpus_rows(), W.lexicon(), KIND[run])
    W.write("items.json", out)
    print(run, f"{sum(len(it['forms']) for it in out)} spellings in {len(out)} items; places {sum(it['uses'] for it in out)}",
          dict(collections.Counter(it["how"] for it in out)),
          dict(collections.Counter((it["lexicon"] or {}).get("kind") or "-" for it in out).most_common()))


# ------------------------------------------------------------------------------------------- G4, the literature

def plain(headword):
    """A headword as Rilly's later works write it: no homonym number, no hyphens, x for ḫ, h for ẖ, lower case."""
    return re.sub(r"\s*\(\d+\)$", "", headword).replace("-", "").replace("ḫ", "x").replace("ẖ", "h").lower()


def leads(headword, pages=None):
    """source -> the pages on which a script finds the headword as a word of its own (hyphens ignored); `pages`
    is {source: [(page, text)]}, the text layers of LEADS by default. A headword under three letters has none."""
    h = plain(headword)
    if len(h) < 3:
        return {}
    pat = re.compile(rf"(?<![a-zñšḫẖ]){re.escape(h)}(?![a-zñšḫẖ])")
    out = {}
    for name, path in LEADS.items():
        texts = pages[name] if pages is not None else W.pages_of(path)
        found = [n for n, text in texts if pat.search(text.lower()) or pat.search(text.lower().replace("-", ""))]
        if found:
            out[name] = found[:8]
    return out


def batches(run):
    here(run)
    answered(run, ["lit/answers"])
    its = W.the_items()
    keys = list(its)
    groups = {f"b{n + 1:02d}": keys[i: i + BATCH] for n, i in enumerate(range(0, len(keys), BATCH))}
    (W.OUT / "lit" / "packs").mkdir(parents=True, exist_ok=True)
    (W.OUT / "lit" / "answers").mkdir(exist_ok=True)
    found = 0
    for name, ks in groups.items():
        blocks = []
        for k in ks:
            ld = leads(k)
            found += bool(ld)
            line = "- Leads (pages on which a script finds this headword; read them, they may hold nothing): " + \
                ("; ".join(f"{s}, p. {', '.join(map(str, ps))}" for s, ps in ld.items()) if ld else "none found") + "\n"
            blocks.append(W.lit_block(its[k]) + line)
        (W.OUT / "lit" / "packs" / f"{name}.md").write_text(f"# Batch `{name}`: {len(ks)} items\n\n" + "\n".join(blocks), encoding="utf-8")
    W.write("lit/batches.json", groups)
    print(run, len(groups), "batches;", len(keys), "items;", found, "with a lead")


def quotes(run):
    here(run)
    W.BATCHES = W.read("lit/batches.json")
    W.quotes()


def verify_packs(run):
    here(run)
    answered(run, ["lit/verify/answers1", "lit/verify/answers2"])
    its, checked = W.the_items(), W.read("lit/checked.json")
    keys = W.class_a(its, W.read("lit/classes.json"))
    (W.OUT / "lit" / "verify" / "packs").mkdir(parents=True, exist_ok=True)
    groups = [keys[i: i + W.VERIFY_PACK] for i in range(0, len(keys), W.VERIFY_PACK)]
    for n, group in enumerate(groups, 1):
        body = "\n".join(W.verify_block(its[k], checked[k]) for k in group)
        for v in (1, 2):
            (W.OUT / "lit" / "verify" / f"answers{v}").mkdir(exist_ok=True)
            text = W.VERIFY_BRIEF.format(n=len(group), answers=f"{rel(run)}/lit/verify/answers{v}/A{n}.jsonl") + "\n---\n\n" + body
            (W.OUT / "lit" / "verify" / "packs" / f"A{n}_v{v}.md").write_text(text, encoding="utf-8")
    W.write("lit/verify/groups.json", groups)
    print(run, len(groups), "packs,", len(keys), "items of class A")


def verify(run):
    here(run)
    W.verify()


# --------------------------------------------------------------------------------------------------- the places

G2_BRIEF = W.PLACE_BRIEF.replace(
    """  - "stated": the spelling here is the word (or the ending) of which the later source named in the item's header
    speaks, in the use it describes. Only possible when the header has a line "A later source states". Put that
    meaning in "meaning".""",
    """  - "stated": the spelling here is a form of the word (or the ending) of the lexicon that the item's header names,
    in a use its meaning covers: that word with endings, in a variant writing, or in a compound. Put the
    lexicon's meaning, shortened to at most eight words of your own, in "meaning".""").replace(
    "holds no accepted meaning for the spellings below. Each\nstands in three texts or more. A first pass collected what the sources say about each item, with quotes that a\nscript has found in the files.",
    "holds no accepted meaning for the spellings below, although it files each under an\nentry of the lexicon of 2003 whose meaning that lexicon calls established or probable. Each stands in one or\ntwo texts.")
assert G2_BRIEF != W.PLACE_BRIEF and "three texts or more" not in G2_BRIEF and '"A later source states"' not in G2_BRIEF
G4_BRIEF = W.PLACE_BRIEF.replace("Each\nstands in three texts or more.", "Each\nstands in one or two texts.")
assert G4_BRIEF != W.PLACE_BRIEF

# The second reading of a place pass (the first is not taken when a place lacks one checker's answer or the kappa is
# under the bar): the same packs for fresh checkers, with the brief's last line corrected to name the count of lines.
REPLY = "When the file is written, reply in one line: how many places, and how many of each case."
COUNTED = ("This pack lists {places} places: your file must have {places} lines, one for each place, none left out. When the "
           "file is written, count its lines against that number, then reply in one line: how many places, and how many of "
           "each case.")
assert REPLY in G2_BRIEF and REPLY in G4_BRIEF
FOLDER = {1: "places", 2: "places2"}


def place_items(run):
    """The items whose places are judged: for g4 those of class A or B; for g2 all of them, each with the lexicon's
    own entry in the place of a later statement."""
    its = W.the_items()
    if run == "g2":
        checked = {k: {"statements": [], "state": "", "piece": ""} for k in its}
        verified = {k: {"verdict": "stated", "uses": it["uses"],
                        "one": {"meaning": it["lexicon"]["meaning"], "source": "the lexicon of 2003", "page": it["lexicon"]["page"],
                                "stance": it["lexicon"]["status"], "note": "none"},
                        "two": {"stance": it["lexicon"]["status"], "note": "none"}} for k, it in its.items()}
        classes = {k: W.CLASSES["A"] for k in its}
        return its, checked, classes, verified
    checked, classes, verified = W.read("lit/checked.json"), W.read("lit/classes.json"), W.read("lit/verify/result.json")
    return {k: it for k, it in its.items() if classes[k][0] in "AB"}, checked, classes, verified


def place_packs(run, rnd=1):
    here(run)
    folder = FOLDER[rnd]
    answered(run, [f"{folder}/answers1", f"{folder}/answers2"])
    its, checked, _, verified = place_items(run)
    brief = G2_BRIEF if run == "g2" else G4_BRIEF
    (W.OUT / folder / "packs").mkdir(parents=True, exist_ok=True)
    groups = W.place_groups(its)
    for n, group in enumerate(groups, 1):
        body = "\n".join(W.place_header(its[k], checked[k], verified.get(k)) + W.place_lines(its[k], lo, hi) for k, lo, hi in group)
        if run == "g2":
            body = body.replace("A later source states (the lexicon of 2003,", "The lexicon's own entry, which it calls sure (the lexicon of 2003,")
        for c in (1, 2):
            (W.OUT / folder / f"answers{c}").mkdir(exist_ok=True)
            text = brief.format(n=len({k for k, _, _ in group}), answers=f"{rel(run)}/{folder}/answers{c}/P{n:02d}.jsonl")
            if rnd == 2:
                text = text.replace(REPLY, COUNTED.format(places=sum(hi - lo for _, lo, hi in group)))
            (W.OUT / folder / "packs" / f"P{n:02d}_c{c}.md").write_text(text + "\n---\n\n" + body, encoding="utf-8")
    W.write(f"{folder}/groups.json", groups)
    print(run, folder, len(groups), "packs,", len(its), "items,", sum(hi - lo for g in groups for _, lo, hi in g), "places")


def places(run, rnd=1):
    here(run)
    folder = FOLDER[rnd]
    its, _, classes, verified = place_items(run)
    groups = W.read(f"{folder}/groups.json")
    rows, pairs = W.place_rows(its, classes, verified, W.place_answers(W.OUT / folder / "answers1", groups),
                               W.place_answers(W.OUT / folder / "answers2", groups))
    out = W.place_summary(rows, pairs) | {"rows": rows}
    W.write(f"{folder}/result.json", out)
    print(run, folder, {k: v for k, v in out.items() if k != "rows"})


def readings(run):
    """{reading: its result}, for the readings of the run's places that were counted, in their order."""
    out = {}
    for rnd, folder in FOLDER.items():
        f = HOME / run / folder / "result.json"
        if f.exists():
            out[rnd] = json.loads(f.read_text(encoding="utf-8"))
    return out


def taken(run):
    """The reading of the run's places that counts: the first one that met its bar. A later reading is made only
    when every one before it missed."""
    for rnd, res in readings(run).items():
        if res["taken"]:
            return rnd, res
    raise SystemExit(f"{run}: no reading of the places met its bar: nothing is taken")


# ----------------------------------------------------------------------------------------- what is laid in the map

def named(g):
    """Whether the map names every part of the word with an entry of the lexicon."""
    parts = g.get("parts") or []
    return bool(parts) and all(p.get("entry") is not None and p.get("entry") not in X.PSEUDO for p in parts)


def unsettled(g, lex, stated):
    """The stems among the word's parts that have no meaning: the lexicon does not call them established or
    probable, no later source states them (`stated`, the entries that passed the bar of class A), and they are no
    names. An ending the lexicon is not sure of does not count."""
    out = []
    for p in g.get("parts") or []:
        e = p.get("entry")
        if e is None or e in X.PSEUDO or W.affix(e):
            continue
        entry = lex.get(e) or {}
        if (entry.get("status") or "") in W.SURE or (entry.get("kind") or "") in C.NAME_KINDS or e in stated:
            continue
        out.append(e)
    return out


def level_of(item, lex):
    """The level a stated place takes: a name where the entry is one by the lexicon, a grammar word where it is an
    ending or a particle, else a meaning."""
    kind = (lex.get(item) or {}).get("kind") or ""
    return "name" if kind in C.NAME_KINDS else "grammar" if W.affix(item) and kind in ("function word", "") else "meaning"


def stated_entries(*results):
    """The entries a later source states: those that passed the bar of class A in any of the results given."""
    return {k for res in results for k, v in res.items() if v["verdict"] == "stated"}


def lines_of(run, gl, its, rows, verified, lex, stated):
    """(the lines the run lays in the map, the places it leaves out and why). gl is the map with the layers laid
    before this one. A stated place is laid only where the map names every part of the spelling and every stem
    among them has a meaning; a piece only where the whole word both checkers name is translated or named in gl."""
    level, gloss = W.form_levels(gl)
    out, apart = [], collections.Counter()
    for r in rows:
        p = its[r["item"]]["places"][r["place"] - 1]
        g = gl[p["text"]][p["n"] - 1]
        if g["form"] != p["form"]:
            raise SystemExit(f"{run}: the map has {g['form']!r} at {(p['text'], p['n'])}, the item {p['form']!r}")
        base = {"text": p["text"], "n": p["n"], "form": p["form"], "item": r["item"], "was": g["level"]}
        what = "ending" if its[r["item"]]["how"].startswith("affix") else "stem"
        if r["verdict"] == "stated":
            if not named(g):
                apart[f"stated, {what}, a part of the spelling unnamed"] += 1
            elif unsettled(g, lex, stated):
                apart[f"stated, {what}, another stem without a meaning"] += 1
            else:
                v = verified[r["item"]]["one"]
                out.append(base | {"level": level_of(r["item"], lex), "gloss": v["meaning"], "why": "form" if run == "g2" else "stated",
                                   "source": f"{v['source']}, p. {v['page']}"})
        elif r["verdict"] == "piece":
            lv = level[r["whole"]].most_common(1)[0][0] if r["whole"] in level else None
            if lv in W.READ + W.NAMED:
                out.append(base | {"level": lv, "gloss": f"part of {r['whole']}: {gloss[r['whole']]}", "why": "piece",
                                   "source": "the map's reading of the whole word"})
            else:
                apart["piece, the whole word " + ("open in the map" if lv in W.OPEN else "not a form of the map")] += 1
    return out, dict(apart)


def by_kind(run, gl, its, rows, lex, stated):
    """The stated places by what their entry is and how the map cuts the spelling: the figure by the rule of the
    place pass, split as the rule for the map needs it."""
    c = collections.Counter()
    for r in rows:
        if r["verdict"] != "stated":
            continue
        p = its[r["item"]]["places"][r["place"] - 1]
        g = gl[p["text"]][p["n"] - 1]
        what = "ending" if its[r["item"]]["how"].startswith("affix") else "stem"
        c[f"{what}, " + ("a part unnamed" if not named(g) else "another stem without a meaning" if unsettled(g, lex, stated)
                         else "every part named")] += 1
    return dict(sorted(c.items()))


def build(run, gl, lex, stated):
    here(run)
    its, _, _, verified = place_items(run)
    rnd, res = taken(run)
    lines, apart = lines_of(run, gl, its, res["rows"], verified, lex, stated)
    return its, res, lines, apart


def layers():
    """Write each run's lines for the map: g2's on the map with the layers before it, then g4's on the map with
    g2's laid too (src/themap.py lays them in that order)."""
    import themap as M
    lex = W.lexicon()
    stated = stated_entries(json.loads((RECURRING / "lit/verify/result.json").read_text(encoding="utf-8")),
                            json.loads((HOME / "g4/lit/verify/result.json").read_text(encoding="utf-8")))
    names = [l["name"] for l in M.LAYERS]
    for run in LAYER:                                   # g2, then g4
        gl = M.current(upto=names.index(LAYER[run]))
        _, _, lines, apart = build(run, gl, lex, stated)
        (HOME / run / "overlay.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in lines), encoding="utf-8")
        print(run, len(lines), "lines", dict(collections.Counter(o["why"] for o in lines)),
              dict(collections.Counter(o["level"] for o in lines)), "left out:", apart)


# ---------------------------------------------------------------------------------------------------- the figures

def summary(res):
    return {k: res[k] for k in ("places", "answered by both", "kappa", "bar", "taken", "verdicts", "by class")}


# The meanings a later source gives the words of the dictionary that G4 lays, in a few words of our own (the two
# readers' wordings follow their source and stay local). The check of tests/test_rare.py holds each to the rule of
# src/lexicon.py: no four words in a row of the lexicon of 2003 or of Rilly 2016 and 2021, eight words at most.
MEANINGS = {
    "Aqedise": "the Moon-god", "abrse": "each man", "anese": "donkey", "aqebese": "their, a variant spelling",
    "asr": "meat, animal", "bqo": "to take control", "erk": "I took", "kb": "to seize", "kdke": "Candace, the queen-mother",
    "mreke": "horse", "pl (2)": "to give, offer", "plete": "to give, offer", "pqr": "prince", "pso": "causative prefix before 'drink'",
    "pẖo": "causative prefix before 'present'", "sr": "meat, animal", "tk (1)": "to seize", "tk (3)": "to seize",
    "tlt": "talent, a weight", "tḫ (1)": "to present a meal", "wese": "his, her", "yel": "to give", "yerki": "I took",
    "ḫr": "to eat", "ẖol": "to present, serve",
}


def dictionary_words(lines, lex):
    """The entries a run's lines give a meaning as a translated word that are words of the dictionary (no name, no
    ending or particle) and that the lexicon does not call sure."""
    laid = {o["item"] for o in lines if o["why"] == "stated" and o["level"] in W.READ}
    return sorted(k for k in laid if (lex[k].get("kind") or "") not in C.NAME_KINDS and not W.affix(k)
                  and (lex[k].get("status") or "") not in W.SURE)


def entries_of(its, lines, rows, lex):
    """The run's entries by what its places gave: with a stated place; with one laid as a translated word; with
    one laid, but only as a name; with none laid; and the words of the dictionary given a meaning."""
    with_stated = {r["item"] for r in rows if r["verdict"] == "stated"}
    mine = [o for o in lines if o["why"] in ("stated", "form")]
    translated = {o["item"] for o in mine if o["level"] in W.READ}
    names = {o["item"] for o in mine} - translated
    return {"with_a_stated_place": len(with_stated), "laid_as_a_translated_word": len(translated), "laid_as_a_name_only": len(names),
            "none_laid": len(with_stated - translated - names), "dictionary_words_given_a_meaning": len(dictionary_words(lines, lex))}


def tokens(run):
    out = {}
    for step, name in TOKENS[run].items():
        f = HOME / name
        if f.exists():
            t = json.loads(f.read_text(encoding="utf-8"))
            out[step] = {"agents": len(t), "tokens": sum(t.values())}
    return out


def figures():
    import themap as M
    lex = W.lexicon()
    stated = stated_entries(json.loads((RECURRING / "lit/verify/result.json").read_text(encoding="utf-8")),
                            json.loads((HOME / "g4/lit/verify/result.json").read_text(encoding="utf-8")))
    names = [l["name"] for l in M.LAYERS]
    figs = {}
    for run in LAYER:
        gl = M.current(upto=names.index(LAYER[run]))
        its, res, lines, apart = build(run, gl, lex, stated)
        every = W.the_items()
        f = {"entries": len(every), "spellings": sum(len(it["forms"]) for it in every.values()), "places": sum(it["uses"] for it in every.values()),
             "entries_that_are": dict(collections.Counter("an ending or a particle" if it["how"].startswith("affix") else "a stem"
                                                          for it in every.values()).most_common()),
             "places_judged": {"entries": len(its), "places": sum(it["uses"] for it in its.values())},
             "readings": {str(rnd): summary(r) for rnd, r in readings(run).items()}, "reading_taken": taken(run)[0],
             "stated": by_kind(run, gl, its, res["rows"], lex, stated),
             "laid": {"lines": len(lines), "why": dict(collections.Counter(o["why"] for o in lines).most_common()),
                      "to": dict(collections.Counter(o["level"] for o in lines).most_common()),
                      "to_by_why": {w: dict(collections.Counter(o["level"] for o in lines if o["why"] == w).most_common())
                                    for w in sorted({o["why"] for o in lines})},
                      "was": dict(collections.Counter(o["was"] for o in lines).most_common())},
             "left_out": apart, "the_entries": entries_of(its, lines, res["rows"], lex), "cost": tokens(run)}
        if run == "g4":
            counts, classes, ver = W.read("lit/counts.json"), W.read("lit/classes.json"), W.read("lit/verify/result.json")
            f["literature"] = counts | {"classes": dict(sorted(collections.Counter(c[0] for c in classes.values()).items()))}
            f["class_a"] = {"entries": len(ver), "verdicts": dict(collections.Counter(v["verdict"] for v in ver.values()).most_common()),
                            "stated_by": dict(collections.Counter(v["one"]["source"] for v in ver.values() if v["verdict"] == "stated").most_common()),
                            "stated_that_are": dict(collections.Counter("an ending or a particle" if every[k]["how"].startswith("affix") else "a stem"
                                                                        for k, v in ver.items() if v["verdict"] == "stated").most_common())}
            words = dictionary_words(lines, lex)
            missing = sorted(set(words) ^ set(MEANINGS))
            if missing:
                raise SystemExit(f"MEANINGS and the words G4 lays differ: {missing}")
            known = set(D.population_of(M.current(), lex, fix=True)[0])
            new = set(M.given_by_layers([(l["name"], M.lines_of(l)) for l in M.LAYERS], known, lex)[LAYER[run]])
            f["words"] = [{"entry": k, "kind": lex[k].get("kind") or "", "meaning": MEANINGS[k], "source": ver[k]["one"]["source"],
                           "page": ver[k]["one"]["page"], "places_laid": sum(o["item"] == k and o["why"] == "stated" for o in lines),
                           "new_to_the_map": k in new} for k in words]
        figs[run] = f
    return figs


def public():
    figs = figures()
    PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({run: {k: f[k] for k in ("stated", "laid", "left_out", "the_entries")} for run, f in figs.items()}, ensure_ascii=False))


COMMANDS = {"items": items, "batches": batches, "quotes": quotes, "verify-packs": verify_packs, "verify": verify,
            "place-packs": place_packs, "places": places,
            "place-packs2": lambda run: place_packs(run, 2), "places2": lambda run: places(run, 2)}
ALL = {"layers": layers, "public": public}

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ALL:
        ALL[sys.argv[1]]()
    elif len(sys.argv) == 3 and sys.argv[1] in KIND and sys.argv[2] in COMMANDS and (sys.argv[1] == "g4" or sys.argv[2] in ("items", "place-packs", "places", "place-packs2", "places2")):
        COMMANDS[sys.argv[2]](sys.argv[1])
    else:
        raise SystemExit(__doc__)
