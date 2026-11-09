import json
C = ("Read sign by sign from Griffith's printed cursive type, right to left. '|' = line break in Griffith's printing "
     "(stone lines only where stated); '?' = a sign I could not settle or one Griffith himself marks '?'; "
     "[x] = Griffith's restoration in square brackets; each [.] = one of Griffith's lacuna dots (not an exact sign count). "
     "'signs' counts read and restored signs, not [.]. ")
FHN_SCHEME = ("FHN confirms REM 0400+N for Meroe nos. 2, 5, 7, 8-10, 12, 15, 18, 19 and 30 (REM 0430 = no. 30's 'Wosi Msmni' table), "
              "so this text is probably REM 04%02d, but no source seen gives it.")
rows = [
 dict(griffith_no=5, rem="0405", page="pp. 62-64 (type on p. 63, archive.org leaf n194)",
      object="votive plaque of dark red slate, king before the lion-god (3 texts)",
      site="Meroe City, temple of the lion-god (Apedemak temple, M 6)",
      text_std="w?lto wteli eto ẖ?to : ẖ?k dqrite || a[pe]dem[k] tñyidmni pwrite elḫte dqrito | ẖ?ewito sno qore : lw : ewkenki : apedemki || [.][.][.][.][.][.] w [.][.][.] l : e[.][.] kkte apedemki",
      notes=C + "Parts in order: (a) before the god || (b) before the king || (c) behind the king (end of about 15 short lines). "
        "Style d. Griffith: the first letter of (a) is 'very uncertain', perhaps a numeral; apedemk (his Apezemak) identified here; "
        "he takes sno (his 'Shane') before qore as the king's name. REM 0405 from FHN II no. 153 (Tañyidamani tablet, Baltimore WAG 22.258). "
        "FHN reads (b) ... *mewito *Mno qo*re l w ewkenki Apedemki and (a) *ato wt li eto*hto *mk dqri*te: Griffith's type has "
        "ẖ? where FHN has *m (ẖ?ewito, ẖ?k: the m/ẖ pair), s where FHN has *M (sno), and w?lto for *ato. Griffith did not read tñyidmni as a name."),
 dict(griffith_no=6, rem="", page="pp. 64-65 (type on p. 64, leaf n195)",
      object="stela sculptured and inscribed on both sides (winged scarab face), lower part lost; Khartoum Museum",
      site="Meroe City, temple of the lion-god (Apedemak temple)",
      text_std="sewitw : woyekite : qesewi : ssiẖete : qesewi : ttñ : | qesewi s?stoselw : erli : aḫlste : yi[.]ḫrtenkelw : yoto : | qete dewite : tendti q?or?kelw : ato ḫmñ?imliselw : | asero : toḫ?ktw : [.][.]s?olw : [.][.]okḫ : ḫrqibliq : [.][.][.][.][.] | [.][.][.][.][.] rimlise?lw wo [.][.][.][.][.][.][.][.][.] s?k?lw : a? [.][.][.][.] rs? [.][.][.]",
      notes=C + "Style d-e. Griffith copied it 'solely from the photograph'; 'probably not more than half of the inscription is preserved'; "
        "he prints an alternative reading for a group in l. 6; sewitw (his 'Sewitiw') may be the deity, perhaps Egyptian Show. " + FHN_SCHEME % 6),
 dict(griffith_no=7, rem="0407", page="pp. 65-67 (type on p. 65, leaf n196)",
      object="large stela, 18 lines under a winged disk, cut down for re-use",
      site="Meroe City, temple of the lion-god (Apedemak temple, M 6)",
      text_std="[p]edemk : soborete : k?e?m?p?[l?] : [ye]seboẖe : qore : | bowidlo b?i[.][.][.]kye | wos : pileqete : ste : [.][.] [p]ileqe pl yeseboẖe[towi] : | ar : ywidl : pileqe [pl] : ytkidetowi : | wos : at[i]yete : [a]tiye pl : ye?seboẖetowi : | ar atiyete : atiye pl : ytkidetowi : | wos : tebwete : tebwe : pl [ye?]seboẖ[eto]wi : | ar [te]bwe[te] : tebwe pl : ytkidetowi [:] | a[m]npte : nptek : mk : tñyiñwitw : ytkideto[wi] [:] | [.][.][.][.]s? [.] [w?]l?bḫetel ywi : yiretwi | aro : ḫ?irl w?ebḫlit : yẖi ntmetwi : | [.]rekl : aḫñwitw : yeritowi : | te?ris : aḫñw[i]tw : ntmetowi : | ayis? : ayi",
      notes=C + "Style g. Griffith's printing sets the text in parallel phrases ('|'), not the 18 stone lines; copied at Meroe and corrected from photographs. "
        "His English: 'The yesbekhe of Apizemak in Shebere ... bewize of the king, Bi(?)..kaye'; Isis and Horus of Philae (pileqe), Atiye (Sedeinga) and Tebawe; "
        "A[m]anapate (Amun of Napata). REM 0407 from FHN III no. 277 (dedication of Yesebokheamani). FHN differs from Griffith's type at: pe (type pl, 6 times), "
        "(w)*ebhetel (type [w?]l?bḫetel), hir*e (type ḫ?irl), nt*hetwi and nt*hetowi (type ntmetwi, ntmetowi: Griffith's type shows the m form), ayi s ayi (type ayis? : ayi)."),
 dict(griffith_no=8, rem="0408", page="pp. 67-69 (type on p. 68, leaf n199)",
      object="square sandstone block (statue base?), 3 lines on each of 4 sides",
      site="Meroe City, temple of the lion-god",
      text_std="pedemk [:] [.]rem?ye?[te] : teqrid[e] a[m]ni : qore : | pwide? : mlol : yese [be]te : s?ow?te : y?te : bntke : tomlo : | [t?]m?lteke : qoleb : yerilw : yibḫebseni : ntkelw : | yibḫebseni : t?m?eteke : ñwi : yite?seni : | ye [.][.][.][.][.] : ypñseni : yelbilise : ypñseni : dimelise | ypñseni : yelebil : ase [.][.][.] | [.][.][.]i : [.][.]dkse[n?i] [.][.][.][.][.][.][.][.] yeli? : yekseni : | yib?ḫ [.][.][.][.][.][.][.] eyk?seni : y[.][.][.]l? : y[.][.][.]",
      notes=C + "Sides (a) to (d) in order. Style g. Griffith: the stone is very friable; side (a) ll. 1-2 restored from No. 9; in side (b) l. 6 'some alteration has been made' "
        "and another sign might be read for te (yite?seni). Lion-god pedemk, king teqride amni (his 'Teqrize-Amani'). Griffith's type has mlol in side (a) where No. 9 has ẖlol in the same phrase. "
        "REM 0408 from FHN III (REM 0408-0410: three dedications of Teqorideamani on sandstone bases from Meroe City)."),
 dict(griffith_no=9, rem="0409", page="pp. 68-69 (type on p. 68, leaf n199)",
      object="square sandstone block (statue base?), 3 lines on each of 4 sides",
      site="Meroe City, temple of the lion-god",
      text_std="pedemk : siqyete : teqride : amni : qore : | pwide : ẖlol : yeseboẖe : wete yk? [.][.][.] | ato : ẖlo : wde?plke : ytwdseni : ḫrim : mlo : yere | [.] tḫnke : yereseni : [.] | ato : beyo?twdy? [.][.][.] ylseni : ḫrim : beyo?try[.]e : | wrse : ylseni : treql? : ylseni | [.][.] kelw : qrseni : y : tenn?i?etilw : sobseni : | ylte?te?kewi : yidḫlseni",
      notes=C + "Sides (a) to (d) in order. Style g; from Griffith's copies at Meroe, the photographs and the originals shown in London. Place siqyete (his 'Shiqye'), "
        "king teqride amni. Griffith: sides (b) and (c) begin with ato 'water' (formula A word); an alteration is possible in l. 11. "
        "The type has ẖlol and ẖlo (3-form with a descender to the lower left) where No. 8 has mlol. REM 0409 from FHN III (REM 0408-0410)."),
 dict(griffith_no=10, rem="0410", page="pp. 69 (type on p. 69, leaf n200)",
      object="square sandstone block (statue base?), lines on 4 sides, much weathered",
      site="Meroe City, temple of the lion-god",
      text_std="pedemk : kobbleteli : teqride [amni] : qore : | q?li?te : mẖ?elidt? r?ekel : [.][.][.][.][.][.][.] : aleḫ? : | tenowitw : kmok : yesw : ke?lt : yetre : kete?[se?] : | [.][.] borẖted?ḫ : kete : lḫ? [.][.][.] | ytlek?ete : l?ḫeketese : atbelw : [.]kide? : kete | [.][.][.]qelw : t [.][.][.][.][.][.][.][.][.]",
      notes=C + "Sides (a), (b), (d) in order; side (c), ll. 7-9, has 'only traces left' and is omitted. Style g; 'this block has evidently suffered from exposure'. "
        "Place kobbleteli (his 'Kebable'), king teqride [amni] with amni restored. REM 0410 from FHN III (REM 0408-0410)."),
 dict(griffith_no=12, rem="0412", page="p. 70 (leaf n201)",
      object="small granite stela (re-used oval corn grinder), king before Isis; 3 texts",
      site="Meroe City, Kenisa or Isis (?) temple (M 600)",
      text_std="ekete : n?s : wid?el : etktetewi : mseqñid?yi || ekete : woswẖ?e : etsto || teriqq?d?r : qoro a?medle?rense? : kdkeḫ? : | p?idtd : ws : lolo",
      notes=C + "Parts in order: (a) behind the king || (b) behind Isis || (c) four lines below the scene. Style d-e. Griffith: 'the readings are by no means certain, "
        "and even the succession of the signs is doubtful in (c), and others may be missing'; wos (his Wêsh, Isis) in (b), the king 'Teriqaqzar or Teriteqñir' and his title in (c), ws (Isis?) at its end. "
        "REM 0412 from FHN II no. 174 (Teriteqas stela), which reads (a) ekete *W*s wi*de l etktetewi mseqnei*d yi; (b) ekete Wos wke [.]tk to; "
        "(c) Teriteqse qor*o Amnirense kd*ke Akinidd ss [..]te lo. Griffith's type differs at n?s, woswẖ?e, etsto, teriqq?d?r, a?medle?rense?, kdkeḫ?, p?idtd, ws and lolo."),
 dict(griffith_no=13, rem="", page="pp. 70-71 (type on p. 71, leaf n202)",
      object="graffito of four lines beside incised figures (lion's head, prostrate man) on a block",
      site="Meroe City, temple of Amun, side of the staircase to the westerly chamber (275)",
      text_std="wbrḫmlo : yesorli | yinsi dekeli : nkeyi | mkedokeli : yinsi dekeli | nmero",
      notes=C + "Here '|' = the four stone lines (Griffith's superscripts 2-4). Style f, 'peculiar'. Griffith: in l. 1 the y-s group 'was originally written and then altered' to y-e-s (yesorli); "
        "mkedokeli (l. 3) 'may be the name of the lion; the word occurs, probably as that of a god, on the columns of Naga and Amara (Inscr. Nos. 34, 84)'. " + FHN_SCHEME % 13),
 dict(griffith_no=14, rem="", page="p. 71 (leaf n202)",
      object="block from the east face of the outer wall: six lines of very large characters, traces of a line of small ones above",
      site="Meroe City, temple of Amun",
      text_std=": aleqese : | [.][.] mdewetye : nẖst? | [.][.] dseke : mni : se[.][.] | [.][.] keteli? : m?o?rl? | [.][.][.] rmnite : wte? | [.][.][.][.] lo :",
      notes=C + "Here '|' = stone lines (Griffith's superscripts 2-6). Style g; the block 'much cut about' at the right; 'the end of the inscription is clear in the sixth line'. "
        "Griffith: aleqese is also the first word left on the Isis statue from Napata (Inscr. No. 75), and a divider may precede it (his '?'); mdewetye is his '..mazetye (?)', "
        "the writer's name by its ending; then 'his title zasake [dseke] of Ammon [mni] in (?) ...ke'. In wte? the first stroke of te is Griffith's restoration. " + FHN_SCHEME % 14),
 dict(griffith_no=22, rem="", page="p. 74 (leaf n205)",
      object="fragment of coarse hand-made pottery, thick blackish ware, incised marks (5 x 4 cm)",
      site="Meroe City, Kenisa (600), at a good depth",
      text_std="l?o?q? [.][.]",
      notes=C + "Griffith prints only 'possibly' these three signs 'of an early type', 'followed by the numeral strokes II' (not counted). Every sign is uncertain. " + FHN_SCHEME % 22),
 dict(griffith_no=44, rem="", page="pp. 76-78 (type on p. 78, leaf n209)",
      object="upper part of a slab or stela, six horizontal lines (only ll. 1-5 printed in type)",
      site="Meroe, middle cemetery, grave 340",
      text_std="[[.][.][.] wosi] so[re]yi | dmse qoli : troys?e? : klke : sbtn : seqe : r e[te]",
      notes=C + "Partial: Griffith prints ll. 1-5 in type only in his comparison of Kar. 41, No. 44 and No. 51 ('&c. most destroyed'); the rest is only in his hand copy (Pl. LXXIII), not read here. "
        "Style e. Griffith: the names of Isis (restored) and Osiris, then 'a long descriptive phrase'; no name of the deceased; a text of the type of No. 51 and Kar. 41 ll. 13-14. "
        "His superscript 2 falls inside troys?e?. " + FHN_SCHEME % 44),
 dict(griffith_no=51, rem="", page="pp. 77-78 (type on p. 78, leaf n209)",
      object="slab (stela) with six lines",
      site="Meroe, north group of cemeteries, western portion, grave 415",
      text_std="[.][.][.][.] [wos] [.][.][.][.][.] dmte qoli : klikelo [:] | sklw : mlon : yetlw [:] mlonki : tkkete : | asori : p?writ troy? d?rpñ qese drpñ?k : likel",
      notes=C + "Style g; 'apparently complete except perhaps at the top'. Printed in three type lines in the comparison on p. 78, not by the six stone lines. "
        "Griffith: the name of Isis (wos, restored) with a descriptive phrase and a prayer or benediction, then Osiris (asori) with epithets; no name of the deceased; "
        "for the group d-r-p-(damaged sign) 'in l. 5' he suggests d-o-r-o-s as 'a possible reading'; he marks the divider before likel 'sic'. " + FHN_SCHEME % 51),
]
json.dump(rows, open('/private/tmp/claude-501/griffith_scripts/meroe/rows.json', 'w'), ensure_ascii=False, indent=1)
print(len(rows))
