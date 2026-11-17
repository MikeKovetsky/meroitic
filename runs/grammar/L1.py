"""Counts for rules L1-1 to L1-6 (noun phrase). Each function takes the table rows and
returns (cases, holds, comparison_rate)."""


def _readable(r):
    return r is not None and r["level"] != "lost" and "." not in r["form"]


def _neighbours(rows):
    """Yield (row, previous row, next row): rows of the same text with n-1 and n+1."""
    index = {(r["text"], r["n"]): r for r in rows}
    for r in rows:
        yield r, index.get((r["text"], r["n"] - 1)), index.get((r["text"], r["n"] + 1))


def _count(rows, is_case, side, hold, comp):
    cases = holds = 0
    for r, prev, nxt in _neighbours(rows):
        other = prev if side == "prev" else nxt
        if is_case(r) and _readable(other):
            cases += 1
            if hold(other):
                holds += 1
    readable = [r for r in rows if _readable(r)]
    rate = sum(1 for r in readable if comp(r)) / len(readable) if readable else 0.0
    return cases, holds, rate


_MX = {"mXe", "mxe", "mX", "mXo"}


def _starts_mx(r):
    return r["form"].startswith(("mX", "mx"))


def _ato_at(r):
    return r["form"] in ("ato", "at")


def _verb_prefix(r):
    return r["form"].startswith(("p", "b", "y"))


def _osiris_i(r):
    f = r["form"]
    return f.startswith(("Sor", "aSor")) and f.endswith("i")


def _name_li_ye(r):
    return r["level"] == "name" or r["form"].endswith(("li", "ye"))


def _name_l_b_li_ye(r):
    return r["level"] == "name" or r["form"].endswith(("l", "b", "li", "ye"))


def test_L1_1(rows):
    return _count(rows, _ato_at, "next", _starts_mx, _starts_mx)


def test_L1_2(rows):
    return _count(rows, lambda r: r["form"] in _MX, "prev", _ato_at, _ato_at)


def test_L1_3(rows):
    return _count(rows, lambda r: r["form"] in _MX, "next", _verb_prefix, _verb_prefix)


def test_L1_4(rows):
    return _count(rows, lambda r: r["form"] in ("woSi", "wiSi"), "next", _osiris_i, _osiris_i)


def test_L1_5(rows):
    return _count(rows, lambda r: r["form"].startswith(("terik", "tedx")), "prev",
                  _name_li_ye, _name_li_ye)


def test_L1_6(rows):
    return _count(rows, lambda r: r["form"].startswith("yetmde"), "prev",
                  _name_l_b_li_ye, _name_l_b_li_ye)
