"""Checks for the search for Egyptian words behind Meroitic ones (src/egyptian.py).

  python3 -I tests/test_egyptian.py

The two word lists, the answer key and the result files are local only, so the checks of the method run on
made-up words; the checks of the reported numbers need the local files and are skipped without them.
"""
import itertools, json, math, random, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import egyptian as E   # noqa: E402
from local_only import needs, run   # noqa: E402

PAGE = ROOT / "data/discovery/egyptian.md"
LOCAL = ("data/sources/egyptian/out/figures.json", "data/sources/egyptian/out/test.jsonl",
         "data/sources/egyptian/out/candidates.jsonl")
WORDS = ("data/sources/egyptian/coptic", "data/sources/egyptian/demotic", "data/sources/egyptian/loans_both.jsonl",
         "data/sources/egyptian/key_sources.json", "data/rilly2003")


def entry(ident, codes, kinds=("noun",)):
    return {"id": ident, "form": ident, "kinds": list(kinds), "codes": sorted(codes), "tokens": 1, "meaning": ""}


def test_meroitic_letters():
    # consonants only, 0 for a vowel at the start; the signs S, N and X of the corpus spelling
    assert E.meroitic("pelmoS") == "plms"
    assert E.meroitic("ant") == "0nt" and E.meroitic("apote") == "0pt"
    assert E.meroitic("xrpxNe") == "xrpxn" and E.meroitic("pXome") == "pXm"
    assert E.meroitic("yirewke") == "yrwk" and E.meroitic("e") == "0"
    assert all(c in E.MER for c in E.meroitic("abdeiklmnopqrstwxyNSX"))
    # a headword in Rilly's spelling goes through the corpus spelling; lost signs give nothing
    assert E.headword("ḫrpḫne") == "xrpxn" and E.headword("Pẖome") == "pXm" and E.headword("yet (2)") == "yt"
    assert E.headword("a[..]te") == ""


def test_demotic_letters():
    assert E.demotic("ḥm-nṯr") == "hmnTr" and E.demotic("mr-mšꜥ") == "mrmSA"
    assert E.demotic("Ꜣs.t") == "Ast" and E.demotic("Ꜣs.t", endings=False) == "As"
    assert E.demotic("fy(.t)-tn(-nb)", endings=False) == "fytn" and E.demotic("fy(.t)-tn(-nb)") == "fyttnnb"
    assert E.demotic("H̱nm") == "Xnm" and E.demotic("h̭rp") == "xrp" and E.demotic("Ḫnsw") == "xnsw"
    assert E.demotic("Pr-ꞽw-lq") == "prAwlq" and E.demotic("Ꞽmn") == "Amn"
    assert all(c in E.EGY for c in E.demotic("ꜣꞽyꜥwbpfmnrlhḥḫẖsšqkgtṱṯdḏz"))


def test_coptic_letters():
    assert E.coptic("ϩⲟⲛⲧ") == "hnt" and E.coptic("ⲗⲉⲙⲏⲏϣⲉ") == "lmS" and E.coptic("ⲗⲁϣⲁⲛⲉ") == "lSn"
    assert E.coptic("ⲟⲩⲱϣⲧ") == "wSt"            # ⲟⲩ before a vowel is w
    assert E.coptic("ⲉⲓⲟⲟⲣ") == "yr"             # ⲉⲓ before a vowel is y
    assert E.coptic("ⲟⲩⲥⲓⲣⲉ") == "Asr"           # a vowel at the start is A, vowels inside are not written
    assert E.coptic("ⲕⲁⲓⲥⲁⲣ") == "ksr" and E.coptic("ⲯⲩⲭⲏ") == "psk" and E.coptic("ⲁⲩⲱ") == "Aw"
    assert E.coptic("ⲣ̄ⲣⲟ") == "rr" and E.coptic("Ⲡⲉ-ⲧⲣⲉ") == "ptr"
    assert all(c in E.EGY for c in E.coptic("".join(E.COP) + E.VOWELS))


def test_the_starting_table_and_the_model_are_chances():
    for e in E.EGY:
        row = E.neutral(e)
        assert math.isclose(sum(row.values()), 1.0), e
        assert set(row) == set(E.MER) | {""}
    assert E.neutral("p")["p"] > E.neutral("p")["b"] > E.neutral("p")["m"]     # itself, its like, the rest
    assert E.neutral("S")["s"] > 0.8 and E.neutral("A")[""] > E.neutral("t")[""]
    md = E.model()
    stay = 1 - sum(math.exp(v) for v in md["add"].values())
    for e in E.EGY:
        assert math.isclose(sum(math.exp(v) for v in md["out"][e].values()), stay), e
    assert math.isclose(sum(math.exp(v) for v in md["article"].values()), 1.0)


def test_score_and_alignment():
    md = E.model()
    assert E.score("plms", "plms", md) > E.score("plms", "plmt", md) > E.score("plms", "krtn", md)
    assert E.score("plsn", "lSn", md) > E.score("plsn", "lSnk", md)        # the article p in front
    a, ops = E.align("plsn", "lSn", md)
    assert a == "p" and ops == [("p", "p"), ("l", "l"), ("S", "s"), ("n", "n")]
    a, ops = E.align("0nt", "hmnTr", md)
    assert a == "" and "".join(e for e, _ in ops) == "hmnTr" and "".join(m for _, m in ops) == "0nt"
    # the score is the sum of the steps of its alignment
    a, ops = E.align("twst", "wSt", md)
    total = md["article"][a] + sum(md["add"][m] if not e else md["out"][e][m] for e, m in ops)
    assert math.isclose(total, E.score("twst", "wSt", md))


def test_training_counts_what_the_loans_show():
    # in these loans š always gives s, h is always dropped, and every word takes the article p
    loans = [("psm", ["hSm"]), ("pstn", ["Stnh"]), ("prs", ["rhS"]), ("pkns", ["hknS"])]
    before, after = E.model(), E.train(loans)
    assert after["out"]["h"][""] > before["out"]["h"][""]
    assert after["out"]["S"]["s"] > before["out"]["S"]["s"]
    assert after["article"]["p"] > after["article"][""] == after["article"]["t"]
    # the article's own letter is not counted as a sound match: the row of p keeps its shape
    assert math.isclose(after["out"]["p"]["p"] - after["out"]["p"]["b"], before["out"]["p"]["p"] - before["out"]["p"]["b"])
    assert not math.isclose(after["out"]["h"][""] - after["out"]["h"]["x"], before["out"]["h"][""] - before["out"]["h"]["x"])
    # a loan that shares a source with the one left out does not train
    pool = [entry("a", ["hSm"]), entry("b", ["Stnh"]), entry("c", ["rhS"])]
    items = [{"word": "psm", "sources": [0]}, {"word": "pstn", "sources": [1]}, {"word": "psm", "sources": [0, 2]},
             {"word": "", "sources": [1]}, {"word": "pkn", "sources": []}]
    assert E.pairs(items, pool) == [("psm", ["hSm"]), ("pstn", ["Stnh"]), ("psm", ["hSm", "rhS"])]
    assert E.pairs(items, pool, without=[0]) == [("pstn", ["Stnh"])]


def test_the_search_equals_scoring_every_entry():
    rnd = random.Random(5)
    pool = [entry(f"e{k}", {"".join(rnd.choice(E.EGY) for _ in range(rnd.randint(1, 6)))
                            for _ in range(rnd.randint(1, 2))}) for k in range(400)]
    trie = E.Trie(list(enumerate(pool)))
    md = E.train([("plms", ["lmS"]), ("0nt", ["hnt"]), ("twst", ["wSt"])])
    for word in ("plms", "0nt", "krr", "twstm", "xXwy0", "ss"):
        full = sorted(((max(E.score(word, c, md) for c in e["codes"]), k) for k, e in enumerate(pool)),
                      key=lambda x: (-x[0], x[1]))
        for top in (1, 5):
            got = E.search(word, trie, md, top=top)
            assert [k for _, k in got] == [k for _, k in full[:top]], (word, top)
            assert all(math.isclose(a, b) for (a, _), (b, _) in zip(got, full))
        floor = full[9][0]
        assert len(E.search(word, trie, md, floor=floor - 1e-9)) == sum(s >= floor - 1e-9 for s, _ in full)


def test_the_place_of_a_true_source():
    pool = [entry("src", ["lmS"], ["title"]), entry("near", ["lmt"], ["title"]), entry("far", ["krt"], ["title"]),
            entry("noun", ["lmS"], ["noun"]), entry("tie", ["lmS", "xxx"], ["title"])]
    tr = E.tries(pool)
    md = E.model()
    title = tr[frozenset({"title"})]
    n, s = E.place("plms", [0], title, md, pool)
    assert n == 2 and math.isclose(s, E.score("plms", "lmS", md))      # itself and the tie; ties count against it
    assert E.place("plms", [3], title, md, pool) == (None, None)       # a noun is not in the pool of titles
    assert E.place("plms", [3], tr["all"], md, pool)[0] == 3
    assert tr["all"].size == 5 and title.size == 4
    # by letters: the same place, and None when no entry of the scope has these letters
    assert E.place_of_letters("plms", {"lmS"}, title, md) == 2
    assert E.place_of_letters("plms", {"lm"}, title, md) is None       # only the beginning of an entry
    assert E.place_of_letters("plms", {"qqq"}, title, md) is None


def test_printed_sources_of_a_key_row():
    row = {"language": "Egyptian", "etymon": "p3 mr-mšᶜ", "also": ["Coptic ⲗⲉⲙⲏⲏϣⲉ", "Greek λεμεισα", "Demotic rṯ"]}
    assert E.printed(row) == {"pAmrmSA", "lmS", "rT"}
    assert E.printed({"language": "Greek", "etymon": "Καῖσαρ", "also": []}) == set()
    assert E.printed({"language": "Egyptian", "etymon": "", "also": []}) == set()


def test_made_up_words():
    words = ["plms", "0nt", "0pt", "ksr", "prt", "twst", "yrwk", "xrpx", "mlkdn", "0rbtk", "qrn", "wyk"] * 3
    a, b = E.made_up(words, n=20, seed=3), E.made_up(words, n=20, seed=3)
    assert a == b and E.made_up(words, n=20, seed=4) != a
    assert sorted(a) == list(range(E.SHORTEST, E.LONGEST + 1))
    for k, made in a.items():
        assert len(made) == 20
        assert all(len(w) == k or (k == E.LONGEST and len(w) >= k) for w in made)
        assert all("0" not in w[1:] and set(w) <= set(E.MER) for w in made)
    pairs_seen = {x + y for w in words for x, y in zip(w, w[1:])}
    assert all(x + y in pairs_seen for made in a.values() for w in made for x, y in zip(w, w[1:]))


def test_chance_and_the_bar_for_many_tries():
    assert E.chance(-1.0, [-3, -2, -1, -0.5]) == 3 / 5          # two reach it, and the word itself
    assert E.chance(0.0, [-3, -2]) == 1 / 3 and E.chance(-9, [-3, -2]) == 1.0
    assert E.passing([0.001, 0.2, 0.5, 0.9], q=0.2) == 1
    assert E.passing([0.01, 0.02, 0.03, 0.9], q=0.2) == 3
    assert E.passing([0.3, 0.4, 0.9], q=0.2) == 0 and E.passing([], q=0.2) == 0


def test_the_kinds_of_the_pools():
    assert all(set(n) <= set(w) for n, w in ((set(a), set(b)) for a, b in E.SCOPE.values()))
    kinds = set(E.TAG.values())
    assert all(set(a) | set(b) <= kinds for a, b in E.SCOPE.values())
    pool = [entry("t", ["mr"], ["title"]), entry("g", ["Amn"], ["god"]), entry("x", ["nb"], [])]
    tr = E.tries(pool)
    assert tr["all"].size == 3 and tr[frozenset({"god"})].size == 1 and tr[frozenset(E.NAMES)].size == 1


def test_the_checkers_answers_are_read_against_the_decoys():
    old = E.HERE, E.CHECK, E.OUT
    with tempfile.TemporaryDirectory() as tmp:
        E.HERE = Path(tmp)
        E.CHECK, E.OUT = E.HERE / "check", E.HERE / "out"
        E.CHECK.mkdir()
        E.OUT.mkdir()
        try:
            key = {"P01": {"piece": "a", "decoy": False, "chance": 0.01}, "P02": {"piece": "b", "decoy": True, "chance": 0.9},
                   "P03": {"piece": "c", "decoy": False, "chance": 0.02}}
            (E.HERE / "check_key.json").write_text(json.dumps(key))
            one = [{"id": "P01", "verdict": "fits", "candidate": "tla:d1", "reason": "x"}, {"id": "P02", "verdict": "no"},
                   {"id": "P03", "verdict": "known", "candidate": "perite"}, {"id": "P09", "verdict": "fits"},
                   {"id": "P01", "verdict": "no"}]
            two = [{"id": "P01", "verdict": "fits", "candidate": "tla:d1"}, {"id": "P02", "verdict": "fits"},
                   {"id": "P03", "verdict": "maybe"}]
            (E.CHECK / "reader1.jsonl").write_text("\n".join(map(json.dumps, one)) + "\nnot json\n[1]\n")
            (E.CHECK / "reader2.jsonl").write_text("\n".join(map(json.dumps, two)) + "\n")
            E.check_merge()
            got = json.loads((E.OUT / "check.json").read_text())
        finally:
            E.HERE, E.CHECK, E.OUT = old
    assert (got["items"], got["best"], got["decoys"]) == (3, 2, 1)
    assert got["readers"]["reader1"] == {"answered": 3, "best": {"fits": 1, "known": 1}, "decoys": {"no": 1}}
    assert got["readers"]["reader2"] == {"answered": 2, "best": {"fits": 1}, "decoys": {"fits": 1}}
    assert got["answered_by_both"] == 2 and got["same_verdict"] == 1
    assert [x["piece"] for x in got["fits_for_both"]] == ["a"] and got["known_for_both"] == []


# ------------------------------------------------------------------------------ the reported numbers (local)

def figures():
    needs(*LOCAL)
    return json.loads((ROOT / LOCAL[0]).read_text(encoding="utf-8"))


def test_reported_pools_and_test():
    f = figures()
    assert f["pool"] == {"entries": 16943, "demotic": 5660, "coptic": 11283,
                         "kinds": {"noun": 9095, "verb": 3683, "person": 1249, "adjective": 532, "title": 310,
                                   "place": 277, "god": 251}}
    t = f["test"]
    assert (t["loans"], t["with_source"]) == (35, 24)
    assert (t["names"]["loans"], t["names"]["with_source"]) == (21, 13)
    assert t["names"]["narrow"] == {"in_scope": 10, "top1": 7, "top3": 10, "top5": 10, "top10": 10}
    assert t["names"]["wide"] == {"in_scope": 10, "top1": 4, "top3": 8, "top5": 8, "top10": 10}
    assert (t["words"]["loans"], t["words"]["with_source"]) == (14, 11)
    assert t["words"]["narrow"] == {"in_scope": 8, "top1": 1, "top3": 1, "top5": 2, "top10": 5}
    assert t["words"]["wide"] == {"in_scope": 11, "top1": 2, "top3": 3, "top5": 4, "top10": 6}
    assert t["words"]["chance_narrow"] == {"compared": 11, "at_most_0.05": 0}
    assert t["words"]["chance_wide"] == {"compared": 11, "at_most_0.05": 2}
    assert t["names"]["chance_narrow"] == {"compared": 8, "at_most_0.05": 3}


def test_reported_search():
    f = figures()
    u = f["unknown"]
    assert (u["pieces"], u["searched"], u["too_short"], u["new"]) == (608, 442, 166, 383)
    assert u["narrow"] == {"at_most_0.05": 22, "expected_by_chance": 19.2, "passing_q_0.2": 0}
    assert u["wide"] == {"at_most_0.05": 26, "expected_by_chance": 19.2, "passing_q_0.2": 0}
    assert f["native"]["words"] == 64
    assert (min(f["native"]["at_most_0.05"].values()), max(f["native"]["at_most_0.05"].values())) == (0, 5)


def test_reported_other_sets_and_the_check():
    f = figures()
    assert f["others"] == {
        "proposal": {"words": 24, "narrow": {"in_scope": 8, "top5": 4}, "wide": {"in_scope": 11, "top5": 2}},
        "in Egyptian letters": {"words": 30, "narrow": {"in_scope": 3, "top5": 3}, "wide": {"in_scope": 3, "top5": 3}}}
    needs("data/sources/egyptian/out/check.json")
    c = json.loads((ROOT / "data/sources/egyptian/out/check.json").read_text(encoding="utf-8"))
    assert (c["items"], c["best"], c["decoys"]) == (45, 33, 12)
    for reader in ("reader1", "reader2"):
        assert c["readers"][reader] == {"answered": 45, "best": {"no": 27, "known": 5, "fits": 1}, "decoys": {"no": 12}}
    assert (c["answered_by_both"], c["same_verdict"]) == (45, 45)
    assert [x["piece"] for x in c["fits_for_both"]] == ["aribet"]
    assert sorted(x["piece"] for x in c["known_for_both"]) == ["menote", "pertese", "petmoS", "prSn", "stol"]
    assert not any(x["decoy"] for x in c["fits_for_both"] + c["known_for_both"])


def test_the_pages_tables_are_the_result_file():
    needs(*LOCAL)
    page = PAGE.read_text(encoding="utf-8").replace("**", "")
    rows = [json.loads(l) for l in (ROOT / LOCAL[1]).read_text(encoding="utf-8").splitlines()]
    shown = 0
    for r in rows:
        name = r["headword"].split(" (")[0]
        line = next((l for l in page.splitlines() if l.startswith(f"| `{name}` |")), None)
        if "all" not in r or line is None:
            continue
        shown += 1
        for scope in ("narrow", "wide"):
            if r[scope]["place"] is not None:
                assert f'| {r[scope]["place"]:,} of {r[scope]["of"]:,} |' in line, (name, scope, line)
        if r["kind"] in ("title", "noun", "verb"):
            assert line.rstrip().endswith(f'| {r["all"]["place"]:,} |'), (name, line)
    assert shown == 21                           # the 11 titles, nouns and verbs and the 10 names in their own pool
    f = figures()
    u = f["unknown"]
    for text in (f'Of the {u["new"]} pieces searched', f'| {u["narrow"]["at_most_0.05"]} | {u["wide"]["at_most_0.05"]} |',
                 f'{u["too_short"]} of those were not searched', f'Of the {u["searched"]} searched',
                 f'for {f["test"]["words"]["wide"]["top5"]} of the 14', f'all {f["test"]["names"]["narrow"]["top3"]} names',
                 f'the {f["native"]["words"]} Meroitic words'):
        assert text in page, text


def test_the_hidden_test_gives_the_reported_places():
    """The test of the titles, nouns and verbs again, from the word lists: the places of the result file."""
    needs(*LOCAL, *WORDS)
    pool = E.pools()
    tr = E.tries(pool)
    items = E.known(pool)
    usable = [it for it in items if it["sources"] and it["word"]]
    saved = {r["headword"]: r for r in map(json.loads, (ROOT / LOCAL[1]).read_text(encoding="utf-8").splitlines())}
    assert len(items) == len(saved) == 35 and len(usable) == 24
    places = {}
    for it in usable:
        if it["kind"] in ("title", "noun", "verb"):
            md = E.train(E.pairs(usable, pool, without=it["sources"]))
            wide = frozenset(E.SCOPE[it["kind"]][1])
            places[it["headword"]] = E.place(it["word"], it["sources"], tr[wide], md, pool)[0]
            assert places[it["headword"]] == saved[it["headword"]]["wide"]["place"], it["headword"]
    assert places == {"ant": 7, "apote": 101, "kisri": 4, "pelmos": 3, "perite": 24, "peseto": 3121, "plsn": 1,
                      "qelile": 15, "tewiseti": 6, "yirewke": 222, "ḫrpḫe": 1}


def test_the_public_list_is_the_result_file():
    needs(*LOCAL)
    rows = [json.loads(l) for l in (ROOT / LOCAL[2]).read_text(encoding="utf-8").splitlines()]
    searched = {r["piece"]: r for r in rows if "narrow" in r}
    lines = [l.split("\t") for l in E.PUBLIC.read_text(encoding="utf-8").splitlines()]
    assert len(lines) == len(searched) + 1 == 443 and len(set(map(len, lines))) == 1
    for cells in lines[1:]:
        r = searched[cells[0]]
        assert cells[1] == r["kind"] and cells[2] == str(r["texts"])
        assert cells[4] == f'{r["narrow"]["chance"]:.3f}' and cells[5] == r["narrow"]["hits"][0]["id"]
        assert cells[7] == f'{r["wide"]["chance"]:.3f}' and cells[8] == r["wide"]["hits"][0]["id"]
    best = [min(float(c[4]), float(c[7])) for c in lines[1:]]
    assert best == sorted(best)                                         # best matches first
    # no meaning of either dictionary and no gloss of the lexicon is in the public list
    assert all(len(c) == 10 for c in lines)


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
