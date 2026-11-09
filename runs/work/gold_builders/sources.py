# Source records; every entry cites these with optional page numbers.
S = {
 'UEE2016': dict(author='Claude Rilly', year=2016, title='Meroitic', publication='UCLA Encyclopedia of Egyptology', url='https://escholarship.org/uc/item/3128r3sw'),
 'UEE2022': dict(author='Claude Rilly', year=2022, title='Meroitic Writing', publication='UCLA Encyclopedia of Egyptology', url='https://escholarship.org/uc/item/2ts0n9p0'),
 'RdV2012': dict(author='Claude Rilly and Alex de Voogt', year=2012, title='The Meroitic Language and Writing System', publication='Cambridge University Press', url='https://doi.org/10.1017/CBO9780511920028'),
 'RdV2012x': dict(author='Claude Rilly and Alex de Voogt', year=2012, title='The Meroitic Language and Writing System, ch. 1 (publisher excerpt, pp. 1-10)', publication='Cambridge University Press', url='https://beckassets.blob.core.windows.net/product/readingsample/10057218/9781107008663_excerpt_001.pdf'),
 'R2010': dict(author='Claude Rilly', year=2010, title='Le méroïtique et sa famille linguistique', publication='Peeters (Afrique et Langage 14), pages as reported in Lipiński 2011', url='https://repozytorium.uni.lodz.pl/xmlui/bitstream/handle/11089/4031/No_2_2011.87-104.pdf'),
 'LIP2011': dict(author='Edward Lipiński', year=2011, title='Meroitic (Review article) [review of Rilly 2010]', publication='Rocznik Orientalistyczny 64(2): 87-104', url='https://repozytorium.uni.lodz.pl/xmlui/bitstream/handle/11089/4031/No_2_2011.87-104.pdf'),
 'R2004': dict(author='Claude Rilly', year=2004, title='The Linguistic Position of Meroitic', publication='ARKAMANI Sudan Electronic Journal of Archaeology and Anthropology', url='https://web.archive.org/web/20150923213222/http://www.ddl.ish-lyon.cnrs.fr/projets/clhass/PageWeb/ressources/Isolats/Meroitic%20Rilly%202004.pdf'),
 'R2011': dict(author='Claude Rilly', year=2011, title='Recent Research on Meroitic, the Ancient Language of Sudan', publication='ITYOPIS 1: 10-24', url='http://www.ityopis.org/Issues-1_files/ITYOPIS-I-Rilly.pdf'),
 'WIKI_ML': dict(author='Wikipedia contributors', year=2026, title='Meroitic language (Vocabulary section)', publication='Wikipedia', url='https://en.wikipedia.org/wiki/Meroitic_language#Vocabulary'),
 'GRIFFITH1911': dict(author='F. Ll. Griffith', year=1911, title='Karanog: The Meroitic Inscriptions of Shablul and Karanog', publication='University Museum, Philadelphia (Eckley B. Coxe Jr. Expedition to Nubia VI)', url='https://archive.org/details/karangmeroitic00grifuoft'),
 'KUCK2021': dict(author='Josefine Kuckertz', year=2021, title='Meroe and Egypt', publication='UCLA Encyclopedia of Egyptology', url='https://escholarship.org/uc/item/6061m848'),
 'TM1916': dict(author='Trismegistos (KU Leuven)', year=2026, title='Trismegistos Places, record 1916: Qasr Ibrim (Primis / Pedeme)', publication='Trismegistos database', url='https://www.trismegistos.org/place/1916'),
 'WIKI_MS': dict(author='Wikipedia contributors', year=2026, title='Meroitic script', publication='Wikipedia', url='https://en.wikipedia.org/wiki/Meroitic_script'),
 'PENN': dict(author='Penn Museum', year=None, title='Karanog, Wealthy Capital of a Lower Nubian Province', publication='Expedition Magazine', url='https://www.penn.museum/sites/expedition/karanog-wealthy-capital-of-a-lower-nubian-province/'),
 'MILLET1968': dict(author='Nicholas B. Millet', year=1968, title='Meroitic Nubia (PhD dissertation, Yale University)', publication='University Microfilms; cited via the transcription MilletExamples.txt in the Otten repository, not checked against the original', url=None),
 'LOBBAN': dict(author='Lobban list (unverified)', year=None, title='LobbanVocabList.txt in the Otten corpus repository', publication='repository file', url=None),
}
def src(key, pages=None, note=None):
    d = dict(S[key])
    if pages: d['pages'] = pages
    if note: d['note'] = note
    return d
