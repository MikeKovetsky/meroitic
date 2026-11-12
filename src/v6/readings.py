"""Every reading of a Meroitic inscription that the project holds, and the rule that says when two are one text.

A reading is one edition's text of one inscription: a row of the Griffith or Karanog transcriptions (public), a
text typed from the Meroitic Newsletter, an entry of Millet 2005 or of FHN III (text layers, in copyright), one
of Otten's three narrative files, or a source line of his per-scholar files (src/v6/otten.py). Each carries the
numbers its edition gives it (REM, Griffith's, Millet's GA number), its licence, and its letters in one reduced
spelling (src/experts/prepare.py), in which runs of five letters are compared.

The rule (set before it was scored, data/discovery/corpus_v6.md): two texts are a sure match when 60% or more of
the own runs of one stand in the other and they share at least 12 own runs; a doubtful one from 30%, or above
60% with fewer than 12 shared; below 30% none. Own runs are runs of five letters that fewer than 8 edition texts
hold (the rest is formula). One thing was added after the first build and before any reader ran: a doubtful
match needs 6 shared own runs (FLOOR), because one or two shared runs are one shared word, and an edition text of
ten letters made every long line "doubtful".

  python3 -I src/v6/readings.py            what is held, by source
  python3 -I src/v6/readings.py test       the rule on the pairs that are already known (bars A and B)
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(Path(__file__).resolve().parent)]
import expand as E     # noqa: E402
import otten as O      # noqa: E402
import prepare as P    # noqa: E402

MNL = ROOT / "data/sources/mnl/mnl_texts.jsonl"
V5 = ROOT / "data/corpus_v5.jsonl"
RUN = P.RUN
COMMON = 8          # a run that this many edition texts hold is formula
SURE, DOUBT, SHARED = 0.6, 0.3, 12
FLOOR = 6           # own runs two texts must share to be a doubtful match (added after the first build)
PD = "public domain (the edition); the row CC BY 4.0"
LICENCES = {
    "griffith": PD, "karanog": PD,
    "mnl": "in copyright (Meroitic Newsletter)",
    "millet2005": "in copyright (JSSEA 32)",
    "fhn": "in copyright (Fontes Historiae Nubiorum III)",
    "otten": "no licence stated (Otten's repository); the reading is Millet's or the edition's, in copyright",
}
OPEN = ("griffith", "karanog")
TYPED = ("griffith", "karanog", "mnl", "otten")       # the two text layers are witnesses, not typed readings
VOLUME = {"mi1a": "Inscr.", "mi1b": "Inscr.", "mi2a": "Inscr.", "mi2b": "Inscr.", "meroe": "Meroe", "karanog": "Kar."}


def runs(letters, n=RUN):
    return {letters[i:i + n] for i in range(len(letters) - n + 1)}


def reduced(text):
    """A text in the corpus spelling as bare letters (prepare.reduced_ours): masked names and numerals drop out."""
    return P.reduced_ours(text.split())


def rem_of(value):
    """A REM number as the tables write it: four digits and what follows them ("0091a", "1041A", "1254B-8")."""
    m = re.match(r"\s*(\d{4})(.*)$", str(value or ""))
    return (m.group(1) + m.group(2).strip()) if m else ""


def griffith_rows(folder, family):
    out = []
    for p in sorted((ROOT / folder).glob("griffith_*.jsonl")):
        part = p.stem.split("_", 1)[1]
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            ws = E.words(r.get("text_corpus", ""))
            if not ws:
                continue
            letter = re.sub(r"^\d*", "", str(r.get("rem") or ""))
            no = str(r.get("griffith_no"))
            vid = f"G-{part}-{no}{letter}"
            shablul = no.startswith("Sh")
            numbers = {"rem": [rem_of(r["rem"])]} if rem_of(r.get("rem")) else {}
            numbers["shablul" if shablul else part if part in ("meroe", "karanog") else "griffith"] = \
                [(no[2:] if shablul else no) + letter]
            partial = (r.get("notes") or "").lstrip().lower().startswith("partial") \
                or r.get("griffith_no") in E.PARTIAL.get(part, ())
            out.append({"key": f"{family}:{vid}", "family": family, "work": r["source"], "ref": r.get("page", ""),
                        "number": ("Sh. " + no[2:] if shablul else f"{VOLUME[part]} {no}{letter}"),
                        "numbers": numbers, "site": r.get("site", ""), "object": r.get("object", ""),
                        "text": " ".join(ws), "whole": not partial, "v5": vid})
    return out


def mnl_rows(path=MNL):
    out = []
    for line in path.read_text().splitlines():
        r = json.loads(line)
        numbers = {"rem": [rem_of(r["rem"])]} if rem_of(r["rem"]) else {}
        ga = re.match(r"GA (\d+)", r["id"])
        if ga:
            numbers["ga"] = [f"{int(ga.group(1)):02d}"]
        if not numbers:
            numbers["mnl"] = [r["id"] or f"{r['file']} p. {r['printed_page']}"]
        out.append({"key": f"mnl:{r['id'] or 'unnumbered'}|{r['file']}", "family": "mnl", "work": r["source"],
                    "ref": f"p. {r['printed_page']}", "number": r["id"], "numbers": numbers, "site": r["site"],
                    "object": r["object"], "text": " ".join(E.words(r["text_corpus"])),
                    "whole": r["complete"] == "whole", "printout": r["kind"] == "printout",
                    "reconstruction": "reconstruction" in r["id"].lower(), "same_as": r["same_as"],
                    # an older reading of a text that a later issue edits again in several numbered pieces
                    "superseded": " and the rest of that edition" in r["same_as"],
                    "mnl_id": r["id"], "mnl_file": r["file"]})
    return out


def millet_rows():
    """One reading for each set of numbers under which the article prints a text ("GA13&GA16" is one text of two
    fitting fragments; GA55 and GA56 have a text each under one heading)."""
    letters, head = collections.defaultdict(str), {}
    for name, block in P.millet_entries():
        s = P.millet_letters(block)
        if s:
            letters[name] += s
        head.setdefault(name, " ".join(block.split("\n")[:2])[:160])
    out = []
    for name, s in letters.items():
        nums = sorted(n[2:] for n in P.numbers(name))
        out.append({"key": f"millet2005:{name}", "family": "millet2005",
                    "work": "Millet 2005, The Meroitic Inscriptions from Gebel Adda (JSSEA 32)", "ref": name,
                    "number": name.replace("&", " + "), "numbers": {"ga": nums}, "site": "Gebel Adda",
                    "object": "", "text": None, "letters": s, "whole": None})
    return out


def fhn_rows():
    out = []
    for number, block in P.fhn_entries():
        s = P.fhn_letters(block)
        head = block.split("Introduction to source")[0]
        rems = list(dict.fromkeys(re.findall(r"REM\s+(\d{4}[A-Za-z]?)", head)))
        if not s:
            continue
        site = block.split("\n")[0].split(".")[0].replace(number, "", 1).strip()
        out.append({"key": f"fhn:{number}", "family": "fhn", "work": "Fontes Historiae Nubiorum III (1998)",
                    "ref": f"no. {number}", "number": f"FHN {number}", "numbers": {"fhn": [number], "rem": rems},
                    "site": site, "object": "", "text": None, "letters": s, "whole": None})
    return out


def narrative_rows():
    out = []
    for vid, fn in O.NARRATIVES.items():
        body = [l for l in (O.DATA / fn).read_text().split("\n") if l.strip() and not l.startswith("#")]
        out.append({"key": f"otten:narrative:{vid}", "family": "otten", "work": f"Otten's file {fn}", "ref": fn,
                    "number": "", "numbers": {}, "site": "", "object": "", "text": O.to_corpus(" ".join(body)),
                    "whole": True, "v5": vid, "narrative": True})
    return out


def otten_rows(lines=None):
    """A reading for each source line of the per-scholar files, in the spelling of corpus_v6."""
    out = []
    for l in lines if lines is not None else O.source_lines():
        text = O.to_corpus(l["mero"], rilly=l["file"] == "RillyExamples.txt")
        out.append({"key": f"otten:{l['key']}", "family": "otten", "work": O.WORKS[l["file"]],
                    "ref": (f"p. {l['page']}; " if l["page"] else "") + f"{l['file']} line {l['line']}",
                    "number": "", "numbers": {}, "site": "", "object": "", "text": text, "whole": None,
                    "line": l})
    return out


def finish(r):
    r.setdefault("letters", reduced(r["text"]) if r.get("text") is not None else "")
    r["licence"] = LICENCES[r["family"]]
    r["open"] = r["family"] in OPEN
    r["typed"] = r["family"] in TYPED
    return r


def load(lines=None):
    """(the edition readings, the narratives, the source lines), each a list of readings."""
    editions = (griffith_rows("data/expansion", "griffith") + griffith_rows("data/expansion/karanog", "karanog")
                + mnl_rows() + millet_rows() + fhn_rows())
    return ([finish(r) for r in editions], [finish(r) for r in narrative_rows()],
            [finish(r) for r in otten_rows(lines)])


def formulae(editions, common=COMMON):
    """The runs that `common` or more of the edition texts hold."""
    held = collections.Counter(g for r in editions for g in runs(r["letters"]))
    return {g for g, n in held.items() if n >= common}


def rule(a, b, skip=frozenset(), floor=FLOOR):
    """(verdict, share of a's own runs in b, share of b's own runs in a, own runs shared) for two letter strings:
    "sure", "doubtful" or "" (no match). floor=1 gives the rule as first written, without the floor."""
    ra, rb = runs(a) - skip, runs(b) - skip
    if not ra or not rb:
        return "", 0.0, 0.0, 0
    n = len(ra & rb)
    sa, sb = n / len(ra), n / len(rb)
    m = max(sa, sb)
    verdict = "sure" if m >= SURE and n >= SHARED else "doubtful" if m >= DOUBT and n >= floor else ""
    return verdict, round(sa, 3), round(sb, 3), n


def matches(x, pool, skip=frozenset(), top=3, floor=FLOOR):
    """The readings of pool that x matches, the best first: [(verdict, share of x, share of the other, shared,
    key)]. The best is the one with the larger of the two shares, then the more runs shared."""
    out = []
    for r in pool:
        if r["key"] == x["key"]:
            continue
        v, sa, sb, n = rule(x["letters"], r["letters"], skip, floor)
        if v:
            out.append((v, sa, sb, n, r["key"]))
    out.sort(key=lambda m: (-max(m[1], m[2]), -m[3], m[4]))
    return out[:top] if top else out


def stands_in(x, pool, least=6):
    """The readings of pool whose letters hold all of x's letters in one stretch (x of `least` letters or more)."""
    s = x["letters"]
    return [r["key"] for r in pool if len(s) >= least and r["key"] != x["key"] and s in r["letters"]]


# ------------------------------------------------------------------------------- the pairs already known

def known_pairs(editions, narratives, lines, v5_sources):
    """[(what, key of one text, key of its known partner)]: the 31 pairs of prepare.HELD (a corpus_v5 text stands
    for its source line), the three Karanog texts that Newsletter 28 and FHN print, the Newsletter rows that
    src/mnl/mnl_dedupe.py found in the corpus, and its second editions. v5_sources: {text id: source key}."""
    by_v5 = {r["v5"]: r["key"] for r in editions + narratives if r.get("v5")}
    by_mnl = collections.defaultdict(list)
    for r in editions:
        if r["family"] == "mnl":
            by_mnl[r["mnl_id"]].append(r)
    ours = lambda tid: by_v5.get(tid) or (f"otten:{v5_sources[tid]}" if tid in v5_sources else None)
    out = []
    for source, table in P.HELD.items():
        for entry, tid in table.items():
            key = f"millet2005:{entry}" if source == "millet" else f"fhn:{entry}"
            out.append((f"HELD {source}", ours(tid), key))
    for kar, rem in (("47", "0247"), ("77", "0277"), ("78", "0278")):
        mnl = next(r["key"] for r in editions if r["family"] == "mnl" and r["numbers"].get("rem") == [rem])
        fhn = next(r["key"] for r in editions if r["family"] == "fhn" and rem in r["numbers"].get("rem", ()))
        out.append(("Karanog in Newsletter 28", f"karanog:G-karanog-{kar}", mnl))
        out.append(("Newsletter 28 in FHN", mnl, fhn))
    for r in editions:
        if r["family"] != "mnl":
            continue
        row = json.loads(next(l for l in MNL.read_text().splitlines()
                              if json.loads(l)["id"] == r["mnl_id"] and json.loads(l)["file"] == r["mnl_file"]))
        hit = row["in_corpus"].split(" (as ")[0]
        if hit and " (as " not in row["in_corpus"]:
            m = re.match(r"Millet's examples, line (\d+)", hit)
            other = f"otten:MilletExamples.txt:{m.group(1)}" if m else ours(hit)
            out.append(("Newsletter row in the corpus", r["key"], other))
        if row["same_as"]:
            name = row["same_as"].split(" and the rest of that edition")[0]
            name = re.sub(r" \(Meroitic Newsletter \d+ \(\d{4}\)\)$", "", name)
            kept = [o for o in by_mnl.get(name, []) if o["key"] != r["key"]]
            if kept:
                out.append(("Newsletter second edition", r["key"], kept[0]["key"]))
    return [p for p in out if p[1] and p[2]]


def score_known(pairs, everything, skip, floor=FLOOR):
    """For each known pair: the verdict of the rule on it, whether the partner is the best match of the first text
    among the texts of the partner's family, and the sure matches to other texts of that family. same_text: the
    best match, when it is not the partner, is a text that the rule itself takes for the partner's (a sure match
    between the two): Otten's files give one text on several lines."""
    by_key = {r["key"]: r for r in everything}
    family = collections.defaultdict(list)
    for r in everything:
        family[r["family"]].append(r)
    same = lambda k, b: k == b or rule(by_key[k]["letters"], by_key[b]["letters"], skip, floor)[0] == "sure"
    out = []
    for what, a, b in pairs:
        x, y = by_key[a], by_key[b]
        v, sa, sb, n = rule(x["letters"], y["letters"], skip, floor)
        found = matches(x, family[y["family"]], skip, top=0, floor=floor)
        best = found[0][4] if found else ""
        wrong = [m[4] for m in found if m[0] == "sure" and m[4] != b]
        out.append({"what": what, "a": a, "b": b, "verdict": v, "share_a": sa, "share_b": sb, "shared": n,
                    "best": best == b, "best_key": best, "same_text": bool(best) and same(best, b),
                    "sure_others": wrong, "sure_others_not_same_text": [k for k in wrong if not same(k, b)]})
    return out


def bars(editions, narratives, lines, first):
    """The figures of bars A and B: as the bar was written (no floor) and with the floor."""
    skip = formulae(editions)
    pairs = known_pairs(editions, narratives, lines, first)
    out = {"pairs": len(pairs), "by_kind": dict(collections.Counter(p[0] for p in pairs))}
    for name, floor in (("as_written", 1), ("with_the_floor", FLOOR)):
        scored = score_known(pairs, editions + narratives + lines, skip, floor)
        ok = [s for s in scored if s["verdict"] and s["best"]]
        ok2 = [s for s in scored if s["verdict"] and (s["best"] or s["same_text"])]
        out[name] = {"right": len(ok), "sure": sum(s["verdict"] == "sure" for s in ok),
                     "doubtful": sum(s["verdict"] == "doubtful" for s in ok),
                     "right_or_another_line_of_the_same_text": len(ok2),
                     "with_a_sure_other": sum(bool(s["sure_others"]) for s in scored),
                     "with_a_sure_other_of_another_text": sum(bool(s["sure_others_not_same_text"]) for s in scored),
                     "missed": [{k: s[k] for k in ("what", "a", "b", "verdict", "shared", "best_key")}
                                for s in scored if not (s["verdict"] and (s["best"] or s["same_text"]))],
                     "scored": scored}
    kar = [r for r in editions if r["family"] == "karanog"]
    twins = {r["key"]: [m for m in matches(r, kar, skip, top=0) if m[0] == "sure"] for r in kar}
    out["karanog"] = {"texts": len(kar), "with_a_sure_match_to_another_number": sum(bool(v) for v in twins.values()),
                      "pairs": sorted({tuple(sorted((k, m[4]))) for k, v in twins.items() for m in v})}
    return out


def main(argv):
    editions, narratives, lines = load()
    if argv[1:] == []:
        n = collections.Counter(r["family"] for r in editions)
        print("edition readings:", dict(n), "| narratives:", len(narratives), "| source lines:", len(lines))
        print("with a REM number:", dict(collections.Counter(r["family"] for r in editions if r["numbers"].get("rem"))))
        print("formula runs:", len(formulae(editions)))
        return
    if argv[1:] == ["test"]:
        rows = [json.loads(l) for l in V5.read_text().splitlines() if l.strip()]
        raws = O.raw_lines()
        src = O.sources_of(O.trace(rows, raws, *O.pools()), O.derive(raws, O.source_lines()))
        b = bars(editions, narratives, lines, {tid: v[0][0] for tid, v in src.items() if v})
        print(f"known pairs: {b['pairs']} {b['by_kind']}")
        for name in ("as_written", "with_the_floor"):
            f = b[name]
            print(f"bar A, {name.replace('_', ' ')}: the partner is the best match, sure or doubtful, for {f['right']} "
                  f"of {b['pairs']} ({f['right'] / b['pairs']:.1%}; the bar is 90%): sure {f['sure']}, doubtful "
                  f"{f['doubtful']}; counting another line of the same text as right: "
                  f"{f['right_or_another_line_of_the_same_text']} ({f['right_or_another_line_of_the_same_text'] / b['pairs']:.1%})")
            print(f"       pairs with a sure match to another text of the partner's family: {f['with_a_sure_other']} "
                  f"(the bar is none); to a text that is not the partner's own: {f['with_a_sure_other_of_another_text']}")
            for m in f["missed"]:
                print("    missed:", m)
        k = b["karanog"]
        print(f"bar B: {k['with_a_sure_match_to_another_number']} of {k['texts']} Karanog texts have a sure match to "
              f"another Karanog number ({k['with_a_sure_match_to_another_number'] / k['texts']:.1%}): {k['pairs']}")
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
