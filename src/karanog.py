"""Build the Karanog and Shablul rows from the readers' files: data/expansion/karanog/griffith_karanog.jsonl.

Griffith's Karanog (1911) gives the inscriptions as hand copies. Each was read twice by one reader
(data/expansion/karanog/readings/<pack>/): first from the copy alone (copy_only.jsonl), then checked against
the words Griffith printed in type in the same book, his table of names, Indexes A to C and the tables of the
closing formulae (final.jsonl; the typed pages are in data/expansion/karanog/refs/). This script turns the
checked readings into rows shaped like the other data/expansion/griffith_*.jsonl files: one row per
inscription, the reading as written (text_std) and in the corpus spelling (text_corpus).

  python3 -I src/karanog.py            # writes the file and prints the counts
"""
import collections, difflib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KAR = ROOT / "data/expansion/karanog"
ITEM = "karangmeroitic00grifuoft"
SOURCE = "Karanòg: The Meroitic Inscriptions of Shablûl and Karanòg (Griffith 1911)"
SIGN = re.compile(r"se|te|to|[aeioywbpmnñrlḫẖskqtd]")
CORPUS = {"s": "S", "se": "s", "ñ": "N", "ḫ": "x", "ẖ": "X"}        # README, the corpus spelling
SITES = {"Kar": "Karanog", "Sh": "Shablul"}
# measured by runs/work/karanog/score_fhn.py on the four texts FHN III prints (data/expansion/karanog/README.md)
ACCURACY = ("Measured accuracy of the method, on the four Karanog texts that FHN III prints (Kar. 47, 77, 78 and the "
            "spout of 121): 639 of 654 signs right (97.7%) after the check, 582 (89.0%) from the hand copies alone.")


def number(text):
    """'Kar. 39' -> ('Kar', 39); None for anything else."""
    m = re.fullmatch(r"\s*(Kar|Sh)\.\s*(\d+)\s*", text or "")
    return (m.group(1), int(m.group(2))) if m else None


def marked(reading):
    """The reading with a NUL for each lost sign and each sign in square brackets (a restoration: lost, as in the
    other Griffith files), and '|' for each line number, which parts two signs but not two words."""
    t = re.sub(r"\(\d+\)", "|", reading).replace("[.]", "\x00")
    return re.sub(r"\[([^\]]*)\]", lambda m: "\x00" * len(SIGN.findall(m.group(1))), t)


def tokens(t):
    return ["." if m.group(0) == "\x00" else m.group(0) for m in re.finditer(r"\x00|" + SIGN.pattern, t)]


def signs(reading):
    """The signs of a reading in order; a lost or restored sign is '.'. Line numbers, dividers and query marks are
    not signs, but they stand between two: "arwt(14)e" is t and e, not the te sign, and "s?e" is s and e."""
    return tokens(marked(reading))


def to_corpus(reading):
    """A reading in the corpus spelling: words apart by one space, a dot for each lost or restored sign.

    A divider and a gap both end a word; a line number inside a word does not.
    """
    words = ("".join(CORPUS.get(s, s) for s in tokens(chunk)) for chunk in re.split(r"[\s:]+", marked(reading)))
    return " ".join(w for w in words if w)


def changed(before, after):
    """How many signs differ between two readings of one text (the longer side of each differing stretch)."""
    a, b = signs(before), signs(after)
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    return sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in ops if op != "equal")


def load(pack, name):
    p = pack / name
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def rows(readings=None):
    """One row per inscription, in Griffith's order."""
    readings = readings or KAR / "readings"
    by_text = collections.defaultdict(lambda: {"final": [], "first": [], "kept": [], "unplaced": [], "pack": ""})
    for pack in sorted(p for p in readings.iterdir() if p.is_dir()):
        final = load(pack, "final.jsonl")
        if not final:
            continue                                   # a pack whose check is not done yet is left out
        for name, key in (("final.jsonl", "final"), ("copy_only.jsonl", "first"),
                          ("kept_against_type.jsonl", "kept"), ("unplaced.jsonl", "unplaced")):
            for o in load(pack, name):
                n = number(o.get("text"))
                if n is None:                          # a reading that names no inscription would be lost
                    raise ValueError(f"{pack / name}: text {o.get('text')!r} is not 'Kar. N' or 'Sh. N' "
                                     f"(a part's letter goes in 'part')")
                by_text[n][key].append(o)
                by_text[n]["pack"] = pack.name
    out = []
    for (site, no) in sorted(by_text, key=lambda k: (k[0] != "Kar", k[1])):
        t = by_text[(site, no)]
        parts, first = t["final"], t["first"]
        label = lambda o: f"{o['part']}: " if o.get("part") else ""
        std = " | ".join(label(o) + o["reading"].strip() for o in parts)
        corpus = " ".join(filter(None, (to_corpus(o["reading"]) for o in parts)))
        sg = [s for o in parts for s in signs(o["reading"])]
        leaf = re.search(r"(\d+)", parts[0].get("page", ""))
        page = f"p. {int(leaf.group(1)) - 15} (leaf n{leaf.group(1)})" if leaf else ""
        caption = re.sub(r"^\s*(Kar|Sh)\.\s*\d+\.?\s*", "", parts[0].get("caption", "")).strip()
        diff = sum(changed(a["reading"], b["reading"]) for a, b in zip(first, parts)) if len(first) == len(parts) else None
        notes = [f"Read from Griffith's hand copy by Claude Opus 5.5 (pack {t['pack']}), then checked against the "
                 f"words he prints in type (names table, Indexes A to C, formula tables): {sum(o.get('entries') or 0 for o in parts)} "
                 f"printed entries placed" + (f", {diff} signs changed by the check" if diff is not None else "") + ".",
                 ACCURACY]
        if len(parts) > 1:
            notes.append("Parts as labelled on the copy: " + "; ".join(
                f"{o.get('part') or '(main)'}" + (f" ({', '.join(o['labels'])})" if o.get("labels") else "") for o in parts) + ".")
        if t["kept"]:
            notes.append("Copy kept against the type: " + "; ".join(
                f"{k.get('copy', '')} (type: {k.get('type', '')})" for k in t["kept"]) + ".")
        if t["unplaced"]:
            notes.append("Printed entries not found in the copy: " + "; ".join(
                f"{u.get('reading', '')} ({u.get('source', '')})" for u in t["unplaced"]) + ".")
        notes += [o["check_notes"].strip() for o in parts if (o.get("check_notes") or "").strip()]
        out.append({"source": SOURCE, "item": ITEM, "griffith_no": no if site == "Kar" else f"Sh{no}",
                    "rem": f"{200 + no:04d}" if site == "Kar" else "", "page": page, "object": caption,
                    "site": SITES[site], "text_std": std, "text_corpus": corpus,
                    "uncertain": sum(o["reading"].count("?") for o in parts),
                    "signs": sum(s != "." for s in sg), "notes": " ".join(notes)})
    return out


def main():
    out = rows()
    with open(KAR / "griffith_karanog.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    words = sum(len([w for w in r["text_corpus"].split() if w.strip(".")]) for r in out)
    print(f"{len(out)} inscriptions, {sum(r['signs'] for r in out)} signs, {words} words, "
          f"{sum(r['uncertain'] for r in out)} query marks -> {KAR / 'griffith_karanog.jsonl'}")


if __name__ == "__main__":
    main()
