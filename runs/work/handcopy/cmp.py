from PIL import Image, ImageDraw
im = Image.open('kar_strip_full.png'); n = 23; cw = im.width//n
names = ['a','e','o','i','y','w','b','p','m','n','N','r','l','x','X','s','S','k','q','t','te','to','d']
pick = ['p','k','n','m','X','S','w','N','d','t','l','e','to','x']
cells = [im.crop((names.index(p)*cw, 0, (names.index(p)+1)*cw, im.height)) for p in pick]
out = Image.new('L', (cw*7, im.height*2), 255)
for i,c in enumerate(cells): out.paste(c, ((i%7)*cw, (i//7)*im.height))
out = out.resize((int(out.width*1.2), int(out.height*1.2))); out.save('cmp_strip.png'); print(out.size)
