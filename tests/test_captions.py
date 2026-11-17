"""Checks for the caption pilot (src/captions.py).

  python3 -I tests/test_captions.py

The inventory, the crops, the packs and the answers are local only, so the checks run on made-up captions; a
check that reads a local file says so and is skipped where it is absent.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import captions as C                    # noqa: E402
from local_only import needs, run       # noqa: E402

PAGE = ROOT / "data/discovery/caption_pilot.md"


def w(form, level, gloss=""):
    return {"form": form, "level": level, "gloss": gloss}


def cap(i, kind, caption=True):
    return {"id": i, "caption": caption, "figure_kind": kind, "crop": f"crops/{i}.png"}


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


def test_order_puts_rem_numbers_first():
    ids = sorted(["Meroe 14", "REM 0010", "MeroNews29e p. 137", "REM 0003", "REM 1041A"], key=C.order)
    assert ids == ["REM 0003", "REM 0010", "REM 1041A", "MeroNews29e p. 137", "Meroe 14"]   # then by the id


def test_site_is_the_place_folded():
    assert C.site_of("Meroë, temple of Amun") == C.site_of("Meroe City, temple of the lion-god") == "meroe"
    assert C.site_of("Naga, temple of the lion-god (Apedemak)") == "naga"
    assert C.site_of("Philae, Temple of Isis, the 'Meroitic Chamber'") == "philae"


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


def test_gate1_counts_and_bar():
    c = C.count(INV, GL)
    assert (c["captions"], c["known_items"], c["open_items"], c["open_spellings"]) == (4, 5, 3, 2)
    assert c["met"] is False
    inv = [cap(f"REM {i:04d}", "king") for i in range(1, 31)]
    gl = {o["id"]: [w(f"k{i}", "meaning", "x"), w(f"o{i}", "unknown")] for i, o in enumerate(inv)}
    assert C.count(inv, gl)["met"] is True                           # 30 known items, 30 open spellings
    gl = {o["id"]: [w(f"k{i}", "meaning", "x"), w(f"o{i % 9}", "unknown")] for i, o in enumerate(inv)}
    assert C.count(inv, gl)["met"] is False                          # 9 open spellings: under 10


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


def test_packs_give_each_reader_every_item_once_and_the_right_or_wrong_picture():
    its, packs = C.make_packs(INV, GL, SITES, "known")
    wr = C.wrong_pictures(INV, SITES)
    for r in "ABCD":
        got = [e for name, p in packs.items() if p["reader"] == r for e in p["items"]]
        assert sorted(e["item"] for e in got) == [C.code("known", i) for i in range(len(its))]
        cond = {p["condition"] for p in packs.values() if p["reader"] == r}
        assert cond == {"right" if r in "AB" else "wrong"}
        for e in got:
            o = its[int(e["item"][1:]) - 1]
            want = o["text"] if r in "AB" else wr[o["text"]]
            assert e["picture"] == f"crops/{want}.png"
            assert o["form"] not in e["caption"].split()


def test_judges_see_no_reader_and_no_condition():
    its = C.items(INV, GL, "known")
    ans = {(C.code("known", i), r): {"meaning": f"m{i}{r}"} for i in range(len(its)) for r in "ABCD"}
    pack, key = C.judge_pack("known", its, ans)
    assert len(pack) == len(key) == 4 * len(its)
    assert all(set(p) == {"id", "reference", "answer"} for p in pack)
    for p in pack:
        item, reader = key[p["id"]]
        assert p["answer"] == f"m{int(item[1:]) - 1}{reader}"


def test_item_scores_average_judges_then_readers():
    key = {"j1": ("k001", "A"), "j2": ("k001", "B"), "j3": ("k001", "C"), "j4": ("k001", "D")}
    judged = {"J1": {"j1": 1, "j2": 0.5, "j3": 0, "j4": 0}, "J2": {"j1": 1, "j2": 1, "j3": 0.5, "j4": 0}}
    s = C.item_scores(key, judged)
    assert s == {"k001": {"right": (1 + 0.75) / 2, "wrong": (0.25 + 0) / 2}}
    try:
        C.item_scores(key, {"J1": judged["J1"], "J2": {"j1": 1}})
    except SystemExit:
        pass
    else:
        raise AssertionError("a judge who skipped answers must stop the count")


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


def test_agreement_and_kappa():
    j = {"J1": {"a": 1, "b": 0, "c": 0.5, "d": 1}, "J2": {"a": 1, "b": 0, "c": 0, "d": 1}}
    a = C.agreement(j)
    assert a["answers"] == 4 and a["same"] == 0.75 and 0 < a["kappa"] < 1


def test_the_page_states_the_bars_the_code_uses():
    page = PAGE.read_text(encoding="utf-8")
    for s in ("at least 20 known items", "at least 10 different open spellings", "seed 17", "10,000 draws",
              "at least 0.50", "at least 0.20 above", "p < 0.05", "at most three times", "6 million"):
        assert s in page, s
    assert (C.GATE1, C.GATE2, C.SEED, C.CAP, C.DRAWS) == ({"known": 20, "open_spellings": 10},
                                                          {"items": 20, "right": 0.50, "gain": 0.20, "p": 0.05},
                                                          17, 3, 10_000)


def test_public_figures_match_the_local_count():
    needs("data/sources/captions/inventory.jsonl", "data/sources/v6/analysts/glosses.jsonl")
    figs = json.loads(C.PUBLIC.read_text(encoding="utf-8"))
    assert figs["gate1"] == C.count(C.load_inventory(), C.the_map())


if __name__ == "__main__":
    run([(n, f) for n, f in globals().items() if n.startswith("test_")])
