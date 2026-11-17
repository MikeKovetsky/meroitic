"""Checks for the REM pilot (src/rem_pilot.py).

  python3 -I tests/test_rem_pilot.py

The REM's pages and the readers' answers are local only, so the checks run on made-up texts and pages, and on the
public files; a check that reads a local file says so and is skipped where it is absent.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import rem_pilot as R                  # noqa: E402
from local_only import needs, run      # noqa: E402


# --- signs ---
def test_corpus_spelling_as_signs():
    assert R.corpus_to_signs("pelmoS") == ["p", "e", "l", "m", "o", "s"]           # S is the sign s
    assert R.corpus_to_signs("pesto") == ["p", "e", "se", "to"]                   # s is the sign se, to one sign
    assert R.corpus_to_signs("akiNtelo") == ["a", "k", "i", "ñ", "te", "l", "o"]
    assert R.corpus_to_signs("xbxN XoSi") == ["ḫ", "b", "ḫ", "ñ", "ẖ", "o", "s", "i"]
    assert R.corpus_to_signs("..re ab.c") == ["r", "e", "a", "b", "c"]            # lost signs are not signs
    assert R.corpus_to_signs("qo(3)re : wi?") == ["q", "o", "r", "e", "w", "i"]   # line marks, dividers, queries
    assert R.corpus_to_signs("12 keN") == ["1", "2", "k", "e", "ñ"]


def test_fhn_print_as_the_same_signs():
    assert R.fhn_to_signs("(1)qo pelmos (2)atolise") == R.corpus_to_signs("qo pelmoS atolis")
    assert R.fhn_to_signs("Pilqe(12)telo,, an(13)t") == R.corpus_to_signs("pilqetelo ant")
    assert R.fhn_to_signs("womnet(11)h̲,, [=womneselh̲]") == R.corpus_to_signs("womnetX")   # [=...] is not on the stone
    assert R.fhn_to_signs("ps(i) ḫr *kete") == R.corpus_to_signs("pSi xr kete")        # (i) restored, * unsure
    assert [len(w) for w in R.fhn_words("Bekemete(4)li sete,, Mnit(4)wwi")] == [9, 2, 7]   # a line mark is no break


# --- the measures ---
def test_measure_counts_extra_signs_against_the_reading():
    ed = R.corpus_words("abc de")
    assert R.measure(R.corpus_to_signs("abc de"), ed) == {"signs": 5, "right": 5, "words": 2, "agree": 2}
    assert R.measure(R.corpus_to_signs("abx de"), ed) == {"signs": 5, "right": 4, "words": 2, "agree": 1}
    assert R.measure(R.corpus_to_signs("abcz de"), ed)["right"] == 4                # a sign only the reading has
    assert R.measure(R.corpus_to_signs("abcdefghij"), ed)["right"] == 0            # never below nothing
    assert R.measure([], ed) == {"signs": 5, "right": 0, "words": 2, "agree": 0}


def test_word_agrees_only_when_every_sign_is_matched():
    ed = R.corpus_words("pesto akiNtelo")
    assert R.measure(R.corpus_to_signs("pesto akiNtelo"), ed)["agree"] == 2
    assert R.measure(R.corpus_to_signs("pesto akiNtlo"), ed)["agree"] == 1        # te read as t: a sign lost
    assert R.measure(R.corpus_to_signs("pestoakiNtelo"), ed)["agree"] == 2        # word division is not scored


def test_align_marks_matched_edition_signs():
    d, same = R.align(list("axc"), list("abc"))
    assert d == 1 and same == [True, False, True]
    d, same = R.align(list("abc"), list("ac"))
    assert d == 1 and same == [True, True]


# --- the rule ---
def made_up(n_fhn=0):
    out = []
    for i in range(12):
        out.append({"id": f"REM {i:04d}", "rem": f"{i:04d}", "volume": 1, "kind": "funerary",
                    "stratum": ["funerary", "M"], "words": 12, "fhn": i < n_fhn, "open": "x"})
    return out


def test_pick_is_fixed_by_its_seed_and_fills_the_stratum():
    a, _ = R.pick(made_up())
    b, _ = R.pick(made_up())
    assert [e["id"] for e in a] == [e["id"] for e in b] and len(a) == R.ALLOC[("funerary", "M")]
    c, _ = R.pick(made_up(), seed=1)
    assert [e["id"] for e in c] != [e["id"] for e in a]


def test_fhn_first_but_no_more_than_half():
    chosen, _ = R.pick(made_up(n_fhn=6))
    n = R.ALLOC[("funerary", "M")]
    assert sum(e["fhn"] for e in chosen) == -(-n // 2)


def test_no_plate_is_passed_over_and_the_next_taken():
    entries = made_up()
    first, _ = R.pick(entries)
    skip = first[0]["id"]
    chosen, passed = R.pick(entries, has_plate=lambda e: e["id"] != skip)
    assert skip not in [e["id"] for e in chosen] and [e["id"] for e in passed] == [skip]
    assert len(chosen) == len(first)


def test_volumes_two_and_three_first_but_no_more_than_late():
    late = [{"id": f"REM 04{i:02d}", "rem": f"04{i:02d}", "volume": 2, "kind": "funerary",
             "stratum": ["funerary", "L"], "words": 60, "fhn": False, "open": "x"} for i in range(5)]
    chosen, _ = R.pick(made_up() + late)
    assert [e["volume"] for e in chosen][:R.LATE] == [2] * R.LATE             # taken first, no more than LATE
    assert [e["volume"] for e in chosen][R.LATE] == 1
    # the stratum is then filled as any other, and its place left can go to one more of them
    assert sum(e["stratum"] == ["funerary", "L"] for e in chosen) == R.ALLOC[("funerary", "L")]
    chosen, _ = R.pick(made_up() + late[:1])
    assert [e["volume"] for e in chosen][:2] == [2, 1]


def test_strata():
    assert R.stratum("funerary", 2) is None and R.stratum("funerary", 151) is None
    assert R.stratum("graffito", 40) == ("graffito", "M")                # graffiti of M and L are one stratum
    assert R.stratum("royal or temple (stela)", 30) == ("royal", "L")
    assert R.stratum("not known", 5) == ("other", "S")


def test_the_pool_from_the_public_table():
    p, left = R.pool()
    assert p and all(R.MIN_WORDS <= e["words"] <= R.MAX_WORDS for e in p)
    assert all(R.volume_of(e["rem"]) for e in p)
    assert not [e for e in p if e["id"] in ("REM 1003", "REM 0094")]            # too long for the pilot
    assert left["two REM numbers"] >= 1


def test_fhn_typed_texts_are_read_from_the_repo():
    f = R.fhn_typed()
    assert {"0097", "0247", "0277", "0278", "0103"} <= set(f)
    assert "ptteb" in f["0103"]                                               # the whole graffito, not the part


# --- the volumes ---
CAT = ("1. Meroitic Inscriptions REM 0003 Localisation actuelle Naga, in situ. Désignation originelle M. I. 3. "
       "Identification du monument Naga, temple du Lion. Dimensions / Description de l'inscription Texte en "
       "hiéroglyphique, gravé au nom de \"x\". Inscription sur trois colonnes, dont l'état de conservation est "
       "mauvais. Bibliographie Griffith 1911c, p. 52.")
PLATE = ("6 RÉPERTOIRE D'ÉPIGRAPHIE MÉROÏTIQUE REM 0003 Fac-similé de l'inscription M. I. 3 (Griffith 1911c, "
         "pl. XVII, 3) Fac-similé de l'inscription M. I. 3 (Griffith 1911c, pl. XVII,) Statue de bélier de Soba "
         "(Griffith 1911c, pl. XV)")


def test_catalogue_fields():
    c = R.catalogue(CAT)
    assert c["script"] == "hieroglyphic" and c["lines"] == 3 and c["unit"] == "colonne" and c["state"] == "mauvais"
    assert c["fields"]["Désignation originelle"].startswith("M. I. 3")


def test_captions_once_each_with_their_kind():
    caps = R.captions(PLATE)
    assert [c["kind"] for c in caps] == ["drawing", "photograph"]
    assert caps[0]["source"].startswith("Griffith 1911c")
    assert R.rem_on(PLATE) == ["0003"]


def test_catalogue_counts_only_the_inscription_sentence():
    c = R.catalogue("Description de l'inscription Texte en hiéroglyphique, gravé sur le fût d'une colonne. "
                    "Inscription sur quatre colonnes, dont l'état de conservation est bon.")
    assert (c["lines"], c["unit"]) == (4, "colonne")


def test_catalogue_wordings():
    c = R.catalogue("Description de l'inscription Texte en cursif, gravé au nom de \"x\". Inscription de six lignes, "
                    "dont l'état de conservation était, au moment de leur découverte, relativement bon (l'érosion).")
    assert (c["script"], c["lines"], c["unit"], c["state"]) == ("cursive", 6, "ligne", "relativement bon")
    c = R.catalogue("Description de l'inscription Épitaphe en cursif. Inscription sur deux bandes, dont l'état de "
                    "conservation est relativement bon.")
    assert (c["lines"], c["unit"]) == (2, "bande")
    c = R.catalogue("Description de l'inscription Texte en cursif. Inscription de dix-huit lignes (a, 10 ; b, 6).")
    assert c["lines"] == 18
    c = R.catalogue("Description de l'inscription Texte en cursif. Inscription d'une ligne, dont l'état de "
                    "conservation est bon.")
    assert (c["lines"], c["state"]) == (1, "bon")
    c = R.catalogue("Description de l'inscription Texte en cursif. 43 Une seule ligne, dont l'état est bon.")
    assert (c["lines"], c["unit"]) == (1, "ligne")
    c = R.catalogue("Description de l'inscription Texte en hiéroglyphique. Inscription en neuf colonnes, six en "
                    "méroïtique.")
    assert (c["script"], c["lines"], c["unit"]) == ("hieroglyphic", 9, "colonne")


def test_catalogue_or_plate_page():
    assert R.is_catalogue(CAT) and not R.is_catalogue(PLATE)
    assert R.is_catalogue("5. Inscriptions de Méroé REM 0407 (suite) Bibliographie Breasted 1908a, p. 98.")
    assert R.is_catalogue("5. Inscriptions de Méroé REM 0403 Garstang, Sayce et Griffith 1911, pp. 61sq. 721")
    assert not R.is_catalogue("730 RÉPERTOIRE D'ÉPIGRAPHIE MÉROÏTIQUE REM 0407 (suite) Fac-similé de l'inscription")


def test_plates_for_lettered_entries():
    idx = [{"rem": "0057A"}, {"rem": "0057B"}, {"rem": "0058"}, {"rem": "0091A"}]
    assert [e["rem"] for e in R.plates_for("0057", idx)] == ["0057A", "0057B"]
    assert [e["rem"] for e in R.plates_for("0091a", idx)] == ["0091A"]


def test_index_of_the_local_volumes():
    needs("data/sources/rem/index.jsonl")
    idx = R.read_index()
    assert len({e["rem"] for e in idx}) == len(idx)
    assert all(R.volume_of(e["rem"]) == e["volume"] for e in idx)


# --- the packs ---
SPEC = {"preview_size": [500, 1000], "page_size": [1000, 2000], "frames": {"pg": [100, 900]},
        "packs": {"P1": ["0001"], "P2": ["0002"]}, "second_reader": ["P1"]}


def test_box_on_page_widens_the_sides_within_the_frame():
    top, left, h, w = R.box_on_page([200, 100, 300, 200], SPEC, "pg", "photograph")
    assert (top, h) == (200, 200)                                             # top and bottom as drawn
    assert left == (200 - R.MARGIN) * 2 and w == (300 + R.MARGIN) * 2 - left   # sides widened
    top, left, h, w = R.box_on_page([10, 100, 490, 200], SPEC, "pg", "photograph")
    assert left == 104 and left + w == 896                                   # never past the frame
    top, left, h, w = R.box_on_page([200, 100, 200 + R.WIDE, 200], SPEC, "pg", "drawing")
    assert (left, left + w) == (104, 896)                                   # a wide drawing: frame to frame


def test_snap_takes_in_a_cut_line_and_stops_at_white():
    img = [[255] * 100 for _ in range(100)]
    for x in range(20, 80):
        for y in (40, 41, 42, 43):
            img[y][x] = 0                                                    # a line of ink, rows 40 to 43
    img[90][50] = 0                                                          # a caption further down
    top, left, h, w = R.snap(img, 30, 30, 12, 30)                            # a box that cuts the line
    assert (top, top + h) == (30, 44) and (left, left + w) == (20, 80)
    top, left, h, w = R.snap(img, 30, 30, 12, 30, frame=(25, 70))           # never onto the frame
    assert (left, left + w) == (31, 64)


def test_folders_one_reader_a_pack_and_a_second_for_some():
    assert R.folders(SPEC) == {"P1": "P1", "P2": "P2", "P1b": "P1"}


# --- the scores ---
def test_score_item_takes_fhn_first():
    eds = {"fhn": R.fhn_words("(1)qo pelmos"), "griffith": R.corpus_words("qo pelmoS")}
    r = R.score_item("(1) qo pelmoS?", eds)
    assert r["main"] == "fhn" and r["fhn"]["right"] == r["fhn"]["signs"] == 8 and r["unsure"] == 1
    r = R.score_item("qo [.]elmoS", {"griffith": R.corpus_words("qo pelmoS")})
    assert r["main"] == "griffith" and r["griffith"]["right"] == 7 and r["lost"] == 1


def test_pooled_and_verdict():
    rs = [{"main": "g", "g": {"signs": 90, "right": 81, "words": 10, "agree": 6}},
          {"main": "g", "g": {"signs": 10, "right": 10, "words": 2, "agree": 2}}]
    p = R.pooled(rs)
    assert (p["signs"], p["right"], p["share"], p["word_share"]) == (100, 91, 0.91, round(8 / 12, 4))
    assert R.verdict(0.95) == "GO" and R.verdict(0.9) == "LAYER" and R.verdict(0.849) == "NO-GO"


def test_editions_of_a_rem_number():
    e = R.editions("0277")
    assert set(e) == {"fhn", "griffith"} and all(isinstance(w, list) for w in e["fhn"])
    assert set(R.editions("0412")) == {"griffith"}


# --- the estimate ---
def test_recurrence_on_made_up_texts():
    forms = {f"T{i}": {"a", f"x{i}"} for i in range(40)}          # x_i once each; a in every text
    for i in range(0, 40, 2):
        forms[f"T{i}"].add(f"x{i + 1}")                           # x_{i+1} stands in two texts
    r = R.recurrence(forms, 20, 20, trials=50)
    assert 0 < r["share"] < 1 and r["share_two"] == 0             # no spelling stands in three texts
    assert R.recurrence({f"T{i}": {f"x{i}"} for i in range(10)}, 5, 5, trials=5)["share"] == 0


def test_extrapolate_a_straight_line_in_log():
    import math
    pts = [{"k": k, "share": 0.1 + 0.02 * math.log(k)} for k in (100, 200, 300)]
    v, slope = R.extrapolate(pts, 500)
    assert abs(v - (0.1 + 0.02 * math.log(500))) < 1e-3 and abs(slope - 0.02) < 1e-3


def test_word_rates_fall_back_to_the_script():
    idx = [{"rem": f"{i:04d}", "catalogue": {"script": "cursive", "unit": "ligne", "lines": 2}} for i in range(12)]
    idx += [{"rem": "0100", "catalogue": {"script": "cursive", "unit": "colonne", "lines": 1}}]
    held = {f"{i:04d}": [{"rem": [f"{i:04d}"], "words": 4}] for i in range(12)}
    held["0100"] = [{"rem": ["0100"], "words": 30}]
    rates, medians, n = R.word_rates(idx, held, mean=True)
    assert rates[("cursive", "ligne")] == 2 and n[("cursive", "colonne")] == 1
    assert rates[("cursive", "colonne")] == (12 * 4 + 30) / (12 * 2 + 1)           # too few: the script's rate
    rates, _, _ = R.word_rates(idx, held)
    assert rates[("cursive", "ligne")] == 2 and rates[("cursive", "colonne")] == 2   # the median: 30 is an outlier


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")])
