"""F2: each entry's spellings, and the pages of the statements on its meaning where the sources in hand give them.

src/lexicon.py writes them into its tables. The spellings are Rilly's: the headword without a homonym's number,
then the variants he lists ("(peut-être)" written "(?)"), and beside them the pieces of the corpus that both
checkers of step 21 confirmed as a spelling or form of the entry (data/discovery/variants_confirmed.tsv).

The pages, of five kinds:
1. Rilly 2003: the page of the entry (lexicon.py has it).
2. A page that Rilly's record gives for a proposal: "(p. 34)" in the proposal or after the author's year
   (record_page). Most proposals give the author and the year, or the author alone.
3. Griffith's own page, for the proposals the check against his texts found as stated (griffith_pages): the
   printed page of Karanòg (1911) or of his Meroitic Studies I to IV (JEA 3 and 4, 1916-17), read from the page's
   own number in the text layer, or from the page beside it where the number is missing.
4. The editors': the pages of the entry of Millet 2005 (JSSEA 32, printed page = PDF page - 1) or FHN III (its
   contents, prepare.FHN_ENTRIES) that holds a word built on the entry (edition_pages). The check against the
   editions recorded the edition's entry of each word, not its line, so the page is that of the entry.
5. FHN IV's indexes of Meroitic titles (pp. 1292-94), Meroitic words (pp. 1329-31) and gods (pp. 1261-65): the
   page of FHN IV where the term is indexed, the term as FHN spells it, and the FHN pages the index gives or the
   entry it sends to (FHN4). Read from the scan's page images on 12 November 2026, because its text layer garbles
   some terms (FHN's ñ, Rilly's "ne"); tests compare the pages with the text layer. A term goes to an entry the map
   uses when it is spelled like the entry or a spelling Rilly lists under it and FHN's gloss is the entry's
   meaning ("at (bread)" is at (2), "-te (locative suffix)" is -te (2)); the index's phrases ("ant qorise") are
   left out. FHN IV's glosses are not used for the statuses: the rules of lexicon.py (item 3) were set without
   them.

FHN IV, Millet 2005, FHN III, Griffith's scans and Rilly's lexicon stay local; the public tables hold spellings,
pages and the names of the works, no wording of theirs.
"""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts")]
import coverage as C                                   # noqa: E402
import prepare as PR                                   # noqa: E402

CONFIRMED = ROOT / "data/discovery/variants_confirmed.tsv"
CHECKED_AS = "the word it is a spelling or a form of, for both checkers"
GRIFFITH_CHECK = ROOT / "data/sources/lexicon/answers/griffith_check.jsonl"
GRIFFITH_TEXTS = {"karanog": ("data/sources/karanog-text/pages.txt", "Karanòg (1911)"),
                  "studies_I": ("data/sources/griffith-jea-text/studies_I.txt", "Meroitic Studies I (1916)"),
                  "studies_II": ("data/sources/griffith-jea-text/studies_II.txt", "Meroitic Studies II (1916)"),
                  "studies_III": ("data/sources/griffith-jea-text/studies_III.txt", "Meroitic Studies III (1917)"),
                  "studies_IV": ("data/sources/griffith-jea-text/studies_IV.txt", "Meroitic Studies IV (1917)")}
NOTES = (("(peut-être)", "(?)"), ("(archaïque)", "(archaic)"), ("(arch.)", "(archaic)"))
PAGE_NOTE = re.compile(r"\((?:p|pp)\. ?(\d+(?:[-–]\d+)?(?:, ?\d+(?:[-–]\d+)?)*)\)")
ONE_WORK = re.compile(r"^[A-Z][\w'’\-]*(?: [A-Z][\w'’\-]*)* \d{4}[a-z]?$")      # "Hintze 1979": one author, one year

# FHN IV's index (5 of the docstring): (the entry, FHN IV's page, the term as FHN spells it, FHN's pages or "see")
FHN4 = (
    ("kroro", 1292, "akroro/kroro", "973, 974-75, 1000, 1008, 1011, 1014, 1025-31, 1034-35"),
    ("beloloke", 1292, "ameloloke", "670"),
    ("ant", 1292, "ant", "673, 675, 720-22, 975"),
    ("apote", 1292, "apote", "720-22"),
    ("arebetke", 1292, "arbetke/arbtke", "1014"),
    ("beliloke", 1293, "beliloke/beloloke", "1035"),
    ("beloloke", 1293, "beliloke/beloloke", "1035"),
    ("dkretri", 1293, "dkretri", "1018-19, 1034-35"),
    ("ḫbḫne", 1293, "ḫbḫñ", "974-75, 1017, 1025-31"),
    ("ḫlbine", 1293, "ḫlbiñ", "670"),
    ("ḫrpḫne", 1293, "ḫrpḫñ", "670-71"),
    ("kdke", 1293, "kdke", "see ktke"),
    ("ktke", 1293, "ktke", "510, 718, 719-22, 723-24, 897-904"),
    ("pelmos", 1293, "pelmos", "716, 940, 965, 972-73"),
    ("perite", 1293, "perite/pirite", "688, 973, 975"),
    ("peseto", 1293, "peseto/pesto", "673-76, 719-22, 988, 1008-9, 1019-20, 1022, 1025-31, 1035, 1038-41"),
    ("pesto", 1293, "peseto/pesto", "673-76, 719-22, 988, 1008-9, 1019-20, 1022, 1025-31, 1035, 1038-41"),
    ("pkrtr", 1293, "pkrtr", "905"),
    ("plsn", 1293, "plsn", "973"),
    ("pnqose", 1293, "pnqose/pñqose", "803"),
    ("pqr", 1293, "pqr", "670, 715-16, 718-22, 726-27, 803, 848, 1019, 1076"),
    ("pqrtr", 1293, "pqrtr", "905, 1039"),
    ("qorbse", 1293, "qorbse/qorpse", "803, 974-75"),
    ("qore", 1293, "qore/qoro", "285, 669, 672, 676, 715-16, 718-24, 801-4, 836-37, 838-40, 897-98, 903, 945, 1008, "
                                "1032-34, 1042-43, 1049, 1103-7"),
    ("qorene", 1293, "qoreñ", "675-76, 688, 944-45, 968, 974-75, 980, 986, 990, 995, 1000-9, 1016-17, 1025-31"),
    ("slẖ", 1293, "s-lḫ", "675-76"),
    ("ssimete", 1294, "ssimete", "670, 736"),
    ("ssor", 1294, "ssor", "670, 1036 n. 633, 1036-41"),
    ("womnise", 1294, "womnise", "1034-35, 1036-38"),
    ("abr", 1329, "abr", "716, 722, 725"),
    ("adb", 1329, "adb", "716"),
    ("aleqese", 1329, "aleqese", "725"),
    ("ant", 1329, "ant", "675"),
    ("arebetke", 1329, "arbetke", "1014"),
    ("ari-", 1330, "ari", "840"),
    ("Aritene", 1330, "ariteñ", "840"),
    ("at (2)", 1330, "at", "671"),
    ("ato", 1330, "ato", "671-72, 854, 975"),
    ("dḫe", 1330, "dḫe", "676"),
    ("-erike-", 1330, "erike", "673, 676"),
    ("ẖr", 1330, "ḫr", "1107"),
    ("kdi", 1330, "kdi", "670, 716, 722, 725, 840, 1033"),
    ("kdise", 1330, "kdite", "510"),
    ("kdke", 1330, "kdwe", "722"),
    ("kroro", 1330, "kroro", "see akroro"),
    ("ktke", 1330, "ktke", "510, 903"),
    ("-leb", 1330, "-leb", "670, 722, 1106"),
    ("lẖ", 1330, "lḫ", "664, 911, 1033, 1037"),
    ("mde", 1330, "mde", "966"),
    ("mte", 1330, "mete/mte", "1036 n. 632"),
    ("mk", 1330, "mk", "670, 672, 676, 840, 1106"),
    ("mlo", 1330, "mlo", "670, 676, 1033-34"),
    ("peseto", 1330, "peseto/pesto", "1022"),
    ("pesto", 1330, "peseto/pesto", "1022"),
    ("pwrite (2)", 1330, "pwrite", "672"),
    ("-qebese", 1330, "-qebese-", "1039-40"),
    ("qo", 1330, "qo", "533, 670, 905 n. 535"),
    ("qo", 1330, "qo", "722"),
    ("qore", 1330, "qore", "663, 801, 840, 903"),
    ("qorise", 1330, "qorese", "1034"),
    ("s", 1330, "s", "676"),
    ("Selele", 1330, "selele", "1107"),
    ("sem", 1330, "sem", "840"),
    ("sete", 1330, "sete", "1029"),
    ("slẖ", 1330, "s-lḫ", "676"),
    ("snptete", 1330, "snptete", "987 n. 608"),
    ("tbo", 1330, "tbo", "1039"),
    ("t-dḫe", 1330, "tdḫe", "840"),
    ("-te (2)", 1330, "-te", "973"),
    ("tewiseti", 1330, "tewiseti", "944"),
    ("wide", 1330, "wide", "803 n. 366"),
    ("wte", 1330, "wte", "664"),
    ("-erike-", 1331, "yerike", "397, 533"),
    ("yeseboẖe", 1331, "yesebohe", "914"),
    ("yetmde", 1331, "yetmde", "see mde"),
    ("yinnidte", 1331, "yinnidte", "840"),
    ("yireqe (1)", 1331, "yireke", "1107"),
    ("Amni", 1261, "Amani", "see Amūn"),
    ("Amnp", 1261, "Amnp", "see Amūn of Luxor"),
    ("Amnpte", 1261, "Amnpte", "see Amūn (Amen-Re) of Napata"),
    ("Aqedise", 1262, "Aqedise", "670, 725"),
    ("Ar (1)", 1262, "Ar[e]", "see Horus"),
    ("Wos", 1262, "Asi", "920-21"),
    ("Asori", 1262, "Asor", "see Osiris"),
    ("Mni", 1264, "Mni, Mno", "see Amūn"),
    ("Ms", 1264, "Ms", "954-55, 955 n. 579"),
    ("Wos", 1265, "Wos", "see Isis"),
)
FHN4_OFFSET = 1214                                     # FHN IV: printed page = PDF page + 1214
FHN4_TEXT = ROOT / "data/sources/fhn4-text/pages.txt"


def spelling(s):
    for a, b in NOTES:
        s = s.replace(a, b)
    return " ".join(s.split())


def spellings(printed):
    """Rilly's spellings of an entry: the headword without a homonym's number, then the variants he lists."""
    head = re.sub(r"\s*\(\d+\)$", "", printed["headword"].strip())
    return list(dict.fromkeys([head] + [spelling(v) for v in printed.get("variants") or [] if v.strip()]))


def confirmed(used, mine, printed, path=CONFIRMED):
    """The pieces of step 21 that both checkers confirmed as a spelling or form of a word, sorted: {"given":
    {headword: [pieces]}, "already": [pieces], "unmatched": [pieces]}. A piece is given to every entry the map
    uses that is that word: the headword itself where the checkers give its number ("smlo (1)"), else an entry
    whose headword or one of whose listed variants is spelled so, without its number. A piece that is already
    one of such an entry's spellings in the corpus's letters (mine[h]["forms"]) is not given again ("already");
    a piece whose word is no entry the map uses is "unmatched"."""
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    given, already, unmatched = {}, set(), set()
    for r in rows:
        word, piece = r[CHECKED_AS].strip(), r["piece"].strip()
        if re.search(r"\(\d+\)$", word):
            hits = [word] if word in used else []
        else:
            hits = sorted(h for h in used if word in {C.bare(s) for s in [h] + list(printed[h].get("variants") or [])})
        for h in hits:
            if piece in mine[h]["forms"]:
                already.add(piece)
            else:
                given.setdefault(h, set()).add(piece)
        if not hits:
            unmatched.add(piece)
    return {"given": {h: sorted(ps) for h, ps in given.items()}, "already": sorted(already - {p for ps in given.values() for p in ps}),
            "unmatched": sorted(unmatched)}


def record_page(p):
    """The page Rilly's record gives for a proposal of one author's one work: after the year in the author field
    ("Griffith 1911a (p. 101)") or in the proposal ("Hintze 1979" and "(p. 34)"), as "p. 34" or "pp. 34, 55";
    None where it gives none, or where the author field names several scholars."""
    author = p["author"].strip()
    m = PAGE_NOTE.search(author)
    if m:
        return f"p. {m.group(1)}" if ONE_WORK.match(author[:m.start()].strip()) and not author[m.end():].strip() \
            else None
    found = PAGE_NOTE.findall(p["proposal"])
    if ONE_WORK.match(author) and found:
        return ("p. " if len(found) == 1 else "pp. ") + ", ".join(found)
    return None


def pages_of(path):
    """{PDF page: text} of a text layer written "=== page N ===" page by page."""
    parts = re.split(r"=== page (\d+) ===\n", path.read_text(encoding="utf-8", errors="replace"))
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def capitals(text):
    """Whether a text reads as a running head: most of its letters are capitals."""
    letters = [c for c in text if c.isalpha()]
    return len(letters) >= 3 and sum(c.isupper() for c in letters) >= 0.7 * len(letters)


def own_number(text):
    """The number a page prints in its running head, as the text layer has it: alone or beside a head of capitals
    on its first line ("DESCRIPTIVE PHRASES 39", "116 F. LL. GRIFFITH", "26"), or alone on the second line under
    such a head ("MEROITIC STUDIES", "117"); None where none stands there."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return None
    m = (re.fullmatch(r"(\d{1,4})", lines[0]) or re.fullmatch(r"(\d{1,4}) (.+)", lines[0])
         or re.fullmatch(r"(.+) (\d{1,4})", lines[0]))
    if m and (m.lastindex == 1 or capitals(m.group(2) if m.group(1).isdigit() else m.group(1))):
        return int(m.group(1) if m.group(1).isdigit() else m.group(2))
    if len(lines) > 1 and re.fullmatch(r"\d{1,4}", lines[1]) and capitals(lines[0]):
        return int(lines[1])
    return None


def printed_page(pages, n, near=3):
    """The printed page of PDF page n. A page's own number counts when a page within `near` of it shows the same
    offset from its PDF page (a lone number in a table does not); n takes its own counted offset, or that of the
    nearest page with one, at most two pages away; None otherwise."""
    offset = {m: c - m for m, c in ((m, own_number(t)) for m, t in pages.items()) if c is not None}
    counted = {m: o for m, o in offset.items() if any(offset.get(x) == o for x in range(m - near, m + near + 1) if x != m)}
    for k in (0, 1, -1, 2, -2):
        if n + k in counted:
            return n + counted[n + k]
    return None


def griffith_pages(path=GRIFFITH_CHECK, root=ROOT):
    """{proposal id: "Karanòg (1911), p. 39"}: the printed page of Griffith's own statement, for the proposals the
    check against his texts found as stated; {} before it is answered."""
    if not path.exists():
        return {}
    import json
    texts, out = {}, {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        a = json.loads(line)
        if (a.get("verdict") or "").strip().lower() != "as stated" or a.get("file") not in GRIFFITH_TEXTS:
            continue
        m = re.search(r"\d+", a.get("page") or "")
        if not m:
            continue
        rel, name = GRIFFITH_TEXTS[a["file"]]
        if rel not in texts:
            texts[rel] = pages_of(root / rel)
        n = printed_page(texts[rel], int(m.group()))
        if n is not None:
            out.setdefault(a["row"], f"{name}, p. {n}")
    return out


def millet_pages(path=PR.MILLET):
    """{"GA05": (first printed page, last printed page)} of the entries of Millet 2005: from the page of its
    heading to the page of the next heading, or the page before when that heading opens its page (it stands
    right under the running head); the last entry to its own page. Printed page = PDF page - 1."""
    pg = PR.pages(path)
    heads = []
    for n in PR.MILLET_PAGES:
        lines = [l for l in pg[n].splitlines() if l.strip()]
        for i, l in enumerate(lines):
            m = re.match(r"^(GA\s?\d+[a-z]?(?:\s?[&+]\s?(?:GA\s?)?\d+)*)\s*:", l)
            if m:
                heads.append((n, i, PR.numbers(m.group(1).replace(" ", ""))))
    out = {}
    for k, (n, _, names) in enumerate(heads):
        last = n
        if k + 1 < len(heads) and heads[k + 1][0] > n:
            nxt, at, _ = heads[k + 1]
            last = nxt - 1 if at <= 1 else nxt
        for g in names:
            out.setdefault(g, (n - 1, last - 1))
    return out


def span(first, last):
    return f"p. {first}" if first == last else f"pp. {first}-{last}"


def edition_pages(entries_of_editions, millet=None):
    """{headword: ["Millet 2005, GA05, p. 4 (the same)", "FHN III, FHN 268, pp. 1031-1034 (otherwise)"]}: the
    editions' entries that hold a word built on the entry that the editor reads the same way or otherwise
    (entries_of_editions: {headword: {verdict: {(source, entry)}}}), with their pages."""
    millet = millet_pages() if millet is None else millet
    said = {"agree": "the same", "differ": "otherwise"}
    out = {}
    for h, by in entries_of_editions.items():
        refs = []
        for verdict in ("agree", "differ"):
            for source, entry in sorted(by.get(verdict, ())):
                if source == "millet" and entry in millet:
                    refs.append(f"Millet 2005, {entry}, {span(*millet[entry])} ({said[verdict]})")
                elif source == "fhn" and entry in PR.FHN_ENTRIES:
                    refs.append(f"FHN III, FHN {entry}, {span(*PR.FHN_ENTRIES[entry])} ({said[verdict]})")
        if refs:
            out[h] = refs
    return out


def fhn_index():
    """{headword: ["FHN IV p. 1293 (qore/qoro): FHN 285, 669, ..."]} from FHN4."""
    out = {}
    for h, page, term, where in FHN4:
        out.setdefault(h, []).append(f"FHN IV p. {page} ({term}): " + (where if where.startswith("see") else
                                                                         f"FHN {where}"))
    return out
