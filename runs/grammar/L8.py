"""Counts for rules L8-1 to L8-7 (writing at stem-ending joints)."""

V = "aeio"


def _forms(rows):
    return [r["form"] for r in rows if r["level"] not in ("lost", "number")]


def test_L8_1(rows):
    cases = holds = pos = glide = 0
    for f in _forms(rows):
        for i in range(len(f) - 1):
            if f[i] not in V:
                continue
            pos += 1
            if f[i + 1] in "yw":
                glide += 1
            if f[i + 1] in V:
                cases += 1
            elif f[i + 1] in "yw" and i + 2 < len(f) and f[i + 2] in V:
                cases += 1
                holds += 1
    return cases, holds, (glide / pos if pos else 0.0)


def test_L8_2(rows):
    cases = holds = alln = ally = 0
    for f in _forms(rows):
        for i in range(len(f) - 2):
            if f[i] in V and f[i + 1] in "yw" and f[i + 2] in V:
                alln += 1
                ally += f[i + 1] == "y"
                if f[i + 2] in "eo":
                    cases += 1
                    holds += f[i + 1] == "y"
    return cases, holds, (ally / alln if alln else 0.0)


def test_L8_3(rows):
    cases = holds = base = base_o = 0
    for f in _forms(rows):
        if len(f) < 3:
            continue
        base += 1
        base_o += f[-3] == "o"
        if f.endswith("wi"):
            cases += 1
            holds += f[-3] == "o"
    return cases, holds, (base_o / base if base else 0.0)


def test_L8_4(rows):
    cases = holds = allo = allo_lqt = 0
    for f in _forms(rows):
        if len(f) >= 4 and f.endswith("owi"):
            cases += 1
            holds += f[-4] in "lqt"
        for i in range(1, len(f)):
            if f[i] == "o":
                allo += 1
                allo_lqt += f[i - 1] in "lqt"
    return cases, holds, (allo_lqt / allo if allo else 0.0)


def test_L8_5(rows):
    cases = holds = tot = plain = 0
    for f in _forms(rows):
        for i, ch in enumerate(f):
            if ch in "SsNn":
                tot += 1
                plain += ch in "Sn"
                if i + 1 < len(f) and f[i + 1] in "io":
                    cases += 1
                    holds += ch in "Sn"
    return cases, holds, (plain / tot if tot else 0.0)


def test_L8_6(rows):
    cases = holds = tot = ne = 0
    for f in _forms(rows):
        for i, ch in enumerate(f):
            if ch in "Nn":
                tot += 1
                ne += ch == "N"
                if i + 1 < len(f) and f[i + 1] in "yw":
                    cases += 1
                    holds += ch == "N"
    return cases, holds, (ne / tot if tot else 0.0)


def test_L8_7(rows):
    cases = holds = tot = rle = 0
    for f in _forms(rows):
        for j in range(len(f) - 1):
            tot += 1
            rle += f[j] in "rle"
        for i in range(1, len(f)):
            if f.startswith("kete", i) or f.startswith("kte", i):
                cases += 1
                holds += f[i - 1] in "rle"
    return cases, holds, (rle / tot if tot else 0.0)
