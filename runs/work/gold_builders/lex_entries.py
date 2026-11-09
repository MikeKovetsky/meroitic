from sources import src
L = []
NOTES = {}
def E(form, variants, gloss, category, confidence, sources, evidence, cf, cv=()):
    d = dict(form=form, variants=list(variants), gloss=gloss, category=category,
             confidence=confidence, sources=sources, evidence_note=evidence,
             corpus_form=cf, corpus_variants=list(cv))
    L.append(d)

# ---- basic vocabulary (Rilly 2016 'basic vocabulary' list; Rilly 2004 list of Griffith-era words) ----
E('abr', ['br'], 'man', 'noun', 'certain',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'pp. 114-115')],
  'Royal war narratives count captured abr beside kdi (men vs women); Griffith-era translation kept by Rilly.',
  'abr')
E('kdi', ['kadi'], 'woman', 'noun', 'certain',
  [src('UEE2016', 'pp. 7, 9'), src('R2004', 'pp. 3, 5'), src('WIKI_ML')],
  'Hesychius glosses kandē as Greek "woman"; base of ktke "Candace"; paired with abr in captive lists; NES cognates.',
  'kdi')
E('asr', ['sr'], 'meat, animal', 'noun', 'certain',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3', 'in the list of words solidly translated since Griffith ("meat")'), src('R2010', 'p. 118')],
  'Griffith-era translation; Rilly 2004 lists "meat" among words solidly translated since Griffith.',
  'asr')
E('at', [], 'bread', 'noun', 'certain',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'pp. 118-119'), src('WIKI_ML')],
  'Funerary benediction B ("at mẖe ...", abundant bread); Griffith-era translation of the stereotyped epitaph formulas.',
  'at')
E('ato', ['ate'], 'water', 'noun', 'certain',
  [src('UEE2016', 'pp. 6, 9'), src('R2004', 'p. 3'), src('R2010', 'pp. 119-120'), src('GRIFFITH1911', 'p. 23', '"water"'), src('WIKI_ML')],
  'Funerary benediction A ("ato mẖe ...", abundant water) on offering tables; Greek Asta- in Nile river names (Astaboras, Astapous).',
  'atE', ['ate'])
E('kdite', ['kdise'], 'sister', 'kinship', 'certain',
  [src('UEE2016', 'pp. 4, 7, 9'), src('R2004', 'p. 3'), src('R2010', 'p. 128')],
  'Relationship clauses of epitaphs; cognates Proto-Nubian *kedidi, Proto-Nara *kadete (Rilly 2016: 4).',
  'kdite', ['kdis', 'kdise'])
E('ked', ['kede'], 'kill, slay', 'verb', 'certain',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 5'), src('R2010', 'pp. 128-130')],
  'Royal war narratives (lists of enemies killed); NES *kod- "slaughter".',
  'ked', ['kede'])
E('l-', ['l'], 'give', 'verb', 'certain',
  [src('UEE2016', 'pp. 7, 9'), src('R2004', 'p. 3'), src('R2010', 'pp. 130-132')],
  'Royal prayers to the gods: pwrite l-ḫ-te "Give him life!" (REM 1151).',
  'l')
E('lẖ', ['lh', 'lx', 'laẖ'], 'great, elder', 'adjective', 'certain',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'p. 132'), src('GRIFFITH1911', 'p. 23', 'adjective "great"'), src('WIKI_ML')],
  'Titles and epithets (mk-lẖ "great god", pelmos-lẖ "chief general"); kdite-lẖ "elder sister". Rilly 2016 prints it lx (font).',
  'lX')
E('mẖe', ['mhe', 'mḫe'], 'abundant, plenty', 'adjective', 'certain',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'p. 133')],
  'Funerary benedictions ato mẖe / at mẖe "abundant water / bread"; also spelled mḫe (Lipinski 2011: 97).',
  'mXe', ['mxe'])
E('mlo', [], 'good', 'adjective', 'certain',
  [src('UEE2016', 'p. 9'), src('RdV2012x', 'p. 6'), src('R2010', 'pp. 133-134')],
  'Napatan names write mlo with Egyptian heart-and-trachea (nfr "good") ideogram; funerary mlo-l-o "he/she was good".',
  'mlE')
E('mte', ['mse', 'mete'], 'child', 'kinship', 'certain',
  [src('UEE2016', 'p. 9'), src('RdV2012x', 'p. 6'), src('UEE2022', 'p. 9'), src('R2010', 'p. 134')],
  'Napatan names write mte with the Egyptian determinative of a child sucking its thumb; later spelling mse.',
  'mte', ['mse'])
E('sem', ['sm'], 'wife', 'kinship', 'certain',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'p. 139')],
  'Relationship clauses of epitaphs (X sem-lowi "she was the wife of X"); Griffith-era translation.',
  'sm')
E('ste', ['sete'], 'mother (tutor)', 'kinship', 'certain',
  [src('UEE2016', 'p. 9', 'glossed "tutor", common designation for "mother"'), src('R2004', 'p. 3'), src('R2010', 'p. 140')],
  'Relationship clauses of epitaphs (X ste-lowi "she was the mother of X"); Rilly refines to "tutor".',
  'Ste')
E('st', [], 'foot, feet', 'noun', 'certain',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'p. 139')],
  'Graffiti carved beside engraved footprints in temples ("st qo": these are the feet of N).',
  'St')
E('tre-', ['tre'], 'offer', 'verb', 'probable',
  [src('UEE2016', 'pp. 8-9', 'imperative p-tre-kete "Offer ye!"'), src('R2010', 'pp. 143-144')],
  'Offering contexts and benedictions; analysed by Rilly as verb stem in p-tre-kete.',
  'tre')
E('wide', ['wi'], 'brother', 'kinship', 'certain',
  [src('UEE2016', 'p. 9', 'often assimilated to wi- before the article'), src('R2004', 'p. 3'), src('R2010', 'p. 144')],
  'Relationship clauses of epitaphs (X wi-lowi "he was the brother of X").',
  'wide', ['wi'])
E('mk', [], 'god, deity', 'noun', 'certain',
  [src('UEE2016', 'p. 7'), src('RdV2012x', 'p. 6'), src('R2010', 'p. 153')],
  'Napatan names write mk with the Egyptian flag sign (ntr "god"); mk-leb "the gods"; in Apede-mk.',
  'mk')
E('mkdi', [], 'goddess', 'noun', 'certain',
  [src('UEE2016', 'p. 7', 'mkdi < mk + kdi')],
  'Compound of mk "god" and kdi "woman" used to mark female deities (Wos mkdi-lẖ "Isis the great goddess").',
  'mkdi')
E('tedḫe', ['tdḫe', 'edḫe', 'dḫe', 'yedḫe', 'tedhe'], 'born of (mother)', 'kinship', 'certain',
  [src('RdV2012', 'p. 14 (Filiation)'), src('R2004', 'p. 3'), src('R2010', 'p. 120'), src('GRIFFITH1911', 'p. 23', '"to bear": tedhe, yedhe'), src('WIKI_ML')],
  'Filiation clause of epitaphs: mother\'s name + tedḫe-lowi; Griffith 1911 already glossed it "to bear".',
  'tedxe', ['tdxe'])
E('terike', ['erike', 'yerike'], 'begotten by (father)', 'kinship', 'certain',
  [src('RdV2012', 'p. 14 (Filiation)'), src('R2004', 'p. 3'), src('R2010', 'pp. 122-123'), src('GRIFFITH1911', 'p. 23', '"to beget": terike, yerike'), src('WIKI_ML')],
  'Filiation clause of epitaphs: father\'s name + terike-lowi, paired with tedhe for the mother.',
  'terike', ['yerike', 'erike'])
E('yetmde', [], 'relative (nephew, niece)', 'kinship', 'certain',
  [src('UEE2016', 'p. 8', 'pqr-leb yetmde-leb-kwi "they were nephews of princes"'), src('R2010', 'p. 147'), src('WIKI_ML')],
  'Most frequent relationship term in epitaphs; Rilly reads a collateral kinsman, translated "nephew"; exact degree debated.',
  'yetmde')
# ---- words added by Rilly 2010 (multicontextual method), marked probable ----
E('ar', ['or'], 'boy, son', 'noun', 'probable',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'pp. 115-116')],
  'Rilly 2010 via contexts and NES comparison; element -or in names (Netror).',
  'ar')
E('are-', ['are', 'erk-'], 'take, receive (seize)', 'verb', 'probable',
  [src('UEE2016', 'p. 9'), src('R2004', 'pp. 3, 5'), src('R2010', 'pp. 116-117')],
  'Razzia contexts in royal narratives; NES *ar "take".',
  'are')
E('dm-', ['dm'], 'take, receive', 'verb', 'probable',
  [src('UEE2016', 'p. 9'), src('UEE2022', 'p. 9'), src('R2004', 'p. 5'), src('R2010', 'p. 122')],
  'Rilly 2010: 82-86 from royal texts; NES *dom- "pick up, take".',
  'dm')
E('dime', [], 'cow', 'noun', 'probable',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'pp. 120-121')],
  'Counted livestock in royal texts (REM 0064, 0070); Lipinski suggests "head (of cattle)" instead.',
  'dime')
E('ḫre', ['ḫr-', 'hre', 'xre'], 'meal, food (eat)', 'noun', 'probable',
  [src('UEE2016', 'p. 9'), src('R2004', 'pp. 3, 5'), src('R2010', 'p. 125')],
  'Reconstructed from funerary benediction C ("x-mlo-l", a good meal); NES *go(o)r "eat".',
  'xre')
E('ḫlbi', ['hlbi', 'xlbi'], 'bull, ox', 'noun', 'probable',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'pp. 123-124')],
  'Cattle offering lists (REM 0064, 0070); in royal protocols the same spelling may be a deity (Lipinski 2011).',
  'xlbi')
E('pwrite', [], 'life', 'noun', 'probable',
  [src('UEE2016', 'pp. 7, 9', 'pwrite l-x-te "Give him life!"'), src('R2004', 'p. 3'), src('R2010', 'pp. 135-136')],
  'Prayers for the king in temple texts, parallel to Egyptian ankh "life" formulas.',
  'pwrite')
E('tke-', ['tke'], 'love, revere', 'verb', 'probable',
  [src('UEE2016', 'p. 9'), src('R2004', 'p. 3'), src('R2010', 'pp. 141-142')],
  'Royal epithet Mni tke parallels Egyptian mry Jmn "beloved of Amun".',
  'tke')
E('wle', [], 'dog', 'noun', 'probable',
  [src('UEE2016', 'p. 9'), src('R2004', 'pp. 3, 5'), src('R2010', 'p. 145')],
  'Graffito REM 1165 at Musawwarat beside a drawn dog; NES *wel "dog".',
  'wle')
E('yer', [], 'milk', 'noun', 'probable',
  [src('UEE2016', 'p. 9'), src('UEE2022', 'p. 9'), src('R2004', 'pp. 3, 5'), src('R2010', 'p. 146')],
  'Rilly 2010 from textual contexts; NES *er- "milk, breast".',
  'yer')
E('aroẖe-', ['arohe', 'aroẖe'], 'protect', 'verb', 'probable',
  [src('R2004', 'p. 3'), src('R2010', 'p. 117')],
  'Rilly 2004/2010 from royal and religious contexts; Lipinski compares Demotic hrh "watch over".',
  'arEXe')
E('nse', ['ns'], 'sacrifice', 'noun', 'probable',
  [src('R2004', 'p. 3'), src('R2010', 'p. 135')],
  'Rilly 2004/2010 from offering contexts (ns-per).',
  'ns')
E('sdk', [], 'journey', 'noun', 'probable',
  [src('R2004', 'p. 3'), src('R2010', 'p. 138'), src('LIP2011', 'p. 99', 'Millet (1977) read "safely"')],
  'Prayers Wos-i Bedewi-k sdk p-ro-ḫe-ne for travel to Meroe; Millet translated "safely".',
  'sdk')
E('sḫi', ['shi', 'sxi'], 'small', 'adjective', 'probable',
  [src('R2010', 'p. 139')],
  'Listed among Rilly 2010\'s 43 translated words; no wider confirmation found.',
  'Sxi')
E('tbo', ['tbe'], 'two, second', 'number', 'probable',
  [src('R2010', 'p. 140', 'marked with a query by Rilly'), src('LIP2011', 'p. 101')],
  'Rilly 2010: 140 marks the meaning with a query; Millet (1968) read tbE as "two" after pairs of names.',
  'tbE')
E('teneke', [], 'west', 'noun', 'probable',
  [src('UEE2016', 'p. 9'), src('R2010', 'p. 141')],
  'Rilly 2010 (cultural vocabulary, cardinal direction); no Nilo-Saharan parallel.',
  'teneke')
E('yireqe', ['yereqe'], 'south', 'noun', 'probable',
  [src('R2010', 'p. 147'), src('LIP2011', 'p. 102')],
  'Kharamadoye inscription: directional terms paired with frontier places; Rilly 2010.',
  'yereqe', ['yireqw'])
E('yirewke', [], 'east', 'noun', 'probable',
  [src('R2010', 'p. 147'), src('LIP2011', 'p. 102')],
  'Rilly 2010 from directional contexts.',
  'yirewke')
E('ẖr', ['hr', 'ẖrw'], 'north', 'noun', 'probable',
  [src('R2010', 'p. 126'), src('LIP2011', 'p. 95')],
  'Kharamadoye inscription: ẖrw ... pilqo-ke, northwards to Philae; Rilly 2010.',
  'Xr')
E('kelw', ['kelwe'], 'and, also', 'other', 'probable',
  [src('R2010', 'p. 86'), src('LIP2011', 'p. 103')],
  'Coordinates lists of persons and offerings in epitaphs and ostraca.',
  'kelw')
E('abese', [], 'gazelle', 'noun', 'probable',
  [src('R2010', 'p. 411 (addendum)'), src('LIP2011', 'pp. 102-103')],
  'Added by Rilly 2010 in the addendum among animal names.',
  'abes')
E('pete', [], 'snake', 'noun', 'probable',
  [src('R2010', 'p. 411 (addendum)'), src('LIP2011', 'p. 103')],
  'Added by Rilly 2010 in the addendum among animal names.',
  'pete')
E('abore', [], 'elephant', 'noun', 'probable',
  [src('R2010', 'pp. 370-371'), src('LIP2011', 'p. 103')],
  'Rilly 2010: 370-371; Lipinski 2011 calls the meaning well known.',
  'abEre')
E('ms', ['mash', 'mš', 'mos'], 'sun (god)', 'deity', 'probable',
  [src('RdV2012x', 'p. 5', 'Mash (sun god) in proto-Meroitic names'), src('R2010', 'pp. 192-193, 371-372'), src('WIKI_ML')],
  'Divine name in proto-Meroitic names and Meroitic titles; Old Nubian masal "sun" borrowed from Meroitic masa-l.',
  'mS')
E('nob', [], 'slave; Nubian', 'people', 'probable',
  [src('UEE2016', 'p. 9', 'nob "slave"'), src('UEE2022', 'p. 9', 'nob "Nubian"'), src('R2011', 'p. 16')],
  'Name of the Noba people, also used for captives; Proto-Nubian *nogu.',
  'nEb')
# ---- titles ----
E('qore', ['qor', 'qr'], 'ruler, king', 'title', 'certain',
  [src('UEE2016', 'p. 9'), src('R2010', 'p. 136'), src('WIKI_ML')],
  'Royal title of male and female sovereigns in royal inscriptions (qore Tanyidamani; Amanirenas qore).',
  'qEre', ['qEr', 'qr'])
E('ktke', ['kdke'], 'queen-mother (Candace)', 'title', 'certain',
  [src('UEE2016', 'pp. 8-9'), src('UEE2022', 'p. 9'), src('WIKI_ML')],
  'Greek kandakē, Latin Candace, Egyptian kntky; nasal before consonant not written.',
  'ktke', ['kdke'])
E('pqr', ['pqore'], 'prince, crown prince', 'title', 'certain',
  [src('UEE2016', 'pp. 8-9'), src('GRIFFITH1911', 'p. 55', 'paqar and peshte are princely titles; paqar takes precedence')],
  'Title of royal princes such as Akinidad (pqr qorise "prince of the ruler").',
  'pqr')
E('ant', ['at'], 'priest, prophet', 'title', 'certain',
  [src('UEE2016', 'pp. 7-9', '< Egyptian hm-ntr'), src('LIP2011', 'p. 99')],
  'Egyptian loan from hm-ntr "prophet" (Coptic hont); ant Mnp "priest of Amanap".',
  'ant')
E('apote', ['apete', 'epote'], 'envoy', 'title', 'certain',
  [src('UEE2016', 'pp. 8-9', '< Egyptian wpwtj'), src('KUCK2021', 'p. 19', 'apote arome-li-se from Egyptian wpw.tj'), src('GRIFFITH1911', 'p. 11', 'apete = Demotic wpte "envoy"')],
  'Egyptian loan wpwtj "messenger"; apote arome-li-se "envoy to Rome".',
  'apEte')
E('pelmos', ['plmos', 'pelamos'], 'general (strategos)', 'title', 'certain',
  [src('UEE2016', 'p. 9', '< Egyptian p3-mr-msa'), src('RdV2012x', 'p. 9'), src('KUCK2021', 'p. 18', 'pelmos ato-li-se, pelmos adb-li-se'), src('GRIFFITH1911', 'p. 22')],
  'Egyptian loan p3-mr-msa "the general"; read /pelamusa/.',
  'pelmES', ['pElmES'])
E('ssor', ['sesor'], 'scribe', 'title', 'certain',
  [src('UEE2016', 'p. 9', '< Egyptian ss')],
  'Egyptian loan from ss "scribe".',
  'SSEr', ['SSer'])
E('tewiseti', ['tewisti'], 'adoration', 'noun', 'certain',
  [src('UEE2016', 'p. 9', '< Demotic t3-wst.t'), src('GRIFFITH1911', 'pp. 9, 22', 'tewisti, "the adoration" (proskynema) in Philae graffiti')],
  'Demotic loan "adoration"; opens pilgrims\' proskynema graffiti.',
  'tewisti')
E('nbr', [], 'gold', 'noun', 'certain',
  [src('UEE2016', 'p. 9', '< Egyptian nbw')],
  'Egyptian loan nbw "gold".',
  'nbr')
# ---- deities ----
E('wos', ['wosi'], 'Isis', 'deity', 'certain',
  [src('RdV2012x', 'p. 10', 'Wos-i "O Isis"'), src('UEE2016', 'p. 8'), src('GRIFFITH1911', 'pp. 23, 34')],
  'Invocation opening epitaphs, Wos-i "O Isis!", from Egyptian 3st (Coptic Ese).',
  'wES', ['wESi'])
E('sorey', ['asori', 'sori', 'asorey'], 'Osiris', 'deity', 'certain',
  [src('RdV2012x', 'p. 10', '(A)sorey-i "O Osiris"'), src('UEE2022', 'p. 9', 'Asori "Osiris" read /usuri/'), src('GRIFFITH1911', 'p. 11', 'Asheri = Egyptian Wsr, Osiris')],
  'Second member of the epitaph invocation (A)sorey-i "O Osiris!", from Egyptian Wsir.',
  'SEre', ['SEri', 'SEreyi', 'aSEri', 'Seri'])
E('amni', ['mni', 'amn'], 'Amun', 'deity', 'certain',
  [src('UEE2016', 'p. 4'), src('R2011', 'p. 13'), src('GRIFFITH1911', 'p. 23', 'Amani, Eg. Amun')],
  'Name of the god Amun (Egyptian Jmn), main god of the Meroites; in royal names (Natakamani).',
  'amni', ['mni'])
E('amnpte', ['amnp', 'mnp'], 'Amun of Napata', 'deity', 'certain',
  [src('UEE2016', 'p. 8'), src('UEE2022', 'p. 9', 'Amnpte read /aman-napat/, Egyptian Jmn-Npt')],
  'From Egyptian Jmn-Npt "Amun of Napata"; ant Mnp "priest of Amanap".',
  'amnp', ['mnp', 'amnpte'])
E('apedemk', ['apdmk', 'pdmk'], 'Apedemak (lion god)', 'deity', 'certain',
  [src('R2011', 'p. 16', 'Apede-mak "God Apede"'), src('R2004', 'p. 5'), src('RdV2012x', 'p. 5'), src('GRIFFITH1911', 'p. 23', 'Apezemak, the Lion-god')],
  'Lion god (Griffith 1911: "the Lion-god"); Rilly analyses Apede + mk "god", with Apede from Proto-NES *Ebede "Creator God".',
  'apedemk')
# ---- places ----
E('bedewe', ['medewe', 'bedewi', 'medewi'], 'Meroe', 'place', 'certain',
  [src('UEE2016', 'p. 6', 'Medewi, later Bedewi = Eg. Mrw.t, Greek Meroe'), src('UEE2016', 'p. 8', 'Bedewi-te "in Meroe"')],
  'Matches Egyptian Mrw.t and Greek Meroe; intervocalic d heard as r by Egyptians and Greeks.',
  'bedewe', ['bedewi', 'medewi'])
E('tolkte', [], 'Naga (city)', 'place', 'certain',
  [src('UEE2016', 'p. 6')],
  'Meroitic name of the city of Naga, from royal temple inscriptions.',
  'tElkte')
E('qoreti', [], 'Qurta (city)', 'place', 'certain',
  [src('UEE2016', 'p. 5'), src('UEE2022', 'p. 9')],
  'Rilly cites the Greek transcription of Qurta in Lower Nubia; read /kwurti/.',
  'qEreti')
E('akine', ['akin'], 'Lower Nubia', 'place', 'certain',
  [src('UEE2022', 'p. 9'), src('KUCK2021', 'p. 20', 'northern Meroitic province of Akine'), src('GRIFFITH1911', 'p. 55', 'Akin, place name at Shablul and Karanog')],
  'Province of Lower Nubia governed by the peseto (Akinidad); Rilly reads /akin(e)/.',
  'akiN')
# ---- function words ----
E('qo', [], 'this (demonstrative)', 'other', 'certain',
  [src('UEE2016', 'p. 8', 'qo "this"; Amnisxeto qo "This is Amanishakheto"'), src('LIP2011', 'p. 93')],
  'Nomination clause N qo-wi "this is N" in epitaphs; older readings (Griffith, Millet) took qe/qo as "noble one".',
  'qE', ['qe'])
# ---- added after interim: titles and places with Griffith 1911 / Kuckertz 2021 support ----
E('peseto', ['pesto', 'peste', 'pesate'], 'viceroy', 'title', 'certain',
  [src('KUCK2021', 'pp. 18, 20', 'peseto (viceroy); Akinidad installed as first governor (peseto) of Akine'), src('GRIFFITH1911', 'p. 55', 'peshte/peste: a princely title'), src('PENN', None, 'peshto, the princely governor of Lower Nubia')],
  'Title of the governors (viceroys) of the province Akine (Lower Nubia), e.g. Akinidad; also in Demotic and Greek graffiti at Philae.',
  'pestE', ['peStE'])
E('perite', ['prite'], 'agent (administrator)', 'title', 'certain',
  [src('GRIFFITH1911', 'p. 22', 'loan-word perite, Eg. "the Agent"'), src('WIKI_MS', None, 'Coptic prit "the agent" -> Meroitic perite')],
  'Egyptian loan (Coptic prit "agent"); perite Wos-se "agent of Isis" in Philae and Karanog texts.',
  'perite', ['prite'])
E('beloloke', ['belileke', 'beleleke'], 'priest (a rank)', 'title', 'probable',
  [src('GRIFFITH1911', 'p. 55', 'belileke of Amanap or of Amun, in Napata or Pedeme')],
  'Title attached to gods (beloloke of Amanap / of Amun) and temple towns, hence a priestly rank; exact office unknown.',
  'belElEke', ['belilEke'])
E('arome', ['areme', 'arme'], 'Rome', 'place', 'certain',
  [src('GRIFFITH1911', 'p. 11', 'Areme = Demotic Hrme "Rome"'), src('KUCK2021', 'p. 19', 'apote arome-li-se "envoy to the Roman Empire"')],
  'Matches Demotic Hrme in the title "great envoy to Rome" (apote arome-li-se) of Philae graffiti.',
  'arEme')
E('atiye', ['atiyete'], 'Sedeinga', 'place', 'certain',
  [src('GRIFFITH1911', 'p. 9', 'name of Sedeinga, Egyptian "fortress (temple) of Tiye"'), src('KUCK2021', 'p. 20', 'sleqene Atiye-te, an official at Sedeinga')],
  'From Egyptian Hwt-Tiye, the temple of Queen Tiye at Sedeinga.',
  'atiye')
E('npte', ['napate', 'npt'], 'Napata', 'place', 'certain',
  [src('GRIFFITH1911', 'p. 23', 'Napate, Napata (Eg. Npt)'), src('UEE2022', 'p. 9', 'Amnpte = Egyptian Jmn-Npt "Amun of Napata"')],
  'Egyptian Npt, Greek Napata; also inside the god name Amnpte "Amun of Napata".',
  'npte')
E('pilqe', ['pileqe', 'pilqo', 'pilaqe'], 'Philae', 'place', 'certain',
  [src('GRIFFITH1911', 'pp. 8, 34', 'name of Philae, Demotic P-iy-lq, Coptic Pilak; "Wos Pileq-te-li" = Isis in Philae')],
  'Matches Demotic and Coptic names of Philae; Wos Pilqe-te-li "Isis in Philae" in pilgrims\' graffiti.',
  'pilqe')
E('pẖrs', ['phrs', 'pakharas', 'pakhoras'], 'Faras (Pachoras)', 'place', 'probable',
  [src('GRIFFITH1911', 'pp. 62, 82', 'Pakhoras (Faras); Pakharas (Faras?)')],
  'Matches Greek/Coptic Pachoras, the ancient name of Faras; Griffith once marks the identification with a query.',
  'pXrs')
E('pedeme', ['pezeme'], 'Qasr Ibrim (Primis)', 'place', 'probable',
  [src('TM1916', None, 'Pedeme listed as the Meroitic name of Qasr Ibrim / Primis'), src('GRIFFITH1911', 'p. 55', 'Griffith read Pezeme and took it for Amara')],
  'Modern view: Pedeme > Greek/Latin Primis (Qasr Ibrim); Griffith 1911 identified it with Amara instead.',
  'pedeme')
E('kisri', [], 'Caesar (Roman emperor)', 'title', 'certain',
  [src('UEE2022', 'p. 9', 'Kisri "Caesar", read /kaisari/'), src('RdV2012x', 'p. 9')],
  'Transcription of Greek Kaisar; only the second element of the diphthong is written.',
  'kiSri')
E('adb', ['adebe'], 'land, territory', 'noun', 'probable',
  [src('KUCK2021', 'p. 18', 'pelmos adb-li-se "strategos of the land"')],
  'Title pelmos adb-li-se, contrasted with pelmos ato-li-se "general of the water"; Millet read "desert".',
  'adb')
E('qes', ['qos', 'qesw'], 'Kush', 'place', 'probable',
  [src('WIKI_ML', None, 'Meroitic toponym qes / qos, citing Rilly 2007 and 2011')],
  'Endonym matching Egyptian K3s "Kush", attested in royal inscriptions (Hamadab stela).',
  'qes', ['qeS'])

E('tkk', ['tk-'], 'plunder, pillage', 'verb', 'probable',
  [src('R2010', 'pp. 77-78, 142-143', 'derived from tk "take"'), src('LIP2011', 'p. 102')],
  'Royal war narratives (Akinidad stela REM 1003, Hamadab stela) in razzia passages.',
  'tkk')

_notes = {
 'abr': 'also br- after loss of initial a (brleb "the men" in the Kharamadoye text); br alone matches many names.',
 'l-': 'absent: the stem is not separable in the corpus; the token l there is the article (FHN royal texts).',
 'dm-': 'substring only, inside names (Sdmdekde, lXidmni); no clear attestation of the verb.',
 'ar': 'short form; corpus tokens ar/ar- may be other words or name parts.',
 'are-': 'short form; corpus token are may be another word.',
 'tre-': 'substring only, inside longer words; no clear attestation.',
 'tke-': 'mostly inside names (ateqiSitkemEli, twteNtkeli); one token tke.',
 'nse': 'short form; tokens ns/mns may be other words.',
 'ms': 'Millet convention mS (m + plain s); the corpus also has mS inside names (mStrq).',
 'abese': 'only inside the personal name abesye.',
 'pete': 'only inside other words (atpete, tpeteNteli).',
 'st': 'one token St; Ste (mother) is a different word.',
 'sḫi': 'absent as a word; Sxi occurs only inside names.',
 'yer': 'absent as a word; yer occurs only inside other words (yerike).',
 'ẖr': 'stem inside Xrw (northward) and Xres in the Kharamadoye text.',
 'ḫre': 'absent as a word; formula C writes x-mlE-l, read by Rilly as x(re) mlo-l.',
 'aroẖe-': 'one token arEXetye in the Kharamadoye text.',
}
for d in L:
    if d['form'] in _notes: d['corpus_note'] = _notes[d['form']]
E('sye', ['saye', 'shaye'], 'Sai (island)', 'place', 'probable',
  [src('GRIFFITH1911', 'pp. 65, 82', '"Shaye is the island of Sai"')],
  'Place name in titles of Karanog epitaphs (X in Shaye); Griffith equates it with Sai island.',
  'Sye')
E('tebwe', ['tebawe'], 'Abaton (Philae)', 'place', 'probable',
  [src('GRIFFITH1911', 'pp. 62, 82', 'perhaps Tebawe, the "Holy Place" (Abaton) in or near Philae')],
  'Paired with Philae in phrases naming forms of Isis and Osiris (Wos Pilqe-te-l, Wos Tebwe-te-l); Griffith hedges with "perhaps".',
  'tebwe')
for d in L:
    if d['form'] == 'sye': d['corpus_note'] = 'substring only, in Syeteli ("in Sai").'

E('ḫrpḫe', ['ḫrpḫne', 'xrpxe', 'xrpxN', 'kharpkhe'], 'governor (?)', 'title', 'debated',
  [src('MILLET1968', 'pp. 54, 77', 'xrpxN pXrs-te "governor of Faras"'), src('GRIFFITH1911', 'pp. 62, 70', 'kharpakhe / kharpkhan in Pakharas, a title, untranslated')],
  'High administrative title often tied to a place (ḫrpḫne Pẖrs-te "in Faras"); Griffith left it untranslated; the gloss "governor" rests on Millet only.',
  'xrpxN', ['xrpxe'])
for d in L:
    if d['form'] == 'kisri':
        d['corpus_note'] = 'corpus hits come from one repeated Lower Nubian text (kiSri mkesmeN axid ...); whether kiSri means "Caesar" there has not been checked.'
    if d['form'] == 'tbo':
        d['corpus_note'] = 'tbE also occurs inside atbEs and tbEyet.'
