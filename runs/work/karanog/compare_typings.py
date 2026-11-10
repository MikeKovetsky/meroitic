"""Compare the second typing of a reference page with the first, sign by sign (data/expansion/karanog/README.md,
section 3).

  python3 -I runs/work/karanog/compare_typings.py                    # every page in refs/second_typing/QA/
  python3 -I runs/work/karanog/compare_typings.py <a.jsonl> <b.jsonl>

Names are paired by inscription, person and column, formulae by formula, inscription and place; index entries
have no key and are paired in order by a sequence match on their signs. A pair counts its signs the same against
the longer of the two. Griffith's (?) and the line numbers are not signs; a [.] is one.
"""
import difflib, json, re, sys
from pathlib import Path

REFS = Path(__file__).resolve().parents[3] / "data/expansion/karanog/refs"


def signs(s):
    s = re.sub(r"\(\d+\)|\(\?\)", "", s)
    out, i = [], 0
    while i < len(s):
        if s.startswith("[.]", i):
            out.append("[.]")
            i += 3
            continue
        if s[i:i + 2] in ("se", "te", "to"):
            out.append(s[i:i + 2])
            i += 2
            continue
        if s[i] in "aeioywbpmnñrlḫẖskqtd":
            out.append(s[i])
        i += 1
    return out


def key(o):
    if o["kind"] == "formula":
        return ("formula", o.get("formula"), o.get("text"), o.get("where"))
    if o["kind"] == "name":
        return ("name", o.get("text"), o.get("person"), o.get("col"))
    return None


def load(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def pairs(a, b):
    """The objects of the two typings paired, and a note for each one that could not be paired."""
    out, notes = [], []
    if a and a[0]["kind"] == "index":
        sa, sb = ["".join(signs(o["reading"])) for o in a], ["".join(signs(o["reading"])) for o in b]
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes():
            if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
                out += [(a[i1 + k], b[j1 + k]) for k in range(i2 - i1)]
            else:
                notes.append(f"not paired: A {[o['reading'] for o in a[i1:i2]]} | B {[o['reading'] for o in b[j1:j2]]}")
        return out, notes
    da, db = {}, {}
    for o in a:
        da.setdefault(key(o), []).append(o)
    for o in b:
        db.setdefault(key(o), []).append(o)
    for k in da:
        if k in db and len(da[k]) == len(db[k]):
            out += list(zip(da[k], db[k]))
        else:
            notes.append(f"only in A or count differs: {k} {[o['reading'] for o in da[k]]} {[o['reading'] for o in db.get(k, [])]}")
    notes += [f"only in B: {k} {[o['reading'] for o in db[k]]}" for k in db if k not in da]
    return out, notes


def compare(a, b):
    """(signs the same, signs compared, notes) for two typings of one page."""
    same = total = 0
    paired, notes = pairs(a, b)
    for x, y in paired:
        p, q = signs(x["reading"]), signs(y["reading"])
        same += sum(i2 - i1 for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, p, q, autojunk=False).get_opcodes()
                    if op == "equal")
        total += max(len(p), len(q))
        if p != q:
            notes.append(f"differ: {x.get('text') or x.get('refs', '')[:30]} | A {x['reading']} | B {y['reading']}")
    return same, total, notes


def main():
    if len(sys.argv) == 3:
        todo = [(Path(sys.argv[1]), Path(sys.argv[2]))]
    else:
        todo = [(next(REFS.glob(f"typed/*/{q.name}")), q) for q in sorted(REFS.glob("second_typing/*/ref_pdf*.jsonl"))]
    for first, second in todo:
        same, total, notes = compare(load(first), load(second))
        print(f"{first.parent.name}/{first.name} against {second.parent.name}/{second.name}: "
              f"{same} of {total} signs the same ({same / max(1, total):.1%})")
        for n in notes:
            print("  ", n)


if __name__ == "__main__":
    main()
