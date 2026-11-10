"""Build the local-only file of texts typed from the Meroitic Newsletter scans.

  python3 -I mnl_build.py <repo root> <harvest dir> <out.jsonl>

Reads the readers' raw files (harvest/M*/out/texts.jsonl for the issues of 1977-2003, harvest/P*/out/reading.txt
and harvest/T*/out/reading.txt for the 1971 printout), and writes one row per text and edition:

  id, rem, source, file, pdf_page, printed_page, site, object, complete, kind ("printout" or "print"),
  lines (as typed from the page), text_corpus (the corpus spelling: s = the se sign, S = plain s, N = ne,
  x and X the two h signs, o; lost signs as dots), round_letters (printout only: how many look-alike
  O/Q/D letters were settled by the reader's choice, by a spelling rule, by a corpus word, by the model),
  line_ends, spelling, has_translation, notes, words, broken_words.

It also reads data/corpus_v3.jsonl and the page lists in data/sources/mnl/readings/inventory/, and stops with a
message when one of them is absent (they are kept locally: README, Data).

Nothing here is checked against a second edition except where the test report says so.
"""
import json, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mnl_round as R  # noqa: E402
import mnl_signs as S  # noqa: E402

ISSUE = {"MeroNews6": "Meroitic Newsletter 6 (1971)", "MeroNews18": "Meroitic Newsletter 18 (1977)",
         "MeroNews21": "Meroitic Newsletter 21 (1980)", "MeroNews22": "Meroitic Newsletter 22 (1982)",
         "MeroNews25b": "Meroitic Newsletter 25 (1994)", "MeroNews26a": "Meroitic Newsletter 26 (1999)",
         "MeroNews27c": "Meroitic Newsletter 27 (2000)", "MeroNews27d": "Meroitic Newsletter 27 (2000)",
         "MeroNews27e": "Meroitic Newsletter 27 (2000)", "MeroNews28": "Meroitic Newsletter 28 (2001)",
         "MeroNews29c": "Meroitic Newsletter 29 (2002)", "MeroNews29d": "Meroitic Newsletter 29 (2002)",
         "MeroNews29e": "Meroitic Newsletter 29 (2002)", "MeroNews30d": "Meroitic Newsletter 30 (2003)",
         "MeroNews30e": "Meroitic Newsletter 30 (2003)"}
LOST = "…"          # one lost stretch of unknown length, inside the working text
PAREN_RESTORES = {"MeroNews18", "MeroNews21", "MeroNews22"}   # the typewritten issues put the editor's restorations in round brackets


# ---------------------------------------------------------------- the printed issues (1977-2003)

def strip_line_numbers(lines):
    """Take the edition's own line numbers off the front of the lines."""
    marked = r"^\s*(?:\(?(?:x\s*\+\s*)?\d+\)?\s*[).:\-–]\s+|\(?(?:x\s*\+\s*)?\d+\)\s*|\((?:x\s*\+\s*)?\d+\)\s*)"
    xplus = r"^\s*x\s*\+\s*(\d+)\s*(?![\d)])"                                                       # x+3 with no bracket
    lines = [re.sub(r"^\s*lignes?\s+\d+\s*:\s*", "", l, flags=re.I) for l in lines]
    lines = [re.sub(r"^\s*\((?:r|v|recto|verso)\)\s*(?=\d)", "", l) for l in lines]                    # a side label before the number: (r) 1
    first = re.match(xplus, lines[0], flags=re.I) if lines else None
    lines = [re.sub(xplus, "", l, flags=re.I) for l in lines]
    if first:                                            # x+1, then the bare numbers count on: 2, 3 ...
        lines = lines[:1] + [re.sub(r"^\s*%d\s+(?=\S)" % (int(first.group(1)) + k), "", l) for k, l in enumerate(lines[1:], 1)]
    lines = [re.sub(r"^\s*%d\s+(?=\S)" % (i + 1), "", l) if len(lines) >= 4 else l for i, l in enumerate(lines)]   # a bare number that is the line's own place (often only every fifth line)
    out = [re.sub(marked, "", l, count=1) for l in lines]
    if out == list(lines):                               # bare numbers: only when they count up line by line (from 1, in a text of one line)
        nums = [re.match(r"\s*(\d+)\s+\S", l) for l in lines]
        if lines and all(nums):
            n = [int(m.group(1)) for m in nums]
            if (len(lines) >= 2 or n[0] == 1) and n == list(range(n[0], n[0] + len(lines))):
                out = [re.sub(r"^\s*\d+\s+", "", l) for l in lines]
    return out


def clean_print(line, millet_h=False, restored_in_parens=False):
    """One printed line to working letters: lower case, dividers as ' : ', a lost stretch as LOST (touching the
    word it breaks, as printed). Restored signs keep their letters, in square brackets and, where the edition
    puts them there (restored_in_parens), in round ones; other round brackets hold the editor's notes. A sign
    no one could read (the reader's ¤, the edition's raised dot ·) is a lost sign; a non-alphabetic sign the
    reader typed as □ ends a word."""
    t = unicodedata.normalize("NFC", line)
    t = re.sub(r"\{\d+\}|[①-⑳㉑-㉟]", "", t)        # the stone's line numbers set inside the text
    t = t.replace("ᵉ", "e").replace("ᵒ", "o")              # raised e and o of the syllable signs
    t = re.sub(r"◁[^▷]*▷", " ", t)                    # a demotic passage between triangles
    t = re.sub(r"\S*[Ḥḥ]\S*", " ", t)                       # an Egyptian word (h with a dot)
    t = t.replace("[--]", "")                                        # a flaw in the stone, no sign lost
    t = re.sub(r"\btraces\b", LOST, t)                               # the editor's "traces"
    t = re.sub(r"\[\s*ca\.?[^\]]*\]", LOST, t)                       # [ca. 5]
    t = re.sub(r"\bca\.?\s*\d+(\s*\?)?|\d+\s*letters?|\d+(-\d+)?\s*\?(?=\s*[\]:])", LOST, t)   # a count of lost signs inside a restoration
    t = re.sub(r"\[\s*[.… ]*\s*\]", LOST, t)                    # [...] and [.]
    t = re.sub(r"\[([^\]\s]+) ou [^\]]*\]", r"\1", t)                # [k ou p]: the first
    if restored_in_parens:
        t = t.replace("(", "").replace(")", "")                      # the editor's restorations: their letters stay, as in [ ]
    t = re.sub(r"\((?:[^()]*)\)", "", t)                             # the editor's notes and footnote calls
    t = re.sub(r"\[([^\]/]+)/[^\]]*\]", r"\1", t)                   # [se/y]: the first
    t = re.sub(r"⌝\s+\[(?=[^\W\d])", "[", t)                   # a half-kept sign and its restored neighbour are one word
    t = re.sub(r"(?<=[^\W\d])\]\s+⌜", "]⌜", t)
    t = t.replace("¤", ".").replace("·", ".").replace("□", " ")   # the reader's unread sign, the edition's unidentified one, a non-alphabetic sign
    t = re.sub(r"[\[\]⌜⌝⌞⌟⸢⸣⌈⌉<>?!|#¿†'’°]", "", t)
    t = re.sub(r"\.{2,}|…+", LOST, t)                       # dots for a lost stretch
    t = t.replace(",,", " : ").replace(":", " : ").replace("-", "").replace("+", " ").replace("=", " ")
    t = t.lower()
    t = unicodedata.normalize("NFD", t)
    t = re.sub(r"ḥ?[̱̲̠]", "X", t)          # h with a line below (a dot below it or not): the second h sign
    t = re.sub(r"ḥ?[̮̰̯]", "x", t)          # h with a curve below: the first h sign
    t = re.sub(r"ṇ?̃", "N", t)                        # n with a tilde: the ne sign
    t = re.sub(r"ṣ?̌", "š", t)                   # s with a caron stays one letter
    t = re.sub(r"ẹ?̂", "o", t)                        # e with a circumflex: o
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("ḫ", "x").replace("ẖ", "X")
    if millet_h:
        t = t.replace("h", "X")
    t = re.sub(rf"[^a-zNxXš.0-9: {LOST}]", " ", t)
    toks = [w for w in t.replace(":", " ").split() if re.fullmatch(r"[a-zNxXš]+", w)]
    if len(toks) >= 5 and sum(len(w) <= 2 for w in toks) / len(toks) >= 0.8:       # the edition prints the signs apart: a word ends only at a divider
        t = " : ".join(re.sub(r"(?<=[a-zNxXš.{LOST}])\s+(?=[a-zNxXš.{LOST}])".replace("{LOST}", LOST), "", g) for g in t.split(":"))
    t = re.sub(r"(?<=[a-zNxXš])(?=[0-9])|(?<=[0-9])(?=[a-zNxXš])", " ", t)   # a numeral is its own word
    return re.sub(rf"{LOST}(\s*{LOST})+", LOST, t)


def to_corpus(working, old_s=False):
    """Working letters to the corpus spelling. old_s: the edition writes s for the se sign and š for plain s."""
    out = []
    for w in working.split():
        if re.fullmatch(r"[0-9.]+", w) and re.search(r"[0-9]", w):
            out.append(w)
            continue
        if old_s:
            w = w.replace("s", "ß").replace("š", "S").replace("ß", "s")
        else:
            w = w.replace("se", "ß").replace("š", "s").replace("s", "S").replace("ß", "s")
        out.append(w.replace("ne", "N").replace(LOST, "..."))
    return " ".join(out)


def runs_on(model, left, right):
    """Does the word at a line's end run on into the next line? Yes only when the two halves together are a
    word of the corpus and at least one half alone is not. None when a half is broken or a numeral."""
    if not re.fullmatch(r"[a-zNxX]+", left) or not re.fullmatch(r"[a-zNxX]+", right):
        return None
    sign = lambda w: tuple(t for t in S.tokens(w) if t != "|")
    return sign(left + right) in model.word and not (sign(left) in model.word and sign(right) in model.word)


def print_row(model, r):
    raw = r["lines"]
    inline = any(re.search(r"[①-⑳㉑-㉟]|\{\d+\}", l) for l in raw)
    colon = any(":" in l for l in raw)
    old_s = any("š" in unicodedata.normalize("NFC", l) for l in raw)
    lines = [clean_print(l, r["file"] == "MeroNews30e", r["file"] in PAREN_RESTORES).strip() for l in strip_line_numbers(raw)]
    check = colon and not inline and not old_s           # old_s: the corpus model cannot read the old spelling
    parts, asked, joined = [], 0, 0
    for l in lines:
        if not l:
            continue
        if parts and check and not parts[-1].endswith(":") and not l.startswith(":"):
            verdict = runs_on(model, parts[-1].split()[-1], l.split()[0])
            if verdict is not None:
                asked += 1
            if verdict:
                joined += 1
                parts[-1] += l
                continue
        parts.append(l)
    text = to_corpus(" ".join(parts).replace(":", " "), old_s)
    if inline:
        ends = "the print runs on with the stone's line numbers set in: printed line ends taken as word ends"
    elif check:
        ends = (f"{asked} line ends have no divider: {joined} joined to the next line because the two halves make a corpus word, "
                f"{asked - joined} taken as word ends")
    else:
        ends = "line ends taken as word ends"
    return text, ends


# ---------------------------------------------------------------- the 1971 printout

def printout_items(text):
    """A text line of the printout, after mnl_signs.heyler_lines(), to items: ("w", [(sign, label)]),
    ("n", digits) or ("gap", "...")."""
    t = re.sub(r"\(\(\s*\)\)", "~", text)                            # (()) a gap of unknown length, touching what it breaks
    t = re.sub(r"[*()]", "", t)
    t = re.sub(r",{2,}", " ", t).replace(",", " ")
    items = []
    for chunk in t.split():
        if re.fullmatch(r"~+", chunk):
            items.append(("gap", "..."))
        elif re.fullmatch(r"[0-9?]+", chunk):
            if re.search(r"[0-9]", chunk):                           # a lone ? is a doubt about nothing typed
                items.append(("n", chunk.replace("?", "")))
        else:
            w = []
            for m in re.finditer(r"([A-Z#@.~])(\?)?|([0-9]+)", chunk):
                if m.group(3):
                    if w:
                        items.append(("w", w)); w = []
                    items.append(("n", m.group(3)))
                    continue
                ch, mark = m.group(1), m.group(2) or ""
                if ch in "OQD@":
                    w.append(("0", "@" if ch == "@" else ch + mark))
                elif ch == "~":
                    w.append(("...", None))
                elif ch in "#.F":                      # unread, illegible on the stone, or Heyler's F (a sign of unknown value)
                    w.append((".", None))
                elif ch == "C":                        # not a letter of the code: a stray continuation mark
                    continue
                else:
                    w.append((S.HEYLER.get(ch, ch.lower()), None))
            if w:
                items.append(("w", w))
    return items


CORPUS_SIGN = {"se": "s", "s": "S"}


def printout_text(model, lines):
    """The printout's lines of one text to the corpus spelling. Returns the text, how its round letters were
    settled, the places with alternative readings, and how many line ends a bracket ran over."""
    out, how, alts = [], Counter(), 0
    resolved = S.heyler_lines(lines)
    for line, a in resolved:
        alts += a
        for kind, val in printout_items(line):
            if kind == "w":
                signs, hows = R.settle(model, val)
                how.update(h for _, _, h, _ in hows)
                out.append("".join(CORPUS_SIGN.get(s, s) for s in signs))
            else:
                out.append(val)
    return " ".join(out), dict(how), alts, len(lines) - len(resolved)


def read_printout(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        parts = [p.strip() for p in line.split("|", 3)]
        if len(parts) == 4 and re.fullmatch(r"p\d+", parts[0]):
            rows.append(parts)
    return rows


def group_printout(rows):
    """Lines to texts: one text per inscription number (its parts A, B, C in order)."""
    texts, order = defaultdict(list), []
    last, last_seg, unknown = None, 0, 0
    for page, ident, seg, text in rows:
        num = re.sub(r"[~?\s]", "", ident)
        m = re.match(r"(\d{4})([A-Z]?)", num)
        seg_n = int(re.sub(r"\D", "", seg) or 0)
        if m:
            key = m.group(1)
        elif last is not None and seg_n >= last_seg:
            key = last                                  # number cut off, the segment count runs on
        else:
            unknown += 1
            key = f"unknown-{page}-{unknown}"
        if key not in texts:
            order.append(key)
        texts[key].append((page, ident, seg, text))
        last, last_seg = key, seg_n
    return [(k, texts[k]) for k in order]


# ---------------------------------------------------------------- main

def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    ROOT, HARVEST, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    inventory = [ROOT / f"data/sources/mnl/readings/inventory/{L}.json" for L in "ABCD"]
    S.need(ROOT / "data/corpus_v3.jsonl", HARVEST, *inventory)
    printed, printout = sorted(HARVEST.glob("M*/out/texts.jsonl")), sorted(HARVEST.glob("[PT]*/out/reading.txt"))
    if not printed and not printout:
        sys.exit(f"no readings in {HARVEST}: it should hold M*/out/texts.jsonl, P*/out/reading.txt or T*/out/reading.txt")
    inv = {}
    for path in inventory:
        for t in json.loads(path.read_text())["texts"]:
            m = re.search(r"REM\s*(\d{4})", str(t["id"]))
            if m and "MeroNews6" in str(t["file"]):
                inv.setdefault(m.group(1), t)
    model = R.Model(R.corpus_words(ROOT))
    out = []
    for path in printed:
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            text, ends = print_row(model, r)
            m = re.search(r"REM\s*(\d{4}[A-Z]?(?:-\d+)?)", r["id"])
            out.append({"id": r["id"], "rem": m.group(1) if m else "", "source": ISSUE.get(r["file"], r["file"]), "file": r["file"],
                        "pdf_page": r["pdf_page"], "printed_page": r.get("printed_page", ""), "site": r.get("site", ""),
                        "object": r.get("object", ""), "complete": r.get("complete", ""), "kind": "print",
                        "lines": r["lines"], "text_corpus": text, "line_ends": ends, "spelling": r.get("spelling", ""),
                        "has_translation": r.get("has_translation", False), "notes": r.get("notes", "")})
    rows = []
    for path in printout:
        rows += read_printout(path)
    rows.sort(key=lambda p: int(p[0][1:]))                 # stable: page order, the readers' order within a page
    for key, lines in group_printout(rows):
        lines = S.first_printing([(p, i, f"{re.sub(r'[~?]', '', i)}/{g}", t) for p, i, g, t in lines])
        if not lines:
            continue
        quick = all(23 <= int(l[0][1:]) <= 30 for l in lines)       # typed by the quick test reader
        R.PRIOR.clear(); R.PRIOR.update(R.QUICK if quick else R.CAREFUL)
        text, how, alts, ran_over = printout_text(model, [l[3] for l in lines])
        t = inv.get(key, {})
        worked_out = any(l[1].startswith("~") or "?" in l[1] for l in lines)
        notes = []
        if worked_out:
            notes.append("the inscription number is cut off on some or all of its lines and was worked out from the order of the printout")
        if quick:
            notes.append("typed in the first test without enlarging: its round letters (O, Q, D) are mostly settled by the model, not seen")
        if alts:
            notes.append(f"{alts} places where the printout gives alternative readings: the first is taken")
        cut = sum(l[3].count(">>") for l in lines)
        if cut:
            notes.append(f"{cut} lines run into the scan's edge")
        out.append({"id": f"REM {key}" if key.isdigit() else f"MNL 6, {key}", "rem": key if key.isdigit() else "",
                    "source": ISSUE["MeroNews6"], "file": "MeroNews6", "pdf_page": int(lines[0][0][1:]), "printed_page": "",
                    "site": t.get("site", ""), "object": t.get("object", ""), "complete": t.get("complete", ""), "kind": "printout",
                    "lines": [f"{l[1]} | {l[2]} | {l[3]}" for l in lines], "text_corpus": text, "round_letters": how,
                    "line_ends": "taken as word ends" + (f", except {ran_over} where a bracket runs over into the next line" if ran_over else ""),
                    "spelling": "Heyler's capital-letter computer code", "has_translation": False,
                    "notes": "; ".join(notes)})
    for r in out:
        toks = [w for w in r["text_corpus"].split() if re.search(r"[a-zNxXS]", w)]
        r["words"] = len([w for w in toks if "." not in w])
        r["broken_words"] = len(toks) - r["words"]
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    by = Counter(r["file"] for r in out)
    print(f"{len(out)} rows, {sum(r['words'] for r in out)} words")
    for f in sorted(by):
        print(f"  {f}: {by[f]} texts, {sum(r['words'] for r in out if r['file'] == f)} words")


if __name__ == "__main__":
    main()
