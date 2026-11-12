"""The doubtful matches of corpus_v6, packed for two readers who see both texts, and their answers merged.

  python3 -I src/v6/packs.py write      the pack (data/sources/v6/readers/pack.md) and its key
  python3 -I src/v6/packs.py merge      the two readers' answers: the trust figures (bar C) and verdicts.jsonl

Local only: the pack quotes Otten's lines, the Newsletter and the two editions. A pack holds every line that
src/v6/build.py leaves pending, each with its best candidates in full, and mixed in, unmarked, 24 lines whose
text is known (the pairs of src/experts/prepare.py HELD): 12 with the right text among the candidates and 12
with it taken out. Both readers get the same pack and write to a file of their own; neither sees the other's.

A match is confirmed when both readers name the same candidate; when both say that none fits, the line matches
nothing; when they differ, it stays not identified. A reader who names the right text for fewer than 10 of the
12 known lines, or fails to answer "none" for fewer than 10 of the 12 with the text taken out, is not used
(bar C), and then nothing is confirmed. `write` refuses to write the pack again once a reader has answered.
"""
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(Path(__file__).resolve().parent)]
import build as B      # noqa: E402
import prepare as P    # noqa: E402
import readings as R   # noqa: E402

OUT = ROOT / "data/sources/v6/readers"
SEED = 22
KNOWN, DECOYS, PASS = 12, 12, 10
LETTERS = "ABC"

BRIEF = """# Is this line a text we already hold?

Each item below shows a **line**: a Meroitic text, or a part of one, as N. B. Millet quoted it in his 1968
thesis (typed by a later hand). Under it stand up to three **candidates**: Meroitic inscriptions from other
editions. For each item, say whether the line is the same inscription as one of the candidates.

- The same inscription means the same stone and the same text, read by another scholar. Expect differences: a
  sign read otherwise, a lost stretch restored or left out, words divided otherwise, one edition longer than the
  other because the stone is broken or because only a part is quoted.
- Two inscriptions that only share their formulae (the invocation of Isis and Osiris, "born of", "begotten of",
  the closing benedictions, a list of titles) are **not** the same. Look at what is the text's own: the names of
  the dead and of the parents, the order of the titles and relatives, anything unusual.
- A stela and an offering table of one person can carry nearly the same text and are two inscriptions; if two
  candidates fit equally well and nothing tells them apart, answer `none` and say so in the note.
- Spelling: S is the sign s, s is the sign se, N is the sign ne, X is ẖ and x is ḫ; o is Millet's ê. Dots are
  lost signs. Some candidates are printed as an edition's raw lines: there `s` may be the sign s, `se` the sign
  se, `h` or `x` either h-sign, `ñ` or `fi` the sign ne, and stray single letters or dots between the lines
  belong to the line above. Compare the letters, not the conventions.

Write your answers to the file `{answers}` as JSON lines, one line per item, in the order of the items,
nothing else in the file:

    {{"item": "I07", "same_as": "B", "part": false, "sure": 4, "note": "same names of the dead and both parents"}}

- `same_as`: "A", "B" or "C" for the candidate that is the same inscription, or "none".
- `part`: true when the line gives only a part of that inscription (a phrase or a few lines quoted from it),
  false when it gives the text as a whole (even with gaps). Leave it false with "none".
- `sure`: 1 to 5.
- `note`: at most fifteen words on what decided it.

Read only this file. Do not open other files, do not search the web. Every item must appear exactly once. When
the file is written, reply with one line: how many items you answered.

"""


def raw_text(r):
    """What a reader sees of a reading: its typed text, or the edition's own lines of transliteration."""
    if r["text"] is not None:
        return r["text"]
    if r["family"] == "millet2005":
        name = r["key"].split(":", 1)[1]
        out = []
        for n, block in P.millet_entries():
            if n != name:
                continue
            cut = re.search(r"^(COMMENTARY|RENDERING|NOTES)", block, re.M)
            body = block[:cut.start()] if cut else block
            first = re.search(r"^\d{1,2}:\s", body, re.M)
            if first:
                out.append(body[first.start():])
        return P.clean("\n".join(out)).strip()
    number = r["key"].split(":", 1)[1]
    block = dict(P.fhn_entries())[number]
    m = re.search(r"^Text\s*$(.*?)^Comments\s*$", block, re.M | re.S)
    return P.clean(m.group(1)).strip() if m else ""


def nearest(x, b, taken, n):
    """The n readings that share most runs of five letters with x, formulae counted, one per inscription and none
    of the inscriptions in `taken`: what fills an item up to three candidates, so that every item looks alike."""
    mine = R.runs(x["letters"])
    pool = sorted((r for r in b["editions"] if r["letters"] and not r.get("reconstruction")),
                  key=lambda r: (-len(R.runs(r["letters"]) & mine), r["key"]))
    out, seen = [], set(taken)
    for r in pool:
        g = b["group_of"](r["key"])
        if g not in seen:
            seen.add(g)
            out.append(r["key"])
        if len(out) == n:
            break
    return out


def items(b):
    """(the items of the pack, its key). An item: {"item", "line", "candidates": [three reading keys]}; the key
    says for each item what kind it is (pending, known, decoy) and which candidate is the right one. Every item
    has three candidates: the rule's own, filled up with the nearest other texts."""
    rnd = random.Random(SEED)
    skip = R.formulae(b["editions"])
    by_key, group_of = b["by_key"], b["group_of"]
    fill = lambda line, keys: (keys + nearest(by_key[line], b, {group_of(k) for k in keys}, 3 - len(keys)))[:3]
    out = []
    for row in B.pending_rows(b):
        out.append({"line": row["line"], "kind": "pending", "right": None,
                    "candidates": fill(row["line"], [c["reading"] for c in row["candidates"]])})
    held = sorted((k, d[2][4], d[1]) for k, d in b["decided"].items()
                  if d[3] == B.HELD_BY and k.startswith("otten:") and d[2])
    rnd.shuffle(held)
    for n, (line, right, group) in enumerate(held[:KNOWN + DECOYS]):
        cands = B.candidates(by_key[line], b["editions"], group_of, skip) or \
            B.candidates(by_key[line], b["editions"], group_of, skip, floor=B.LOOSE)
        others = [c[4] for c in cands if c[5] != group]
        if n < KNOWN:
            out.append({"line": line, "kind": "known", "right": right,
                        "candidates": ([right] + others)[:1] + nearest(by_key[line], b, {group}, 2)})
        else:
            out.append({"line": line, "kind": "decoy", "right": None, "candidates": nearest(by_key[line], b, {group}, 3)})
    rnd.shuffle(out)
    key = {}
    for n, it in enumerate(out, 1):
        it["item"] = f"I{n:02d}"
        rnd.shuffle(it["candidates"])
        key[it["item"]] = {"line": it["line"], "kind": it["kind"],
                           "candidates": dict(zip(LETTERS, it["candidates"])),
                           "right": next((l for l, k in zip(LETTERS, it["candidates"]) if k == it["right"]), "none")
                           if it["kind"] != "pending" else None}
    return out, key


def pack(b, its, reader):
    parts = [BRIEF.format(answers=f"data/sources/v6/readers/answers/reader{reader}.jsonl")]
    for it in its:
        parts.append(f"\n---\n\n## {it['item']}\n\n**The line**\n\n```\n{b['by_key'][it['line']]['text']}\n```\n")
        for letter, k in zip(LETTERS, it["candidates"]):
            parts.append(f"\n**Candidate {letter}**\n\n```\n{raw_text(b['by_key'][k])}\n```\n")
    return "".join(parts)


def write(out=OUT):
    if any((out / "answers").glob("reader*.jsonl")):
        raise SystemExit(f"{out}/answers holds a reader's answers: not writing the pack again")
    b = B.build(verdicts={})
    its, key = items(b)
    (out / "answers").mkdir(parents=True, exist_ok=True)
    for reader in (1, 2):
        (out / f"pack_reader{reader}.md").write_text(pack(b, its, reader), encoding="utf-8")
    (out / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1) + "\n")
    kinds = [v["kind"] for v in key.values()]
    print(f"items {len(its)}: pending {kinds.count('pending')}, known {kinds.count('known')}, decoys {kinds.count('decoy')}; "
          f"pack {(out / 'pack_reader1.md').stat().st_size} bytes")


def load_answers(path, key):
    """({item: answer}, [problems]) of one reader's file: only item, same_as, part and sure are read."""
    out, problems = {}, []
    if not path.exists():
        return out, [f"no file {path.name}"]
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            a = json.loads(line)
            item, same = a["item"], a["same_as"]
        except (ValueError, KeyError, TypeError):
            problems.append(f"line {n}: not an answer")
            continue
        if item not in key or item in out or same not in tuple(key[item]["candidates"]) + ("none",):
            problems.append(f"line {n}: unknown item, a second answer, or a candidate the item does not have")
            continue
        out[item] = {"same_as": same, "part": a.get("part") is True}
    problems += [f"no answer for {i}" for i in sorted(set(key) - set(out))]
    return out, problems


def trust(answers, key):
    """Bar C for one reader: (right of the known lines, "none" of the decoys, passes)."""
    known = [i for i, k in key.items() if k["kind"] == "known"]
    decoys = [i for i, k in key.items() if k["kind"] == "decoy"]
    right = sum(answers.get(i, {}).get("same_as") == key[i]["right"] for i in known)
    none = sum(answers.get(i, {}).get("same_as") == "none" for i in decoys)
    return {"known": len(known), "right": right, "decoys": len(decoys), "none": none,
            "passes": right >= min(PASS, len(known)) and none >= min(PASS, len(decoys))}


def verdicts(one, two, key):
    """[{line, same_as, part}] for the pending lines that both readers settled alike: same_as is the reading key
    both named, or "" when both said none. A line named a part by either reader is a part."""
    out = []
    for item, k in key.items():
        if k["kind"] != "pending" or item not in one or item not in two:
            continue
        a, b = one[item], two[item]
        if a["same_as"] != b["same_as"]:
            continue
        same = "" if a["same_as"] == "none" else k["candidates"][a["same_as"]]
        out.append({"line": k["line"], "same_as": same, "part": bool(same) and (a["part"] or b["part"])})
    return out


def merge(out=OUT):
    key = json.loads((out / "key.json").read_text())
    readers, figures = [], {}
    for n in (1, 2):
        answers, problems = load_answers(out / "answers" / f"reader{n}.jsonl", key)
        readers.append(answers)
        figures[f"reader{n}"] = dict(trust(answers, key), problems=len(problems))
    pending = [i for i, k in key.items() if k["kind"] == "pending"]
    both = [i for i in pending if i in readers[0] and i in readers[1]]
    figures["pending"] = len(pending)
    figures["same_answer"] = sum(readers[0][i]["same_as"] == readers[1][i]["same_as"] for i in both)
    used = figures["reader1"]["passes"] and figures["reader2"]["passes"]
    settled = verdicts(readers[0], readers[1], key) if used else []
    figures["confirmed"] = sum(bool(v["same_as"]) for v in settled)
    figures["none"] = sum(not v["same_as"] for v in settled)
    figures["used"] = used
    (out / "verdicts.jsonl").write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in settled))
    (out / "figures.json").write_text(json.dumps(figures, indent=1) + "\n")
    print(json.dumps(figures, indent=1))


def main(argv):
    if argv[1:] == ["write"]:
        return write()
    if argv[1:] == ["merge"]:
        return merge()
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
