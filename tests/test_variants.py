"""Checks for the search for spellings and forms of known words (src/variants.py).

  python3 -I tests/test_variants.py

Rilly's lexicon, the gloss file and the result files are local only, so the checks of the method run on a made-up
lexicon; the checks of the reported numbers need the local files and are skipped without them.
"""
import collections, contextlib, io, json, math, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import coverage as C   # noqa: E402
import egyptian as E   # noqa: E402
import lexique as L    # noqa: E402
import variants as V   # noqa: E402
from local_only import needs, run   # noqa: E402

PAGE = ROOT / "data/discovery/variants.md"
LOCAL = ("data/sources/variants/out/figures.json", "data/sources/variants/out/test.jsonl",
         "data/sources/variants/out/candidates.jsonl", "data/sources/variants/out/real.jsonl",
         "data/sources/variants/out/model.json")
WORDS = ("data/rilly2003", "data/corpus_v5.jsonl")
CHECKED = ("data/sources/variants/check_key.json", "data/sources/variants/out/check.json",
           "data/sources/variants/out/confirmed.jsonl", "data/sources/coverage/glosses.jsonl")


def raw(head, variants=(), meaning="a meaning", status="established", category="substantif", page=10, view=""):
    return {"headword": head, "variants": list(variants), "category": category, "meaning_en": meaning,
            "meaning_fr": "", "status": status, "rilly_view": view, "proposals": [], "rem": [], "page_pdf": page,
            "page_printed": page}


LEXICON = [raw("plsn", ["plsne"]), raw("pelmos", ["pelmes (?)", "plmos"]), raw("Amni", ["Mni", "Mn (peut-être)"]),
           raw("Mni", [], "Amun"), raw("tk (1)", ["tke"]), raw("tk (2)", ["tke"], status="hypothesis"),
           raw("-ke (2)", ["-k"], category="suffixe"), raw("perite"), raw("qore", ["qor"]), raw("mlo", ["mle"]),
           raw("zzz", ["zzy"], page=290), raw("Asori", ["Asori", "Sori"]), raw("mk", ["mke"]),
           raw("wide", [], "", "unknown", "", view="perhaps a variant of wi"), raw("at", [], "bread")]
ENDINGS = dict({s: 0 for s in L.SUFFIXES}, **{"": 40, "se": 5, "l": 5})


def pool():
    es = V.words(LEXICON)
    return es, V.units(es), *V.cases(es), V.ending_chances(ENDINGS)


def test_letter_strings():
    assert V.back("perite") == "etirep" and V.back("") == ""
    assert V.strings("anese") == {"0nes", "0nese"}             # the sign se, or s and e
    assert V.strings("Pẖome") == {"pXome"} and V.strings("ḫbḫl(i)") == {"xbxl", "xbxli"}
    assert V.strings("a[..]te") == set() and V.strings("Mit (?)") == {"mit"}
    assert all(c in V.LETTERS for s in ("abdeiklmnopqrstwxy", "ẖḫšñ") for x in V.strings(s) for c in x)


def test_the_starting_table_assumes_nothing():
    for e in V.LETTERS:
        row = V.flat(e)
        assert math.isclose(sum(row.values()), 1.0) and set(row) == set(V.LETTERS) | {""}, e
        assert row[e] == 0.80 and row[""] == 0.10
        assert len({p for m, p in row.items() if m not in (e, "")}) == 1        # every other letter alike
    # no letter is weaker than another, and none is nearer to one than to another
    assert V.flat("e")[""] == V.flat("t")[""] and V.flat("l")["r"] == V.flat("l")["p"] == V.flat("e")["i"]
    md = E.model(None, V.LETTERS, V.LETTERS, ("",), V.flat)
    stay = 1 - sum(math.exp(v) for v in md["add"].values())
    assert all(math.isclose(sum(math.exp(v) for v in md["out"][e].values()), stay) for e in V.LETTERS)
    assert md["article"] == {"": 0.0}


def test_the_egyptian_model_is_what_it_was():
    # the two arguments that this search added leave the search for Egyptian words as it was
    assert E.model() == E.model(None, E.MER, E.EGY, E.ARTICLES, E.neutral)
    assert list(E.model()["article"]) == list(E.ARTICLES)
    pairs = [("plms", ["lmS"]), ("0nt", ["hmnTr"])]
    assert E.train(pairs) == E.train(pairs, articles=E.ARTICLES, start=E.neutral)
    md = E.model()
    assert E.score("plsn", "lSn", md) > E.score("plsn", "lSn", dict(md, article={"": md["article"][""]}))
    assert E.align("plsn", "lSn", md)[0] == "p" and E.align("plsn", "lSn", dict(md, article={"": 0.0}))[0] == ""


def test_the_pool_is_the_words_of_the_lexicon_proper():
    es, us, pairs, items, _ = pool()
    assert len(es) == len(LEXICON) - 1 and "zzz" not in [e["headword"] for e in es]      # the appendix is left out
    by = {u["key"]: u for u in us}
    assert "ke" not in by                                                                 # an ending is no word
    assert by["tk"]["entries"] == ["tk (1)", "tk (2)"]                 # headwords spelled alike are one match
    assert by["tk"]["codes"] == sorted(["kt", "ekt"])                  # its strings, read from the end
    assert by["0mni"]["codes"] == sorted(["inm0", "inm", "nm"]) and by["mni"]["entries"] == ["Mni"]
    assert by["0sori"]["codes"] == sorted(["iros0", "iros"])           # a variant spelled like the headword adds nothing
    assert {e["headword"]: e["level"] for e in es}["tk (2)"] == "hypothesis"
    # every string of every match is in the search's letters
    assert all(c in V.LETTERS for u in us for code in u["codes"] for c in code)


def test_the_pairs_and_the_hidden_variants():
    es, us, pairs, items, _ = pool()
    # every listed variant that is not spelled like its headword trains the model, an ending's too
    assert {"letters": "k", "head": ["ke"], "entry": "-ke (2)"} in pairs
    assert not any(p["letters"] == "0sori" for p in pairs) and len(pairs) == 12
    by = {i["letters"]: i for i in items}
    # hidden in the test: variants of words, three letters or more, each spelling once
    assert set(by) == {"plsne", "pelmes", "plmos", "mni", "tke", "qor", "mle", "sori", "mke"}
    assert by["tke"]["owners"] == ["tk (1)", "tk (2)"] and by["tke"]["hidden"] == {"tke"}
    assert by["pelmes"]["uncertain"] and not by["plmos"]["uncertain"]
    assert "mn" not in by                                              # two letters: anything fits


def test_a_hidden_variant_is_hidden_everywhere():
    es, us, pairs, items, endings = pool()
    it = next(i for i in items if i["letters"] == "mni")
    left = {u["key"]: u for u in V.units(es, it["hidden"])}
    assert "mni" not in left                                           # the entry that has it as its headword goes
    assert left["0mni"]["codes"] == sorted(["inm0", "nm"])             # and its owner no longer lists it
    assert len(left) == len(us) - 1
    rest = V.without(pairs, it)
    assert len(rest) == len(pairs) - 1 and not any(p["letters"] == "mni" for p in rest)
    # the stricter test: the owner keeps none of its variants, and none of its pairs trains the model
    alone = {u["key"]: u for u in V.units(es, it["hidden"], {"Amni"})}
    assert alone["0mni"]["codes"] == ["inm0"]
    assert [p["entry"] for p in V.without(pairs, it, owners=True)].count("Amni") == 0
    # a pair whose headword is the hidden spelling goes too
    hid = {"letters": "x", "hidden": {"qore"}, "owners": []}
    assert not any(p["entry"] == "qore" for p in V.without(pairs, hid))


def test_the_alternations_are_counted_not_assumed():
    es, us, pairs, items, endings = pool()
    start = E.model(None, V.LETTERS, V.LETTERS, ("",), V.flat)
    md = V.trained(pairs, endings)
    # what the variants show is likelier than at the start: o written e, a final e left out or added
    assert md["out"]["o"]["e"] > start["out"]["o"]["e"] and md["out"]["e"][""] > start["out"]["e"][""]
    assert md["add"]["e"] > start["add"]["e"]
    # what they do not show is not: no pair has r for l, so it is no likelier than p for l
    assert math.isclose(md["out"]["l"]["r"], md["out"]["l"]["p"]) and md["out"]["l"]["r"] < start["out"]["l"]["r"]
    out, add, seen = V.counted(pairs, md)
    assert out["o", "e"] == 2 and out["e", ""] == 3 and add == {"e": 4} and out["0", ""] == 3
    assert seen["l"] == sum(k for (e, _), k in out.items() if e == "l")
    # the endings are the model's "articles", read from the end, the bare word first
    assert list(md["article"])[0] == "" and "es" in md["article"] and "iwol" in md["article"]
    assert math.isclose(sum(math.exp(v) for v in md["article"].values()), 1.0)
    assert md["article"][""] > md["article"]["es"] == md["article"]["l"] > md["article"]["iwol"]


def test_a_piece_is_an_entry_with_an_ending():
    es, us, pairs, items, endings = pool()
    md, trie = V.trained(pairs, endings), E.Trie(list(enumerate(us)))
    hit = V.found("peritese", us, trie, md)[0]
    assert (hit["entries"], hit["spelling"], hit["ending"], hit["differences"]) == (["perite"], "perite", "se", [])
    # its score is the ending's chance and every letter staying
    stay = sum(md["out"][c][c] for c in "peritese")
    assert math.isclose(hit["score"], md["article"]["es"] + stay)
    # a letter left out on top of the ending; the letters that differ come in the word's order
    hit = V.found("pertese", us, trie, md)[0]
    assert (hit["entries"], hit["ending"], hit["differences"]) == (["perite"], "se", [["i", ""]])
    hit = V.found("prsn", us, trie, md)[0]
    assert hit["entries"] == ["plsn"] and hit["differences"] == [["l", "r"]] and hit["ending"] == ""
    assert V.differs([["l", "r"], ["i", ""], ["", "e"]]) == "r for l, i dropped, e added"
    # the search gives what scoring every string of every match with every ending gives
    for word in ("prsn", "peritese", "0mn", "qorl", "tkelowi", "mlese"):
        best = max((max(E.score(V.back(word), c, md) for c in u["codes"]), -k) for k, u in enumerate(us))
        got = E.search(V.back(word), trie, md)[0]
        assert math.isclose(got[0], best[0]) and got[1] == -best[1], word
    # a piece that is a headword is not compared with itself
    assert V.found("tk", us, trie, md, top=1)[0]["entries"] == ["tk (1)", "tk (2)"]
    assert V.found("tk", us, trie, md, top=1, skip=["tk (1)", "tk (2)"])[0]["entries"] != ["tk (1)", "tk (2)"]


def test_the_place_of_a_hidden_variant():
    es, us, pairs, items, endings = pool()
    by = {i["letters"]: i for i in items}
    for letters, owner in (("plsne", "plsn"), ("mni", "Amni"), ("tke", "tk (1)"), ("qor", "qore")):
        it = by[letters]
        got = V.placed(it, V.units(es, it["hidden"]), V.trained(V.without(pairs, it), endings))
        assert got["place"] == 1 and owner in got["best"], letters
    # a tie with another match is a miss: two entries one letter away from the hidden spelling
    twins = V.words([raw("bete"), raw("bite")])
    it = {"letters": "bote", "owners": ["bete"], "hidden": {"bote"}}
    md = V.trained([], endings)
    got = V.placed(it, V.units(twins, it["hidden"]), md)
    assert got["place"] == 2 and got["of"] == 2
    # but the entries of one spelling are one match, so they do not tie with each other
    it = by["tke"]
    assert V.placed(it, V.units(es, it["hidden"]), md)["place"] == 1


def test_chance_against_made_up_words():
    es, us, pairs, items, endings = pool()
    md, trie = V.trained(pairs, endings), E.Trie(list(enumerate(us)))
    fake = E.made_up(sorted(u["key"] for u in us), n=20, seed=V.SEED, longest=6)
    assert sorted(fake) == [3, 4, 5, 6] and all(len(v) == 20 for v in fake.values())
    assert all(len(w) == k or (k == 6 and len(w) >= 6) for k, ws in fake.items() for w in ws)
    scores = V.yardstick(trie, md, fake)
    assert all(math.isclose(s, E.search(V.back(w), trie, md)[0][0]) for k in fake for w, s in zip(fake[k], scores[k]))
    # the share of made-up words of the word's length that do as well, the word counted in; the longest together
    assert V.chance(0.0, "abc", {3: [-1.0, -2.0, -3.0]}) == 0.25
    assert V.chance(-2.0, "abc", {3: [-1.0, -2.0, -3.0]}) == 0.75
    assert V.chance(-5.0, "abcdefgh", {3: [0.0], 6: [-9.0, -9.0, -1.0]}) == 0.5
    assert V.made_up(us).keys() == set(range(V.SHORTEST, V.LONGEST + 1)) and len(V.made_up(us)[5]) == V.MADE_UP


def test_the_real_words_of_the_second_yardstick():
    es, us, pairs, items, endings = pool()
    md, trie = V.trained(pairs, endings), E.Trie(list(enumerate(us)))
    scores = V.yardstick(trie, md, E.made_up(sorted(u["key"] for u in us), n=20, seed=V.SEED, longest=6))
    got = V.real_words(es, us, trie, md, scores)
    # only a word with an accepted meaning that lists no variant and shares no spelling: perite
    assert [r["headword"] for r in got] == ["perite"]
    assert got[0]["best"] != ["perite"] and 0 < got[0]["chance"] <= 1


def test_the_lexicon_s_own_links():
    es = {e["headword"]: e for e in V.words(LEXICON + [raw("wi", [], "brother"), raw("are", [], "to take")])}
    assert V.names("perhaps a variant of wi", "wi") and V.names("see pẖo", "pẖo")
    assert not V.names("they are priests of mk", "are")               # an English word, and no word that sends on
    assert not V.names("a title of the cult", "at") and not V.names("variant of wide", "wi")
    assert not V.names("variant of ḫr at Arminna", "at") and V.names("variant of ḫr at Arminna", "ḫr")
    assert V.names("name of the queen, a variant of the more frequent spelling Mnitore", "Mnitore")
    assert V.names("probably a variant of the title tqi", "tqi") and V.names("a variant (?) of mte", "mte")
    assert V.names("a variant in REM 0234, 0249 and 0259 of ant 'priest'", "ant")
    assert V.names("perhaps the same lexeme as the adjective mẖe or mẖo (1)", "mẖe")
    assert V.linked("wide", {"entries": ["wi"]}, es)                   # the entry sends to its match
    assert V.linked("Mni", {"entries": ["Amni"]}, es)                  # the match lists the piece's spelling
    assert not V.linked("perite", {"entries": ["plsn"]}, es)
    assert not V.linked("prSn", {"entries": ["plsn"]}, es)             # letters are no headword


def texts_of(*rows):
    """A gloss file of made-up texts: each row is (id, [(form, level, gloss, parts)])."""
    return [{"id": i, "text": " ".join(w[0] for w in ws),
             "glosses": [{"form": f, "level": lv, "gloss": gl, "kind": "", "by": "analyst",
                          "parts": [{"form": pf, "entry": pe} for pf, pe in parts]} for f, lv, gl, parts in ws]}
            for i, ws in rows]


TEXTS = texts_of(
    ("T1", [("ant", "meaning", "priest", [("ant", "at")]), ("prSn", "unknown", "a guess", [("prSn", "?")]),
            ("Mnp", "name", "Amanap", [("Mnp", "NAME")])]),
    ("T2", [("prSn", "unknown", "another guess", [("prSn", "?")]), ("qore", "meaning", "ruler", [("qore", "qore")])]),
    ("T3", [("plSn", "meaning", "administrator / steward", [("plSn", "plsn")]), ("xyz", "unknown", "", [("xyz", "?")]),
            ("prSnli", "unknown", "", [("prSn", "?"), ("li", "ending")])]))


def test_the_contexts_do_not_show_a_guess():
    heads = C.index(C.lexicon(LEXICON))[2]
    at = V.places(TEXTS, heads)
    assert at["prSn", False] == [(0, 1), (1, 0), (2, 2)] and at["xyz", False] == [(2, 1)]
    got = V.contexts(at["prSn", False], TEXTS)
    assert [c["text"] for c in got] == ["T1", "T2", "T3"]
    assert got[0] == {"text": "T1", "words": "ant [prSn] Mnp", "glosses": "priest / ? / Amanap"}
    assert got[1]["glosses"] == "? / ruler"                            # the piece's own word shows no gloss
    assert all("guess" not in c["glosses"] for c in got)
    assert len(V.contexts(at["prSn", False], TEXTS, n=2)) == 2
    # a candidate's own contexts keep their glosses: its meaning is in the pack anyway
    spots = V.stands({"plSn"}, TEXTS)
    assert spots == [(2, 0)]
    # one gloss a word, also for a gloss that names two senses
    assert V.contexts(spots, TEXTS, masked=False)[0]["glosses"] == "administrator; steward / ? / ?"


def result(piece, chance, entries, headword=False, linked=False):
    return {"piece": piece, "headword": headword, "kind": "title", "level": "unknown", "texts": 2, "words": 3,
            "letters": piece.lower(), "chance": chance, "linked": linked, "accepted": True,
            "hits": [{"entries": entries, "key": entries[0], "spelling": entries[0], "ending": "", "score": -1.0,
                      "differences": [["l", "r"]]}]}


def test_every_match_that_beats_the_bar_goes_to_the_checkers():
    rows = ([result(f"good{k}", 0.001 + k / 1000, ["plsn"]) for k in range(30)]
            + [result("edge", V.BAR, ["plsn"], headword=True, linked=True)]
            + [result(f"mid{k}", 0.2, ["plsn"]) for k in range(10)]
            + [result(f"poor{k}", 0.5 + k / 100, ["plsn"]) for k in range(40)]
            + [{"piece": "ab", "headword": False, "kind": "", "level": "unknown", "texts": 1, "words": 1, "letters": "ab"}])
    test = [{"letters": f"v{k}", "listed": {"chance": 0.01 if k % 2 else 0.3}} for k in range(40)]
    best, known, _ = V.pack_draw(rows, test)
    # every searched piece at the bar or under it, set aside or not, and nothing else
    assert {r["piece"] for r in best} == {f"good{k}" for k in range(30)} | {"edge"}
    # the hidden variants, every one, in an order that is the same every time and not the file's
    assert sorted(r["letters"] for r in known) == sorted(r["letters"] for r in test)
    assert [r["letters"] for r in known] == [r["letters"] for r in V.pack_draw(rows, test)[1]]
    assert [r["letters"] for r in known] != sorted(r["letters"] for r in test)


def test_the_items_whose_answer_is_known():
    lex = [raw("pelmos", ["polmos"]), raw("pelmes"), raw("sleqene", ["sleqel"]), raw("sleqete"), raw("sleqe"),
           raw("yetmde", ["yetmd"]), raw("tereki", ["terek"]), raw("asente", [], "see snte"), raw("snte", ["sente"])]
    es = V.words(lex)
    pairs, items = V.cases(es)
    texts = texts_of(("T1", [("polmoS", "meaning", "general", [("polmoS", "pelmos")]), ("x", "unknown", "", [("x", "?")])]),
                     ("T2", [("Sleqel", "meaning", "a title", [("Sleqel", "sleqene")])]),
                     ("T3", [("Sente", "meaning", "a title", [("Sente", "snte")]), ("x", "unknown", "", [("x", "?")])]))
    rows = [{"letters": i["letters"], "listed": {"chance": 0.01 if i["letters"] == "polmos" else 0.2}} for i in items]
    made = {m["letters"]: m for m in V.known_items(rows, items, es, pairs, V.ending_chances(ENDINGS), texts)}
    # a variant that does not stand in the texts is no item (yetmd, terek); nor is one with four letters as a decoy
    assert set(made) == {"polmos", "sleqel", "sente"}
    # the control keeps its candidates: the entry that lists it is the first
    c = made["polmos"]
    assert c["what"] == "control" and c["piece"] == "polmoS" and c["owners"] == ["pelmos"] and c["texts"] == 1
    assert c["hits"][0]["entries"] == ["pelmos"] and c["hide"] == {"polmoS"} and c["spots"] == [(0, 0)]
    # the decoy has it taken out, with every entry the lexicon links with it: only look-alikes are left
    d = made["sleqel"]
    assert d["what"] == "decoy" and d["owners"] == ["sleqene"]
    assert sorted(h["entries"] for h in d["hits"][:2]) == [["sleqe"], ["sleqete"]]
    assert not any("sleqene" in h["entries"] for h in d["hits"])
    d = made["sente"]
    assert d["what"] == "decoy" and not any(set(h["entries"]) & {"snte", "asente"} for h in d["hits"])
    assert len(d["hits"]) == V.TOP


def test_the_public_list_holds_forms_and_no_gloss():
    rows = [result("prSn", 0.002, ["plsn"]), result("tke", 0.3, ["tk (1)", "tk (2)"], headword=True, linked=True),
            {"piece": "ab", "headword": False, "kind": "", "level": "unknown", "texts": 1, "words": 1, "letters": "ab"}]
    rows[1]["hits"][0].update(ending="se", differences=[])
    lines = V.public_list(rows).splitlines()
    assert lines[0].split("\t") == V.HEAD and len(lines) == 3          # a piece too short to search is not listed
    assert lines[1].split("\t") == ["prSn", "letters", "title", "2", "prsn", "0.0020", "plsn", "plsn", "", "r for l",
                                    "yes", "no"]
    assert lines[2].split("\t")[6:] == ["tk (1) / tk (2)", "tk (1)", "-se", "", "yes", "yes"]


def merged(key, answers, packs):
    """Run check_merge on a made-up key, packs and answers in a temporary folder; give back check.json's content,
    the confirmed rows and the public list."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        old = V.HERE, V.OUT, V.CHECK, V.KEYFILE, V.CONFIRMED, V.moved
        V.HERE, V.OUT, V.CHECK, V.KEYFILE, V.CONFIRMED = tmp, tmp / "out", tmp / "check", tmp / "key.json", tmp / "c.tsv"
        V.moved = lambda confirmed: {"confirmed": len(confirmed)}
        try:
            V.OUT.mkdir()
            V.KEYFILE.write_text(json.dumps(key))
            for name, items in packs.items():
                (V.CHECK / name).mkdir(parents=True)
                (V.CHECK / name / "pack.jsonl").write_text("".join(json.dumps(x) + "\n" for x in items))
                for reader, lines in answers.get(name, {}).items():
                    (V.CHECK / name / f"{reader}.jsonl").write_text("\n".join(lines) + "\n")
            with contextlib.redirect_stdout(io.StringIO()):
                V.check_merge()
            out = json.loads((V.OUT / "check.json").read_text())
            rows = [json.loads(l) for l in (V.OUT / "confirmed.jsonl").read_text().splitlines()]
            return out, rows, V.CONFIRMED.read_text() if V.CONFIRMED.exists() else ""
        finally:
            V.HERE, V.OUT, V.CHECK, V.KEYFILE, V.CONFIRMED, V.moved = old


def test_the_checkers_answers_are_read_against_the_key():
    def item(i, what, piece, owners=()):
        return {"piece": piece, "headword": False, "what": what, "chance": 0.01, "best": ["plsn"],
                "owners": list(owners), "linked": False}

    key = {"V001": item(1, "best", "prSn"), "V002": item(2, "best", "tkel"), "V003": item(3, "decoy", "xyz"),
           "V004": item(4, "control", "mni", ["Amni"]), "V005": item(5, "best", "bete"), "V006": item(6, "best", "qr")}
    cands = [{"entries": [{"headword": "plsn"}]}, {"entries": [{"headword": "tk (1)"}, {"headword": "tk (2)"}]},
             {"entries": [{"headword": "Amni"}]}]
    packs = {"pack01": [{"id": i, "candidates": cands} for i in ("V001", "V002", "V003")],
             "pack02": [{"id": i, "candidates": cands} for i in ("V004", "V005", "V006")]}
    ans = lambda i, v, c="": json.dumps({"id": i, "verdict": v, "candidate": c, "confidence": 4, "reason": "r"})   # noqa: E731
    answers = {"pack01": {"reader1": [ans("V001", "same", "plsn"), ans("V002", "same", "tk (1)"), ans("V003", "no"),
                                      "not json", ans("V001", "no"), ans("V999", "same", "plsn")],
                          "reader2": [ans("V001", "same", "plsn"), ans("V002", "same", "tk (2)"), ans("V003", "no")]},
               "pack02": {"reader1": [ans("V004", "same", "Amni"), ans("V005", "same", "plsn"), ans("V006", "other", "qore")],
                          "reader2": [ans("V004", "same", "Amni"), ans("V005", "same", "Amni"), ans("V006", "other", "qore"),
                                      ans("V006", "maybe")]}}
    out, rows, public = merged(key, answers, packs)
    assert (out["items"], out["best"], out["decoy"], out["control"]) == (6, 4, 1, 1)
    r1 = out["readers"]["reader1"]
    assert r1["answered"] == 6 and r1["best"] == {"same": 3, "other": 1} and r1["decoy"] == {"no": 1}
    assert r1["controls_right"] == 1 and out["controls_right_for_both"] == 1
    assert out["answered_by_both"] == 6 and out["same_verdict"] == 6
    # confirmed: both say `same` and name entries of one candidate; two homonyms of one match count, two
    # different matches do not
    assert out["same_for_both"] == {"best": 2, "decoy": 0, "control": 1} and out["confirmed"] == 2
    assert [(r["piece"], r["entries"]) for r in rows] == [("prSn", ["plsn"]), ("tkel", ["tk (1)", "tk (2)"])]
    assert out["same_for_both_but_another_candidate"] == ["V005"]
    assert out["other_for_both"] == [{"id": "V006", "piece": "qr", "what": "best", "candidates": ["qore", "qore"]}]
    lines = public.splitlines()
    assert len(lines) == 3 and lines[1].split("\t")[:3] == ["prSn", "letters", "plsn"]
    assert lines[2].split("\t")[2] == "tk (1) / tk (2)"
    # one checker alone confirms nothing
    out, rows, _ = merged(key, {"pack01": {"reader1": answers["pack01"]["reader1"]}}, packs)
    assert out["confirmed"] == 0 and rows == [] and "same_verdict" not in out
    # a headword named without its number or its capital names every entry of the one candidate spelled so
    groups = [["plsn"], ["tk (1)", "tk (2)"], ["Amni"], ["Ar (1)", "ar (2)"]]
    assert V.which("tk (2)", groups) == (1, ["tk (2)"]) and V.which("tk", groups) == (1, ["tk (1)", "tk (2)"])
    assert V.which(" amni ", groups) == (2, ["Amni"]) and V.which("ar", groups) == (3, ["Ar (1)", "ar (2)"])
    assert V.which("qore", groups) == (None, []) and V.which("", groups) == (None, []) and V.which(None, groups) == (None, [])
    assert V.which("tk", groups + [["tk (5)"]]) == (None, [])           # two candidates spelled so: no telling
    loose = {"pack01": {"reader1": [ans("V001", "same", "PLSN"), ans("V002", "same", "tk")],
                        "reader2": [ans("V001", "same", "plsn"), ans("V002", "same", "tk (2)")]},
             "pack02": {"reader1": [ans("V004", "same", "amni")], "reader2": [ans("V004", "same", "Mni")]}}
    out, rows, _ = merged(key, loose, packs)
    assert [(r["piece"], r["entries"]) for r in rows] == [("prSn", ["plsn"]), ("tkel", ["tk (1)", "tk (2)"])]
    assert out["readers"]["reader1"]["controls_right"] == 1 and out["readers"]["reader2"]["controls_right"] == 0


def test_what_the_confirmed_list_would_move():
    lex = LEXICON + [raw("xyz", [], "", "unknown", "titre")]
    confirmed = [{"piece": "prSn", "headword": False, "entries": ["plsn", "plsn"]},
                 {"piece": "xyz", "headword": True, "entries": ["tk (1)", "tk (2)"]}]
    texts = texts_of(
        ("T1", [("ant", "meaning", "priest", [("ant", "at")]), ("prSn", "unknown", "", [("prSn", "?")])]),
        ("T2", [("prSnli", "unknown", "", [("prSn", "?"), ("li", "ending")]), ("abc", "unknown", "", [("abc", "?")])]),
        ("T3", [("prSnabc", "unknown", "", [("prSn", "?"), ("abc", "?")]), ("xyz", "kind", "", [("xyz", "xyz")]),
                ("lost.", "lost", "", [])]))
    got = V.moved(confirmed, texts, lex)
    # prSn is confirmed as a word with an accepted meaning; xyz as tk, and tk (2) is a proposal only
    assert (got["confirmed"], got["with_an_accepted_meaning"]) == (2, 1)
    assert [c["accepted"] for c in confirmed] == [True, False]
    # a word moves when every piece that blocks it is confirmed: prSn and prSnli, not prSnabc
    assert (got["words"], got["all_words"], got["translated_now"]) == (2, 7, 1) and got["by_piece"] == {"prSn": 2}
    assert got["texts_completed_once"] == 1                            # T1 is complete then; T2 still lacks abc
    assert (got["words_once"], got["all_words_once"]) == (2, 7)


def test_an_accepted_meaning_follows_the_entry_it_sends_to():
    lex = [raw("Wos", ["Wis"], "Isis"), raw("Wis", [], "Isis (variant of Wos)"),
           raw("wetne", ["qetne"], "an epithet", "hypothesis"), raw("qetne", [], "variant of wetne"),
           raw("kr", [], "variant of ḫr at Arminna"), raw("ḫr", ["kr"], "to feed (?)", "hypothesis"),
           raw("at", [], "bread"), raw("lone", [], "a variant of something the lexicon does not have")]
    got = {e["headword"]: e["accepted"] for e in V.words(lex)}
    assert got["Wos"] and got["Wis"]                       # a variant of a word with an accepted meaning
    assert not got["wetne"] and not got["qetne"]           # "established" as a variant of a proposal
    assert not got["kr"] and got["at"]                     # sends to ḫr, not to the English word in "at Arminna"
    assert got["lone"]                                     # sends nowhere the lexicon has: its level stands
    # two entries that only send to each other are not accepted
    ring = [{"headword": h, "level": "meaning", "sends": True, "head": {h}, "listed": [], "meaning": f"variant of {o}"}
            for h, o in (("loop", "pool"), ("pool", "loop"))]
    V.accept(ring)
    assert [e["accepted"] for e in ring] == [False, False]


def test_the_made_up_words_that_are_an_entry():
    es, us, pairs, items, endings = pool()
    fake = {3: ["mlo", "mle", "0mn", "xyz"], 4: ["qore", "mlol", "tkse", "zzzz"]}
    assert V.letter_for_letter(us, fake) == {3: [2, 2, 4], 4: [1, 3, 4]}       # mlo, mle; qore, and mlo-l, tk-se
    # more than a thousand tries: the sum of egyptian.as_many no longer fits a float, this one does
    for k, n in ((22, 383), (26, 383), (13, 241), (0, 10), (5, 5), (3, 64)):
        assert math.isclose(V.as_many(k, n), E.as_many(k, n), rel_tol=1e-9), (k, n)
    assert V.as_many(0, 1200) == 1.0 and 0.4 < V.as_many(60, 1200) < 0.6 and V.as_many(300, 1200) < 1e-100
    assert V.as_many(82, 1140) < 0.001 < V.as_many(70, 1140)


def test_the_made_up_scores_are_kept_with_their_fingerprint():
    es, us, pairs, items, endings = pool()
    md, trie = V.trained(pairs, endings), E.Trie(list(enumerate(us)))
    fake = E.made_up(sorted(u["key"] for u in us), n=5, seed=V.SEED, longest=5)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "yardstick.json"
        first = V.kept_yardstick(us, trie, md, fake, path)
        assert first == V.yardstick(trie, md, fake) and path.exists()
        kept = json.loads(path.read_text())
        # read back while the pool, the model and the words are the same
        path.write_text(json.dumps(dict(kept, scores={k: [0.0] * len(v) for k, v in kept["scores"].items()})))
        assert V.kept_yardstick(us, trie, md, fake, path) == {k: [0.0] * 5 for k in fake}
        # and searched again when one of them changed
        other = V.trained(pairs[:-1], endings)
        assert V.kept_yardstick(us, trie, other, fake, path) == V.yardstick(trie, other, fake)
        assert json.loads(path.read_text())["fingerprint"] != kept["fingerprint"]
        assert V.kept_yardstick(us[:-1], E.Trie(list(enumerate(us[:-1]))), other, fake, path) != {}
        assert json.loads(path.read_text())["fingerprint"] not in (kept["fingerprint"],)


def test_a_hidden_variant_s_own_chance():
    # the made-up words searched as the variant itself is: in the pool without it, with the model without it
    es, us, pairs, items, endings = pool()
    fake = E.made_up(sorted(u["key"] for u in us), n=30, seed=V.SEED, longest=6)
    it = next(i for i in items if i["letters"] == "plsne")
    left, md = V.units(es, it["hidden"]), V.trained(V.without(pairs, it), endings)
    scores = V.yardstick(E.Trie(list(enumerate(left))), md, fake)
    assert V.own_chance(it, es, pairs, endings, fake) == V.chance(V.placed(it, left, md)["score"], "plsne", scores)


def test_a_candidate_as_the_checker_sees_it():
    es, us, pairs, items, endings = pool()
    by_head = {e["headword"]: e for e in es}
    md = V.trained(pairs, endings)
    hit = V.found("prsnse", us, E.Trie(list(enumerate(us))), md)[0]
    got = V.shown(hit, by_head, V.counted(pairs, md), TEXTS)
    assert got["entries"] == [{"headword": "plsn", "kind": "noun", "status": "established", "accepted": True,
                               "meaning": "a meaning"}]
    assert (got["spelling"], got["ending"]) == ("plsn", "-se")
    assert got["differences"] == [{"what": "r for l", "in the listed variants": "0 of 4 l"}]
    assert [c["text"] for c in got["contexts"]] == ["T3"] and got["contexts"][0]["glosses"].startswith("administrator")
    # a control's own spelling is not shown among its candidate's places
    assert V.shown(hit, by_head, V.counted(pairs, md), TEXTS, hide={"plSn"})["contexts"] == []
    added = V.shown(V.found("plsnee", us, E.Trie(list(enumerate(us))), md)[0], by_head, V.counted(pairs, md), TEXTS)
    assert {"what": "e added", "in the listed variants": "4 added"} in added["differences"]


# ------------------------------------------------------------------------- the reported numbers (local files)

def figures():
    needs(*LOCAL)
    return json.loads((ROOT / LOCAL[0]).read_text(encoding="utf-8"))


def lines(k):
    needs(*LOCAL)
    return [json.loads(l) for l in (ROOT / LOCAL[k]).read_text(encoding="utf-8").splitlines()]


def page():
    """The page as one line, without the marks of bold and code, so that a phrase is found across line ends."""
    return " ".join(PAGE.read_text(encoding="utf-8").replace("**", "").replace("`", "").split())


def table(after):
    """The rows under the head of the table whose head starts with a phrase of the page, as lists of cells."""
    text = PAGE.read_text(encoding="utf-8")
    rows = text[text.index(after):].split("\n|", 1)[1].split("\n\n", 1)[0].splitlines()
    return [[c.strip().replace("**", "").replace("`", "") for c in ("|" + r if k else "|" + r).strip("|").split("|")]
            for k, r in enumerate(rows) if not set(r) <= set("|- ")]


def number(cell):
    """The first number of a table cell: "187 (77%)" is 187, "1,140" is 1140."""
    return int(re.match(r"[\d,]+", cell).group().replace(",", ""))


def test_reported_pool_and_bar():
    fig, text = figures(), page()
    assert fig["pool"] == {"entries": 804, "words": 688, "matches": 655, "letter_strings": 1067} and fig["pairs"] == 307
    assert "804 entries: 688 words and 116 endings" in text and "655 matches with 1,067 letter strings" in text
    assert "which leaves 307 pairs" in text and "268 under words and 39 under" in text
    # the bar is the one written down before the first run, and the page reports the result against it
    assert (V.FOUND, V.STANDS_OUT, V.BAR, V.MADE_UP, V.SHORTEST) == (2 / 3, 1 / 2, 0.05, 1000, 3)
    t = fig["test"]["all"]
    assert (t["hidden"], t["best_match"], t["among_three"], t["beats_the_bar"], t["best_match_and_beats_the_bar"]) \
        == (242, 187, 232, 118, 105)
    assert fig["bar"] == {"found": 0.6667, "stands_out": 0.5, "found_reached": True, "stands_out_reached": False}
    assert (math.ceil(V.FOUND * 242), math.ceil(V.STANDS_OUT * 242)) == (162, 121)
    assert "The test missed its bar." in text and "part 1 needed 162 and has 187, so it is reached" in text
    assert "Part 2 needed 121 and has 105, so it is not reached" in text
    assert "187 of the 242 hidden variants back to their own entry as the single best match (77%" in text
    assert "only 105 of the 242 (43%)" in text and round(100 * 187 / 242) == 77 and round(100 * 105 / 242) == 43
    assert "232 of the 242 (96%)" in text and "105 times in 118 (89%)" in text and round(100 * 105 / 118) == 89
    m = fig["test"]["misses"]
    assert m == {"all": 55, "to_a_linked_entry_or_a_tie": 24, "beat_the_bar": 13,
                 "beat_the_bar_to_a_linked_entry_or_a_tie": 12}
    assert "The 55 misses. 24 went to an entry" in text and "12 of the other 13 went to an entry" in text
    long = [fig["test"]["by_length"][k] for k in V.LENGTHS[1:]]
    assert (sum(x["hidden"] for x in long), sum(x["best_match_and_beats_the_bar"] for x in long)) == (149, 105)
    assert "105 of 149 hidden variants come back and stand out (70%)" in text


def test_the_page_s_table_of_the_test_is_the_result_file():
    fig = figures()["test"]
    rows = table("| Hidden variants |")
    want = [("All", fig["all"]), ("3 or 4 letters", fig["by_length"]["3 or 4 letters"]),
            ("5 or 6 letters", fig["by_length"]["5 or 6 letters"]),
            ("7 letters or more", fig["by_length"]["7 letters or more"]),
            ("Marked as uncertain by Rilly (mle (?))", fig["uncertain"]), ("Not marked", fig["sure"]),
            ("Stricter: the entry's other variants hidden too", fig["strict"])]
    assert len(rows) == len(want)
    for row, (name, f) in zip(rows, want):
        assert row[0] == name, row
        assert [number(c) for c in row[1:]] == [f["hidden"], f["best_match"], f["among_three"], f["beats_the_bar"],
                                                f["best_match_and_beats_the_bar"]], row
    # the result file adds up to the figures
    test = lines(1)
    assert V.tally(test, "listed") == fig["all"] and V.tally(test, "strict") == fig["strict"]
    assert sum(r["uncertain"] for r in test) == 26 and len({r["letters"] for r in test}) == 242
    assert all(len(r["letters"]) >= V.SHORTEST for r in test)
    assert "178 of 242 (74%)" in page() and round(100 * 178 / 242) == 74


def test_the_hidden_test_gives_the_reported_places():
    needs(*LOCAL, *WORDS, "data/sources/variants/out/yardstick.json")
    entries = V.words()
    pairs, items = V.cases(entries)
    endings = V.ending_chances(V.ending_counts())
    scores = {int(k): v for k, v in json.loads((ROOT / "data/sources/variants/out/yardstick.json").read_text())["scores"].items()}
    assert sorted(scores) == list(range(3, 13)) and all(len(v) == V.MADE_UP for v in scores.values())
    reported = {r["letters"]: r for r in lines(1)}
    assert set(reported) == {i["letters"] for i in items}
    for it in items[::6]:                                      # every sixth hidden variant, with its own model
        for name, strict in (("listed", False), ("strict", True)):
            got = V.placed(it, V.units(entries, it["hidden"], set(it["owners"]) if strict else frozenset()),
                           V.trained(V.without(pairs, it, strict), endings))
            want = reported[it["letters"]][name]
            assert (got["place"], got["best"], got["of"]) == (want["place"], want["best"], want["of"]), it["letters"]
            assert math.isclose(got["score"], want["score"]), it["letters"]
            assert math.isclose(V.chance(got["score"], it["letters"], scores), want["chance"]), it["letters"]
    # the hidden spelling is nowhere in its pool, and its owners are
    for it in items[::6]:
        us = V.units(entries, it["hidden"])
        assert not any(V.back(c) in it["hidden"] for u in us for c in u["codes"]), it["letters"]
        assert all(any(o in u["entries"] for u in us) for o in it["owners"]), it["letters"]


def test_the_test_s_shortcut_on_three_hidden_variants():
    # the reported chance takes the made-up words' scores from the whole pool; searched as the variant itself is,
    # they give the same within a few made-up words (the page reports a sample of 30)
    needs(*LOCAL, *WORDS)
    entries = V.words()
    pairs, items = V.cases(entries)
    endings = V.ending_chances(V.ending_counts())
    fake = V.made_up(V.units(entries))
    reported = {r["letters"]: r["listed"]["chance"] for r in lines(1)}
    for it in [i for i in sorted(items, key=lambda i: i["letters"]) if len(i["letters"]) == 5][:3]:
        assert abs(V.own_chance(it, entries, pairs, endings, fake) - reported[it["letters"]]) <= 0.005, it["letters"]


def test_what_the_model_counted_from_the_variants():
    needs(*LOCAL, *WORDS)
    model = json.loads((ROOT / LOCAL[4]).read_text(encoding="utf-8"))
    entries = V.words()
    pairs, _ = V.cases(entries)
    counts = V.ending_counts()
    out, add, seen = V.counted(pairs, V.trained(pairs, V.ending_chances(counts)))
    assert model["pairs"] == len(pairs) == 307 and model["letters"] == sum(seen.values()) == 1484
    assert model["added"] == sum(add.values()) == 132 and model["endings"] == counts
    assert {(e, m): k for e, m, k in model["out"]} == {k: v for k, v in out.items() if k[0] != k[1]}
    assert dict(map(tuple, model["add"])) == dict(add) and model["seen"] == dict(seen)
    # the page's table: (the headword's letter, the variant's letter or "" for left out, or None for added)
    rows = table("| The variant has |")
    want = [("e", ""), (None, "e"), ("0", ""), (None, "0"), ("i", "e"), ("e", "o"), (None, "i"), ("i", ""),
            ("e", "i"), ("y", "0"), ("o", "e"), ("o", ""), ("o", "i"), ("n", "l"), ("s", "t"), ("d", "t"), ("w", "q"),
            ("x", "k")]
    assert len(rows) == len(want)
    for row, (e, m) in zip(rows, want):
        times, of = number(row[1]), number(row[2])
        assert (times, of) == ((add[m], 132) if e is None else (out[e, m], seen[e])), row
    # the table holds every change counted four times or more, and the rarer ones the text names are right
    often = {(e, m) for (e, m), k in out.items() if e != m and k >= 5} | {(None, m) for m, k in add.items() if k >= 19}
    assert often <= set(want)
    assert not any(k for (e, m), k in out.items() if (e, m) in (("l", "r"), ("r", "l"), ("l", "t")))
    assert (seen["l"], seen["r"]) == (64, 89)
    text = page()
    assert "(64 l and 89 r in the headwords)" in text
    vowels = sum(k for (e, m), k in out.items() if e in "eio" and m in ("e", "i", "o") and e != m)
    assert (out["e", ""] + add["e"], vowels, out["0", ""] + add["0"]) == (133, 73, 42)
    assert "(133 times in 307 variants)" in text and "stand for one another (73 times)" in text and "Mni: 42 times" in text
    # the endings
    assert sum(counts.values()) == 654 and counts[""] == 402 and len(counts) == 26
    named = {"l": 34, "li": 27, "lowi": 24, "te": 22, "lo": 20, "leb": 16, "se": 15}
    assert all(counts[k] == v for k, v in named.items()) and 654 - 402 - sum(named.values()) == 94
    assert ("402 are bare, 34 have -l, 27 -li, 24 -lowi, 22 -te, 20 -lo, 16 -leb, 15 -se and the other 17 endings "
            "94 together") in text


def test_reported_search_of_the_pieces():
    fig, text = figures(), page()
    u = fig["unknown"]
    rows = lines(2)
    searched = [r for r in rows if "hits" in r]
    new = [r for r in searched if not r["linked"]]
    under = [r for r in new if r["chance"] <= V.BAR]
    assert (len(rows), len(searched), len(new), len(under)) == (1336, 1210, 1140, 82)
    assert (u["pieces"], u["searched"], u["too_short"], u["linked_by_the_lexicon"], u["new"], u["at_most_0.05"]) \
        == (1336, 1210, 126, 70, 1140, 82)
    short = [r for r in rows if "hits" not in r]
    assert (sum(not r["letters"] for r in short), sum(0 < len(r["letters"]) < 3 for r in short)) == (2, 124)
    assert "126 were not searched: 124 have one or two letters" in text and "and 2 hold a digit or a lost sign" in text
    assert (sum(not r["headword"] for r in searched), sum(r["headword"] for r in searched)) == (963, 247)
    assert "963 are letters that no entry explains and 247 are headwords" in text
    assert all(not r["linked"] for r in searched if not r["headword"])
    assert u["under_the_bar"] == {"headwords": 12, "letters": 70, "match_has_an_accepted_meaning": 46,
                                  "with_an_ending": 43, "linked_and_under_the_bar": 23}
    assert sum(r["chance"] <= V.BAR for r in searched) == 82 + 23 == 105
    assert "Set aside: 70 headwords" in text and "23 of them beat the bar" in text
    assert "70 are letters and 12 are headwords; 43 would carry an ending; for 46 the best match" in text
    assert u["words_they_stand_in"] == sum(r["words"] for r in under) == 375 and "stand in 375 running words" in text
    # against the made-up words
    assert u["expected_by_chance"] == 57.0 and math.isclose(u["as_many_by_chance"], V.as_many(82, 1140))
    assert round(100 * u["as_many_by_chance"], 2) == 0.08 and "chance alone gives as many 0.08% of the time" in text
    assert u["passing_q_0.2"] == E.passing([r["chance"] for r in new]) == 0
    assert u["fewest_at_the_smallest_chance_to_pass"] == E.fewest_to_pass(1140, made=V.MADE_UP) == 6
    assert u["smallest_chance"] == round(1 / 1001, 6) and "six pieces at the smallest chance there is, 1 in 1,001" in text
    # the table by length: searched, under the bar, 5% of the searched, and the real words' rate
    real = fig["real_words"]["by_length"]
    table_rows = table("| The other 1,140 pieces |")
    total = [0, 0, 0, 0]
    for row, k in zip(table_rows, V.LENGTHS):
        b = u["by_length"][k]
        rate = round(b["searched"] * real[k]["at_most_0.05"] / real[k]["words"])
        want = [b["searched"], b["at_most_0.05"], round(V.BAR * b["searched"]), rate]
        assert row[0] == k and [number(c) for c in row[1:]] == want, row
        total = [a + b for a, b in zip(total, want)]
    assert table_rows[3][0] == "All" and [number(c) for c in table_rows[3][1:]] == total == [1140, 82, 57, 104]
    assert "82 where 57 are expected" in text and "would give about 104, more than the 82 found" in text
    # each chance is the piece's best score among the kept scores of the made-up words
    needs("data/sources/variants/out/yardstick.json")
    scores = {int(k): v for k, v in json.loads((ROOT / "data/sources/variants/out/yardstick.json").read_text())["scores"].items()}
    assert all(math.isclose(r["chance"], V.chance(r["hits"][0]["score"], r["letters"], scores)) for r in searched)
    assert all(len(r["hits"]) == V.TOP and r["hits"][0]["score"] >= r["hits"][-1]["score"] for r in searched)


def test_reported_yardsticks():
    fig, text = figures(), page()
    made = fig["made_up"]
    assert made["of_each_length"] == 1000
    assert [made["letter_for_letter"][k] for k in ("3", "4", "5", "6")] == [[350, 467, 1000], [63, 244, 1000],
                                                                            [18, 100, 1000], [1, 27, 1000]]
    assert "Of 1,000 made-up words of three letters, 350 are a spelling of the lexicon letter for letter" in text
    assert ("350 of the 1,000 made-up words of three letters and 63 of those of four letters are a spelling of the "
            "lexicon letter for letter (467 and 244 when an ending may follow)") in text
    assert "Of five letters it is 18 (100 with an ending), of six letters 1 (27)." in text
    real = lines(3)
    apart = [r for r in real if not r["linked"]]
    r = fig["real_words"]
    assert (r["words"], r["linked_by_the_lexicon"], r["not_linked"], r["at_most_0.05"]) == (91, 15, 76, 8)
    assert (len(real), len(apart), sum(x["chance"] <= V.BAR for x in apart)) == (91, 76, 8)
    assert [(r["by_length"][k]["words"], r["by_length"][k]["at_most_0.05"]) for k in V.LENGTHS] == [(25, 0), (27, 2), (24, 6)]
    assert "91 words of the lexicon have an accepted meaning" in text and "For 15 of them" in text
    assert ("Of the other 76, 8 beat the 5% bar where 4 are expected: none of 25 with three or four letters, 2 of 27 "
            "with five or six, and 6 of 24 with seven or more") in text
    assert "beat the same bar 8 times in 76, and 6 times in 24 from seven letters up" in text
    # the pairs of names the page gives as examples are among the eight
    under = {x["headword"]: x["best"] for x in apart if x["chance"] <= V.BAR}
    assert under["Tkidemni"] == ["Tktidmni"] and under["Teqoridemni"] == ["Tmelọrdeamni"]
    assert under["Amniterese"] == ["Amnitore"]


def test_the_sample_for_the_test_s_shortcut():
    needs(*LOCAL, "data/sources/variants/out/sample.json")
    got = json.loads((ROOT / "data/sources/variants/out/sample.json").read_text(encoding="utf-8"))
    reported = {r["letters"]: r["listed"]["chance"] for r in lines(1)}
    assert got["sample"] == len(got["rows"]) == V.SAMPLE == 30
    assert all(r["reported"] == reported[r["letters"]] for r in got["rows"])
    assert got["same"] == sum(r["own"] == r["reported"] for r in got["rows"]) == 21
    assert got["largest_difference"] == max(abs(r["own"] - r["reported"]) for r in got["rows"])
    assert round(got["largest_difference"], 3) == 0.011 and got["on_the_other_side_of_the_bar"] == 0
    assert ("For a sample of 30 hidden variants" in page() and "the chance is the same for 21, differs by at most "
            "0.011 for the other 9 (11 made-up words in 1,000), and no variant changes sides of the 5% bar") in page()


def test_the_by_product_for_the_coverage_map():
    fig = figures()["coverage_map"]
    assert len(fig["entries"]) == 15 and fig["words"] == 152
    assert {"kroro", "qetrri", "Kine", "qetneyineqeli"} <= set(fig["entries"])
    text = " ".join((ROOT / "NEXT_STEPS.md").read_text(encoding="utf-8").replace("`", "").split())
    assert "15 entries count as translated in the map" in text and "152 running words rest on them" in text
    # on made-up texts: a word counts when the map has it translated through such an entry
    lex = [raw("wetne", ["qetne"], "an epithet", "hypothesis"), raw("qetne", [], "variant of wetne"), raw("at", [], "bread")]
    texts = texts_of(("T1", [("qetne", "meaning", "variant of wetne", [("qetne", "qetne")]),
                             ("at", "meaning", "bread", [("at", "at")]),
                             ("qetneli", "hypothesis", "", [("qetne", "qetne"), ("li", "ending")])]))
    assert V.rest_on_a_variant(V.words(lex), texts) == {"entries": ["qetne"], "words": 1}


def test_the_examples_that_started_the_step():
    rows = {r["piece"]: r for r in lines(2) if not r["headword"]}
    best = lambda p: rows[p]["hits"][0]   # noqa: E731
    assert best("pertese")["entries"] == ["perite"] and best("pertese")["ending"] == "se"
    assert best("pertese")["differences"] == [["i", ""]] and rows["pertese"]["chance"] <= V.BAR
    assert best("prSn")["entries"] == ["plsn"] and best("prSn")["differences"] == [["l", "r"]]
    assert best("petmoS")["entries"] == ["pelmos"] and best("petmoS")["differences"] == [["l", "t"]]
    assert rows["prSn"]["chance"] > V.BAR and rows["petmoS"]["chance"] > V.BAR and len(rows["prSn"]["letters"]) == 4
    assert best("amn")["entries"] == ["Amni"] and rows["amn"]["letters"] == "0mn" and rows["amn"]["chance"] > V.BAR
    assert rows["menote"]["chance"] <= V.BAR and best("menote")["entries"] != ["Amnote"]
    assert rows["menote"]["hits"][1]["entries"] == ["Amnote"]
    assert not any("pestol" in h["entries"] or "peseto" in h["entries"] for h in rows["stol"]["hits"])


def test_the_public_files_hold_forms_and_no_gloss():
    needs(*LOCAL, "data/rilly2003")
    rows = lines(2)
    listed = (ROOT / "data/discovery/variants_candidates.tsv").read_text(encoding="utf-8")
    assert listed == V.public_list(rows)
    body = [l.split("\t") for l in listed.splitlines()]
    assert body[0] == V.HEAD and len(body) == 1211 and all(len(l) == len(V.HEAD) for l in body)
    assert [float(l[5]) for l in body[1:]] == sorted(float(l[5]) for l in body[1:])        # the best chance first
    assert "the 1,210 searched pieces" in page()
    # no meaning of the lexicon stands in a public file of this search: not in the lists, the page or the brief
    public = [listed, PAGE.read_text(encoding="utf-8"), (ROOT / "data/discovery/variants_brief.md").read_text(encoding="utf-8")]
    confirmed = ROOT / "data/discovery/variants_confirmed.tsv"
    if confirmed.exists():
        public.append(confirmed.read_text(encoding="utf-8"))
    meanings = {e["meaning"] for e in V.words() if len(e["meaning"]) >= 30}
    assert len(meanings) > 300
    assert not [m for m in meanings for text in public if m in text]


def test_the_packs_hold_every_match_that_beats_the_bar():
    needs(*LOCAL, "data/sources/variants/check_key.json", "data/sources/variants/check")
    key = json.loads((ROOT / "data/sources/variants/check_key.json").read_text(encoding="utf-8"))
    packs = sorted((ROOT / "data/sources/variants/check").glob("pack*/pack.jsonl"))
    items = [json.loads(l) for q in packs for l in q.read_text(encoding="utf-8").splitlines()]
    assert len(packs) == 3 and len(items) == len(key) == 129 and {x["id"] for x in items} == set(key)
    assert max(len(q.read_text(encoding="utf-8").splitlines()) for q in packs) <= V.PER_PACK
    assert collections.Counter(a["what"] for a in key.values()) == {"best": 105, "decoy": V.DECOYS, "control": V.CONTROLS}
    rows = lines(2)
    under = {(r["piece"], r["headword"]): r for r in rows if "hits" in r and r["chance"] <= V.BAR}
    best = {(a["piece"], a["headword"]): i for i, a in key.items() if a["what"] == "best"}
    assert set(best) == set(under) and len(under) == 105            # every one, the 23 the lexicon links too
    by_id = {x["id"]: x for x in items}
    for k, i in best.items():
        shown = [[e["headword"] for e in c["entries"]] for c in by_id[i]["candidates"]]
        assert shown == [h["entries"] for h in under[k]["hits"]], k       # its best match first, then the next two
        assert key[i]["best"] == shown[0] and math.isclose(key[i]["chance"], under[k]["chance"])
    # the controls and the decoys are hidden variants of the test, shown as letters; a control beat the bar, and
    # no candidate of a decoy holds an entry that lists it
    test = {r["letters"]: r for r in lines(1)}
    listing = collections.defaultdict(set)
    for r in test.values():
        for o in r["owners"]:
            listing[o] |= {x for v in r["variants"] for x in V.strings(v)}
    for i, a in key.items():
        if a["what"] != "best":
            assert a["owners"] and by_id[i]["lexicon"] is None and not a["headword"], i
            assert any(V.E.meroitic(a["piece"], True) in listing[o] for o in a["owners"]), i
            shown = {e["headword"] for c in by_id[i]["candidates"] for e in c["entries"]}
            assert len(by_id[i]["candidates"]) == V.TOP, i
            if a["what"] == "control":
                assert a["chance"] <= V.BAR, i
            else:
                assert not shown & set(a["owners"]) and len(V.E.meroitic(a["piece"], True)) >= 5, i
    # nothing in an item says what it is, and the piece's own word never shows a gloss
    assert all(set(x) == {"id", "piece", "kind", "texts", "contexts", "lexicon", "candidates"} for x in items)
    for x in items:
        for c in x["contexts"]:
            k = next(n for n, w in enumerate(c["words"].split()) if w.startswith("["))
            assert c["glosses"].split(" / ")[k] == "?", x["id"]
    # the draw is the one the result files give: the first hidden variants of the shuffled order that qualify
    b, known, _ = V.pack_draw(rows, list(test.values()))
    assert [(r["piece"], r["headword"]) for r in b] == sorted(under)
    needs(*WORDS, "data/sources/coverage/glosses.jsonl")
    entries = V.words()
    pairs, hidden = V.cases(entries)
    made = V.known_items(known, hidden, entries, pairs, V.ending_chances(V.ending_counts()), V.glossed())
    assert sorted((m["what"], m["piece"], m["owners"], m["hits"][0]["entries"]) for m in made) \
        == sorted((a["what"], a["piece"], a["owners"], a["best"]) for a in key.values() if a["what"] != "best")
    assert "129 items in three packs" in page() and "12 decoys" in page() and "12 controls" in page()


CHECKS = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]

if __name__ == "__main__":
    run(CHECKS)
