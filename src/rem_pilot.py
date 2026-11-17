"""The REM pilot: can a Claude reader read the plates of the Répertoire d'épigraphie méroïtique into the corpus?

The REM (Leclant and others, 2000; three volumes on Persée, REM 0001 to 1278) gives each inscription a page of
plates (photographs and drawings, most of them reprinted from the first edition) and a page of catalogue (where
the object is, its first designation, the monument, its size, the script and the number of lines, the state, the
bibliography). It prints no transliteration. This script:

  index      reads the text layers of the volumes' pages (local) into one row per REM entry: its plate pages, the
             captions of its figures, and what the catalogue says of script, lines and state
  pool       the inscriptions the pilot may draw from: a REM number, and an open reading of an edition in hand
  pick       the rule that chose the inscriptions (data/discovery/rem_pilot.md, section 3), written before any
             reader ran: strata of kind and length, a seed, the entries with a modern edition (FHN III) first
  score      the readers' answers against the editions: signs right and words that agree
  estimate   what reading every plate would cost and add (inscriptions and words new to the corpus, and the open
             spellings that stand in one text and would then recur)
  public     the counts, for the public figures file (no reading of the REM, no image)

The REM is in copyright: its pages, plates and the readings taken from them stay in data/sources/rem/ (local).
The public files hold counts only.

  python3 -I src/rem_pilot.py index | pool | pick | score | estimate | public
"""
import ast
import collections
import html
import json
import math
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REM = ROOT / "data/sources/rem"                       # local: the volumes' text layers, the plates, the packs
TEXT = REM / "text"
INDEX = REM / "index.jsonl"
PILOT = REM / "pilot"
TABLE = ROOT / "data/inscriptions.jsonl"              # public: every inscription, with its open reading
GLOSSES = ROOT / "data/sources/v6/analysts/glosses.jsonl"   # local: the analysts' map of corpus_v6
FIGURES = ROOT / "data/discovery/rem_pilot_figures.json"
FHN_TYPED = (ROOT / "runs/work/griffith/score.py", "fhn"), (ROOT / "runs/work/handcopy/score_hc.py", "FHN")
VOLUMES = {1: range(1, 388), 2: range(401, 852), 3: range(1001, 1279)}

# ------------------------------------------------------------------------------------------ the rule (section 3)
SEED = 20261117
MIN_WORDS, MAX_WORDS = 3, 150          # too short to score; too long for the pilot's cost (REM 0094, 1003)
BANDS = (("S", 3, 9), ("M", 10, 29), ("L", 30, MAX_WORDS))
ALLOC = {("funerary", "S"): 2, ("funerary", "M"): 4, ("funerary", "L"): 3,
         ("royal", "S"): 3, ("royal", "M"): 2, ("royal", "L"): 2,
         ("graffito", "S"): 2, ("graffito", "M"): 1, ("graffito", "L"): 0,
         ("other", "S"): 1, ("other", "M"): 0, ("other", "L"): 0}
GRAFFITO_ML = True                     # graffiti of M and L length are one stratum (there are six)
LATE = 2                               # entries of volumes II and III taken first, at most

# ------------------------------------------------------------------------------------------ the bar (section 3)
BAR_GO = 0.95                          # signs right, pooled: the standard the Karanog rows met (97.7%, bar 95%)
BAR_LAYER = 0.85                       # below this the readings are of no use, not even as a flagged layer
EXPECTED = 0.85                        # what we expect, pooled, written before any reader ran


def kind_group(kind):
    k = (kind or "").lower()
    if k.startswith("funerary"):
        return "funerary"
    if k.startswith("royal"):
        return "royal"
    if k.startswith("graffito"):
        return "graffito"
    return "other"


def band(words):
    for name, lo, hi in BANDS:
        if lo <= words <= hi:
            return name
    return None


def stratum(kind, words):
    g, b = kind_group(kind), band(words)
    if b is None:
        return None
    if g == "graffito" and GRAFFITO_ML and b == "L":
        b = "M"
    return g, b


# ------------------------------------------------------------------------------------------ signs and the measures

def corpus_to_signs(text):
    """A text in the corpus spelling as a list of signs: S the sign s, s the sign se, N the sign ne, x and X the
    two h-signs, te and to one sign each, a digit one sign; lost signs ('.'), dividers and marks are dropped."""
    t = re.sub(r"\(\d+\)|\[\.\]|\?", " ", text)
    out = []
    for w in re.split(r"[\s:]+", t):
        w = re.sub(r"[^A-Za-z0-9]", "", w)
        i = 0
        while i < len(w):
            c = w[i]
            if c == "t" and i + 1 < len(w) and w[i + 1] in "eo":
                out.append("t" + w[i + 1])
                i += 2
                continue
            out.append({"S": "s", "s": "se", "N": "ñ", "x": "ḫ", "X": "ẖ"}.get(c, c.lower()))
            i += 1
    return out


def corpus_words(text):
    """The words of a text in the corpus spelling, each as its list of signs; words without a sign drop out."""
    t = re.sub(r"\(\d+\)", "", text)
    return [s for s in (corpus_to_signs(w) for w in re.split(r"[\s:]+", t)) if s]


def fhn_to_signs(text):
    """A text as FHN prints it (the first test's typing: ñ, ḫ, h̲ or ẖ, se and s, (N) line numbers, (x) a
    restoration, [=...] a normalised form, * an unsure sign, ,, a divider) as a list of signs: the same signs as
    corpus_to_signs gives, so that the two compare."""
    s = text.lower().replace("h̲", "ẖ")
    s = re.sub(r"\[=[^\]]*\]", " ", s)
    s = re.sub(r"\(\d+\)", "", s)
    s = re.sub(r"\(([^)\d]+)\)", r"\1", s)
    s = re.sub(r"[*:,.|?\[\]]", " ", s)
    out = []
    for w in s.split():
        i = 0
        while i < len(w):
            if w[i:i + 2] in ("se", "te", "to"):
                out.append(w[i:i + 2])
                i += 2
            else:
                out.append(w[i])
                i += 1
    return out


def fhn_words(text):
    s = re.sub(r"\[=[^\]]*\]", " ", text)
    s = re.sub(r"\(\d+\)", "", s)
    return [x for x in (fhn_to_signs(w) for w in re.split(r"[\s,:|]+", s)) if x]


def align(a, b):
    """The edit distance of two lists of signs and, for each sign of b, whether it is matched by an equal sign of
    a (Levenshtein, the first test's alignment: ties go to a match, then to a sign only a has)."""
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    i, j, same = n, m, [False] * m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            same[j - 1] = a[i - 1] == b[j - 1]
            i, j = i - 1, j - 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            i -= 1
        else:
            j -= 1
    return D[n][m], same


def measure(reading_signs, edition_words):
    """{signs, right, words, agree} of a reading against an edition. signs right: the edition's signs less the
    edit distance, so a sign the reading has and the edition has not counts against it too (the measure of the
    Karanog page). A word of the edition agrees when every one of its signs is matched by an equal sign of the
    reading (the rule of the Akinidad page, on signs and with nothing folded)."""
    b = [s for w in edition_words for s in w]
    d, same = align(reading_signs, b)
    agree, k = 0, 0
    for w in edition_words:
        agree += all(same[k:k + len(w)])
        k += len(w)
    return {"signs": len(b), "right": max(len(b) - d, 0), "words": len(edition_words), "agree": agree}


# ------------------------------------------------------------------------------------------ the editions in hand

def fhn_typed(sources=FHN_TYPED):
    """{REM number: FHN III's text} for the entries the first tests typed from FHN's page images (in the repo:
    runs/work/griffith/score.py, runs/work/handcopy/score_hc.py). For REM 0103 the whole graffito ('0103full'),
    not the part Griffith's type covers."""
    out = {}
    for path, name in sources:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets) \
                    and isinstance(node.value, ast.Dict):
                for k, v in ast.literal_eval(node.value).items():
                    if k == "0103":
                        continue
                    out[k.replace("full", "")] = v
    return out


def rows(path=TABLE):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def rem_int(rem):
    m = re.match(r"(\d{4})", rem or "")
    return int(m.group(1)) if m else None


def volume_of(rem):
    n = rem_int(rem)
    return next((v for v, r in VOLUMES.items() if n in r), None) if n else None


def open_words(r):
    """The number of words of a row's open reading (Griffith's print, the Karanog copies, or Griffith 1917)."""
    o = next((x for x in r["readings"] if x["key"] == r.get("open_reading")), None)
    return (o or {}).get("words") or 0


def pool(table=None, fhn=None):
    """The inscriptions the pilot draws from, each with its stratum. In: one REM number within the volumes, an
    open reading of an edition in hand. Out, and why: a row of two REM numbers (its parts stand on two entries);
    fewer than MIN_WORDS or more than MAX_WORDS words in the open reading."""
    table = rows() if table is None else table
    fhn = fhn_typed() if fhn is None else fhn
    out, left = [], collections.Counter()
    for r in table:
        rems = r.get("rem") or []
        if not rems or not any(volume_of(x) for x in rems):
            continue
        if not r.get("open_reading"):
            left["no open reading"] += 1
            continue
        if len(rems) > 1:
            left["two REM numbers"] += 1
            continue
        w = open_words(r)
        st = stratum(r["kind"], w)
        if st is None:
            left["fewer than %d words" % MIN_WORDS if w < MIN_WORDS else "more than %d words" % MAX_WORDS] += 1
            continue
        out.append({"id": r["id"], "rem": rems[0], "volume": volume_of(rems[0]), "kind": r["kind"],
                    "stratum": list(st), "words": w, "fhn": rems[0][:4] in fhn and rems[0][4:] == "",
                    "open": r["open_reading"]})
    return out, left


def pick(entries, has_plate=lambda e: True, seed=SEED):
    """The rule. All entries in one seeded order. First, up to LATE entries of volumes II and III are taken (most
    texts new to the corpus are in those volumes; the pool's are all Meroe City texts of 1911, hence no more than
    LATE). Then each stratum is filled to ALLOC: its entries in the seeded order, those with a typed FHN text
    first, but no more of them than half the stratum's places, rounded up. An entry the REM shows no plate for is
    passed over, and the next one taken. Returns the picks in order and the entries passed over."""
    rnd = random.Random(seed)
    entries = sorted(entries, key=lambda e: e["id"])
    rnd.shuffle(entries)
    chosen, passed = [], []
    need = dict(ALLOC)
    for e in entries:
        if e["volume"] in (2, 3) and sum(x["volume"] in (2, 3) for x in chosen) < LATE \
                and need.get(tuple(e["stratum"]), 0) > 0:
            if has_plate(e):
                chosen.append(e)
                need[tuple(e["stratum"])] -= 1
            else:
                passed.append(e)
    for st, n in ALLOC.items():
        if not need.get(st):
            continue
        here = [e for e in entries if tuple(e["stratum"]) == st and e not in chosen]
        cap = math.ceil(ALLOC[st] / 2)
        order = [e for e in here if e["fhn"]][:cap] + [e for e in here if not e["fhn"]] + [e for e in here if e["fhn"]][cap:]
        got = 0
        for e in order:
            if got == need[st]:
                break
            if has_plate(e):
                chosen.append(e)
                got += 1
            else:
                passed.append(e)
    return chosen, passed


# ------------------------------------------------------------------------------------------ the volumes (index)

FIELDS = ("Localisation actuelle", "Désignation originelle", "Identification du monument", "Dimensions",
          "Description de l'inscription", "Bibliographie")
NUMBERS = {"une": 1, "un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6, "sept": 7, "huit": 8,
           "neuf": 9, "dix": 10, "onze": 11, "douze": 12, "treize": 13, "quatorze": 14, "quinze": 15, "seize": 16,
           "dix-sept": 17, "dix-huit": 18, "dix-neuf": 19, "vingt": 20}


def page_text(raw):
    """The words of a page's text layer (Persée's HTML), one line."""
    t = re.sub(r'in me remove \.expandable add \.expanded remove it">', " ", raw)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", t)).replace("''", "'").strip()


def rem_on(text):
    """The REM numbers a page names (its running head or its plate's heading), as printed: '0057A', '0073'."""
    return list(dict.fromkeys(m.upper() for m in re.findall(r"REM\s*(\d{4}[A-Za-z]?)\b", text)))


def catalogue(text):
    """{field: text} of a catalogue page, and what it says of script, lines and state."""
    pos = [(text.find(f), f) for f in FIELDS if text.find(f) >= 0]
    pos.sort()
    out = {}
    for k, (p, f) in enumerate(pos):
        end = pos[k + 1][0] if k + 1 < len(pos) else len(text)
        out[f] = text[p + len(f):end].strip()
    d = out.get("Description de l'inscription", "")
    script = "hieroglyphic" if re.search(r"hiéroglyph", d, re.I) else "cursive" if re.search(r"cursive", d, re.I) else ""
    m = re.search(r"sur (\S+(?:-\S+)?) (ligne|lignes|colonne|colonnes)", d)
    lines = None
    if m:
        w = m.group(1).lower()
        lines = int(w) if w.isdigit() else NUMBERS.get(w)
    st = re.search(r"état de conservation est ([^.,;]+)", d)
    return {"fields": out, "script": script, "lines": lines, "unit": m.group(2).rstrip("s") if m else "",
            "state": st.group(1).strip() if st else ""}


def caption_kind(caption):
    """What a figure is, by its caption: a drawing (facsimile, copy, drawing; Lepsius's plates are drawings) or
    a photograph (every other caption names the object or the scene)."""
    c = caption.lower()
    if re.search(r"fac-?simil|copie|dessin|lepsius|relevé", c):
        return "drawing"
    return "photograph"


def captions(text):
    """The captions of a plate page: a description, then its source in brackets. The text layer gives each
    twice (the image's alt text and the printed caption); each is kept once."""
    out = []
    for m in re.finditer(r"([A-ZÉÈ][^()]{3,200}?)\s*\(([^()]*\d[^()]*)\)", text):
        desc = re.sub(r"^.*?RÉPERTOIRE D'ÉPIGRAPHIE MÉRO.TIQUE\s*", "", m.group(1)).strip()
        desc = re.sub(r"^.*?REM \d{4}[A-Za-z]?\s*", "", desc).strip()
        key = re.sub(r"\W", "", desc.lower())[:40]
        if desc and key not in [re.sub(r"\W", "", c["text"].lower())[:40] for c in out]:
            out.append({"text": desc, "source": m.group(2).strip(), "kind": caption_kind(desc + " " + m.group(2))})
    return out


def index(folder=TEXT):
    """One row per REM entry: its plate pages (with captions) and its catalogue (script, lines, state)."""
    entries = collections.OrderedDict()
    for vol in (1, 2, 3):
        for p in sorted((folder / f"v{vol}").glob("T*.html")):
            text = page_text(p.read_text(encoding="utf-8"))
            nums = rem_on(text)
            if not nums or re.search(r"REM \d{4} à REM \d{4}", text):
                continue
            num = nums[0]
            e = entries.setdefault(num, {"rem": num, "volume": vol, "plates": [], "catalogue": None, "pages": []})
            e["pages"].append(p.stem)
            if "Localisation actuelle" in text or "Identification du monument" in text:
                if e["catalogue"] is None:
                    e["catalogue"] = catalogue(text)
                    e["catalogue"]["page"] = p.stem
            else:
                caps = captions(text)
                if caps:
                    e["plates"].append({"page": p.stem, "captions": caps})
    return list(entries.values())


def write_index():
    rows_ = index()
    INDEX.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows_), encoding="utf-8")
    return rows_


def read_index(path=INDEX):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def plates_for(rem, idx):
    """The index rows that are this REM number: the same number, or its lettered parts ('0057' has 0057A to C)."""
    m = re.match(r"(\d{4})([A-Za-z]?)", rem)
    digits, letter = m.group(1), m.group(2).upper()
    return [e for e in idx if e["rem"][:4] == digits and (not letter or e["rem"][4:] in ("", letter))]


# ------------------------------------------------------------------------------------------ commands

def main(argv):
    cmd = argv[0] if argv else "pool"
    if cmd == "index":
        r = write_index()
        print(f"{INDEX.relative_to(ROOT)}: {len(r)} entries, {sum(len(e['plates']) for e in r)} plate pages, "
              f"{sum(1 for e in r if e['catalogue'])} with a catalogue page")
    elif cmd == "pool":
        p, left = pool()
        print(len(p), "in the pool;", dict(left))
        print(collections.Counter(tuple(e["stratum"]) for e in p))
    elif cmd == "pick":
        p, _ = pool()
        idx = read_index() if INDEX.exists() else None
        has = (lambda e: any(x["plates"] for x in plates_for(e["rem"], idx))) if idx else (lambda e: True)
        chosen, passed = pick(p, has)
        for e in chosen:
            print(e["id"], e["stratum"], e["words"], "FHN" if e["fhn"] else "")
        print(len(chosen), "chosen;", len(passed), "passed over:", [e["id"] for e in passed])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
