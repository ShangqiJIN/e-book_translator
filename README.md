# EPUB Translator V6 Lite

V6 intentionally removes the heavy V5.x workflow.

Expected path:

`HTML/EPUB/TXT/MD -> chapterNN.md -> model translates each chapter once -> EPUB`

For HTML there is no intermediate source EPUB. There are no prose-bearing JSON batches and no model-generated merge stage. Chapters are not proactively split.

Minimal work directory:

- `units/chapterNN.md`
- `translations/chapterNN.md`
- `translation_profile.md`
- `terminology.json`
- `state.json`

PDF is conservative: V6 does not OCR by default.
