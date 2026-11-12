"""The public side of corpus_v6: the table of inscriptions without in-copyright text, the map of the corpus_v5
ids, the figures, and the tables of the page.

  python3 -I src/v6/public.py          writes data/inscriptions.jsonl, data/inscriptions_map.tsv,
                                        data/discovery/corpus_v6_figures.json and the tables between the
                                        markers of data/discovery/corpus_v6.md

Local only (it reads data/sources/v6/, which src/v6/build.py, readings.py and recount.py write). A public row
holds a text only when its reading is open: a row of the Griffith or Karanog transcriptions (public domain,
CC BY 4.0). For every other reading it holds the edition, the place in it, the licence and counts.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(Path(__file__).resolve().parent)]
import readings as R   # noqa: E402

LOCAL = ROOT / "data/sources/v6"
TABLE = ROOT / "data/inscriptions.jsonl"
MAP = ROOT / "data/inscriptions_map.tsv"
FIGURES = ROOT / "data/discovery/corpus_v6_figures.json"
PAGE = ROOT / "data/discovery/corpus_v6.md"
BEGIN, END = "<!-- tables: written by src/v6/public.py -->", "<!-- end of the tables -->"
MAP_COLUMNS = ("corpus_v5 id", "words", "what it is", "copy", "inscription", "reading", "page of Millet 1968",
               "share of the text's own runs in the other", "share of the other's own runs in the text", "own runs shared",
               "share of the text's runs in the other (all runs, as src/experts/prepare.py)",
               "share of the other's runs in the text (all runs, as src/experts/prepare.py)", "compared with",
               "settled by")


def rows(name):
    return [json.loads(l) for l in (LOCAL / name).read_text().splitlines() if l.strip()]


def public_reading(r):
    out = {k: r[k] for k in ("key", "work", "ref", "number", "licence", "open", "typed", "whole", "letters", "words")}
    if r["open"]:
        out.update(site=r["site"], object=r["object"], text=r["text"])
    return out


def public_row(i, in_corpus):
    """An inscription as the public table holds it: no text but an open one."""
    best = next((r for r in i["readings"] if r["key"] == i["preferred"]), None)
    return {"id": i["id"], "rem": i["rem"], "numbers": i["numbers"], "site": i["site"], "kind": i["kind"],
            "kind_by": i["kind_by"], "in_corpus_v6": i["id"] in in_corpus, "v5": in_corpus.get(i["id"], []),
            "preferred": i["preferred"], "parts": i["parts"],
            "preferred_is_open": bool(best and best["open"]),
            "words": len(i["text"].split()) if i["text"] else 0, "names_marked": len(i["names"]),
            "numerals_set": len(i["numerals_set"]),
            "text": i["text"] if best and best["open"] and not i["parts"] else None,
            "open_reading": i["open"], "open_text": i["open_text"], "open_whole": i["open_whole"],
            "readings": [public_reading(r) for r in i["readings"]]}


def map_table(mapped):
    cell = lambda v: "" if v is None else str(v)
    lines = ["\t".join(MAP_COLUMNS)]
    for m in mapped:
        lines.append("\t".join(cell(v) for v in (
            m["id"], m["words"], m.get("what"), m.get("copy"), m.get("inscription"), m.get("reading"), m.get("page"),
            m.get("share_of_text"), m.get("share_of_other"), m.get("shared_runs"), m.get("share_of_text_all"),
            m.get("share_of_other_all"), m.get("against"), m.get("by"))))
    return "\n".join(lines) + "\n"


def alike(letters, systems, skip):
    """(the pairs of rows that the rule matches surely and that share a way of numbering, so that they carry two
    different numbers of it; the pairs that share no way of numbering and that the rule matches at all, with the
    verdict). letters: [(id, letters)] of the rows; systems: {id: the numberings its numbers are in}."""
    same, across = [], []
    for n, (a, x) in enumerate(letters):
        for b, y in letters[n + 1:]:
            v = R.rule(x, y, skip)[0]
            if v == "sure" and systems[a] & systems[b]:
                same.append((a, b))
            elif v and not systems[a] & systems[b]:
                across.append((a, b, v))
    return same, across


def pct(a, b):
    return f"{a / b:.1%}" if b else "n/a"


def tables(f):
    """The tables of the page, from the figures."""
    i, v5, v6, bar, cov, exp = f["inscriptions"], f["corpus_v5"], f["corpus_v6"], f["bars"], f["coverage"], f["experts"]
    n = i["all"]
    o, held, most, tw = f["otten"], f["held"]["edition_readings"], f["otten"]["most_copied"], f["twins"]
    mi = o["most_copied_inscription"]
    cls = v5["classes"]
    wait = cls.get("not settled by two readers", {"texts": 0, "words": 0})
    rd = f.get("readers")
    if rd:
        read = (f"- Doubtful matches read by two readers: {rd['pending']} lines. Both gave the same answer for "
                f"{rd['same_answer']} and differ on {rd['differ']}. Both named the same candidate for "
                f"{rd['same_candidate_as_the_bar_was_written']}: {rd['confirmed']} are used, {rd['confirmed_whole_text']} as "
                f"the whole text and {rd['confirmed_part']} as a part of it, and {rd['same_answer_but_unsure']} is not, "
                f"because both marked it as a guess. Both answered \"none\" for {rd['none']}. Not settled: "
                f"{rd['not_settled']} lines, behind {wait['texts']} texts and {wait['words']:,} words of `corpus_v5`.")
        st = f["settled"]
        read += (f"\n- The lines the readers settled, as they stand in the build: {st['readings']} are readings of an "
                 f"inscription, {st['phrases']} are example phrases from one, {st['set_aside']} is set aside, and "
                 f"{st['none']} matches nothing and is an inscription of its own.")
    else:
        read = (f"- Doubtful matches waiting for two readers: {f['pending']} lines, behind {wait['texts']} texts and "
                f"{wait['words']:,} words of `corpus_v5`.")
    num, ph = f["numerals"], f["phrases"]
    source_names = {"mnl": "the Meroitic Newsletter", "griffith": "Griffith's printed type (rows that `corpus_v5` left out)",
                    "karanog": "Griffith's Karanòg copies", "otten": "Millet 1968 as Otten typed it",
                    "otten:narrative": "Otten's narrative files"}
    out = [BEGIN, "", "### The counts the text uses", "",
           f"- Otten's padded file: {o['padded_lines']:,} lines, {o['raw_lines']:,} of them different. Equal to a line of his "
           f"per-scholar files: {o['equal']:,}. Such a line with one stretch swapped: {o['one_stretch_swapped']:,}. Near "
           f"one, with a second small difference: {o['near']:,}. From no such line: {o['from_no_source_line']} (the three "
           f"narratives, which have files of their own).",
           f"- Source lines in the per-scholar files: {o['source_lines']:,}. The {o['texts_traced']} texts of the older "
           f"corpus come from {o['source_lines_behind_them']} of them.",
           f"- The most copied line: {most['line']} ({most['inscription']}), {most['texts']} texts and {most['words']:,} "
           f"words of `corpus_v5`. The most copied inscription: {mi['inscription']}, {mi['texts']} texts and "
           f"{mi['words']:,} words, from {mi['lines']} source lines.",
           f"- Readings held besides Otten's lines: {held['griffith']} rows of Griffith's print, {held['karanog']} Karanòg "
           f"rows, {held['mnl']} Newsletter rows, {held['millet2005']} texts of Millet 2005, {held['fhn']} entries of "
           f"FHN III, {f['held']['narratives']} narrative files; and {f['held']['witnesses']} texts that FHN III prints "
           f"under one number (no. {', '.join(f['held']['witness_entries'])}), each set beside the inscription of its "
           f"REM number after the matching.",
           f"- Source lines by what they are: {f['lines'].get('reading', 0)} readings of an inscription, "
           f"{f['lines'].get('phrase', 0)} example phrases, {f['lines'].get('word list', 0)} word-list entries, "
           f"{f['lines'].get('unidentified', 0)} inscriptions not identified, {f['lines'].get('pending', 0)} with a doubtful "
           f"match that is not settled.",
           f"- The example phrases: {ph['in_one_text']} are a part of one held text or stand whole in it, "
           f"{ph['in_several']} stand whole in several, {ph['doubtful']} have a doubtful match that was not read, "
           f"{ph['set_aside']} was taken by the readers for a text of one inscription and is set aside because the rule "
           f"matches it surely with another, and {ph['nothing']} match nothing held.",
           read,
           f"- A lone `l` read as a numeral: {num['all']} ({num['by_another_edition']} by another edition, "
           f"{num['by_analogy']} by analogy), in {num['inscriptions']} inscription(s): "
           + ", ".join(f"{k} ({c})" for k, c in num["by_inscription"].items()) + ".",
           f"- Words marked as a personal name by Otten's own tags: {v6['name_words_marked']}.",
           f"- Inscriptions whose text is in two or more parts: {i['in_two_or_more_parts']}.",
           f"- Pairs of rows of `corpus_v6` that the rule takes for a sure match and that carry two different numbers of "
           f"one numbering: {tw['pairs']} (in {tw['rows']} rows). Pairs of rows numbered in two different ways (a REM "
           f"number and a number of Griffith's, Millet's or the Newsletter's, or none) that the rule matches at all: "
           f"{tw['across_numberings']['pairs']}, of them surely {tw['across_numberings']['sure']}"
           + (": " + "; ".join(f"{a} and {b}" for a, b in tw['across_numberings']['list']) if tw['across_numberings']['pairs'] else "") + ".",
           "", "### The measures", "", "| Measure | Count | Share of the inscriptions |", "|---|---|---|",
           f"| Inscriptions | {n} | |",
           f"| with a REM number | {i['with_a_rem_number']} | {pct(i['with_a_rem_number'], n)} |",
           f"| with a typed reading (the rows of `corpus_v6`) | {i['with_a_typed_reading']} | {pct(i['with_a_typed_reading'], n)} |",
           f"| with real names in the preferred reading | {i['with_real_names']} | {pct(i['with_real_names'], n)} |",
           f"| with two readings or more, from two editions or more | {i['with_readings_from_two_editions_or_more']} | {pct(i['with_readings_from_two_editions_or_more'], n)} |",
           f"| with a reading under an open licence | {i['with_an_open_reading']} | {pct(i['with_an_open_reading'], n)} |",
           f"| with an open reading of the whole text | {i['with_an_open_reading_of_the_whole_text']} | {pct(i['with_an_open_reading_of_the_whole_text'], n)} |",
           f"| whose preferred reading is the open one | {i['preferred_reading_is_open']} | {pct(i['preferred_reading_is_open'], n)} |",
           f"| held only as a text layer of Millet 2005 (not typed) | {i['only_a_text_layer']} | {pct(i['only_a_text_layer'], n)} |",
           f"| typed, without a legible word | {i['typed_without_a_legible_word']} | {pct(i['typed_without_a_legible_word'], n)} |",
           f"| quoted by Millet 1968 and not identified | {i['not_identified']} | {pct(i['not_identified'], n)} |",
           "", "New to the corpus (rows of `corpus_v6` that no text of `corpus_v5` is a reading of): "
           + ", ".join(f"{c} from {source_names[k]}" for k, c in i["new_to_the_corpus_by_source"].items()) + ".",
           "", "### What the texts of `corpus_v5` turned out to be", "",
           "| What | Texts | Words | Share of the words |", "|---|---|---|---|"]
    for name, c in v5["classes"].items():
        out.append(f"| {name[0].upper() + name[1:]} | {c['texts']} | {c['words']:,} | {pct(c['words'], v5['words'])} |")
    out += [f"| All of `corpus_v5` | {v5['texts']} | {v5['words']:,} | |", "",
            "### The kinds of text", "", "| Kind | Inscriptions |", "|---|---|"]
    out += [f"| {k[0].upper() + k[1:]} | {c} |" for k, c in i["by_kind"].items()]
    out += ["", f"Of the {i['by_kind'].get('not known', 0)} of a kind not known, {i['kind_not_known_and_only_in_the_printout']} are held "
                f"only in the Newsletter's printout of 1971, which states no object for them."]
    out += ["", "### The preferred reading, by source", "", "| Source | Inscriptions |", "|---|---|"]
    names = {"mnl": "The Meroitic Newsletter (typed by the model, in copyright)",
             "karanog": "Griffith's Karanòg hand copies, checked against his type (open)",
             "griffith": "Griffith's printed type (open)",
             "otten": "Millet 1968 as Otten typed it, with real names",
             "otten:narrative": "Otten's three narrative files"}
    out += [f"| {names[k]} | {c} |" for k, c in i["preferred_by_source"].items()]
    a, w = bar["as_written"], bar["with_the_floor"]
    k = bar["karanog"]
    out += ["", "### The rule on the pairs already known", "",
            "| | As the bar was written | With the floor of six shared runs |", "|---|---|---|",
            f"| Known pairs | {bar['pairs']} | {bar['pairs']} |",
            f"| The partner is the best match, sure or doubtful | {a['right']} ({pct(a['right'], bar['pairs'])}) | {w['right']} ({pct(w['right'], bar['pairs'])}) |",
            f"| of them sure | {a['sure']} | {w['sure']} |",
            f"| of them doubtful | {a['doubtful']} | {w['doubtful']} |",
            f"| Counting another line of the same text as right | {a['right_or_another_line_of_the_same_text']} ({pct(a['right_or_another_line_of_the_same_text'], bar['pairs'])}) | {w['right_or_another_line_of_the_same_text']} ({pct(w['right_or_another_line_of_the_same_text'], bar['pairs'])}) |",
            f"| Pairs with a sure match to another text | {a['with_a_sure_other']} | {w['with_a_sure_other']} |",
            f"| Missed | {bar['pairs'] - a['right']} | {bar['pairs'] - w['right']} |"]
    out += [f"| of them: {why} | {a['why_missed'][why]} | {w['why_missed'][why]} |" for why in a["why_missed"]]
    kind = bar["by_kind"]
    out += ["",
            f"The known pairs: {kind.get('HELD millet', 0) + kind.get('HELD fhn', 0)} read side by side for the expert check, "
            f"{kind.get('Karanog in Newsletter 28', 0) + kind.get('Newsletter 28 in FHN', 0)} of the Karanòg texts that "
            f"Newsletter 28 and FHN print, {kind.get('Newsletter row in the corpus', 0)} Newsletter rows that an earlier test "
            f"found in the corpus, {kind.get('Newsletter second edition', 0)} second editions in the Newsletter.",
            "",
            f"Bar B: {k['with_a_sure_match_to_another_number']} of the {k['texts']} Karanòg texts have a sure match to another "
            f"Karanòg number ({pct(k['with_a_sure_match_to_another_number'], k['texts'])}).",
            ""]
    if rd:
        out += ["### The two readers (bar C)", "", "| | Reader 1 | Reader 2 |", "|---|---|---|",
                f"| Known lines: the right text named | {rd['reader1']['right']} of {rd['reader1']['known']} | {rd['reader2']['right']} of {rd['reader2']['known']} |",
                f"| Lines with the text taken out: \"none\" answered | {rd['reader1']['none']} of {rd['reader1']['decoys']} | {rd['reader2']['none']} of {rd['reader2']['decoys']} |",
                f"| Passes the bar | {'yes' if rd['reader1']['passes'] else 'no'} | {'yes' if rd['reader2']['passes'] else 'no'} |",
                ""]
    out += ["### The coverage map, counted again", "",
            "| Counted on | Texts | Words | Translated | Share |", "|---|---|---|---|---|"]
    old, was, new, al = cov["corpus_v5"]["all"], cov["inscriptions_that_were_in_corpus_v5"], cov["inscriptions_new_to_the_corpus"], cov["all"]
    once = cov["corpus_v5"]["near_copies_once"]
    out += [f"| `corpus_v5`, every text (the old figure) | {old['texts']} | {old['words']:,} | {old['translated']:,} | {pct(old['translated'], old['words'])} |",
            f"| `corpus_v5`, near-copies counted once (the old figure) | {once['texts']} | {once['words']:,} | {once['translated']:,} | {pct(once['translated'], once['words'])} |",
            f"| `corpus_v6`, the inscriptions that were in `corpus_v5` | {was['texts']} | {was['words']:,} | {was['translated']:,} | {pct(was['translated'], was['words'])} |",
            f"| `corpus_v6`, the inscriptions new to the corpus | {new['texts']} | {new['words']:,} | {new['translated']:,} | {pct(new['translated'], new['words'])} |",
            f"| `corpus_v6`, all | {al['texts']} | {al['words']:,} | {al['translated']:,} | {pct(al['translated'], al['words'])} |",
            "", "| Level | `corpus_v5` | `corpus_v6`, were in `corpus_v5` | `corpus_v6`, new | `corpus_v6`, all |", "|---|---|---|---|---|"]
    for level in old["levels"]:
        out.append(f"| {level} | {old['levels'][level]:,} | {was['levels'][level]:,} | {new['levels'][level]:,} | {al['levels'][level]:,} |")
    t5, t6 = cov["corpus_v5"]["texts"], cov["texts"]
    na = cov["not_analysed"]
    out += ["",
            f"Near-copies counted once in both: texts with a legible word, {t6['legible']} of {t6['texts']} in `corpus_v6` "
            f"({t5['legible']} of {t5['texts']} in `corpus_v5`); every legible word translated in {t6['no_blocker']} "
            f"({t5['no_blocker']}); one piece missing in {t6['one_blocker']} ({t5['one_blocker']}). Words whose spelling no "
            f"analyst has seen: {na['words']:,} in {na['spellings']:,} spellings, {na['in_new_inscriptions']:,} of them in the "
            f"inscriptions new to the corpus and {na['in_inscriptions_that_were_in_corpus_v5']:,} in the others. Words that "
            f"are a name by the source's own tag: {cov['names_by_the_source']}. Words written apart that the map joins by "
            f"its own rule: {cov['corrections']['a word written apart']['words']}.",
            "", "### The check against the two editions, counted again", "",
            "| | On `corpus_v5` | On the words that still stand in `corpus_v6` |", "|---|---|---|"]
    e5, e6 = exp["corpus_v5"]["translated"], exp["corpus_v6"]["translated"]
    out += [f"| Judged rows | {exp['corpus_v5']['rows']:,} | {exp['corpus_v6']['rows']:,} |",
            f"| Words the map counts as translated | {e5['rows']} | {e6['rows']} |",
            f"| of them given a meaning by the edition | {e5['given']} | {e6['given']} |",
            f"| of them with the map's meaning | {e5['agree']} ({pct(e5['agree'], e5['given'])}) | {e6['agree']} ({pct(e6['agree'], e6['given'])}) |",
            "",
            f"Not carried over: {exp['not_carried']} of the {exp['corpus_v5']['rows']:,} judged rows ("
            + "; ".join(f"{c} because {w}" for w, c in exp["why"].items()) + ").", "", END]
    return "\n".join(out)


def main(argv):
    if argv[1:]:
        sys.exit(__doc__)
    import build as B
    import otten as O
    ins, mapped = rows("inscriptions.jsonl"), rows("map.jsonl")
    corpus = [json.loads(l) for l in (ROOT / "data/corpus_v6.jsonl").read_text().splitlines() if l.strip()]
    in_corpus = {c["id"]: c["v5"] for c in corpus}
    TABLE.write_text("".join(json.dumps(public_row(i, in_corpus), ensure_ascii=False) + "\n" for i in ins))
    MAP.write_text(map_table(mapped))
    figs = json.loads((LOCAL / "figures.json").read_text())
    editions, narratives, lines = R.load()
    v5 = [json.loads(l) for l in R.V5.read_text().splitlines() if l.strip()]
    raws = O.raw_lines()
    derived = O.derive(raws, O.source_lines())
    src = O.sources_of(O.trace(v5, raws, *O.pools()), derived)
    bars = R.bars(editions, narratives, lines, {tid: v[0][0] for tid, v in src.items() if v})
    for name in ("as_written", "with_the_floor"):
        bars[name].pop("scored")
    how = {}
    for d in derived.values():
        how[d[1]] = how.get(d[1], 0) + 1
    copied = {}
    for m in mapped:
        if m.get("reading", "").startswith("otten:") and ":narrative:" not in m["reading"]:
            c = copied.setdefault(m["reading"], {"texts": 0, "words": 0, "inscription": m.get("inscription")})
            c["texts"] += 1
            c["words"] += m["words"]
    top = max(copied, key=lambda k: (copied[k]["texts"], k))
    stood = {}                                     # the texts of corpus_v5 that are a reading of one inscription
    for m in mapped:
        if m.get("class") in ("reading", "unidentified") and m.get("inscription"):
            s = stood.setdefault(m["inscription"], {"texts": 0, "words": 0, "lines": set()})
            s["texts"] += 1
            s["words"] += m["words"]
            s["lines"].add(m["reading"])
    most = max(stood, key=lambda k: (stood[k]["texts"], k))
    skip = R.formulae(editions)
    letters = [(c["id"], R.reduced(c["text"])) for c in corpus]
    pairs, loose = alike(letters, {i["id"]: set(i["numbers"]) for i in ins}, skip)
    figs["twins"] = {"pairs": len(pairs), "rows": len({k for pair in pairs for k in pair}), "list": pairs,
                     "across_numberings": {"pairs": len(loose), "list": [[a, b] for a, b, _ in loose],
                                           "sure": sum(v == "sure" for _, _, v in loose)}}
    phrases = [l for l in rows("lines.jsonl") if l["class"] == "phrase"]
    figs["phrases"] = {"in_one_text": sum(bool(l["inscription"]) for l in phrases),
                       "in_several": sum(not l["inscription"] and "held texts" in l["by"] for l in phrases),
                       "doubtful": sum(l["by"].startswith("a doubtful match") for l in phrases),
                       "set_aside": sum(l["by"].startswith("set aside") for l in phrases),
                       "nothing": sum(not l["inscription"] and (l["by"].startswith("matches nothing held") or l["by"].startswith("no letters"))
                                      for l in phrases)}
    assert sum(figs["phrases"].values()) == len(phrases), "a phrase of a kind the page does not count"
    every = rows("lines.jsonl")
    figs["settled"] = {"readings": sum(l["class"] == "reading" and l["by"] == B.READ for l in every),
                       "phrases": sum(l["class"] == "phrase" and l["by"] == B.READ for l in every),
                       "set_aside": sum(l["by"].startswith("set aside") for l in every),
                       "none": sum(l["by"].endswith(B.READ_NONE) for l in every)}
    fixes = [(i["id"], x) for i in ins for x in i["numerals_set"]]
    figs["numerals"] = {"all": len(fixes), "by_another_edition": sum(x[3] == B.ANOTHER for _, x in fixes),
                        "by_analogy": sum(x[3] == "by analogy" for _, x in fixes),
                        "inscriptions": len({k for k, _ in fixes}), "where": sorted({k for k, _ in fixes}),
                        "by_inscription": {k: sum(i == k for i, _ in fixes) for k in sorted({k for k, _ in fixes})}}
    figs["otten"] = {"padded_lines": sum(bool(l.strip()) for l in O.PADDED.read_text().split("\n")),
                     "most_copied": dict(copied[top], line=top.split(":", 1)[1].replace(":", " line ")),
                     "most_copied_inscription": {"inscription": most, "texts": stood[most]["texts"],
                                                 "words": stood[most]["words"], "lines": len(stood[most]["lines"])},
                     "source_lines": len(lines), "raw_lines": len(raws), "equal": how.get("equal", 0),
                     "one_stretch_swapped": how.get("swap", 0), "near": how.get("near", 0),
                     "from_no_source_line": len(raws) - len(derived),
                     "texts_traced": sum(bool(v) for v in src.values()),
                     "source_lines_behind_them": len({v[0][0] for v in src.values() if v})}
    parts = R.witnesses()
    figs["held"] = {"edition_readings": {k: sum(r["family"] == k for r in editions) for k in R.LICENCES if k != "otten"},
                    "narratives": len(narratives), "witnesses": len(parts),
                    "witness_entries": sorted({r["numbers"]["fhn"][0] for r in parts})}
    figs["bars"] = bars
    recount = json.loads((LOCAL / "recount.json").read_text())
    figs["coverage"], figs["experts"] = recount["coverage"], recount["experts"]
    readers = LOCAL / "readers" / "figures.json"
    figs["readers"] = json.loads(readers.read_text()) if readers.exists() else None
    FIGURES.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n")
    if PAGE.exists():
        page = PAGE.read_text()
        if BEGIN in page and END in page:
            page = page[:page.index(BEGIN)] + tables(figs) + page[page.index(END) + len(END):]
            PAGE.write_text(page)
    print(tables(figs))


if __name__ == "__main__":
    main(sys.argv)
