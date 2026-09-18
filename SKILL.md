---
name: epub-translator
description: Lightweight chapter-first book translation for HTML, EPUB, TXT, MD, and text-layer PDF inputs, with EPUB output and minimal model overhead.
---

# EPUB Translator V6 Lite

Purpose: make automatic long-form translation behave as closely as possible to manual chapter-by-chapter translation.

## Core workflow

`source -> lightweight chapter Markdown -> translate chapter once -> save -> next chapter -> build EPUB once`

The model does language work only. Deterministic scripts do extraction, progress, validation, and EPUB building.

Do not convert HTML to EPUB before translation. Do not create prose-bearing JSON. Do not ask the model to merge files. Do not proactively split normal chapters.

## Inputs

Run `python scripts/prepare.py SOURCE --work-dir WORK`.

- HTML/HTM: extract chapters directly.
- EPUB: read XHTML directly.
- TXT/MD: normalize directly.
- PDF: text-layer only. Never OCR by default. If no safe local text extraction is available, stop and report it.

All inputs become `work/units/chapterNN.md`.

## Model-facing text

Use lightweight Markdown plus minimal SEG anchors. SEG is only a reconstruction/validation anchor, never a separate translation request.

Preserve natural paragraphs. Never sentence-split prose. Translate the complete chapter in one model context by default. Preserve SEG markers exactly and in order. Preserve useful lightweight formatting such as `*italics*`.

## Preview

Unless explicitly skipped, translate the first substantial chapter, save it, build a preview EPUB, then stop for user feedback. After approval update `translation_profile.md`, run `approve_preview.py`, and continue automatically.

## Production loop

1. Run `next_chapter.py`.
2. Read only that chapter, concise profile, selective terminology, and a small previous tail if useful.
3. Translate the entire chapter directly to `translations/chapterNN.md`.
4. During translation, if a new recurring, ambiguous, or book-specific term requires a stable translation across later chapters, append only that term and its chosen translation to `terminology.json`. Do not perform a separate terminology-review pass. Do not add ordinary vocabulary, personal names already covered by the profile, or terms whose translation is obvious and does not require cross-chapter consistency.
5. Run `save_translation.py`.
6. Continue immediately.

Do not reread completed chapters. Do not narrate routine file operations. Do not perform model QA or a separate terminology-extraction pass after every chapter.

## Long chapters

Try whole-chapter translation first. Split only after an actual practical context/output limitation. If splitting is necessary, split between paragraphs into a few large parts and retain a small previous tail. Never split inside a paragraph.

## Book-specific rules

Keep them in `translation_profile.md`, not here. Examples: preserve personal names in English; special treatment for Russian dialogue.

Keep `terminology.json` selective. Do not automatically add every name or noun.

## Token discipline

Never inspect the whole book in model context. Never reread completed translations. Never create an intermediate `source.epub` for HTML/TXT/MD. Never create JSON containing prose. Never write ad-hoc conversion scripts when supplied scripts support the input. After compaction reload only profile, relevant terminology, minimal state, previous tail, and next chapter.

## Finish

When `next_chapter.py` returns DONE, run `build_epub.py` once for the full EPUB and then `validate.py`.
