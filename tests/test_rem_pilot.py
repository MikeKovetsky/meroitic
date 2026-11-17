"""Checks for the REM pilot (src/rem_pilot.py).

  python3 -I tests/test_rem_pilot.py

The REM's pages and the readers' answers are local only, so the checks run on made-up texts and pages, and on the
public files; a check that reads a local file says so and is skipped where it is absent.
"""
import json, pathlib, re, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import rem_pilot as R                  # noqa: E402
from local_only import needs, run      # noqa: E402

PAGE = ROOT / "data/discovery/rem_pilot.md"


def figs():
    return json.loads(R.FIGURES.read_text(encoding="utf-8"))


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


def test_doubted_marks_the_sign_before_the_query():
    for text in ("ab? c:te?o", "(1) t?e [.] Sx?", "?ab"):
        assert len(R.doubted(text)) == len(R.corpus_to_signs(text)), text
    assert R.doubted("ab? c:te?o") == [False, True, False, True, False]          # te is one sign
    assert R.doubted("(1) t?e [.] Sx?") == [True, False, False, True]           # a query parts t from e
    assert R.doubted("?ab") == [False, False]                                    # a query before any sign marks none


def test_score_item_counts_the_faults():
    ed = {"griffith": R.corpus_words("abc de")}
    r = R.score_item("abk? de z?", ed)
    assert r["confusions"] == {"k for c": 1} and (r["extra"], r["missing"]) == (1, 0)
    assert (r["unsure"], r["wrong_marked"], r["right_marked"]) == (2, 2, 0)
    r = R.score_item("ab? de", ed)
    assert r["confusions"] == {} and (r["extra"], r["missing"]) == (0, 1) and (r["wrong_marked"], r["right_marked"]) == (0, 1)
    r = R.score_item("Sb se", {"griffith": R.corpus_words("mb se")})
    assert r["confusions"] == {"s for m": 1}                                     # the signs, not the letters


def test_once_open_counts_the_words_of_the_recurrences():
    words = R.corpus_words("abc de")
    assert R.once_open("abx de", words, ["abc", "de"], {"de"}) == {"words": 1, "agree": 1}
    assert R.once_open("abx de", words, ["abc", "de"], {"abc", "de"}) == {"words": 2, "agree": 1}
    assert R.once_open("abx de", words, ["abc", "dex"], {"de"}) is None         # the map's words are not the edition's


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


def test_catalogue_counts_above_twenty():
    def count(sentence):
        c = R.catalogue("Description de l'inscription Texte en cursif. " + sentence)
        return c["lines"], c["unit"]
    assert count("Inscription de vingt-quatre lignes, dont l'état est bon.") == (24, "ligne")
    assert count("Inscription de vingt et une lignes.") == (21, "ligne")
    assert count("Inscription de quarante deux lignes, dont l'état est bon.") == (42, "ligne")
    assert count("Inscription de dix -neuf lignes.") == (19, "ligne")                # the text layer parts the hyphen
    assert count("Inscription d'au moins trois lignes.") == (3, "ligne")
    assert count("Inscription sur une bande et deux colonnes.") == (1, "bande")       # the first count
    assert count("Inscription sur plusieurs lignes.") == (None, "")
    assert [R.number(w) for w in ("trente-cinq", "soixante-neuf", "vingt", "12", "plusieurs")] == [35, 69, 20, 12, None]


# made-up pages of two volumes, as the text layers give them: a section's title page, a plate, a catalogue that
# names another number before its running head, a catalogue whose commentary names a range of documents, a blank
# verso; in volume III a catalogue whose head has a footnote's mark glued to it, then the annexes and an index
MADE_UP_PAGES = {
    "v1/T5_0001_0000": "1. Meroitic Inscriptions : REM 0001 à REM 0137",
    "v1/T5_0002_0000": "2 RÉPERTOIRE D'ÉPIGRAPHIE MÉROÏTIQUE REM 0001 Dessin de la stèle (Auteur 1900, pl. 1)",
    "v1/T5_0003_0000": "Localisation actuelle Musée (voir REM 0002). Désignation originelle X 1. Identification du "
                       "monument 1. Meroitic Inscriptions REM 0001 Stèle. Dimensions / Description de l'inscription "
                       "Texte en cursif. Inscription de vingt-quatre lignes, dont l'état de conservation est bon. "
                       "Bibliographie Auteur 1900, p. 1.",
    "v1/T5_0004_0000": "4 RÉPERTOIRE D'ÉPIGRAPHIE MÉROÏTIQUE REM 0002 Table d'offrandes (Auteur 1901, pl. 2)",
    "v1/T5_0005_0000": "1. Meroitic Inscriptions REM 0002 Localisation actuelle Musée. Description de l'inscription "
                       "Épitaphe en cursif. Inscription sur deux bandes. Bibliographie Auteur 1901. 1. Les "
                       "documents REM 0002 à REM 0009 viennent d'une tombe.",
    "v1/T5_0006_0000": "",
    "v3/T2_0001_0000": "9. Textes publiés isolément depuis 1911. REM 1001 à REM 1278",
    "v3/T2_0002_0000": "2 RÉPERTOIRE D'ÉPIGRAPHIE MÉROÏTIQUE REM 1034 Dessin de l'inscription (Auteur 1958, pl. 3)",
    "v3/T2_0003_0000": "9. Textes publiés isolément depuis 1911 REM 10341 Localisation actuelle in situ. Description "
                       "de l'inscription Graffito en cursif. Inscription de trois lignes. Bibliographie Auteur 1958. "
                       "2. Cf. REM 1045.",
    "v3/T2_0004_0000": "Annexe 1. Les tables d'offrandes (REM 1045) REM 1050",
    "v3/T2_0005_0000": "Index A : numéros des REM REM 1060 REM 1061",
}


def test_index_files_pages_by_their_running_head():
    with tempfile.TemporaryDirectory() as d:
        for name, text in MADE_UP_PAGES.items():
            p = pathlib.Path(d) / f"{name}.html"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f"<div>{text}</div>", encoding="utf-8")
        idx = R.index(pathlib.Path(d))
    got = {e["rem"]: ([p["page"] for p in e["plates"]], (e["catalogue"] or {}).get("pages")) for e in idx}
    assert got == {"0001": (["T5_0002_0000"], ["T5_0003_0000"]), "0002": (["T5_0004_0000"], ["T5_0005_0000"]),
                   "1034": (["T2_0002_0000"], ["T2_0003_0000"])}
    c = {e["rem"]: e["catalogue"] for e in idx}
    assert (c["0001"]["lines"], c["0002"]["lines"], c["0002"]["unit"], c["1034"]["lines"]) == (24, 2, "bande", 3)
    assert R.is_title("4. Inscriptions de Méroé : REM 0401 à REM 0451")
    assert R.is_title("7. Inscriptions de Kawa. REM 0601 à REM 0707B") and not R.is_title(MADE_UP_PAGES["v1/T5_0005_0000"])


def test_held_by_the_rems_own_designation():
    assert [R.series_number(s) for s in ("Meroe 13", "Meroe 13.", "Meroe Il .", "Meroe2!.", "Meroe3l.", "Sh. l.",
                                          "Sh. lO.", "Sh. 19", "Kar. 47.", "Meroe", None)] == \
        [("Meroe", 13), ("Meroe", 13), ("Meroe", 11), ("Meroe", 21), ("Meroe", 31), ("Sh.", 1), ("Sh.", 10),
         ("Sh.", 19), None, None, None]
    entry = lambda rem, des: {"rem": rem, "catalogue": {"fields": {"Désignation originelle": des}}}   # noqa: E731
    idx = [entry("0413", "Meroe 13."), entry("0368", "Sh. l."), entry("0421", "Meroe2!."), entry("0256", "Kar. 56."),
           {"rem": "0500", "catalogue": None}]
    table = [{"id": "Meroe 13", "in_corpus_v6": True, "rem": []}, {"id": "Sh. 1", "in_corpus_v6": True, "rem": []},
             {"id": "Meroe 21", "in_corpus_v6": False, "rem": []},
             {"id": "REM 0256", "in_corpus_v6": True, "rem": ["0256"]}]
    assert set(R.held_numbers(table)) == {"0256"}
    held = R.held_numbers(table, idx)
    assert set(held) == {"0256", "0413", "0368"} and [r["id"] for r in held["0413"]] == ["Meroe 13"]


def test_the_corpus_is_the_texts_the_map_is_drawn_on():
    """A row added to corpus_v6 after the map was drawn (an ostracon, or a Faras text with its REM number) neither
    counts in the corpus nor holds a REM number: the estimate stays set against the texts the open spellings are."""
    table = [{"id": "REM 0256", "in_corpus_v6": True, "rem": ["0256"], "words": 5},
             {"id": "Meroe 13", "in_corpus_v6": True, "rem": [], "words": 3},
             {"id": "F.O. 1", "in_corpus_v6": True, "rem": [], "words": 4},
             {"id": "REM 0501", "in_corpus_v6": True, "rem": ["0501"], "words": 6},
             {"id": "REM 0300", "in_corpus_v6": False, "rem": ["0300"], "words": 9}]
    texts = {"REM 0256", "Meroe 13", "REM 0300"}
    assert [r["id"] for r in R.corpus_rows(table, texts)] == ["REM 0256", "Meroe 13"]
    idx = [{"rem": "0413", "catalogue": {"fields": {"Désignation originelle": "Meroe 13."}}}]
    assert set(R.held_numbers(table, idx, texts)) == {"0256", "0413"}
    assert "F.O. 1" not in R.corpus_rows(R.rows()) and len(R.corpus_rows(R.rows())) == 548 < sum(
        1 for r in R.rows() if r.get("in_corpus_v6"))


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


# --- the public figures and the page ---
SIGNS = {"a", "e", "o", "i", "y", "w", "b", "p", "m", "n", "ñ", "r", "l", "ḫ", "ẖ", "se", "s", "k", "q", "t", "te", "to",
         "d"}


def pct(x):
    return f"{100 * x:.1f}%"


def test_the_figures_add_up():
    f = figs()
    items, p, fa, oo = f["items"], f["pooled"], f["faults"], f["once_open"]
    m = [r[r["main"]] for r in items]
    assert (p["items"], p["signs"], p["right"], p["words"], p["agree"]) == (
        len(items), *(sum(x[k] for x in m) for k in ("signs", "right", "words", "agree")))
    assert p["share"] == round(p["right"] / p["signs"], 4) and p["word_share"] == round(p["agree"] / p["words"], 4)
    assert f["verdict"] == R.verdict(p["share"]) and f["bar"] == {"go": R.BAR_GO, "layer": R.BAR_LAYER, "expected": R.EXPECTED}
    assert f["pooled_griffith"] == p and f["pooled_fhn"]["items"] == 0 == f["agreement_of_two_readers"]["items"]
    # the faults: every sign of the edition is matched, read as another sign or missed; every sign of the reading
    # is matched, read as another or extra
    assert fa["substituted"] == sum(fa["by_pair"].values()) and fa["wrong"] == fa["substituted"] + fa["extra"] + fa["missing"]
    assert fa["wrong"] == p["signs"] - p["right"]
    assert [fa[k] for k in ("extra", "missing", "marked", "wrong_marked", "right_marked")] == [
        sum(r[k] for r in items) for k in ("extra", "missing", "unsure", "wrong_marked", "right_marked")]
    assert fa["wrong_marked"] + fa["right_marked"] <= fa["marked"]
    for r, x in zip(items, m):
        assert r["reading_signs"] == x["signs"] - r["missing"] + r["extra"] and x["agree"] <= x["words"], r["rem"]
        assert r["once_open"]["words"] <= x["words"] and r["once_open"]["agree"] <= min(x["agree"], r["once_open"]["words"])
    assert oo == {"items": len(items), "words": sum(r["once_open"]["words"] for r in items),
                  "agree": sum(r["once_open"]["agree"] for r in items), "share": round(oo["agree"] / oo["words"], 4)}
    # what the REM holds
    e, table = f["estimate"], R.rows()
    assert e["numbers"] == sum(e["by_section"].values()) == e["held"] + e["new"] == e["with_a_plate"] == e["with_a_catalogue"]
    assert e["by_section"] == {name: hi - lo + 1 for name, lo, hi in R.SECTIONS} and e["entries"] >= e["numbers"]
    assert e["new"] == sum(e["new_by_section"].values()) == sum(e["new_by_script"].values()) == e["new_with_a_plate"]
    assert all(e["new_by_section"][k] <= e["by_section"][k] for k in e["new_by_section"])
    assert sum(e["all_by_script"].values()) == e["numbers"] and all(v <= e["all_by_script"][k] for k, v in e["new_by_script"].items())
    assert max(e["new_lines_stated"], e["new_with_a_drawing_by_caption"]) <= e["new"] and e["held_by_designation"] <= e["held"]
    assert abs(e["words_new"] - sum(e["words_new_by_section"].values())) <= len(R.SECTIONS) / 2
    assert set(e["rates"]) == set(e["rate_pairs"]) and e["words_new"] <= e["words_new_at_the_mean_rate"]
    v6 = R.corpus_rows(table)
    assert (e["corpus_inscriptions"], e["corpus_words"]) == (len(v6), sum(r["words"] for r in v6))
    assert e["corpus_inscriptions"] == len(json.loads(R.MAP_TEXTS.read_text(encoding="utf-8"))["texts"]) == 548
    cc = e["caption_check"]
    assert cc["drawing_named_by_caption"] <= cc["drawing_by_eye"] <= cc["picks"] == sum(R.ALLOC.values())
    # what it would add
    rc, rr = e["recurrence"], e["recurrence"]["read_right"]
    assert rr == {"once_open": oo, "all_words": p["word_share"]}
    for k, ratio in (("by_words", e["words_new"] / e["corpus_words"]), ("by_words_mean", e["words_new_at_the_mean_rate"] / e["corpus_words"]),
                     ("by_inscriptions", e["new"] / e["corpus_inscriptions"])):
        v = rc[k]
        assert abs(v["ratio"] - ratio) < 0.002 and [x["k"] for x in v["points"]] == [120, 150, 180, 210], k
        assert all(abs(x["m"] - x["k"] * v["ratio"]) <= 1 and x["share_two"] <= x["share"] for x in v["points"]), k
        assert (v["share_at_corpus"], v["slope"]) == R.extrapolate(v["points"], e["corpus_inscriptions"]), k
        assert v["would_recur"] == round(rc["once_now"] * v["share_at_corpus"]), k
        assert v["would_reach_three_texts"] == round(rc["once_now"] * v["share_two_at_corpus"]), k
        assert v["would_recur_read_right"] == round(v["would_recur"] * oo["share"]), k
        assert v["would_recur_at_the_share_of_all_words"] == round(v["would_recur"] * p["word_share"]), k
    # what it would cost
    c = e["cost"]
    assert (c["items"], c["signs"]) == (p["items"], p["signs"]) and c["per_item"] == round(c["tokens"] / c["items"])
    assert c["per_sign"] == round(c["tokens"] / c["signs"], 1) and c["signs_an_inscription_pilot"] == round(c["signs"] / c["items"], 1)
    assert c["full_read_by_inscriptions"] == round(c["tokens"] / c["items"] * e["new"])
    assert abs(c["full_read"] / (c["tokens"] / c["signs"] * e["words_new"] * c["signs_per_word"]) - 1) < 0.002
    assert abs(c["full_read_mean"] / (c["tokens"] / c["signs"] * e["words_new_at_the_mean_rate"] * c["signs_per_word"]) - 1) < 0.002
    assert abs(c["signs_an_inscription_new"] - e["words_new"] * c["signs_per_word"] / e["new"]) < 0.1
    assert c["the_rest_at_this_rate"] == round(c["tokens"] / c["folders_run"] * (c["folders_planned"] - c["folders_run"]))
    assert c["folders_planned"] == len(R.folders({"packs": {f"P{k}": [] for k in range(1, 6)}, "second_reader": ["P1", "P3"],
                                                  "photo_only": {"PH": "P2"}}))


def test_the_figures_hold_counts_only():
    """No string of the figures is a reading or a caption: each is a REM number, a pack, a stratum, an edition, the
    verdict, or a pair of signs (a confusion's count); no key names a reading, a note, a figure or a text."""
    f = figs()

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield "key", path, k
                yield from walk(v, f"{path}/{k}")
        elif isinstance(o, list):
            for v in o:
                yield from walk(v, path)
        elif isinstance(o, str):
            yield "value", path, o
    vocab = {"griffith", "karanog", "fhn", "GO", "LAYER", "NO-GO", "funerary", "royal", "graffito", "other", "S", "M", "L"}
    for kind, path, s in walk(f):
        if kind == "value":
            assert re.fullmatch(r"\d{4}[A-Z]?|P\d|P\db|PH", s) or s in vocab, (path, s)
        else:
            assert s.lower() not in {"reading", "readings", "notes", "figures", "confusions", "text", "crops", "captions"}, (path, s)
    assert f["faults"]["by_pair"] and all(set(k.split(" for ")) <= SIGNS and k.count(" for ") == 1 for k in f["faults"]["by_pair"])


def test_the_page_says_what_the_figures_say():
    f, text = figs(), " ".join(PAGE.read_text(encoding="utf-8").split())
    p, e, fa, oo = f["pooled"], f["estimate"], f["faults"], f["once_open"]
    c, rc, bp = e["cost"], e["recurrence"], fa["by_pair"]
    signs, words, open_ = p["right"] / p["signs"], p["agree"] / p["words"], oo["agree"] / oo["words"]    # the shares from the counts
    mil = lambda x: round(x / 1e6)                                                       # noqa: E731
    both = lambda a, b: bp.get(f"{a} for {b}", 0) + bp.get(f"{b} for {a}", 0)            # noqa: E731
    shares = [r["griffith"]["right"] / r["griffith"]["signs"] for r in f["items"]]
    phrases = [
        # the answer
        f"A blind reader read {p['right']} of {p['signs']} signs right against Griffith ({pct(signs)}) and "
        f"{p['agree']} of {p['words']} words ({pct(words)}), below the bar's lowest tier ({round(100 * f['bar']['layer'])}%), "
        f"at {c['per_item']:,} subagent tokens an inscription",
        f"The REM holds {e['numbers']} inscriptions, not 1,278: {e['new']} are new to the corpus, about {round(e['words_new'], -2):,} words.",
        f"Reading them all this way would cost about {mil(c['full_read'])} to {mil(c['full_read_by_inscriptions'])} million tokens, and "
        f"about {rc['by_words']['would_recur_read_right']} of the {rc['once_now']:,} open spellings",
        # the scores
        f"**{c['tokens']:,} subagent tokens for {c['items']} inscriptions**",
        f"(7 of the {c['folders_planned']} readers' folders) would have taken about {c['the_rest_at_this_rate'] / 1e6:.1f} million more",
        f"| **All four** | | **{p['right']} of {p['signs']}** | **{pct(signs)}** | **{p['agree']} of {p['words']} "
        f"({pct(words)})** | {fa['marked']} |",
        f"**Verdict: {f['verdict']}** (below {round(100 * f['bar']['layer'])}%)",
        f"The four lie between {pct(min(shares))} and {pct(max(shares))}",
        f"Of the {fa['wrong']} signs wrong ({fa['substituted']} read as another sign, {fa['extra']} that only the reading has, "
        f"{fa['missing']} missed), the 3-shaped signs m, s, ẖ and q account for "
        f"{sum(n for k, n in bp.items() if set(k.split(' for ')) <= {'m', 's', 'ẖ', 'q'})} of the {fa['substituted']}, e against l for "
        f"{both('e', 'l')}, p against k for {both('p', 'k')} and d against ne for {both('d', 'ñ')}. The commonest single fault is the "
        f"sign s written for m ({bp['s for m']}).",
        f"Of the {fa['substituted'] + fa['extra']} signs it wrote wrong (read as another sign, or only in the reading), "
        f"{fa['wrong_marked']} carry its `?`; of its {fa['marked']} marks, {fa['right_marked']} sit on signs that are right.",
        f"it read {oo['agree']} of {oo['words']} right ({pct(open_)})",
        # what the REM holds
        f"the REM gives **{e['numbers']} numbers in nine sections**, not 1,278 (the numbering leaves gaps between sections), as "
        f"{e['entries']} entries with their lettered parts. Every number has a page of plates and a catalogue page.",
        f"| **All** | **{e['numbers']}** | **{e['new']}** | **{e['words_new']:,}** |",
        f"**{e['held']} of the {e['numbers']} are in `corpus_v6`; {e['new']} are new** to it: the corpus would go from "
        f"{e['corpus_inscriptions']} to about {e['corpus_inscriptions'] + e['new']:,} inscriptions",
        f"{e['held_by_designation']} of the {e['held']} are Griffith's Meroë and Shablul texts",
        f"{e['new_by_section']['Faras'] + e['new_by_section']['Ostraca of several sites']} of the {e['new']} are the Faras texts and the ostraca",
        f"about {round(e['words_new'], -2):,} new words, under half the corpus's {e['corpus_words']:,}",
        f"({e['new_lines_stated']} of the {e['new']} do)",
        f"({e['rates']['cursive ligne']:.1f} a cursive line, {e['rates']['cursive bande']} a cursive band, "
        f"{e['rates']['hieroglyphic colonne']} a hieroglyphic column). The mean gives {e['words_new_at_the_mean_rate']:,}, the high end.",
        f"**Script of the new:** {e['new_by_script']['cursive']} cursive, {e['new_by_script']['hieroglyphic']} hieroglyphic, "
        f"{e['new_by_script']['not stated']} not stated.",
        f"for {e['new_with_a_drawing_by_caption']} of the {e['new']} a caption names a drawing",
        f"the captions named a drawing for {e['caption_check']['drawing_named_by_caption']} of the {e['caption_check']['drawing_by_eye']} that have one",
        # the cost
        f"**{round(c['per_sign']):,} tokens a sign of the edition**, and {c['signs_per_word']} signs a word: **about {mil(c['full_read'])} "
        f"million subagent tokens** for the {e['new']} ({mil(c['full_read_mean'])} million at the mean count of words). By the "
        f"inscription, {c['per_item']:,} each, it would be **{mil(c['full_read_by_inscriptions'])} million**",
        f"(about {round(c['signs_an_inscription_new'])} signs each, against {round(c['signs_an_inscription_pilot'])} in the pack)",
        # what it would add
        f"| Recur and read right ({pct(open_)}) | At {pct(words)}, the share of all words |",
        f"about {round(rc['by_words']['would_recur'], -1)} of the {rc['once_now']:,} a second text if every word were read right, and "
        f"about {rc['by_words']['would_reach_three_texts']} of them the three texts",
        f"With the words this reader gets right it would give about {rc['by_words']['would_recur_read_right']}",
        f"the reader got {oo['agree']} of {oo['words']} right ({pct(open_)}), fewer than its {pct(words)} of all words",
        # the recommendation and the files
        f"the full read would cost {mil(c['full_read'])} to {mil(c['full_read_by_inscriptions'])} million tokens for about "
        f"{rc['by_words']['would_recur_read_right']} spellings with a second text",
        f"{e['numbers']} inscriptions, {e['new']} of them not in the corpus",
        f"should read about {e['corpus_inscriptions'] + e['new']:,}.",
        f"| Reader of pack P1 (4 inscriptions) | {c['tokens']:,} |",
        f"**{e['held_by_designation']} texts the corpus holds were counted as new:**",
        f"({pct(words)}) for the spellings that stand in one text; it reads those worse ({pct(open_)})",
    ]
    for ph in phrases:
        assert ph in text, ph
    names = {"Meroitic Inscriptions": "*Meroitic Inscriptions* (Griffith)", "Karanog and Shablul": "Karanòg and Shablul",
             "Meroe": "Meroë"}
    for name, lo, hi in R.SECTIONS:
        row = (f"| {names.get(name, name)}, {lo:04d} to {hi:04d} | {e['by_section'][name]} | {e['new_by_section'][name]} | "
               f"{e['words_new_by_section'][name]:,} |")
        assert row in text, row
    labels = {"by_words": "By words, median", "by_words_mean": "By words, mean", "by_inscriptions": "By inscriptions"}
    for k, label in labels.items():
        v = rc[k]
        first = f"{v['would_recur']} of {rc['once_now']:,}" if k == "by_words" else f"{v['would_recur']}"
        row = (f"| {label} ({v['ratio']:.2f}) | {first} ({pct(v['share_at_corpus'])}) | {v['would_reach_three_texts']} | "
               f"{v['would_recur_read_right']} | {v['would_recur_at_the_share_of_all_words']} |")
        assert row in text, row
    for r in f["items"]:
        g = r["griffith"]
        row = rf"\| REM {r['rem']} \([^|]*\) \| [^|]* \| {g['right']} of {g['signs']} \| {re.escape(pct(g['right'] / g['signs']))} \| " \
              rf"{g['agree']} of {g['words']} \| {r['unsure']} \|"
        assert re.search(row, text), r["rem"]


def test_the_summaries_quote_the_figures():
    e = figs()["estimate"]
    c, rc = e["cost"], e["recurrence"]
    text = " ".join((ROOT / "NEXT_STEPS.md").read_text(encoding="utf-8").split())
    assert (f"{e['new']} are new to `corpus_v6`, about {round(e['words_new'], -2):,} words" in text
            and f"would cost about {round(c['full_read'] / 1e6)} to {round(c['full_read_by_inscriptions'] / 1e6)} million tokens and give "
                f"about {rc['by_words']['would_recur_read_right']} of the {rc['once_now']:,} open" in text)
    index = (ROOT / "data/INDEX.md").read_text(encoding="utf-8")
    assert "`data/sources/rem/`" in index and f"the index of the {e['entries']} entries" in index and "rem_pilot.md" in index


# --- with the local files ---
LOCAL = ("data/sources/rem/text", "data/sources/rem/index.jsonl", "data/sources/rem/pilot/spec.json",
         "data/sources/rem/pilot/key.json", "data/sources/rem/pilot/packs", "data/sources/rem/pilot/tokens.json",
         "data/sources/v6/analysts/glosses.jsonl")


def test_the_figures_are_the_count_of_the_local_files():
    """The index again from the volumes' text layers is the local index; the scores from the reader's answers and the
    estimate from both give the public figures (written to a folder of the check's own, not over the local files)."""
    needs(*LOCAL)
    assert json.loads(json.dumps(R.index(), ensure_ascii=False)) == R.read_index()
    keep = R.SCORES, R.ESTIMATE, R.FIGURES
    with tempfile.TemporaryDirectory() as d:
        R.SCORES, R.ESTIMATE, R.FIGURES = (pathlib.Path(d) / n for n in ("scores.json", "estimate.json", "figures.json"))
        try:
            s = R.score()
            out = R.public(s, R.estimate(s))
        finally:
            R.SCORES, R.ESTIMATE, R.FIGURES = keep
    assert json.loads(json.dumps(out, ensure_ascii=False)) == figs()


def test_no_reading_of_the_rem_is_public():
    """The words the reader wrote that no public edition has (its own readings of the plates) stand nowhere in the
    public files of the pilot."""
    needs("data/sources/rem/pilot/packs", "data/sources/rem/pilot/key.json")
    key = json.loads(R.KEY.read_text(encoding="utf-8"))
    words = lambda t: {w for w in re.split(r"[\s:]+", re.sub(r"\(\d+\)|\[\.\]|\?", " ", t or "")) if len(w) >= 4}   # noqa: E731
    public = set().union(*(words(r.get("open_text")) for r in R.rows()))
    read = set().union(*(words(o.get("reading")) for folder in key for o in R.answers(folder).values()))
    assert read                                                                            # the reader answered
    mine = read - public
    files = [PAGE, R.FIGURES, ROOT / "tests/test_rem_pilot.py", ROOT / "NEXT_STEPS.md", ROOT / "data/INDEX.md"]
    for path in files:
        text = path.read_text(encoding="utf-8")
        hits = sorted(w for w in mine if re.search(rf"(?<![A-Za-z]){re.escape(w)}(?![A-Za-z])", text))
        assert not hits, (path.name, len(hits))


if __name__ == "__main__":
    run([(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")])
