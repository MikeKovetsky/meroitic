"""Find the name pools Otten swapped in, from one-slot differences between lines."""
import collections, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(line):
    return re.sub(r"\s+", " ", line.replace(".", " ")).strip()


def main():
    lines = [norm(l) for l in (ROOT / "data/otten/Data/mero-corpus.txt").read_text().split("\n")]
    uniq = list(dict.fromkeys(l for l in lines if l))
    sig = collections.defaultdict(list)
    for i, l in enumerate(uniq):
        t = l.split()
        if len(t) > 150:
            continue
        for j in range(len(t)):
            sig[hash((len(t), j, tuple(t[:j]), tuple(t[j + 1:])))].append((i, t[j]))
    partners = collections.defaultdict(set)
    for items in sig.values():
        words = {w for _, w in items}
        if len(words) > 1:
            for w in words:
                partners[w] |= words - {w}
    deg = sorted(((len(p), w) for w, p in partners.items()), reverse=True)
    # sorted keys: set order changes with each run's string hashing, the file should not
    json.dump({w: sorted(partners[w]) for w in sorted(partners)}, open(ROOT / "data/swap_partners.json", "w"))
    hist = collections.Counter(min(d, 50) // 5 * 5 for d, _ in deg)
    print("degree histogram", sorted(hist.items()))
    print("top", deg[:40])
    print("mid", [w for d, w in deg if 5 <= d < 15][:60])


if __name__ == "__main__":
    main()
