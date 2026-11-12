"""Analysts for the spellings of corpus_v6 that none has read, and what their answers change.

  python3 -I src/v6/readers.py packs     the packs for the spellings no pack holds yet (data/sources/v6/packs/)
  python3 -I src/v6/readers.py count     the coverage map of corpus_v6 without and with the new answers

Local only (Rilly's lexicon, corpus_v6, the analysts' answers). The packs are those of src/coverage.py: words.jsonl,
lexicon.tsv, BRIEF.md, and the analyst's analysis.jsonl. They are numbered after the packs of the first run and
kept in a folder of their own, so that the map of corpus_v5 is rebuilt from the same answers as before. `count`
leaves the figures of src/v6/recount.py as they are and writes its own in a folder of its own (OUT, not the
folder of src/v6/packs.py, whose figures src/v6/public.py publishes).
"""
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(Path(__file__).resolve().parent)]
import coverage as C   # noqa: E402
import recount as R    # noqa: E402

NEW = ROOT / "data/sources/v6/packs"
OUT = ROOT / "data/sources/v6/analysts"
PUBLIC = ROOT / "data/discovery/corpus_v6_readers.json"
PER, TWICE = 133, 110                  # words in a pack; the most frequent words read by a second analyst


def masked(rows):
    """The rows with every word that the source of the reading tags as a personal name written NAME, as the
    older corpus masks a name: the lookup then takes it for a name, and no analyst is asked about it."""
    out = []
    for r in rows:
        named = set(r.get("names") or ())
        out.append(dict(r, text=" ".join("NAME" if i in named and not t.isdigit() else t
                                          for i, t in enumerate(r["text"].split()))))
    return out


def packed(folder, letters="AB"):
    """The words of the packs of a folder whose name starts with one of letters, as the packs hold them (word,
    count, texts, contexts), pack by pack."""
    return [json.loads(l) for p in (sorted(folder.iterdir()) if folder.exists() else ())
            if p.is_dir() and p.name[:1] in letters for l in (p / "words.jsonl").read_text().splitlines() if l.strip()]


def held(*folders):
    """The words that a pack of the folders holds already."""
    return {w["word"] for f in folders for w in packed(f)}


def unread(rows, words, affixes, have):
    """The words the lookup leaves on the rows and no pack holds, the most frequent first (as coverage.left)."""
    return [w for w in C.left(masked(rows), words, affixes) if w["word"] not in have]


def write_packs(new, es, old=R.PACKS, out=NEW, per=PER, twice=TWICE):
    """Packs A (every word once) and B (the `twice` most frequent again, for a second analyst), numbered after
    the last pack of each letter in old and out. Refuses when out already holds packs: the answers given on
    them would no longer match."""
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"{out} holds packs already: not writing them again")
    last = lambda letter: max((int(p.name[1:]) for f in (old, out) if f.exists() for p in f.iterdir()
                               if p.is_dir() and p.name[0] == letter and p.name[1:].isdigit()), default=0)
    table, made = C.lexicon_table(es), []
    for letter, words in (("A", new), ("B", new[:twice])):
        first = last(letter)
        for k in range(0, len(words), per):
            pack = out / f"{letter}{first + k // per + 1:03d}"
            pack.mkdir(parents=True)
            (pack / "words.jsonl").write_text("".join(json.dumps(w, ensure_ascii=False) + "\n" for w in words[k:k + per]))
            (pack / "lexicon.tsv").write_text(table)
            (pack / "BRIEF.md").write_text(C.BRIEF.read_text())
            made.append(pack.name)
    return made


def side(g):
    return g["level"] in C.TRANSLATED


def longer_joins(glossed, words, affixes):
    """How many words more the map's third correction (a word written apart) would translate without its limit on
    the length of a piece: counted on a copy of each text of the corrected map, not applied."""
    whole, n = C.written_whole(glossed), 0
    for _, gs in glossed:
        copy = list(gs)
        C.joins(copy, words, affixes, whole, fragment=None)
        n += sum(not side(a) and side(b) for a, b in zip(gs, copy))
    return n


def count(corpus, old=R.PACKS, new=NEW):
    """The corrected map of corpus_v6 with the answers of the first run alone and with the new answers added:
    (glossed with them, figures). An answer of the first run stands where both hold a word."""
    es = C.lexicon()
    words, affixes, heads = C.index(es)
    first, _ = C.analyses(old, heads)
    more, report = C.analyses(new, heads)
    rows = R.rows_for_map(corpus)
    maps = {}
    for name, analysed in (("before", first), ("after", {**more, **first})):
        glossed = C.gloss_texts(rows, words, affixes, analysed)
        C.correct(glossed, words, affixes, heads)
        maps[name] = glossed
    figs = {name: R.part(C.figures(g)) for name, g in maps.items()}
    figs["by_part"] = {name: {k: {"words": v["words"], "translated": v["translated"]}
                              for k, v in C.figures(g).items() if k in R.GROUPS.values()} for name, g in maps.items()}
    moved = collections.Counter()
    for (_, a), (_, b) in zip(maps["before"], maps["after"]):
        moved.update(y["level"] for x, y in zip(a, b) if not side(x) and side(y))
    figs["newly_translated"] = {"words": sum(moved.values()), **{l: moved[l] for l in C.TRANSLATED}}
    figs["still_not_analysed"] = sum(g["by"] == "nobody" for _, gs in maps["after"] for g in gs)
    figs["longer_joins"] = longer_joins(maps["after"], words, affixes)
    levels = collections.Counter(g["level"] for g in more.values())
    figs["answers"] = {"spellings": len(more), "running_words": sum(w["count"] for w in packed(new, "A")),
                       "translated": sum(side(g) for g in more.values()),
                       "levels": {l: levels[l] for l in C.LEVELS if levels[l]},
                       "dropped": len(report["dropped"]), "missing": len(report["missing"]),
                       "read_twice": report["twice"], "same_level": report["same_level"],
                       "same_translated_or_not": report["same_translated_or_not"],
                       "translated_by": report["translated_by"]}
    return maps["after"], figs


def main(argv):
    corpus = [json.loads(l) for l in R.CORPUS.read_text().splitlines() if l.strip()]
    if argv[1:] == ["packs"]:
        es = C.lexicon()
        words, affixes, _ = C.index(es)
        new = unread(R.rows_for_map(corpus), words, affixes, held(R.PACKS, NEW))
        made = write_packs(new, es)
        print(f"{len(new)} spellings, {sum(w['count'] for w in new)} running words; packs {made[0]} to {made[-1]} in {NEW}")
        return
    if argv[1:] == ["count"]:
        glossed, figs = count(corpus)
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "glosses.jsonl").write_text("".join(json.dumps({"id": r["id"], "glosses": gs}, ensure_ascii=False) + "\n"
                                                   for r, gs in glossed))
        for path in (OUT / "figures.json", PUBLIC):
            path.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n")
        print(json.dumps({k: figs[k] for k in ("before", "after", "newly_translated", "still_not_analysed", "answers")},
                         ensure_ascii=False, indent=1))
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
