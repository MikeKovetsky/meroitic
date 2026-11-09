"""For given Commons file titles: categories, thumb url (1000px), original url/size/licence,
and whether the description LOOKS like it holds a transliteration (boolean only, text not shown)."""
import json, re, sys
sys.path.insert(0, "/private/tmp/claude-501/vision_scripts")
from commons import get
titles = sys.argv[1:]
d = get({"action": "query", "titles": "|".join(titles), "prop": "imageinfo|categories",
         "iiprop": "url|size|extmetadata", "iiurlwidth": "1000", "cllimit": "50"})
for p in d["query"]["pages"]:
    ii = (p.get("imageinfo") or [{}])[0]
    em = ii.get("extmetadata", {})
    desc = re.sub(r"<[^>]+>", " ", em.get("ImageDescription", {}).get("value", ""))
    looks = bool(re.search(r"\b(wos|soreyi|qore|tedḫe|terik|ato\b|mhe|psḫ)", desc, re.I)) or desc.count(":") >= 3
    cats = [c["title"].replace("Category:", "") for c in p.get("categories", [])]
    print(p["title"])
    print("  licence:", em.get("LicenseShortName", {}).get("value"), "| artist:", re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value", ""))[:80])
    print("  size:", ii.get("width"), "x", ii.get("height"), ii.get("size"), "B")
    print("  orig:", ii.get("url"))
    print("  thumb:", ii.get("thumburl"))
    print("  desc chars:", len(desc), "| looks like translit:", looks)
    print("  cats:", "; ".join(cats)[:400])
