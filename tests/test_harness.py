"""Checks for the test harness: scoring, leaks into blind tasks, the corpus build.

  python3 -I tests/test_harness.py
"""
import contextlib, io, itertools, json, math, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import build_extra, build_tasks, clean_v2, cloze, cloze_families, cognates, corpus, score, synth   # noqa: E402


def brute_p(answer, key, c):
    words, meanings = list(key), list(key.values())
    hits = [sum(answer.get(w) == m for w, m in zip(words, perm)) for perm in itertools.permutations(meanings)]
    return sum(h >= c for h in hits) / len(hits)


def test_p_value_is_exact():
    key = {f"w{i}": f"m{i}" for i in range(6)}
    full = dict(key)
    partial = {"w0": "m0", "w1": "m1", "w2": "m3"}
    repeated = {"w0": "m0", "w1": "m0", "w2": "m0", "w3": "m2", "w4": None}
    for answer in (full, partial, repeated, {}):
        for c in range(7):
            assert math.isclose(score.p_at_least(answer, key, c), brute_p(answer, key, c), abs_tol=1e-12), (answer, c)
    key18 = {f"w{i}": f"m{i}" for i in range(18)}
    assert math.isclose(score.p_at_least(key18, key18, 18), 1 / math.factorial(18))   # never 0
    assert score.p_at_least(key18, key18, 0) == 1


def test_meaning_must_be_an_option():
    options = ["god", "good", "water"]
    assert score.option("goods", options) is None        # near a real option, still not one
    assert score.option(" God ", options) == "god"
    assert score.option("Begotten by father", ["begotten by (father)"]) == "begotten by (father)"


def test_score_joins_answers_to_key():
    key = {"a": "god", "b": "good", "c": "water"}
    ans = {"assignments": [{"word": "a", "meaning": "God", "confidence": 2},
                           {"word": "b", "meaning": "goods", "confidence": 5},
                           {"word": " c ", "meaning": "water", "confidence": "4"}]}
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "answer.json"
        p.write_text(json.dumps(ans))
        r = score.score("X", key, p)
    assert (r["correct"], r["unmatched"], r["answered"]) == (2, 1, 3), r
    assert (r["confident"], r["confident_correct"]) == (2, 1), r       # " c " and "4" still count


def test_corpus_lines_carry_no_ids():
    rows = [{"id": "hamadab", "text": "a b c"}, {"id": "T0001", "text": " ".join(["qo"] * 150)}]
    block = build_tasks.corpus_block(rows)
    assert "hamadab" not in block and "T0001" not in block, block[:80]
    assert [l.split(":")[0] for l in block.split("\n")] == ["L0000", "L0001.1", "L0001.2"]


def test_existing_task_is_never_rebuilt():
    old = build_tasks.BLIND
    with tempfile.TemporaryDirectory() as d:
        build_tasks.BLIND = Path(d)
        try:
            (Path(d) / "S_f0").mkdir()
            (Path(d) / "S_f0" / "task.md").write_text("built")
            try:
                build_tasks.fresh(["R_f0", "S_f0"])
                raise AssertionError("fresh() rebuilt a folder that holds a task")
            except SystemExit:
                pass
            assert not (Path(d) / "R_f0").exists()          # nothing written before the refusal
            build_tasks.fresh(["R_f1"])
            assert (Path(d) / "R_f1").is_dir()
        finally:
            build_tasks.BLIND = old


def test_keys_are_merged_not_replaced():
    old = build_tasks.ROOT
    with tempfile.TemporaryDirectory() as d:
        build_tasks.ROOT = Path(d)
        try:
            build_tasks.save_keys({"Y_f0": {"x": "water"}})
            build_tasks.save_keys({"R_f0": {"ato": "water"}})
            keys = json.loads((Path(d) / "runs/keys/step0.json").read_text())
        finally:
            build_tasks.ROOT = old
    assert set(keys) == {"Y_f0", "R_f0"}


def test_spelling_keeps_words_whole():
    assert corpus.norm("li *tk*k ymope") == "li tkk ymope"                 # star marks a doubtful sign
    assert corpus.norm("sy*e(te) pXe*te") == "syete pXete"                 # restored letters stay in the word
    assert corpus.norm("wE Si SErey?i atE") == "wo Si Soreyi ato"
    assert corpus.norm("teNke l lbr tbr (EITXER-LBR-OR-TBR) ke") == "teNke l lbr ke"
    assert corpus.norm("ro[.]te trw[…]nide") == "ro te trw nide"           # a lost sign still ends a word


def test_each_narrative_once():
    rows = [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]
    nar = {r["id"]: r["text"] for r in rows if r["src"] == "narrative"}
    assert sorted(nar) == ["hamadab", "kharamadoye", "tanyidamani"]
    long_funerary = [r for r in rows if r["src"] == "funerary" and len(r["text"].split()) >= 100]
    copies = [r["id"] for r in long_funerary for t in nar.values() if corpus.same_text(r["text"], t)]
    assert not copies, copies
    words = {w for t in nar.values() for w in t.split()}
    assert not any(w.startswith("oitXor") for w in words) and "tkk" in words


def test_mask_catches_repeats():
    assert clean_v2.mask("a li ye li ye b", ["li ye"]) == "a NAME NAME b"
    assert clean_v2.mask("pte oye qo", clean_v2.SAFE) == "NAME qo"


def test_baseline_does_not_see_the_other_mask():
    train = [{"id": f"A{i}", "text": "q r"} for i in range(5)] + [{"id": f"B{i}", "text": "z w"} for i in range(5)]
    items = [{"text": "T", "pos": 1, "answer": "q", "mask": "[?1]"}, {"text": "T", "pos": 2, "answer": "r", "mask": "[?2]"}]
    a = cloze.ngram_guess(train, items, [{"id": "T", "text": "p q r s"}])
    b = cloze.ngram_guess(train, items, [{"id": "T", "text": "p z r s"}])
    assert a["T[?2]"] == b["T[?2]"], (a, b)           # [?1]'s hidden word must not steer [?2]


def test_baseline_backoff_order_beats_counts():
    train = [{"id": f"A{i}", "text": "w1 r"} for i in range(3500)] + [{"id": "B", "text": "p q w2"}]
    items = [{"text": "T", "pos": 2, "answer": "w2", "mask": "[?1]"}]
    g = cloze.ngram_guess(train, items, [{"id": "T", "text": "p q x r"}])
    assert g["T[?1]"][0] == "w2", g                    # left two words beat a right word seen 3,500 times


def test_cloze_score_needs_whole_words():
    with tempfile.TemporaryDirectory() as d:
        k, a = Path(d) / "key.json", Path(d) / "ans.json"
        k.write_text(json.dumps({"T1[?1]": "qo", "T1[?2]": "li", "T2[?1]": "wi"}))
        a.write_text(json.dumps({"guesses": {"T1[?1]": "qoleb", "T1[?2]": ["l", "li"], "T9[?1]": ["wi"]}}))
        assert cloze.score(a, k) == (0, 1, 3, 1)       # "qo" is not "qoleb"; T2 has no guess


def test_synthetic_test_words_are_attested():
    texts = synth.corpus()
    freq = {}
    for t in texts:
        for x in t.split():
            freq[x] = freq.get(x, 0) + 1
    pool = synth.testable(texts)
    assert pool and all(freq.get(synth.LEX[m], 0) >= 2 and synth.LEX[m] not in synth.AFF.values() for m in pool)
    assert not {"small", "father", "cow"} & set(pool)


def test_cognate_forms_keep_their_vowels():
    assert cognates.skeleton("ɔto") == "oto"
    assert cognates.skeleton("màlléː") == "male"
    assert cognates.skeleton("pòɕɕ-íɕí-r") == "posisir"
    assert cognates.skeleton("ki5o") == "kino"
    nes = cognates.load_nes()
    assert "proto_nes" not in {lang for lang, _, _ in nes}
    assert not any("~" in f for _, f, _ in nes)


def test_swap_partners_file_is_stable():
    keys = list(json.loads((ROOT / "data/swap_partners.json").read_text()))
    assert keys == sorted(keys)


def c3_rebuild():
    return cloze_families.split([json.loads(l) for l in open(cloze_families.SNAPSHOT)])


def test_restoration_tasks_rebuild_as_run():
    train, test, items = cloze.split(cloze.load())
    assert cloze.task_text(train, test, items) == (ROOT / "runs/tasks/C2_cloze.md").read_text()
    assert {f"{it['text']}{it['mask']}": it["answer"] for it in items} == json.load(open(ROOT / "runs/keys/cloze.json"))
    _, _, train, test, items = c3_rebuild()
    assert cloze_families.task_text(train, test, items) == (ROOT / "runs/tasks/C3_cloze.md").read_text()
    assert {f"{it['text']}{it['mask']}": it["answer"] for it in items} == json.load(open(cloze_families.KEY))


def test_extra_tasks_rebuild_as_run():
    for name, fn in build_extra.BUILDERS.items():
        assert fn(build_extra.BLIND / name) == (ROOT / f"runs/tasks/{name}.md").read_text(), name


def test_extra_check_flags_a_changed_task():
    old = build_extra.SAVED
    with tempfile.TemporaryDirectory() as d:
        build_extra.SAVED = Path(d)
        try:
            for name in build_extra.BUILDERS:
                (Path(d) / f"{name}.md").write_text((ROOT / f"runs/tasks/{name}.md").read_text())
            (Path(d) / "N_open.md").write_text("another task")
            (Path(d) / "YK_morph.md").unlink()                # a saved copy is required, blind folder or not
            with contextlib.redirect_stdout(io.StringIO()):
                assert build_extra.check() == ["N_open", "YK_morph"]
        finally:
            build_extra.SAVED = old


def test_saved_key_is_never_rebuilt():
    old = cloze_families.KEY, cloze_families.NGRAM, cloze_families.SAVED_TASK, cloze_families.BLIND
    with tempfile.TemporaryDirectory() as d:
        key = Path(d) / "key.json"
        key.write_text(json.dumps({"B001[?1]": "qo"}))
        cloze_families.KEY, cloze_families.NGRAM = key, Path(d) / "ngram.json"
        cloze_families.SAVED_TASK, cloze_families.BLIND = Path(d) / "task.md", Path(d) / "blind"
        try:
            cloze_families.build(write_task=False)
            raise AssertionError("build() replaced a key that a run is scored against")
        except SystemExit:
            pass
        finally:
            cloze_families.KEY, cloze_families.NGRAM, cloze_families.SAVED_TASK, cloze_families.BLIND = old
        assert json.loads(key.read_text()) == {"B001[?1]": "qo"}


def test_parallel_finds_what_trigram_families_miss():
    def blob(texts):
        return "\n".join(t.replace(" ", "").lower() for t in texts)
    a = blob(["amnirense qore li akinidd pqrNyi pestoNyi pqr qorise l qor", "teketi 59 yed tlt 16 kelw yikidbitelowi ato",
              "aa yetmdelowiqoreN bb"])
    copy = "akinidd pqrNyi peStoNyi pqr qorisl qor".split()      # another word break, S for s
    assert cloze_families.parallel(copy, 1, a)
    part = "yed tlt 16 kelw yikidbitelowi s 10 kelw axide".split()  # a partial copy
    assert cloze_families.parallel(part, 3, a) and not cloze_families.parallel(part, 7, a)
    assert not cloze_families.parallel("zz yetmdelowiqoreN zz".split(), 1, a)   # the word alone is no parallel
    train = [{"id": "A", "text": "x"}]
    test = [{"id": "B001", "text": "pelmoS adblis NAME yetmdelowi"}, {"id": "B002", "text": "pelmoS adblis NAME yetmdelowi ato"}]
    own = [{"text": "B001", "pos": 0, "mask": "[?1]"}]
    assert not cloze_families.parallel(test[0]["text"].split(), 0, cloze_families.visible(train, test[:1], own))
    assert cloze_families.parallel(test[0]["text"].split(), 0, cloze_families.visible(train, test, own))  # B002 shows it


def test_mcnemar_is_exact():
    for n in range(9):
        for b in range(n + 1):
            m = min(b, n - b)
            brute = sum(1 for bits in itertools.product((0, 1), repeat=n) if min(sum(bits), n - sum(bits)) <= m) / 2 ** n
            assert math.isclose(cloze_families.mcnemar(b, n - b), brute), (b, n - b)
    assert math.isclose(cloze_families.mcnemar(57, 2), 6.139e-15, rel_tol=1e-3)


def test_baseline_counts_what_the_solver_sees():
    test = [{"id": "U", "text": "a q b"}, {"id": "W", "text": "c z d"}, {"id": "T", "text": "a x b c y d"}]
    items = [{"text": "W", "pos": 1, "answer": "z", "mask": "[?1]"},
             {"text": "T", "pos": 1, "answer": "q", "mask": "[?1]"}, {"text": "T", "pos": 4, "answer": "z", "mask": "[?2]"}]
    g = cloze.ngram_guess([{"id": "A", "text": "e f"}], items, test)
    assert g["T[?1]"][0] == "q", g                       # U is shown to the solver, so the baseline counts it
    assert "z" not in g["T[?2]"], g                      # W's masked word is hidden from both


def test_null_guess_scores_as_wrong():
    old = cloze_families.KEY
    with tempfile.TemporaryDirectory() as d:
        k, a = Path(d) / "key.json", Path(d) / "ans.json"
        k.write_text(json.dumps({"B001[?1]": "qo", "B001[?2]": "li"}))
        a.write_text(json.dumps({"guesses": {"B001[?1]": None, "B001[?2]": "li"}}))
        cloze_families.KEY = k
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                cloze_families.score(a)
        finally:
            cloze_families.KEY = old
        assert cloze.score(a, k) == (1, 1, 2, 0)



def test_reported_restoration_numbers():
    par = cloze_families.parallels()
    saved = json.load(open(cloze_families.COPIES))
    assert sorted(k for k in par if par[k]) == saved["with_parallel"]
    rows = cloze_families.split_scores(par, ROOT / "runs/answers/C3_cloze.json", cloze_families.NGRAM)
    assert [r[:4] for r in rows] == [("all masks", 120, 84, 35), ("with a parallel", 58, 54, 19), ("no parallel", 62, 30, 16)]
    assert cloze.score(ROOT / "runs/cloze_ngram.json") == (40, 45, 88, 0)


def test_reported_synthetic_numbers():
    assert synth.usable_score() == (41, 52, 24, 24)
    yk = json.load(open(ROOT / "runs/yk_morph_scored.json"))
    count = lambda rows, v: sum(r["verdict"] == v for r in rows)
    assert {v: count(yk["endings"], v) for v in ("right", "partly", "wrong")} == yk["totals"]["endings"] == \
        {"right": 2, "partly": 4, "wrong": 2}
    k2 = json.load(open(ROOT / "runs/k2_morph_scored.json"))
    gold = [g["form"] for g in json.load(open(ROOT / "data/gold_morphology.json"))]
    assert [i["form"] for i in k2["items"]] == gold
    assert {v: count(k2["items"], v) for v in ("right", "partly", "missed")} == k2["totals"]

if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("ok  ", name)
        except Exception as e:      # noqa: BLE001 - report every failing check, then exit non-zero
            failed += 1
            print("FAIL", name, type(e).__name__, e)
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
