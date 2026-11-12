"""The coverage map and the check against two editions, counted again on corpus_v6.

  python3 -I src/v6/recount.py          writes data/sources/v6/coverage/ and data/sources/v6/recount.json

Local only (Rilly's lexicon, the analysts' answers, the judges' answers). No new analyst and no new judge:

1. The coverage map (src/coverage.py, `correct`) runs as it is on the rows of corpus_v6. A word keeps what the
   lookup or an analyst gave its spelling; a word at a place the row marks as a name is a name, as a masked name
   was; a spelling that no analyst saw is "unknown" as before, and counted apart as not analysed.
2. The check against Millet 2005 and FHN III (src/experts/) is counted on the judged words that still stand in
   corpus_v6: the word of the corpus_v5 text is aligned with the inscription's preferred reading, and a row is
   carried over when the spelling and the map's level are the same. The rest is listed with what changed.

The old figures are read from the local files of the first counts and written beside the new ones.
"""
import collections
import difflib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(Path(__file__).resolve().parent)]
import coverage as C   # noqa: E402
import tally as T      # noqa: E402

CORPUS = ROOT / "data/corpus_v6.jsonl"
V5 = ROOT / "data/corpus_v5.jsonl"
MAP = ROOT / "data/sources/v6/map.jsonl"
OUT = ROOT / "data/sources/v6"
PACKS = ROOT / "data/sources/coverage/packs"
OLD = ROOT / "data/sources/coverage/corrected/figures.json"
EXPERT = ROOT / "data/sources/expert"
GROUPS = {"otten": "Otten's files with real names (Millet 1968, the three narratives)",
          "griffith": "Griffith's other volumes", "karanog": "Karanog and Shablul (Griffith 1911)",
          "mnl": "the Meroitic Newsletter"}


def rows_for_map(corpus):
    """The rows of corpus_v6 as src/coverage.py takes them."""
    out = []
    for c in corpus:
        family, _, rest = c["reading"].partition(":")
        row = {"id": c["id"], "text": c["text"], "names": c["names"], "group": GROUPS[family], "v5": c["v5"]}
        if family == "karanog":
            row["karanog"] = rest
        out.append(row)
    return out


def part(figs):
    f = figs["all"]
    return {"texts": f["texts"], "words": f["words"], "translated": f["translated"],
            "share": round(f["translated"] / f["words"], 4) if f["words"] else None, "levels": f["levels"]}


def coverage(corpus, old_forms, packs=PACKS):
    """(glossed, figures) of the corrected coverage map on corpus_v6."""
    es = C.lexicon()
    words, affixes, heads = C.index(es)
    analysed, report = C.analyses(packs, heads)
    rows = rows_for_map(corpus)
    glossed = C.gloss_texts(rows, words, affixes, analysed)
    report["corrections"] = C.correct(glossed, words, affixes, heads)
    figs = C.figures(glossed)
    ranked, texts_by = C.ranking(glossed, heads)
    was = [(r, gs) for r, gs in glossed if r["v5"]]
    new = [(r, gs) for r, gs in glossed if not r["v5"]]
    nobody = [(g["form"], bool(r["v5"])) for r, gs in glossed for g in gs if g["by"] == "nobody"]
    unseen = [f for f, _ in nobody if f not in old_forms]
    unseen_old = sum(in_v5 for f, in_v5 in nobody if f not in old_forms)
    out = {"all": part(figs), "by_part": {k: {"texts": v["texts"], "words": v["words"], "translated": v["translated"],
                                               "share": round(v["translated"] / v["words"], 4)}
                                          for k, v in figs.items() if k in GROUPS.values()},
           "near_copies_once": {"texts": figs["near-copies counted once"]["texts"],
                                "words": figs["near-copies counted once"]["words"],
                                "translated": figs["near-copies counted once"]["translated"]},
           "inscriptions_that_were_in_corpus_v5": part(C.figures(was)) if was else None,
           "inscriptions_new_to_the_corpus": part(C.figures(new)) if new else None,
           "texts": texts_by, "pieces_without_an_accepted_meaning": len(ranked),
           "names_by_the_source": sum(g["source"].startswith("a name, as the source") for _, gs in glossed for g in gs),
           "not_analysed": {"words": len(unseen), "spellings": len(set(unseen)),
                            "in_new_inscriptions": len(unseen) - unseen_old,
                            "in_inscriptions_that_were_in_corpus_v5": unseen_old,
                            "unknown_words_seen_before": len(nobody) - len(unseen)},
           "corrections": {k: v for k, v in report["corrections"].items() if k != "joins"}}
    return glossed, ranked, texts_by, figs, report, out


def align(old, new):
    """{place in old: place in new} for the words that stand in both, in order (the longest matching blocks)."""
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    return {i + k: j + k for i, j, n in sm.get_matching_blocks() for k in range(n)}


def unmatched(form, place, places, new):
    """Why a word of the old text has no place in the new one: the words of the new text between the nearest
    aligned words around it hold it inside a longer word (written apart in corpus_v5, as one in the preferred
    reading), or hold other words (spelled otherwise), or none (not in the preferred reading)."""
    before = max((i for i in places if i < place), default=None)
    after = min((i for i in places if i > place), default=None)
    there = new[places[before] + 1 if before is not None else 0:places[after] if after is not None else len(new)]
    if any(form in w and form != w for w in there):
        return "the word is a part of a longer word in the preferred reading"
    return "the word is spelled otherwise in the preferred reading" if there else "the word is not in the preferred reading"


def experts(glossed, mapped, v5_text, folder=EXPERT):
    """The check against the editions on the judged words that still stand in corpus_v6: (figures, [what changed])."""
    rows = T.load_rows(folder / "rows.jsonl")
    judges = collections.defaultdict(dict)
    for f in sorted((folder / "answers").glob("judge*_*.jsonl")):
        name, _, pack = f.stem.partition("_")
        answers, _ = T.load_answers(f, {r["row"] for r in rows if r["pack"] == pack})
        judges[name].update(answers)
    ins_of = {m["id"]: m.get("inscription") for m in mapped}
    by_id = {r["id"]: gs for r, gs in glossed}
    places = {}
    kept, changed = [], []
    for r in rows:
        tid = r["text"]
        gs = by_id.get(ins_of.get(tid))
        if gs is None:
            changed.append({"row": r["row"], "text": tid, "form": r["form"], "why": "its inscription is not in corpus_v6"})
            continue
        if tid not in places:
            places[tid] = align(v5_text[tid].split(), [g["form"] for g in gs])
        j = places[tid].get(r["place"])
        if j is None:
            changed.append({"row": r["row"], "text": tid, "form": r["form"],
                            "why": unmatched(r["form"], r["place"], places[tid], [g["form"] for g in gs])})
        elif gs[j]["level"] != r["level"]:
            changed.append({"row": r["row"], "text": tid, "form": r["form"],
                            "why": f"the map's level is {gs[j]['level']}, it was {r['level']}"})
        else:
            kept.append(r)
    old = T.figures(rows, judges)
    new = T.figures(kept, judges) if kept else None
    brief = lambda f: {"rows": f["rows"], "decoys": f["decoys"], "texts": f["texts"], "translated": f["translated"]["all"]}
    return {"corpus_v5": brief(old), "corpus_v6": brief(new) if new else None, "carried": len(kept),
            "not_carried": len(changed), "why": dict(collections.Counter(c["why"].split(",")[0] for c in changed))}, changed


def main(argv):
    if argv[1:]:
        sys.exit(__doc__)
    corpus = [json.loads(l) for l in CORPUS.read_text().splitlines() if l.strip()]
    v5 = [json.loads(l) for l in V5.read_text().splitlines() if l.strip()]
    mapped = [json.loads(l) for l in MAP.read_text().splitlines() if l.strip()]
    old_forms = {w for r in v5 for w in r["text"].split()}
    glossed, ranked, texts_by, figs, report, cov = coverage(corpus, old_forms)
    out = OUT / "coverage"
    C.write(glossed, ranked, figs, texts_by, report, out=out)
    old = json.loads(OLD.read_text())
    cov["corpus_v5"] = {"all": part(old["figures"]),
                        "near_copies_once": {k: old["figures"]["near-copies counted once"][k] for k in ("texts", "words", "translated")},
                        "texts": old["texts"]}
    exp, changed = experts(glossed, mapped, {r["id"]: r["text"] for r in v5})
    (OUT / "recount.json").write_text(json.dumps({"coverage": cov, "experts": exp}, ensure_ascii=False, indent=1) + "\n")
    (OUT / "experts_changed.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in changed))
    print(json.dumps({"coverage": cov, "experts": exp}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv)
