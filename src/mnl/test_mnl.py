"""Tests of the Newsletter tools on made-up lines (no text from the scans or from Otten's files).

  python3 -I src/mnl/test_mnl.py
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mnl_build as B  # noqa: E402
import mnl_dedupe as D  # noqa: E402
import mnl_score as M  # noqa: E402
import mnl_signs as S  # noqa: E402
import mnl_round as R  # noqa: E402


class References(unittest.TestCase):
    def test_millet_thesis_reads_the_text_once_without_the_translation(self):
        text = ("# header\n\ntEbe : abEl : kdes\n\n# here are parts of the text that are translated by Millet:\n"
                "tEbe : abEl\tthe word\n")
        self.assertEqual(S.millet_thesis(text).split(), ["tobe", "abol", "kdese"])

    def test_fhn_keeps_the_first_of_two_readings_and_lowers_dotted_letters(self):
        self.assertEqual(S.fhn("abr ldr tdr (EITXER-LDR-OR-TDR) kdi").split(), ["abr", "ldr", "kdi"])
        self.assertEqual(S.fhn("pl Bmnt yo [k|m]e").split(), ["pl", "bmnt", "yo", "ke"])


class Alternatives(unittest.TestCase):
    def test_a_reading_with_brackets_of_its_own(self):
        self.assertEqual(S.first_reading("KB(T/(((D)))L)I,, WE"), ("KBTI,, WE", 1))
        self.assertEqual(S.first_reading("( ((.)) (MA/PA)/  (MA/PA/T) )RE"), (" ((.)) MARE", 2))

    def test_gaps_and_restored_signs_keep_their_brackets(self):
        self.assertEqual(S.first_reading("((BR))ATE (())"), ("((BR))ATE (())", 0))

    def test_a_reading_cut_by_the_scans_edge_ends_there(self):
        self.assertEqual(S.first_reading("TMD(E/I>>"), ("TMDE ", 1))

    def test_a_bracket_left_open_by_a_slip_keeps_the_typed_letters(self):
        self.assertEqual(S.first_reading("LIT(K/P#ES,, ABR"), ("LITK/P#ES,, ABR", 0))
        self.assertEqual(S.first_reading("BKE(#/ #,,, TQLJ 1,,, MKD WI>>"), ("BKE#/ #,,, TQLJ 1,,, MKD WI ", 0))

    def test_a_reading_run_over_the_line_end(self):
        self.assertEqual(S.heyler_lines(["AR(MLE/MTI/(MLI/MLI)", ")KG,, (L/T)BOK,,"]), [("ARMLEKG,, LBOK,,", 2)])
        self.assertEqual(S.heyler_lines(["WIPAN,, (T", "COD? KI/TOD? ((B))KI),,"]), [("WIPAN,, TOD? KI,,", 1)])

    def test_no_run_on_when_the_next_line_does_not_close_it(self):
        self.assertEqual([t for t, _ in S.heyler_lines(["LIT(K/P#ES,,", "WOTE,, (A/B),,"])], ["LITK/P#ES,,", "WOTE,, A,,"])

    def test_continuation_mark_and_analysis_go(self):
        self.assertEqual(S.heyler_lines(["1CMB,, V'TE'RI KDOWI,,"]), [("MB,, VRI KDOWI,,", 0)])
        self.assertEqual(S.heyler("MB,, VRI CKDOWI,,").split(), ["mb", "teri", "kdowi"])
        self.assertEqual([s for s, _ in R.parse("MB,, CMKE,,")[1]], ["m", "k", "e"])


class FirstPrinting(unittest.TestCase):
    def test_the_second_printing_goes_with_its_continuation_lines(self):
        lines = [("p1", "?", 10, "1CWOR,, TMDEL,,"), ("p1", "?", 10, "K,, NPT,,"),
                 ("p1", "?", 10, "2CWOR,, TMDEL,,"), ("p1", "?", 10, "K,, NPT,, ABEL,,"), ("p1", "?", 11, "ABEL,,")]
        self.assertEqual([b for *_, b in S.first_printing(lines)], ["WOR,, TMDEL,,", "K,, NPT,,", "ABEL,,"])

    def test_numbered_versions_keep_the_first(self):
        lines = [("p1", "?", 34, "1 MBWI,, ERESWIT,,"), ("p1", "?", 34, "2 MBWI,, ERESWIL,,")]
        self.assertEqual([b for *_, b in S.first_printing(lines)], ["MBWI,, ERESWIT,,"])

    def test_versions_marked_by_other_digits_keep_the_first_printed(self):
        lines = [("p1", "?", 7, "3 AB *M*L*I,, TMDEL OWI"), ("p1", "?", 7, "2 AB*QI,, TMDEL OWI,,"), ("p2", "?", 8, "4 NOB,, ERESWIT,,")]
        self.assertEqual([b for *_, b in S.first_printing(lines)], ["AB *M*L*I,, TMDEL OWI", "4 NOB,, ERESWIT,,"])

    def test_a_lone_second_printing_goes(self):
        lines = [("p1", "?", 9, "WOR,, TMDEL,,"), ("p1", "?", 9, "2CWOR,, TMDEK,, NPT,,")]
        self.assertEqual([b for *_, b in S.first_printing(lines)], ["WOR,, TMDEL,,"])

    def test_a_line_typed_twice_is_kept_once(self):
        lines = [("p1", "1099", 5, "TMDSLW,, YEKOLI,,"), ("p2", "1099", 5, "TMDSLW,, YEKOL,,")]
        self.assertEqual(len(S.first_printing(lines)), 1)

    def test_the_test_mode_parses_first_printings_only(self):
        rows = [("p1", "?", 1, "1CMB,, TEKE,,"), ("p1", "?", 1, "2CMB,, TEKE,,"), ("p1", "?", 1, "WEZLI,, DOLIT,,")]
        words = [w for t, _ in S.heyler_lines([b for *_, b in S.first_printing(rows)]) for w in R.parse(t)]
        self.assertEqual(len(words), 2)


def corpus(line, old_s=False, **kw):
    """One printed line to the corpus spelling, as print_row does it."""
    return B.to_corpus(B.clean_print(line, **kw).replace(":", " "), old_s)


class PrintedIssues(unittest.TestCase):
    def test_line_numbers_after_a_side_label_or_counting_on_from_x_plus_1(self):
        side = ["(r) 1 kabare", "di : mte", "pasoli :", "aqoẖe", "5 tedi ark"]
        self.assertEqual(B.strip_line_numbers(side), ["kabare", "di : mte", "pasoli :", "aqoẖe", "tedi ark"])
        self.assertEqual(B.strip_line_numbers(["X + 1 nabida ko,,", "2 tamore,, sab ...."]),
                         ["nabida ko,,", "tamore,, sab ...."])

    def test_the_number_of_a_text_of_one_line(self):
        self.assertEqual(B.strip_line_numbers(["1 (abri ko)reli"]), ["(abri ko)reli"])
        self.assertEqual(B.strip_line_numbers(["4 l..."]), ["4 l..."])

    def test_restorations_in_round_brackets_keep_their_letters(self):
        self.assertEqual(corpus("Dm(tᵉ)ke lo wi,, (pare so)ki", restored_in_parens=True), "dmteke lo wi pare Soki")
        self.assertEqual(corpus("ke(a)... amresᵉ(?) dos(b)"), "ke... amres doS")

    def test_unread_and_unidentified_signs_are_lost_signs(self):
        self.assertEqual(corpus("...dakimre,, p·odase... ab¤de"), "...dakimre p.odas... ab.de")
        self.assertEqual(corpus("... 2□3□□..."), "... 2 3 ...")

    def test_a_doubtful_s_with_a_caron_stays_plain_s(self):
        self.assertEqual(corpus("ṣ̌ab : wo s", old_s=True), "Sab wo s")

    def test_old_spelling_rows_say_line_ends_were_taken_as_word_ends(self):
        row = {"file": "MeroNews21", "lines": ["1. Pr [te] : šabe", "2. [taš] : ḷedewi", "3. tabḫeli : s : Mrko"]}
        text, ends = B.print_row(None, row)
        self.assertEqual(ends, "line ends taken as word ends")
        self.assertEqual(text, "pr te Sabe taS ledewi tabxeli s mrko")


class Printout(unittest.TestCase):
    def test_a_text_says_how_many_line_ends_a_bracket_ran_over(self):
        model = R.Model([tuple("abr")])
        text, how, alts, ran_over = B.printout_text(model, ["ABR,, AR(MLE/MTI/(MLI/MLI)", ")KG,, WI,,", "KDI,,"])
        self.assertEqual((text, alts, ran_over), ("abr armlekx wi kdi", 1, 1))


class Alignment(unittest.TestCase):
    def test_each_kind_of_difference_is_counted_once(self):
        self.assertEqual(M.align(list("abxde"), list("abcd")),
                         [("=", 0, 0), ("=", 1, 1), ("s", 2, 2), ("=", 3, 3), ("i", 4, None)])
        self.assertEqual(M.align(list("acd"), list("abcd")), [("=", 0, 0), ("d", None, 1), ("=", 1, 2), ("=", 2, 3)])

    def test_free_ends_leave_out_what_only_one_side_runs_on_into(self):
        self.assertEqual(M.align(list("bcd"), list("abcdef"), free_ref_ends=True), [("=", 0, 1), ("=", 1, 2), ("=", 2, 3)])
        self.assertEqual(M.align(list("xxabcyy"), list("abc"), free_read_ends=True), [("=", 2, 0), ("=", 3, 1), ("=", 4, 2)])


def tool(*args):
    """Run one of the tools as a user does; returns its exit code and what it printed on stderr."""
    cmd = ["bash"] if args[0].endswith(".sh") else [sys.executable, "-I"]
    p = subprocess.run(cmd + [str(HERE / args[0]), *args[1:]], capture_output=True, text=True)
    return p.returncode, p.stderr


class Stops(unittest.TestCase):
    """Without their arguments, or without their local-only inputs (README, Data), the tools stop with a message."""

    def test_without_arguments_each_tool_gives_its_usage(self):
        for name in ("mnl_build.py", "mnl_dedupe.py", "mnl_corpus.py", "mnl_score.py", "mnl_round.py", "round_tab2.py",
                     "rebuild.sh"):
            code, err = tool(name)
            with self.subTest(name):
                self.assertEqual(code, 1)
                self.assertIn("usage: bash rebuild.sh" if name == "rebuild.sh" else f"python3 -I {name}", err)
                self.assertNotIn("Traceback", err)

    def test_without_the_local_files_each_tool_names_them(self):
        with tempfile.TemporaryDirectory() as d:
            for args in [("mnl_build.py", d, f"{d}/raw", f"{d}/out.jsonl"), ("mnl_dedupe.py", d, f"{d}/t.jsonl"),
                         ("mnl_corpus.py", d, f"{d}/t.jsonl", f"{d}/c.jsonl"), ("mnl_score.py", "pair", f"{d}/a.txt", f"{d}/b.txt"),
                         ("mnl_round.py", "test", d, f"{d}/r.txt", f"{d}/f.txt"), ("round_tab2.py", f"{d}/r.txt", f"{d}/f.txt", "p1"),
                         ("rebuild.sh", d, f"{d}/out")]:
                code, err = tool(*args)
                with self.subTest(args[0]):
                    self.assertEqual(code, 1)
                    self.assertTrue(err.startswith("missing "), err)
                    self.assertIn(f"{d}/r.txt" if args[0] == "round_tab2.py" else
                                  f"{d}/a.txt" if args[0] == "mnl_score.py" else f"{d}/data/corpus_v3.jsonl", err)
                    self.assertNotIn("Traceback", err)

    def test_a_harvest_folder_without_readings_is_not_zero_texts(self):
        with tempfile.TemporaryDirectory() as d:
            inventory = Path(d, "data/sources/mnl/readings/inventory")
            inventory.mkdir(parents=True)
            for L in "ABCD":
                (inventory / f"{L}.json").write_text('{"texts": []}')
            Path(d, "data/corpus_v3.jsonl").write_text(json.dumps({"id": "T1", "src": "funerary", "text": "abr"}) + "\n")
            Path(d, "raw").mkdir()
            code, err = tool("mnl_build.py", d, f"{d}/raw", f"{d}/out.jsonl")
            self.assertEqual(code, 1)
            self.assertTrue(err.startswith(f"no readings in {d}/raw"), err)
            self.assertFalse(Path(d, "out.jsonl").exists())


class RoundLetters(unittest.TestCase):
    def test_a_long_word_weighs_the_corpus_model_as_a_short_one_does(self):
        model = R.Model([tuple("toto")] * 50)
        word = [("t", None)] + [("0", "D?"), ("t", None)] * 8
        weight = R.LM_WEIGHT
        try:
            R.LM_WEIGHT = 0.0                              # the reader alone: D? is d more often than o
            self.assertEqual(R.settle(model, word)[0][1::2], ["d"] * 8)
        finally:
            R.LM_WEIGHT = weight


def row(ident, year, rem, file, grams, kind="print", idents=("1",), in_corpus="", words=5):
    return {"id": ident, "source": f"Meroitic Newsletter ({year})", "rem": rem, "file": file, "kind": kind, "words": words,
            "lines": [f"{i} | {i}/1 | X" for i in idents], "_g": set(grams), "tested": len(grams) >= D.MIN, "in_corpus": in_corpus}


NAME = ["abcdef", "bcdefg", "cdefgh", "defghi", "efghij", "fghijk"]
FORMULA = ["lmnopq", "mnopqr", "nopqrs", "opqrst", "pqrstu", "qrstuv"]


class Editions(unittest.TestCase):
    def test_two_rem_numbers_on_the_pages_are_two_inscriptions(self):
        rows = [row("REM 2001", 1971, "2001", "MeroNews6", NAME), row("REM 2002", 1977, "2002", "MeroNews18", NAME)]
        D.editions(rows, ["", ""])
        self.assertEqual([r["same_as"] for r in rows], ["", ""])

    def test_a_number_worked_out_from_the_order_does_not_count(self):
        rows = [row("REM 2003", 1971, "2003", "MeroNews6", NAME, kind="printout", idents=("~2003",)),
                row("REM 2004", 1971, "2004", "MeroNews6", NAME + ["ghijkl"], kind="printout", idents=("~2004",), words=9)]
        D.editions(rows, ["", ""])
        self.assertEqual(rows[0]["same_as"], "REM 2004 (Meroitic Newsletter (1971))")

    def test_the_same_rem_in_two_issues_is_compared_even_when_too_short_to_test(self):
        rows = [row("REM 2005", 1971, "2005", "MeroNews6", NAME[:3], kind="printout", idents=("~2005",)),
                row("Site 3, REM 2005", 2000, "2005", "MeroNews27c", NAME[2:])]
        D.editions(rows, ["abcxi#klmno", "abcdxi#klmnp"])
        self.assertEqual(rows[0]["same_as"], "Site 3, REM 2005 (Meroitic Newsletter (2000))")

    def test_texts_alike_only_in_their_formulae_are_two_texts(self):
        rows = [row("REM 2006", 1971, "", "MeroNews6", NAME + FORMULA), row("REM 2007", 1971, "", "MeroNews6", FORMULA + ["ghijkl"])]
        D.editions(rows, ["", ""], frozenset(FORMULA))
        self.assertEqual([r["same_as"] for r in rows], ["", ""])

    def test_a_later_reprint_of_a_part_gives_way_to_the_fuller_text(self):
        more = ["ghijkl", "hijklm", "ijklmn", "jklmno", "klmnop", "rstuvw", "stuvwx", "tuvwxy"]
        rows = [row("REM 2009", 1971, "2009", "MeroNews6", NAME + more, words=30), row("REM 2009A", 2002, "2009A", "MeroNews29e", NAME),
                row("REM 2009A", 2001, "2009A", "MeroNews28", NAME)]       # the 2001 part first goes with the 2002 part
        D.editions(rows, ["", "", ""])
        self.assertEqual([r["same_as"] for r in rows], ["", "REM 2009 (Meroitic Newsletter (1971))", "REM 2009 (Meroitic Newsletter (1971))"])

    def test_an_inscription_edited_again_under_another_number_keeps_the_later_edition(self):
        more = ["ghijkl", "hijklm", "ijklmn", "jklmno", "klmnop", "rstuvw", "stuvwx", "tuvwxy"]
        rows = [row("REM 1041", 1971, "1041", "MeroNews6", NAME + more, kind="printout", idents=("1041",), words=30),
                row("REM 1361A", 2002, "1361A", "MeroNews29e", more[:6], words=20), row("REM 1041A", 2002, "1041A", "MeroNews29e", NAME)]
        D.editions(rows, ["", "", ""])
        self.assertEqual([r["same_as"] for r in rows], ["REM 1361A and the rest of that edition (Meroitic Newsletter (2002))", "", ""])

    def test_an_inscription_with_one_edition_in_the_corpus_is_in_the_corpus(self):
        rows = [row("REM 2008", 1971, "2008", "MeroNews6", NAME, in_corpus="T0001"), row("REM 2008", 1977, "2008", "MeroNews18", NAME)]
        D.editions(rows, ["", ""])
        self.assertEqual(rows[0]["same_as"], "REM 2008 (Meroitic Newsletter (1977))")
        self.assertEqual(rows[1]["in_corpus"], "T0001 (as REM 2008, Meroitic Newsletter (1971))")


if __name__ == "__main__":
    unittest.main()
