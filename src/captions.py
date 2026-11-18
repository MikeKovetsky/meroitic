"""The caption pilot (data/discovery/caption_pilot.md): the captions of temple reliefs read against their pictures.

Gate 1 counts the material, gate 2 tests the pictures on caption words whose meaning is known (each read with its
own picture and with a wrong one), gate 3 reads the open words only if gate 2 is met. The rules and bars were set
and pushed before anything ran (the page, sections 3 and 4); this file carries them out.

  python3 -I src/captions.py count          gate 1 from the inventory and the map as it stands
  python3 -I src/captions.py packs known     the readers' packs for gate 2, once gate 1 is met (packs/known/)
  python3 -I src/captions.py judges known    the judges' pack, once every reader's answers are in
  python3 -I src/captions.py score known     gate 2 from the two judges' scores
  python3 -I src/captions.py public          data/discovery/caption_pilot_figures.json

`packs open` makes gate 3's packs, and runs only once gate 2 is met. Gate 3 is judged otherwise (a proposal stands
when both right-picture readers give it and neither wrong-picture reader does), which is not built here yet.

The inventory (data/sources/captions/inventory.jsonl) has a row for each of the 87 texts: "id", "caption" (true or
false) and, for a caption, "figure_kind" (one of KINDS) and "crop" (its cut picture, a path from the repo's root or
from data/sources/captions/). Each pack is read by one fresh agent, which writes the file the pack names, one line
an item: {"item": ..., "meaning": at most five words, "element": the element of the picture, or "none"}. The judges
write judges/<kind>/J1.jsonl and J2.jsonl, one line an answer of their pack: {"id": ..., "score": 1, 0.5 or 0}.

The inventory, the cut pictures, the packs, the key, the answers and the scores are local: they hold the readings
of the map and the plates' crops. Only the counts go public.
"""
import collections
import json
import math
import pathlib
import random
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src")]

HERE = ROOT / "data/sources/captions"
INVENTORY = HERE / "inventory.jsonl"
TEXTS = HERE / "texts87.json"
PUBLIC = ROOT / "data/discovery/caption_pilot_figures.json"

# the map's seven layers when the page was set (section 3): a layer laid later does not count here
LAYERS = ("recurring", "rare_sure", "rare_later", "unnamed", "rare_millet", "leftover", "leftover_stems")
SEED = 17                    # the wrong pictures, the packs and the sign-flip test (page, section 4)
CAP = 3                      # a spelling counts in at most its first three captions (section 3)
EXCLUDED = ("meaning", "grammar", "name", "number", "lost")   # the levels an open item may not have
KINDS = ("god", "goddess", "king", "queen", "prince", "official", "priest", "animal", "object", "scene")
PLACES = {"napata": "gebel"}  # Napata is the town at Gebel Barkal: its texts and Gebel Barkal's are of one place
READERS = {"right": ("A", "B"), "wrong": ("C", "D")}           # two readers a condition, none in both; A and C
#                                                                read the same packs of items, and so do B and D
JUDGES = ("J1", "J2")
BATCH = 12                   # items in one pack, at most; each pack is read by one fresh agent
NAMED = 3                    # a spelling named inside another word's gloss counts as shown from this many letters
WORDS = 5                    # a reader's meaning has at most five words (section 4, gate 2, point 3)
DRAWS = 10_000
GATE1 = {"known": 20, "open_spellings": 10}
GATE2 = {"items": 20, "right": 0.50, "gain": 0.20, "p": 0.05}
SCORES = (0, 0.5, 1)


def load_inventory(path=INVENTORY):
    rows = read_jsonl(path)
    twice = sorted(i for i, c in collections.Counter(o["id"] for o in rows).items() if c > 1)
    if twice:
        raise SystemExit(f"the inventory lists {', '.join(twice)} more than once")
    for o in rows:
        if not isinstance(o.get("caption"), bool):
            raise SystemExit(f"{o['id']}: caption {o.get('caption')!r} is not true or false")
        if o["caption"] and o.get("figure_kind") not in KINDS:
            raise SystemExit(f"{o['id']}: figure_kind {o.get('figure_kind')!r} is not one of {KINDS}")
    return rows


def held(inv, texts):
    """The inventory, once it gives a row for each of the texts and for no other, and a cut picture that is a file
    for each caption (gate 1 counts the captions beside a picture that is held); it stops otherwise."""
    ids = {o["id"] for o in inv}
    missing, other = sorted(set(texts) - ids), sorted(ids - set(texts))
    if missing or other:
        raise SystemExit(f"the inventory is not the {len(texts)} texts: no row for {missing[:5]} ({len(missing)}), "
                         f"rows for other texts {other[:5]} ({len(other)})")
    lost = [o["id"] for o in captions(inv) if not crop_file(o.get("crop") or "").is_file()]
    if lost:
        raise SystemExit(f"no cut picture for the captions {', '.join(lost[:5])} ({len(lost)})")
    return inv


def order(text_id):
    """The texts in REM order, the texts without a REM number after them (section 3: "by REM number")."""
    return (not text_id.startswith("REM "), text_id)


def site_of(site):
    """The place a text comes from: the first word of its site, folded to plain letters ("Meroë, temple of Amun"
    and "Meroe City" are both meroe), with the names of one place made one (PLACES)."""
    first = site.split(",")[0].split("(")[0].strip().split()[0]
    folded = unicodedata.normalize("NFKD", first).encode("ascii", "ignore").decode().lower()
    return PLACES.get(folded, folded)


def captions(inv):
    return sorted((o for o in inv if o.get("caption")), key=lambda o: order(o["id"]))


def items(inv, gl, kind):
    """The items of one kind ("known" or "open"). An item is one word in one caption, at its first place there,
    and its level at that place makes it known, open or neither; a spelling gives items in its first CAP captions
    by REM number, known and open together."""
    if kind not in ("known", "open"):
        raise ValueError(kind)
    seen = collections.Counter()
    out = []
    for o in captions(inv):
        if o["id"] not in gl:
            raise SystemExit(f"{o['id']}: not on the map")
        first = {}
        for n, w in enumerate(gl[o["id"]], 1):
            first.setdefault(w["form"], (n, w))
        for form, (n, w) in first.items():
            known = w["level"] == "meaning"
            if (not known and w["level"] in EXCLUDED) or seen[form] >= CAP:
                continue
            seen[form] += 1
            if known == (kind == "known"):
                out.append({"text": o["id"], "n": n, "form": form, "gloss": w.get("gloss", ""), "level": w["level"]})
    return out


def count(inv, gl):
    """Gate 1: the known items and the different open spellings in captions beside a held picture."""
    known, opened = items(inv, gl, "known"), items(inv, gl, "open")
    spellings = sorted({o["form"] for o in opened})
    caps = captions(inv)
    return {"texts": len(inv), "captions": len(caps), "by_kind": dict(collections.Counter(o["figure_kind"] for o in caps)),
            "known_items": len(known), "known_spellings": len({o["form"] for o in known}),
            "open_items": len(opened), "open_spellings": len(spellings),
            "bar": GATE1, "met": len(known) >= GATE1["known"] and len(spellings) >= GATE1["open_spellings"]}


def shown(words, target):
    """The caption as a reader sees it: every place of the item's spelling hidden as [?], every other word with
    what the map says of it (a name only as "a name", an open word as "meaning unknown")."""
    out = []
    for w in words:
        level = w["level"]
        if w["form"] == target:
            out.append("[?]")
        elif level in ("meaning", "grammar"):
            out.append(f"{w['form']} ({w['gloss']})")
        elif level == "name":
            out.append(f"{w['form']} (a name)")
        elif level == "number":
            out.append(f"{w['form']} (a numeral)")
        elif level == "lost":
            out.append(f"{w['form']} (damaged)")
        else:
            out.append(f"{w['form']} (meaning unknown)")
    return " ".join(out)


def wrong_pictures(inv, sites, seed=SEED):
    """For each caption, the caption whose picture its wrong-picture readers see: drawn by lot among captions
    whose figure is of another kind and whose picture is not its own, at the same place when one exists, at any
    place otherwise."""
    rng = random.Random(seed)
    caps = captions(inv)
    out = {}
    for o in caps:
        pool = [p for p in caps if p["id"] != o["id"] and p["figure_kind"] != o["figure_kind"] and p["crop"] != o["crop"]]
        same = [p for p in pool if sites[p["id"]] == sites[o["id"]]]
        if not pool:
            raise SystemExit(f"{o['id']}: no caption with a figure of another kind")
        out[o["id"]] = rng.choice(same or pool)["id"]
    return out


def code(kind, i):
    return f"{kind[0]}{i + 1:03d}"


def clash(x, y, gl):
    """Whether two entries ({"item", "right", "wrong"}: an item and its picture in each condition) may not stand in
    one pack. One gives the other away where its caption shows the other's hidden spelling (two items of one
    caption, or a parallel caption), names it inside a gloss ("a form of qore"; spellings of NAMED letters or more,
    since shorter ones are English words and endings there), or shows a word with the gloss of the other's hidden
    word (another spelling of it); and a pack never shows one picture twice (two captions that drew the same wrong
    picture)."""
    def seen(o):
        ws = [w for w in gl[o["text"]] if w["form"] != o["form"]]
        glosses = {w["gloss"] for w in ws if w["level"] in ("meaning", "grammar")}
        named = {t for g in glosses for t in re.findall(r"[A-Za-z]+", g) if len(t) >= NAMED}
        return {w["form"] for w in ws} | named, glosses
    a, b = x["item"], y["item"]
    (fa, ga), (fb, gb) = seen(a), seen(b)
    return (a["form"] in fb or b["form"] in fa or a["gloss"] in gb or b["gloss"] in ga
            or x["right"] == y["right"] or x["wrong"] == y["wrong"])


def grouped(n, clashes, seed):
    """Items 0 to n - 1 cut into packs of at most BATCH, no pack holding two that clash: the items in an order
    drawn by lot, those with the most clashes first, each into the smallest pack it fits; as few packs as that
    allows. Each pack in an order drawn by lot."""
    rng = random.Random(seed)
    ranked = list(range(n))
    rng.shuffle(ranked)
    ranked.sort(key=lambda i: -len(clashes[i]))
    k = max(1, math.ceil(n / BATCH))
    while True:
        packs = [[] for _ in range(k)]
        for i in ranked:
            fits = [p for p in packs if len(p) < BATCH and not clashes[i].intersection(p)]
            if not fits:
                break
            min(fits, key=len).append(i)
        else:
            break
        k += 1
    packs = [p for p in packs if p]
    for p in packs:
        rng.shuffle(p)
    return packs


def make_packs(inv, gl, sites, kind):
    """The readers' packs, each read by one fresh agent. A pack shows its items, each under its code, with a
    picture under a name drawn by lot and the caption as `shown` gives it; it says nothing of the reader, the
    condition or the text. The right-picture readers' packs show each item's own crop, the wrong-picture readers'
    the crop drawn for its caption; A's packs and C's hold the same items in the same order, B's and D's another
    cut drawn by lot. Gives the items, the packs ({name: pack}) and the key, which is kept apart: each pack's
    reader, condition and items, and the crop behind each picture's name."""
    its = items(inv, gl, kind)
    crop = {o["id"]: o["crop"] for o in captions(inv)}
    wrong = wrong_pictures(inv, sites)
    entries = [{"item": o, "right": crop[o["text"]], "wrong": crop[wrong[o["text"]]]} for o in its]
    clashes = [{j for j, y in enumerate(entries) if j != i and clash(x, y, gl)} for i, x in enumerate(entries)]
    used = sorted({e[c] for e in entries for c in ("right", "wrong")})
    random.Random(f"{SEED}-{kind}-pictures").shuffle(used)
    folder = (HERE / "packs" / kind).relative_to(ROOT)
    named = {c: f"pic{k:02d}{pathlib.PurePath(c).suffix}" for k, c in enumerate(used, 1)}
    cuts = [(r, cond, p) for right, wrong_reader in zip(READERS["right"], READERS["wrong"])
            for p in grouped(len(its), clashes, f"{SEED}-{kind}-{right}{wrong_reader}")
            for r, cond in ((right, "right"), (wrong_reader, "wrong"))]
    numbers = list(range(1, len(cuts) + 1))
    random.Random(f"{SEED}-{kind}-packs").shuffle(numbers)
    packs, key = {}, {"packs": {}, "pictures": {name: c for c, name in named.items()}}
    for (r, cond, p), k in sorted(zip(cuts, numbers), key=lambda x: x[1]):
        name = f"pack{k:02d}"
        packs[name] = {"answers": f"{(HERE / 'answers' / kind / name).relative_to(ROOT)}.jsonl",
                       "items": [{"item": code(kind, i), "picture": f"{folder}/pictures/{named[entries[i][cond]]}",
                                  "caption": shown(gl[its[i]["text"]], its[i]["form"])} for i in p]}
        key["packs"][name] = {"reader": r, "condition": cond, "items": [code(kind, i) for i in p]}
    return its, packs, key


def answers_of(key, folder):
    """Every reader's answers, {(item, reader): answer}, from each pack's file in `folder`. Each pack must answer
    each of its items once, with a meaning of one to WORDS words, and no other item; it stops otherwise."""
    out, wrong = {}, []
    for name, p in key["packs"].items():
        f = folder / f"{name}.jsonl"
        got = {}
        for a in read_jsonl(f) if f.exists() else []:
            item, words = a.get("item"), str(a.get("meaning") or "").split()
            if item not in p["items"] or item in got:
                wrong.append(f"{name}: {'a second answer for' if item in got else 'not an item of the pack:'} {item!r}")
            elif not 1 <= len(words) <= WORDS:
                wrong.append(f"{name}, {item}: a meaning of {len(words)} words")
            got.setdefault(item, a)
        wrong += [f"{name}: no answer for {i}" for i in p["items"] if i not in got]
        out |= {(i, p["reader"]): got[i] for i in p["items"] if i in got}
    if wrong:
        raise SystemExit(f"{len(wrong)} faults in the answers: " + "; ".join(wrong[:10]))
    return out


def judge_pack(kind, its, answers):
    """The judges' pack: every answer with the item's meaning on the map, in an order drawn by lot, under a
    number that hides the reader and the condition; the key is kept apart."""
    gloss = {code(kind, i): o["gloss"] for i, o in enumerate(its)}
    rows = [(item, reader, a) for (item, reader), a in sorted(answers.items())]
    random.Random(f"{SEED}-{kind}-judges").shuffle(rows)
    pack = [{"id": f"j{i + 1:04d}", "reference": gloss[item], "answer": a["meaning"]} for i, (item, _, a) in enumerate(rows)]
    key = {f"j{i + 1:04d}": [item, reader] for i, (item, reader, _) in enumerate(rows)}
    return pack, key


def item_scores(key, judged):
    """Each item's score in each condition: the mean of its two readers, each reader's answer averaged over the
    judges. `judged` maps a judge to {answer id: score}."""
    by_answer = collections.defaultdict(list)
    for j in JUDGES:
        for aid, s in judged[j].items():
            if isinstance(s, bool) or s not in SCORES:
                raise SystemExit(f"judge {j}: score {s!r} for {aid}")
            by_answer[aid].append(s)
    if set(by_answer) != set(key) or any(len(v) != len(JUDGES) for v in by_answer.values()):
        raise SystemExit("the judges did not score every answer exactly once each")
    per = collections.defaultdict(dict)
    for aid, (item, reader) in key.items():
        per[item][reader] = sum(by_answer[aid]) / len(JUDGES)
    out = {}
    for item, rs in per.items():
        out[item] = {cond: sum(rs[r] for r in readers) / len(readers) for cond, readers in READERS.items()}
    return out


def sign_flip(diffs, clusters, draws=DRAWS, seed=SEED):
    """One-sided p that the mean right-minus-wrong difference is this large by chance: the items of one spelling
    flip their sign together. p counts the real arrangement as one draw."""
    sums = collections.defaultdict(float)
    for d, c in zip(diffs, clusters):
        sums[c] += d
    vals = list(sums.values())
    real = sum(vals)
    rng = random.Random(seed)
    hits = sum(1 for _ in range(draws) if sum(v if rng.random() < 0.5 else -v for v in vals) >= real - 1e-12)
    return (hits + 1) / (draws + 1)


def gate2(scores, forms):
    """Gate 2's four bars on the items' scores. `forms` gives each item's spelling."""
    its = sorted(scores)
    n = len(its)
    right = sum(scores[i]["right"] for i in its) / n if n else 0.0
    wrong = sum(scores[i]["wrong"] for i in its) / n if n else 0.0
    p = sign_flip([scores[i]["right"] - scores[i]["wrong"] for i in its], [forms[i] for i in its]) if n else 1.0
    return {"items": n, "right": round(right, 4), "wrong": round(wrong, 4), "gain": round(right - wrong, 4),
            "p": round(p, 4), "bar": GATE2,
            "met": n >= GATE2["items"] and right >= GATE2["right"] and right - wrong >= GATE2["gain"] - 1e-9
            and p < GATE2["p"]}


def agreement(judged):
    """How often the two judges gave the same score, and Cohen's kappa over the three scores."""
    ids = sorted(judged[JUDGES[0]])
    a = [judged[JUDGES[0]][i] for i in ids]
    b = [judged[JUDGES[1]][i] for i in ids]
    n = len(ids)
    same = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    chance = sum(ca[s] * cb[s] for s in SCORES) / (n * n)
    return {"answers": n, "same": round(same, 4), "kappa": round((same - chance) / (1 - chance), 4) if chance < 1 else None}


# --- files ---
def the_map():
    """The map with the seven layers it had when the page was set."""
    import themap
    names = tuple(l["name"] for l in themap.LAYERS)
    if names[:len(LAYERS)] != LAYERS:
        raise SystemExit(f"the map's layers are no longer {LAYERS}")
    return themap.current(upto=len(LAYERS))


def the_texts():
    return json.loads(TEXTS.read_text(encoding="utf-8"))


def the_sites():
    return {o["id"]: site_of(o["site"]) for o in the_texts()}


def the_inventory():
    return held(load_inventory(), [o["id"] for o in the_texts()])


def crop_file(crop):
    """The file of a crop the inventory names: from the repo's root where it stands there, else from
    data/sources/captions/."""
    p = pathlib.Path(crop)
    return ROOT / p if p.is_absolute() or (ROOT / p).is_file() else HERE / p


def read_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_once(path, data):
    """Writes a file the run makes once (bytes, or text): nothing to do where it stands as it would be written,
    and a stop where it stands otherwise, since a reader or a judge may have read it."""
    if path.exists():
        if (path.read_bytes() if isinstance(data, bytes) else path.read_text(encoding="utf-8")) != data:
            raise SystemExit(f"{path} stands already and is not what would be written now: the inventory, the map "
                             f"or the answers have changed since it was made")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        path.write_bytes(data)
    else:
        path.write_text(data, encoding="utf-8")


def dump(data):
    return json.dumps(data, ensure_ascii=False, indent=1) + "\n"


def scores_of(path):
    """A judge's scores: {answer id: score}, an answer once."""
    out = {}
    for o in read_jsonl(path):
        if o["id"] in out:
            raise SystemExit(f"{path.name}: {o['id']} is scored twice")
        out[o["id"]] = o["score"]
    return out


def gate2_met():
    s = HERE / "judges" / "known" / "scores.json"
    return s.exists() and json.loads(s.read_text(encoding="utf-8"))["gate2"]["met"] is True


def main(argv):
    cmd, kind = (argv + [None, None])[:2]
    kinds = {"count": (None,), "public": (None,), "packs": ("known", "open"), "judges": ("known",), "score": ("known",)}
    if kind not in kinds.get(cmd, ()):
        print(__doc__)
        return 2
    if cmd == "count":
        print(json.dumps(count(the_inventory(), the_map()), indent=1))
    elif cmd == "packs":
        inv, gl = the_inventory(), the_map()
        if kind == "known" and not count(inv, gl)["met"]:
            raise SystemExit("gate 1 is missed: the pilot stops (the page, section 4)")
        if kind == "open" and not gate2_met():
            raise SystemExit("gate 2 is not met: the open items are not read (the page, section 4)")
        its, packs, key = make_packs(inv, gl, the_sites(), kind)
        write_once(HERE / f"items_{kind}.json", dump(its))
        write_once(HERE / f"key_{kind}.json", dump(key))
        for name, crop in key["pictures"].items():
            write_once(HERE / "packs" / kind / "pictures" / name, crop_file(crop).read_bytes())
        for name, p in packs.items():
            write_once(HERE / "packs" / kind / f"{name}.json", dump(p))
        (HERE / "answers" / kind).mkdir(parents=True, exist_ok=True)
        print(f"{len(its)} items, {len(packs)} packs, {len(key['pictures'])} pictures in {HERE / 'packs' / kind}")
    elif cmd == "judges":
        its = json.loads((HERE / f"items_{kind}.json").read_text(encoding="utf-8"))
        key = json.loads((HERE / f"key_{kind}.json").read_text(encoding="utf-8"))
        ans = answers_of(key, HERE / "answers" / kind)
        expected = {(code(kind, i), r) for i in range(len(its)) for rs in READERS.values() for r in rs}
        if set(ans) != expected:
            raise SystemExit(f"answers missing: {sorted(expected - set(ans))[:5]}; extra: {sorted(set(ans) - expected)[:5]}")
        pack, jkey = judge_pack(kind, its, ans)
        d = HERE / "judges" / kind
        write_once(d / "pack.json", dump(pack))
        write_once(d / "key.json", dump(jkey))
        print(f"{len(pack)} answers to judge in {d / 'pack.json'}")
    elif cmd == "score":
        its = json.loads((HERE / f"items_{kind}.json").read_text(encoding="utf-8"))
        d = HERE / "judges" / kind
        key = {k: tuple(v) for k, v in json.loads((d / "key.json").read_text(encoding="utf-8")).items()}
        judged = {j: scores_of(d / f"{j}.jsonl") for j in JUDGES}
        scores = item_scores(key, judged)
        forms = {code(kind, i): o["form"] for i, o in enumerate(its)}
        out = {"gate2": gate2(scores, forms), "judges": agreement(judged)}
        (d / "scores.json").write_text(json.dumps({"items": scores} | out, indent=1), encoding="utf-8")
        print(json.dumps(out, indent=1))
    elif cmd == "public":
        inv, gl = the_inventory(), the_map()
        figs = {"gate1": count(inv, gl)}
        for kind in ("known", "open"):
            f = HERE / f"items_{kind}.json"
            if f.exists() and json.loads(f.read_text(encoding="utf-8")) != items(inv, gl, kind):
                raise SystemExit(f"the {kind} items are no longer those the packs were made from")
        s = HERE / "judges" / "known" / "scores.json"
        if s.exists():
            got = json.loads(s.read_text(encoding="utf-8"))
            figs |= {"gate2": got["gate2"], "judges": got["judges"]}
        PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {PUBLIC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
