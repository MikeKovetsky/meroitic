# Task: can the model read Meroitic cursive from a photograph?

If a model could read Meroitic script directly from photographs of inscriptions, it could help check disputed readings and read unpublished stones. Test it.

1. Find 2 to 5 photographs of Meroitic CURSIVE inscriptions that are openly licensed (Wikimedia Commons first; museum open-access collections such as the British Museum or Boston MFA if their terms allow) AND whose published transliteration you can find (REM number, FHN, Griffith, a museum record, a scholarly article). Good candidates: funerary stelae and offering tables from Karanog, Faras or Sedeinga; the Hamadab stela (BM EA 1650 / REM 1003); Meroitic inscriptions on Wikimedia's "Meroitic script" pages.
2. Download only the image files (jpg/png/tif) from Wikimedia (upload.wikimedia.org) or the museum's own image server, into a NEW empty folder `/private/tmp/claude-501/vision/` (create it). Nothing else may be downloaded or run from there. Record each file's URL, licence and size.
3. Where useful, crop or enlarge lines with Python (Pillow, if available: `python3 -I -c "import PIL"`; scripts go in a different folder, e.g. `/private/tmp/claude-501/vision_scripts/`). Then look at each image (the Read tool shows images) and transliterate as many signs as you can, line by line, right to left, in standard transliteration (a e i o y w b p m n ñ r l ḫ ẖ s se k q t te to d, word divider ":"), marking uncertain signs with "?".
4. Only AFTER your reading is written down, fetch the published transliteration and compare: sign-level accuracy (signs right / signs in the published text), words fully right, and the kinds of errors (confusable signs, direction, divider). Be honest: this is a capability test, not a show.
5. Write `/Users/mike/repos/mike/meroitic/data/discovery/vision.md`: each image (source URL, licence, inscription, published source), your reading, the published reading, the accuracy numbers, and a short verdict on whether the model can read the script from photos well enough to help.

Rules: no accounts or credentials; only image downloads from the named hosts; do not modify any other file in the repo. Work for at most about 60 minutes.

Final message: per-image accuracy and the verdict in two sentences.
