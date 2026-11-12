"""Checks for the search for Egyptian words behind Meroitic ones (src/egyptian.py).

  python3 -I tests/test_egyptian.py

The two word lists, the answer key and the result files are local only, so the checks of the method run on
made-up words; the checks of the reported numbers need the local files and are skipped without them.
"""
import collections, contextlib, io, json, math, random, sys, tempfile
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


def test_letters_with_vowels():
    # Meroitic: the written e, i and o stay; a is written at the start only, and that is the 0
    assert E.meroitic("pelmoS", True) == "pelmos" and E.meroitic("ant", True) == "0nt"
    assert E.meroitic("apote", True) == "0pote" and E.meroitic("erike", True) == "0erike"
    assert E.meroitic("kiSri", True) == "kisri" and E.meroitic("qelile", True) == "qelile"
    assert E.headword("Pẖome", True) == "pXome" and E.headword("a[..]te", True) == ""
    assert (E.consonants("pelmos"), E.consonants("0erike"), E.consonants("")) == (4, 3, 0)
    assert all(c in E.MER + E.VOWELS_M for c in E.meroitic("abdeiklmnopqrstwxyNSX", True))
    # the sign ne (N) writes its e, once; without vowels it is n as before
    assert E.meroitic("tmNte", True) == "tmnete" and E.meroitic("mleNe", True) == "mlene"
    assert E.meroitic("N", True) == "ne" and E.meroitic("tmNte") == "tmnt"
    assert E.headword("qorene", True) == "qorene" and E.headword("ḫrpḫne", True) == "xrpxne"
    # Coptic: each vowel as its class, a doubled one once; the glides and the mark of the start are as without
    assert E.coptic("ⲗⲉⲙⲏⲏϣⲉ", True) == "lemeSe" and E.coptic("ⲗⲁϣⲁⲛⲉ", True) == "laSane"
    assert E.coptic("ϩⲟⲛⲧ", True) == "hont" and E.coptic("ⲣⲏⲧ", True) == "ret"
    assert E.coptic("ⲟⲩⲱϣⲧ", True) == "woSt" and E.coptic("ⲉⲓⲟⲟⲣ", True) == "yor"
    assert E.coptic("ⲟⲩⲥⲓⲣⲉ", True) == "Aosire" and E.coptic("ⲕⲁⲓⲥⲁⲣ", True) == "kaisar"
    assert E.coptic("ⲛⲟⲩⲃ", True) == "nob" and E.coptic("ⲏⲥⲉ", True) == "Aese"
    assert all(c in E.EGY + E.VOWELS_E for c in E.coptic("".join(E.COP) + E.VOWELS, True))
    # without its vowels a string is the consonant string
    for form in ("ⲗⲉⲙⲏⲏϣⲉ", "ⲟⲩⲱϣⲧ", "ⲉⲓⲟⲟⲣ", "ⲟⲩⲥⲓⲣⲉ", "ⲕⲁⲓⲥⲁⲣ", "ⲁⲩⲱ", "ⲣ̄ⲣⲟ", "ⲉⲓⲱⲧ", "ⲟⲩⲟⲉⲓⲛ"):
        assert "".join(c for c in E.coptic(form, True) if c not in E.VOWELS_E) == E.coptic(form), form


def test_the_model_with_vowels():
    mer, egy = E.MER + E.VOWELS_M, E.EGY + E.VOWELS_E
    for e in egy:
        row = E.neutral(e, mer)
        assert math.isclose(sum(row.values()), 1.0) and set(row) == set(mer) | {""}, e
    assert E.neutral("e", mer)["e"] > E.neutral("e", mer)["i"] > E.neutral("e", mer)["p"]   # itself, a vowel, the rest
    assert E.neutral("a", mer)["e"] == E.neutral("a", mer)["o"] > E.neutral("a", mer)["p"]  # no a inside a word
    assert E.neutral("e", mer)[""] > E.neutral("t", mer)[""]                                # a vowel drops easily
    md = E.model(None, mer, egy)
    stay = 1 - sum(math.exp(v) for v in md["add"].values())
    assert all(math.isclose(sum(math.exp(v) for v in md["out"][e].values()), stay) for e in egy)
    # the build's model is what it was: the consonant alphabets, and no vowel in it
    assert E.model() == E.model(None, E.MER, E.EGY) and set(E.model()["add"]) == set(E.MER)
    assert E.train([("plms", ["lmS"])]) == E.train([("plms", ["lmS"])], mer=E.MER, egy=E.EGY)
    # vowels are counted like any letter: here ⲏ and ⲉ always give e, and ⲁ always drops
    md = E.train([("pelmes", ["lemeS"]), ("ret", ["raet"]), ("mes", ["maes"])], mer=mer, egy=egy)
    assert md["out"]["e"]["e"] > E.model(None, mer, egy)["out"]["e"]["e"]
    assert md["out"]["a"][""] > E.model(None, mer, egy)["out"]["a"][""]
    assert E.score("pelmes", "lemeS", md) > E.score("pelmes", "lomoS", md) > E.score("pelmes", "tomoS", md)
    # the letter strings to search are chosen by name
    pool = [dict(entry("a", ["lmS"]), voiced=["lemeS"]), dict(entry("b", ["lmS"]), voiced=["lomoS"])]
    trie = E.Trie(list(enumerate(pool)), "voiced")
    assert E.place("pelmes", [0], trie, md, pool, "voiced")[0] == 1
    assert E.place("pelmes", [1], trie, md, pool, "voiced")[0] == 2
    assert E.place("plms", [0], E.Trie(list(enumerate(pool))), E.model(), pool)[0] == 2     # consonants: a tie
    items = [{"word": "plms", "voiced": "pelmes", "sources": [0]}, {"word": "rt", "voiced": "", "sources": [1]}]
    assert E.pairs(items, pool, (), "voiced", "voiced") == [("pelmes", ["lemeS"])]
    assert E.pairs(items, pool) == [("plms", ["lmS"]), ("rt", ["lmS"])]


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
    # nor when a Meroitic letter is added before the article: that letter counts as added, the article does not
    assert E.align("0psm", "Sm", before) == ("p", [("", "0"), ("p", "p"), ("S", "s"), ("m", "m")])
    once = E.train([("0psm", ["Sm"])], rounds=1)
    assert math.isclose(once["out"]["p"]["p"] - once["out"]["p"]["b"], before["out"]["p"]["p"] - before["out"]["p"]["b"])
    assert once["add"]["0"] > once["add"]["k"] and math.isclose(before["add"]["0"], before["add"]["k"])
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
    # many exact ties, from a few letters: the search keeps the best `top` and breaks ties by entry number
    letters = "pmkrlnS"
    pool = [entry(f"t{k}", {"".join(rnd.choice(letters) for _ in range(rnd.randint(1, 4)))
                            for _ in range(rnd.randint(1, 2))}) for k in range(600)]
    trie, md = E.Trie(list(enumerate(pool))), E.model()
    for word in ["".join(rnd.choice("pmkrlns0") for _ in range(rnd.randint(2, 5))) for _ in range(20)]:
        full = sorted(((max(E.score(word, c, md) for c in e["codes"]), k) for k, e in enumerate(pool)),
                      key=lambda x: (-x[0], x[1]))
        for top in (1, 2, 5, 10):
            assert E.search(word, trie, md, top=top) == full[:top], (word, top)
    # a tie the walk meets in the other order: entry 2 (mk) lies under the m of entry 0 and is met before entry 1
    pool = [entry(f"e{k}", [c]) for k, c in enumerate(["mr", "kp", "mk", "rr", "ll", "nn"])]
    assert E.score("kk", "kp", md) == E.score("kk", "mk", md) > E.score("kk", "mr", md)
    assert E.search("kk", E.Trie(list(enumerate(pool))), md, top=1) == [(E.score("kk", "kp", md), 1)]


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
    # the hits as the result files keep them
    assert E.hit_rows([(-1.23456, 0), (-2.0, 4)], pool) == [{"id": "src", "form": "src", "meaning": "", "score": -1.235},
                                                           {"id": "tie", "form": "tie", "meaning": "", "score": -2.0}]


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
    # the first letter is drawn as often as the words start with it: nine words in ten open with a vowel here
    skewed = E.made_up(["0nt", "0rbtk", "0pt", "0mn", "0ns", "0trs", "0rm", "0sr", "0tmk", "plms"], n=100, seed=3)
    starts = [w[0] for made in skewed.values() for w in made]
    assert starts.count("0") > 0.8 * len(starts)
    # a word's chance is counted among the made-up words of its length, the longest of them together
    trie, md = E.Trie(list(enumerate([entry("a", ["lmS"]), entry("b", ["krt"])]))), E.model()
    fake, cache = {3: ["plm", "krt"], 4: ["plms", "xXwy"]}, {}
    best = lambda w: E.search(w, trie, md)[0][0]   # noqa: E731
    assert E.chance_of("plms", trie, md, fake, cache) == E.chance(best("plms"), [best(w) for w in fake[4]]) == 2 / 3
    assert E.chance_of("krtpp", trie, md, fake, cache) == E.chance(best("krtpp"), [best(w) for w in fake[4]])
    assert E.chance_of("krt", trie, md, fake, cache) == 2 / 3 and set(cache) == {(trie, 3), (trie, 4)}


def test_made_up_words_with_vowels():
    words = ["pelmos", "0nt", "0pote", "kisri", "perite", "tewiseti", "yirewke", "qelile", "0rebetke", "qorene",
             "mlo", "xrpxne", "0tepedemo"] * 3
    made = E.made_up(words, n=15, seed=3, longest=11, least=3)
    assert sorted(made) == list(range(E.SHORTEST, 12)) and made == E.made_up(words, n=15, seed=3, longest=11, least=3)
    for k, ws in made.items():
        assert len(ws) == 15 and all(len(w) == k or (k == 11 and len(w) >= k) for w in ws)
        assert all(E.consonants(w) >= 3 and set(w) <= set(E.MER + E.VOWELS_M) for w in ws)
    assert any(set(w) & set(E.VOWELS_M) for ws in made.values() for w in ws)
    # the build's made-up words are unchanged: no least number of consonants, the build's lengths
    plain = ["plms", "0nt", "0pt", "ksr", "prt", "twst", "yrwk", "xrpx", "mlkdn", "0rbtk", "qrn", "wyk"] * 3
    assert E.made_up(plain, n=20, seed=3) == E.made_up(plain, n=20, seed=3, longest=E.LONGEST, least=0)


def test_the_list_of_the_vowel_search():
    hit = {"id": "ccl:C1", "form": "ⲣⲏⲧ", "meaning": "a title", "score": -1.0}
    rows = [{"piece": "bbb", "kind": "title", "letters": "bebe", "texts": 2, "mentions_egyptian": False,
             "spelled_like": "", "vowels": {"chance": 0.5, "hits": [hit]}},
            {"piece": "aaa", "kind": "noun", "letters": "0ro", "texts": 1, "mentions_egyptian": False,
             "spelled_like": "aro", "vowels": {"chance": 0.01, "hits": [dict(hit, id="ccl:C2")]}},
            {"piece": "ccc", "kind": "verb", "letters": "ker", "texts": 9, "mentions_egyptian": True,
             "spelled_like": "", "vowels": {"chance": 0.5, "hits": [hit]}}]
    lines = [l.split("\t") for l in E.public_vowel_list(rows).splitlines()]
    assert {len(c) for c in lines} == {8} and lines[0][0] == "piece"
    assert [c[0] for c in lines[1:]] == ["aaa", "ccc", "bbb"]            # best first, then the more texts
    assert lines[1][3:] == ["spelled like aro", "0ro", "0.010", "ccl:C2", "ⲣⲏⲧ"] and lines[2][3] == "yes"
    assert "a title" not in E.public_vowel_list(rows)                    # no meaning of the dictionary
    # the test's figures: a loan moves only when both searches place its source
    test = [{"headword": "a", "kind": "title", "consonants": 3, "vowels": 1},
            {"headword": "b", "kind": "god name", "consonants": None, "vowels": 4},
            {"headword": "c", "kind": "noun", "consonants": 2, "vowels": 5, "chance": 0.01}]
    t = E.vowel_figures([], test, {}, rows, 64)["test"]
    assert (t["moved_up"], t["moved_down"], t["chance"]) == (1, 1, {"compared": 1, "at_most_0.05": 1})
    assert (t["all"]["consonants"]["in_scope"], t["all"]["vowels"]["in_scope"], t["names"]["loans"]) == (2, 3, 1)


def test_chance_and_the_bar_for_many_tries():
    assert E.chance(-1.0, [-3, -2, -1, -0.5]) == 3 / 5          # two reach it, and the word itself
    assert E.chance(0.0, [-3, -2]) == 1 / 3 and E.chance(-9, [-3, -2]) == 1.0
    assert E.passing([0.001, 0.2, 0.5, 0.9], q=0.2) == 1
    assert E.passing([0.01, 0.02, 0.03, 0.9], q=0.2) == 3
    assert E.passing([0.3, 0.4, 0.9], q=0.2) == 0 and E.passing([], q=0.2) == 0
    # the bar grows with the rank (a fixed bar of q / n would pass 2 and 0 of these), and a later pass carries
    # the earlier ones with it
    assert E.passing([0.01, 0.04, 0.06, 0.9], q=0.2) == 3 and E.passing([0.06, 0.07, 0.08, 0.09], q=0.2) == 4
    # with 300 made-up words no chance is below 1 in 301, so one piece of 383 never passes on its own: seven
    # would have to sit at that floor together
    assert E.fewest_to_pass(383, q=0.2, made=300) == 7 and E.fewest_to_pass(60, q=0.2, made=300) == 1
    floor = [1 / 301] * 7 + [0.5] * 376
    assert E.passing(floor) == 7 and E.passing(floor[1:] + [0.5]) == 0
    # how often chance alone gives k or more of n words below a 5% bar
    assert math.isclose(E.as_many(0, 383), 1.0) and math.isclose(E.as_many(1, 1), 0.05)
    assert math.isclose(E.as_many(2, 2, p=0.5), 0.25) and E.as_many(26, 383) < E.as_many(22, 383) < 0.5


def test_the_kinds_of_the_pools():
    assert all(set(n) <= set(w) for n, w in ((set(a), set(b)) for a, b in E.SCOPE.values()))
    kinds = set(E.TAG.values())
    assert all(set(a) | set(b) <= kinds for a, b in E.SCOPE.values())
    pool = [entry("t", ["mr"], ["title"]), entry("g", ["Amn"], ["god"]), entry("x", ["nb"], [])]
    tr = E.tries(pool)
    assert tr["all"].size == 3 and tr[frozenset({"god"})].size == 1 and tr[frozenset(E.NAMES)].size == 1


def test_the_checkers_answers_are_read_against_the_decoys():
    old = E.HERE, E.CHECK, E.CHECK_VOWELS, E.OUT
    with tempfile.TemporaryDirectory() as tmp:
        E.HERE = Path(tmp)
        E.CHECK, E.CHECK_VOWELS, E.OUT = E.HERE / "check", E.HERE / "check_vowels", E.HERE / "out"
        E.CHECK.mkdir()
        E.CHECK_VOWELS.mkdir()
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
            (E.CHECK / "reader1.jsonl").write_text("\n".join(map(json.dumps, one)) + '\nnot json\n[1]\n{"id": ["P02"], "verdict": "no"}\n')
            (E.CHECK / "reader2.jsonl").write_text("\n".join(map(json.dumps, two)) + "\n")
            # the second pack: its own key, folder and result file, and nothing of the first
            (E.HERE / "check_vowels_key.json").write_text(json.dumps({"P01": {"piece": "d", "decoy": True, "chance": 0.7}}))
            for name in ("reader1", "reader2"):
                (E.CHECK_VOWELS / f"{name}.jsonl").write_text(json.dumps({"id": "P01", "verdict": "no"}) + "\n")
            with contextlib.redirect_stdout(io.StringIO()):
                E.check_merge()
                E.check_merge(with_vowels=True)
            got = json.loads((E.OUT / "check.json").read_text())
            second = json.loads((E.OUT / "check_vowels.json").read_text())
        finally:
            E.HERE, E.CHECK, E.CHECK_VOWELS, E.OUT = old
    assert (got["items"], got["best"], got["decoys"]) == (3, 2, 1)
    assert got["readers"]["reader1"] == {"answered": 3, "best": {"fits": 1, "known": 1}, "decoys": {"no": 1}}
    assert got["readers"]["reader2"] == {"answered": 2, "best": {"fits": 1}, "decoys": {"fits": 1}}
    assert got["answered_by_both"] == 2 and got["same_verdict"] == 1
    assert [x["piece"] for x in got["fits_for_both"]] == ["a"] and got["known_for_both"] == []
    assert (second["items"], second["best"], second["decoys"], second["same_verdict"]) == (1, 0, 1, 1)
    assert second["readers"]["reader1"] == {"answered": 1, "best": {}, "decoys": {"no": 1}}


def test_a_pack_with_answers_is_never_replaced():
    with tempfile.TemporaryDirectory() as tmp:
        folder, key = Path(tmp) / "check", Path(tmp) / "check_key.json"
        files = {folder / "pack.jsonl": '{"id": "P01"}\n', key: '{"P01": {}}'}
        assert E.write_pack(folder, files, "brief one")                      # a new pack: written, with its brief
        assert (folder / "BRIEF.md").read_text() == "brief one" and key.read_text() == '{"P01": {}}'
        assert E.write_pack(folder, files, "brief two") and (folder / "BRIEF.md").read_text() == "brief two"
        (folder / "reader1.jsonl").write_text('{"id": "P01", "verdict": "no"}\n')
        # with answers beside it: the same pack is left as it is, and so is the brief the checkers read
        assert not E.write_pack(folder, files, "brief three")
        assert (folder / "BRIEF.md").read_text() == "brief two"
        # another pack or key stops the build, and nothing is written
        for changed in ({**files, key: '{"P01": {"decoy": true}}'}, {**files, folder / "pack.jsonl": "{}\n"}):
            try:
                E.write_pack(folder, changed, "brief four")
                raise AssertionError("write_pack replaced a pack that holds answers")
            except SystemExit as e:
                assert "reader1.jsonl" in str(e)
            assert all(p.read_text() == text for p, text in files.items()) and (folder / "BRIEF.md").read_text() == "brief two"


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
    assert u["narrow"] == {"at_most_0.05": 22, "expected_by_chance": 19.2, "as_many_by_chance": 0.283, "passing_q_0.2": 0}
    assert u["wide"] == {"at_most_0.05": 26, "expected_by_chance": 19.2, "as_many_by_chance": 0.073, "passing_q_0.2": 0}
    # the bar for 383 tries asks the best piece for 1 in 1,915; no chance is below 1 in 301
    assert (u["smallest_chance"], u["first_step_q_0.2"], u["fewest_at_the_smallest_chance_to_pass"]) == (0.00332, 0.000522, 7)
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
    second = page.split("\n## 2. ")[1].split("\n## 3. ")[0]       # section 5 has a table of its own
    for r in rows:
        name = r["headword"].split(" (")[0]
        line = next((l for l in second.splitlines() if l.startswith(f"| `{name}` |")), None)
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
    pct = lambda name: f'{u[name]["as_many_by_chance"]:.0%}'   # noqa: E731
    number = {6: "six"}
    kinds = collections.Counter(r["kind"] for r in rows if r["kind"] in E.C.NAME_KINDS and r.get("narrow", {}).get("place"))
    assert kinds == {"god name": 7, "place name": 2, "person name": 1}           # the 10 names of section 1
    candidates = [json.loads(l) for l in (ROOT / LOCAL[2]).read_text(encoding="utf-8").splitlines()]
    spelled = sum("narrow" in r and bool(r["spelled_like"]) and not r["mentions_egyptian"] for r in candidates)
    flat = " ".join(page.split())
    for text in (f'Of the {u["new"]} pieces searched', f'| {u["narrow"]["at_most_0.05"]} | {u["wide"]["at_most_0.05"]} |',
                 f'{u["too_short"]} of those were not searched', f'Of the {u["searched"]} searched',
                 f'for {f["test"]["words"]["wide"]["top5"]} of the 14', f'for {f["test"]["words"]["narrow"]["top5"]} among',
                 f'all {f["test"]["names"]["narrow"]["top3"]} names',
                 '(seven gods, two places and a person)', f'the {f["native"]["words"]} Meroitic words',
                 f'as many or more {pct("narrow")} and {pct("wide")} of the time', f'| {pct("narrow")} | {pct("wide")} |',
                 f'1 in {E.MADE_UP + 1}', f'1 in {round(u["new"] / E.FDR):,}',
                 f'{number[u["fewest_at_the_smallest_chance_to_pass"] - 1]} others at that floor',
                 f'At least {spelled + 5} pieces', f'{spelled} are spelled like such a word', 'recognised 5 more among the 33'):
        assert text in flat, text


def test_the_hidden_test_gives_the_reported_places():
    """The hidden test again, from the word lists: the pools the figures count, and every place of the result
    file, each loan with a model trained without it."""
    needs(*LOCAL, *WORDS)
    pool = E.pools()
    tr = E.tries(pool)
    assert figures()["pool"] == {"entries": len(pool), "demotic": sum(e["id"].startswith("tla:") for e in pool),
                                 "coptic": sum(e["id"].startswith("ccl:") for e in pool),
                                 "kinds": dict(collections.Counter(k for e in pool for k in e["kinds"]).most_common())}
    items = E.known(pool)
    usable = [it for it in items if it["sources"] and it["word"]]
    saved = {r["headword"]: r for r in map(json.loads, (ROOT / LOCAL[1]).read_text(encoding="utf-8").splitlines())}
    assert len(items) == len(saved) == 35 and len(usable) == 24
    wide = {}
    for it in usable:
        md = E.train(E.pairs(usable, pool, without=it["sources"]))
        for name, s in E.scopes(it["kind"]) + (("all", "all"),):
            n, sc = E.place(it["word"], it["sources"], tr[s], md, pool)
            assert (n, tr[s].size) == (saved[it["headword"]][name]["place"], saved[it["headword"]][name]["of"]), (it["headword"], name)
            if name == "wide" and it["kind"] in ("title", "noun", "verb"):
                wide[it["headword"]] = n
    assert wide == {"ant": 7, "apote": 101, "kisri": 4, "pelmos": 3, "perite": 24, "peseto": 3121, "plsn": 1,
                    "qelile": 15, "tewiseti": 6, "yirewke": 222, "ḫrpḫe": 1}


def test_what_the_model_counted_from_the_loans():
    """Section 6 of the page, point 3: the alignments the final model was counted from (the last of the three
    rounds aligns with the model of the second)."""
    needs(*LOCAL, *WORDS)
    pool = E.pools()
    items = E.known(pool)
    pairs = E.pairs([it for it in items if it["sources"] and it["word"]], pool)
    md = E.train(pairs, rounds=2)
    articles, out = collections.Counter(), collections.Counter()
    for word, codes in pairs:
        a, ops = E.align(word, max(codes, key=lambda c: (E.score(word, c, md), c)), md)
        articles[a] += 1
        egyptian = [(e, m) for e, m in ops if e]
        out.update(egyptian[len(a):])                # the article's letters are not sound matches
    row = lambda e: {m: k for (x, m), k in out.items() if x == e}   # noqa: E731
    assert (len(pairs), articles) == (24, {"": 19, "p": 4, "t": 1})
    assert row("h") == {"0": 4} and row("S") == {"s": 3} and row("n") == {"n": 5, "": 2}
    page = PAGE.read_text(encoding="utf-8")
    assert ("give the mark of a vowel at the start all 4 times, š gives s all 3 times, n is dropped 2 times in 7, "
            "and 4 loans carry the article p and 1 the article t") in " ".join(page.split())


def test_the_public_list_is_the_result_file():
    needs(*LOCAL)
    rows = [json.loads(l) for l in (ROOT / LOCAL[2]).read_text(encoding="utf-8").splitlines()]
    assert E.PUBLIC.read_text(encoding="utf-8") == E.public_list(rows)    # the list as the script writes it
    searched = {r["piece"]: r for r in rows if "narrow" in r}
    lines = [l.split("\t") for l in E.PUBLIC.read_text(encoding="utf-8").splitlines()]
    assert len(lines) == len(searched) + 1 == 443 and {len(c) for c in lines} == {10}
    best = [min(float(c[4]), float(c[7])) for c in lines[1:]]
    assert best == sorted(best)                                         # best matches first
    # the pieces set aside (section 3 of the page): 48 whose entry mentions one of the languages, 11 spelled
    # like an entry linked to Egyptian
    aside = collections.Counter("spelled like" if c[3].startswith("spelled like ") else c[3] for c in lines[1:])
    assert aside == {"no": 383, "yes": 48, "spelled like": 11}
    # no meaning of either dictionary is in it: the match columns hold chances, lemma numbers and lemma forms
    meanings = {h["meaning"] for r in searched.values() for name in ("narrow", "wide") for h in r[name]["hits"]} - {""}
    assert not meanings & {cell for c in lines[1:] for cell in c[4:]}


# ------------------------------------------------------------------------------------- with vowels (local)

VOWEL_FILES = ("data/sources/egyptian/out/vowel_figures.json", "data/sources/egyptian/out/vowel_test.jsonl",
               "data/sources/egyptian/out/vowel_candidates.jsonl")


def test_reported_vowel_search():
    needs(*VOWEL_FILES)
    f = json.loads((ROOT / VOWEL_FILES[0]).read_text(encoding="utf-8"))
    assert f["pool"] == {"coptic": 11283, "kinds": {"noun": 7139, "verb": 2946, "adjective": 448}}
    t = f["test"]
    assert (t["loans"], t["moved_up"], t["moved_down"]) == (13, 9, 3)
    assert t["all"]["consonants"] == {"in_scope": 13, "top1": 1, "top3": 3, "top5": 4, "top10": 7}
    assert t["all"]["vowels"] == {"in_scope": 13, "top1": 2, "top3": 4, "top5": 7, "top10": 9}
    assert (t["words"]["loans"], t["words"]["consonants"]["top5"], t["words"]["vowels"]["top5"]) == (8, 3, 6)
    assert (t["names"]["loans"], t["names"]["consonants"]["top5"], t["names"]["vowels"]["top5"]) == (5, 1, 1)
    assert t["chance"] == {"compared": 11, "at_most_0.05": 1}
    assert f["native"] == {"words": 64, "at_most_0.05": {"adjective+noun": 2, "noun": 2, "verb": 3},
                           "at_most_0.2": {"adjective+noun": 16, "noun": 17, "verb": 17}}
    u = f["unknown"]
    assert (u["searched"], u["new"], u["at_most_0.05"], u["expected_by_chance"]) == (278, 241, 13, 12.1)
    assert (u["as_many_by_chance"], u["passing_q_0.2"], u["fewest_at_the_smallest_chance_to_pass"]) == (0.43, 0, 5)
    # the figures are the result files' own
    rows = [json.loads(l) for l in (ROOT / VOWEL_FILES[2]).read_text(encoding="utf-8").splitlines()]
    test = [json.loads(l) for l in (ROOT / VOWEL_FILES[1]).read_text(encoding="utf-8").splitlines()]
    assert f["test"] == E.vowel_figures([], test, {}, rows, 64)["test"]
    assert f["unknown"] == E.vowel_figures([], test, {}, rows, 64)["unknown"]
    aside = collections.Counter("like" if r["spelled_like"] and not r["mentions_egyptian"] else r["mentions_egyptian"]
                                for r in rows)
    assert aside == {False: 241, True: 32, "like": 5}
    # the bar of the first section: five best by consonants (wide pool), five best with vowels, and either
    needs(*LOCAL)
    first = {r["headword"]: r for r in map(json.loads, (ROOT / LOCAL[1]).read_text(encoding="utf-8").splitlines())}
    words = [h for h, r in first.items() if r["kind"] in ("title", "noun", "verb")]
    by_consonants = {h for h in words if "wide" in first[h] and (first[h]["wide"]["place"] or 99) <= 5}
    with_vowels = {r["headword"] for r in test if r["kind"] in ("title", "noun", "verb") and r["vowels"] <= 5}
    assert (len(words), len(by_consonants), len(with_vowels), len(by_consonants | with_vowels)) == (14, 4, 6, 8)
    # the page's section 5 says these numbers
    flat = " ".join(PAGE.read_text(encoding="utf-8").split())
    words_for = {9: "Nine", 3: "three"}
    for text in (f'{t["all"]["consonants"]["top5"]} of 13 by consonants, {t["all"]["vowels"]["top5"]} of 13 with vowels',
                 f'Among the ten best: {t["all"]["consonants"]["top10"]} and {t["all"]["vowels"]["top10"]}',
                 f'{words_for[t["moved_up"]]} loans move up, {words_for[t["moved_down"]]} move down',
                 f'With vowels, {len(with_vowels)} of the 14', f'by consonants it was {len(by_consonants)}',
                 f'hold the source for {len(by_consonants | with_vowels)} of the 14',
                 f'for {t["chance"]["at_most_0.05"]} of the {t["chance"]["compared"]} loans compared',
                 f'{f["native"]["at_most_0.05"]["noun"]} beat the 5% bar among the nouns',
                 f'{f["native"]["at_most_0.2"]["noun"]} beat a 20% bar',
                 f'{u["searched"]} titles, nouns, verbs and adjectives were searched',
                 f'{u["searched"] - u["new"]} are set aside', f'which leaves {u["new"]}',
                 f'| Pieces whose best match beats the 5% bar | {u["at_most_0.05"]} |',
                 f'| How often chance alone gives {u["at_most_0.05"]} or more, by the made-up words | {u["as_many_by_chance"]:.0%} |',
                 f'for 7 of the 13 loans that have a Coptic source, against 4 by consonants alone',
                 f'for 6 of the 14 titles, nouns and verbs of the bar'):
        assert text in flat, text
    # what the native words predict, each piece in its own pool
    native = f["native"]["at_most_0.05"]
    expected = sum(native["+".join(sorted(E.VOWEL_SCOPE[r["kind"]]))] / f["native"]["words"]
                   for r in rows if not (r["mentions_egyptian"] or r["spelled_like"]))
    assert (f'pool ({native["noun"]} of 64 among the nouns, {native["verb"]} of 64 among the verbs) | '
            f'{round(expected)} |') in flat


def test_the_vowel_test_gives_the_reported_places():
    """The test of the vowel search again, from the Coptic lexicon: both columns of the page's table."""
    needs(*VOWEL_FILES, *WORDS)
    pool = E.coptic_pool()
    for e in pool:                                   # without its vowels a string is the consonant string
        assert {"".join(c for c in v if c not in E.VOWELS_E) for v in e["voiced"]} == set(e["codes"]), e["id"]
    nouns = [(k, e) for k, e in enumerate(pool) if "noun" in e["kinds"]]
    voiced, bare = E.Trie(nouns, "voiced"), E.Trie(nouns)
    items = [it for it in E.known(pool) if it["sources"] and it["voiced"]]
    saved = [json.loads(l) for l in (ROOT / VOWEL_FILES[1]).read_text(encoding="utf-8").splitlines()]
    assert [it["headword"] for it in items] == [r["headword"] for r in saved] and len(items) == 13
    mer, egy = E.MER + E.VOWELS_M, E.EGY + E.VOWELS_E
    page = PAGE.read_text(encoding="utf-8")
    for it, r in zip(items, saved):
        md = E.train(E.pairs(items, pool, it["sources"], "voiced", "voiced"), mer=mer, egy=egy)
        plain = E.train(E.pairs(items, pool, it["sources"]))
        got = (E.place(it["word"], it["sources"], bare, plain, pool)[0],
               E.place(it["voiced"], it["sources"], voiced, md, pool, "voiced")[0])
        assert got == (r["consonants"], r["vowels"]) and r["of"] == voiced.size == 7139, it["headword"]
        name = it["headword"].split(" (")[0]
        fifth = page.split("\n## 5. ")[1].split("\n## 6. ")[0]
        line = next(l for l in fifth.splitlines() if l.startswith(f"| `{name}` | "))
        assert line.rstrip().endswith(f"| {got[0]} | {got[1]} |"), line
    assert {r["headword"]: r["vowels"] for r in saved} == {
        "ant": 5, "Asori": 2, "kisri": 3, "pelmos": 16, "perite": 5, "Pẖome": 8, "plsn": 1, "qelile": 5,
        "tewiseti": 1, "Wos": 192, "yirewke": 35, "Atri": 13, "Beke": 6}


def test_the_vowel_list_and_the_second_check():
    needs(*VOWEL_FILES, "data/sources/egyptian/out/check_vowels.json", "data/sources/egyptian/check_vowels_key.json",
          "data/sources/egyptian/check_key.json")
    rows = [json.loads(l) for l in (ROOT / VOWEL_FILES[2]).read_text(encoding="utf-8").splitlines()]
    assert E.PUBLIC_VOWELS.read_text(encoding="utf-8") == E.public_vowel_list(rows)
    lines = [l.split("\t") for l in E.PUBLIC_VOWELS.read_text(encoding="utf-8").splitlines()]
    assert len(lines) == 279 and all(c[6].startswith("ccl:") for c in lines[1:])
    meanings = {h["meaning"] for r in rows for h in r["vowels"]["hits"]} - {""}
    assert not meanings & {cell for c in lines[1:] for cell in c}
    # the second pack: the pieces that beat the bar with a best match the first checkers were not shown, and
    # six decoys
    key = json.loads((ROOT / "data/sources/egyptian/check_vowels_key.json").read_text(encoding="utf-8"))
    first = json.loads((ROOT / "data/sources/egyptian/check_key.json").read_text(encoding="utf-8"))
    needs("data/sources/egyptian/check/pack.jsonl", "data/sources/egyptian/check_vowels/pack.jsonl")
    shown = collections.defaultdict(set)
    for item in map(json.loads, (ROOT / "data/sources/egyptian/check/pack.jsonl").read_text(encoding="utf-8").splitlines()):
        shown[first[item["id"]]["piece"]] |= {h["id"] for h in item["candidates"]}
    low = {r["piece"]: r for r in rows
           if r["vowels"]["chance"] <= E.BAR and not (r["mentions_egyptian"] or r["spelled_like"])}
    unseen = {p for p, r in low.items() if r["vowels"]["hits"][0]["id"] not in shown[p]}
    assert (len(low), len(unseen)) == (13, 6)
    assert sorted(unseen) == ["lks", "mtr", "ponni", "ptri", "tereki", "tmNte"]
    assert {a["piece"] for a in key.values() if not a["decoy"]} == unseen
    assert sum(a["decoy"] for a in key.values()) == 6 and all(a["chance"] >= 0.5 for a in key.values() if a["decoy"])
    # every best match that beats the bar has been before a checker, in one pack or the other
    second = collections.defaultdict(set)
    for item in map(json.loads, (ROOT / "data/sources/egyptian/check_vowels/pack.jsonl").read_text(encoding="utf-8").splitlines()):
        second[key[item["id"]]["piece"]] |= {h["id"] for h in item["candidates"]}
    assert all(r["vowels"]["hits"][0]["id"] in shown[p] | second[p] for p, r in low.items())
    c = json.loads((ROOT / "data/sources/egyptian/out/check_vowels.json").read_text(encoding="utf-8"))
    assert (c["items"], c["best"], c["decoys"], c["answered_by_both"], c["same_verdict"]) == (12, 6, 6, 12, 12)
    for reader in ("reader1", "reader2"):
        assert c["readers"][reader] == {"answered": 12, "best": {"no": 6}, "decoys": {"no": 6}}
    assert c["fits_for_both"] == c["known_for_both"] == []
    flat = " ".join(PAGE.read_text(encoding="utf-8").split())
    for text in ("For seven of the 13, the first checkers had already been shown",
                 "`lks`, `mtr`, `ponni`, `ptri`, `tereki` and `tmNte`", 'for all 12: no new source, no decoy accepted'):
        assert text in flat, text


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
