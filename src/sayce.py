"""Sayce's reading of REM 1003, the Great Stela of Akinidad (Liverpool Annals 7, pp. 69-72), against Griffith 1917.

A. H. Sayce printed the whole stela, ll. 1 to 42, in his own letters, in the Liverpool Annals of Archaeology and
Anthropology 7 (1914-15), before Griffith's edition (JEA 4, 1917; src/akinidad.py). data/expansion/jea/
sayce1914_rem1003.txt holds his lines as typed by hand from page images. Sayce died in 1933: his reading is in the
public domain in the US and in the UK.

His letters and Griffith's (SIGNS, fixed on 2026-11-17 before any comparison ran, from the values the two print side
by side in the opening lines and from Meroitic Studies VI, JEA 15, p. 70, where Griffith quotes Sayce's rh for the
sign Griffith wrote z): a e i y b p m n r l s as written; u w; ṇ ñ; sh š; k q (his k is Griffith's q) and g k; th t,
t tê, to tê and toh te; rh and rhe z (rhe is one unit, as in Agini-rherhe); ḥ and h ḫ; gh ẖ; a prime ' ê, either
after a letter (k' is q then ê) or as a unit of its own; ă a. Then Griffith's letters go to the corpus spelling as in
src/akinidad.py. A capital is the same letter. The table is a reading of his print, not his own sign list (that is in
Liverpool Annals 7, p. 23, which is not in hand); how often each of his units lines up with each of Griffith's signs
is counted (`units`), so a value that does not hold shows.

How his print is read: a word is what stands between his dividers ":" and spaces; his hyphens part the signs of a
word, and a hyphen at the end of a line runs the word on into the next line (it belongs to the line it starts on);
"(?)" doubts the sign before it, or the word when it stands alone; [ ] are his restorations (kept, and counted as
unsure); a run of dots is a lost stretch; his roman numerals are numerals.

The comparison: both texts in the corpus spelling, lined up letter by letter (difflib) over the whole text. A word
agrees when all its letters lie in stretches the two share. Two spellings: folded (src/akinidad.py fold(), as for
the closed readings) and strict (the corpus letters as they stand, with x and X one letter, since Sayce does not
part Griffith's two h-signs).

Griffith's doubted words (his "?" and "(?)", 38 words): each is lined up with Sayce's letters at the same place, and
classed as data/discovery/ostraca_sayce.md fixes before the comparison: confirms, reads otherwise, also unsure, not
found. Where the closed readings are here (local only), each place also says whether the later reading sides with
Griffith, with Sayce, with both or with neither (folded spelling; counts only are public).

  python3 -I src/sayce.py          write data/expansion/jea/sayce_rem1003.json (the words) and sayce_comparison.json
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
SOURCE = JEA / "sayce1914_rem1003.txt"
WORDS = JEA / "sayce_rem1003.json"
COMPARISON = JEA / "sayce_comparison.json"
BLIND = ROOT / "data/sources/sayce/blind/second_typing.txt"
LOCAL = ROOT / "data/sources/sayce"
LOT = (3, 13, 19, 35)                    # drawn 2026-11-17 08:28 (data/discovery/ostraca_sayce.md)
BAR = 0.97
# his units -> Griffith's letters of 1917 (fixed before the comparison; see the head)
SIGNS = {"a": "a", "ă": "a", "e": "e", "i": "i", "y": "y", "u": "w", "b": "b", "p": "p", "m": "m", "n": "n",
         "ṇ": "ñ", "r": "r", "l": "l", "s": "s", "sh": "š", "k": "q", "g": "k", "th": "t", "t": "tê", "to": "tê",
         "toh": "te", "rh": "z", "rhe": "z", "ḥ": "ḫ", "h": "ḫ", "gh": "ẖ", "'": "ê"}
DIGRAPHS = ("toh", "rhe", "sh", "th", "rh", "gh", "to")
ROMAN = re.compile(r"[MDCLXVI]+")
DOT = "̣"


def lines(text=None):
    """[(line, his text)] from the source file."""
    text = SOURCE.read_text(encoding="utf-8") if text is None else text
    out = []
    for raw in text.splitlines():
        if raw.startswith("#") or not raw.strip():
            continue
        n, body = raw.split("\t", 1)
        out.append((int(n), unicodedata.normalize("NFC", body.strip())))
    return out


def tidy(body):
    """His line with the spaces inside a word closed: "b (?)-ḥ" "[ḥ-r-] p" "a- . . . m" "[e :]"."""
    body = re.sub(r"\s+\(\?\)(?=-)", "(?)", body)                    # b (?)-ḥ-e -> b(?)-ḥ-e
    body = re.sub(r"-\]\s+", "-]", body)                            # [ḥ-r-] p -> [ḥ-r-]p
    body = re.sub(r"\[([^\]:]*?)\s*:\]", r"[\1] :", body)          # g-[e :] -> g-[e] :
    body = re.sub(r"-\s+((?:\.\s+)+)(?=\S)", lambda m: "-" + m.group(1).replace(" ", "") + "-", body)   # a- . . . m
    return body


def units(word):
    """The units of one of his words: [(unit, unsure)], unit as printed (lower case), unsure when he queries it or
    restores it. A prime after a unit is a unit of its own (')."""
    out, bracket = [], False
    word = re.sub(r"\](?=[^\s\-\]])", "]-", word)            # [ḥ-r-]p: the p after the bracket is his own
    for part in [p for p in word.split("-") if p != ""]:
        unsure = "(?)" in part
        if part.startswith("["):
            bracket = True
        here = bracket or "[" in part or "]" in part
        if "]" in part:
            bracket = False
        p = re.sub(r"[\[\]]|\(\?\)", "", part)
        p = unicodedata.normalize("NFC", p).lower()
        if not p:
            continue
        if set(p) <= {"."}:
            out += [(".", True)] * len(p)
            continue
        primes = p.count("'")
        core = p.replace("'", "")
        if core:
            out.append((core, unsure or here))
        out += [("'", unsure or here)] * primes
    return out


def split(core):
    """A unit in his letters as Griffith's signs: a unit of the table, else letter by letter (pi -> p i)."""
    if core in SIGNS:
        return [SIGNS[core]]
    out, k = [], 0
    while k < len(core):
        for d in DIGRAPHS:
            if core.startswith(d, k):
                out.append(SIGNS[d])
                k += len(d)
                break
        else:
            out.append(SIGNS.get(core[k], "?"))
            k += 1
    return out


def words(src=None):
    """Every word in the order of the stela: [{line, printed, units, griffith, corpus, doubt, kind}]. kind: word,
    numeral or lost. A word cut by a hyphen at the end of a line goes on into the next line and is of the first."""
    out, carry = [], None
    for n, body in (lines() if src is None else src):
        toks = [t for t in re.split(r"[:\s]+", tidy(body)) if t]
        for k, t in enumerate(toks):
            if carry is not None:
                t, n_word = carry[0] + t, carry[1]
                carry = None
            else:
                n_word = n
            if k == len(toks) - 1 and t.endswith("-") and not t.endswith("]-"):
                carry = (t, n_word)
                continue
            if t == "(?)":
                if out:
                    out[-1]["doubt"] = "; ".join(filter(None, [out[-1]["doubt"], "(?) after it"]))
                continue
            if ROMAN.fullmatch(t):
                out.append({"line": n_word, "printed": t, "units": [], "griffith": t, "corpus": t, "doubt": "",
                            "kind": "numeral"})
                continue
            us = units(t)
            if all(u == "." for u, _ in us):
                out.append({"line": n_word, "printed": t, "units": [], "griffith": "", "corpus": "." * len(us),
                            "doubt": "", "kind": "lost"})
                continue
            signs = [(s, unsure) for u, unsure in us for s in (["."] if u == "." else split(u))]
            g = "".join(s for s, _ in signs)
            out.append({"line": n_word, "printed": t, "units": [u for u, _ in us], "griffith": g,
                        "corpus": A.to_corpus(g), "signs": signs,
                        "doubt": "(?) or [ ] on a sign" if any(x for _, x in signs) else "", "kind": "word"})
    if carry:
        raise SystemExit(f"a word runs on past the last line: {carry[0]}")
    return out


# ------------------------------------------------------------------------------------------ the comparison

def strict(text):
    """The corpus spelling as it stands, x and X one letter."""
    return re.sub(r"[^A-Za-z0-9]", "", text.replace("X", "x"))


def as_akinidad(ws):
    """Words in the shape src/akinidad.py compare() takes (corpus, line), numerals turned to digits."""
    out = []
    for w in ws:
        if w["kind"] == "lost":
            continue
        c = str(roman(w["corpus"])) if w["kind"] == "numeral" else w["corpus"]
        out.append({"line": w["line"], "corpus": c, "printed": w["printed"], "doubt": w["doubt"]})
    return out


def roman(s):
    vals = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}
    total = 0
    for k, c in enumerate(s):
        v = vals[c]
        total += -v if k + 1 < len(s) and vals[s[k + 1]] > v else v
    return total


def stream(ws, spell):
    """(the letters of the words in one string, [index of the word of each letter])."""
    s, owner = "", []
    for k, w in enumerate(ws):
        f = spell(w["corpus"])
        s += f
        owner += [k] * len(f)
    return s, owner


def aligned(a_ws, b_ws, spell):
    """For each word of a: the letters of b lined up with it (difflib over the whole texts), and whether all its
    letters lie in shared stretches."""
    a, a_own = stream(a_ws, spell)
    b, _ = stream(b_ws, spell)
    seg, good = collections.defaultdict(list), [True] * len(a_ws)
    shared = [False] * len(a)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for d in range(i2 - i1):
                shared[i1 + d] = True
                seg[a_own[i1 + d]].append(j1 + d)
        elif tag == "replace":
            for i in range(i1, i2):
                seg[a_own[i]] += list(range(j1, j2))
    for i, k in enumerate(a_own):
        good[k] = good[k] and shared[i]
    out = []
    for k, w in enumerate(a_ws):
        js = sorted(set(seg.get(k, [])))
        out.append({"word": w, "agrees": good[k] if spell(w["corpus"]) else None,
                    "other": "".join(b[j] for j in js), "at": js})
    return out, b


def by_line(result):
    c = collections.defaultdict(lambda: [0, 0])
    for x in result:
        if x["agrees"] is None:
            continue
        c[x["word"]["line"]][1] += 1
        c[x["word"]["line"]][0] += bool(x["agrees"])
    return {str(k): {"agree": v[0], "words": v[1]} for k, v in sorted(c.items())}


def unsure_at(s_ws, spell):
    """For each letter of Sayce's stream: whether it is a sign he queries or restores, or lies in a lost stretch."""
    flags = []
    for w in s_ws:
        if w["kind"] == "numeral":
            flags += [False] * len(spell(str(roman(w["corpus"]))))
            continue
        if w["kind"] != "word":
            continue
        for g, unsure in w["signs"]:
            flags += [unsure or g == "."] * len(spell(A.to_corpus(g)))
    return flags


def doubted(g_ws, s_ws, closed=None):
    """Griffith's doubted words, each with Sayce's letters at the same place and its class."""
    gw = [w for w in g_ws if A.counted(w)]
    sw = [w for w in s_ws if w["kind"] != "lost"]
    res, _ = aligned(gw, as_akinidad(sw), strict)
    flags = unsure_at(sw, strict)
    vs = {}
    if closed:
        for key, text in closed.items():
            cl = [{"line": 0, "corpus": x} for x in text.split()]
            g_res, _ = aligned(gw, cl, A.fold)
            s_res, _ = aligned(as_akinidad(sw), cl, A.fold)
            vs[key] = (g_res, s_res)
    out = []
    for k, x in enumerate(res):
        w = x["word"]
        if not w["doubt"]:
            continue
        other = x["other"]
        unsure = any(flags[j] for j in x["at"] if j < len(flags))
        if not other:
            cls = "not found"
        elif unsure:
            cls = "also unsure"
        elif other == strict(w["corpus"]):
            cls = "confirms"
        else:
            cls = "reads otherwise"
        item = {"line": w["line"], "griffith": w["printed"], "doubt": w["doubt"], "sayce": other, "class": cls}
        for key, (g_res, s_res) in vs.items():
            g_ok = bool(g_res[k]["agrees"])
            s_ok = None
            if x["at"]:
                s_stream, s_own = stream(as_akinidad(sw), strict)
                s_words = {s_own[j] for j in x["at"] if j < len(s_own)}
                s_ok = all(s_res[i]["agrees"] for i in s_words if s_res[i]["agrees"] is not None)
            item[key] = "both" if g_ok and s_ok else "Griffith" if g_ok else "Sayce" if s_ok else "neither"
        out.append(item)
    return out


def unit_table(g_ws, s_ws):
    """{his unit: {Griffith's sign it lines up with: count}}: each of his signs lined up with Griffith's signs in
    the stretches where the two agree or are replaced one for one (difflib over sign lists)."""
    gs = [s for w in g_ws if A.counted(w) for s in A.SIGN.findall(A.plain(w["griffith"]).lower())
          if not re.fullmatch(r"[\d·.]", s)]
    ss, us = [], []
    for w in s_ws:
        if w["kind"] != "word":
            continue
        for u in w["units"]:
            if u == ".":
                continue
            for s in split(u):
                ss.append(s)
                us.append(u)
    gs = [s.lower() for s in gs]
    table = collections.defaultdict(collections.Counter)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ss, gs, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for d in range(i2 - i1):
                table[us[i1 + d]][gs[j1 + d]] += 1
    return {u: dict(c.most_common()) for u, c in sorted(table.items())}


def blind(first=None, second=None):
    """Sayce's lot typed twice: his letters (units) of the two typings lined up line by line."""
    first = dict(lines()) if first is None else first
    if second is None:
        if not BLIND.exists():
            return None
        second = dict(lines(BLIND.read_text(encoding="utf-8")))
    per, tot = {}, [0, 0, 0]
    for n in LOT:
        a = [u for w in words([(n, first[n])]) for u in w["units"] + ([w["printed"]] if w["kind"] == "numeral" else [])]
        b = [u for w in words([(n, second[n])]) for u in w["units"] + ([w["printed"]] if w["kind"] == "numeral" else [])]
        m = difflib.SequenceMatcher(None, a, b, autojunk=False)
        same = sum(blk.size for blk in m.get_matching_blocks())
        per[str(n)] = {"units": len(a), "units_second": len(b), "agree": same, "identical": first[n] == second[n]}
        tot = [tot[0] + same, tot[1] + len(a), tot[2] + len(b)]
    share = min(tot[0] / tot[1], tot[0] / tot[2])
    return {"lot": list(LOT), "bar": BAR, "units_first": tot[1], "units_second": tot[2], "agree": tot[0],
            "share": round(share, 4), "met": share >= BAR, "lines": per}


def figures(s_ws=None, g_ws=None, closed=None):
    s_ws = words() if s_ws is None else s_ws
    g_ws = A.words() if g_ws is None else g_ws
    sw = as_akinidad(s_ws)
    gw = [w for w in g_ws if A.counted(w)]
    out = {"sayce": {"lines": len({w["line"] for w in s_ws}), "words": sum(1 for w in s_ws if w["kind"] == "word"),
                     "numerals": sum(1 for w in s_ws if w["kind"] == "numeral"),
                     "signs": sum(len(w["signs"]) for w in s_ws if w["kind"] == "word"),
                     "words_unsure": sum(1 for w in s_ws if w["kind"] == "word" and w["doubt"])},
           "how": "both texts in the corpus spelling, lined up letter by letter (difflib) over the whole text; a "
                  "word agrees when all its letters lie in stretches the two share. folded: src/akinidad.py fold(); "
                  "strict: the corpus letters as they stand, x and X one letter. units: how often each of his "
                  "units lines up with each of Griffith's signs where the two agree or are replaced one for one",
           "against_griffith": {}, "units": unit_table(g_ws, s_ws)}
    for name, spell in (("folded", A.fold), ("strict", strict)):
        res, _ = aligned(sw, gw, spell)
        rev, _ = aligned(gw, sw, spell)
        out["against_griffith"][name] = {
            "sayce_words": sum(1 for x in res if x["agrees"] is not None),
            "sayce_words_agree": sum(1 for x in res if x["agrees"]),
            "griffith_words": sum(1 for x in rev if x["agrees"] is not None),
            "griffith_words_agree": sum(1 for x in rev if x["agrees"]),
            "by_line": by_line(res)}
    ds = doubted(g_ws, s_ws, closed)
    out["doubted"] = {"words": len(ds), "by_class": dict(collections.Counter(d["class"] for d in ds)),
                      "places": [{k: v for k, v in d.items() if k in ("line", "griffith", "doubt", "sayce", "class")}
                                 for d in ds]}
    if closed:
        out["against_closed"] = {}
        for key, text in closed.items():
            cl = [{"line": 0, "corpus": x} for x in text.split()]
            res, _ = aligned(sw, cl, A.fold)
            n = sum(1 for x in res if x["agrees"] is not None)
            a = sum(1 for x in res if x["agrees"])
            out["against_closed"][key] = {"sayce_words": n, "agree": a, "share": round(a / n, 3),
                                          "doubted_sides_with": dict(collections.Counter(d[key] for d in ds))}
    b = blind()
    if b is not None:
        out["second_typing"] = b
    return out


def main(argv):
    if argv[1:]:
        sys.exit(__doc__)
    s_ws = words()
    WORDS.write_text("[\n" + ",\n".join(json.dumps({k: w[k] for k in ("line", "printed", "griffith", "corpus", "doubt",
                                                                    "kind")}, ensure_ascii=False) for w in s_ws)
                     + "\n]\n", encoding="utf-8")                          # one word a line
    closed = A.closed_readings()
    figs = figures(s_ws, closed=closed)
    if closed is None:            # the closed readings are not here: keep the counts that need them as they are
        old = json.loads(COMPARISON.read_text()) if COMPARISON.exists() else {}
        figs = {k: v for k, v in old.items() if k == "against_closed"} | figs
    COMPARISON.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    s = figs["sayce"]
    print(f"Sayce: {s['words']} words on {s['lines']} lines, {s['signs']} signs, {s['numerals']} numerals")
    for name, v in figs["against_griffith"].items():
        print(f"  {name}: {v['sayce_words_agree']} of {v['sayce_words']} of his words agree with Griffith's text; "
              f"{v['griffith_words_agree']} of {v['griffith_words']} of Griffith's with his")
    print("  Griffith's doubted words:", figs["doubted"]["by_class"])
    for key, v in figs.get("against_closed", {}).items():
        print(f"  against {key}: {v['agree']} of {v['sayce_words']} ({v['share']:.1%}); doubted words side with "
              f"{v['doubted_sides_with']}")
    if "second_typing" in figs:
        b = figs["second_typing"]
        print(f"  second typing of ll. {b['lot']}: {b['agree']} of {b['units_first']} units ({b['share']:.1%}); "
              f"bar {'met' if b['met'] else 'MISSED'}")


if __name__ == "__main__":
    main(sys.argv)
