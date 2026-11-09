import json
lines = [
 # p. 27 (n46): ll. 1-3, phrased
 "xrmdoye : qore : ariTNl :",
 "mdes :",
 "mnitke^ : (2)mkleb : yereqe : qyitX?l :",
 "yesboXe : qrleb : tro(3)s :",
 "ariTN : Trekelis :",
 "dblilx : qrke :",
 # p. 28 (n47) left: ll. 3-7, the seven parallel phrases
 "qore : mnpT(4)s : lw : qoreyi :",
 "tx : mnoT : s : lw : txNyi :",
 "qr : ariTNlis (5)lw : qrNyi :",
 "Sob : xlbi : lis : lw : SobNyi :",
 "tx : mnoTslw : (6)txNyi :",
 "aretT : woSslw : xiretTNyi :",
 "xrpxe mkedo(7)kelislw : xrpxeNyi :",
 # p. 28 right: ll. 7-11
 "Tris : mnpT : pdXos : tlo (8)lis",
 "kidkeTt : yismeniye : qorelX :",
 "yeOlxe : yiti {4} yoO : (9)ptpoTkye",
 ": able : ywiO : swide : aqtoye",
 ": Tpke : yed : mk^l^ : T(10)pke :",
 "ye yk : wyed : Tpke : pyk : xiwr :",
 # p. 29 left: ll. 11-32
 "ado : ws : pXrs : tdo(11)mN : aSy :",
 "kede^bxeky : qorelik : dik : pilqoyT bqok : (12)e^kS : SqyeS : nsdokeS : TmeyyeS nxbreS : bqobx",
 "(13)Simlok : dik : pilqoyT : bqol :",
 "pro : dole : plw : penn : t(14)lT : br :",
 "pxiN^l : bxemi : yenet : byekelx",
 "dik : kdimloye : (15)S^qkdi : p^tpoto",
 "yismeniye : ysbet^ : berSowi :",
 "tT : ws : (16)ayekenl : ytpo^O : yed :",
 "ykle : aroXetye : nle : dolk",
 "(17)mTl : pikedelw^i : yed : ptpoTkye : wk^diw^ikeT : tTws (18)qorX :",
 "txeNye : tkl^w^i : ysbeT : berekn",
 "wi : x(19)rpxe : deTlxl : w^eN : yed :",
 "wokike : tilyeyki : (20)wrleb : kedebx :",
 "kdileb : mrorleb : SSleb :",
 "kbb (21)T : pdXos : lXleb : yexoyk?e :",
 "yeTT : mrorb^e^ : qe(22)Sw : adereke : m?tr : ws : Xrw^ : pilqok^e :",
 "m?tr : ws : (23)qore {4} {4} X^res : wTb :",
 "axi : d^e^T^ : S^kle : d^e(24)T : wedi :",
 "nxe : m?T : kdi : aqtoyes {2}w bqob(25)T : wido : xroSyeqo : wido :",
 "yis^xT^Tyeqo : bqo(26)bx : smle :",
 "wSi : tkbT : ST : wes{sign} : bqobT :",
 "(27)Simlok : dik : sleleyT : mXo :",
 "Tmey : nsdoke (28)kdike (:) br :",
 "nxbreS : k?bx : mXoli : Tmeyli :",
 "dk : (29)pro : dole : plw : penn : tlT :",
 "br : kX^ole : bxem?i : (30)yenet : Xrw :",
 "adonilikeT yireqw : a^(31)r^w^ :",
 # p. 29 right column top: ll. 32-34
 "Tr^[e]keT : Xrw : sleleke : mtr :",
 "ws yire(32)qw : ad^e^r^eke : m?tr :",
 "ws : qore : ptSide : tmot : (33)m^[.][.][.][.]e^S^ :",
 "[.][.][.]plN^ ptmkide : tm?ot : ariTle :",
 "wo(34)k^l^e^ :",
]
notes = ("Griffith no. 94: the Meroitic inscription of king Kharamadoye (Griffith's Kharamazeye), 34 lines of very late cursive "
 "cut on the second column of the facade of the hall of columns of the great temple, beginning on one drum and ending on the next, "
 "with a Greek inscription above and below; height 72 cm. L., D., VI, Bl. 6, no. 21; Pls. XIII-XVI. Griffith: practically complete, "
 "ll. 22-23 injured at the joint, right-hand ends of ll. 29-34 chiselled, signs 'not of very distinct forms', lines crowded. "
 "He prints ll. 1-3 and the seven parallel phrases of ll. 3-7 phrase by phrase (type lines 1-13), then the running text. "
 "His readings bearing on the text: 'sic' over the two-stroke y of qoreyi (l. 4); in l. 8 the stone has e-o-se (sic) where the type "
 "prints the corrected yismeniye; in l. 15 the o of ptpoto is 'sic', probably for ':' before t; (:) in l. 28 is his supplied divider; "
 "the divider before smle (l. 26) is queried; {sign} after wes (l. 26) is a 'peculiar sign', a numeral or an ill-formed s; l. 21 "
 "'much confused'; in l. 31 every sign of a(31)rw and the final ':' are uncertain; l. 33 is almost illegible through chiselling, "
 "with 'sic?' over the n of plN. Names and words he identifies: Kharamazeye, qore, Arite(n), Amanitake, Amanapate (mnpte), "
 "Amanete (mnote), Makezeke (mkedoke), kharpkhe (xrpxe), Yismeniye, Aqateye, Pakhoras/Faras (pXrs), Shimale/Ibrim (Simlok), "
 "Pilqeyte/Philae, Selele, Azere (adere-ke), Azenil (adonili-ke-te), qesw, hrw (Xrw), yireqw, kdileb 'women', Arekhetaye (aroXetye), "
 "Patashize (ptSide), Patamakize (ptmkide), Kharêshaye and Yisakhteteye with qo, Wezi (wedi), 'eight kings' (qore 4 4). "
 "A word split by Griffith's type-line break or by a superscript line number is joined only where his notes or renderings show "
 "one word (aqtoye, ptpotekye, pilqoyte, nsdokes, kedebx, adereke, x(19)rpxe, qe(22)sw, bqob(25)te, bqo(26)bx, wo(34)kle, "
 "te(10)pke, t(14)lte, de(24)te); other spaces are as printed. My own '?' marks are on m vs h-underline and p vs k forms that stayed unclear at 2.5x or were not zoomed (repeats of mtr, the second bxemi); every other m, h-underline, s, p and k decision was checked at 2.5x.")
row = {"griffith_no": 94, "rem": "0094", "page": "pp. 27-29 (leaves n46-n48); notes pp. 28-32",
       "object": "Column drums (two), long royal inscription of king Kharamadoye",
       "site": "Kalabsha (Talmis), great temple of Mandulis, second column of the facade of the hall of columns",
       "lines": lines, "notes": notes}
json.dump(row, open('/private/tmp/claude-501/griffith_scripts/mi2a/read/0094.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(lines))
