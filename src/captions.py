"""The caption pilot (data/discovery/caption_pilot.md): the captions of temple reliefs read against their pictures.

Gate 1 counts the material, gate 2 tests the pictures on caption words whose meaning is known (each read with its
own picture and with a wrong one), gate 3 reads the open words only if gate 2 is met. The rules and bars were set
and pushed before anything ran (the page, sections 3 and 4); this file carries them out.

  python3 -I src/captions.py count          gate 1 from the inventory and the map as it stands
  python3 -I src/captions.py packs known     the readers' packs for gate 2 (data/sources/captions/packs/known/)
  python3 -I src/captions.py judges known    the judges' pack, once every reader's answers are in
  python3 -I src/captions.py score known     gate 2 from the two judges' scores
  python3 -I src/captions.py public          data/discovery/caption_pilot_figures.json

The inventory (data/sources/captions/inventory.jsonl), the cut pictures, the packs, the answers and the scores are
local: they hold the readings of the map and the plates' crops. Only the counts go public.
"""
import collections
import json
import pathlib
import random
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src")]

HERE = ROOT / "data/sources/captions"
INVENTORY = HERE / "inventory.jsonl"
TEXTS = HERE / "texts87.json"
PUBLIC = ROOT / "data/discovery/caption_pilot_figures.json"

SEED = 17                    # the wrong pictures, the readers' order and the sign-flip test (page, section 4)
CAP = 3                      # a spelling counts in at most its first three captions (section 3)
EXCLUDED = ("meaning", "grammar", "name", "number", "lost")   # the levels an open item may not have
KINDS = ("god", "goddess", "king", "queen", "prince", "official", "priest", "animal", "object", "scene")
READERS = {"right": ("A", "B"), "wrong": ("C", "D")}           # two readers a condition, none in both
JUDGES = ("J1", "J2")
BATCH = 12                   # items in one reader's pack
DRAWS = 10_000
GATE1 = {"known": 20, "open_spellings": 10}
GATE2 = {"items": 20, "right": 0.50, "gain": 0.20, "p": 0.05}
SCORES = (0, 0.5, 1)


def load_inventory(path=INVENTORY):
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    for o in rows:
        if o.get("caption") and o.get("figure_kind") not in KINDS:
            raise SystemExit(f"{o['id']}: figure_kind {o.get('figure_kind')!r} is not one of {KINDS}")
    return rows


def order(text_id):
    """The texts in REM order, the texts without a REM number after them (section 3: "by REM number")."""
    return (not text_id.startswith("REM "), text_id)


def site_of(site):
    """The place a text comes from: the first word of its site, folded to plain letters ("Meroë, temple of Amun"
    and "Meroe City" are both meroe)."""
    first = site.split(",")[0].split("(")[0].strip().split()[0]
    return unicodedata.normalize("NFKD", first).encode("ascii", "ignore").decode().lower()


def captions(inv):
    return sorted((o for o in inv if o.get("caption")), key=lambda o: order(o["id"]))


def items(inv, gl, kind):
    """The items of one kind ("known" or "open"): one word in one caption, its first place there; a spelling
    in at most its first CAP captions."""
    if kind not in ("known", "open"):
        raise ValueError(kind)
    seen = collections.Counter()
    out = []
    for o in captions(inv):
        taken = set()
        for n, w in enumerate(gl.get(o["id"], []), 1):
            fits = w["level"] == "meaning" if kind == "known" else w["level"] not in EXCLUDED
            if not fits or w["form"] in taken or seen[w["form"]] >= CAP:
                continue
            seen[w["form"]] += 1
            taken.add(w["form"])
            out.append({"text": o["id"], "n": n, "form": w["form"], "gloss": w.get("gloss", ""), "level": w["level"]})
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
    whose figure is of another kind, at the same place when one exists, at any place otherwise."""
    rng = random.Random(seed)
    caps = captions(inv)
    out = {}
    for o in caps:
        pool = [p for p in caps if p["id"] != o["id"] and p["figure_kind"] != o["figure_kind"]]
        same = [p for p in pool if sites[p["id"]] == sites[o["id"]]]
        if not pool:
            raise SystemExit(f"{o['id']}: no caption with a figure of another kind")
        out[o["id"]] = rng.choice(same or pool)["id"]
    return out


def code(kind, i):
    return f"{kind[0]}{i + 1:03d}"


def make_packs(inv, gl, sites, kind):
    """The readers' packs: for each reader, every item once, in an order of its own, BATCH items a pack; the
    right-picture readers see the item's own crop, the wrong-picture readers the crop of its drawn caption."""
    its = items(inv, gl, kind)
    crop = {o["id"]: o["crop"] for o in captions(inv)}
    wrong = wrong_pictures(inv, sites)
    packs = {}
    for cond, readers in READERS.items():
        for r in readers:
            entries = [{"item": code(kind, i), "picture": crop[o["text"]] if cond == "right" else crop[wrong[o["text"]]],
                        "caption": shown(gl[o["text"]], o["form"])} for i, o in enumerate(its)]
            random.Random(f"{SEED}-{kind}-{r}").shuffle(entries)
            for b in range(0, len(entries), BATCH):
                packs[f"{r}_{b // BATCH + 1}"] = {"reader": r, "condition": cond, "items": entries[b:b + BATCH]}
    return its, packs


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
            if s not in SCORES:
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
    import themap
    return themap.current()


def the_sites():
    return {o["id"]: site_of(o["site"]) for o in json.loads(TEXTS.read_text(encoding="utf-8"))}


def read_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def answers_of(kind):
    """Every reader's answers: {(item, reader): answer}. Each reader must answer each item exactly once."""
    out = {}
    for f in sorted((HERE / "answers" / kind).glob("*.jsonl")):
        reader = f.stem.split("_")[0]
        for a in read_jsonl(f):
            k = (a["item"], reader)
            if k in out:
                raise SystemExit(f"{f.name}: a second answer for {k}")
            out[k] = a
    return out


def main(argv):
    cmd, kind = (argv + [None, None])[:2]
    inv = load_inventory()
    if cmd == "count":
        print(json.dumps(count(inv, the_map()), indent=1))
    elif cmd == "packs":
        gl = the_map()
        its, packs = make_packs(inv, gl, the_sites(), kind)
        d = HERE / "packs" / kind
        d.mkdir(parents=True, exist_ok=True)
        for name, p in packs.items():
            (d / f"{name}.json").write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
        (HERE / f"items_{kind}.json").write_text(json.dumps(its, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(its)} items, {len(packs)} packs in {d}")
    elif cmd == "judges":
        its = json.loads((HERE / f"items_{kind}.json").read_text(encoding="utf-8"))
        ans = answers_of(kind)
        expected = {(code(kind, i), r) for i in range(len(its)) for rs in READERS.values() for r in rs}
        if set(ans) != expected:
            raise SystemExit(f"answers missing: {sorted(expected - set(ans))[:5]}; extra: {sorted(set(ans) - expected)[:5]}")
        pack, key = judge_pack(kind, its, ans)
        d = HERE / "judges" / kind
        d.mkdir(parents=True, exist_ok=True)
        (d / "pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=1), encoding="utf-8")
        (d / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
        print(f"{len(pack)} answers to judge in {d / 'pack.json'}")
    elif cmd == "score":
        its = json.loads((HERE / f"items_{kind}.json").read_text(encoding="utf-8"))
        d = HERE / "judges" / kind
        key = {k: tuple(v) for k, v in json.loads((d / "key.json").read_text(encoding="utf-8")).items()}
        judged = {j: {o["id"]: o["score"] for o in read_jsonl(d / f"{j}.jsonl")} for j in JUDGES}
        scores = item_scores(key, judged)
        forms = {code(kind, i): o["form"] for i, o in enumerate(its)}
        out = {"gate2": gate2(scores, forms), "judges": agreement(judged)}
        (d / "scores.json").write_text(json.dumps({"items": scores} | out, indent=1), encoding="utf-8")
        print(json.dumps(out, indent=1))
    elif cmd == "public":
        figs = {"gate1": count(inv, the_map())}
        s = HERE / "judges" / "known" / "scores.json"
        if s.exists():
            got = json.loads(s.read_text(encoding="utf-8"))
            figs |= {"gate2": got["gate2"], "judges": got["judges"]}
        PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {PUBLIC.relative_to(ROOT)}")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
