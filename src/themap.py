"""The map of corpus_v6 as it stands: the analysts' map with the layers that later studies have laid over it, and
the counts the status table reads from it (data/discovery/map_layers.md, .claude/skills/reporting/SKILL.md).

The base is data/sources/v6/analysts/glosses.jsonl (src/v6/readers.py count). A layer is a file of lines, one for
each running word it changes: the text, the word's number in it, its spelling, the new level and reading, why, and
the source. Layers are laid in the order of LAYERS. Nothing is written back to the base: the studies that were run
on it (the lexicon's statuses, the translations, the recurring open words, the sample behind the count of distinct
words) keep reading it and are not counted again. What is counted from now on reads current().

  python3 -I src/themap.py        the counts of the base, of each layer and of the map as it stands
                                  (writes data/discovery/map_figures.json; needs the local files)
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import lexicon as X                                    # noqa: E402
import recurring as W                                  # noqa: E402
import words as D                                      # noqa: E402

BASE = X.GLOSSES
PUBLIC = ROOT / "data/discovery/map_figures.json"
WORDS = ROOT / "data/discovery/distinct_words_figures.json"
# The layers, in the order they are laid: a name, the file of its lines (local), the page of the study it comes
# from, the day it was laid, and what it is in a few words.
LAYERS = [
    {"name": "recurring", "file": "data/sources/recurring/overlay.jsonl", "page": "data/discovery/recurring_words.md",
     "laid": "2026-11-16", "what": "the recurring open spellings, each place judged by two checkers"},
    {"name": "rare_sure", "file": "data/sources/rare/g2/overlay.jsonl", "page": "data/discovery/rare_spellings.md",
     "laid": "2026-11-16", "what": "rare spellings that are forms of a word the lexicon calls sure (G2)"},
    {"name": "rare_later", "file": "data/sources/rare/g4/overlay.jsonl", "page": "data/discovery/rare_spellings.md",
     "laid": "2026-11-16", "what": "rare spellings whose entry a later source gives a meaning (G4)"},
    {"name": "unnamed", "file": "data/sources/g3/overlay.jsonl", "page": "data/discovery/unnamed_spellings.md",
     "laid": "2026-11-16", "what": "open spellings the lexicon does not hold that two checkers call a name or a piece (G3)"},
]
WHY = ("stated", "form", "piece", "name")   # why a line changes a word: a later source states its meaning there; it
#                                             is a form of a word the lexicon calls sure; it is a piece of a word or
#                                             name the map holds; it is a name (by the sources, or, in the layer
#                                             `unnamed`, by its place in the text)
DRIFT = 0.02                           # the estimate of how many unnamed stems are words (src/words.py) rests on a
#                                        sample of the base's stems: it is carried while the layers take at most this
#                                        share of those stems out of the unnamed ones; past it the estimate is made
#                                        again from the sampled stems that are still unnamed (unnamed_words). A stem
#                                        the sample was not drawn from stops the count.


def base():
    return {r["id"]: r["glosses"] for r in map(json.loads, BASE.read_text(encoding="utf-8").splitlines())}


def lines_of(layer):
    return [json.loads(l) for l in (ROOT / layer["file"]).read_text(encoding="utf-8").splitlines() if l.strip()]


def lay(gl, lines, name):
    """A copy of the map with a layer's lines laid over it. A line must name a word that stands there with that
    spelling and the level the line says it had (the figures count what the layers moved from it), give a level
    the map knows and a reason of WHY, and no two lines may name one word, in this layer or in one laid before it:
    a layer that does not fit the map it is laid on stops the build."""
    out = {t: list(gs) for t, gs in gl.items()}
    seen = set()
    for o in lines:
        at = (o["text"], o["n"])
        gs = out.get(o["text"])
        if gs is None or not 1 <= o["n"] <= len(gs) or gs[o["n"] - 1]["form"] != o["form"]:
            raise SystemExit(f"layer {name}: no word {o['form']!r} at {at}")
        if at in seen:
            raise SystemExit(f"layer {name}: two lines for {at}")
        if "layer" in gs[o["n"] - 1]:
            raise SystemExit(f"layer {name}: {at} was changed by the layer {gs[o['n'] - 1]['layer']} already")
        if o.get("was") != gs[o["n"] - 1]["level"]:
            raise SystemExit(f"layer {name}: {at} has the level {gs[o['n'] - 1]['level']!r} in the map, the line says {o.get('was')!r}")
        if o["level"] not in W.READ + W.NAMED or o["why"] not in WHY:
            raise SystemExit(f"layer {name}: {at} has the level {o['level']!r} and the reason {o['why']!r}")
        seen.add(at)
        g = gs[o["n"] - 1]
        gs[o["n"] - 1] = g | {"level": o["level"], "gloss": o["gloss"], "source": o["source"], "by": f"layer: {name}",
                              "layer": name, "why": o["why"], "was": g["level"]}
    return out


def current(upto=None):
    """The map as it stands: the base with the layers laid over it (the first `upto` of them, all by default)."""
    gl = base()
    for layer in LAYERS[:upto]:
        gl = lay(gl, lines_of(layer), layer["name"])
    return gl


def counts(gl):
    """The running words and the spellings of a map by what they are, and the two shares the status table gives:
    of the words that need a meaning (no name, no numeral, no lost sign) those that have one. A spelling has the
    level it has most often (at a tie, the one it has first in the texts' order). `of_all` is the coverage page's
    wider measure: translated or named, of all words."""
    def group(level):
        return "translated" if level in W.READ else "named" if level in W.NAMED else "open" if level in W.OPEN else "lost"

    def tally(c):
        need = c["translated"] + c["open"]
        return {k: c[k] for k in ("translated", "named", "open", "lost")} | {"need": need, "share": round(c["translated"] / need, 4) if need else None}

    run, by_form = collections.Counter(), collections.defaultdict(collections.Counter)
    for gs in gl.values():
        for g in gs:
            run[group(g["level"])] += 1
            by_form[g["form"]][group(g["level"])] += 1
    spell = collections.Counter(c.most_common(1)[0][0] for c in by_form.values())
    every = sum(run.values())
    return {"running": tally(run) | {"all": every, "of_all": round((run["translated"] + run["named"]) / every, 4) if every else None},
            "spellings": tally(spell) | {"all": sum(spell.values())}}


def given(lines, known, lex):
    """The dictionary words in use (`known`, src/words.py: no name, no ending or particle) that a layer's lines give
    a meaning: a place laid as a translated word for the reason "stated", of an entry the lexicon of 2003 does not
    call established or probable."""
    return {o["item"] for o in lines if o["why"] == "stated" and o.get("level") in W.READ and o.get("item") in known
            and (lex[o["item"]].get("status") or "") not in W.SURE}


def given_by_layers(layers_lines, known, lex):
    """layer -> the words given(); a word counts for the first layer that gives it one."""
    out, taken = {}, set()
    for name, lines in layers_lines:
        out[name] = sorted(given(lines, known, lex) - taken)
        taken |= set(out[name])
    return out


def north_star(known, lex, layers_lines, unnamed):
    """Distinct words translated on the map as it stands: the dictionary words in use that the lexicon calls
    established or probable, and those a layer gives a meaning from a later source, over the dictionary words in
    use and the estimate of the unnamed stems that are words (src/words.py). Before the project it was the same:
    every one of these meanings is a scholar's."""
    by_lexicon = D.translated(known, lex)
    by_layer = given_by_layers(layers_lines, known, lex)
    done = len(by_lexicon) + sum(map(len, by_layer.values()))
    star = D.star(done, len(known), unnamed)
    return {"dictionary_words": len(known), "translated_by_the_lexicon": len(by_lexicon),
            "translated_by_a_layer": {k: len(v) for k, v in by_layer.items()}, "translated": done,
            "distinct_words": {k: len(known) + v for k, v in unnamed.items()}, "star": star, "before_us": star}


def unnamed_words(words, stems, sample, drawn):
    """(how many of the stems the map cannot name are words of their own, what the estimate rests on). `words` is
    the figures file of the count of distinct words, `stems` the stems unnamed on the map as it stands; `sample`
    gives that count's judged sample as {stem: verdict}, read only when it is needed, and `drawn` the stems that
    sample was drawn from.

    A stem the sample was not drawn from stops the count, however many stems the layers took out: the sample says
    nothing of it. While the layers have taken at most DRIFT of the sampled stems out of the unnamed ones, that
    count's estimate is carried. Past it the estimate is made again by that count's own rule (words.estimate) from
    the sampled stems that are still unnamed: they are a sample by lot of the stems still unnamed, because a stem
    leaves or stays by what it is, not by whether it was sampled."""
    sampled, now = words["unnamed_stems"], len(stems)
    new = sorted(set(stems) - set(drawn()))
    if new or now > sampled:
        raise SystemExit(f"the map has {now} unnamed stems, {len(new)} of them not among the {sampled} the estimate of the words among "
                         f"them was drawn from ({', '.join(new[:5])}): draw and judge a new sample (src/words.py) before the north star "
                         "is counted again")
    if sampled - now <= DRIFT * sampled:
        return words["unnamed_words"], {"sampled": sampled, "now": now}
    left = collections.Counter(v for stem, v in sample().items() if stem in stems)
    return D.estimate(now, left), {"sampled": sampled, "now": now, "sample_still_unnamed": sum(left.values()),
                                   "its_verdicts": dict(left.most_common())}


def the_sample():
    """{stem: verdict} of the sample behind the count of distinct words (its last reading; local)."""
    rows = json.loads((D.OUT / f"{D.ROUNDS[D.LAST]['folder']}result.json").read_text(encoding="utf-8"))["rows"]
    return {r["stem"]: r["verdict"] for r in rows}


def the_population():
    """The unnamed stems that sample was drawn from (its population.json; local)."""
    return set(json.loads((D.OUT / "population.json").read_text(encoding="utf-8"))["stems"])


def figures():
    """What the status table reads: the base, each layer and what it moved, the map as it stands, the plain lookup
    of the lexicon ("before us" for the running words and the spellings), and the north star, also as it stood
    once each layer was laid (a study's page quotes the map as it left it). Counts only."""
    lex, gl, laid = W.lexicon(), base(), []
    first = counts(gl)
    words, drawn = json.loads(WORDS.read_text(encoding="utf-8")), the_population()
    layers_lines = [(layer["name"], lines_of(layer)) for layer in LAYERS]
    for n, (layer, (name, lines)) in enumerate(zip(LAYERS, layers_lines), 1):
        gl = lay(gl, lines, name)
        known, stems, _ = D.population_of(gl, lex, fix=True)
        unnamed, rests_on = unnamed_words(words, stems, the_sample, lambda: drawn)
        star = north_star(known, lex, layers_lines[:n], unnamed) | {"unnamed_words": unnamed, "unnamed_stems": rests_on}
        laid.append({k: layer[k] for k in ("name", "page", "laid", "what")}
                    | {"places": len(lines), "why": dict(collections.Counter(o["why"] for o in lines).most_common()),
                       "to": dict(collections.Counter(o["level"] for o in lines).most_common()),
                       "was": dict(collections.Counter(o["was"] for o in lines).most_common()), "after": counts(gl),
                       "distinct_words_translated": star["translated"],
                       "north_star": {k: star[k] for k in ("translated", "distinct_words", "star", "unnamed_stems")}})
    if not laid:
        known, stems, _ = D.population_of(gl, lex, fix=True)
        unnamed, rests_on = unnamed_words(words, stems, the_sample, lambda: drawn)
        star = north_star(known, lex, [], unnamed) | {"unnamed_words": unnamed, "unnamed_stems": rests_on}
    return {"inscriptions": len(gl), "base": first, "layers": laid, "current": counts(gl), "lookup": counts(D.lookup_only()),
            "north_star": star}


def pct(x):
    return f"{100 * x:.1f}%"


def star_pct(n):
    """A north star's share and its range in percent, to one decimal, from its counts (`translated` over
    `distinct_words`). Its `star` is rounded to four places already, and rounding that again can put the tenth one
    too high: 156 of 1,284 is 12.1495%, stored as 0.1215."""
    t, d = n["translated"], n["distinct_words"]
    return {"point": pct(t / d["point"]), "low": pct(t / d["high"]), "high": pct(t / d["low"])}


def lines(figs):
    """The four lines the command prints; the reporting skill quotes them as they stand. Each share is divided
    from its counts and rounded once."""
    out = []
    for name, c in (("plain lookup", figs["lookup"]), ("base", figs["base"]), ("as it stands", figs["current"])):
        r, s = c["running"], c["spellings"]
        out.append(f"{name}: running words translated {r['translated']} of {r['need']} = {pct(r['translated'] / r['need'])}; "
                   f"distinct spellings translated {s['translated']} of {s['need']} = {pct(s['translated'] / s['need'])}")
    n, s = figs["north_star"], star_pct(figs["north_star"])
    return out + [f"north star: {n['translated']} of about {n['distinct_words']['point']} = {s['point']} ({s['low']} to {s['high']})"]


def main():
    figs = figures()
    PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("\n".join(lines(figs)))


if __name__ == "__main__":
    main()
