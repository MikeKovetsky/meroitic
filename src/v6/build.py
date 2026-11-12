"""corpus_v6: one row per inscription, with real names and a source for every reading.

  python3 -I src/v6/build.py            build the table, the map and data/corpus_v6.jsonl, and print the measures

Local only (it reads Otten's files, the Newsletter texts and the two editions' text layers). What it writes:

  data/sources/v6/inscriptions.jsonl    every inscription with every reading held, texts included (local)
  data/sources/v6/lines.jsonl           every source line of Otten's per-scholar files with what it is (local)
  data/sources/v6/map.jsonl             every id of corpus_v5: what it is, of which inscription, on what evidence
  data/sources/v6/pending.jsonl         the doubtful matches that wait for two readers
  data/sources/v6/figures.json          the measures
  data/corpus_v6.jsonl                  one row per inscription that has a typed reading (local)

How an inscription is made (data/discovery/corpus_v6.md has the method and the bar):

1. Numbers first. Readings that share a number of one system (REM, Millet's GA, Griffith's) are one inscription;
   two readings with two different numbers of one system are two, however alike their letters (a stela and an
   offering table of one person). A number an edition gives for its text counts (FHN names the REM numbers of
   each entry, and joins two for a text in two pieces).
2. Letters for what has no number: Otten's three narratives and the source lines of his per-scholar files, by the
   rule of src/v6/readings.py. A sure match to one inscription only stands; a sure match with a second inscription
   close behind, and every doubtful one, waits for two readers (data/sources/v6/readers/verdicts.jsonl).
3. A source line that holds half or more of an inscription's own runs is a reading of it; one that holds less,
   or stands whole in a held text, is an example phrase from a grammar; a line of 40 letters or more that matches
   nothing held is an inscription not identified; the rest are example phrases whose source is not held.
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(Path(__file__).resolve().parent)]
import otten as O      # noqa: E402
import prepare as P    # noqa: E402
import readings as R   # noqa: E402

OUT = ROOT / "data/sources/v6"
CORPUS = ROOT / "data/corpus_v6.jsonl"
VERDICTS = OUT / "readers" / "verdicts.jsonl"
READING = 0.5        # a line that holds this share of an inscription's own runs is a reading of it
CLOSE = 0.5          # a second inscription that shares this much of what the best one shares makes a match unsure
OWN_TEXT = 40        # letters from which a line that matches nothing is an inscription of its own
READABLE = 15        # letters from which a doubtful match is worth a reader
LOOSE = 3            # shared own runs from which a long line that matches nothing still gets a reader
DOUBT_SHARE = 0.3    # ... when the line holds this share of an inscription's own runs (it may be a reading)
WHOLE = 0.8          # a reading with this share of the longest typed reading's letters gives the whole text
ORDER = ("otten-narrative", "otten", "griffith", "karanog", "mnl-print", "mnl-printout")   # the preferred reading
SYSTEMS = ("rem", "ga", "griffith", "meroe", "shablul", "karanog", "mnl")
HELD_BY = "read side by side on 2026-11-12 (src/experts/prepare.py, HELD)"
READ = "two readers who saw both texts"
READ_NONE = "two readers who saw both texts: none of the candidates"
SET_ASIDE = "set aside: two readers took it for a text of this inscription, and the rule matches it surely with"

DECREE = "wtelipkeli"      # the opening formula of the oracular decrees, after the first word (a name or a title)
KINDS = (
    ("oracular decree", r"oracular|amuletic|decree"),
    ("document (ostracon, papyrus, wood, vessel)", r"ostrac|papyr|wooden|wood |leather|amphora|dipinto|\bjar\b|bowl|sherd"),
    ("graffito", r"graffit|proskynema|adoration|scratched|rock"),
    ("funerary", r"offering[- ]?table|table of offerings|altar|funerary|epitaph|tomb|grave|\bba[- ]statue|lintel"),
    ("royal or temple (stela, wall, cartouche, label)",
     r"cartouche|label|legend|relief|wall|column|pylon|gateway|statue|\bram\b|bark|plaque|votive|dedicat|obelisk|"
     r"temple|chapel|pyramid|king|queen|royal"),
    ("funerary", r"stela|stele"),
)
ISIS, OSIRIS = re.compile(r"^a?w?o?S"), re.compile(r"^a?Sor")


def kind_of(objects, text):
    """(kind, why) of an inscription from the descriptions of its object and the opening of its text: an epitaph
    opens with the names of Isis and Osiris."""
    first = (text or "").split()[:4]
    if any(ISIS.match(w) and "wo" in w[:3] for w in first) and any(OSIRIS.match(w) for w in first):
        return "funerary", "the text opens with the invocation of Isis and Osiris"
    if DECREE in R.reduced(" ".join((text or "").split()[:8])):
        return "oracular decree", "the text opens with the formula of the oracular decrees (wteli pkeli)"
    described = " ; ".join(o for o in objects if o).lower()
    for kind, pattern in KINDS:
        m = re.search(pattern, described)
        if m:
            return kind, f"the object is described as \"{m.group(0).strip()}\""
    return "not known", ""


def words(text):
    """The words of a text of corpus_v6: a stretch of lost signs that stands alone is not one."""
    return [w for w in (text or "").split() if w.strip(".…")]


# ------------------------------------------------------------------------------------------ inscriptions

class Groups:
    """Readings joined into inscriptions (a union-find over reading keys)."""

    def __init__(self, keys):
        self.up = {k: k for k in keys}

    def find(self, k):
        while self.up[k] != k:
            self.up[k] = self.up[self.up[k]]
            k = self.up[k]
        return k

    def join(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.up[max(a, b)] = min(a, b)

    def sets(self):
        out = collections.defaultdict(list)
        for k in self.up:
            out[self.find(k)].append(k)
        return dict(out)


def same_as_key(row, by_mnl):
    """The Newsletter row that src/mnl/mnl_dedupe.py kept for the inscription of `row` (same_as), or None."""
    if not row.get("same_as"):
        return None
    name = row["same_as"].split(" and the rest of that edition")[0]
    name = re.sub(r" \(Meroitic Newsletter \d+ \(\d{4}\)\)$", "", name)
    kept = [o for o in by_mnl.get(name, []) if o["key"] != row["key"]]
    return kept[0]["key"] if kept else None


def by_number(editions):
    """The edition readings joined by the numbers they give. Returns (groups, [(key, key, why)])."""
    g, why = Groups(r["key"] for r in editions), []
    seen = {}
    for r in editions:
        for system in SYSTEMS:
            for value in r["numbers"].get(system, ()):
                first = seen.setdefault((system, value), r["key"])
                if first != r["key"]:
                    g.join(first, r["key"])
                    why.append((first, r["key"], f"both are {system.upper() if system in ('rem', 'ga') else system} {value}"))
    by_mnl = collections.defaultdict(list)
    for r in editions:
        if r["family"] == "mnl":
            by_mnl[r["mnl_id"]].append(r)
    for r in editions:
        kept = same_as_key(r, by_mnl) if r["family"] == "mnl" else None
        if kept:
            g.join(r["key"], kept)
            why.append((r["key"], kept, "two editions of one text in the Newsletter (src/mnl/mnl_dedupe.py)"))
    return g, why


def name_of(rs):
    """The id of an inscription from the numbers of its readings: its REM numbers, else Millet's GA number, else
    Griffith's number, else the Newsletter's own."""
    nums = collections.defaultdict(set)
    for r in [r for r in rs if not r.get("superseded")] or rs:
        for system, values in r["numbers"].items():
            nums[system].update(values)
    for system, label in (("rem", "REM"), ("ga", "GA"), ("griffith", "Inscr."), ("meroe", "Meroe"), ("shablul", "Sh."),
                          ("karanog", "Kar."), ("mnl", "")):
        if nums[system]:
            return f"{label} {'+'.join(sorted(nums[system]))}".strip()
    return ""


def source_rank(r):
    if r["family"] == "otten":
        return ORDER.index("otten-narrative" if r.get("narrative") else "otten")
    if r["family"] == "mnl":
        return ORDER.index("mnl-printout" if r.get("printout") else "mnl-print")
    return ORDER.index(r["family"])


def year(r):
    """The year of the edition a reading is from (0 for Otten's narrative files, which name none)."""
    m = re.search(r"\b(1[89]\d\d|20\d\d)\b", r["work"])
    return int(m.group(1)) if m else 0


def stream(text):
    """A text as one string of reduced letters with its numerals kept: for finding a word before a numeral."""
    return "".join(w if w.isdigit() else R.reduced(w) for w in words(text))


def numerals(text, others):
    """The text with a lone `l` read as the numeral that a later edition of the same inscription has after the same
    word. others: the texts of the readings from a later edition. Each lone `l` is compared through the last
    letters of the word before it: the later edition has a numeral there (confirmed), the letter l (kept), or the
    place cannot be found (lost or read otherwise). Where two or more are confirmed and none is kept, one that
    cannot be found is read as the numeral 1 too when the word after it is the word after a confirmed one: the
    same list goes on ("pesto X 1 pesto Y 1"). Returns (text, [(place, word before, numeral, "a later edition"
    or "by analogy")])."""
    ws = text.split()
    streams = [stream(o) for o in others if re.search(r"\d", o or "")]
    lone = [i for i in range(1, len(ws)) if ws[i] == "l" and not ws[i - 1].isdigit()]
    confirmed, kept, unknown = [], [], []
    for i in lone:
        tail = R.reduced(ws[i - 1])[-5:]
        hit = None
        for s in streams if len(tail) >= 4 else ():
            if re.search(re.escape(tail) + r"l(?!o)", s):
                hit = "l"
                break
            m = re.search(re.escape(tail) + r"(\d+)", s)
            if m:
                hit = m.group(1)
                break
        (kept if hit == "l" else confirmed if hit else unknown).append((i, hit))
    fixed = [(i, ws[i - 1], n, "a later edition") for i, n in confirmed]
    after = {ws[i + 1] for i, _ in confirmed if i + 1 < len(ws)}
    if len(confirmed) >= 2 and not kept:
        fixed += [(i, ws[i - 1], "1", "by analogy") for i, _ in unknown if i + 1 < len(ws) and ws[i + 1] in after]
    for i, _, n, _ in fixed:
        ws[i] = n
    return " ".join(ws), sorted(fixed)


def apart(a, b):
    """Two readings of one inscription are two parts of it (two sides, two pieces) when neither holds a run of the
    other and neither's letters stand in the other's."""
    return bool(a["letters"]) and bool(b["letters"]) and not (R.runs(a["letters"]) & R.runs(b["letters"])) \
        and a["letters"] not in b["letters"] and b["letters"] not in a["letters"]


def prefer(rs):
    """(the preferred reading, its further parts, the open reading or None) of an inscription's readings.

    Of the typed readings that give the whole text (WHOLE of the longest one's letters; not a part Griffith
    printed, not a reconstruction), the first in ORDER, then the latest, then the longest. A typed reading that
    shares nothing with it and with the parts already taken is a further part (the other side of a label, the
    second piece of a broken table), taken in the same order."""
    typed = [r for r in rs if r["typed"] and words(r["text"]) and not r.get("reconstruction")]
    typed = [r for r in typed if not r.get("superseded")] or typed
    if not typed:
        return None, [], None
    rank = lambda r: (source_rank(r), -year(r), -len(r["letters"]), r["key"])
    longest = max(len(r["letters"]) for r in typed)
    whole = [r for r in typed if len(r["letters"]) >= WHOLE * longest and r.get("whole") is not False] or \
            [r for r in typed if len(r["letters"]) >= WHOLE * longest] or typed
    best = min(whole, key=rank)
    parts = []
    for r in sorted(typed, key=rank):
        if r is not best and all(apart(r, o) for o in [best] + parts):
            parts.append(r)
    parts.sort(key=lambda r: r["key"])
    opens = [r for r in typed if r["open"]]
    open_ = min(opens, key=lambda r: (r.get("whole") is False, -len(r["letters"]), r["key"])) if opens else None
    return best, parts, open_


# ------------------------------------------------------------------------------------------ source lines

def candidates(x, editions, group_of, skip, floor=R.FLOOR):
    """The inscriptions a text matches, the best first: [(verdict, share of x, share of the other, shared, key of
    the best reading, group, letters of x over letters of that reading)], one per inscription. A reconstruction
    is no candidate."""
    letters = {r["key"]: len(r["letters"]) for r in editions}
    best = {}
    for m in R.matches(x, [r for r in editions if not r.get("reconstruction")], skip, top=0, floor=floor):
        g = group_of(m[4])
        if g not in best:
            best[g] = m + (g, round(len(x["letters"]) / max(letters[m[4]], 1), 3))
    return list(best.values())


def is_reading(m):
    """A text that matches an inscription is a reading of it when it holds half of the inscription's own runs, or
    is half as long as the reading it matches (a text layer's stray letters lower the first share)."""
    return m[2] >= READING or m[6] >= READING


def decide(x, cands, whole_in, held=None, loose=()):
    """What a text without a number is, from its candidates: (class, group or None, the match, confirmed by).

    class: "reading"; "phrase" (an example phrase: part of the group, found whole in whole_in, or with a doubtful
    match that could only make it a phrase); "pending" (a doubtful match, or a sure one with a second inscription
    close behind, that could make the text a reading or leaves a text of OWN_TEXT letters without a home: for two
    readers); or "" (matches nothing). held: the match that an earlier side-by-side reading settled. loose: the
    candidates under the rule's floor (LOOSE shared runs or more), which a line of OWN_TEXT letters that matches
    nothing else still gets read against, before it is called an inscription of its own."""
    if held is not None:
        return "reading", held[5], held, HELD_BY
    sure = [c for c in cands if c[0] == "sure"]
    if sure:
        top = sure[0]
        rival = next((c for c in cands if c[5] != top[5] and c[3] >= CLOSE * top[3]), None)
        if rival is None:
            return ("reading" if is_reading(top) else "phrase"), top[5], top, "the rule: a sure match to one inscription"
    elif len(whole_in) == 1:
        return "phrase", whole_in[0], None, "its letters stand whole in one held text"
    elif whole_in:
        return "phrase", None, None, f"its letters stand whole in {len(whole_in)} held texts"
    if not cands:
        return ("pending", None, loose[0], "") if loose and len(x["letters"]) >= OWN_TEXT else ("", None, None, "")
    if len(x["letters"]) >= OWN_TEXT or (len(x["letters"]) >= READABLE and any(c[2] >= DOUBT_SHARE or c[6] >= READING for c in cands[:3])):
        return "pending", None, cands[0], ""
    return "phrase", None, cands[0], "a doubtful match that was not read: a phrase whichever text it is from"


def settle(decision, cands, verdict, group_of):
    """A pending decision after the two readers: verdict is (the reading key both named or "", whether the line is
    only a part of that text), or None while they have not settled it. A line both took for the whole text is a
    reading of that inscription, one they took for a part is an example phrase from it, and one for which both
    found no candidate matches nothing (and may then be an inscription of its own)."""
    cls, g, m, by = decision
    if cls != "pending" or verdict is None:
        return decision
    same, part = verdict
    if not same:
        return "", None, None, READ_NONE
    g = group_of(same)
    return ("phrase" if part else "reading"), g, next((c for c in cands if c[5] == g), None), READ


def read_verdicts(path=VERDICTS):
    """{reading key of a line: (the reading key that the two readers both named, or "" when both said none; whether
    both took the line for a part of that text only)} of the doubtful matches that both readers settled alike."""
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text().splitlines():
        if line.strip():
            v = json.loads(line)
            out[v["line"]] = (v["same_as"], bool(v.get("part")))
    return out


# ------------------------------------------------------------------------------------------------ build

def build(verdicts=None):
    lines = O.source_lines()
    raws = O.raw_lines()
    derived = O.derive(raws, lines)
    v5 = [json.loads(l) for l in R.V5.read_text().splitlines() if l.strip()]
    traced = O.trace(v5, raws, *O.pools())
    v5_sources = O.sources_of(traced, derived)
    editions, narratives, olines = R.load(lines)
    skip = R.formulae(editions)
    verdicts = read_verdicts() if verdicts is None else verdicts
    by_key = {r["key"]: r for r in editions + narratives + olines}

    groups, why = by_number(editions)
    for r in editions:                                           # an edition that names two REM numbers joins them
        rems = r["numbers"].get("rem", [])
        if r["family"] == "fhn" and len(rems) > 1:
            first = next((e["key"] for e in editions if e["key"] != r["key"] and rems[0] in e["numbers"].get("rem", ())), None)
            for other in rems[1:]:
                o = next((e["key"] for e in editions if e["key"] != r["key"] and other in e["numbers"].get("rem", ())), None)
                if first and o:
                    groups.join(first, o)
                    why.append((first, o, f"{r['number']} prints REM {rems[0]} and REM {other} as one text in two pieces"))
    group_of = groups.find

    # the texts that an earlier side-by-side reading settled: Millet's and FHN's entries against corpus_v5 texts
    held = {}
    first_source = {tid: v[0][0] for tid, v in v5_sources.items() if v}
    by_v5 = {r["v5"]: r["key"] for r in editions + narratives if r.get("v5")}
    for source, table in P.HELD.items():
        for entry, tid in table.items():
            ed = f"millet2005:{entry}" if source == "millet" else f"fhn:{entry}"
            ours = by_v5.get(tid) or (f"otten:{first_source[tid]}" if tid in first_source else None)
            if ours and ed in by_key:
                held[ours] = ed
    for ours, ed in held.items():                                # an edition row held against an edition entry
        if ours in groups.up and ed in groups.up:
            groups.join(ours, ed)
            why.append((ours, ed, HELD_BY))

    # the narratives and the source lines against the inscriptions
    decided = {}
    for x in narratives + olines:
        line = x.get("line")
        if line and line["file"] == "LobbanVocabList.txt":
            decided[x["key"]] = ("word list", None, None, "an entry of Lobban's word list")
            continue
        if not x["letters"]:
            decided[x["key"]] = ("phrase", None, None, "no letters (an ending or a sign)")
            continue
        cands = candidates(x, editions, group_of, skip)
        whole_in = sorted({group_of(k) for k in R.stands_in(x, editions)})
        want = None
        if x["key"] in held:
            y = by_key[held[x["key"]]]
            v, sa, sb, n = R.rule(x["letters"], y["letters"], skip, floor=1)
            want = (v, sa, sb, n, y["key"], group_of(y["key"]), round(len(x["letters"]) / max(len(y["letters"]), 1), 3))
        loose = candidates(x, editions, group_of, skip, floor=LOOSE) if not cands and len(x["letters"]) >= OWN_TEXT else ()
        d = settle(decide(x, cands, whole_in, want, loose), cands + list(loose), verdicts.get(x["key"]), group_of)
        if d[3] == READ and d[2] is None:                        # the readers named a text the rule did not offer
            y = by_key[verdicts[x["key"]][0]]
            v, sa, sb, n = R.rule(x["letters"], y["letters"], skip, floor=1)
            d = (d[0], d[1], (v, sa, sb, n, y["key"], d[1], round(len(x["letters"]) / max(len(y["letters"]), 1), 3)), d[3])
        decided[x["key"]] = d

    # what matches nothing held: the long lines are inscriptions of their own, the rest are parts of those or phrases
    loose = [x for x in olines if decided[x["key"]][0] == ""]
    read_none = {x["key"] for x in loose if decided[x["key"]][3] == READ_NONE}
    seeds = []
    for x in sorted(loose, key=lambda x: (-len(x["letters"]), x["key"])):
        if len(x["letters"]) < OWN_TEXT:
            break
        hit = None
        for s in seeds:
            v, sa, sb, n = R.rule(x["letters"], s["letters"], skip)
            if v == "sure" or x["letters"] in s["letters"]:
                hit = (s, (v or "whole", sa, sb, n, s["key"], s["key"], round(len(x["letters"]) / len(s["letters"]), 3)))
                break
        if hit:
            s, m = hit
            decided[x["key"]] = ("reading" if is_reading(m) else "phrase", s["key"], m,
                                 "the rule: a sure match to a longer line that matches nothing held")
        else:
            seeds.append(x)
            decided[x["key"]] = ("unidentified", x["key"], None, f"{OWN_TEXT} letters or more, matching nothing held")
    for x in loose:
        if decided[x["key"]][0] != "":
            continue
        inside = [s for s in seeds if len(x["letters"]) >= 6 and x["letters"] in s["letters"]]
        part = [(s, R.rule(x["letters"], s["letters"], skip)) for s in seeds]
        part = [(s, r) for s, r in part if r[0] == "sure"]
        if len(inside) == 1:
            decided[x["key"]] = ("phrase", inside[0]["key"], None, "its letters stand whole in a line that matches nothing held")
        elif len(part) == 1:
            s_, r = part[0]
            decided[x["key"]] = ("phrase", s_["key"], r + (s_["key"], s_["key"], round(len(x["letters"]) / len(s_["letters"]), 3)),
                                 "the rule: a sure match to a line that matches nothing held")
        else:
            decided[x["key"]] = ("phrase", None, None, "matches nothing held")
    # A line the readers took for the text of an inscription, and that the rule matches surely with a line that is
    # an inscription of its own: two quotations run together on one line, or a parallel. The readers saw the
    # candidates of the editions, not that line. It is a phrase of neither, so that no text stands in two rows.
    for x in olines:
        cls, g, m, by = decided[x["key"]]
        if cls != "reading" or by != READ:
            continue
        other = next((s_ for s_ in seeds if R.rule(x["letters"], s_["letters"], skip)[0] == "sure"), None)
        if other is not None:
            l = other["line"]
            decided[x["key"]] = ("phrase", None, m, f"{SET_ASIDE} the text of Millet 1968 p. {l['page'] or '?'} ({l['file']} line {l['line']})")
    for key in read_none:                                        # what the readers found stays on the record
        cls, g, m, by = decided[key]
        decided[key] = (cls, g, m, f"{by}; {READ_NONE}")

    # the inscriptions: the numbered groups, with the narratives and lines that are readings of them, and the seeds
    members = collections.defaultdict(list)
    for root, keys in groups.sets().items():
        members[root] = [by_key[k] for k in keys]
    for x in narratives + olines:
        cls, g, m, by = decided[x["key"]]
        if cls in ("reading", "unidentified") and g is not None:
            members[g].append(x)
    # the names: the spellings of the lines that Otten's files tag as a person's name (ANTHROPONYM, ROYAL NAME, NAME)
    name_spellings = [s for l in lines if l["file"] != "LobbanVocabList.txt" and ("ANTHROPONYM" in l["tag"] or "NAME" in l["tag"])
                      for s in O.spellings(l)]
    inscriptions, id_of = [], {}
    for root, rs in members.items():
        rs = sorted(rs, key=lambda r: (source_rank(r) if r["typed"] else 9, r["key"]))
        iid = name_of(rs)
        if not iid:
            l = next(r["line"] for r in rs if r.get("line"))
            iid = f"Millet 1968 p. {l['page'] or '?'} ({l['file']} line {l['line']})"
        best, parts, open_ = prefer(rs)
        text, fixes, marked = None, [], []
        if best:
            later = [r["text"] for r in rs if r is not best and r["typed"] and year(r) > year(best) > 0]
            text, fixes = numerals(" ".join(w for r in [best] + parts for w in words(r["text"])), later)
            if any(r["family"] == "otten" for r in rs):
                marked = O.name_words(text, name_spellings)
        sites = [r["site"] for r in sorted(rs, key=lambda r: ("griffith karanog fhn millet2005 mnl otten".split().index(r["family"])))
                 if r["site"] and not r["site"].lower().startswith("not stated")]
        kind, kind_why = kind_of([r["object"] for r in rs], text or "")
        ins = {"id": iid, "rem": sorted({v for r in rs for v in r["numbers"].get("rem", ())}),
               "numbers": {s: sorted({v for r in rs for v in r["numbers"].get(s, ())}) for s in SYSTEMS + ("fhn",)
                           if any(r["numbers"].get(s) for r in rs)},
               "site": sites[0] if sites else "", "kind": kind, "kind_by": kind_why,
               "preferred": best["key"] if best else None, "parts": [r["key"] for r in parts], "text": text,
               "names": marked, "numerals_set": fixes,
               "open": open_["key"] if open_ else None,
               "open_text": " ".join(words(open_["text"])) if open_ else None,
               "open_whole": (open_.get("whole") is not False) if open_ else None,
               "readings": [{k: r.get(k) for k in ("key", "family", "work", "ref", "number", "licence", "open", "typed",
                                                    "whole", "site", "object", "text")}
                            | {"letters": len(r["letters"]), "words": len(words(r["text"])) if r["text"] else None,
                               "v5": r.get("v5")} for r in rs],
               "_root": root}
        inscriptions.append(ins)
    order = lambda i: (0 if i["rem"] else 1 if "ga" in i["numbers"] else 2 if not i["id"].startswith("Millet 1968") else 3, i["id"])
    inscriptions.sort(key=order)
    if len({i["id"] for i in inscriptions}) != len(inscriptions):
        twice = [k for k, n in collections.Counter(i["id"] for i in inscriptions).items() if n > 1]
        raise SystemExit(f"two inscriptions under one id: {twice}")
    for i in inscriptions:
        id_of[i.pop("_root")] = i["id"]
    return {"lines": lines, "olines": olines, "narratives": narratives, "editions": editions, "v5": v5,
            "derived": derived, "traced": traced, "v5_sources": v5_sources, "decided": decided,
            "inscriptions": inscriptions, "id_of": id_of, "group_of": group_of, "joins": why, "by_key": by_key}


def line_rows(b):
    """The source lines with what each is: [{key, file, line, page, class, inscription, by, shares...}]."""
    out = []
    for x in b["olines"]:
        cls, g, m, by = b["decided"][x["key"]]
        l = x["line"]
        out.append({"key": x["key"], "file": l["file"], "line": l["line"], "page": l["page"], "section": l["section"],
                    "tag": l["tag"], "class": cls, "inscription": b["id_of"].get(g) if g is not None else None,
                    "by": by, "share_of_line": m[1] if m else None, "share_of_text": m[2] if m else None,
                    "shared_runs": m[3] if m else None, "against": m[4] if m else None,
                    "letters": len(x["letters"]), "text": x["text"], "translation": l["translation"]})
    return out


WHAT = {"reading": "a reading of an inscription", "phrase": "an example phrase from a grammar, not an inscription",
        "word list": "an entry of a word list, not an inscription", "unidentified": "an inscription not identified",
        "pending": "not identified: a doubtful match that two readers have not settled"}


def map_rows(b):
    """Every id of corpus_v5: what it is, of which inscription, and the evidence."""
    lines = {r["key"]: r for r in line_rows(b)}
    by_v5 = {r["v5"]: r for r in b["editions"] + b["narratives"] if r.get("v5")}
    ins_of_reading = {r["key"]: i["id"] for i in b["inscriptions"] for r in i["readings"]}
    preferred = {i["preferred"]: i["id"] for i in b["inscriptions"] if i["preferred"]}
    first_row = {}                                             # the text of the older corpus that stands for a line
    for tid, src in sorted(b["v5_sources"].items(), key=lambda kv: (-(kv[1][0][1] if kv[1] else 0), kv[0])):
        if src:
            first_row.setdefault(src[0][0], tid)
    out = []
    for r in b["v5"]:
        tid, n = r["id"], len(r["text"].split())
        row = {"id": tid, "words": n, "copies": r.get("copies", 1)}
        if tid in by_v5:
            x = by_v5[tid]
            cls, g, m, by = b["decided"].get(x["key"], ("reading", None, None, "the row is the edition's own text"))
            row.update({"class": "reading", "what": WHAT["reading"], "inscription": ins_of_reading.get(x["key"]),
                        "reading": x["key"], "by": by, "share_of_text": m[1] if m else None,
                        "share_of_other": m[2] if m else None, "shared_runs": m[3] if m else None,
                        "against": m[4] if m else None, "copy": ""})
        else:
            src = b["v5_sources"].get(tid) or []
            if not src:
                row.update({"class": "not traced", "what": "not identified: no source line", "inscription": None})
                out.append(row)
                continue
            key = f"otten:{src[0][0]}"
            l = lines[key]
            how = collections.Counter(b["derived"][raw][1] for raw in b["traced"][tid] if raw in b["derived"])
            row.update({"class": l["class"], "what": WHAT[l["class"]], "inscription": l["inscription"], "reading": key,
                        "page": l["page"], "source_lines": len(src), "raw_lines": dict(how), "by": l["by"],
                        "share_of_text": l["share_of_line"], "share_of_other": l["share_of_text"],
                        "shared_runs": l["shared_runs"], "against": l["against"],
                        "copy": "" if first_row.get(src[0][0]) == tid else "a copy of its source line with a name swapped"})
        out.append(row)
    # one row of corpus_v5 stands for each inscription: the row of its preferred reading, else its first reading
    stands = {}
    for row in out:
        if row.get("class") in ("reading", "unidentified") and row.get("inscription") and not row.get("copy"):
            key = (row["reading"] not in preferred, row["id"])
            if row["inscription"] not in stands or key < stands[row["inscription"]][0]:
                stands[row["inscription"]] = (key, row["id"])
    kept = {v[1] for v in stands.values()}
    for row in out:
        if row.get("class") in ("reading", "unidentified") and row["id"] not in kept and not row.get("copy"):
            row["copy"] = "another reading of an inscription that a row already stands for"
        row["stands"] = row["id"] in kept
    return out


def corpus_rows(b, mapped):
    """data/corpus_v6.jsonl: one row per inscription with a typed reading."""
    v5_of = collections.defaultdict(list)
    for m in mapped:
        if m.get("inscription") and m.get("class") in ("reading", "unidentified"):
            v5_of[m["inscription"]].append(m["id"])
    out = []
    for i in b["inscriptions"]:
        if not i["text"]:
            continue
        best = next(r for r in i["readings"] if r["key"] == i["preferred"])
        out.append({"id": i["id"], "rem": i["rem"], "site": i["site"], "kind": i["kind"], "reading": i["preferred"],
                    "source": best["work"], "licence": best["licence"], "open": best["open"],
                    "readings": len(i["readings"]), "v5": sorted(v5_of.get(i["id"], [])), "names": i["names"],
                    "text": i["text"]})
    return out


def measures(b, mapped, corpus):
    ins = b["inscriptions"]
    n = len(ins)
    w = lambda rows: sum(r["words"] for r in rows)
    classes = collections.defaultdict(list)
    for m in mapped:
        key = ("stands for its inscription" if m.get("stands") else
               "a second reading of an inscription already counted" if m.get("class") in ("reading", "unidentified") and "another reading" in (m.get("copy") or "") else
               "a name-swapped copy of a reading" if m.get("class") in ("reading", "unidentified") else
               "an example phrase or a word-list entry" if m.get("class") in ("phrase", "word list") and not m.get("copy") else
               "a name-swapped copy of an example phrase" if m.get("class") in ("phrase", "word list") else
               "not settled by two readers" if m.get("class") == "pending" else "not traced")
        classes[key].append(m)
    typed = [i for i in ins if i["text"]]
    return {
        "corpus_v5": {"texts": len(mapped), "words": w(mapped),
                      "classes": {k: {"texts": len(v), "words": w(v)} for k, v in sorted(classes.items())}},
        "inscriptions": {
            "all": n,
            "with_a_typed_reading": len(typed),
            "only_a_text_layer": sum(not i["text"] and not any(r["typed"] for r in i["readings"]) for i in ins),
            "typed_without_a_legible_word": sum(not i["text"] and any(r["typed"] for r in i["readings"]) for i in ins),
            "in_two_or_more_parts": sum(bool(i["parts"]) for i in ins),
            "with_a_rem_number": sum(bool(i["rem"]) for i in ins),
            "with_real_names": len(typed),
            "with_two_readings_or_more": sum(len(i["readings"]) >= 2 for i in ins),
            "with_an_open_reading": sum(bool(i["open"]) for i in ins),
            "with_an_open_reading_of_the_whole_text": sum(bool(i["open"]) and i["open_whole"] for i in ins),
            "preferred_reading_is_open": sum(bool(c["open"]) for c in corpus),
            "in_corpus_v5": sum(bool(c["v5"]) for c in corpus),
            "not_identified": sum(i["id"].startswith("Millet 1968") for i in ins),
            "by_kind": dict(collections.Counter(i["kind"] for i in ins).most_common()),
            "preferred_by_source": dict(collections.Counter(c["reading"].split(":")[0] + (":narrative" if ":narrative:" in c["reading"] else "")
                                                             for c in corpus).most_common()),
        },
        "corpus_v6": {"texts": len(corpus), "words": sum(len(c["text"].split()) for c in corpus),
                      "words_of_inscriptions_in_corpus_v5": sum(len(c["text"].split()) for c in corpus if c["v5"]),
                      "name_words_marked": sum(len(c["names"]) for c in corpus),
                      "numerals_set": sum(len(i["numerals_set"]) for i in ins)},
        "lines": dict(collections.Counter(d[0] for k, d in b["decided"].items() if k.startswith("otten:") and ":narrative:" not in k)),
        "pending": sum(d[0] == "pending" for d in b["decided"].values()),
    }


def pending_rows(b):
    out = []
    for x in b["olines"]:
        cls, g, m, by = b["decided"][x["key"]]
        if cls == "pending":
            skip = R.formulae(b["editions"])
            cands = (candidates(x, b["editions"], b["group_of"], skip)
                     or candidates(x, b["editions"], b["group_of"], skip, floor=LOOSE))[:3]
            out.append({"line": x["key"], "letters": len(x["letters"]),
                        "candidates": [{"reading": c[4], "inscription": b["id_of"].get(c[5]), "verdict": c[0],
                                        "share_of_line": c[1], "share_of_text": c[2], "shared_runs": c[3]} for c in cands]})
    return out


def write(b, out=OUT, corpus_path=CORPUS):
    out.mkdir(parents=True, exist_ok=True)
    mapped = map_rows(b)
    corpus = corpus_rows(b, mapped)
    figs = measures(b, mapped, corpus)
    dump = lambda rows: "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    (out / "inscriptions.jsonl").write_text(dump(b["inscriptions"]))
    (out / "lines.jsonl").write_text(dump(line_rows(b)))
    (out / "map.jsonl").write_text(dump(mapped))
    (out / "pending.jsonl").write_text(dump(pending_rows(b)))
    (out / "joins.jsonl").write_text(dump([{"a": a, "b": c, "why": w} for a, c, w in b["joins"]]))
    (out / "figures.json").write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n")
    corpus_path.write_text(dump(corpus))
    return mapped, corpus, figs


def main(argv):
    if argv[1:]:
        sys.exit(__doc__)
    b = build()
    mapped, corpus, figs = write(b)
    print(json.dumps(figs, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv)
