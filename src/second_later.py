"""A second scholar for the meanings Rilly states in 2016 or 2021 (step G5, data/discovery/second_scholar_later.md).

The entries are those for which two readers found a later meaning among the recurring open words
(src/recurring.py) and the rare spellings (src/rare.py). Beside each stands what other scholars say of the entry:
the statements the literature passes collected from their own works, and the proposals the lexicon of 2003
reports. Two judges say of each pair whether it gives the same meaning; a tenth more rows are decoys. The result
is a status for each meaning, not a count of the map.

Everything is read and written under data/sources/g5/ (local only: the rows quote the sources), except `public`.

  python3 -I src/second_later.py rows      the entries, the rows and the decoys (entries.json, rows.json)
  python3 -I src/second_later.py packs     the rows for two judges (packs/)
  python3 -I src/second_later.py count     the judges compared, the bars, the statuses (result.json)
  python3 -I src/second_later.py public    data/discovery/second_scholar_later_figures.json

What the judges were given is in runs/prompts/G5_judges.md.
"""
import collections
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import lexicon as X                                    # noqa: E402
import recurring as W                                  # noqa: E402

HOME = ROOT / "data/sources/g5"
PUBLIC = ROOT / "data/discovery/second_scholar_later_figures.json"
RARE = ROOT / "data/discovery/rare_spellings_figures.json"
TOKENS = "tokens.json"                                # from the task notifications, typed by hand (local)
RUNS = {"recurring": ROOT / "data/sources/recurring", "g4": ROOT / "data/sources/rare/g4"}
OWN = ("Rilly 2003", "Rilly 2016", "Rilly 2021", "Project")      # not another scholar: Rilly's own works, our pages
SAYS = ("accepts", "probable", "proposes", "doubts", "rejects")  # a statement that takes a stance on a meaning
SEED, DECOYS, PACK = 20261116, 0.10, 60
VERDICTS = ("same", "partly", "other", "no meaning")
BARS = {"kappa_same_or_not": 0.6, "decoys_called_same": 0.10}
# When the rules were set against the judges (2026-11-16, Pacific time), as src/rare.py records it: the commit of the
# rules and its time in git, the first launch and the first count of the answers (the session's log, by hand), and
# the earliest and the latest times of the answer files under HOME.
WHEN = {"set_in": "7395a7f", "set": "13:59:53", "started": "14:00:15", "first_answer": "14:00:57", "last_answer": "14:01:11",
        "counted": "14:02:32"}

BRIEF = """# Two statements about the meaning of a Meroitic word: do they give the same meaning?

Each row below has a Meroitic word (an entry of a dictionary: a word, a stem, or an ending written with a
hyphen), the meaning a recent work gives it, and what another scholar says about it (a quote, or a dictionary's
report of that scholar's proposal, and a line on what it says). For each row, say whether the other scholar gives
the same meaning as the recent work:

- "same": the same meaning, perhaps in other words, a little wider or narrower, or with a different shade
  ("king" and "ruler"; "to give" and "to grant"; "genitive ending" and "possessive suffix");
- "partly": the two overlap but are not the same meaning (one is a part or a kind of the other, or they share a
  field but name different things: "prince" and "king's son"; "water" and "libation");
- "other": a different meaning;
- "no meaning": the other scholar says nothing about the meaning (only about the word's form, reading, class or
  ending, or only prints the word), so that it can neither agree nor disagree. A statement that only rejects some
  meaning without giving its own is "no meaning", unless the meaning it rejects is the recent work's: then "other".

Judge each row on its own, from the two statements alone; do not look anything up and open no other file. Some
rows are wrong on purpose. Write one JSON object per row, in the order of this file, to `{answers}`:

{{"row": "R0001", "verdict": "same", "why": "both say king"}}

"why" is at most twelve words. This pack has {rows} rows: your file must have {rows} lines, one for each row, none
left out. When the file is written, count its lines against that number, then reply in one line: how many rows,
and how many of each verdict.
"""


def read(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def write(name, data):
    (HOME / name).parent.mkdir(parents=True, exist_ok=True)
    (HOME / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def entries():
    """entry -> the meaning Rilly states in 2016 or 2021 (two readers agreed), its source and page, the run it is
    from (the recurring words first), and what other scholars say of it: the statements the literature passes
    collected from their own works, and the proposals the lexicon of 2003 reports."""
    lex, out = W.lexicon(), {}
    for run, folder in RUNS.items():
        ver, checked = read(folder / "lit/verify/result.json"), read(folder / "lit/checked.json")
        for k, v in ver.items():
            if v["verdict"] != "stated":
                continue
            e = out.setdefault(k, {"entry": k, "meaning": v["one"]["meaning"], "source": v["one"]["source"], "page": v["one"]["page"],
                                   "runs": [], "others": []})
            e["runs"].append(run)
            seen = {(o["scholar"], o["quote"]) for o in e["others"]}
            for s in checked[k]["statements"]:
                if s["source"] in OWN or s.get("stance") not in SAYS or (s["source"], s["quote"]) in seen:
                    continue
                seen.add((s["source"], s["quote"]))
                e["others"].append({"scholar": s["source"], "how": "own work", "page": s["page"], "quote": s["quote"], "says": s["says"]})
    for k, e in out.items():
        for p in (lex.get(k) or {}).get("proposals") or []:
            if (p.get("author") or "").startswith("Rilly") or not (p.get("proposal") or "").strip():
                continue
            e["others"].append({"scholar": p["author"], "how": "reported by the lexicon of 2003", "page": lex[k]["page"],
                                "quote": p["proposal"], "says": ""})
    return out


def rows():
    """The rows for the judges: every (entry, other scholar's statement), and a tenth more rows that are decoys:
    an entry's meaning beside a statement about another entry, drawn by a fixed seed."""
    if any(HOME.glob("answers*/*.jsonl")):
        raise SystemExit("answers exist: the rows are not written again")
    ents = entries()
    real = [{"entry": k, "meaning": e["meaning"], "source": e["source"], **o, "decoy": False} for k, e in sorted(ents.items()) for o in e["others"]]
    rnd = random.Random(SEED)
    pool = [r for r in real if r["how"] == "own work" or r["quote"]]
    decoys = []
    for r in rnd.sample(real, round(DECOYS * len(real))):
        other = rnd.choice([p for p in pool if p["entry"] != r["entry"] and p["meaning"] != r["meaning"]])
        decoys.append({**r, **{k: other[k] for k in ("scholar", "how", "page", "quote", "says")}, "decoy": True, "from": other["entry"]})
    table = real + decoys
    rnd.shuffle(table)
    for i, r in enumerate(table, 1):
        r["row"] = f"R{i:04d}"
    write("entries.json", ents)
    write("rows.json", table)
    print(len(ents), "entries;", sum(bool(e["others"]) for e in ents.values()), "with another scholar's statement;", len(real), "rows;",
          len(decoys), "decoys;", dict(collections.Counter(r["how"] for r in real)), dict(collections.Counter(r["scholar"] for r in real).most_common(12)))


def packs():
    if any(HOME.glob("answers*/*.jsonl")):
        raise SystemExit("answers exist: the packs are not written again")
    table = read(HOME / "rows.json")
    groups = [table[i: i + PACK] for i in range(0, len(table), PACK)]
    (HOME / "packs").mkdir(exist_ok=True)
    for n, g in enumerate(groups, 1):
        body = "\n".join(f"- **{r['row']}** | word `{r['entry']}` | the recent work: {r['meaning']} | {r['scholar']} ({r['how']}): \"{r['quote']}\""
                         + (f" | what it says: {r['says']}" if r["says"] else "") for r in g)
        for j in (1, 2):
            (HOME / f"answers{j}").mkdir(exist_ok=True)
            text = BRIEF.format(answers=f"data/sources/g5/answers{j}/J{n:02d}.jsonl", rows=len(g)) + "\n---\n\n" + body + "\n"
            (HOME / "packs" / f"J{n:02d}_j{j}.md").write_text(text, encoding="utf-8")
    write("groups.json", [[r["row"] for r in g] for g in groups])
    print(len(groups), "packs,", len(table), "rows")


def answers(j):
    """A judge's verdicts, kept only for the rows of the pack the file is named after, with a known verdict."""
    groups = read(HOME / "groups.json")
    lines = W.own_lines(HOME / f"answers{j}", groups, "J{n:02d}", "row",
                        lambda r, n: r.get("row") if r.get("row") in groups[n - 1] and r.get("verdict") in VERDICTS else None)
    return {k: r["verdict"] for k, r in lines.items()}


def status(pairs):
    """An entry's status from its real rows' verdict pairs: agreed by two scholars when both judges call a row
    "same"; else disputed when both call a row "other"; else stated by one."""
    same = any(a == b == "same" for a, b in pairs)
    other = any(a == b == "other" for a, b in pairs)
    return "agreed by two scholars" + (", with a dissent" if other else "") if same else "disputed" if other else "stated by one"


def count():
    table, ents = read(HOME / "rows.json"), read(HOME / "entries.json")
    one, two = answers(1), answers(2)
    real = [r for r in table if not r["decoy"]]
    both = [(one[r["row"]], two[r["row"]]) for r in real if r["row"] in one and r["row"] in two]
    kp = W.kappa([(a == "same", b == "same") for a, b in both])
    dec = {str(j): {"shown": sum(r["decoy"] for r in table), **{f"called_{v}": sum(ans.get(r["row"]) == v for r in table if r["decoy"]) for v in ("same", "partly")}}
           for j, ans in ((1, one), (2, two))}             # "partly" is reported: F2's bar counted it with "same"
    bars = {"every_row_answered_by_both": all(r["row"] in one and r["row"] in two for r in table),
            "kappa_same_or_not": kp is not None and kp >= BARS["kappa_same_or_not"],
            "decoys_called_same": all(d["called_same"] <= BARS["decoys_called_same"] * d["shown"] for d in dec.values())}
    by, named = collections.defaultdict(list), collections.defaultdict(list)
    for r in real:
        if r["row"] in one and r["row"] in two:
            by[r["entry"]].append((one[r["row"]], two[r["row"]]))
            if not X.unnamed(r["scholar"]):
                named[r["entry"]].append((one[r["row"]], two[r["row"]]))
    st = {k: status(by.get(k, [])) for k in ents}
    # as F2 did (src/lexicon.py, unnamed): the statuses that rest on a proposal the lexicon gives without a scholar's
    # name, and what they would be without it; reported, not taken out
    alone = {k: status(named.get(k, [])) for k in sorted(ents) if status(named.get(k, [])) != st[k]}
    out = {"entries": len(ents), "rows": len(real), "decoys": dec, "answered_by_both": len(both), "kappa_same_or_not": None if kp is None else round(kp, 4),
           "pairs": dict(collections.Counter(f"{a} / {b}" for a, b in both).most_common()), "bars": bars, "taken": all(bars.values()),
           "statuses": dict(collections.Counter(st.values()).most_common()), "by_entry": st,
           "with_no_other_scholar": sum(not e["others"] for e in ents.values()),
           "without_the_proposals_of_no_named_scholar": alone}
    write("result.json", out)
    print({k: v for k, v in out.items() if k != "by_entry"})


def figures():
    """The public figures: the counts, the bars, each entry's status (headwords only, no wording of a source)."""
    r, tok = read(HOME / "result.json"), read(HOME / TOKENS) if (HOME / TOKENS).exists() else {}
    if not r["taken"]:
        raise SystemExit("the judges missed a bar: no status is taken")
    table = read(HOME / "rows.json")
    real = [x for x in table if not x["decoy"]]
    words = collections.Counter(r["by_entry"][w["entry"]] for w in read(RARE)["g4"]["words"])
    reported = collections.Counter(first_name(x["scholar"]) for x in real if x["how"] != "own work")
    return {"entries": r["entries"], "rows": r["rows"], "rows_by": dict(collections.Counter(x["how"] for x in real).most_common()),
            "reported_by_the_lexicon_most_often": {k: n for k, n in reported.most_common() if n >= 10},
            "decoys": r["decoys"], "answered_by_both": r["answered_by_both"], "kappa_same_or_not": r["kappa_same_or_not"], "pairs": r["pairs"],
            "bars": r["bars"], "taken": r["taken"], "statuses": r["statuses"], "with_no_other_scholar": r["with_no_other_scholar"],
            "without_the_proposals_of_no_named_scholar": r["without_the_proposals_of_no_named_scholar"],
            "by_entry": dict(sorted(r["by_entry"].items())), "words_given_a_meaning_by_g4": dict(words.most_common()),
            "cost": {"agents": len(tok), "tokens": sum(tok.values())}}


def first_name(scholar):
    """The first scholar a row names ("Hintze 1979" and "Hintze; Priese" are Hintze's)."""
    return re.split(r"[\s,;(]", scholar.strip(), maxsplit=1)[0]


def public():
    figs = figures()
    PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print({k: v for k, v in figs.items() if k != "by_entry"})


COMMANDS = {"rows": rows, "packs": packs, "count": count, "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
