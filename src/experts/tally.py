"""Counts for the check of the coverage map against Millet 2005 and FHN III (local only).

  python3 -I src/experts/tally.py [folder]

Reads rows.jsonl (every word of the held texts with our level and reading, and which rows are decoys) and the
judges' answers in answers/, prints the tables and writes figures.json, differences.tsv, missing_meanings.tsv
(rows any judge gives a meaning) and decoys.tsv (each decoy beside the reading we really hold) beside them. The
answers are untrusted data: only the fields row, verdict, expert and doubt are read.
"""
import collections
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FOLDER = ROOT / "data/sources/expert"
VERDICTS = ("agree", "partly", "differ", "new", "silent", "absent")
GIVEN = ("agree", "partly", "differ", "new")          # the expert gives the word a meaning
TRANSLATED = ("meaning", "grammar", "name", "number")  # the levels the map counts as translated
CLASSES = {"agree": "agree", "partly": "other meaning", "differ": "other meaning", "new": "other meaning",
           "silent": "no meaning", "absent": "no meaning"}
SOURCES = {"millet": "Millet 2005", "fhn": "FHN III"}


def load_rows(path):
    """The judged rows (those with a row id), in order."""
    return [r for r in (json.loads(l) for l in path.open(encoding="utf-8")) if r["row"]]


def load_answers(path, ids):
    """({row id: answer}, [problems]) of one judge's file. An answer is kept when its row id is one of ids, its
    verdict is one of VERDICTS and the row was not answered before; everything else is a problem, and so is a
    row id of ids without an answer."""
    out, problems = {}, []
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            a = json.loads(line)
            row, verdict = a["row"], a["verdict"]
        except (ValueError, KeyError, TypeError):
            problems.append(f"line {n}: not an answer")
            continue
        if not isinstance(row, str) or not isinstance(verdict, str):
            problems.append(f"line {n}: not an answer")
            continue
        if row not in ids:
            problems.append(f"line {n}: unknown row {row!r}")
        elif verdict not in VERDICTS:
            problems.append(f"line {n}: unknown verdict {verdict!r} for {row}")
        elif row in out:
            problems.append(f"line {n}: {row} answered twice (first answer kept)")
        else:
            out[row] = {"verdict": verdict, "expert": str(a.get("expert") or "")[:120], "doubt": a.get("doubt") is True}
    problems += [f"no answer for {i}" for i in sorted(ids - set(out))]
    return out, problems


def count(rows, answers):
    """Verdicts of the rows that have an answer, as a dict in the order of VERDICTS, with the total, the rows
    without an answer, the number where the expert gives a meaning, and the share of those where the two readings
    agree."""
    c = collections.Counter(answers[r["row"]]["verdict"] for r in rows if r["row"] in answers)
    given = sum(c[v] for v in GIVEN)
    return {**{v: c[v] for v in VERDICTS}, "rows": sum(c.values()), "unanswered": len(rows) - sum(c.values()),
            "given": given,
            "agree_share": round(c["agree"] / given, 4) if given else None,
            "agree_or_partly_share": round((c["agree"] + c["partly"]) / given, 4) if given else None}


def kappa(pairs):
    """Cohen's kappa of two judges' labels, [(first, second)]; None without pairs or when chance agreement is 1."""
    n = len(pairs)
    if not n:
        return None
    same = sum(a == b for a, b in pairs) / n
    first, second = collections.Counter(a for a, _ in pairs), collections.Counter(b for _, b in pairs)
    chance = sum(first[k] * second[k] for k in first) / (n * n)
    return None if chance == 1 else round((same - chance) / (1 - chance), 4)


def two_judges(rows, one, two):
    """How two judges of the same rows compare: on the six verdicts and on three classes (agree, another meaning
    given, no meaning given)."""
    both = [r for r in rows if r["row"] in one and r["row"] in two]
    pairs = [(one[r["row"]]["verdict"], two[r["row"]]["verdict"]) for r in both]
    classes = [(CLASSES[a], CLASSES[b]) for a, b in pairs]
    return {"rows": len(pairs), "same_verdict": sum(a == b for a, b in pairs), "kappa": kappa(pairs),
            "same_class": sum(a == b for a, b in classes), "kappa_classes": kappa(classes),
            "table": {f"{a} / {b}": k for (a, b), k in sorted(collections.Counter(pairs).items())}}


def figures(rows, judges):
    """All counts. judges = {name: {row id: answer}}; "judge1" has every pack, a second judge only some rows."""
    one = judges["judge1"]
    real = [r for r in rows if not r["decoy"]]
    done = [r for r in real if r["level"] in TRANSLATED]
    rest = [r for r in real if r["level"] not in TRANSLATED]
    out = {"rows": len(rows), "decoys": sum(r["decoy"] for r in rows), "texts": len({r["text"] for r in rows}),
           "translated": {"all": count(done, one)}, "not_translated": {"all": count(rest, one)},
           "decoys_by_judge": {}, "two_judges": {}}
    for level in TRANSLATED:
        out["translated"][level] = count([r for r in done if r["level"] == level], one)
    for source, label in SOURCES.items():
        out["translated"][label] = count([r for r in done if r["source"] == source], one)
    for level in ("hypothesis", "kind", "unknown"):
        out["not_translated"][level] = count([r for r in rest if r["level"] == level], one)
    agreed = [r for r in done if one.get(r["row"], {}).get("verdict") == "agree"]
    out["translated"]["agree_with_doubt"] = sum(one[r["row"]]["doubt"] for r in agreed)
    for name, answers in judges.items():
        packs = {r["pack"] for r in rows if r["row"] in answers}       # a second judge reads only some packs
        out["decoys_by_judge"][name] = count([r for r in rows if r["decoy"] and r["pack"] in packs], answers)
        if name != "judge1":
            mine = [r for r in rows if r["row"] in answers]
            out["two_judges"][name] = {
                "all rows": two_judges(mine, one, answers),
                "translated, decoys left out": two_judges([r for r in mine if r in done], one, answers),
                "translated, by this judge": count([r for r in mine if r in done], answers),
                "translated, by the first judge on the same rows": count([r for r in mine if r in done], one)}
    return out


def listed(rows, judges, verdicts, translated, any_judge=False):
    """The rows (decoys left out) of translated or of not translated words whose first judge's verdict is one of
    verdicts (with any_judge: whose verdict of any judge is), as table lines with the other judges' verdicts
    beside."""
    one = judges["judge1"]
    out = []
    for r in rows:
        a = one.get(r["row"])
        hit = bool(a) and a["verdict"] in verdicts
        if any_judge:
            hit = hit or any(j[r["row"]]["verdict"] in verdicts for j in judges.values() if r["row"] in j)
        if r["decoy"] or not hit or (r["level"] in TRANSLATED) != translated:
            continue
        a = a or {"verdict": "", "expert": "", "doubt": False}
        others = "; ".join(f"{j[r['row']]['verdict']}: {j[r['row']]['expert']}"
                           for n, j in judges.items() if n != "judge1" and r["row"] in j)
        out.append({"row": r["row"], "source": SOURCES[r["source"]], "entry": r["entry"], "text": r["text"],
                    "word": r["form"], "level": r["level"], "our reading": r["ours"], "verdict": a["verdict"],
                    "the expert's meaning": a["expert"], "expert unsure": "yes" if a["doubt"] else "",
                    "second judge": others})
    return out


def decoy_list(rows, judges):
    """The decoys with the reading we really hold beside the one the judges saw, to tell a judge's slip from a
    decoy that happens to mean the same, and to compare the expert's meaning with our real reading."""
    return [{"row": r["row"], "source": SOURCES[r["source"]], "entry": r["entry"], "word": r["form"],
             "our real reading": r.get("really") or "", "the decoy shown": r["ours"],
             **{f"{n} verdict": (j[r["row"]]["verdict"] if r["row"] in j else "") for n, j in judges.items()},
             **{f"{n} expert": (j[r["row"]]["expert"] if r["row"] in j else "") for n, j in judges.items()}}
            for r in rows if r["decoy"]]


def write_tsv(path, lines):
    if not lines:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lines[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(lines)


def show(name, c):
    share = "" if c["agree_share"] is None else f"  agree {c['agree_share']:.1%} of {c['given']} with a meaning"
    cells = "  ".join(f"{v} {c[v]}" for v in VERDICTS)
    missing = f"  NO ANSWER {c['unanswered']}" if c["unanswered"] else ""
    print(f"  {name:28} rows {c['rows']:4}  {cells}{share}{missing}")


def main(argv):
    folder = pathlib.Path(argv[1]) if len(argv) > 1 else FOLDER
    rows = load_rows(folder / "rows.jsonl")
    ids = {r["row"] for r in rows}
    if len(ids) != len(rows):
        raise SystemExit("rows.jsonl: a row id stands twice")
    odd = {r["level"] for r in rows} - set(TRANSLATED) - {"hypothesis", "kind", "unknown"}
    if odd:
        raise SystemExit(f"rows.jsonl: judged rows of a level the tables do not show: {sorted(odd)}")
    judges, problems = collections.defaultdict(dict), {}
    for f in sorted((folder / "answers").glob("judge*_*.jsonl")):
        m = re.fullmatch(r"(judge\d+)_([A-Z])", f.stem)
        if not m:
            problems[f.name] = ["not read: the name is not judgeN_PACK.jsonl"]
            continue
        name, pack = m.groups()
        answers, bad = load_answers(f, {r["row"] for r in rows if r["pack"] == pack})
        judges[name].update(answers)
        problems[f.name] = bad
    for pack in sorted({r["pack"] for r in rows}):
        if f"judge1_{pack}.jsonl" not in problems:
            problems[f"judge1_{pack}.jsonl"] = ["no such file: the first judge's pack is not counted"]
    if "judge1" not in judges:
        raise SystemExit("no answers of the first judge yet")
    figs = figures(rows, judges)
    figs["problems"] = problems
    for f, bad in problems.items():
        print(f"{f}: {len(bad)} problems" + ("" if not bad else ": " + "; ".join(bad[:6])))
    print(f"\n{figs['texts']} texts, {figs['rows']} rows, {figs['decoys']} of them decoys (left out below)")
    print("\nWords the map counts as translated, first judge:")
    for name, c in figs["translated"].items():
        if isinstance(c, dict):
            show(name, c)
    print(f"  of the agreements, on a meaning the expert marks as unsure: {figs['translated']['agree_with_doubt']}")
    print("\nWords the map does not count as translated, first judge:")
    for name, c in figs["not_translated"].items():
        show(name, c)
    print("\nDecoys (a reading swapped for another word's):")
    for name, c in figs["decoys_by_judge"].items():
        show(name, c)
    for name, t in figs["two_judges"].items():
        print(f"\nTwo judges on the same rows ({name} against the first):")
        for part in ("all rows", "translated, decoys left out"):
            x = t[part]
            print(f"  {part:28} rows {x['rows']:4}  same verdict {x['same_verdict']} (kappa {x['kappa']})  "
                  f"same class {x['same_class']} (kappa {x['kappa_classes']})")
        show("translated, this judge", t["translated, by this judge"])
        show("translated, first judge", t["translated, by the first judge on the same rows"])
    (folder / "figures.json").write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write_tsv(folder / "differences.tsv", listed(rows, judges, ("partly", "differ", "new"), True))
    write_tsv(folder / "missing_meanings.tsv", listed(rows, judges, GIVEN, False, any_judge=True))
    write_tsv(folder / "decoys.tsv", decoy_list(rows, judges))


if __name__ == "__main__":
    main(sys.argv)
