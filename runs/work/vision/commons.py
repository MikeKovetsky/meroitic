"""Query Wikimedia Commons for candidate files; print license, size, url.
Descriptions are masked where they look like a transliteration (no peeking)."""
import json, re, sys, urllib.error, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "MeroiticVisionTest/0.1 (one-off research script; contact: mike@sunapp.ai) python-urllib"

def get(params):
    params = dict(params, format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    import time
    for attempt in range(6):
        time.sleep(1.2)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(int(e.headers.get("Retry-After") or 5) + 2 * attempt)
    raise RuntimeError("rate limited")

def mask(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    # mask colon-separated runs of short lowercase words (transliteration-like)
    text = re.sub(r"(\b[\wḫẖñ-]+\b\s*:\s*){2,}[\wḫẖñ-]*", "[MASKED]", text)
    text = re.sub(r"\S*[ḫẖ]\S*", "[M]", text)
    keep = set("""Meroitic Meroe Meroë British Museum Karanog Faras Sedeinga Sai Nubia Sudan Egypt Penn Pennsylvania
    University Stela Stele Offering Table Funerary Inscription Inscribed Sandstone Louvre Berlin Munich München Aegyptisches
    Ägyptisches Staatliches Khartoum National Ashmolean Oxford Boston Fine Arts Metropolitan Brooklyn Walters Kingdom King Queen
    The A An In At On From With Of This It Its Neues Altes Hamadab Naga Musawwarat Kawa Qasr Ibrim Philae Dakka Shablul Gammai
    Arminna Toshka Ballana Qustul Wadi Halfa Kerma Dongola Nag Gamus Masmas Masmás Royal Ontario ROM Expedition REM EA ÄS AE
    Oriental Institute Chicago Leipzig Toronto Cambridge Fitzwilliam Petrie London Paris Vienna Kunsthistorisches Collection
    Nubian Kushite Kush Ptolemaic Roman Period AD BC CE BCE Kursive Cursive Hieroglyphic Script Writing Language Text Ostracon
    Sandstein Inschrift Jh Chr Estela Necrópolis Época Nubien Nubie Musée Écriture""".split())
    text = re.sub(r"\b([A-ZÄÖÜÉÈ][\w'’-]*)", lambda m: m.group(1) if m.group(1) in keep else "[Cap]", text)
    return text[:200]

def info(titles):
    out = []
    for i in range(0, len(titles), 40):
        d = get({"action": "query", "titles": "|".join(titles[i:i+40]), "prop": "imageinfo",
                 "iiprop": "url|size|extmetadata|mime"})
        for p in d["query"]["pages"]:
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            lic = em.get("LicenseShortName", {}).get("value", "?")
            desc = mask(em.get("ImageDescription", {}).get("value", ""))
            out.append((p["title"], ii.get("width"), ii.get("height"), ii.get("size"), lic, ii.get("url"), desc))
    return out

def cat(name, depth=0, seen=None):
    seen = seen or set()
    files, subs = [], []
    cont = {}
    while True:
        d = get(dict({"action": "query", "list": "categorymembers", "cmtitle": name, "cmlimit": "500",
                      "cmtype": "file|subcat"}, **cont))
        for m in d["query"]["categorymembers"]:
            (files if m["ns"] == 6 else subs).append(m["title"])
        if "continue" in d:
            cont = d["continue"]
        else:
            break
    return files, subs

def search(q, n=50):
    d = get({"action": "query", "list": "search", "srsearch": q, "srnamespace": "6", "srlimit": str(n)})
    return [m["title"] for m in d["query"]["search"]]

if __name__ == "__main__":
    mode, arg = sys.argv[1], sys.argv[2]
    if mode == "cat":
        files, subs = cat(arg)
        print("SUBCATS:", subs)
        titles = files
    else:
        titles = search(arg)
    if "--names" in sys.argv:
        for t in titles: print(t)
    else:
        for t in info(titles) if titles else []:
            print(f"{t[0]} | {t[1]}x{t[2]} | {t[3]} B | {t[4]}\n   {t[5]}\n   desc: {t[6]}")
