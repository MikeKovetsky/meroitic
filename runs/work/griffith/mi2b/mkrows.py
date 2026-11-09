import json, re, sys, unicodedata
# mkrows.py: builds rows_129_137.jsonl from the readings in READ below.
SIGNS2 = ('se', 'te', 'to')
SIGNS1 = set('aeioywbpmnñrlḫẖskqtd')
MAP = {'s': 'S', 'se': 's', 'ñ': 'N', 'ḫ': 'x', 'ẖ': 'X'}
def conv(std):
    std = unicodedata.normalize('NFC', std)
    t = re.sub(r'\((?:\d+|a|b)\)', '', std)          # Griffith's line numbers and the a/b markers
    t = t.replace('|', ' ').replace('[:]', ' ').replace(':', ' ')
    words, signs, unc = [], 0, 0
    for w in t.split():
        w = w.replace('[...]', '\x01').replace('[.]', '\x00').replace('[', '').replace(']', '')
        out, i = '', 0
        while i < len(w):
            c2 = w[i:i + 2]
            if c2 in SIGNS2:
                out += MAP.get(c2, c2); signs += 1; i += 2
            elif w[i] in SIGNS1:
                out += MAP.get(w[i], w[i]); signs += 1; i += 1
            elif w[i] == '?':
                unc += 1; i += 1
            elif w[i] == '·':
                i += 1
            elif w[i] == '\x00':
                out += '.'; i += 1
            elif w[i] == '\x01':
                out += '...'; i += 1
            else:
                raise SystemExit(f'bad char {w[i]!r} in {std!r}')
        if out:
            words.append(out)
    return ' '.join(words), signs, unc
if __name__ == '__main__':
    for s in sys.argv[1:]:
        print(conv(s))
