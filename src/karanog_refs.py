"""Merge the typed reference pages of Griffith's Karanog into one table per inscription.

Griffith prints most words of every Karanog and Shablul inscription a second time in type: the table of names
and parentage (pp. 87-94), Indexes A to C (pp. 95-122) and the tables of the closing formulae (pp. 42-53).
data/expansion/karanog/refs/typed/<typist>/ref_pdfNNN.jsonl hold those pages as typed (NNN is the page of the
archive.org PDF, the printed page plus 16). This script works out which inscriptions each typed entry names and
writes data/expansion/karanog/refs/by_inscription/<Kar|Sh>_<NNN>.jsonl, the table a reading of the hand copy
is checked against, and refs/all_refs.jsonl.

  python3 -I src/karanog_refs.py       # writes the files and prints the counts
"""
import collections, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "data/expansion/karanog/refs"
TOK = re.compile(r"Kar\.\s*(?:graff|Ostr)\.|Kar\.|Sh\.|Inscr\.|Mero[eë]|\bcf\.|\bsee\b|\bpp?\.|\bCh\.|\bPl\.|\bnote\b|;"
                 r"|\d+\s?[ab]?\b(?:\s?[-–]\s?\d+)?(?:/\d+)?")
LAST = {"Kar": 132, "Sh": 20}                    # the numbers Griffith gives


def text_id(s):
    """'Kar. 39 b' -> ('Kar', 39, 'b'); None when it is not a Karanog or Shablul number."""
    m = re.fullmatch(r"\s*(Kar|Sh)\.\s*(\d+)\s*([a-d])?\s*", s or "")
    return (m.group(1), int(m.group(2)), m.group(3) or "") if m else None


def parse_refs(refs):
    """The inscriptions an index entry's references name: [(site, number, part, cf, line, flag)].

    cf is true after "cf." (a comparison, not an occurrence). A form printed inside the entry (typed in braces)
    has its own typed object, so reading stops at the first brace. Page, chapter and note numbers, graffiti,
    ostraca and other publications are skipped, and so is the figure in a label such as "form D 2" or "n. A 2". "118-20" is a short range; a wide one such as "Kar. 19-89" is two
    monuments of one person, and both are flagged "pair".
    """
    s = re.sub(r"\([^)]*\)", " ", refs.split("{")[0])
    s = re.sub(r"\b(form\s+[A-J]|n\.\s*[A-C]{1,3})\s*\d\b", " ", s)
    site, cf, skip, out = None, False, False, []
    for m in TOK.finditer(s):
        t = m.group(0)
        if t.startswith("Kar.") and t != "Kar.":       # graffiti and ostraca have numbers of their own
            site, skip = None, True
        elif t in ("Kar.", "Sh."):
            site, skip = t[:-1], False
        elif t.startswith(("Inscr", "Mero")):
            site, skip = None, True
        elif t == "cf.":
            cf = True
        elif t in ("see", "p.", "pp.", "Ch.", "Pl.", "note"):
            skip = True
        elif t == ";":
            cf = False
        elif t[0].isdigit():
            if skip and site is None:
                continue
            if skip:                              # "see p. 81": one number, then back to the site
                skip = False
                continue
            mm = re.fullmatch(r"(\d+)\s?([ab])?(?:\s?[-–]\s?(\d+))?(?:/(\d+))?", t)
            a, part, b, line = int(mm.group(1)), mm.group(2) or "", mm.group(3), mm.group(4)
            st = site or "Kar"
            if st == "Sh" and a > LAST["Sh"]:     # "Sh. 1, 2, 9. Later 64/23": the list goes on with Karanog
                st = "Kar"
            if b:
                b = int(b)
                if b < a:                         # "118-20" = 118 to 120
                    b = int(str(a)[:len(str(a)) - len(str(b))] + str(b))
                nums = [(n, "") for n in range(a, b + 1)] if b - a <= 5 else [(a, "pair"), (b, "pair")]
            else:
                nums = [(a, "")]
            out += [(st, n, part if len(nums) == 1 else "", cf, line, flag) for n, flag in nums if 1 <= n <= LAST[st]]
    return out


def bare(reading):
    return re.sub(r"[?()\[\]. :]", "", reading)


def load(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def typed(refs=None):
    """Every typed object, with two repairs that the double typing showed to be needed.

    The first typist of the names of Kar. 1 to 71 (N1) typed the joined pair b + i as "ii": the second typing of
    p. 87 and Griffith's own English forms (Sharbiye, Trebit, Trebiñti) show b + i, so "ii" becomes "bi" there,
    with a note. And where the second typing of a names cell differs from the first, it is added as a second
    entry, so that a reader sees both.
    """
    refs = refs or REFS
    out = []
    for p in sorted((refs / "typed").glob("*/ref_pdf*.jsonl")):
        for n, o in enumerate(load(p), 1):
            o["typist"], o["row"] = p.parent.name, n
            if o["typist"] == "N1" and o["kind"] == "name" and "ii" in o["reading"]:
                o["notes"] = (f"Typed {o['reading']}; 'ii' corrected to 'bi' (a joined b and i). " + o.get("notes", "")).strip()
                o["reading"] = o["reading"].replace("ii", "bi")
            out.append(o)
    first = {(o["page"], o["text"], o.get("person"), o.get("col")): o for o in out if o["kind"] == "name"}
    for p in sorted((refs / "second_typing").glob("*/ref_pdf*.jsonl")):
        for n, o in enumerate(load(p), 1):
            if o["kind"] != "name":
                continue
            x = first.get((o["page"], o["text"], o.get("person"), o.get("col")))
            if x is None or bare(x["reading"]) != bare(o["reading"]):
                o["typist"], o["row"] = p.parent.name, n
                o["notes"] = (f"Second, independent typing of this cell; the first has {x['reading'] if x else 'nothing'}. "
                              + o.get("notes", "")).strip()
                out.append(o)
    return out


def tables(objs):
    """{(site, number): [entry, ...]} and the objects that name no inscription."""
    per, none = collections.defaultdict(list), []
    for o in objs:
        if o["kind"] in ("formula", "name"):
            tid = text_id(o.get("text"))
            targets = [(tid[0], tid[1], tid[2], False, None, "")] if tid and tid[1] <= LAST[tid[0]] else []
        else:
            targets = parse_refs(o.get("refs", ""))
        if not targets:
            none.append(o)
        source = {"formula": f"formula {o.get('formula')} ({o.get('where')})",
                  "name": f"names table, column {o.get('col')} (person {o.get('person')})",
                  "index": f"Index {o.get('index')}"}[o["kind"]]
        for site, num, part, cf, line, flag in targets:
            e = {"source": source, "reading": o["reading"], "part": part, "compare_only": cf, "line": line, "flag": flag,
                 "printed_refs": o.get("refs") or o.get("marks") or "", "gloss": o.get("gloss", ""),
                 "page": o["page"], "typist_notes": o.get("notes", "")}
            if e not in per[(site, num)]:
                per[(site, num)].append(e)
    return per, none


def main():
    objs = typed()
    per, none = tables(objs)
    out = REFS / "by_inscription"
    out.mkdir(exist_ok=True)
    for old in out.glob("*.jsonl"):
        old.unlink()
    for (site, num), es in per.items():
        (out / f"{site}_{num:03d}.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in es))
    (REFS / "all_refs.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs))
    kinds = collections.Counter(o["kind"] for o in objs)
    missing = [f"{s}. {n}" for s in LAST for n in range(1, LAST[s] + 1) if (s, n) not in per]
    print(f"typed objects {len(objs)} ({dict(kinds)}); inscriptions with entries {len(per)} of {sum(LAST.values())}; "
          f"entries {sum(len(v) for v in per.values())}; objects that name no inscription {len(none)}")
    print("without any entry:", missing or "none")


if __name__ == "__main__":
    main()
