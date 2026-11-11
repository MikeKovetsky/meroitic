"""Build the Karanog and Shablul rows from the readers' files: data/expansion/karanog/griffith_karanog.jsonl.

Griffith's Karanog (1911) gives the inscriptions as hand copies. Each was read twice by one reader
(data/expansion/karanog/readings/<pack>/): first from the copy alone (copy_only.jsonl), then checked against
the words Griffith printed in type in the same book, his table of names, Indexes A to C and the tables of the
closing formulae (final.jsonl; the typed pages are in data/expansion/karanog/refs/). This script turns the
checked readings into rows shaped like the other data/expansion/griffith_*.jsonl files: one row per
inscription, the reading as written (text_std) and in the corpus spelling (text_corpus).

Eleven pages were then read again by a second reader in the same two steps (data/expansion/karanog/second_reading/
<pack>/), who settled each place where the two checked readings differed against the copy and the type
(settled.jsonl, decisions.jsonl; README.md, section 6). For those inscriptions the settled reading is the row's.

text_std is the reading, untouched. text_corpus is made uniform in two ways, so that the same word is
spelled and divided alike in every row (data/expansion/karanog/README.md, section 5):
  - the closing formulae are divided as Griffith divides them. Where his formula tables print as one word of that
    inscription what the reading parts only at a gap ("ḫm lol" where he prints "ḫmlol"), the parts are joined
    (joined()); a divider is the stone's and stays. Where the tables print two words apart ("ato mẖe") and the
    reading has them run together as the stone does ("atomẖe"), they are parted (divided()). A pair the tables
    print apart for 5 inscriptions or more is parted in every row, unless that inscription's own entries print it
    as one word. His indexes are not used for this: there he also sets endings apart from their words
    ("pesto l"), which is analysis, not word division;
  - the title that two readers read slms is slẖs, as in the other rows: Griffith writes it shalkhash (ONE_SPELLING).

  python3 -I src/karanog.py            # writes the file and prints the counts
"""
import collections, difflib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KAR = ROOT / "data/expansion/karanog"
ITEM = "karangmeroitic00grifuoft"
SOURCE = "Karanòg: The Meroitic Inscriptions of Shablûl and Karanòg (Griffith 1911)"
SIGN = re.compile(r"se|te|to|[aeioywbpmnñrlḫẖskqtd]")
MARK = re.compile(r"\(\d+\)|\(sic\)")             # a line number of the stone; Griffith's "sic" by a sign
CORPUS = {"s": "S", "se": "s", "ñ": "N", "ḫ": "x", "ẖ": "X"}        # README, the corpus spelling
SITES = {"Kar": "Karanog", "Sh": "Shablul"}
PAIR = 5        # two words that Griffith prints apart are parted in a reading when they have this many signs together
EVERYWHERE = 5   # a pair that the formula tables print apart for this many inscriptions is parted in every row
JOIN = 4         # the most words that joined() makes one: Griffith's siwiwil, which a reading has as "si wi wi l"
# A word that readers settled two ways, and the spelling text_corpus gives it: the start of the word as read, the
# start as it is written. slẖs: 11 rows have ẖ and 2 have m, where the hand's 3-shaped signs cannot be told
# apart; Griffith's catalogue writes the title "shalkhash" thirteen times and never with m. (As typed, Indexes B and
# C print ẖ and Index A m; README, section 5, says what the readers saw in the type.)
ONE_SPELLING = {("s", "l", "m", "s"): ("s", "l", "ẖ", "s")}
# measured by runs/work/karanog/score_fhn.py on the four texts FHN III prints (data/expansion/karanog/README.md)
ACCURACY = ("Measured accuracy of the method, on the four Karanog texts that FHN III prints (Kar. 47, 77, 78 and the "
            "spout of 121): 639 of 654 signs right (97.7%) after the check, 582 (89.0%) from the hand copies alone.")


def number(text, part_ok=False):
    """'Kar. 39' -> ('Kar', 39); None for anything else. With part_ok, 'Kar. 39 b' is Kar. 39 too: a reader's
    note on a place may name the part, a reading may not (its part has its own field)."""
    m = re.fullmatch(r"\s*(Kar|Sh)\.\s*(\d+)\s*" + (r"(?:[a-d]\s*)?" if part_ok else ""), text or "")
    return (m.group(1), int(m.group(2))) if m else None


def marked(reading):
    """The reading with a NUL for each lost sign and each sign in square brackets (a restoration: lost, as in the
    other Griffith files), and '|' for each line number and each "(sic)", which part two signs but not two words."""
    t = MARK.sub("|", reading).replace("[.]", "\x00")
    return re.sub(r"\[([^\]]*)\]", lambda m: "\x00" * len(SIGN.findall(m.group(1))), t)


def tokens(t):
    return ["." if m.group(0) == "\x00" else m.group(0) for m in re.finditer(r"\x00|" + SIGN.pattern, t)]


def stray(reading):
    """What a reading holds besides signs, lost signs, line numbers, "(sic)", dividers, gaps and query marks.
    tokens() would drop it without a word ("(sic)" was once read as the signs s and i), so rows() stops on it."""
    return re.sub(r"\x00|\||[\s:?]|" + SIGN.pattern, "", marked(reading))


def signs(reading):
    """The signs of a reading in order; a lost or restored sign is '.'. Line numbers, dividers and query marks are
    not signs, but they stand between two: "arwt(14)e" is t and e, not the te sign, and "s?e" is s and e."""
    return tokens(marked(reading))


def runs(reading):
    """The words of a reading in runs that no divider parts: [[word, ...], ...], each word a list of signs. A gap
    (a space, the end of a line) ends a word but not a run; a line number inside a word ends neither."""
    out = []
    for stretch in marked(reading).split(":"):
        ws = [w for w in (tokens(chunk) for chunk in re.split(r"\s+", stretch)) if w]
        if ws:
            out.append(ws)
    return out


def words_of(reading):
    """The words of a reading, each a list of signs. A divider and a gap both end a word; a line number inside a
    word does not."""
    return [w for run in runs(reading) for w in run]


def printed(entries):
    """[(source, words)] of the entries of one inscription whose words can be taken as Griffith's division, each
    word a tuple of signs. An entry that holds brackets of Griffith's (a restoration, an optional letter) is left
    out, and so is one kept for comparison only; his "(?)" and a typist's "?" are dropped."""
    out = []
    for e in entries:
        text = e["reading"].replace("(?)", "").replace("?", "")
        if not e.get("compare_only") and not re.search(r"[()\[\]]", text):
            out.append((e["source"], [tuple(w) for w in words_of(text)]))
    return out


def whole(entries, formula=False):
    """The words that the entries of one inscription print as one word (with formula, the formula tables' only)."""
    return {w for source, ws in printed(entries) if source.startswith("formula") or not formula for w in ws}


def phrases(entries):
    """The pairs of words that Griffith prints apart, side by side, in the formula tables' entries for one
    inscription: [(first, second)], each a tuple of signs, of the entries that printed() keeps. A pair that another
    entry of the inscription prints as one word is no pair (a gap in the table's type, not a word end)."""
    out = {}                                           # a dict for its order: each pair once
    for source, ws in printed(entries):
        if source.startswith("formula"):
            out.update(dict.fromkeys((a, b) for a, b in zip(ws, ws[1:]) if len(a) + len(b) >= PAIR))
    return [(a, b) for a, b in out if a + b not in whole(entries)]


def joined(runs_, whole_words):
    """The words of runs_, joined where Griffith prints as one word what only gaps part in the reading: two to JOIN
    words of one run whose signs together are a word of whole_words ("ḫm lol" is "ḫmlol" when the formula tables
    print ḫmlol); and how many gaps that closed. A divider parts two runs, and is the stone's: it stays."""
    out, closed = [], 0
    for run in runs_:
        i = 0
        while i < len(run):
            j = next((j for j in range(min(len(run), i + JOIN), i + 1, -1)
                      if tuple(s for w in run[i:j] for s in w) in whole_words), i + 1)
            out.append([s for w in run[i:j] for s in w])
            closed += j - i - 1
            i = j
    return out, closed


def divided(words, pairs):
    """words, parted wherever the two words of a pair stand run together inside one of them, before the first and
    between the two; and how many boundaries that added. "atomẖe" with the pair (ato, mẖe) is "ato mẖe", and
    "psoẖatmḫe" with (at, mḫe) is "psoẖ at mḫe". Nothing is cut after the second word: it may be the start of a
    longer one ("pisiḫrkte" where another part of the monument has "pisiḫr"). Words the reading already parts
    stay as they are."""
    out, added = [], 0
    for w in words:
        cuts = set()
        for a, b in pairs:
            both = list(a + b)
            for i in range(len(w) - len(both) + 1):
                if w[i:i + len(both)] == both:
                    cuts |= {i, i + len(a)} - {0}
        added += len(cuts)
        edges = [0] + sorted(cuts) + [len(w)]
        out += [w[i:j] for i, j in zip(edges, edges[1:])]
    return out, added


def one_spelling(words):
    """words with each ONE_SPELLING start replaced; and how many words changed."""
    out, n = [], 0
    for w in words:
        new = next((list(to) + w[len(frm):] for frm, to in ONE_SPELLING.items() if tuple(w[:len(frm)]) == frm), w)
        n += new != w
        out.append(new)
    return out, n


def spell(words):
    return " ".join("".join(CORPUS.get(s, s) for s in w) for w in words)


def count(n, noun):
    """'1 place', '3 places'."""
    return f"{n} {noun}{'' if n == 1 else 's'}"


def to_corpus(reading):
    """A reading in the corpus spelling: words apart by one space, a dot for each lost or restored sign."""
    return spell(words_of(reading))


def changed(before, after):
    """How many signs differ between two readings of one text (the longer side of each differing stretch)."""
    a, b = signs(before), signs(after)
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    return sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in ops if op != "equal")


def load(pack, name):
    p = pack / name
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def entries(site, no, refs):
    """The printed entries of one inscription (refs/by_inscription/, written by src/karanog_refs.py), or []."""
    p = refs / f"{site}_{no:03d}.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def twice(second):
    """{(site, number): (pack, the settled objects, the decisions)} for the inscriptions that a second reader read
    as well and whose differences from the first reading it then settled (second_reading/<pack>/settled.jsonl,
    decisions.jsonl; data/expansion/karanog/README.md, section 6)."""
    out = {}
    for pack in sorted(p for p in second.iterdir() if p.is_dir()) if second.exists() else []:
        decisions = collections.defaultdict(list)
        for d in load(pack, "decisions.jsonl"):
            decisions[number(d["text"], part_ok=True)].append(d)
        objs = collections.defaultdict(list)
        for o in load(pack, "settled.jsonl"):
            if number(o.get("text")) is None or stray(o["reading"]):
                raise ValueError(f"{pack / 'settled.jsonl'}: {o.get('text')!r} names no inscription, or its reading holds "
                                 f"{stray(o['reading'])!r}: {o['reading']!r}")
            objs[number(o["text"])].append(o)
        out.update({n: (pack.name, os, decisions[n]) for n, os in objs.items()})
    return out


def rows(readings=None, refs=None, second=None):
    """One row per inscription, in Griffith's order."""
    readings = readings or KAR / "readings"
    refs = refs or KAR / "refs/by_inscription"
    again = twice(second or KAR / "second_reading")
    by_text = collections.defaultdict(lambda: {"final": [], "first": [], "kept": [], "unplaced": [], "pack": ""})
    for pack in sorted(p for p in readings.iterdir() if p.is_dir()):
        final = load(pack, "final.jsonl")
        if not final:
            continue                                   # a pack whose check is not done yet is left out
        for name, key in (("final.jsonl", "final"), ("copy_only.jsonl", "first"),
                          ("kept_against_type.jsonl", "kept"), ("unplaced.jsonl", "unplaced")):
            for o in load(pack, name):
                n = number(o.get("text"), part_ok=key in ("kept", "unplaced"))
                if n is None:                          # a reading that names no inscription would be lost
                    raise ValueError(f"{pack / name}: text {o.get('text')!r} is not 'Kar. N' or 'Sh. N' "
                                     f"(a part's letter goes in 'part')")
                if key in ("final", "first") and stray(o["reading"]):
                    raise ValueError(f"{pack / name}: the reading of {o['text']} holds {stray(o['reading'])!r}, "
                                     f"neither signs nor marks: {o['reading']!r}")
                by_text[n][key].append(o)
                by_text[n]["pack"] = pack.name
    entries_of = {n: entries(n[0], n[1], refs) for n in by_text}
    pairs = {n: phrases(es) for n, es in entries_of.items()}
    held = collections.Counter(p for ps in pairs.values() for p in ps)
    common = [p for p, k in held.items() if k >= EVERYWHERE]
    out = []
    for (site, no) in sorted(by_text, key=lambda k: (k[0] != "Kar", k[1])):
        t = by_text[(site, no)]
        checked, first = t["final"], t["first"]        # the first reader's reading after the check, and before it
        pack2, both, decided = again.get((site, no), ("", None, []))
        if both is not None and [(o["text"], o.get("part", "")) for o in both] != [(o["text"], o.get("part", "")) for o in checked]:
            raise ValueError(f"second_reading/{pack2}/settled.jsonl: the parts of {site}. {no} are not the first reader's")
        parts = checked if both is None else both      # read twice: the settled reading is the row's
        label = lambda o: f"{o['part']}: " if o.get("part") else ""
        std = " | ".join(label(o) + o["reading"].strip() for o in parts)
        es = entries_of[(site, no)]
        words, closed = joined([r for o in parts for r in runs(o["reading"])], whole(es, formula=True))
        own = whole(es)                                # a pair this inscription prints as one word is not parted
        words, parted = divided(words, pairs[(site, no)] + [(a, b) for a, b in common if a + b not in own])
        words, respelt = one_spelling(words)
        corpus = spell(words)
        sg = [s for o in parts for s in signs(o["reading"])]
        leaf = re.search(r"(\d+)", parts[0].get("page", ""))
        page = f"p. {int(leaf.group(1)) - 15} (leaf n{leaf.group(1)})" if leaf else ""
        caption = re.sub(r"^\s*(Kar|Sh)\.\s*\d+\.?\s*", "", parts[0].get("caption", "")).strip()
        paired = len(first) == len(checked) and all((a["text"], a.get("part")) == (b["text"], b.get("part"))
                                                    for a, b in zip(first, checked))
        diff = sum(changed(a["reading"], b["reading"]) for a, b in zip(first, checked)) if paired else None
        notes = [f"Read from Griffith's hand copy by Claude Opus 5.5 (pack {t['pack']}), then checked against the "
                 f"words he prints in type (names table, Indexes A to C, formula tables): {sum(o.get('entries') or 0 for o in checked)} "
                 f"printed entries placed" + (f", {diff} signs changed by the check" if diff is not None else "") + ".",
                 ACCURACY]
        if both is not None:
            took = collections.Counter(d.get("verdict") for d in decided)
            notes.append(f"Read a second time by another reader (second_reading/{pack2}): the two checked readings differed at "
                         f"{count(len(decided), 'place')}, which the second reader settled against the copy and the type, "
                         f"{took['first']} for the first reading, {took['second']} for the second, {took['other']} for neither and "
                         f"{took['open']} left open; "
                         f"{count(sum(changed(a['reading'], b['reading']) for a, b in zip(checked, parts)), 'sign')} "
                         f"of the first reader's row changed.")
        if len(parts) > 1:
            notes.append("Parts as labelled on the copy: " + "; ".join(
                f"{o.get('part') or '(main)'}" + (f" ({', '.join(o['labels'])})" if o.get("labels") else "") for o in parts) + ".")
        if t["kept"]:
            notes.append("Copy kept against the type: " + "; ".join(
                f"{k.get('copy', '')} (type: {k.get('type', '')})" for k in t["kept"]) + ".")
        if t["unplaced"]:
            notes.append("Printed entries not found in the copy: " + "; ".join(
                f"{u.get('reading', '')} ({u.get('source', '')})" for u in t["unplaced"]) + ".")
        uniform = [x for x in (
            closed and f"{count(closed, 'gap')} between words {'is' if closed == 1 else 'are'} closed where his formula tables print one word",
            parted and f"{parted} word {'boundary is' if parted == 1 else 'boundaries are'} Griffith's, from his formula tables",
            respelt and f"{count(respelt, 'word')} read slms {'is' if respelt == 1 else 'are'} written slẖs, as Griffith's shalkhash") if x]
        if uniform:
            notes.append("text_corpus differs from the reading: " + (", ".join(uniform[:-1]) + " and " if uniform[1:] else "")
                         + uniform[-1] + ".")
        notes += [o[k].strip() for k, objs in (("check_notes", checked), ("settled_notes", both or [])) for o in objs
                  if (o.get(k) or "").strip()]
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
