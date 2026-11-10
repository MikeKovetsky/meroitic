"""Turn a reading of a Newsletter text, or one of Otten's files, into a list of signs in one spelling.

One sign per item: the syllable signs are "se", "te", "to" and "N" (ne), the two h signs are "x" and "X",
"s" is the plain s sign. A word boundary is the item "|". Numerals and gap marks are left out.

need() is the check every tool makes first: its inputs stay on the author's machine.
"""
import difflib
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

SYLL = ("se", "te", "to", "ne")


def need(*paths):
    """Stop with a message, not a traceback, unless every path exists. The readers' typing, data/corpus_v3.jsonl
    and Otten's files are not in the public repo (README, Data)."""
    missing = [str(p) for p in paths if not Path(p).exists()]
    if missing:
        sys.exit(f"missing {', '.join(missing)}: the Newsletter readings, data/corpus_v3.jsonl and Otten's files are "
                 "kept locally, not in the public repo (README, Data; data/expansion/newsletter_reading.md)")


def tokens(plain):
    """Signs of a string already in plain letters (a-z, N, x, X) with spaces between words."""
    out = []
    for word in plain.split():
        i = 0
        while i < len(word):
            two = word[i:i + 2]
            if two in SYLL:
                out.append("N" if two == "ne" else two)
                i += 2
            else:
                out.append(word[i])
                i += 1
        out.append("|")
    return out


CONTINUED = r"^\s*[12]?\s*C\s*(?=[A-Z,(*@#./)])"   # the printout's continuation mark C, with a 1C/2C version mark
VERSION = r"\s*([1-9])\s*C?\s*(?=[A-Z(*@#.])"


def first_printing(lines):
    """Lines (page, inscription, segment, text) of the printout, in order. A segment printed in two or more
    versions (marked 1C and 2C, or by digits such as 1, 2, 3, or 3 and 2 where the scan lost the first) keeps the
    first one printed, with its mark taken off; a leading digit counts as a version mark only when lines of the
    segment begin with two or more different digits. A lone 2C is a second printing and goes. A line typed twice
    is kept once. The segment is a key: callers make it unique enough (inscription and segment, or page,
    inscription and segment)."""
    marks = defaultdict(set)
    for _, _, seg, text in lines:
        m = re.match(VERSION, text)
        if m:
            marks[seg].add(m.group(1))
    kept, seen, later, first = [], defaultdict(list), set(), {}
    for page, ident, seg, text in lines:
        m = re.match(VERSION, text) if len(marks[seg]) >= 2 else None
        lone_second = m is None and re.match(r"\s*2\s*C", text)
        body = text[m.end():] if m else re.sub(r"^\s*C\s*(?=[A-Z,(*@#.])", "", text)
        plain = re.sub(r"[^A-Z]", "", re.sub(r"\([^()]*\)|'[^']*'", "", body))
        if lone_second or (m and first.setdefault(seg, m.group(1)) != m.group(1)):
            later.add(seg)
            continue
        if m is None and seg in later:
            continue                                   # the rest of a later version
        if len(plain) >= 6 and any(_similar(plain, p) for p in seen[seg]):
            continue                                   # the same line typed twice
        seen[seg].append(plain)
        kept.append((page, ident, seg, body))
    return kept


def _similar(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() >= 0.8


def _balance(text):
    """The brackets made to match: one left open where the scan's edge cuts the line (>>), with no word divider
    on the way, closes there; one left open anywhere else is a slip of typing and goes, as does a ')' that
    closes nothing."""
    opened, drop, close_at = [], set(), defaultdict(int)
    for k, c in enumerate(text):
        if c == "(":
            opened.append(k)
        elif c == ")":
            if opened:
                opened.pop()
            else:
                drop.add(k)
    for k in opened:
        cut = text.find(">>", k)
        if cut < 0 or ",," in text[k:cut]:
            drop.add(k)
        else:
            close_at[cut] += 1
    return "".join(")" * close_at[k] + ("" if k in drop else c) for k, c in enumerate(text))


def first_reading(text):
    """Heyler's alternative readings, (A/B) or (A/B/C), reduced to the first, also where a reading holds
    brackets of its own, as in KB(T/(((D)))L)I. Other brackets (gaps, restored signs) stay. The scan's edge
    (>>) ends a word. Brackets are first made to match (_balance), so a reading cut off by the edge ends there
    and a mistyped one keeps all its letters, as typed. Returns the text and the number of places with
    alternatives."""
    done, stack, places = [], [], 0             # each open bracket: [first reading so far, seen '/', inside a later reading]
    text = _balance(text).replace(">>", " ")
    for c in text:
        if c == "(":
            stack.append([[], False, bool(stack) and (stack[-1][1] or stack[-1][2])])
        elif c == ")":
            if not stack:
                continue
            buf, alt, skip = stack.pop()
            if skip:
                continue
            places += alt
            (stack[-1][0] if stack else done).append("".join(buf) if alt else "(" + "".join(buf) + ")")
        elif c == "/" and stack and not stack[-1][2]:
            stack[-1][1] = True
        elif not stack:
            done.append(c)
        elif not (stack[-1][1] or stack[-1][2]):
            stack[-1][0].append(c)
    return "".join(done), places


def _depth(text):
    d = 0
    for c in text:
        d = d + 1 if c == "(" else max(0, d - 1) if c == ")" else d
    return d


def _closes(text, nxt):
    """Does the next line close the bracket the text leaves open?"""
    d = _depth(text)
    for c in nxt:
        d += (c == "(") - (c == ")")
        if d == 0:
            return True
    return False


def heyler_lines(texts):
    """Lines of Heyler's code in their printed order, with the continuation mark C and the analysis in
    apostrophes taken off and each alternative reading reduced to the first (first_reading). A line that leaves
    a reading open runs on into the next line when that line closes it (the two become one line); otherwise
    the bracket closes at the line's end. Returns [(text, places with alternatives)]."""
    clean = [re.sub(r"'[^']*'", "", re.sub(CONTINUED, "", t.strip())) for t in texts]
    out, k = [], 0
    while k < len(clean):
        t = clean[k]
        while _depth(t) and k + 1 < len(clean) and _closes(t, clean[k + 1]):
            k += 1
            t += clean[k]
        out.append(first_reading(t))
        k += 1
    return out


# Heyler's capitals that stand for another sign; every other capital is its own letter, lowered
HEYLER = {"S": "se", "Z": "s", "J": "N", "V": "te", "U": "to", "G": "x", "X": "X"}


def heyler(text, g="x", x="X"):
    """A text line in Heyler's capital-letter code (Newsletter 5 and 6), after heyler_lines(), to plain
    letters.

    Drops the doubt and gap marks, the stone's illegible dots and the tally numerals. '?' (reader unsure) is
    dropped, '#' (reader could not read) is kept as a sign. C is no letter of the code.
    """
    t = re.sub(r"[*()?.]", "", text)
    t = re.sub(r",{2,}", " ", t).replace(",", " ")
    t = re.sub(r"[0-9]+", " ", t)
    t = re.sub(r"[^A-Z# ]", "", t)
    table = {**HEYLER, "G": g, "X": x, "C": ""}
    return "".join(table.get(c, c.lower()) for c in t)


EITHER = re.compile(r"(\S+) (\S+) \(EIT[HX]ER-(\S+?)-OR-(\S+?)\)")


def _first_of_two(mo):
    """'ldr tdr (EITXER-LDR-OR-TDR)' is one word read two ways: keep the first, as src/corpus.py does."""
    a, b, x, y = mo.groups()
    return a if (a.lower(), b.lower()) == (x.lower(), y.lower()) else f"{a} {b}"


def fhn(text):
    """Otten's narrative files (FHN spelling: N, x, X, se) to plain letters. Where Otten gives a word two
    readings ("ldr tdr (EITXER-LDR-OR-TDR)") the first is kept, an alternative in brackets ([a|b]) gives its
    first letter, and the capitals of dotted (uncertain) letters are lowered, as src/corpus.py does."""
    t = "\n".join(l for l in text.splitlines() if not l.startswith("#"))
    t = EITHER.sub(_first_of_two, t)
    t = re.sub(r"\[([a-z])\|[^\]]*\]", r"\1", t)
    t = re.sub(r"\[[^\]]*\]", " ", t)
    t = re.sub(r"[0-9]+", " ", t)
    t = "".join(c.lower() if c.isupper() and c not in "NX" else c for c in t)
    return re.sub(r"[^a-zNxX\s]", "", t)


def millet_thesis(text):
    """Otten's Kalabsha_Millet.txt (E for o, s for se, S for s) to plain letters: the whole text as Millet
    transcribes it. The file then repeats parts of it, with his English translation after a tab; those are
    left out."""
    text = re.split(r"^# here are parts of the text", text, maxsplit=1, flags=re.M)[0]
    t = "\n".join(l.split("\t")[0] for l in text.splitlines() if not l.startswith("#"))
    t = re.sub(r"[0-9]+", " ", t).replace(":", " ")
    t = re.sub(r"[^a-zA-Z\s]", "", t)
    table = {"E": "o", "s": "se", "S": "s"}
    return "".join(table.get(c, c) for c in t)


def millet_2003(text):
    """Millet's spelling in Newsletter 30 (x for the first h sign, plain h for the second, ne, se) to plain letters."""
    t = re.sub(r"\{[0-9]+\}", "", text)
    t = unicodedata.normalize("NFC", t)
    t = t.replace("ñ", "N").replace("š", "s").replace("ḫ", "x").replace("ẖ", "X").replace("ê", "o")
    t = "".join(c for c in unicodedata.normalize("NFD", t) if not unicodedata.combining(c))   # doubt dots under a letter
    t = re.sub(r"[0-9]+", " ", t).replace(":", " ").replace("-", "").replace("|", " ")
    t = t.replace("h", "X")
    return re.sub(r"[^a-zNxX¤\s]", "", t)

