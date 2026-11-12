"""Closing the two gaps of the list of missing meanings (local only; run with python3 -I).

  reader   the pack of the experts' comments on the 31 held entries, for a reader that lists every meaning given
  table    the judges' table: each meaning the two readers listed, beside our map's reading of the word; each
           judge sees a decoy in place of our reading on a tenth of the lines, on different lines
           (answers/extractor.jsonl and answers/reader_held.jsonl -> packs/meanings_judgeN.md)
  count    the judges' verdicts (answers/meanings_judgeN.jsonl) and the complete list, lacking.tsv

reader and table refuse to write their pack again once it has been answered. The readers' and judges' files are
untrusted data: only their named fields are read.
"""
import collections
import json
import pathlib
import random
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import missing as M                                    # noqa: E402
import prepare as P                                    # noqa: E402
import tally as T                                      # noqa: E402

FOLDER = M.FOLDER
READERS = ("extractor", "reader_held")
SEED = 17
DECOYS = 0.10
OTHERWISE = ("partly", "differ", "new")                # verdicts that say our reading is not the expert's
ASKED = ("agree",) + OTHERWISE                         # the verdicts the judges are given
SHORT = {"the", "and", "one", "his", "her", "its", "who", "was", "are", "for", "not", "has", "him", "may", "all",
         "any", "but", "own", "per", "two"}             # words of three letters that carry no meaning of their own

READER = """# Meanings an expert gives to Meroitic words: a list from the comments of two printed editions

Below are the comment sections of two printed editions of Meroitic inscriptions, one section per inscription.
Sections marked "Millet 2005" come from N. B. Millet, "The Meroitic Inscriptions from Gebel Adda" (the text layer
of a PDF: some letters and the dots under doubtful letters have fallen onto lines of their own). Sections marked
"FHN III" come from Fontes Historiae Nubiorum III (an OCR of a scan: expect misread letters, "fi" or "ii" for the
letter ñ, a mark like „ between words).

List **every Meroitic word, ending or fixed phrase to which the expert gives a meaning** anywhere in these
sections: about the inscription under discussion or, in passing, about a word of another inscription. Include
meanings the expert only proposes, and mark them. Leave out words the expert only transliterates, personal names
taken simply as names, and place names taken simply as places. Use only what is printed here, not your own
knowledge of Meroitic.

Write the list to the file `data/sources/expert/answers/reader_held.jsonl` as JSON lines, nothing else in the file:

    {{"source": "Millet 2005", "entries": ["GA04", "GA29"], "word": "pelmos", "meaning": "general", "doubt": false, "quote": "the generals of the river"}}

One line per source, word and meaning: when the same edition gives the same word the same meaning in several
sections, write one line and name the sections in `entries` (at most five). `word` is the Meroitic word as the
expert spells it (in Millet x is ḫ and h is ẖ); `meaning` has at most ten words; `doubt` is true when the expert
marks the meaning as unsure; `quote` is at most fifteen words of the expert's own that show it.

Read only this file. Do not open other files in the repository, do not search the web. When the file is written,
reply with one line: how many lines you wrote.

"""

JUDGE = """# Two readings of Meroitic words: do they give the same meaning?

Each line of the table below has a Meroitic word or phrase as a printed edition spells it, the meaning that
edition gives it ("(unsure)" when the edition marks it so), and the reading another source gives the same word.
For a phrase of several words the other reading lists its words' readings with " / " between them; a "+x" at the
end of a reading names an ending. Some of the other readings will be wrong.

Give every row one verdict, judging only from the two meanings printed on the line, not from your own knowledge
of Meroitic:

- `agree`: the two give the word the same meaning (the wording may differ; "perhaps" against a plain statement
  is still `agree`; a title left as the same title is `agree`).
- `partly`: the two overlap but differ in a way that matters (another relation of kin, another rank, a narrower
  or wider thing).
- `differ`: the two give different meanings.
- `new`: the edition gives a meaning and the other reading gives none, or only says what kind of word it is
  ("[title]", "[noun]", "a title", "adjective").

Write your answers to the file `{answers}` as JSON lines, one line per row, in the order of the table, nothing
else in the file:

    {{"row": "X001", "verdict": "agree"}}

Every row id must appear exactly once. Read only this file. Do not open other files in the repository, do not
search the web. When the file is written, reply with one line: the number of rows you wrote.

| row | word | the edition's meaning | the other reading |
|---|---|---|---|
"""


def comments(block):
    """An entry from its comments on (Millet's COMMENTARY and RENDERING, FHN's Comments); the whole entry when it
    has no such heading."""
    m = re.search(r"^(COMMENTARY|RENDERING|Comments)\s*$", block, re.M)
    return block[m.start():].strip() if m else block.strip()


def reader(out=FOLDER):
    """The second reader's pack. Refuses to write it again once the reader has answered."""
    if (out / "answers" / "reader_held.jsonl").exists():
        raise SystemExit(f"{out}/answers holds the second reader's list: not writing its pack again")
    text = P.blocks()
    parts = [READER]
    for source, label in (("millet", "Millet 2005"), ("fhn", "FHN III")):
        for entry in P.HELD[source]:
            parts.append(f"\n---\n\n## {label}, entry {entry}\n\n```\n{comments(text[source, entry])}\n```\n")
    f = out / "packs" / "reader_held.md"
    f.write_text("".join(parts), encoding="utf-8")
    print(f.name, f.stat().st_size, "bytes,", len(parts) - 1, "sections")


def our_map():
    """(words, affixes, in_map) as src/experts/missing.py loads them: the lexicon's index and the map's own words."""
    return M.our_map()[:3]


held = M.held                                          # (how our map holds a word or a phrase, our reading of it)


def source_of(text):
    return "Millet 2005" if "millet" in text.lower() else "FHN III" if "fhn" in text.lower() else text[:20]


def answers_of(name, folder=FOLDER):
    """A reader's lines as dicts with source, entries, word, meaning, doubt; lines that are not such a line are
    left out."""
    out = []
    path = folder / "answers" / f"{name}.jsonl"
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        try:
            a = json.loads(raw)
            word, meaning, source = str(a["word"]).strip(), str(a["meaning"]).strip(), source_of(str(a["source"]))
        except (ValueError, KeyError, TypeError):
            continue
        entries = a.get("entries", a.get("entry", ""))
        entries = [str(e) for e in entries] if isinstance(entries, list) else [str(entries)]
        if word and meaning:
            out.append({"source": source, "entries": [e for e in entries if e][:5], "word": word,
                        "meaning": meaning[:120], "doubt": a.get("doubt") is True, "from": name})
    return out


def lines(found, m):
    """The readers' meanings, once per source, word and meaning, each with how our map holds the word. A line is
    judged when our map gives the word a reading. The meaning counts as unsure when every mention marks it so."""
    out = {}
    for a in found:
        key = (a["source"], re.sub(r"[^a-zñ ]", "", a["word"].lower()).strip(),
               re.sub(r"\W+", " ", a["meaning"].lower()).strip())
        if key not in out:
            state, reading = held(a["word"], a["source"], m)
            out[key] = {**a, "entries": [], "our map": state, "ours": reading,
                        "judged": bool(re.sub(r"[^A-Za-zḫẖ]", "", reading))}
        row = out[key]
        row["entries"] = sorted(set(row["entries"]) | set(a["entries"]))
        row["doubt"] = row["doubt"] and a["doubt"]
        row["from"] = row["from"] if a["from"] in row["from"] else f"{row['from']}, {a['from']}"
    rows = list(out.values())
    for n, r in enumerate(rows, 1):
        r["line"] = f"L{n:03d}"
    return rows


def content(text):
    """The words of three letters or more that carry a reading's meaning, each cut to a crude stem (no final s,
    five letters at most), so that "mother" and "of the mothers" count as the same word, and "god" or "son" count
    at all."""
    return {w.rstrip("s")[:5] for w in re.findall(r"[a-zḫẖ]{3,}", text.lower())
            if w not in M.STOP and w not in SHORT}


def shares(a, b):
    """Whether two sets of stems share a word: the same stem, or one the start of the other ("god", "godde")."""
    return any(x.startswith(y) or y.startswith(x) for x in a for y in b)


def parts(reading):
    """How many words a reading covers: a phrase's reading has its words' readings with " / " between them."""
    return reading.count(" / ") + 1


def decoys_on(chosen, judged, rnd):
    """{line id: a reading that is not ours} for the chosen lines. A decoy is another judged line's reading that
    shares no content word with our real reading nor with the expert's meaning of the line, so it can neither
    echo the one nor fit the other, and covers as many words, so that its shape does not give it away."""
    shown = {}
    for r in chosen:
        near = content(r["ours"]) | content(r["meaning"])
        far = sorted({o["ours"] for o in judged if content(o["ours"]) and not shares(content(o["ours"]), near)
                      and parts(o["ours"]) == parts(r["ours"])})
        if far:
            shown[r["line"]] = rnd.choice(far)
    return shown


def decoys_by_judge(rows, judges=2, seed=SEED, share=DECOYS):
    """One {line id: decoy} per judge, on lines that do not overlap: each judge sees a tenth of the judged lines
    with a decoy in place of our reading, and every line keeps our reading for the other judge."""
    rnd = random.Random(seed)
    judged = [r for r in rows if r["judged"]]
    n = min(round(len(judged) * share), len(judged) // judges)
    drawn = rnd.sample(judged, n * judges)
    return [decoys_on(drawn[j * n:(j + 1) * n], judged, rnd) for j in range(judges)]


def table_rows(rows, seed=SEED, share=DECOYS):
    """The judges' rows: every judged line once, shuffled and then numbered. A line decoyed for a judge carries
    that judge's number in "decoy" (0: for neither) and the reading shown to that judge in "decoy_reading"; the
    other judge sees our reading. So no line is without a real verdict, and no judge sees a word and its meaning
    twice, which would give the decoy away. Lines that are not judged follow, without a row id."""
    first, second = decoys_by_judge(rows, 2, seed, share)
    out = []
    for r in rows:
        if r["judged"]:
            judge = 1 if r["line"] in first else 2 if r["line"] in second else 0
            out.append(dict(r, decoy=judge, decoy_reading=first.get(r["line"]) or second.get(r["line"])))
    random.Random(f"order {seed}").shuffle(out)    # a seed of its own: with the draw's seed, the drawn lines end last
    for n, t in enumerate(out, 1):
        t["row"] = f"X{n:03d}"
    return out + [dict(r, decoy=0, decoy_reading=None, row=None) for r in rows if not r["judged"]]


def shown_to(r, judge):
    """The reading a judge sees on a row: the decoy when the row is decoyed for that judge, else ours."""
    return r["decoy_reading"] if r["decoy"] == judge else r["ours"]


def table(out=FOLDER):
    if any((out / "answers").glob("meanings_judge*.jsonl")):
        raise SystemExit("answers/ holds the judges' answers on the table: not writing it again")
    found = [a for name in READERS for a in answers_of(name, out)]
    rows = table_rows(lines(found, our_map()))
    cell = lambda text: text.replace("|", "/")
    for judge in (1, 2):
        body = "".join(f"| {r['row']} | {cell(r['word'])} | {cell(r['meaning'])}{' (unsure)' if r['doubt'] else ''}"
                       f" | {cell(shown_to(r, judge))} |\n" for r in rows if r["row"])
        (out / "packs" / f"meanings_judge{judge}.md").write_text(
            JUDGE.format(answers=f"data/sources/expert/answers/meanings_judge{judge}.jsonl") + body, encoding="utf-8")
    (out / "meanings_rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                                             encoding="utf-8")
    print(len(found), "lines from the readers;", len(rows), "different;", sum(bool(r["row"]) for r in rows),
          "judged; decoys for the first judge", sum(r["decoy"] == 1 for r in rows), "and for the second",
          sum(r["decoy"] == 2 for r in rows), ";", dict(collections.Counter(r["our map"] for r in rows)))


def verdict_of(r, one, two):
    """Why a line belongs on the list of what our map lacks, or "" when it does not. one and two hold each judge's
    verdicts on our real readings only (a row decoyed for a judge is not in that judge's). On the list: a word
    for which our map has no accepted meaning; a word it translates where every judge who saw our reading says it
    is not the expert's, or one of two says so; and a translated word no judge gave a verdict on (so that it is
    not lost)."""
    if r["our map"] != "translated":
        return "our map has no accepted meaning for the word"
    seen = [a[r["row"]]["verdict"] for a in (one, two) if r["row"] in a]
    said = [v for v in seen if v in OTHERWISE]
    if not seen:
        return "not judged: no verdict from either judge"
    if len(said) == 2:
        return "our map reads the word otherwise (both judges)"
    if said and len(seen) == 1 and r.get("decoy"):
        return "our map reads the word otherwise (the one judge who saw our reading)"
    if said and len(seen) == 1:
        return "our map may read the word otherwise (one judge; the other gave no verdict)"
    if said:
        return "our map may read the word otherwise (one judge of two)"
    return ""


def count(folder=FOLDER):
    rows = [json.loads(l) for l in (folder / "meanings_rows.jsonl").open(encoding="utf-8")]
    ids = {r["row"] for r in rows if r["row"]}
    decoy_of = {r["row"]: r["decoy"] for r in rows if r["row"]}
    lines_ = sorted(rows, key=lambda r: r["line"])
    problems, real_answers, decoy_answers = {}, [], []
    for judge, name in enumerate(("meanings_judge1", "meanings_judge2"), 1):
        path = folder / "answers" / f"{name}.jsonl"
        got, bad = T.load_answers(path, ids) if path.exists() else ({}, ["no such file"])
        for row in [k for k, a in got.items() if a["verdict"] not in ASKED]:
            bad.append(f"{row}: verdict {got.pop(row)['verdict']!r} is not one the judges were given")
        real_answers.append({k: a for k, a in got.items() if decoy_of[k] != judge})
        decoy_answers.append({k: a for k, a in got.items() if decoy_of[k] == judge})
        problems[name] = bad
    one, two = real_answers
    for name, bad in problems.items():
        print(f"{name}: {len(bad)} problems" + ("" if not bad else ": " + "; ".join(bad[:6])))
    real = [r for r in lines_ if r["row"]]
    done = [r for r in real if r["our map"] == "translated"]
    rest = [r for r in real if r["our map"] != "translated"]
    seen_by = lambda rs, judge: [r for r in rs if r["decoy"] != judge]
    figs = {"lines": len(lines_), "judged": len(real),
            "decoys": {"first judge": sum(r["decoy"] == 1 for r in real),
                       "second judge": sum(r["decoy"] == 2 for r in real)},
            "problems": problems, "our map": dict(collections.Counter(r["our map"] for r in lines_)),
            "translated, first judge": T.count(seen_by(done, 1), one),
            "translated, second judge": T.count(seen_by(done, 2), two),
            "held without an accepted meaning, first judge": T.count(seen_by(rest, 1), one),
            "held without an accepted meaning, second judge": T.count(seen_by(rest, 2), two),
            "decoys, first judge": T.count([r for r in real if r["decoy"] == 1], decoy_answers[0]),
            "decoys, second judge": T.count([r for r in real if r["decoy"] == 2], decoy_answers[1]),
            "two judges, translated": T.two_judges([r for r in done if not r["decoy"]], one, two),
            "two judges, all": T.two_judges([r for r in real if not r["decoy"]], one, two)}
    said = lambda r, judge, answers: "(saw a decoy)" if r["decoy"] == judge else answers.get(r["row"], {}).get("verdict", "")
    out, lacking = [], []
    for r in lines_:
        line = {"line": r["line"], "source": r["source"], "entries": ", ".join(r["entries"]), "word": r["word"],
                "the expert's meaning": r["meaning"], "expert unsure": "yes" if r["doubt"] else "",
                "our map": r["our map"], "our reading": r["ours"], "first judge": said(r, 1, one),
                "second judge": said(r, 2, two), "found by": r["from"]}
        out.append(line)
        why = verdict_of(r, one, two)
        if why:
            lacking.append({**line, "why": why})
    figs["lacking"] = dict(collections.Counter(l["why"] for l in lacking))
    figs["lacking, stated as sure"] = dict(collections.Counter(l["why"] for l in lacking if not l["expert unsure"]))
    T.write_tsv(folder / "meanings_checked.tsv", out)
    T.write_tsv(folder / "meanings_decoys.tsv", [
        {"row": r["row"], "line": r["line"], "word": r["word"], "the expert's meaning": r["meaning"],
         "our real reading": r["ours"], "the decoy shown": r["decoy_reading"],
         "shown to": "the first judge" if r["decoy"] == 1 else "the second judge",
         "verdict": decoy_answers[r["decoy"] - 1].get(r["row"], {}).get("verdict", "")}
        for r in real if r["decoy"]])
    T.write_tsv(folder / "lacking.tsv", lacking)
    (folder / "meanings_figures.json").write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n",
                                                  encoding="utf-8")
    print(f"{figs['lines']} lines, {figs['judged']} judged, decoys {figs['decoys']}; our map: {figs['our map']}")
    for name in ("translated, first judge", "translated, second judge",
                 "held without an accepted meaning, first judge", "held without an accepted meaning, second judge",
                 "decoys, first judge", "decoys, second judge"):
        T.show(name[:28], figs[name])
    for name in ("two judges, translated", "two judges, all"):
        x = figs[name]
        print(f"  {name:28} rows {x['rows']:4}  same verdict {x['same_verdict']} (kappa {x['kappa']})")
    print("on the list of what our map lacks:", len(lacking), figs["lacking"])
    print("of them stated as sure by the expert:", figs["lacking, stated as sure"])


def main(argv):
    commands = {"reader": reader, "table": table, "count": count}
    if len(argv) != 2 or argv[1] not in commands:
        raise SystemExit(__doc__)
    commands[argv[1]]()


if __name__ == "__main__":
    main(sys.argv)
