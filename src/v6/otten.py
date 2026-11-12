"""The older corpus traced back to the lines it was padded from.

Otten's mero-corpus.txt (18,090 lines) is his per-scholar example files with one name swapped per line: every
line of the padded file is a line of Data/MilletExamples.txt, RillyExamples.txt, LobbanVocabList.txt or
Kalabsha_Millet.txt, or such a line with one stretch (a name) replaced by another name. The per-scholar files
hold what the padded file lost: the real names, Millet's brackets and dividers, his translation where he gives
one, and the page of his 1968 thesis. This module reads those source lines, says which source line each raw line
and each text of corpus_v5 comes from, and writes a source line in the spelling of corpus_v6.

Local only: data/otten/ has no licence and data/corpus_v5.jsonl is built from it (README, Data).

  python3 -I src/v6/otten.py        the counts: source lines, raw lines by how they derive, texts traced
"""
import collections
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import clean_v2 as V   # noqa: E402
import corpus as C     # noqa: E402

DATA = ROOT / "data/otten/Data"
PADDED = DATA / "mero-corpus.txt"
POOLS = ROOT / "data/name_pools.json"          # written by src/dedup.py (local)
V5 = ROOT / "data/corpus_v5.jsonl"
FILES = ("MilletExamples.txt", "RillyExamples.txt", "LobbanVocabList.txt", "Kalabsha_Millet.txt")
WORKS = {"MilletExamples.txt": "Millet 1968, Meroitic Nubia (thesis), as typed by Otten",
         "Kalabsha_Millet.txt": "Millet 1968, Meroitic Nubia (thesis), as typed by Otten",
         "RillyExamples.txt": "Rilly 2007, as typed by Otten",
         "LobbanVocabList.txt": "Lobban's word list, as typed by Otten"}
AUTHOR = {"MilletExamples.txt": "Millet 1968", "Kalabsha_Millet.txt": "Millet 1968", "RillyExamples.txt": "Rilly 2007",
          "LobbanVocabList.txt": "Lobban"}
ANALYSIS = "same as line above"   # Otten's note over a line that gives the line above segmented (MilletExamples 979)
NARRATIVES = C.NARRATIVES                      # {corpus id: file}: the three royal texts, each a file of its own
SWAP = 25          # a swapped name is at most this many letters (the longest of Otten's is 18)
SHARED = 3         # a raw line derives from a source line by a swap when they share this many letters around it
NEAR = 0.8         # ... or, failing that, when the two are this alike letter for letter


def key(s):
    """The letters and digits of a line, for comparing Otten's files with each other: his padded file drops the
    brackets, dividers and hyphens of the per-scholar files."""
    return re.sub(r"[^A-Za-z0-9]", "", re.sub(r"\(EIT[HX]ER.*?\)", "", s))


def source_lines(folder=DATA, files=FILES):
    """[{key, file, line, page, section, mero, translation, tag, note}] of the per-scholar files: every line that
    is not a comment, with the page note ("# pg. 114") and the section heading that stand above it, and the
    comment on the line just above it, if any (note: "same as line above, but with segmentation ...")."""
    out = []
    for fn in files:
        page = section = note = ""
        for n, line in enumerate((folder / fn).read_text(errors="replace").split("\n"), 1):
            if not line.strip():
                note = ""
                continue
            if line.startswith("#"):
                m = re.match(r"#\s*pg\.?\s*([\d/\-, ]*\d)", line)
                if m:
                    page = m.group(1).strip()
                if "UNTRANSLATED" in line:
                    section = "untranslated"
                elif "TRANSLATED" in line:
                    section = "translated"
                note = "" if m else line.lstrip("#").strip()
                continue
            cells = [c.strip() for c in line.split("\t")]
            above, note = note, ""
            if not key(cells[0]):
                continue
            out.append({"key": f"{fn}:{n}", "file": fn, "line": n, "page": page, "section": section,
                        "mero": cells[0], "translation": cells[1] if len(cells) > 1 else "",
                        "tag": cells[2] if len(cells) > 2 else "", "note": above})
    return out


def is_analysis(line):
    """A line that Otten's note marks as the line above in an analysis (segmented, t written s and l): not a
    reading of the stone."""
    return (line.get("note") or "").lower().startswith(ANALYSIS)


def label(line):
    """The name of a text known only from a source line: its author and the page or line ("Millet 1968 p. 362-364
    (MilletExamples.txt line 489)")."""
    return f"{AUTHOR[line['file']]} p. {line['page'] or '?'} ({line['file']} line {line['line']})"


def spellings(line):
    """The spellings a source line gives: one, or several divided by ";" (a word list's variants, a phrase with
    and without hyphens)."""
    return [s for s in line["mero"].split(";") if key(s)]


def raw_lines(path=PADDED):
    """The different lines of the padded file, in its order."""
    return list(dict.fromkeys(l.strip() for l in path.read_text().split("\n") if l.strip()))


def _lcp(a, b):
    n, i = min(len(a), len(b)), 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def derive(raws, lines):
    """{raw line: (source key, how, was, now, share)} for each raw line that comes from a source line.

    how is "equal" (the same letters), "swap" (the same but for one stretch: `was` in the source line, `now` in
    the raw line, each at most SWAP letters, with SHARED letters or more around it) or "near" (the best source line
    by letters, at NEAR or more: a swap and a second, small difference). A raw line that fits none is left out.
    Among several source lines the one with the smallest swap wins, then the one that shares most, then the first
    in the files."""
    keys = collections.OrderedDict()
    for l in lines:
        for s in spellings(l):
            keys.setdefault(key(s), l["key"])
    first, last = collections.defaultdict(list), collections.defaultdict(list)
    grams = collections.defaultdict(set)
    for k in keys:
        first[k[:SHARED]].append(k)
        last[k[-SHARED:]].append(k)
        for i in range(len(k) - 3):
            grams[k[i:i + 4]].add(k)
    out = {}
    for raw in raws:
        k = key(raw)
        if k in keys:
            out[raw] = (keys[k], "equal", "", "", 1.0)
            continue
        best = None
        for c in dict.fromkeys(first[k[:SHARED]] + last[k[-SHARED:]]):
            p = _lcp(k, c)
            s = min(_lcp(k[::-1], c[::-1]), len(k) - p, len(c) - p)
            was, now = c[p:len(c) - s], k[p:len(k) - s]
            if p + s >= SHARED and max(len(was), len(now)) <= SWAP:
                rank = (len(was) + len(now), -(p + s))
                if best is None or rank < best[0]:
                    best = (rank, c, was, now)
        if best:
            _, c, was, now = best
            out[raw] = (keys[c], "swap", was, now, round((len(c) - len(was)) / max(len(c), 1), 3))
            continue
        cands = collections.Counter(c for i in range(len(k) - 3) for c in grams.get(k[i:i + 4], ()))
        near = max(((difflib.SequenceMatcher(None, k, c, autojunk=False).ratio(), c) for c, _ in cands.most_common(5)),
                   default=(0.0, ""))
        if near[0] >= NEAR:
            out[raw] = (keys[near[1]], "near", "", "", round(near[0], 3))
    return out


def pools(path=POOLS):
    p = json.loads(path.read_text())
    return set(p["private"]), set(p["royal"])


def v5_text(raw, private, royal):
    """The text a raw line becomes in the older corpus: names of the two pools masked (src/dedup.py), the corpus
    spelling (src/corpus.py), the names of several words masked (src/clean_v2.py)."""
    line = re.sub(r"\s+", " ", raw.replace(".", " ")).strip()
    sk = " ".join("NAME" if w in private else "RNAME" if w in royal else w for w in line.split())
    t = C.norm(sk.replace("RNAME", "\1").replace("NAME", "\0")).replace("\0", "NAME").replace("\1", "RNAME")
    t = V.mask(t, V.SAFE)
    return V.mask(t, V.FILLERS) if len(t.split()) <= 8 else t


def trace(rows, raws, private, royal):
    """{id of a text of the older corpus: [its raw lines]}: the raw lines whose masked text is the text. The raw
    lines that src/collapse.py merged into another skeleton trace to no text."""
    by_text = {r["text"]: r["id"] for r in rows if r["src"] == "funerary"}
    out = collections.defaultdict(list)
    for raw in raws:
        tid = by_text.get(v5_text(raw, private, royal))
        if tid:
            out[tid].append(raw)
    return dict(out)


def sources_of(traced, derived):
    """{text id: [(source key, raw lines from it, of them equal to it)]}, the source line most raw lines come from
    first."""
    out = {}
    for tid, raws in traced.items():
        n, eq = collections.Counter(), collections.Counter()
        for raw in raws:
            d = derived.get(raw)
            if d:
                n[d[0]] += 1
                eq[d[0]] += d[1] == "equal"
        out[tid] = [(k, c, eq[k]) for k, c in sorted(n.items(), key=lambda x: (-x[1], x[0]))]
    return out


def swapped_names(derived):
    """{source key: Counter of the stretches of that line that the padding swapped out}: the names in it, as
    letters (key())."""
    out = collections.defaultdict(collections.Counter)
    for src, how, was, now, _ in derived.values():
        if how == "swap" and was:
            out[src][was] += 1
    return out


# ------------------------------------------------------------------------------- the spelling of corpus_v6

RILLY_S = re.compile(r"s(?!e)")


def to_corpus(mero, rilly=False):
    """A source line in the spelling of corpus_v6.

    As src/corpus.py: o for Millet's E, capitals that only mark a doubtful letter lowered, restored letters kept
    without their brackets, the first of two readings. Unlike it: an editor's hyphens (Millet's cuts into
    morphemes) join, so that a word is what stands between dividers or spaces; and a lost sign stays a dot that
    touches the word it breaks, so that a broken word is one broken word and not two whole ones. Of several
    spellings divided by ";" the first is taken. rilly: the line is in Rilly's spelling, where s is the sign s
    and se the sign se (the corpus writes them S and s), and ne the sign ne (N)."""
    s = next(iter([p for p in mero.split(";") if key(p)]), "")
    s = C.EITHER.sub(C.first_reading, s)
    s = re.sub(r"\(EIT[HX]ER.*?\)", "", s)
    s = re.sub(r"[*?\[\]()\-]", "", s)
    s = re.sub(r"[,…:]", " ", s)
    s = "".join(c if (not c.isupper() or c in C.KEEP_CAPS) else c.lower() for c in s)
    s = s.replace("E", "o")
    if rilly:
        s = RILLY_S.sub("S", s).replace("se", "s").replace("ne", "N")
    words = [w for w in s.split() if re.search(r"[A-Za-z0-9]", w) or set(w) == {"."}]
    out = []
    for w in words:                                   # a stretch of lost signs between words: one gap
        if set(w) == {"."} and out and set(out[-1]) == {"."}:
            continue
        out.append(w)
    return " ".join(out)


def spelled(s):
    """The letters of a name or of a stretch of words, compared without spaces, hyphens and brackets; a lost sign
    inside stays one dot, so that a broken name ("li...ye") is not the two words "li ye"."""
    return re.sub(r"\.+", ".", re.sub(r"[^A-Za-z0-9.]", "", s)).strip(".")


def name_words(text, names):
    """The places of the words of a text (in the corpus_v6 spelling) that spell one of the names: [word index].
    names are spellings of the source file; a name of several words marks each of them."""
    words = text.split()
    want = {spelled(to_corpus(n)) for n in names}
    want.discard("")
    out = set()
    for i in range(len(words)):
        for j in range(i, min(i + 4, len(words))):
            if spelled("".join(words[i:j + 1])) in want:
                out.update(range(i, j + 1))
    return sorted(out)


def main():
    lines = source_lines()
    raws = raw_lines()
    derived = derive(raws, lines)
    how = collections.Counter(d[1] for d in derived.values())
    print(f"source lines {len(lines)}: " + ", ".join(f"{f} {n}" for f, n in collections.Counter(l['file'] for l in lines).items()))
    print(f"raw lines {len(raws)} different: equal to a source line {how['equal']}, one stretch swapped {how['swap']}, "
          f"near {how['near']}, from no source line {len(raws) - len(derived)}")
    rows = [json.loads(l) for l in V5.read_text().splitlines() if l.strip()]
    older = [r for r in rows if r["src"] == "funerary"]
    traced = trace(rows, raws, *pools())
    src = sources_of(traced, derived)
    print(f"texts of the older corpus {len(older)}: traced to raw lines {len(traced)} "
          f"({sum(len(v) for v in traced.values())} raw lines), to a source line {sum(bool(v) for v in src.values())}, "
          f"to {len({v[0][0] for v in src.values() if v})} different source lines; to more than one source line "
          f"{sum(len(v) > 1 for v in src.values())}")
    longest = max((len(w) for c in swapped_names(derived).values() for w in c), default=0)
    print(f"the longest swapped stretch: {longest} letters")


if __name__ == "__main__":
    main()
