"""The check of the coverage map against two printed sources: Millet 2005 (Gebel Adda) and FHN III.

Local only. Reads the text layers in data/sources/jssea-text and data/sources/fhn-text (untrusted data: run with
python3 -I) and the corrected map in data/sources/coverage/corrected. Commands:

  match   which of the experts' entries are texts of our corpus, by shared runs of letters
  packs   the judges' packs (the experts' words beside our reading of each word), with unmarked decoys
"""
import collections
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MILLET = ROOT / "data/sources/jssea-text/pages.txt"
FHN = ROOT / "data/sources/fhn-text/pages.txt"
GLOSSES = ROOT / "data/sources/coverage/corrected/glosses.jsonl"
OUT = ROOT / "data/sources/expert"
FHN_OFFSET = 744                      # printed page = PDF page + 744
MILLET_PAGES = range(2, 68)           # the article, in PDF pages
FHN_ENTRIES = {                       # entry number: (first printed page, last printed page), from the contents
    "192": (837, 840), "246": (972, 974), "247": (974, 976), "264": (1018, 1020), "267": (1024, 1031),
    "268": (1031, 1034), "269": (1034, 1035), "270": (1035, 1038), "271": (1038, 1041), "277": (1050, 1052),
    "291": (1074, 1076), "300": (1103, 1107),
}
TRANSLATED = ("meaning", "grammar", "name", "number")
MASKED = ("NAME", "RNAME")
RUN = 5
SEED = 17
DECOYS = 0.10                         # share of the rows with a meaning whose reading is swapped for another's
PACKS = 3

# The experts' entries that are texts of our corpus. Chosen from `match` (shared runs of five letters, in both
# directions) and read side by side on 2026-11-12: at least half of each text's runs are in the other, or our
# text is a part of a longer entry (GA19, GA28), or a fragment read differently (GA47, GA56, FHN 271). Where the
# older corpus holds padded copies of a text, the copy with the highest score stands for it.
HELD = {
    "millet": {"GA04": "T0083", "GA07": "T0011", "GA19": "T0892", "GA20": "T0282", "GA21": "T0045",
               "GA22": "T0059", "GA24": "T0022", "GA25": "T0792", "GA28": "T0823", "GA29": "T0213",
               "GA30": "T0214", "GA31": "T0795", "GA37": "T0565", "GA39": "T0038", "GA41": "T0074",
               "GA42": "T0693", "GA46": "T0296", "GA47": "T0915", "GA53": "T0256", "GA54": "T0767",
               "GA55": "T0780", "GA56": "T1007", "GA57": "T0168"},
    "fhn": {"246": "G-mi2a-89", "247": "G-mi2a-88", "264": "G-karanog-78", "268": "G-karanog-47",
            "269": "G-karanog-77", "271": "T0818", "277": "G-meroe-7", "300": "kharamadoye"},
}


def pages(path):
    """{PDF page number: text} of a text layer written page by page."""
    out = {}
    for p in path.read_text(encoding="utf-8").split("\x0c=== page ")[1:]:
        n, _, body = p.partition(" ===\n")
        out[int(n)] = body
    return out


def millet_entries():
    """[(name, block)] of the article's headed entries, each block running to the next heading."""
    pg = pages(MILLET)
    body = "\n".join(pg[n] for n in MILLET_PAGES)
    body = body[:body.rfind("Table 1 - Gebel Adda")]
    heads = list(re.finditer(r"^(GA\s?\d+[a-z]?(?:\s?[&+]\s?(?:GA\s?)?\d+)*)\s*:", body, re.M))
    out = []
    for k, h in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else len(body)
        out.append((h.group(1).replace(" ", ""), body[h.start():end].strip()))
    return out


def millet_letters(block):
    """The letters of an entry's numbered lines of transliteration, in the reduced spelling."""
    cut = re.search(r"^(COMMENTARY|RENDERING)", block, re.M)
    part = block[:cut.start()] if cut else block
    lines = [re.sub(r"^\d{1,2}:\s*", "", l) for l in part.split("\n") if re.match(r"^\d{1,2}:\s", l)]
    return reduced_expert(" ".join(lines))


def fhn_entries():
    """[(number, block)] of the volume's entries on Meroitic texts, cut from the entry's heading to the next
    entry's heading on its pages."""
    pg = pages(FHN)
    out = []
    for number, (first, last) in FHN_ENTRIES.items():
        body = "\n".join(pg[p - FHN_OFFSET] for p in range(first, last + 1))
        start = re.search(r"^\(?%s\)? [A-Z]" % number, body, re.M)
        if not start:
            raise SystemExit(f"FHN {number}: heading not found on pages {first} to {last}")
        rest = body[start.start():]
        nxt = re.search(r"^\(?%d\)? [A-Z]" % (int(number) + 1), rest, re.M)
        out.append((number, rest[:nxt.start()].strip() if nxt else rest.strip()))
    return out


def fhn_letters(block):
    """The letters of an entry's section "Text", in the reduced spelling."""
    m = re.search(r"^Text\s*$(.*?)^Comments\s*$", block, re.M | re.S)
    if not m:
        return ""
    text = re.sub(r"\(\d+\)", " ", m.group(1))
    text = "\n".join(l for l in text.split("\n") if not re.match(r"^(Fontes Historiae|The Sources|\d+)\s*$", l))
    return reduced_expert(text)


def reduced_expert(s):
    """An expert's transliteration as bare letters: lower case, both h-signs as h, nothing but letters."""
    s = s.lower().replace("fi", "ne").replace("ñ", "ne").replace("x", "h")
    return re.sub(r"[^a-z]", "", s)


def reduced_ours(words):
    """Our corpus spelling in the same bare letters: the sign se as "se", the sign ne as "ne", both h-signs as h;
    masked names left out."""
    out = []
    for w in words:
        if w in MASKED:
            continue
        out.append(w.replace("s", "se").replace("S", "s").replace("N", "ne").replace("X", "h").replace("x", "h"))
    return re.sub(r"[^a-z]", "", "".join(out))


def runs(letters, n=RUN):
    return {letters[i:i + n] for i in range(len(letters) - n + 1)}


def glossed():
    return [json.loads(l) for l in GLOSSES.open(encoding="utf-8")]


def match(entries, letters_of, ours):
    """For each entry: (name, letters, [(share of its runs found, text id), best two])."""
    out = []
    for name, block in entries:
        letters = letters_of(block)
        g = runs(letters)
        best = sorted(((len(g & r) / len(g), i) for i, r in ours), reverse=True)[:2] if g else []
        out.append((name, letters, best))
    return out


def matches():
    rows = glossed()
    ours = [(r["id"], runs(reduced_ours(r["text"].split()))) for r in rows]
    return (match(millet_entries(), millet_letters, ours), match(fhn_entries(), fhn_letters, ours))


def blocks():
    """{(source, entry): the expert's words on it}. Millet's entries with one number are joined in the order of
    the article (GA55 and GA56 share a heading)."""
    out = collections.defaultdict(list)
    for name, block in millet_entries():
        for number in re.findall(r"GA\d+", name) + [f"GA{n}" for n in re.findall(r"[&+](\d+)", name)]:
            out["millet", number].append(block)
    for number, block in fhn_entries():
        out["fhn", number].append(block)
    return {k: clean("\n\n".join(v)) for k, v in out.items()}


def clean(text):
    """A text layer without the control characters a PDF leaves in it (they make a pack read as a binary file)."""
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f-\x9f\ufffd\ufeff]", " ", text)


def reading(g):
    """Our reading of a word as the judge sees it: the gloss, or a dash where the map has none."""
    if g["form"] in MASKED:
        return "(a personal name, masked in our copy)"
    if g["level"] in ("unknown", "lost") or not g.get("gloss"):
        return "—"
    return g["gloss"]


def rows_of():
    """Every word of the held texts as a row: id, source, entry, text, place, form, level, our reading. A masked
    name is a row without an id (shown, not judged)."""
    by_id = {r["id"]: r for r in glossed()}
    out = []
    for source, table in HELD.items():
        for entry, tid in table.items():
            n = 0
            for k, g in enumerate(by_id[tid]["glosses"]):
                judged = g["form"] not in MASKED and g["level"] != "lost"
                n += judged
                out.append({"row": f"{'M' if source == 'millet' else 'F'}{entry.replace('GA', '')}-{n:03d}"
                            if judged else None, "source": source, "entry": entry, "text": tid, "place": k,
                            "form": g["form"], "level": g["level"], "ours": reading(g),
                            "entry_of": [p["entry"] for p in g.get("parts", [])], "kind": g.get("kind", "")})
    return out


def with_decoys(rows):
    """The rows with a tenth of the readings that state a meaning swapped for the reading of another word of the
    same kind (a title for a title). Returns (rows, key): key[row id] = the reading we really hold."""
    rnd = random.Random(SEED)
    pool = collections.defaultdict(set)
    for r in glossed():
        for g in r["glosses"]:
            if g["level"] == "meaning" and g.get("gloss"):
                pool[g.get("kind", "")].add((tuple(p["entry"] for p in g.get("parts", [])), g["gloss"]))
    cand = [r for r in rows if r["row"] and r["level"] == "meaning"]
    chosen = set(x["row"] for x in rnd.sample(cand, round(len(cand) * DECOYS)))
    key, out = {}, []
    for r in rows:
        r = dict(r)
        if r["row"] in chosen:
            others = sorted(g for e, g in pool[r["kind"]] if e != tuple(r["entry_of"]) and g != r["ours"]
                            and g.split()[0] not in r["ours"])
            if others:
                key[r["row"]] = r["ours"]
                r["ours"] = rnd.choice(others)
        out.append(r)
    return out, key


INSTRUCTIONS = """# Pack {pack}: an expert's reading beside another reading of the same Meroitic texts

You are judging, word by word, whether two readings of the same inscription give a word the same meaning.

- **The expert** is the printed edition quoted in each section below: its transliteration, its commentary and,
  where it has one, its rendering into English. Sections marked "Millet 2005" come from N. B. Millet, "The
  Meroitic Inscriptions from Gebel Adda" (the text layer of a PDF: the dots under doubtful letters and some
  letters have fallen onto lines of their own; line numbers above 9 have lost their first digit). Sections marked
  "FHN III" come from Fontes Historiae Nubiorum III (an OCR of a scan: expect misread letters, "fi" or "ii" for
  the letter ñ, a mark like „ between words, line numbers as (3)); there the translation is inside the
  "Comments".
- **The other reading** is the table under each section: the words of the same inscription from another copy,
  in order, each with the reading that copy gives it. That copy spells differently: S is the sign s, s is the
  sign se, N is the sign ne, X is ẖ (Millet's h), x is ḫ (Millet's x). Its word division often differs from the
  expert's, personal names are masked, and some of its readings will be wrong or absent ("—").
- The expert's entry may hold more text than the table (a second inscription, a longer copy), or read some
  letters differently. Align by the letters.

For **every row that has a row id**, give one verdict:

- `agree`: the expert gives this word the same meaning as the table (the wording may differ; a name taken as
  the same kind of name, a title as the same title, a grammatical ending as the same function).
- `partly`: the two overlap but differ in a way that matters (kin term of another relation, a title of another
  rank, "perhaps" against a plain statement does NOT count: that is `agree` with doubt).
- `differ`: the expert gives the word a different meaning.
- `new`: the expert gives the word a meaning, and the table has none ("—") or only says what kind of word it is.
- `silent`: the word is in the expert's text, but the expert gives it no meaning (left in Meroitic, a gap in the
  rendering, "whatever that may mean", no rendering and no comment on it).
- `absent`: the word is not in the expert's text of this inscription, or cannot be aligned.

Judge only from what the expert prints here. Do not use your own knowledge of Meroitic to fill a gap: if the
expert does not render or explain the word, the verdict is `silent`, even when you know what it means. A word the
expert merely transliterates inside a translated sentence is `silent`.

Write your answers to the file `{answers}` as JSON lines, one line per row id, in the order of the tables,
nothing else in the file:

    {{"row": "M04-001", "verdict": "agree", "expert": "Isis (vocative)", "doubt": false}}

`expert` is the meaning the expert gives, in at most eight words, in English ("" for `silent` and `absent`).
`doubt` is true when the expert marks that meaning as unsure ("?", "perhaps", "I take it to be", italics of
doubt). Every row id of this pack must appear exactly once. Rows without a row id are masked names: skip them.

Read only this file. Do not open other files in the repository, do not search the web. When the file is
written, reply with one line: the number of rows you wrote and anything in the pack that could not be judged.

"""


def packs(out=OUT):
    """Write the packs, the key of the decoys and the table of rows. Refuses to write over a folder that already
    holds a judge's answers."""
    folder = out / "packs"
    if any(out.glob("answers/*.jsonl")):
        raise SystemExit(f"{out}/answers holds judges' answers: not writing the packs again")
    folder.mkdir(parents=True, exist_ok=True)
    rows, key = with_decoys(rows_of())
    text = blocks()
    order = sorted({(r["source"], r["entry"]) for r in rows},
                   key=lambda k: -sum(1 for r in rows if (r["source"], r["entry"]) == k and r["row"]))
    load, where = [0] * PACKS, {}
    for k in order:                                        # largest first, each into the lightest pack
        i = load.index(min(load))
        where[k] = i
        load[i] += sum(1 for r in rows if (r["source"], r["entry"]) == k and r["row"])
    for i in range(PACKS):
        name = "ABCDEFGH"[i]
        for judge in (1, 2):
            parts = [INSTRUCTIONS.format(pack=name, answers=f"data/sources/expert/answers/judge{judge}_{name}.jsonl")]
            for k in sorted((k for k in where if where[k] == i), key=lambda k: (k[0], int(re.sub(r"\D", "", k[1])))):
                label = "Millet 2005" if k[0] == "millet" else "FHN III"
                parts.append(f"\n---\n\n## {label}, entry {k[1]}\n\n### The expert\n\n```\n{text[k]}\n```\n\n"
                             f"### The other reading\n\n| row id | word | its reading |\n|---|---|---|\n")
                for r in rows:
                    if (r["source"], r["entry"]) == k:
                        parts.append(f"| {r['row'] or ''} | {r['form']} | {r['ours'].replace('|', '/')} |\n")
            (folder / f"judge{judge}_{name}.md").write_text("".join(parts), encoding="utf-8")
    (out / "answers").mkdir(exist_ok=True)
    (out / "rows.jsonl").write_text("".join(json.dumps({**r, "pack": "ABCDEFGH"[where[r["source"], r["entry"]]],
                                                        "decoy": r["row"] in key, "really": key.get(r["row"])},
                                                       ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    judged = [r for r in rows if r["row"]]
    print("texts:", len(order), "| rows judged:", len(judged), "| per pack:", load, "| decoys:", len(key))
    print("levels of the judged rows:", dict(collections.Counter(r["level"] for r in judged)))
    for i in range(PACKS):
        f = folder / f"judge1_{'ABCDEFGH'[i]}.md"
        print(f.name, f.stat().st_size, "bytes")


EXTRA = """# Meanings an expert gives to Meroitic words: a list from two printed editions

Below are sections of two printed editions of Meroitic inscriptions. Sections marked "Millet 2005" come from
N. B. Millet, "The Meroitic Inscriptions from Gebel Adda" (the text layer of a PDF: the dots under doubtful
letters and some letters have fallen onto lines of their own). Sections marked "FHN III" come from Fontes
Historiae Nubiorum III (an OCR of a scan: expect misread letters, "fi" or "ii" for the letter ñ, a mark like „
between words); there the translation is inside the "Comments".

List **every Meroitic word, ending or fixed phrase to which the expert gives a meaning** in these sections: in a
rendering, in a commentary, or in passing about a word of another inscription. Include meanings the expert only
proposes, and mark them. Leave out words the expert only transliterates, personal names taken simply as names,
and place names taken simply as places. Use only what is printed here, not your own knowledge of Meroitic.

Write the list to the file `data/sources/expert/answers/extractor.jsonl` as JSON lines, nothing else in the file:

    {{"source": "Millet 2005", "entry": "GA06", "word": "penn", "meaning": "year", "doubt": true, "quote": "the word penn may mean year"}}

`word` is the Meroitic word as the expert spells it (in Millet x is ḫ and h is ẖ); `meaning` has at most ten
words; `doubt` is true when the expert marks the meaning as unsure; `quote` is at most fifteen words of the
expert's own that show it. One line per word and entry; the same word in two entries gets two lines.

Read only this file. Do not open other files in the repository, do not search the web. When the file is written,
reply with one line: how many lines you wrote.

"""
FHN_EXTRA = ("192", "267", "270", "291")
FHN_NOTE = (762, 764)                 # "A General Note to the Meroitic Texts", printed pages


def extra(out=OUT):
    """The pack of everything not held in our corpus, for a list of the meanings the experts give there."""
    held = set(HELD["millet"])
    parts = [EXTRA]
    pg = pages(MILLET)
    intro = "\n".join(pg[n] for n in MILLET_PAGES)
    intro = intro[:re.search(r"^GA\s?\d+", intro, re.M).start()]
    parts.append(f"\n---\n\n## Millet 2005, introduction\n\n```\n{clean(intro).strip()}\n```\n")
    n = 0
    for name, block in millet_entries():
        if not (set(re.findall(r"GA\d+", name)) & held):
            parts.append(f"\n---\n\n## Millet 2005, entry {name}\n\n```\n{clean(block)}\n```\n")
            n += 1
    fp = pages(FHN)
    note = "\n".join(fp[p - FHN_OFFSET] for p in range(FHN_NOTE[0], FHN_NOTE[1] + 1))
    parts.append(f"\n---\n\n## FHN III, a general note to the Meroitic texts\n\n```\n{clean(note).strip()}\n```\n")
    for number, block in fhn_entries():
        if number in FHN_EXTRA:
            parts.append(f"\n---\n\n## FHN III, entry {number}\n\n```\n{clean(block)}\n```\n")
    f = out / "packs" / "extractor.md"
    f.write_text("".join(parts), encoding="utf-8")
    print(f.name, f.stat().st_size, "bytes |", n, "entries of Millet not held,", len(FHN_EXTRA), "of FHN")


def main(argv):
    if argv[1:] == ["packs"]:
        return packs()
    if argv[1:] == ["extra"]:
        return extra()
    if argv[1:] == ["match"]:
        for label, found in zip(("Millet 2005", "FHN III"), matches()):
            print(label)
            for name, letters, best in found:
                shown = "  ".join(f"{s:.2f} {i}" for s, i in best)
                print(f"  {name:12} {len(letters):4} letters   {shown}")
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
