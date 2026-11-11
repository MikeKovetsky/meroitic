"""How far do two independent readers of the same Karanog hand copies agree?

  python3 -I runs/work/karanog/compare_readers.py [--differences <out.jsonl>]

data/expansion/karanog/second_reading/<pack>/ holds a second reader's files for one page, made like the first
reader's (copy_only.jsonl from the copy alone, final.jsonl after the check against Griffith's type), and pick.json
says how the pages were chosen. For every inscription read twice this prints the signs of the first reading
that the second also has: the first reading's signs less the edit distance between the two, the measure
score_fhn.py uses against FHN (a sign only one reader has counts against it). Lost signs are left out of the
signs and counted apart, because the two readers estimate a hatched stretch each in their own way. The last line
of each part gives the figure for all 53 pages: the seven damaged pages, all read twice, at their own rate, and
the other 46 at the rate of the three drawn at random, each weighted by its signs of the first reading.
"""
import collections, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
import karanog as K   # noqa: E402

SECOND = K.KAR / "second_reading"


def distance(a, b):
    """Edit distance between two lists of signs (one sign changed, added or left out costs 1)."""
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def by_text(objs):
    """{(site, number): the readings of its parts, in file order}."""
    out = collections.defaultdict(list)
    for o in objs:
        out[K.number(o["text"])].append(o["reading"])
    return out


def read(reading_parts):
    """(signs without the lost ones, number of lost signs) of an inscription's parts."""
    signs = [s for r in reading_parts for s in K.signs(r)]
    return [s for s in signs if s != "."], signs.count(".")


def first_readings(name):
    out = {}
    for pack in sorted(p for p in (K.KAR / "readings").iterdir() if p.is_dir()):
        out.update(by_text(K.load(pack, name)))
    return out


def compare(name, first=None, second_dir=None):
    """[(pack, (site, number), signs of the first reading, edit distance, lost signs first, lost signs second)]
    for one kind of file ("copy_only.jsonl" or "final.jsonl"), over every second-reading pack that has it."""
    first = first or first_readings(name)
    rows = []
    for pack in sorted(p for p in (second_dir or SECOND).iterdir() if p.is_dir()):
        for n, parts in by_text(K.load(pack, name)).items():
            if n not in first:
                raise ValueError(f"{pack / name}: {n} has no first reading")
            (a, lost_a), (b, lost_b) = read(first[n]), read(parts)
            rows.append((pack.name, n, len(a), distance(a, b), lost_a, lost_b))
    return rows


def differences(first=None, second_dir=None):
    """The places where the two checked readings differ: [{text, first, second, before, after}], each the signs
    of one differing stretch with up to six signs of the first reading on either side."""
    import difflib
    first = first or first_readings("final.jsonl")
    out = []
    for pack in sorted(p for p in (second_dir or SECOND).iterdir() if p.is_dir()):
        for (site, no), parts in by_text(K.load(pack, "final.jsonl")).items():
            a, b = read(first[(site, no)])[0], read(parts)[0]
            for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                if op != "equal":
                    out.append({"pack": pack.name, "text": f"{site}. {no}", "first": "".join(a[i1:i2]), "second": "".join(b[j1:j2]),
                                "before": "".join(a[max(0, i1 - 6):i1]), "after": "".join(a[i2:i2 + 6])})
    return out


def groups(second_dir=None):
    pick = json.loads(((second_dir or SECOND) / "pick.json").read_text())
    return {f"S{leaf}": g for g in ("damaged", "random", "control") for leaf in pick[g]}


def page_signs(name, readings=None):
    """{leaf: the signs of the first reading on that page, lost signs left out} for one kind of file."""
    out = collections.Counter()
    for pack in sorted(p for p in (readings or K.KAR / "readings").iterdir() if p.is_dir()):
        for o in K.load(pack, name):
            out[re.search(r"(\d+)", o["page"]).group(1)] += len(read([o["reading"]])[0])
    return out


def whole_set(total, group, signs):
    """(the agreement for all pages, signs of the damaged pages, signs of the others): the damaged pages at their
    own rate, since every one of them was read twice, and the others at the rate of the pages drawn at random.
    total is {group: (signs the second reader has, signs of the first reading)}, signs is page_signs()."""
    damaged = sum(n for leaf, n in signs.items() if group.get(f"S{leaf}") == "damaged")
    other = sum(signs.values()) - damaged
    rate = lambda g: total[g][0] / total[g][1]
    return (damaged * rate("damaged") + other * rate("random")) / (damaged + other), damaged, other


def main():
    group = groups()
    for name, title in (("copy_only.jsonl", "hand copy alone"), ("final.jsonl", "after the check against the type")):
        rows = compare(name)
        print(f"{title}:")
        total = collections.defaultdict(lambda: [0, 0])
        for pack, (site, no), n, d, lost_a, lost_b in rows:
            print(f"  {pack} {site}. {no}: {n - d} of {n} signs of the first reading ({(n - d) / n:.1%}); lost signs {lost_a} and {lost_b}")
            for g in (group[pack], "all"):
                total[g][0] += n - d
                total[g][1] += n
        for g in ("damaged", "random", "control", "all"):
            if total[g][1]:
                print(f"  {g.upper()}: {total[g][0]} of {total[g][1]} ({total[g][0] / total[g][1]:.1%})")
        signs = page_signs(name)
        est, damaged, other = whole_set(total, group, signs)
        print(f"  ALL {len(signs)} PAGES: {est:.1%} (the damaged pages, {damaged} signs, at their rate; the other "
              f"{len(signs) - sum(g == 'damaged' for g in group.values())}, {other} signs, at the random pages' rate)")
    if "--differences" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--differences") + 1])
        diff = differences()
        out.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in diff))
        print(f"{len(diff)} differing places -> {out}")


if __name__ == "__main__":
    main()
