"""Griffith's ostraca from Faras, Buhen and Dakkah (Meroitic Studies V, JEA 11, 1925) as open readings.

Griffith, "Meroitic Studies V" (Journal of Egyptian Archaeology 11, 1925, pp. 218-224, plates XXVI-XXX) prints 47
ostraca in his transliteration of 1925: F.O. 1 to 40 from Faras, B.O. 1 to 6 from Buhen and D.O. 1 from Dakkah.
F.O. 38 prints no letters, so 46 texts are typed. The article is in the public domain.
data/expansion/jea/griffith1925_ostraca.txt holds them as typed by hand from page images (its head says how his
marks are typed); this script turns them into the corpus spelling and writes one row per text to
data/expansion/jea/griffith_jea11.jsonl, which src/v6/readings.py reads as open readings. They carry no REM number
(the REM volumes are not in hand), so src/v6/readings.py numbers them by the article's own siglum (F.O. 1).

His signs of 1925 are those of 1917 (src/akinidad.py, SIGNS: ê o, š S, plain s s, ñ N, z d, ḫ x, ẖ X). Meroitic
Studies VI (JEA 15, 1929) gives the sign he wrote z the value r, "nearly d" (today d): it prints no ostraca.

How his print is read (the source file's head has the marks):
- a word is what stands between dividers and spaces; his hyphens join (trêzes-lw is one word, as in REM 1003);
  [ ] and ( ) keep their letters; "*" (the second hand) and the symbols ⍋ ⍦ are not letters;
- a dot below a letter is his mark of a doubtful sign: the word is listed among the doubts, the letter is kept;
- "." is a lost sign; a run of dots between spaces, and his hatched "//", stand as a stretch of lost signs (no word);
- a numeral is written in digits, as the corpus writes numerals: his point parts the whole from the fraction,
  which Meroitic writes with signs of their own, so 6·3 is the two numerals 6 and 3 (as "1·2" in REM 1003); his
  ½ is kept in text_std only;
- one full stop at the end of a printed line or of the text is his punctuation, not a lost sign.

  python3 -I src/ostraca.py           write the rows and the public figures (data/expansion/jea/ostraca_figures.json)
  python3 -I src/ostraca.py blind     compare the blind second typing of the lot with the first (local files)
"""
import collections
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import akinidad as A   # noqa: E402

JEA = ROOT / "data/expansion/jea"
SOURCE = JEA / "griffith1925_ostraca.txt"
ROW = JEA / "griffith_jea11.jsonl"
FIGURES = JEA / "ostraca_figures.json"
BLIND = ROOT / "data/sources/ostraca/blind/second_typing.txt"
WORK = 'Griffith, "Meroitic Studies V", JEA 11 (1925)'
ITEM = "https://archive.org/details/in.ernet.dli.2015.70984"
DOT = "̣"                       # combining dot below: his mark of a doubtful sign
SYMBOLS = "⍋⍦"
LOT = ("F.O. 6", "F.O. 12", "F.O. 25", "F.O. 31", "F.O. 36")     # drawn 2026-11-17 08:28 (data/discovery/ostraca_sayce.md)
BAR = 0.97
NUMERAL = re.compile(r"[\d·½]+")
MARK = re.compile(r"^\((\d+)\)$")

# Where each text was found and what it is, from his descriptions (pp. 220-224). F.O. 1-36 are "all from the
# 'Western Palace'" (p. 223).
PALACE = "Faras, the \"Western Palace\""
SITES = {f"F.O. {n}": PALACE for n in range(1, 37)} | {
    "F.O. 37": "Faras, the northern Meroitic House",
    "F.O. 39": "Faras, the site of the church in the south-west of the Enclosure",
    "F.O. 40": "Faras (MacIver, Woolley and Mileham's exploration; the Philadelphia collection)",
    "B.O. 6": "Buhen, south of the North Temple (Philadelphia No. 10939)",
    "D.O. 1": "Dakkah (from W. E. Crum)"} | {
    f"B.O. {n}": "Buhen, west of the South Temple (Philadelphia No. 10938)" for n in range(1, 6)}
DESCRIBED = {
    "F.O. 1": "fragments of a large vessel of smooth buff ware, about two-thirds of its circle; large early writing",
    "F.O. 2": "buff, reddish outside; complete", "F.O. 3": "red inside and out; probably complete except left top",
    "F.O. 4": "coarse, red inside and out; left top corner lost", "F.O. 5": "apparently complete",
    "F.O. 6": "buff; probably complete; writing finely incised", "F.O. 7": "red, thick resin inside; complete",
    "F.O. 8": "two lines, imperfect at each end", "F.O. 9": "pink; right edge injured, left end lost",
    "F.O. 10": "left end probably imperfect", "F.O. 11": "red, dark inside; end of second line perhaps broken away",
    "F.O. 12": "apparently complete", "F.O. 13": "apparently complete", "F.O. 14": "buff, inside red; probably complete",
    "F.O. 15": "perhaps complete", "F.O. 16": "left side lost", "F.O. 17": "buff, outside red; original edge on left",
    "F.O. 18": "buff, outside red; top left perhaps lost, left end perhaps complete",
    "F.O. 19": "sherd from a large vessel, outside pink, inside black with resin",
    "F.O. 20": "red inside and out; right edge lost",
    "F.O. 21": "red, inside blackish with resin; right and lower edges lost; early style in a thin hand",
    "F.O. 22": "left edge complete", "F.O. 23": "apparently complete",
    "F.O. 24": "red, blackish resin inside; imperfect on right", "F.O. 25": "resin inside; top and left side broken away",
    "F.O. 26": "buff, outside red; apparently broken away all round except at the top",
    "F.O. 27": "reddish inside and out; lines imperfect at each end", "F.O. 28": "",
    "F.O. 29": "peg bottom of a wine-amphora", "F.O. 30": "complete unless at right end", "F.O. 31": "black resin inside",
    "F.O. 32": "resin inside", "F.O. 33": "", "F.O. 34": "resin inside",
    "F.O. 35": "very thick, coarse red; left edge lost; writing in white, of late style",
    "F.O. 36": "buff, resin inside; writing in white, late style", "F.O. 37": "red inside and out; writing white; late style",
    "F.O. 39": "buff", "F.O. 40": "faint, but probably complete",
    "B.O. 1": "large ostrakon in nine fragments, apparently from a large jar or wine-amphora with shiny red surface",
    "B.O. 2": "a similar fragment showing parts of two lines",
    "B.O. 3": "thick grey ware, reddish inside and out; complete",
    "B.O. 4": "thick pinkish ware, outside red, inside glazed black with resin; two lines in black ink; complete",
    "B.O. 5": "buff, outside reddish, inscribed in red ink",
    "B.O. 6": "coarse reddish, inscribed in late style; right edge and lower left lost",
    "D.O. 1": "thick pinkish, outside red; not early; bottom edge lost"}
# What his notes doubt or read otherwise (his words), and the places we are unsure of (OURS): (text, word as
# typed, why). The word is found in the text by its letters without the marks.
NOTES = (
    ("F.O. 1", "12·1", "his note on l. 3: \"Or omit ·1\""),
    ("F.O. 1", "1·3", "his note on l. 3 ends \"or 1·1 :\" (for ant-mnês 1·3)"),
    ("F.O. 1", "tr", "his note on l. 4: \"It is not clear whether tr 2·8 or trê 1·8 should be read\""),
    ("F.O. 3", "·2", "his note: \"the last two spots seem best explained as additions to the original ·9, producing "
                     "a total which would have been properly expressed by 1·1\""),
    ("F.O. 12", "10·1", "his note on F.O. 12 and 13: \"The upper spot after 10 may be accidental but looks like ink\""),
    ("F.O. 16", "abel", "his note: \"abel[te] F.O. 1/1\""),
    ("F.O. 19", "mkšḫi", "his note on l. 4 reads mkšḫi (5) ze as one word, mkšḫize (cf. the title mkešḫe K.I.)"),
    ("F.O. 21", "qệ", "his note on l. 2: \"a horizontal line crossed by a short oblique line at the end\" (a sign "
                      "of l. 2 that he does not name)"),
    ("B.O. 1", "qe", "his note: \"possibly šleqeñ 4·8 should be read here\" (for šle qe 74·8); \"if not, the "
                     "doubtful sign may be a 10-numeral\""),
    ("B.O. 1", "⍋", "his note on l. 2: \"the broken sign should be a 10-numeral or some special symbol\" (printed as "
                    "the symbol after 16·6, which the corpus leaves out)"),
    ("B.O. 2", "ṃr", "his note: \"the tail of the m(?) very short\""),
)
OURS = (
    ("F.O. 10", "·ḷ", "a point and an upright with a dot below: read as the numeral ·1 (doubtful); it could be the "
                      "letter l"),
    ("F.O. 13", "ariketê", "printed with a grave accent (è): read as ê, the circumflex damaged, as in F.O. 22"),
    ("F.O. 18", "·", "a point printed apart between ṭẹ and 6·3½: left out"),
    ("F.O. 21", "tñs", "the tilde does not show in the text line on this scan; his note on l. 3 writes tñs"),
    ("F.O. 22", "erqêtê", "printed erqêtè: read as ê, as his note on F.O. 21 writes it (\".erqêtê F.O. 22\")"),
    ("F.O. 22", "ỵệ", "the ê printed with a grave accent: read as ê (dots below both the y and the è)"),
    ("F.O. 25", "ḷ", "an upright with a dot below and no flag at the top: read as the letter l; it could be the "
                     "numeral 1 (the last sign of the text, with a flag, is read as the numeral 1)"),
    ("F.O. 26", "l", "an upright between two hatched stretches: read as the letter l; it could be the numeral 1"),
    ("B.O. 1", "mrê", "the two printed lines carry no numbers: (1) and (2) are ours"),
    ("B.O. 6", "ỵ", "the mark below the y looks like a breve with a dot under it: read as a dot below"),
)


def plain(token):
    """A token without his marks: the dot below, brackets, parentheses, hyphens, the second hand's asterisk."""
    t = unicodedata.normalize("NFD", token).replace(DOT, "")
    t = re.sub(r"[\[\]()\-*]", "", t)
    return unicodedata.normalize("NFC", t)


def to_corpus(token):
    """One of his tokens in the corpus spelling: a numeral as its digits (6·3 -> "6 3", ·4½ -> "4"), a word in the
    corpus letters."""
    p = plain(token)
    if p.startswith("·"):                       # ·ḷ (F.O. 10): a point before an upright is a numeral
        p = p.replace("l", "1")
    if NUMERAL.fullmatch(p):
        return " ".join(d for d in re.split(r"[·½]", p) if d)
    return p.lower().translate(A.SIGNS)


def texts(text=None):
    """[{no, page, plates, printed}] from the source file."""
    text = SOURCE.read_text(encoding="utf-8") if text is None else text
    out = []
    for raw in text.splitlines():
        if raw.startswith("#") or not raw.strip():
            continue
        no, page, plates, printed = raw.split("\t")
        out.append({"no": no, "page": page, "plates": "" if plates == "-" else plates,
                    "printed": unicodedata.normalize("NFC", printed.strip())})
    return out


def tokens(printed):
    """[(line, token)] of a text: his line marks set the line, dividers and spaces part the tokens, one full stop at
    the end of a printed line or of the text goes, a "(?)" stays as a token of its own."""
    parts = re.split(r"\s+", re.sub(r"\s*\(sic\)", "", printed).replace(":", " "))
    out, line = [], 1
    parts = [p for p in parts if p]
    for k, p in enumerate(parts):
        m = MARK.match(p)
        if m:
            line = int(m.group(1))
            continue
        last = k == len(parts) - 1 or MARK.match(parts[k + 1])
        if last and re.search(r"[^.]\.$", p):
            p = p[:-1]
        if p.endswith("(?)") and p != "(?)":
            out += [(line, p[:-3]), (line, "(?)")]
        else:
            out.append((line, p))
    return out


def words(printed):
    """Every token that stands in the corpus, in order: [{line, printed, corpus, kind, doubt}]. kind is word,
    numeral or lost (a stretch of lost signs); the symbols and his "(?)" are not tokens of the corpus."""
    out = []
    for line, t in tokens(printed):
        if t == "(?)":
            if out:
                out[-1]["doubt"] = "; ".join(filter(None, [out[-1]["doubt"], "(?) after it"]))
            continue
        if all(c in SYMBOLS for c in t) or t == "·" or t == "*":
            continue
        if t == "//":
            out.append({"line": line, "printed": t, "corpus": "...", "kind": "lost", "doubt": ""})
            continue
        c = to_corpus(t)
        doubt = "dot below a sign" if DOT in unicodedata.normalize("NFD", t) else ""
        if NUMERAL.fullmatch(plain(t).replace("l", "1") if plain(t).startswith("·") else plain(t)):
            for d in c.split():                                           # 6·3: the numerals 6 and 3
                out.append({"line": line, "printed": t, "corpus": d, "kind": "numeral", "doubt": doubt})
            continue
        kind = "word" if re.search(r"[A-Za-z]", c) else "lost"
        out.append({"line": line, "printed": t, "corpus": c, "kind": kind, "doubt": doubt})
    return out


def signs(printed):
    """The Meroitic signs of a text in his letters, without the dots below, in order (te and tê one sign each)."""
    return [s for w in words(printed) if w["kind"] == "word" for s in A.SIGN.findall(plain(w["printed"]).lower())]


def doubts(t, ws):
    """[{line, word, why}] of a text: the words with a dot below or a (?), his notes, then ours."""
    out = [{"line": l, "word": p, "why": why} for l, p, why in dict.fromkeys((w["line"], w["printed"], w["doubt"])
                                                                            for w in ws if w["doubt"])]
    for table in (NOTES, OURS):
        for no, word, why in table:
            if no != t["no"]:
                continue
            w = next((x for x in ws if plain(x["printed"]) == plain(word)), None)
            # a mark that is no token of the corpus (the point of F.O. 18, a symbol): found among his tokens
            line = w["line"] if w else next((l for l, tok in tokens(t["printed"]) if tok == word), None)
            if line is None:
                raise SystemExit(f"{no}: not in the text: {word}")
            out.append({"line": line, "word": word, "why": why})
    return out


def row(t):
    ws = words(t["printed"])
    lines = collections.defaultdict(list)
    for w in ws:
        lines[w["line"]].append(w["corpus"])
    ds = doubts(t, ws)
    return {
        "source": WORK, "item": ITEM, "griffith_no": None, "rem": "", "number": t["no"],
        "label": f"{t['no']} (JEA 11, 1925)", "page": f"{t['page']}" + (f"; {t['plates']}" if t["plates"] else ""),
        "object": "ostracon" + (f": {DESCRIBED[t['no']]}" if DESCRIBED[t["no"]] else ""),
        "site": SITES[t["no"]],
        "text_std": t["printed"],
        "text_corpus": " ".join(w["corpus"] for w in ws),
        "lines": {str(k): " ".join(v) for k, v in sorted(lines.items())},
        "uncertain": sum(1 for w in ws if w["doubt"] and w["kind"] == "word"),
        "signs": len(signs(t["printed"])),
        "words": sum(1 for w in ws if w["kind"] == "word"),
        "numerals": sum(1 for w in ws if w["kind"] == "numeral"),
        "symbols": sum(t["printed"].count(s) for s in SYMBOLS),
        "doubts": ds,
        "notes": ("Typed by hand from page images of Griffith's article (public domain; archive.org "
                  "in.ernet.dli.2015.70984), not from its text layer. text_std: his letters and marks as printed. "
                  "text_corpus: the corpus spelling (ê o, š S, s s, ñ N, z d, ḫ x, ẖ X), his word division, his "
                  "hyphens joining, his restorations kept as letters, '.' a lost sign, his numerals in digits (his "
                  "point parts two numerals, his ½ is left out); "
                  "the second hand's '*' and the symbols ⍋ ⍦ left out. doubts: the words with his dot below a "
                  "sign or a (?), what his notes doubt, and the places we are unsure of. src/ostraca.py writes "
                  "this row from data/expansion/jea/griffith1925_ostraca.txt."),
    }


def rows(ts=None):
    return [row(t) for t in (texts() if ts is None else ts)]


# ------------------------------------------------------------------------------------------ the second typing

def compare_signs(a, b):
    """(signs of a that fall in stretches a and b share, signs of a, signs of b)."""
    m = difflib.SequenceMatcher(None, a, b, autojunk=False)
    same = sum(blk.size for blk in m.get_matching_blocks())
    return same, len(a), len(b)


def second_typing(path=BLIND):
    """{text: printed} of the blind second typing (local), or None where it is not here."""
    if not path.exists():
        return None
    out = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            no, printed = raw.split("\t", 1)
            out[no.strip()] = unicodedata.normalize("NFC", printed.strip())
    return out


def blind(first=None, second=None):
    """The two typings of the lot compared: signs (the bar), words, numerals and the dots below."""
    first = {t["no"]: t["printed"] for t in texts()} if first is None else first
    second = second_typing() if second is None else second
    per, tot = {}, [0, 0, 0]
    for no in LOT:
        a, b = signs(first[no]), signs(second[no])
        same, na, nb = compare_signs(a, b)
        wa = [w["corpus"] for w in words(first[no])]
        wb = [w["corpus"] for w in words(second[no])]
        da = [plain(w["printed"]) for w in words(first[no]) if w["doubt"]]
        db = [plain(w["printed"]) for w in words(second[no]) if w["doubt"]]
        per[no] = {"signs": na, "signs_second": nb, "agree": same, "words_same": wa == wb,
                   "doubted_words": len(da), "doubted_alike": da == db}
        for k, v in enumerate((same, na, nb)):
            tot[k] += v
    share = min(tot[0] / tot[1], tot[0] / tot[2]) if tot[1] and tot[2] else 0.0
    return {"lot": list(LOT), "bar": BAR, "signs_first": tot[1], "signs_second": tot[2], "agree": tot[0],
            "share": round(share, 4), "met": share >= BAR, "texts": per}


# ------------------------------------------------------------------------------------------ the map

GLOSSES = ROOT / "data/sources/v6/analysts/glosses.jsonl"


def recurrence(rs=None, gl=None):
    """What the ostraca's spellings are on the map as it stands (src/themap.py current(), local), and how many of
    the open spellings that stood in one text of the map stand in an ostracon too: a spelling has the group its
    places have most often (themap.counts); a spelling with a lost sign is left out. None where the map is not here."""
    if gl is None:
        if not GLOSSES.exists():
            return None
        sys.path[:0] = [str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
        import themap as T
        gl = T.current()
    import recurring as W
    group = lambda level: ("translated" if level in W.READ else "named" if level in W.NAMED
                           else "open" if level in W.OPEN else "lost")
    by_form, texts_of = collections.defaultdict(collections.Counter), collections.defaultdict(set)
    for tid, gs in gl.items():
        for g in gs:
            by_form[g["form"]][group(g["level"])] += 1
            texts_of[g["form"]].add(tid)
    level = {f: c.most_common(1)[0][0] for f, c in by_form.items()}
    rs = rows() if rs is None else rs
    ours = collections.defaultdict(set)
    for r in rs:
        for w in r["text_corpus"].split():
            if re.search(r"[A-Za-z]", w) and "." not in w:
                ours[w].add(r["number"])
    on_map = collections.Counter(level.get(f, "not on the map") for f in ours)
    single = {f for f, l in level.items() if l == "open" and len(texts_of[f]) == 1}
    now = sorted(f for f in single if f in ours)
    new = sorted(f for f in ours if f not in level and len(ours[f]) >= 2)
    return {"spellings": len(ours), "on_the_map": dict(sorted(on_map.items())),
            "open_in_one_text_before": len(single), "now_in_a_second_text": len(now), "which": now,
            "new_in_two_ostraca_or_more": len(new), "which_new": new,
            "running_words": sum(1 for r in rs for w in r["text_corpus"].split()
                                 if re.search(r"[A-Za-z]", w)),
            "how": "the map as it stands (src/themap.py current()): a spelling has the group its places have most "
                   "often; an open spelling that stood in one text of the map and stands in an ostracon now stands "
                   "in two; spellings with a lost sign are left out"}


# ------------------------------------------------------------------------------------------ figures

def figures(rs=None):
    rs = rows() if rs is None else rs
    by_site = collections.Counter(r["number"].split()[0] for r in rs)
    return {"texts": len(rs), "by_series": dict(sorted(by_site.items())),
            "words": sum(r["words"] for r in rs), "signs": sum(r["signs"] for r in rs),
            "numerals": sum(r["numerals"] for r in rs), "symbols": sum(r["symbols"] for r in rs),
            "lines": sum(len(r["lines"]) for r in rs),
            "words_doubted": sum(r["uncertain"] for r in rs),
            "his_notes": len(NOTES), "ours": len(OURS),
            "printed_without_letters": ["F.O. 38"],
            "missing_pages": "pp. 218-219 (the opening of the article) are not in the scan used"}


def main(argv):
    if argv[1:] == ["blind"]:
        out = blind()
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return out
    if argv[1:]:
        sys.exit(__doc__)
    rs = rows()
    ROW.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs), encoding="utf-8")
    figs = figures(rs)
    old = json.loads(FIGURES.read_text()) if FIGURES.exists() else {}
    figs = old | figs
    if second_typing() is not None:
        figs["second_typing"] = blind()
    rec = recurrence(rs)
    if rec is not None:
        figs["map"] = rec
    FIGURES.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{ROW.relative_to(ROOT)}: {figs['texts']} texts, {figs['words']} words, {figs['signs']} signs, "
          f"{figs['numerals']} numerals, {figs['words_doubted']} words doubted")
    if "second_typing" in figs:
        s = figs["second_typing"]
        print(f"second typing of the lot: {s['agree']} of {s['signs_first']} signs ({s['share']:.1%}); bar "
              f"{s['bar']:.0%} {'met' if s['met'] else 'MISSED'}")


if __name__ == "__main__":
    main(sys.argv)
