"""The public figures and the public word list of the check against two printed editions.

  python3 -I src/experts/publish.py

Reads the local results in data/sources/expert/ (rows.jsonl, the first run's answers, figures.json of tally.py,
missing_grouped.tsv of missing.py, the readers' lists and meanings_figures.json of close.py) and writes two public
files. They hold counts and word forms only: no reading
of ours and no meaning of the experts'.

  data/discovery/experts_figures.json   every number the page data/discovery/experts.md gives
  data/discovery/experts_words.tsv      each word of the 31 texts with our level and the first judge's verdicts

The judges' files are untrusted data: they are read through tally.load_answers only.
"""
import collections
import csv
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import close as K                                      # noqa: E402
import tally as T                                      # noqa: E402

FOLDER = T.FOLDER
PUBLIC = T.ROOT / "data/discovery"
MASKED = ("NAME", "RNAME")
NOT_AGREED = ("partly", "differ", "new")
GROUPS = ("yetmde", "qo", "other")
DIFFERENCES = ("the numeral 1 typed as the letter l", "a name or a piece of a word read as a word",
               "our map has only the kind of word", "another meaning or identification")


def first_judge(rows, folder=FOLDER):
    """The first judge's answers on all packs, {row id: answer}."""
    out = {}
    for pack in sorted({r["pack"] for r in rows}):
        got, _ = T.load_answers(folder / "answers" / f"judge1_{pack}.jsonl", {r["row"] for r in rows if r["pack"] == pack})
        out.update(got)
    return out


def group_of(ours):
    """Which of the two words of a known difference of school a reading of ours belongs to, by its wording:
    "yetmde" (our "nephew, niece", and the halves of yetmdelowi written apart), "qo" (our "this one", "this one
    is", and a name with -qowi, "this is X"), else "other"."""
    o = ours.lower()
    if "nephew" in o or "(part of yetmdelowi)" in o:
        return "yetmde"
    if re.search(r"\bthis one\b|variant of qo|^this is ", o):
        return "qo"
    return "other"


def difference_of(r, a):
    """The kind of a non-agreement outside the two words, from the row and the judge's note of the expert's
    meaning: the numeral 1 where our copy has the letter l; a word for which our map names only the kind (the
    judge's verdict "new"); a name or a piece of another word that our map reads as a word; anything else."""
    e = a["expert"].lower()
    if r["form"] == "l" and "numeral" in e:
        return DIFFERENCES[0]
    if a["verdict"] == "new":
        return DIFFERENCES[2]
    if re.search(r"\bnames?\b|part of|end of|ending of|initial of", e):
        return DIFFERENCES[1]
    return DIFFERENCES[3]


def breakdown(rows, one):
    """({group: counts of the translated words in it}, {kind of difference: words}) for the first judge, decoys
    left out."""
    done = [r for r in rows if not r["decoy"] and r["level"] in T.TRANSLATED]
    groups = {g: T.count([r for r in done if group_of(r["ours"]) == g], one) for g in GROUPS}
    kinds = collections.Counter(difference_of(r, one[r["row"]]) for r in done
                                if group_of(r["ours"]) == "other" and one.get(r["row"], {}).get("verdict") in NOT_AGREED)
    return groups, {k: kinds[k] for k in DIFFERENCES}


def words(rows, one):
    """One line per word form and level: how often it stands in the 31 texts and what the first judge said of
    our reading of it. A place where the judge saw a decoy is counted apart."""
    out = collections.defaultdict(collections.Counter)
    for r in rows:
        key = (r["form"], r["level"])
        out[key]["places"] += 1
        out[key]["a decoy was shown" if r["decoy"] else one.get(r["row"], {}).get("verdict", "no answer")] += 1
    cols = ("places",) + T.VERDICTS + ("a decoy was shown", "no answer")
    return [{"word": form, "level": level, **{c: n[c] for c in cols}} for (form, level), n in sorted(out.items())]


def new_words(folder=FOLDER):
    """The words of the held texts that our map leaves without a meaning and to which a judge found the edition
    giving one (verdict "new" in missing_grouped.tsv): how many, of which kind, and how many of the words the
    edition marks as unsure."""
    rows = [r for r in csv.DictReader((folder / "missing_grouped.tsv").open(encoding="utf-8"), delimiter="\t")
            if "new" in r["verdicts"]]
    kinds = collections.Counter(r["kind"] for r in rows)
    return {"all": len(rows), **dict(sorted(kinds.items())),
            "a word, marked as unsure": sum(1 for r in rows if r["kind"] == "a word" and r["expert unsure"])}


def public_figures(folder=FOLDER):
    """Every number of the page, from the local files."""
    every = [json.loads(l) for l in (folder / "rows.jsonl").open(encoding="utf-8")]
    rows = [r for r in every if r["row"]]
    one = first_judge(rows, folder)
    first = json.loads((folder / "figures.json").read_text(encoding="utf-8"))
    second = json.loads((folder / "meanings_figures.json").read_text(encoding="utf-8"))
    groups, kinds = breakdown(rows, one)
    texts = {(r["source"], r["entry"]) for r in rows}
    return {
        "texts": {"held by both": len(texts), **{label: sum(1 for s, _ in texts if s == source)
                                                 for source, label in T.SOURCES.items()}},
        "words": {"in the texts": len(every), "judged": len(rows),
                  "masked names, not judged": sum(1 for r in every if not r["row"] and r["form"] in MASKED),
                  "lost, not judged": sum(1 for r in every if not r["row"] and r["form"] not in MASKED),
                  "decoys": sum(r["decoy"] for r in rows),
                  **{f"judged, {label}": sum(1 for r in rows if r["source"] == source)
                     for source, label in T.SOURCES.items()}},
        "translated": first["translated"], "not translated": first["not_translated"],
        "groups": groups, "other differences": kinds,
        "decoys": first["decoys_by_judge"], "two judges": first["two_judges"],
        "new in the held texts": new_words(folder),
        "meanings": {"lines from the readers": sum(len(K.answers_of(name, folder)) for name in K.READERS),
                     **{k: v for k, v in second.items() if k != "problems"}},
    }


def main():
    figs = public_figures()
    (PUBLIC / "experts_figures.json").write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    every = [json.loads(l) for l in (FOLDER / "rows.jsonl").open(encoding="utf-8")]
    rows = [r for r in every if r["row"]]
    table = words(rows, first_judge(rows))
    T.write_tsv(PUBLIC / "experts_words.tsv", table)
    t = figs["translated"]["all"]
    print(f"{figs['texts']['held by both']} texts, {figs['words']['judged']} words judged; translated {t['rows']}, "
          f"with a meaning from the expert {t['given']}, agree {t['agree']} ({t['agree_share']:.1%})")
    for g in GROUPS:
        c = figs["groups"][g]
        print(f"  {g:7} words {c['rows']:4}  with a meaning {c['given']:4}  agree {c['agree']:4}  partly {c['partly']:3}  "
              f"differ {c['differ']:3}  new {c['new']:3}")
    print("  other differences:", figs["other differences"])
    print(len(table), "lines in experts_words.tsv")


if __name__ == "__main__":
    main()
