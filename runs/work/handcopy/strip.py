from PIL import Image, ImageDraw
K='/private/tmp/claude-501/expansion/karanog/'
im = Image.open(K+'leaf_34.jpg').convert('L'); W,H = im.size; s = W/1400
print(W,H)
# columns in thumb coords: labels 140-215, Kar col 14: 712-822, col 15: 822-920
rows_y = [262,340,400,463,522,590,655,715,780,850,915,980,1040,1105,1170,1235,1295,1360,1420,1480,1545,1610,1675]
names = ['a','e','o','i','y','w','b','p','m','n','N','r','l','x(kh)','X(h)','s(se)','S(sh)','k','q','t','te','to','d(z)']
cols = [(140,215),(712,822),(822,922)]
cw = sum(int((b-a)*s) for a,b in cols)
rh = int(64*s)
out = Image.new('L', (len(rows_y)*int(105*s/1.0), rh+60), 255)
# horizontal strip: each sign cell = label col + kar col (+inscr col), arranged left to right
cells=[]
for y,nm in zip(rows_y,names):
    parts=[im.crop((int(a*s), int((y-34)*s), int(b*s), int((y+34)*s))) for a,b in cols[1:2]]
    cells.append((nm,parts[0]))
cwid = max(c.width for _,c in cells)
strip = Image.new('L', (cwid*len(cells), cells[0][1].height+50), 255)
d = ImageDraw.Draw(strip)
for i,(nm,c) in enumerate(cells):
    strip.paste(c,(i*cwid,0)); d.text((i*cwid+10, c.height+8), nm, fill=0)
strip.save('kar_strip_full.png'); print(strip.size)
# two-row version for viewing
half = (len(cells)+1)//2
A = Image.new('L',(cwid*half, 2*(cells[0][1].height+50)),255)
A.paste(strip.crop((0,0,cwid*half,strip.height)),(0,0))
A.paste(strip.crop((cwid*half,0,strip.width,strip.height)),(0,strip.height))
A = A.resize((A.width*1, A.height*1))
A.save('kar_strip2.png'); print(A.size)
