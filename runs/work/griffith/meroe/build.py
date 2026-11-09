import json, re, sys
SRC = "Meroe, the City of the Ethiopians (Garstang, Sayce, Griffith 1911)"
ITEM = "merocityofethiop00gars"
DIG = ("se", "te", "to")
MAP = {"se": "s", "s": "S", "ñ": "N", "ḫ": "x", "ẖ": "X"}

def tokens(word):
    w = word.replace("[.]", "§").replace("[", "").replace("]", "")
    out, i = [], 0
    while i < len(w):
        if w[i] == "§":
            out.append(("§", False)); i += 1; continue
        if w[i:i + 2] in DIG:
            t, i = w[i:i + 2], i + 2
        else:
            t, i = w[i], i + 1
        q = False
        if i < len(w) and w[i] == "?":
            q, i = True, i + 1
        out.append((t, q))
    return out

def convert(std):
    words, signs, unc = [], 0, 0
    for w in std.replace("[:]", ":").replace("||", " ").replace("|", " ").split():
        if w == ":" or set(w) <= set(":"):
            continue
        w = w.strip(":")
        toks = tokens(w)
        if not toks:
            continue
        cw = ""
        for t, q in toks:
            if t == "§":
                cw += "."; continue
            signs += 1; unc += q
            cw += MAP.get(t, t)
        words.append(cw)
    return " ".join(words), signs, unc

rows = json.load(open(sys.argv[1]))
with open(sys.argv[2], "w") as f:
    for r in rows:
        corpus, n, u = convert(r["text_std"])
        bad = re.findall(r"[^a-zA-Z.\s]", corpus)
        assert not bad, (r["griffith_no"], bad, corpus)
        row = {"source": SRC, "item": ITEM, "griffith_no": r["griffith_no"], "rem": r["rem"], "page": r["page"],
               "object": r["object"], "site": r["site"], "text_std": r["text_std"], "text_corpus": corpus,
               "uncertain": u, "signs": n, "notes": r["notes"]}
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(r["griffith_no"], n, u, corpus[:90])
