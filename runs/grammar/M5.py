"""Rule counts for the M5 rules (names, titles and the endings they carry)."""
import re

VOWELS = "aeio"
COPULA = re.compile(r"^[lqt]?o(w|wi)?$|^lw$")


def _parts(row):
    """The word's parts as (letters, entry) pairs, in order; tokens without '=' are skipped."""
    out = []
    for tok in row["parts"].split(" "):
        if "=" in tok:
            letters, entry = tok.split("=", 1)
            out.append((letters, entry))
    return out


def _is_stem(entry):
    return entry not in ("?", "ending", "NUMBER", "") and not entry.startswith("-") and not entry.endswith("-")


def _is_affix(entry):
    return entry == "ending" or entry.startswith("-")


def _is_name(entry):
    return entry == "NAME" or entry[:1].isupper()


def _junctions(rows):
    """Every stem part directly followed by an ending part, in words whose level is not 'lost'.
    Yields (stem_letters, stem_entry, ending_letters)."""
    out = []
    for r in rows:
        if r["level"] == "lost":
            continue
        ps = _parts(r)
        for k in range(len(ps) - 1):
            (l1, e1), (l2, e2) = ps[k], ps[k + 1]
            if _is_stem(e1) and _is_affix(e2) and l1 and l2:
                out.append((l1, e1, l2))
    return out


def test_M5_1(rows):
    """A name carrying an ending does not take an ending that begins with l (the article)."""
    J = _junctions(rows)
    cases = [j for j in J if _is_name(j[1])]
    holds = sum(1 for j in cases if not j[2].startswith("l"))
    other = [j for j in J if not _is_name(j[1])]
    comp = sum(1 for j in other if not j[2].startswith("l")) / len(other) if other else 0.0
    return len(cases), holds, comp


def test_M5_2(rows):
    """A common noun (not a name) carrying the copula -o(wi) has the article l right before the o."""
    J = _junctions(rows)
    common = [j for j in J if not _is_name(j[1])]
    cases = [j for j in common if COPULA.match(j[2])]
    ok = lambda j: j[2].startswith("l") or j[0].endswith("l")
    holds = sum(1 for j in cases if ok(j))
    other = [j for j in common if not COPULA.match(j[2])]
    comp = sum(1 for j in other if ok(j)) / len(other) if other else 0.0
    return len(cases), holds, comp


def test_M5_3(rows):
    """An ending that begins with a vowel follows a stem ending in a consonant; an ending that
    begins with y follows a stem ending in a vowel."""
    J = _junctions(rows)
    cases = [j for j in J if j[2][0] in VOWELS or j[2][0] == "y"]

    def ok(j):
        if j[2][0] in VOWELS:
            return j[0][-1] not in VOWELS
        return j[0][-1] in VOWELS

    holds = sum(1 for j in cases if ok(j))
    if not cases or not J:
        return len(cases), holds, 0.0
    p_cons = sum(1 for j in J if j[0][-1] not in VOWELS) / len(J)
    n_v = sum(1 for j in cases if j[2][0] in VOWELS)
    n_y = len(cases) - n_v
    comp = (n_v * p_cons + n_y * (1 - p_cons)) / len(cases)
    return len(cases), holds, comp
