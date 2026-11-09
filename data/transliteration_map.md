# Meroitic transliteration map: standard (Hintze/Rilly) vs the corpus files

This file maps the standard transliteration of the 23 Meroitic signs to the ASCII convention of
`data/otten/Data/mero-corpus.txt` and the other Otten files, and lists where that convention is ambiguous.
Counts below were taken with grep/Python on `mero-corpus.txt` (18,090 lines, 5.8 MB) on 2026-11-08.

## 1. The short version

The corpus is written almost entirely in **Millet's (1968) convention**, which keeps Griffith's old names for
four signs. To go from the standard transliteration to the corpus spelling:

| Standard (Hintze/Rilly) | Corpus file | Example (standard → corpus) |
|---|---|---|
| `o` | `E` (Griffith/Millet ê) | `qore` → `qEre`, `ato` → `atE` |
| `s` (plain s sign) | `S` (Griffith š) | `wos` → `wES`, `ste` → `Ste` |
| `se` (syllabic se sign) | `s` (Griffith s) | `kdise` → `kdis`, `qore-se` → `qEris`, `tewiseti` → `tewisti` |
| `ne` (syllabic ne sign) | `N` (Griffith ñ) | `ḫrpḫne` → `xrpxN` |
| `ḫ` (3rd h, /χa/) | `x` | `ḫlbi` → `xlbi`, `tedḫe` → `tedxe` |
| `ẖ` (4th h, /χʷa/; Rilly 2016 prints it `h`) | `X` | `lẖ` → `lX`, `mẖe` → `mXe` |
| `to` (syllabic to sign) | `tE` | `pesto`/`peseto` → `pestE` |
| everything else | unchanged | `abr`, `kdi`, `pqr`, `yetmde`, `terike` |

Apply the rules in this order: `se`→`s`, then plain `s`→`S`, `ne`→`N`, `to`→`tE`, `o`→`E`, `ḫ`→`x`, `ẖ`→`X`.

The coordinator's test corpus converts the file back part of the way: Millet's `E` → `o`, uncertain-reading
capitals → lowercase, and `S`, `X`, `x`, `N` kept. In that test convention: `qore`, `woS`, `pelmoS`, `atE` → `ato`.
The `corpus_form` fields in `gold_lexicon.json` and `gold_morphology.json` are in the **original file's
spelling** (with `E`).

## 2. The 23 signs

Sign list and values from Rilly & de Voogt 2012 (Table 1.1, p. 7), Rilly 2016 (UEE "Meroitic", Fig. 3) and
Rilly 2022 (UEE "Meroitic Writing", pp. 8–9). Order as in Hintze's list (Wikipedia, "Meroitic script").

| # | Standard (Hintze/Rilly) | Older (Griffith 1911 / Millet 1968) | Value (Rilly) | Corpus ASCII | Notes |
|---|---|---|---|---|---|
| 1 | `a` | a | initial /a/ or /u/ only | `a` | Only word-initially (`abr`, `ato`, `amni`). |
| 2 | `e` | e | /e/, /ə/ or no vowel | `e` | Also the "killer" mark for a bare consonant. |
| 3 | `i` | i | vowel modifier /i/ | `i` | Initial /i/ is written `yi`. |
| 4 | `o` | ê (Griffith), E (Millet) | vowel modifier /u/ (maybe /o/) | `E` | **Often typed as lowercase `e` in the corpus** (see 4.2). No lowercase `o` occurs in the file. |
| 5 | `y` | y | /ya/; dummy before initial e/i | `y` | `ye-`/`yi-` mark initial /e/, /i/ (`yetmde`, `yireqe`). |
| 6 | `w` | w | /wa/ | `w` | |
| 7 | `b` | b | /ba/ | `b` | Alternates with `p` (`qorpse`/`qorbse`). |
| 8 | `p` | p | /pa/ (?) or /ba/ | `p` | Mostly Egyptian loans; phonemic status doubtful. |
| 9 | `m` | m | /ma/ | `m` | |
| 10 | `n` | n | /na/ | `n` | Nasals before consonants are not written (`ktke` = /kandake/). |
| 11 | `ne` | ñ | /ne/, /nə/ or /n/ | `N` | FHN-based lines sometimes keep `ne` (8 hits: `iddne`, `mne`, `nete`). |
| 12 | `r` | r | /ra/ | `r` | |
| 13 | `l` | l | /la/ | `l` | |
| 14 | `ḫ` | ḫ / kh (3rd h) | /χa/ | `x` | |
| 15 | `ẖ` | ẖ (4th h); Rilly 2016 prints `h` | /χʷa/ | `X` | |
| 16 | `s` | š / sh | /sa/ ([ɕ]) | `S` | FHN-based lines write it `s` (see 4.1). |
| 17 | `se` | s | /se/, /sə/ or /s/ | `s` | FHN-based lines write it `se`. |
| 18 | `k` | k | /ka/ | `k` | |
| 19 | `q` | q | /kʷa/ | `q` | |
| 20 | `t` | t | /ta/ | `t` | |
| 21 | `te` | te | /te/, /tə/ or /t/ | `te` | Same letters as t + e (see 4.4). |
| 22 | `to` | tê | /tu/ | `tE` | Same letters as t + o. |
| 23 | `d` | z (Griffith 1911), d (Millet) | /da/, [ɽ] between vowels | `d` | Griffith's `z` (Pezeme, Apezemak) is modern `d`. |
| — | `:` word divider | : | | space | No `:` survives in the corpus; Millet's `:` became spaces. |

Rilly 2016 (UEE, p. 5) prints `ẖ` as `h` and `ḫ` as `x`; Rilly 2010 (as cited by Lipiński 2011), Hintze and
Wikipedia print `ḫ` and `ẖ`. The gold files use `ḫ`/`ẖ` in `form` and give ASCII spellings in `variants`.

## 3. Other symbols in the corpus

| Symbol | Count | Meaning | Ambiguity |
|---|---|---|---|
| `E` | 387,447 | the `o` sign | also, rarely, Millet's E in names; and `e` often stands for it (4.2) |
| `S`, `s`, `N`, `x`, `X` | 104,816 / 100,888 / 43,065 / 81,709 / 73,568 | see table above | `s` changes meaning in FHN lines (4.1) |
| `A M P L R Q K W B D T G I Y U` | 2,335 / 1,572 / 1,556 / 986 / 803 / 778 / 397 / 394 / 294 / 198 / 4 / 4 / 2 / 2 / 1 | dotted letters, i.e. uncertain readings of a, m, p, l, r, q, k, w, b, d, t, …; the test corpus lowercases them | `A` also "A with a dot"; `G` has no Meroitic value (a damaged sign) |
| `H` | 92 | Millet's "H-tilde", an uncertain h sign (`atmetH`) | not a standard sign |
| `h` | 491 | appears mainly in `tdhelEwi` (393), a variant of `tdxelEwi`, and `mh.witr` | not one of the 23 signs; most likely a variant transcription of `x` |
| `g` | 94 | only in `grmrwet` (92) and `pilege` (2, probably a typo for `pilqe` Philae) | no Meroitic `g`; transcription error or uncertain sign |
| `.` | 41,925 | lost or illegible sign(s) (Millet's dots, FHN's `[.]`) | sometimes sits where a word divider was, splitting or joining words (`Sklte.lxeye`, `trqye.yetmde`) |
| `…` | 23 | longer lacuna (FHN `[…]`) | |
| digits | — | Meroitic numeral signs | |
| `?`, `,`, `|` | 7 / 4 / 1 | editorial marks | |

## 4. Where the convention is ambiguous

### 4.1 Two conventions in one file: `s` means two different signs

Most lines follow Millet (plain s = `S`, se sign = `s`). A few long royal texts were taken from *Fontes
Historiae Nubiorum* (Hintze's convention) and only had `o` → `E` applied, so in them plain s = `s` and the se
sign = `se`:

- line 17060, the Hamadab stela of Amanirenas and Akinidad (`amnirense qEre li kdwe li … qes … abrse l`),
- line 6234, the Tanyidamani stela (`qEre tNyidamani aleqese … sErse …`),
- the Kalabsha text of Kharamadoye appears in Millet's version (line 6487: `SEb`, `wESslw`), not the FHN one.

So `qes` (Kush, FHN line) would be `qeS` in Millet's spelling, and FHN `abrse` (abr-se "of a man") would be
`abrs`. Treat `s` before `e` in those lines as possibly the se sign.

### 4.2 `E` versus `e`

Millet's `E` (= `o`) is often typed as lowercase `e`, so after the test conversion some `o` words stay with `e`:
`qEwi` 6,079 vs `qewi` 4,231; `qE` 9,493 vs `qe` 5,214; `SSEr` 977 vs `SSer` 92; `atE` 4,311 vs `ate` 792;
`kditelEwi` 975 vs `kditelewi` 198; `SEri` vs `Seriqetrri` (777). The gold files list these as
`corpus_variants`.

### 4.3 `x` versus `X` for the same word

The two h signs alternate in real spellings and in transcriptions: `atE mXe` 1,377 vs `atE mxe` 1,164
(Lipiński 2011 notes `mẖe` is "spelled also `mḫe`"). Do not treat `x`/`X` as a hard contrast for matching.

### 4.4 Syllabic signs versus consonant + vowel

`te` (te sign) and `tE` (to sign) are indistinguishable from t + e and t + o. In Millet's lines `s` (se sign)
is distinct from `Se` (s + e), and `N` (ne sign) from `ne`; in FHN lines they are not. Rilly 2022 (p. 8):
the four signs ne, se, te, to "cannot be followed by a vowel modifier" and are frequent in suffixes (`-te` "in",
`-se` "of").

### 4.5 Initial vowels and prefixes

Initial `a` stands for /a/ or /u/; initial /e/ and /i/ are written with a dummy `y` (`ye`, `yi`). Words
therefore appear with and without `y`/`t`: `terike`/`yerike`/`erike`, `tedxe`/`tdxe`, `yereqe`/`yireqw`.

### 4.6 Word boundaries

Spaces reflect Millet's word dividers or editorial cuts, and Meroitic dividers often separate phrases, not
words. Many tokens fuse words (`yetmdelEwiateqi`, `abryeterikelEwi`) and some split one word (`yetmdelE wi`,
`t dxe`). Match lexical forms as substrings, with care for short forms (`at`, `mk`, `ar`).

### 4.7 The corpus is augmented

`mero-corpus.txt` repeats each inscription many times with personal names swapped into name slots (see
`data/texts.jsonl`, fields `variants` and `name_slots`). Token counts are therefore inflated and say little
about real frequency.

## 5. How the gold files use this map

- `form`: standard Hintze/Rilly transliteration (Unicode `ḫ`, `ẖ`).
- `corpus_form`: the most common spelling of the word in `mero-corpus.txt`, in the original file's convention
  (with `E`). When the word does not occur, it is the converted spelling the word would have.
- `corpus_variants`: other spellings of the same word found in the file (with/without final vowel, `e` for
  `E`, `x`/`X`, with/without initial `y`/`t`); stems only, without suffixes.
- `in_corpus`: `"token"` (occurs as a whole token), `"substring"` (only inside longer tokens) or `false`.
- `corpus_token_count`: whole-token count in the augmented file.
- `corpus_note`: a warning where a short form matches unrelated words or names.

## Sources

- Claude Rilly and Alex de Voogt, 2012, *The Meroitic Language and Writing System*, Cambridge University Press,
  Table 1.1 p. 7 and pp. 7–10 ([publisher excerpt](https://beckassets.blob.core.windows.net/product/readingsample/10057218/9781107008663_excerpt_001.pdf)).
- Claude Rilly, 2016, "Meroitic", *UCLA Encyclopedia of Egyptology*, Fig. 3 and pp. 4–6
  ([eScholarship](https://escholarship.org/uc/item/3128r3sw)).
- Claude Rilly, 2022, "Meroitic Writing", *UCLA Encyclopedia of Egyptology*, pp. 8–9
  ([eScholarship](https://escholarship.org/uc/item/2ts0n9p0)).
- Edward Lipiński, 2011, "Meroitic (Review article)", *Rocznik Orientalistyczny* 64(2): 87–104
  ([PDF](https://repozytorium.uni.lodz.pl/xmlui/bitstream/handle/11089/4031/No_2_2011.87-104.pdf)).
- F. Ll. Griffith, 1911, *Karanog: The Meroitic Inscriptions of Shablul and Karanog*, pp. 8–11, 22–23
  ([archive.org](https://archive.org/details/karangmeroitic00grifuoft)).
- Wikipedia, "Meroitic script" ([Hintze's list](https://en.wikipedia.org/wiki/Meroitic_script)).
- Header comments of the Otten files: `HamadabStelaOfAmanirenasNarrative.txt`, `TanyidamaniNarrative.txt`,
  `KalabshaMeroiticInscriptionOfKharamadoyeNarrative.txt` ("Dotted letters transcribed with capitals. 4th h
  transcribed as 'X'; 3rd h transcribed as 'x'; S-hat transcribed as 'S'; N-tilda transcribed as 'N'"),
  `Kalabsha_Millet.txt` ("Millet's 'E' (E-hat) appears to correlate with the Fontes Historiae Nubiorum 'o'").
