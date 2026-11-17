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
    pos = [(text.find(f), f) for f in FIELDS if text.find(f) >= 0]     # the first place each field is named
    pos.sort()
    out = {}
    for k, (p, f) in enumerate(pos):
        end = pos[k + 1][0] if k + 1 < len(pos) else len(text)
        out[f] = text[p + len(f):end].strip()
    d = out.get("Description de l'inscription", "")
    script = "hieroglyphic" if re.search(r"hiéroglyph", d, re.I) else "cursive" if re.search(r"cursi[fv]", d, re.I) \
        else ""
    lines, unit = None, ""
    m = re.search(r"\b(?:sur|de|d'|en) ?(\S+?(?:-\S+)?) (ligne|colonne|bande)s?\b", d)
    one = re.search(r"\b[Uu]ne seule (ligne|colonne|bande)", d)
    if m:
        w = m.group(1).lower()
        lines, unit = (int(w) if w.isdigit() else NUMBERS.get(w)), m.group(2)
    elif one:
        lines, unit = 1, one.group(1)
    st = re.search(r"état de conservation (?:est|était)(?:, au moment de [^,]+,)? ([^.,;(]+)", d)
    return {"fields": out, "script": script, "lines": lines, "unit": unit, "state": st.group(1).strip() if st else ""}


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


def is_catalogue(text):
    """A catalogue page names one of its fields (a continuation may hold the bibliography alone), or, where the
    text layer kept little, has the running head of a right-hand page ("5. Inscriptions de Méroé REM 0403") and
    not that of a page of plates ("RÉPERTOIRE D'ÉPIGRAPHIE MÉROÏTIQUE")."""
    if any(f in text for f in FIELDS):
        return True
    return bool(re.search(r"\b\d{1,2}\. \S[^:]{2,60}?REM \d{4}", text)) and "RÉPERTOIRE" not in text.upper()


def index(folder=TEXT):
    """One row per REM entry: its plate pages (every page of the entry that is not catalogue: each holds figures,
    with the captions the text layer has) and its catalogue (script, lines, state), read from its catalogue pages
    run together."""
    entries, cat_text = collections.OrderedDict(), collections.defaultdict(list)
    for vol in (1, 2, 3):
        for p in sorted((folder / f"v{vol}").glob("T*.html")):
            text = page_text(p.read_text(encoding="utf-8"))
            nums = rem_on(text)
            if not nums or re.search(r"REM \d{4} à REM \d{4}", text):
                continue
            num = nums[0]
            e = entries.setdefault(num, {"rem": num, "volume": vol, "plates": [], "catalogue": None, "pages": []})
            e["pages"].append(p.stem)
            if is_catalogue(text):
                cat_text[num].append((p.stem, text))
            else:
                e["plates"].append({"page": p.stem, "captions": captions(text)})
    for num, e in entries.items():
        if cat_text[num]:
            e["catalogue"] = catalogue(" ".join(t for _, t in cat_text[num]))
            e["catalogue"]["pages"] = [s for s, _ in cat_text[num]]
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


# ------------------------------------------------------------------------------------------ the readers' packs

SPEC = PILOT / "spec.json"            # local: each pick's figures (page, box, kind), object and lines; the packs
KIT = PILOT / "kit"                   # local: the brief and the signs
PACKS = PILOT / "packs"
KEY = PILOT / "key.json"
PAGES = REM / "pages"


def chosen():
    """The picks, by the rule, against the index of the volumes."""
    idx = read_index()
    p, _ = pool()
    return pick(p, lambda e: any(x["plates"] for x in plates_for(e["rem"], idx)))[0]


WIDE = 250                            # a drawing this wide on the preview runs across the plate: cut to the frame
MARGIN = 15                           # preview pixels added to each side of a box drawn by eye


def box_on_page(box, spec, page=None, kind=""):
    """A box drawn by eye on the preview of a page, on the page itself: (top, left, height, width) in its pixels.
    The eye misjudged the sides by up to 25 preview pixels, so the sides are widened by MARGIN and kept within the
    page's frame (spec["frames"], found by a scan for dark columns and checked on the page), and a wide drawing is
    cut from frame to frame, so that no line loses its ends. Top and bottom stay as drawn: the captions are there."""
    (pw, ph), (W, H) = spec["preview_size"], spec["page_size"]
    x0, y0, x1, y1 = box
    frame = (spec.get("frames") or {}).get(page) or (0, W)
    left = max(round((x0 - MARGIN) * W / pw), frame[0] + 4)
    right = min(round((x1 + MARGIN) * W / pw), frame[1] - 4)
    if kind == "drawing" and x1 - x0 >= WIDE:
        left, right = frame[0] + 4, frame[1] - 4
    top, bottom = round(y0 * H / ph), min(round(y1 * H / ph), H)
    return top, left, bottom - top, right - left


def gray(path, run=None):
    """The page as rows of grey values (0 black, 255 white), read from a BMP that macOS sips writes."""
    import struct
    import subprocess
    import tempfile
    tmp = Path(tempfile.mkdtemp()) / "page.bmp"
    (run or (lambda c: subprocess.run(c, check=True, capture_output=True)))(
        ["sips", "-s", "format", "bmp", str(path), "--out", str(tmp)])
    b = tmp.read_bytes()
    off = struct.unpack_from("<I", b, 10)[0]
    w, h = struct.unpack_from("<ii", b, 18)
    px = struct.unpack_from("<H", b, 28)[0] // 8
    row = ((w * px * 8 + 31) // 32) * 4
    up, h = h > 0, abs(h)
    return [[b[off + (h - 1 - y if up else y) * row + x * px] for x in range(w)] for y in range(h)]


INK = 110                             # darker than this is ink
SNAP_UP_DOWN, SNAP_SIDES = 25, 80      # how far an edge may move out, in pixels


def snap(img, top, left, height, width, frame=None):
    """Move each edge of a box out while the row or column just outside it holds ink, so that a box drawn by eye
    does not cut a line of signs; the white gap before a caption stops it. Never onto the frame (6 pixels inside
    it), and up or down by SNAP_UP_DOWN at most, so that a photograph close above or below is not taken in.
    (top, left, height, width) again."""
    H, W = len(img), len(img[0])
    lo, hi = (frame[0] + 6, frame[1] - 6) if frame else (0, W)
    bottom, right = top + height, left + width
    left, right = max(left, lo), min(right, hi)
    ink_row = lambda y: 0 <= y < H and any(img[y][x] < INK for x in range(left, right))
    ink_col = lambda x: lo <= x < hi and any(img[y][x] < INK for y in range(max(top, 0), min(bottom, H)))
    t0, b0, l0, r0 = top, bottom, left, right
    while top > t0 - SNAP_UP_DOWN and ink_row(top - 1):
        top -= 1
    while bottom < b0 + SNAP_UP_DOWN and ink_row(bottom):
        bottom += 1
    while left > max(l0 - SNAP_SIDES, lo) and ink_col(left - 1):
        left -= 1
    while right < min(r0 + SNAP_SIDES, hi) and ink_col(right):
        right += 1
    return top, left, bottom - top, right - left


def folders(spec):
    """{folder name: pack name}: one reader for each pack, and a second for the packs named in the spec."""
    out = {p: p for p in spec["packs"]}
    out.update({p + "b": p for p in spec["second_reader"]})
    return out


def write_packs(spec=None, run=None):
    """The readers' folders: the brief, the signs, each item's figures cut out of its plate page, items.json and an
    empty out/; and the key (folder, item id -> REM number), outside the folders. Refuses once a reader has
    answered."""
    import shutil
    import subprocess
    spec = json.loads(SPEC.read_text(encoding="utf-8")) if spec is None else spec
    picks = {e["rem"] for e in chosen()}
    idx = read_index()
    script = {r: next((x["catalogue"]["script"] for x in plates_for(r, idx) if x["catalogue"]), "") for r in picks}
    if picks != set(spec["items"]) or picks != {r for v in spec["packs"].values() for r in v}:
        raise SystemExit("the spec's items are not the rule's picks")
    if any(PACKS.glob("*/out/readings.jsonl")):
        raise SystemExit("a reader has answered: not writing the packs again")
    run = run or (lambda cmd: subprocess.run(cmd, check=True, capture_output=True))
    key = {}
    for name, pack in folders(spec).items():
        d = PACKS / name
        if d.exists():
            shutil.rmtree(d)
        (d / "plates").mkdir(parents=True)
        (d / "out" / "crops").mkdir(parents=True)
        shutil.copy(KIT / "BRIEF.md", d / "BRIEF.md")
        shutil.copytree(KIT / "signs", d / "signs")
        items = []
        for k, rem in enumerate(spec["packs"][pack]):
            iid = "ABCDEFGH"[k]
            it = spec["items"][rem]
            files = []
            for n, (page, box, kind) in enumerate(it["figures"], 1):
                top, left, h, w = box_on_page(box, spec, page, kind)
                if kind == "drawing":
                    top, left, h, w = snap(gray(PAGES / f"{page}.jpg"), top, left, h, w, spec["frames"].get(page))
                out = d / "plates" / f"{iid}_{n}.jpg"
                run(["sips", "-c", str(h), str(w), "--cropOffset", str(top), str(left), str(PAGES / f"{page}.jpg"),
                     "--out", str(out)])
                files.append(out.name)
            items.append({"id": iid, "object": it["object"], "script": script[rem] or "not stated", "lines": it["lines"],
                          "figures": files})
            key.setdefault(name, {})[iid] = rem
        (d / "items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    KEY.write_text(json.dumps(key, indent=1) + "\n", encoding="utf-8")
    return key


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
    elif cmd == "packs":
        key = write_packs()
        print(f"{len(key)} folders:", {k: len(v) for k, v in key.items()})
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
