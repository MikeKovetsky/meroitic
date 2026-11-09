import re, sys
# list pure-number OCR words (with boxes) per leaf in the hand-copy range, from archive.org djvu.xml
x = open('/private/tmp/claude-501/expansion/karanog/kar_djvu.xml', encoding='utf-8').read()
objs = re.split(r'<OBJECT ', x)[1:]
print('objects', len(objs))
for i, o in enumerate(objs):
    if not (140 <= i <= 200): continue
    m = re.search(r'usemap="([^"]+)"', o)
    words = re.findall(r'<WORD coords="([^"]+)"[^>]*>([^<]*)</WORD>', o)
    nums = [(w, c) for c, w in words if re.fullmatch(r'\d{1,3}\.?', w.strip())]
    print(i, m.group(1) if m else '', [(w, c.split(',')[:2]) for w, c in nums][:30])
