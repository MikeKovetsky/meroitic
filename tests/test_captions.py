"""Checks for the caption pilot (src/captions.py).

  python3 -I tests/test_captions.py

The inventory, the crops, the packs and the answers are local only, so the checks run on made-up captions; a
check that reads a local file says so and is skipped where it is absent.
"""
import contextlib
import io
import json
import pathlib
import re
import sys
import tempfile
import types

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import captions as C                    # noqa: E402
from local_only import Skip, needs, run   # noqa: E402

PAGE = ROOT / "data/discovery/caption_pilot.md"
THE_MAP = ["data/sources/v6/analysts/glosses.jsonl", "data/sources/recurring/overlay.jsonl",
           "data/sources/rare/g2/overlay.jsonl", "data/sources/rare/g4/overlay.jsonl", "data/sources/g3/overlay.jsonl",
           "data/sources/rare/g4m/overlay.jsonl", "data/sources/g8b/overlay.jsonl", "data/sources/g9/overlay.jsonl"]


def w(form, level, gloss=""):
    return {"form": form, "level": level, "gloss": gloss}


def cap(i, kind, caption=True):
    return {"id": i, "caption": caption, "figure_kind": kind, "crop": f"crops/{i}.png"}


def stops(fn, part):
    try:
        fn()
    except SystemExit as e:
        assert part in str(e), e
        return True
    raise AssertionError("did not stop")


@contextlib.contextmanager
def set_to(obj, **values):
    """Module values replaced for the length of a check."""
    old = {k: getattr(obj, k) for k in values}
    for k, v in values.items():
        setattr(obj, k, v)
    try:
        yield
    finally:
        for k, v in old.items():
            setattr(obj, k, v)


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


INV = [cap("REM 0010", "king"), cap("REM 0003", "queen"), cap("Meroe 14", "god"), cap("REM 0020", "god"),
       cap("REM 0030", "king", caption=False)]
GL = {
    "REM 0003": [w("kdke", "meaning", "queen"), w("amnitre", "name"), w("abc", "kind"), w("qore", "meaning", "king")],
    "REM 0010": [w("qore", "meaning", "king"), w("ntkmni", "name"), w("abc", "unknown"), w("qore", "meaning", "king"),
                 w("-l", "grammar", "determiner"), w("..re", "lost"), w("3", "number")],
    "REM 0020": [w("qore", "meaning", "king"), w("xyz", "hypothesis")],
    "Meroe 14": [w("qore", "meaning", "king"), w("mk", "meaning", "god")],
    "REM 0030": [w("pqr", "meaning", "prince")],
}
SITES = {"REM 0003": "naga", "REM 0010": "naga", "REM 0020": "naga", "Meroe 14": "meroe", "REM 0030": "naga"}

# Captions with several items each, parallel formulas and a variant spelling (ntke, ntki): the packs' checks.
INV2 = [cap("REM 0001", "god"), cap("REM 0002", "goddess"), cap("REM 0003", "king"), cap("REM 0004", "queen"),
        cap("REM 0005", "god"), cap("REM 0006", "king"), cap("REM 0007", "priest"), cap("REM 0008", "animal")]
GL2 = {
    "REM 0001": [w("apedemki", "name"), w("pwrite", "meaning", "life"), w("lbxte", "meaning", "give to them"),
                 w("ntke", "meaning", "strength")],
    "REM 0002": [w("pwrite", "meaning", "life"), w("lbxte", "meaning", "give to them"), w("ntki", "meaning", "strength")],
    "REM 0003": [w("qore", "meaning", "king"), w("ntkmni", "name"), w("abc", "unknown")],
    "REM 0004": [w("kdke", "meaning", "queen"), w("mnitore", "name")],
    "REM 0005": [w("amni", "name"), w("mk", "meaning", "god")],
    "REM 0006": [w("qore", "meaning", "king"), w("ato", "meaning", "water")],
    "REM 0007": [w("at", "meaning", "priest"), w("xyz", "hypothesis")],
    "REM 0008": [w("xlbi", "meaning", "bull"), w("dime", "meaning", "cow")],
}
SITES2 = {o["id"]: "naga" if o["id"] < "REM 0005" else "meroe" for o in INV2}


# ---------------------------------------------------------------------------------------------- the material

def test_order_puts_rem_numbers_first():
    ids = sorted(["Meroe 14", "REM 0010", "MeroNews29e p. 137", "REM 0003", "REM 1041A"], key=C.order)
    assert ids == ["REM 0003", "REM 0010", "REM 1041A", "MeroNews29e p. 137", "Meroe 14"]   # then by the id


def test_site_is_the_place_folded():
    assert C.site_of("Meroë, temple of Amun") == C.site_of("Meroe City, temple of the lion-god") == "meroe"
    assert C.site_of("Naga, temple of the lion-god (Apedemak)") == "naga"
    assert C.site_of("Philae, Temple of Isis, the 'Meroitic Chamber'") == "philae"
    # REM 0075 is Napata's, REM 0076 to 0078 Gebel Barkal's: one place; Wad Ben Naga is not Naga
    assert C.site_of("Napata (Gebel Barkal or Merawi: the squeeze is marked Barkal, L., D. gives Merawi); now Berlin") \
        == C.site_of("Gebel Barkal, pyramid 15 (Lepsius), chapel (shrine) on the north-east wall")
    assert C.site_of("Wad Ben Naga, the eastern (Isis) temple") != C.site_of("Naga, temple of Ammon")


def test_items_take_the_right_levels_once_a_caption_and_cap_a_spelling():
    known = C.items(INV, GL, "known")
    # captions only (REM 0030 is not one), in REM order; qore once in a caption, in its first three captions only
    assert [(o["text"], o["form"]) for o in known] == [("REM 0003", "kdke"), ("REM 0003", "qore"),
                                                       ("REM 0010", "qore"), ("REM 0020", "qore"), ("Meroe 14", "mk")]
    assert known[1]["n"] == 4 and known[2]["n"] == 1                # the first place of the spelling in the caption
    opened = C.items(INV, GL, "open")
    assert [(o["text"], o["form"]) for o in opened] == [("REM 0003", "abc"), ("REM 0010", "abc"), ("REM 0020", "xyz")]
    assert all(o["level"] not in C.EXCLUDED for o in opened)        # no grammar, name, number or lost word


def test_the_cap_is_three_captions():
    inv = [cap(f"REM {i:04d}", "king") for i in range(1, 6)]
    gl = {o["id"]: [w("qore", "meaning", "king")] for o in inv}
    assert [o["text"] for o in C.items(inv, gl, "known")] == ["REM 0001", "REM 0002", "REM 0003"]


def test_an_item_is_a_spelling_at_its_first_place_and_the_cap_counts_known_and_open_together():
    inv = [cap(f"REM {i:04d}", "king") for i in range(1, 6)]
    gl = {"REM 0001": [w("kete", "meaning", "you"), w("kete", "hypothesis")],   # one word, known at its first place
          "REM 0002": [w("wse", "kind"), w("wse", "meaning", "his")],           # one word, open at its first place
          "REM 0003": [w("kete", "meaning", "you")],
          "REM 0004": [w("kete", "hypothesis")],                                  # kete's third caption: open
          "REM 0005": [w("kete", "hypothesis"), w("kete", "meaning", "you")]}     # its fourth: no item
    known, opened = C.items(inv, gl, "known"), C.items(inv, gl, "open")
    assert [(o["text"], o["form"], o["n"]) for o in known] == [("REM 0001", "kete", 1), ("REM 0003", "kete", 1)]
    assert [(o["text"], o["form"], o["n"]) for o in opened] == [("REM 0002", "wse", 1), ("REM 0004", "kete", 1)]
    gl["REM 0001"] = [w("amni", "name"), w("amni", "meaning", "Amun")]          # a name at its first place: no item
    assert not [o for o in C.items(inv, gl, "known") if o["form"] == "amni"]
    assert stops(lambda: C.items(inv + [cap("REM 0009", "god")], gl, "known"), "not on the map")


def test_gate1_counts_and_bar():
    c = C.count(INV, GL)
    assert (c["captions"], c["known_items"], c["open_items"], c["open_spellings"]) == (4, 5, 3, 2)
    assert c["met"] is False
    inv = [cap(f"REM {i:04d}", "king") for i in range(1, 21)]
    gl = {o["id"]: [w(f"k{i}", "meaning", "x"), w(f"o{i % 10}", "unknown")] for i, o in enumerate(inv)}
    c = C.count(inv, gl)
    assert (c["known_items"], c["open_spellings"], c["met"]) == (20, 10, True)   # both bars met exactly
    c = C.count(inv[:19], gl)
    assert (c["known_items"], c["open_spellings"], c["met"]) == (19, 10, False)  # 19 known items: under 20
    gl = {o["id"]: [w(f"k{i}", "meaning", "x"), w(f"o{i % 9}", "unknown")] for i, o in enumerate(inv)}
    c = C.count(inv, gl)
    assert (c["known_items"], c["open_spellings"], c["met"]) == (20, 9, False)   # 9 open spellings: under 10


def test_the_inventory_is_the_texts_once_each_with_a_held_picture():
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        f = d / "inventory.jsonl"
        f.write_text("\n".join(json.dumps(o) for o in INV + [INV[0]]) + "\n", encoding="utf-8")
        assert stops(lambda: C.load_inventory(f), "more than once")
        f.write_text(json.dumps(cap("REM 0003", "dog")) + "\n", encoding="utf-8")
        assert stops(lambda: C.load_inventory(f), "figure_kind")
        f.write_text(json.dumps(cap("REM 0003", "king", caption="no")) + "\n", encoding="utf-8")
        assert stops(lambda: C.load_inventory(f), "is not true or false")      # "no" would count as a caption
        f.write_text("".join(json.dumps(o) + "\n" for o in INV), encoding="utf-8")
        assert C.load_inventory(f) == INV
        inv = [o | {"crop": str(d / f"{o['id']}.png")} for o in INV]
        texts = [o["id"] for o in INV]
        for o in inv[1:]:
            pathlib.Path(o["crop"]).write_bytes(b"x")
        assert stops(lambda: C.held(inv, texts), "no cut picture for the captions REM 0010")
        pathlib.Path(inv[0]["crop"]).write_bytes(b"x")
        assert C.held(inv, texts) == inv
        assert stops(lambda: C.held(inv, texts + ["REM 0040"]), "no row for ['REM 0040']")
        assert stops(lambda: C.held(inv, texts[1:]), "rows for other texts ['REM 0010']")


def test_the_hidden_word_is_hidden_everywhere_and_names_say_only_name():
    s = C.shown(GL["REM 0010"], "qore")
    assert "qore" not in s and s.count("[?]") == 2 and "king" not in s
    assert "ntkmni (a name)" in s and "abc (meaning unknown)" in s and "-l (determiner)" in s
    assert "..re (damaged)" in s and "3 (a numeral)" in s


def test_wrong_pictures_are_of_another_kind_and_the_same_place_when_possible():
    wr = C.wrong_pictures(INV, SITES)
    kind = {o["id"]: o["figure_kind"] for o in INV}
    assert set(wr) == {"REM 0003", "REM 0010", "REM 0020", "Meroe 14"}
    for a, b in wr.items():
        assert a != b and kind[a] != kind[b] and b != "REM 0030"   # never a text that is not a caption
    assert SITES[wr["REM 0010"]] == "naga"                          # a naga caption of another kind exists
    assert wr["Meroe 14"] in ("REM 0003", "REM 0010")               # no other meroe caption: any place, not a god
    assert wr == C.wrong_pictures(INV, SITES)                       # the draw is fixed by its seed
    # one caption of another kind at the same place among ten elsewhere: always that one
    inv = [cap("REM 0001", "king"), cap("REM 0002", "god")] + [cap(f"REM {i:04d}", "god") for i in range(3, 13)]
    sites = {o["id"]: "naga" if o["id"] <= "REM 0002" else "meroe" for o in inv}
    assert C.wrong_pictures(inv, sites)["REM 0001"] == "REM 0002"


def test_a_wrong_picture_is_never_the_captions_own_scene():
    # nine captions of gods beside the king's scene share its crop; a god and a queen have scenes of their own
    inv = [cap("REM 0001", "king")] + [cap(f"REM {i:04d}", "god") | {"crop": "crops/REM 0001.png"} for i in range(2, 11)] \
        + [cap("REM 0011", "god"), cap("REM 0012", "queen")]
    sites = {o["id"]: "naga" for o in inv}
    wr = C.wrong_pictures(inv, sites)
    crop = {o["id"]: o["crop"] for o in inv}
    assert all(crop[a] != crop[b] for a, b in wr.items())
    assert wr["REM 0001"] in ("REM 0011", "REM 0012") and {wr[f"REM {i:04d}"] for i in range(2, 11)} == {"REM 0012"}


# ---------------------------------------------------------------------------------------------- the packs

def packs_of(inv=INV2, gl=GL2, sites=SITES2, kind="known"):
    return C.make_packs(inv, gl, sites, kind)


def test_packs_give_each_reader_every_item_once_and_the_right_or_wrong_picture():
    its, packs, key = packs_of()
    wr = C.wrong_pictures(INV2, SITES2)
    crop = {o["id"]: o["crop"] for o in INV2}
    codes = [C.code("known", i) for i in range(len(its))]
    for r in "ABCD":
        mine = [n for n, p in key["packs"].items() if p["reader"] == r]
        got = [e for n in mine for e in packs[n]["items"]]
        assert sorted(e["item"] for e in got) == codes
        assert {key["packs"][n]["condition"] for n in mine} == {"right" if r in "AB" else "wrong"}
        for e in got:
            o = its[codes.index(e["item"])]
            want = o["text"] if r in "AB" else wr[o["text"]]
            assert key["pictures"][e["picture"].rsplit("/", 1)[1]] == crop[want]
            assert e["caption"] == C.shown(GL2[o["text"]], o["form"])
    for a, c in (("A", "C"), ("B", "D")):                            # the two conditions read the same cuts
        cut = lambda r: sorted(tuple(p["items"]) for p in key["packs"].values() if p["reader"] == r)   # noqa: E731
        assert cut(a) == cut(c)
    assert (its, packs, key) == packs_of()                           # the packs are fixed by their seeds


def test_two_items_clash_where_one_would_give_the_other_away():
    gl = GL2 | {"REM 0009": [w("ntki", "meaning", "strength"), w("mlo", "meaning", "good")],
                "REM 0010": [w("abc", "unknown", "?"), w("dd", "meaning", "x")],
                "REM 0011": [w("qorpslo", "meaning", "genitive plural of qore / ruler"), w("ee", "meaning", "y")],
                "REM 0012": [w("tt", "meaning", "the god at Napata"), w("ff", "meaning", "z")]}

    def entry(text, form, gloss, right=None, wrong=None):
        return {"item": {"text": text, "form": form, "gloss": gloss}, "right": right or f"crops/{text}.png",
                "wrong": wrong or f"crops/w{text}.png"}

    ntke = entry("REM 0001", "ntke", "strength")
    assert C.clash(ntke, entry("REM 0001", "pwrite", "life"), gl)                           # one caption
    assert C.clash(entry("REM 0002", "pwrite", "life"), entry("REM 0001", "lbxte", "give to them"), gl)   # parallels
    assert C.clash(ntke, entry("REM 0009", "mlo", "good"), gl)               # REM 0009 shows ntki, glossed as ntke
    assert C.clash(entry("REM 0003", "abc", "?"), entry("REM 0010", "dd", "x"), gl)   # shows the open spelling hidden
    assert C.clash(entry("REM 0003", "qore", "king"), entry("REM 0011", "ee", "y"), gl)   # names it in a gloss
    assert not C.clash(entry("REM 0007", "at", "priest"), entry("REM 0012", "ff", "z"), gl)   # "at": an English word
    assert not C.clash(ntke, entry("REM 0009", "ntki", "strength"), gl)      # each hidden: neither shows the other
    assert not C.clash(ntke, entry("REM 0004", "kdke", "queen"), gl)         # nothing in common
    assert C.clash(ntke, entry("REM 0004", "kdke", "queen", right="crops/REM 0001.png"), gl)     # one picture twice
    assert C.clash(ntke, entry("REM 0004", "kdke", "queen", wrong="crops/wREM 0001.png"), gl)


def test_no_pack_gives_a_hidden_word_away_or_shows_a_picture_twice():
    its, packs, key = packs_of()
    by_code = {C.code("known", i): o for i, o in enumerate(its)}
    assert len(its) == 14 and len({o["text"] for o in its}) == 8    # several items in a caption, parallel captions
    for name, p in packs.items():
        assert len(p["items"]) <= C.BATCH
        assert len({e["picture"] for e in p["items"]}) == len(p["items"])
        texts = [by_code[e["item"]]["text"] for e in p["items"]]
        assert len(set(texts)) == len(texts)                         # never two items of one caption
        for e in p["items"]:
            o = by_code[e["item"]]
            for f in p["items"]:
                if f is not e:                                       # nor the hidden word shown in another caption
                    assert o["form"] not in f["caption"].split() and f"({o['gloss']})" not in f["caption"], (name, e, f)


def test_a_pack_says_nothing_of_its_reader_its_condition_or_its_texts():
    its, packs, key = packs_of()
    ids = [o["id"] for o in INV2]
    for name, p in packs.items():
        assert re.fullmatch(r"pack\d\d", name) and set(p) == {"answers", "items"}
        assert p["answers"] == f"data/sources/captions/answers/known/{name}.jsonl"
        text = json.dumps(p, ensure_ascii=False)
        assert not any(s in text for s in ids + ["condition", "right", "wrong", "reader", "crops/"]), text
        for e in p["items"]:
            assert set(e) == {"item", "picture", "caption"}
            assert re.fullmatch(r"data/sources/captions/packs/known/pictures/pic\d\d\.png", e["picture"]), e
    assert set(key["pictures"].values()) <= {o["crop"] for o in INV2}


def test_answers_are_each_packs_items_once_in_five_words_at_most():
    key = {"packs": {"pack01": {"reader": "A", "condition": "right", "items": ["k001", "k002"]},
                     "pack02": {"reader": "C", "condition": "wrong", "items": ["k002", "k001"]}}}
    good = {"pack01": [{"item": "k001", "meaning": "king"}, {"item": "k002", "meaning": "the god of the moon"}],
            "pack02": [{"item": "k002", "meaning": "water"}, {"item": "k001", "meaning": "none", "element": "none"}]}

    def answers(files):
        with tempfile.TemporaryDirectory() as d:
            for name, rows in files.items():
                (pathlib.Path(d) / f"{name}.jsonl").write_text("".join(json.dumps(a) + "\n" for a in rows), encoding="utf-8")
            return C.answers_of(key, pathlib.Path(d))

    got = answers(good)
    assert {k: a["meaning"] for k, a in got.items()} == {("k001", "A"): "king", ("k002", "A"): "the god of the moon",
                                                         ("k002", "C"): "water", ("k001", "C"): "none"}
    assert stops(lambda: answers(good | {"pack01": good["pack01"][:1]}), "pack01: no answer for k002")
    assert stops(lambda: answers(good | {"pack01": good["pack01"] + [{"item": "k003", "meaning": "x"}]}),
                 "not an item of the pack: 'k003'")
    assert stops(lambda: answers(good | {"pack02": good["pack02"] + [{"item": "k002", "meaning": "x"}]}),
                 "a second answer for 'k002'")
    assert stops(lambda: answers(good | {"pack02": [{"item": "k002", "meaning": "a word of six words here"},
                                                    good["pack02"][1]]}), "a meaning of 6 words")
    assert stops(lambda: answers(good | {"pack02": [{"item": "k002", "meaning": " "}, good["pack02"][1]]}),
                 "a meaning of 0 words")
    assert stops(lambda: answers({"pack01": good["pack01"]}), "pack02: no answer for k002")


# ---------------------------------------------------------------------------------------------- the judges and gate 2

def test_judges_see_no_reader_and_no_condition():
    its = C.items(INV, GL, "known")
    ans = {(C.code("known", i), r): {"meaning": f"m{i}{r}", "element": "the crown"} for i in range(len(its)) for r in "ABCD"}
    pack, key = C.judge_pack("known", its, ans)
    assert len(pack) == len(key) == 4 * len(its)
    assert all(set(p) == {"id", "reference", "answer"} for p in pack)
    for p in pack:
        item, reader = key[p["id"]]
        assert p["answer"] == f"m{int(item[1:]) - 1}{reader}"
        assert p["reference"] == its[int(item[1:]) - 1]["gloss"]


def test_item_scores_average_judges_then_readers():
    key = {"j1": ("k001", "A"), "j2": ("k001", "B"), "j3": ("k001", "C"), "j4": ("k001", "D")}
    judged = {"J1": {"j1": 1, "j2": 0.5, "j3": 0, "j4": 0}, "J2": {"j1": 1, "j2": 1, "j3": 0.5, "j4": 0}}
    s = C.item_scores(key, judged)
    assert s == {"k001": {"right": (1 + 0.75) / 2, "wrong": (0.25 + 0) / 2}}
    assert stops(lambda: C.item_scores(key, {"J1": judged["J1"], "J2": {"j1": 1}}), "exactly once")
    assert stops(lambda: C.item_scores(key, {"J1": judged["J1"], "J2": judged["J2"] | {"j4": True}}), "score True")
    assert stops(lambda: C.item_scores(key, {"J1": judged["J1"], "J2": judged["J2"] | {"j4": 0.25}}), "score 0.25")
    with tempfile.TemporaryDirectory() as d:
        f = pathlib.Path(d) / "J1.jsonl"
        f.write_text('{"id": "j1", "score": 1}\n{"id": "j1", "score": 0}\n', encoding="utf-8")
        assert stops(lambda: C.scores_of(f), "j1 is scored twice")


def test_sign_flip_finds_a_clear_gain_and_not_a_null():
    assert C.sign_flip([1.0] * 25, [f"s{i}" for i in range(25)]) < 0.001
    assert C.sign_flip([1, -1] * 12, [f"s{i}" for i in range(24)]) > 0.3
    # one spelling's items flip together: 25 items of one spelling are one draw of two signs
    assert C.sign_flip([1.0] * 25, ["qore"] * 25) > 0.4


def test_gate2_bars():
    good = {f"k{i:03d}": {"right": 0.9, "wrong": 0.3} for i in range(24)}
    forms = {k: k for k in good}
    assert C.gate2(good, forms)["met"] is True
    assert C.gate2(dict(list(good.items())[:19]), forms)["met"] is False         # under 20 items
    low = {k: {"right": 0.45, "wrong": 0.0} for k in good}
    assert C.gate2(low, forms)["met"] is False                                    # right under 0.50
    small = {k: {"right": 0.9, "wrong": 0.75} for k in good}
    assert C.gate2(small, forms)["met"] is False                                  # gain under 0.20
    one = {k: {"right": 0.9, "wrong": 0.3} for k in good}
    assert C.gate2(one, {k: "qore" for k in good})["met"] is False                # one spelling: p too high


def test_gate2_bars_at_their_edges():
    # scores are means of two readers' means of two judges: steps of 1/8. Exactly 20 items, a right-picture mean of
    # exactly 0.50 and a gain of exactly 0.20 meet the bars; one step under any of them misses
    edge = {f"k{i:03d}": {"right": 0.5, "wrong": 0.25 if i < 16 else 0.5} for i in range(20)}
    forms = {k: k for k in edge}
    g = C.gate2(edge, forms)
    assert (g["items"], g["right"], g["gain"], g["p"] < 0.05, g["met"]) == (20, 0.5, 0.2, True, True)
    under = edge | {"k019": {"right": 0.25, "wrong": 0.25}}                      # right 0.4875, gain 0.1875
    assert C.gate2(under, forms)["met"] is False
    under = edge | {"k015": {"right": 0.5, "wrong": 0.375}}                      # gain 0.19375
    assert C.gate2(under, forms)["met"] is False
    assert C.gate2(dict(list(edge.items())[1:]), forms)["met"] is False           # 19 items


def test_agreement_and_kappa():
    j = {"J1": {"a": 1, "b": 0, "c": 0.5, "d": 1}, "J2": {"a": 1, "b": 0, "c": 0, "d": 1}}
    assert C.agreement(j) == {"answers": 4, "same": 0.75, "kappa": 0.6}          # chance 6/16: (0.75 - 0.375) / 0.625


# ---------------------------------------------------------------------------------------------- the run

def test_a_run_from_the_packs_to_gate_2_and_the_steps_that_must_not_run():
    """The commands on made-up captions in a folder of their own: packs, answers, judges, score, public; the packs
    are written once; gate 2's packs wait for gate 1, gate 3's for gate 2."""
    inv = [cap(f"REM {i:04d}", ("king", "god")[i % 2]) | {"crop": f"crops/REM_{i:04d}.png"} for i in range(1, 25)]
    gl = {o["id"]: [w(f"k{i}", "meaning", f"x{i}"), w(f"o{i}", "unknown")] for i, o in enumerate(inv)}
    sites = {o["id"]: "naga" for o in inv}
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        here = root / "data/sources/captions"
        (here / "crops").mkdir(parents=True)
        for o in inv:
            (here / o["crop"]).write_bytes(o["id"].encode())
        with set_to(C, ROOT=root, HERE=here, PUBLIC=root / "figures.json", the_inventory=lambda: inv,
                    the_map=lambda: gl, the_sites=lambda: sites):
            assert stops(lambda: C.main(["packs", "open"]), "gate 2 is not met")
            with set_to(C, the_inventory=lambda: inv[:19]):
                assert stops(lambda: C.main(["packs", "known"]), "gate 1 is missed")
            assert quiet(C.main, ["packs", "known"]) == 0
            key = json.loads((here / "key_known.json").read_text(encoding="utf-8"))
            for name, c in key["pictures"].items():
                assert (here / "packs/known/pictures" / name).read_bytes() == (here / c).read_bytes()
            assert quiet(C.main, ["packs", "known"]) == 0                     # the same packs again: nothing to do
            with set_to(C, the_map=lambda: gl | {"REM 0001": [w("k0", "meaning", "x0"), w("o1", "unknown")]}):
                assert stops(lambda: C.main(["packs", "known"]), "stands already")
            its = json.loads((here / "items_known.json").read_text(encoding="utf-8"))
            gloss = {C.code("known", i): o["gloss"] for i, o in enumerate(its)}
            assert (here / "answers/known").is_dir()                           # made with the packs
            for name, p in key["packs"].items():
                pack = json.loads((root / f"data/sources/captions/packs/known/{name}.json").read_text(encoding="utf-8"))
                assert [e["item"] for e in pack["items"]] == p["items"]
                rows = [{"item": e["item"], "meaning": gloss[e["item"]] if p["condition"] == "right" else "a lion"}
                        for e in pack["items"]]
                (root / pack["answers"]).write_text("".join(json.dumps(a) + "\n" for a in rows), encoding="utf-8")
            assert quiet(C.main, ["judges", "known"]) == 0
            pack = json.loads((here / "judges/known/pack.json").read_text(encoding="utf-8"))
            for j in C.JUDGES:
                (here / f"judges/known/{j}.jsonl").write_text("".join(
                    json.dumps({"id": p["id"], "score": 1 if p["answer"] == p["reference"] else 0}) + "\n" for p in pack),
                    encoding="utf-8")
            assert quiet(C.main, ["score", "known"]) == 0
            got = json.loads((here / "judges/known/scores.json").read_text(encoding="utf-8"))
            assert (got["gate2"]["items"], got["gate2"]["right"], got["gate2"]["wrong"], got["gate2"]["met"]) == (24, 1.0, 0.0, True)
            assert got["judges"] == {"answers": 96, "same": 1.0, "kappa": 1.0}
            assert quiet(C.main, ["public"]) == 0
            figs = json.loads((root / "figures.json").read_text(encoding="utf-8"))
            assert set(figs) == {"gate1", "gate2", "judges"} and figs["gate1"]["known_items"] == 24
            assert quiet(C.main, ["packs", "open"]) == 0                      # gate 2 met: gate 3's packs
            with set_to(C, the_inventory=lambda: inv[:23]):
                assert stops(lambda: C.main(["public"]), "no longer those the packs were made from")


def test_the_map_is_the_seven_layers_of_the_page():
    asked = []
    fake = types.SimpleNamespace(LAYERS=[{"name": n} for n in C.LAYERS + ("later",)],
                                 current=lambda upto=None: asked.append(upto) or {})
    old = sys.modules.get("themap")
    sys.modules["themap"] = fake
    try:
        assert C.the_map() == {} and asked == [7]                      # a layer laid later is left off
        fake.LAYERS = [{"name": "recurring"}, {"name": "other"}]
        assert stops(C.the_map, "no longer")
    finally:
        if old is None:
            del sys.modules["themap"]
        else:
            sys.modules["themap"] = old


def test_the_page_states_the_bars_the_code_uses():
    page = PAGE.read_text(encoding="utf-8")
    for s in ("at least 20 known items", "at least 10 different open spellings", "seed 17", "10,000 draws",
              "at least 0.50", "at least 0.20 above", "p < 0.05", "at most three times", "6 million",
              "with its seven layers", "in at most five words"):
        assert s in page, s
    assert (C.GATE1, C.GATE2, C.SEED, C.CAP, C.DRAWS, len(C.LAYERS), C.WORDS) == (
        {"known": 20, "open_spellings": 10}, {"items": 20, "right": 0.50, "gain": 0.20, "p": 0.05}, 17, 3, 10_000, 7, 5)


def test_public_figures_match_the_local_count():
    needs("data/sources/captions/inventory.jsonl", "data/sources/captions/texts87.json", *THE_MAP)
    if not C.PUBLIC.exists():
        raise Skip("the figures are not written yet")
    figs = json.loads(C.PUBLIC.read_text(encoding="utf-8"))
    assert figs["gate1"] == C.count(C.the_inventory(), C.the_map())


if __name__ == "__main__":
    run([(n, f) for n, f in globals().items() if n.startswith("test_")])
