# Couple OA Note 8105

A light handwritten Chinese font for notes, messages and small labels. Text remains editable in ordinary design software.

Part of the [Couple OA Fonts collection](https://github.com/georgehuang000/couple-oa-todo-font), alongside Couple OA Todo.

[Live preview](https://georgehuang000.github.io/couple-oa-todo-font/note/) · [Downloads](https://github.com/georgehuang000/couple-oa-todo-font/releases/tag/note-v2.100) · [中文](README.md) · [License](OFL.txt)

![Actual font specimen](assets/specimen.png)

- All **8,105** Han characters in the 2013 Table of General Standard Chinese Characters.
- **8,234** mapped characters including Latin letters, digits, common punctuation and spaces.
- **196** supplementary-plane characters, supported with Unicode format 12 cmap.
- One Regular weight, provided as TTF and WOFF.

Install the TTF and select **Couple OA Note 8105**. The download includes an offline `index.html` specimen with editable text and coverage feedback. For web use, include `font.css` and apply `class="couple-note"`.

This is a general Simplified Chinese collection, not complete Traditional Chinese or Unicode coverage. Start at 24–40px for notes and larger sizes for dense characters.

## Editable sources

From a repository clone, run `cd note` first. For the standalone Source ZIP, run these commands in its extracted root.

```sh
python -m pip install -r requirements.txt
python tools/build.py
python tools/verify.py --fonts build/fonts --compare-release
```

Requires Python 3.10+ and fontTools. Editable outlines and metrics are stored in split TTX files under `source/`. Building the final fonts requires neither an ML model nor system fonts. After dependencies are installed, the build works offline.

## Provenance and release

Version **2.100** preserves 735 original project glyphs and metrics. Its 7,499 additional Han glyphs were regenerated with OFL-licensed Source Han Serif content inputs and the project's own handwritten style references. This differs from the earlier private prototype. See [PROVENANCE.md](PROVENANCE.md), [FONTLOG.md](FONTLOG.md) and [review scope](qa/review.json) for the exact process and verification limits.

The fonts and editable masters are licensed under **SIL OFL 1.1**. Commercial use, embedding, modification and redistribution are allowed under its terms. Preserve notices and the license, keep modified fonts under OFL, and do not sell the font on its own. Independent build and verification tools use [MIT](LICENSE-CODE); third-party notices remain in `licenses/`.

Maintained by [georgehuang000](https://github.com/georgehuang000). Please report the character, version, application and font size when filing a glyph issue.
