# Task: transcribe Griffith's printed Meroitic, Meroitic Inscriptions II (Griffith 1912) nos. 75 to 105

A test showed you can read the Meroitic cursive TYPE printed in F. Ll. Griffith's editions at 95.6% sign accuracy against the modern REM text (99.6% against what Griffith printed): `/Users/mike/repos/mike/meroitic/data/expansion/printed_type_test.md`. Read it first: it has the sign key, the crop method, the timing and the two lessons (zoom on every sign you mark uncertain; m and ẖ are the confusable pair). Its scripts and the sign chart are in `/private/tmp/claude-501/griffith_scripts/` and page images in `/private/tmp/claude-501/griffith/` (reuse what fits). Python with Pillow and pypdf: `/Users/mike/repos/mike/viewfy/backend/.venv/bin/python`. Sources and ids: `/Users/mike/repos/mike/meroitic/data/expansion/README.md`.

Your share: Meroitic Inscriptions II (Griffith 1912), inscriptions 75 to 105 (archive.org item archaeologicals20egyp). REM number = the Griffith number, four digits (no. 75 = REM 0075); for nos. 97 to 111 reuse the readings saved by the test in /private/tmp/claude-501/griffith_scripts/ where they exist, finishing any lines the test skipped.

For each inscription in your share that Griffith prints in Meroitic type:
1. Find it in the volume (the archive.org OCR word boxes or page images help locate the Meroitic lines; Griffith's English and his notes are fine to read here, this is transcription, not a blind test).
2. Read every line, right to left, sign by sign, into standard transliteration (a e i o y w b p m n ñ r l ḫ ẖ s se k q t te to d; word divider written as ":"), marking uncertain signs with "?" after the sign and lost signs as "[.]". Zoom on every uncertain sign before deciding.
3. Also give the same text in the corpus spelling of `/Users/mike/repos/mike/meroitic/data/corpus_v2.jsonl`: drop ":" and write words separated by spaces; s → S, se → s, ñ → N, ḫ → x, ẖ → X; everything else as is; drop "?" marks but keep "[.]" as ".".
4. Note the object (stela, offering table, graffito, altar...), the site, and anything Griffith says that bears on the reading.

Write one JSON per inscription to `/Users/mike/repos/mike/meroitic/data/expansion/griffith_mi2a.jsonl`:
{"source": "Meroitic Inscriptions II (Griffith 1912)", "item": "archaeologicals20egyp", "griffith_no": 1, "rem": "0001", "page": "...", "object": "...", "site": "...", "text_std": "...", "text_corpus": "...", "uncertain": 0, "signs": 0, "notes": "..."}
(`uncertain` = number of signs marked "?", `signs` = total signs read.)

Rules: download only page images or the item's PDF/JP2 from archive.org or HathiTrust into `/private/tmp/claude-501/griffith/` (or a subfolder); scripts go in `/private/tmp/claude-501/griffith_scripts/` or a subfolder of your own; no accounts. Do not modify any other repo file. Work for at most about 90 minutes; if you run out of time, write what you have and list the numbers you did not reach.

Final message: inscriptions transcribed, total signs, share of uncertain signs, and the numbers you skipped and why.
