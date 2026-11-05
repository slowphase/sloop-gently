# SLOOP, Gently: editable source

This folder holds everything needed to rebuild both editions of the handbook, for example when SLOOP changes. You don't need any of it to *read* the book: the finished PDFs are on the [Releases page](https://github.com/suprsomething/sloop-gently/releases).

One manuscript, two editions.

## What's where

| Path | What it is |
| --- | --- |
| `book/content.html` | The verified manuscript (SLOOP 2.8.4). **Edit the words here.** Every lesson is a `<section class="page">`. |
| `book/build.py` | Assembles the manuscript into page order, places figures and resolves cross-reference tokens such as `{{P:anchor}}`. |
| `book/pages2.py`, `book/interior_sections.py` | Place the explanatory graphics on their pages. |
| `book/illus.py`, `book/interior.py`, `book/diagrams.py`, `book/art.py` | Draw the illustrations, diagrams and granular artwork (Python that writes SVG). |
| `book/proto_p11.html`, `proto_p20.html`, `proto_p25.html` | Three art-directed lesson pages. |
| `book/fm1_topview.svg` | The FM-1 hardware drawing, traced at true proportions. |
| `book/img/` | SLOOP screen and web-editor captures (third-party, see [NOTICE](book/img/NOTICE.md)). |
| `book/fonts/` | Albert Sans and Big Shoulders Display, latin subsets (SIL OFL 1.1). |
| `book/ds.css`, `a4.css`, `ipad.css` | The original light design system, which the editions restyle. |
| `concepts/` | Drawing helpers, the Weather lesson composition and the dark design concept the editions are built on. |
| `editions/build_editions.py` | Builds both editions: restyles the manuscript into the dark palette, composes each format and renders it. |
| `editions/ipad_draw.py` | Tall iPad redraws of the wide A4 diagrams. |
| `editions/theme.css`, `a4-theme.css`, `ipad-theme.css` | The shared design system and the per-edition layers. |
| `editions/finish_editions.py` | Adds PDF bookmarks and metadata, and audits every link. |
| `editions/check_editions.py` | Reports any A4 page whose content overflows. |

## Building

You'll need Python 3 with `pypdf`, `numpy` and `Pillow`, plus Google Chrome (or Chromium) available as `google-chrome`. The overflow check also needs `playwright`.

```
cd source/editions
python3 build_editions.py all    # writes out/SLOOP-Gently-A4.pdf and out/SLOOP-Gently-iPad-Mini.pdf
python3 finish_editions.py       # bookmarks, metadata and link audit
python3 check_editions.py        # optional: A4 overflow report
```

`build_editions.py a4` or `build_editions.py ipad` builds one edition. The iPad edition renders twice so that page numbers in the text come out right. A full build takes under a minute.

The granular artwork is randomly scattered, so the dots differ slightly from one build to the next. The text and layout do not.

## Rules the build keeps

- The build never rewrites text, it only places it. Page numbers in the text are tokens, resolved separately for each edition after pagination.
- SLOOP's four track colours appear only where a track is meant. Song sections A to D are greys. Lime is used for annotation.
- Every drawing restates a sentence that was checked against the official SLOOP 2.8.4 guide and firmware source. When updating for a newer SLOOP, please check the facts against that version's official documentation.

## Licences

The original text, artwork and diagrams are CC BY-SA 4.0. The build scripts and stylesheets are MIT. The fonts are SIL OFL 1.1. The SLOOP captures in `book/img/` are not covered by this project's licences. Full details are in [LICENSE.md](../LICENSE.md).
