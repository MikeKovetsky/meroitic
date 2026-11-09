from sources import src
M = []
def F(form, variants, function, confidence, sources, evidence, cf=None, cv=(), note=None):
    d = dict(form=form, variants=list(variants), function=function, confidence=confidence,
             sources=sources, evidence_note=evidence, corpus_form=cf, corpus_variants=list(cv))
    if note: d['corpus_note'] = note
    M.append(d)

F('-l', ['-li', '-le'], 'singular determiner (article); links the members of a noun phrase and is required before genitive and postpositional suffixes; often best translated "a"', 'certain',
  [src('UEE2016', 'pp. 7-8'), src('RdV2012', 'pp. 138-143 (The Determinant)'), src('R2004', 'p. 6', 'article -l /la/ from Proto-NES *de'), src('GRIFFITH1911', 'p. 23')],
  'Identified by Griffith as the suffix of a qualified word; Rilly derives it from Proto-NES *de (Nara demonstrative te).',
  'l', ['li', 'lE'])
F('-leb', ['-lb'], 'plural determiner (article)', 'certain',
  [src('UEE2016', 'p. 7', 'mk-leb "(the) gods"'), src('R2004', 'p. 6', 'plural -leb /laba/ from Proto-NES *degu'), src('GRIFFITH1911', 'p. 23', 'plural leb')],
  'Plural of -l in all contexts (pqr-leb, mk-leb); the only regular marker of noun plurality.',
  'leb')
F('-b-', ['-b'], 'plural marker inside the determiner and pronouns (/ba/)', 'certain',
  [src('UEE2016', 'p. 8', 'from Proto-NES pronominal plural *-gu'), src('RdV2012', 'pp. 153-154'), src('WIKI_ML')],
  'Seen in -l/-leb, -ḫ(e)/-bḫ(e) and plural verb forms; Rilly derives it from Proto-NES *-gu.',
  'b')
F('-se', ['-s'], 'genitive "of" (analytic genitive for alienable relations), placed after the possessor and its determiner: ant mk-li-se "priest of the god"', 'certain',
  [src('UEE2016', 'p. 7'), src('UEE2022', 'p. 8', '-se "of"'), src('RdV2012', 'pp. 146-150'), src('GRIFFITH1911', 'p. 23', '-s for the genitive')],
  'Griffith from phrases like "prophet of Isis" (ant Wos-se); Rilly distinguishes it from the juxtaposed genitive.',
  's', ['se'], 'Millet-convention lines write the se sign as s (qEris = qore-se); FHN royal texts write se.')
F('(juxtaposition)', [], 'synthetic genitive for inalienable relations: possessor + determiner + head noun, no suffix (ant-li kdite "sister of a priest")', 'certain',
  [src('UEE2016', 'p. 7'), src('RdV2012', 'p. 147')],
  'Kinship descriptions in epitaphs (X-l kdite-lowi); original Proto-NES genitive *-n lost as in Nara.')
F('-te', [], 'locative "in, at"', 'certain',
  [src('UEE2016', 'p. 8', 'Bedewi-te "in Meroe"'), src('UEE2022', 'p. 8', '-te "in"'), src('GRIFFITH1911', 'pp. 23, 34', 'Wos Pileq-te-li "Isis in Philae"'), src('RdV2012', 'p. 152')],
  'Place names + -te in titles and pilgrims\' graffiti (Isis in Philae, priest in Meroe).',
  'te')
F('-yte', ['-yete', '-ite'], 'directional locative after place names, in "from X to Y" phrases; direction of the relation is read differently by different scholars', 'debated',
  [src('WIKI_ML', None, 'Simalo-ke dik Selele-yte "from Simalo to Selele"'), src('LIP2011', 'p. 99')],
  'Kharamadoye inscription: Simlo-k dik Selele-yte. Wikipedia reads -yte as "to" and -ke as "from"; Millet translated the reverse.',
  'yte')
F('-ke', ['-k'], 'local postposition in "from X to Y" phrases (ablative "from" or terminative "as far as"); allative "to" in Lipinski\'s reading of Bedewi-k sdk "to Meroe"', 'debated',
  [src('WIKI_ML', None, '-k(e) ablative'), src('LIP2011', 'p. 99', 'Bedewi-k sdk p-ro-ḫe-ne, "to Meroe"')],
  'Kharamadoye inscription and travel prayers; scholars disagree on the direction.',
  'k')
F('-i', ['-yi'], 'vocative "O ...!" on divine names (Wos-i "O Isis!", Sorey-i "O Osiris!")', 'certain',
  [src('UEE2016', 'p. 8'), src('RdV2012x', 'p. 10'), src('RdV2012', 'p. 155'), src('GRIFFITH1911', 'p. 23')],
  'Invocation opening epitaphs, syntactically independent of the rest of the text; Griffith identified it as vocative.',
  'i', ['yi'], 'wESi, SEreyi')
F('-o', [], 'copula, singular ("is/was"), attached to the determiner (-l-o)', 'certain',
  [src('UEE2016', 'p. 8', 'ktke-l-o "She is the Candace"'), src('RdV2012', 'p. 164'), src('WIKI_ML', None, 'Old Nubian focus -lo from Meroitic -l + -o')],
  'Non-verbal predication in epitaphs; Old Nubian -lo continues -l + -o.',
  'E')
F('-lowi', ['-lo', '-l-o-wi'], 'predicative ending of epitaph clauses: determiner -l + copula -o + emphatic -wi, "he/she is (was) the ..." (X tedḫe-lowi "born of X")', 'certain',
  [src('UEE2016', 'p. 8', 'apote-l-o-wi "He was an envoy"'), src('GRIFFITH1911', 'p. 23', 'lowi for the copula (?) or emphasis (?)')],
  'Ends nearly every descriptive clause of epitaphs; Rilly segments it as -l-o-wi.',
  'lEwi', ['lE', 'lewi'])
F('-wi', [], 'emphatic marker after the singular copula (-o-wi)', 'probable',
  [src('UEE2016', 'p. 8', '"considered as an emphatic marker"')],
  'Optional element after -o; Rilly reports it as an emphatic marker.',
  'wi')
F('-kwi', ['-lebkwi'], 'copula, plural ("they are/were")', 'certain',
  [src('UEE2016', 'pp. 4, 8', 'pqr-leb yetmde-leb-kwi "They were nephews of princes"'), src('RdV2012', 'p. 164'), src('GRIFFITH1911', 'p. 23', 'plural lebakwi')],
  'Plural epitaphs; cognate with Old Nubian -agoue and Proto-Taman *agi.',
  'kwi', [], 'rare in the corpus (terikelebkwi, yedxelebkwi, yeritelebkwi).')
F('qo-wi', ['qo', '-qowi'], 'presentative with personal names: demonstrative qo "this" + copula, "this is N" (nomination clause of epitaphs)', 'certain',
  [src('UEE2016', 'pp. 8-9', 'Akilible qo-wi "This is Akilibale"'), src('RdV2012', 'p. 12 (Nomination); pp. 163-166')],
  'Follows the deceased\'s name after the invocation; older readings (Griffith, Millet) took qo/qe as "noble".',
  'qEwi', ['qE', 'qewi', 'qe'])
F('-ḫ(e)', ['-x', '-xe', '-kh(e)'], 'verbal dative / object pronoun, 3rd person singular ("to him/her"), placed inside the verb', 'probable',
  [src('UEE2016', 'p. 7', 'pwrite l-x-te "Give him life!"'), src('RdV2012', 'p. 158')],
  'Royal prayers for life; contrasts with plural -bḫ(e).',
  'x', [], 'not separable by spelling alone; it sits inside verb forms.')
F('-bḫ(e)', ['-bx', '-bxe', '-bkh(e)'], 'verbal dative / object pronoun, plural ("to them"); appears in benedictions for several deceased', 'probable',
  [src('UEE2016', 'p. 7', 'pwrite l-b-x-te "Give them life!" (REM 0018)'), src('RdV2012', 'p. 158')],
  'Same prayers with plural beneficiaries; plural funerary benedictions add -bḫ- to the verb.',
  'bx', [], 'e.g. bSixrbxes, bSiXebxes in plural epitaphs.')
F('-te (imperative)', [], 'imperative singular verbal ending', 'probable',
  [src('UEE2016', 'p. 8', 'l-x-te "Give him!"')],
  'Rilly reads it in royal prayers; homonymous with locative -te.')
F('-kete', ['-kese', '-kes'], 'plural imperative/optative ending of the funerary benediction verbs, addressed to Isis and Osiris ("may you (pl.) ...")', 'probable',
  [src('UEE2016', 'p. 8', '-kete plural imperative: p-tre-kete "Offer ye!"'), src('RdV2012', 'pp. 19-30 (Formulas A to X)')],
  'Benedictions A (ato mẖe ps-...-kete, water) and B (at mẖe ps-...-kete, bread) after the invocation of Isis and Osiris.',
  'kete', ['kes'], 'the corpus mostly has -kes (piSiXekes, pSixrkes) beside -kete.')
F('p-', ['pi-', 'b-'], 'verbal prefix of benediction and prayer verbs, possibly an optative auxiliary ("may ...")', 'debated',
  [src('UEE2016', 'p. 8', '"p- could be an optative auxiliary"')],
  'Initial element of benediction verbs (p-tre-kete, psi-...-kete); Rilly gives the optative reading with reservation.',
  'p', ['b'], 'benediction verbs start with p or b (piSiXekes, bSixrbxes).')
F('ps-', ['psi-', 'pso-', 'pis-'], 'prefix complex of the water and bread benediction verbs (p- + s-element); function of the s-element unknown', 'debated',
  [src('UEE2016', 'p. 8'), src('RdV2012', 'pp. 19-30 (Formulas A to X)')],
  'Constant in formulas A and B (ato mẖe ps-...-kete, at mẖe ps-...-kete); segmentation varies between authors.',
  'pS', ['piS', 'bS'])
F('-w', ['-xe'], 'accusative/dative case marking on nouns (rare survivals)', 'probable',
  [src('UEE2016', 'p. 7', 'suffix -w or -xe, from Proto-NES *g + vowel')],
  'Rilly 2010: 394-395; local variants of one old case suffix.')
F('m-', [], 'negative marker', 'probable',
  [src('RdV2012', 'p. 171'), src('LIP2011', 'pp. 93, 104', 'Rilly 2010: 398-399; kdi-m-dḫe "woman who has not given birth" (Millet 1996)')],
  'Rilly 2010 compares Proto-NES negation; kdi-m-dḫe in epitaphs.')
F('-se (each)', [], 'distributive "each", distinct from the genitive -se', 'debated',
  [src('R2010', 'p. 138'), src('LIP2011', 'p. 99')],
  'Listed by Rilly 2010 among translated items; context-based, no wider confirmation found.')
F('tedḫe', ['tdḫe', 'yedḫe', 'dḫe', 'tedhe'], 'filiation predicate for the mother: mother\'s name + tedḫe-lowi "(he/she was) born of"', 'certain',
  [src('RdV2012', 'p. 14 (Filiation)'), src('GRIFFITH1911', 'p. 23', '"to bear": tedhe, yedhe'), src('R2010', 'p. 120')],
  'Filiation clause; follows women\'s names (mother); t-/y- initial element varies.',
  'tedxe', ['tdxe'])
F('terike', ['erike', 'yerike'], 'filiation predicate for the father: father\'s name + terike-lowi "(he/she was) begotten by"', 'certain',
  [src('RdV2012', 'p. 14 (Filiation)'), src('GRIFFITH1911', 'p. 23', '"to beget": terike, yerike'), src('R2010', 'pp. 122-123')],
  'Filiation clause; follows men\'s names (father).',
  'terike', ['yerike'])
F('yetmde', [], 'relationship predicate: X yetmde-lowi "(he/she was) a relative (nephew/niece) of X"', 'certain',
  [src('UEE2016', 'p. 8'), src('R2010', 'p. 147'), src('RdV2012', 'p. 17 (Description of relatives)')],
  'Most frequent term in the description of relatives in epitaphs; exact degree debated.',
  'yetmde')
