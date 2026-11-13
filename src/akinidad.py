"""REM 1003, the Great Stela of Akinidad, in Griffith's transliteration of 1917: an open reading.

Griffith, "Meroitic Studies IV: The Great Stela of Prince Akinizaz" (JEA 4, 1917, pp. 159-173), prints the whole
text of the stela, ll. 1 to 42, in 21 sections in his transliteration of 1917 (pp. 164, 166 and 168-172). The
article is in the public domain. data/expansion/jea/griffith1917_rem1003.txt holds those sections as typed by hand
from page images of the article; this script turns them into the corpus spelling and writes the row
data/expansion/jea/griffith_jea4.jsonl, which src/v6/readings.py reads as an open reading of REM 1003. The row
is in the folder's own sub-folder, so that src/expand.py, which reads the griffith_*.jsonl files of
data/expansion and not of its sub-folders, does not take it into corpus_v3 and corpus_v5, which stay as they were.

Griffith's signs of 1917 and the corpus spelling (data/expansion/README.md, section 2, from his sign list of
1911; the 1917 article marks every h with one of the two marks, which the 1911 list does not):

  ê -> o   (his sign 3; tê is the sign to)       š -> S   (the sign s)        plain s -> s   (the sign se)
  ñ -> N   (the sign ne)                          z -> d                       ḫ (h, breve below) -> x
  ẖ (h, line below) -> X
  every other letter as written; capitals (names) lowered; his initial e and i are the signs e and i. A plain h
  is no letter of the corpus spelling, so a slip of the typing that drops a mark shows in the row (the tests).

How his print is read (all of it stated in the source file's head): "(l. N)" starts line N of the stela; a
word is what stands between dividers and spaces, as he prints it; a line mark inside a word (Aki(l. 2)nizz)
keeps the word whole and the word belongs to the line it starts on; his hyphens join (qêre-yi, and the two
words he breaks at the end of a printed line); his restorations in [ ] and ( ) are kept as letters; "." is a
lost sign, and a stretch of lost signs between spaces stands as a word of its own (the corpus counts no word
there). A word with his "?" above a sign or his "(?)" after it is a word he doubts: the row lists them, and after
them the signs his footnotes and his notes on the sections doubt or read otherwise, and the places we are unsure
of (OURS).

The comparison (local only: the closed readings are Millet's, as Otten's file has it, and the Newsletter's
printout, both in copyright): both texts are spelled alike (src/expand.py skeleton(), digits kept), lined up
letter by letter (difflib), and a word of Griffith's agrees when every one of its letters falls in a stretch the
two share. Words without a letter or a digit do not count. The counts, not the texts, are public:
data/expansion/jea/rem1003_comparison.json.

  python3 -I src/akinidad.py           writes the row and, where the closed readings are present, the comparison
"""
import collections
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import expand as E     # noqa: E402

JEA = ROOT / "data/expansion/jea"
SOURCE = JEA / "griffith1917_rem1003.txt"
ROW = JEA / "griffith_jea4.jsonl"
COMPARISON = JEA / "rem1003_comparison.json"
LOCAL = ROOT / "data/sources/akinidad"
V6 = ROOT / "data/sources/v6/inscriptions.jsonl"
CLOSED = ("otten:narrative:hamadab", "mnl:REM 1003|MeroNews6")     # the preferred reading first

WORK = 'Griffith, "Meroitic Studies IV: The Great Stela of Prince Akinizaz", JEA 4 (1917)'
ZENODO = "https://zenodo.org/records/2497984"
SIGNS = str.maketrans({"ê": "o", "š": "S", "ñ": "N", "z": "d", "ḫ": "x", "ẖ": "X"})
SIGN = re.compile(r"tê|te|[a-zêšñḫẖ]")            # one Meroitic sign in his letters (te and tê are one sign each)
MARK = re.compile(r"\(l\. (\d+)\)")
# what is unsure beyond his own question marks, in the order of the stela: (his word as printed, why). Where his
# footnotes and his notes on the sections (pp. 166-171) doubt a sign or read it otherwise, and where we are unsure.
OURS = (
    ("Armeyêsli", "his footnote: \"Or Arẖeyêsli here and in l. 5\" (p. 167: \"or Arẖeyês in both ll. 3 and 5\"): "
                  "the sign m perhaps ẖ"),
    ("Armil", "his footnote: \"m fairly certain\""),
    ("Armeyslḫe", "his footnote on l. 3: \"Or Arẖeyêsli here and in l. 5; in the latter ê is lacking, one stroke "
                  "having probably been omitted by accident\": the sign m perhaps ẖ"),
    ("yezk", "his note on § 5 (p. 168) writes it \"yez(?)k\""),
    ("1·2", "a numeral printed \"1·2\" (so too in his summary, \"1·2 women\"): read as two numerals, 1 and 2"),
    ("ytes", "his note (p. 168): \"ytes might be read yter, or even be corrected to yqês\""),
    ("weštel", "his note (p. 168): \"weštel seems a better reading than šeš\""),
    ("ḫrpḫ.", "his footnote on the lost sign: \"Perhaps a numeral\""),
    ("allebšê", "his footnote: \"Probably confused for alleleb-šê, cf. l. 13\""),
    (".ḫrpḫi", "his footnote mark on the lost sign before it, the note \"Perhaps a numeral\""),
    ("tewwibḫt", "his note on § 15 (p. 170): \"tewwibḫl or t\""),
    ("mzeybeli", "his note (p. 170): \"mzeybeli the initial uncertain\""),
    ("wlbrt[e", "his note (p. 170) writes it \"wt(?)brte l. 22\""),
    (".....", "his note (p. 171): \"The signs at the beginning of l. 25 might be in part numerals, the last k or 9\""),
    ("wwikewi", "his note (p. 171): \"wwikewi or perhaps wwi awi, see §§ 17, 21 following\""),
    ("teslke", "\"Mnê\" ends a printed line and \"teslke\" begins the next, without a hyphen: kept as two words"),
    ("1032.", "the last digit is hatched in the print (damaged): kept as a lost sign"),
)


def sections(text=None):
    """[(number, the section as printed)] from the source file: one line per section, comments dropped."""
    text = SOURCE.read_text(encoding="utf-8") if text is None else text
    out = []
    for raw in text.splitlines():
        m = re.match(r"§(\d+)\s+(.*)$", raw)
        if m:
            out.append((int(m.group(1)), m.group(2).split("#")[0].strip()))
    return out


def to_corpus(word):
    """One of his words, as printed and without his marks, in the corpus spelling."""
    if re.fullmatch(r"[\d·.]+", word) and "·" in word:
        return " ".join(word.split("·"))
    return word.lower().translate(SIGNS)


def plain(token):
    """A token without his marks: question marks, brackets, parentheses, hyphens and the inner line marks."""
    t = re.sub(r"<\d+>", "", token).replace("(?)", "").replace("?", "")
    return re.sub(r"[\[\]()\-]", "", t)


def words(secs=None):
    """Every word of the text in the order of the stela: [{line, section, printed, griffith, corpus, doubt}].
    printed keeps his marks; griffith is the word in his letters without them; corpus its spelling in the corpus;
    doubt says what he doubts ("" for nothing). A stretch of lost signs is a word whose corpus form has no letter."""
    out, line = [], 1
    for number, body in sections() if secs is None else secs:
        body = re.sub(r"-\s*", "-", body)                                          # his hyphens join
        body = re.sub(r"(?<=\S)\(l\. (\d+)\)(?=\S)", lambda m: f"<{m.group(1)}>", body)   # a mark inside a word
        for part in re.split(r"(\(l\. \d+\))", body):
            m = MARK.fullmatch(part)
            if m:
                line = int(m.group(1))
                continue
            for token in [t for t in re.split(r"[:\s]+", part) if t]:
                if re.fullmatch(r"\[?\(?\?\)?\]?", token):                       # his doubt about the word before
                    out[-1]["doubt"] = "; ".join(filter(None, [out[-1]["doubt"], "? after the word"]))
                    continue
                g = plain(token)
                if not g:
                    continue
                doubt = []
                if re.search(r"[^\s(]\?|^\?", token.replace("(?)", "")):
                    doubt.append("? above a sign")
                if "(?)" in token:
                    doubt.append("(?) by the word")
                printed = re.sub(r"<(\d+)>", r"(l. \1)", token)
                for c in to_corpus(g).split():                                    # "1·2" is two numerals
                    out.append({"line": line, "section": number, "printed": printed, "griffith": g, "corpus": c,
                                "doubt": "; ".join(doubt)})
                marks = re.findall(r"<(\d+)>", token)
                if marks:
                    line = int(marks[-1])
    return out


def counted(w):
    """A word that counts: it has a letter or a digit (a stretch of lost signs does not)."""
    return bool(re.search(r"[A-Za-z0-9]", w["corpus"]))


def text_std(secs=None):
    """His text as printed, sections run together, with "(N)" for the start of line N (as the other rows)."""
    body = " ".join(b for _, b in (sections() if secs is None else secs))
    return MARK.sub(lambda m: f"({m.group(1)})", body)


def unsure(ws):
    """[(line, his word, why)]: the words he doubts, then ours."""
    out = list(dict.fromkeys((w["line"], w["printed"], w["doubt"]) for w in ws if w["doubt"]))
    for printed, why in OURS:
        w = next((x for x in ws if x["griffith"] == plain(printed)), None)
        if w is None:
            raise SystemExit(f"not in the text: {printed}")
        out.append((w["line"], printed, why))
    return out


def row(ws=None, secs=None):
    ws = words(secs) if ws is None else ws
    lines = collections.defaultdict(list)
    for w in ws:
        lines[w["line"]].append(w["corpus"])
    signs = sum(len(SIGN.findall(w["griffith"].lower())) for w in ws)
    doubts = unsure(ws)
    return {
        "source": WORK, "item": ZENODO, "griffith_no": None, "rem": "1003",
        "label": "JEA 4 (1917), §§ 1-21",
        "page": "pp. 164, 166, 168-172 (§§ 1-21; the PDF's pages 7, 10, 12, 14-17)",
        "object": "the Great Stela of Queen Amanirenas and Prince Akinidad (gritstone; British Museum EA 1650), "
                  "from the temple at Hamadab near Meroe",
        "site": "Hamadab, near Meroe City",
        "text_std": text_std(secs),
        "text_corpus": " ".join(w["corpus"] for w in ws),
        "lines": {str(k): " ".join(v) for k, v in sorted(lines.items())},
        "uncertain": sum(1 for w in ws if w["doubt"]),
        "signs": signs,
        "words": sum(1 for w in ws if counted(w)),
        "doubts": [{"line": l, "word": p, "why": why} for l, p, why in doubts],
        "notes": ("Typed by hand from page images of Griffith's article (public domain; the JSTOR copy on Zenodo, "
                  "record 2497984), not from its text layer. He prints the text in 21 sections (§§ 1-21) that run "
                  "on from l. 1 to l. 42; this row runs them together in the order of the stela. text_std: his "
                  "letters and marks, with (N) for the start of line N of the stela. text_corpus: the corpus "
                  "spelling (ê o, š S, s s, ñ N, z d, ḫ x, ẖ X), his word division, his restorations kept as "
                  "letters, '.' a lost sign. lines: the words of text_corpus by the line of the stela each "
                  "starts on. doubts: the words he marks with '?' or '(?)', then the signs his footnotes and notes "
                  "doubt or read otherwise, and the places we are unsure of. "
                  "src/akinidad.py writes this row from data/expansion/jea/griffith1917_rem1003.txt."),
    }


# ------------------------------------------------------------------------------------------ the comparison

def fold(text):
    """A text as one string of letters and digits, spelled alike whatever convention wrote it (expand.skeleton,
    with digits kept)."""
    t = re.sub(r"\bR?NAME\b|[.…]+", "", text).lower()
    t = t.replace("o", "e").replace("se", "s").replace("ne", "n")
    return re.sub(r"[^a-z0-9]", "", t)


def exact(text):
    """A text as one string of its letters and digits as the corpus spells them, nothing folded."""
    return re.sub(r"[^A-Za-z0-9]", "", text)


def compare(ws, closed, spell=fold):
    """({line: (words that agree, words)}, (letters that agree, letters), [(word, agrees)]) of Griffith's words
    against a closed text. A word agrees when all its letters lie in stretches that the two texts share once
    lined up. spell: how both are spelled for it (fold, or exact for the corpus spelling as it stands)."""
    ws = [w for w in ws if counted(w)]
    stream, owner = "", []
    for k, w in enumerate(ws):
        f = spell(w["corpus"])
        stream += f
        owner += [k] * len(f)
    other = "".join(spell(x) for x in closed.split())
    shared = [False] * len(stream)
    for tag, a0, a1, _, _ in difflib.SequenceMatcher(None, stream, other, autojunk=False).get_opcodes():
        if tag == "equal":
            shared[a0:a1] = [True] * (a1 - a0)
    good = [True] * len(ws)
    for i, k in enumerate(owner):
        good[k] = good[k] and shared[i]
    by_line = collections.defaultdict(lambda: [0, 0])
    for k, w in enumerate(ws):
        by_line[w["line"]][1] += 1
        by_line[w["line"]][0] += good[k]
    return ({l: tuple(v) for l, v in sorted(by_line.items())}, (sum(shared), len(stream)),
            [(w, good[k]) for k, w in enumerate(ws)])


def closed_readings(path=V6):
    """{key: text} of the closed readings of REM 1003 (local only), or None where the build is not here."""
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["id"] == "REM 1003":
            return {x["key"]: x["text"] for x in r["readings"] if x["key"] in CLOSED}
    return None


def figures(ws, closed):
    out = {"griffith": {"lines": len({w["line"] for w in ws}), "words": sum(1 for w in ws if counted(w)),
                        "words_he_doubts": sum(1 for w in ws if w["doubt"] and counted(w))},
           "how": "both texts spelled alike (src/expand.py skeleton(), digits kept: o and e, s and se, n and ne, "
                  "x and X, capitals and small letters folded) and lined up letter by letter (difflib); a word of "
                  "Griffith's agrees when every letter of it lies in a stretch the two share. strict: the same "
                  "with nothing folded, the corpus spelling as it stands (Otten's file writes the sign s as s, "
                  "where the corpus writes S, so it agrees less there)",
           "against": {}}
    for key in CLOSED:
        if key not in closed:
            continue
        by_line, (la, ln), _ = compare(ws, closed[key])
        a, n = sum(v[0] for v in by_line.values()), sum(v[1] for v in by_line.values())
        out["against"][key] = {
            "words": n, "agree": a, "share": round(a / n, 3), "letters": ln, "letters_agree": la,
            "letters_share": round(la / ln, 3), "closed_words": len([x for x in closed[key].split() if x.strip(".")]),
            "by_line": {str(l): {"agree": v[0], "words": v[1]} for l, v in by_line.items()}}
        strict = compare(ws, closed[key], exact)[0]
        sa = sum(v[0] for v in strict.values())
        out["against"][key]["strict"] = {"agree": sa, "share": round(sa / n, 3)}
    return out


def main(argv):
    ws = words()
    r = row(ws)
    ROW.write_text(json.dumps(r, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{ROW.relative_to(ROOT)}: {r['words']} words on {len(r['lines'])} lines, {r['signs']} signs, "
          f"{r['uncertain']} words he doubts, {len(r['doubts'])} places listed as unsure")
    closed = closed_readings()
    if not closed:
        print("the closed readings are not here (local only): the comparison is left as it is")
        return
    figs = figures(ws, closed)
    COMPARISON.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    LOCAL.mkdir(exist_ok=True)
    with (LOCAL / "comparison.tsv").open("w", encoding="utf-8") as f:     # the words, with the closed text: local
        f.write("against\tline\tgriffith\tcorpus\tagrees\n")
        for key in CLOSED:
            if key in closed:
                for w, ok in compare(ws, closed[key])[2]:
                    f.write(f"{key}\t{w['line']}\t{w['griffith']}\t{w['corpus']}\t{ok}\n")
    for key, v in figs["against"].items():
        print(f"against {key}: {v['agree']} of {v['words']} words agree ({v['share']:.1%}; strict "
              f"{v['strict']['agree']}, {v['strict']['share']:.1%}); letters {v['letters_agree']} of {v['letters']} "
              f"({v['letters_share']:.1%})")


if __name__ == "__main__":
    main(sys.argv[1:])
