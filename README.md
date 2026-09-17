# EPUB Translator V6 Lite

一个面向 Codex 的轻量级长文本翻译 Skill，用于将 HTML、EPUB、TXT 或 Markdown 长文本按章节自动翻译，并最终生成 EPUB。

A lightweight long-form translation skill for Codex. It translates HTML, EPUB, TXT, and Markdown books chapter by chapter and builds the completed translation as an EPUB.

## 中文

### 功能

EPUB Translator V6 Lite 的核心目标是让自动长文本翻译尽可能接近手动逐章翻译：

```text
原文件
  ↓
提取章节
  ↓
轻量 Markdown
  ↓
逐章翻译
  ↓
保存译文
  ↓
自动进入下一章
  ↓
生成 EPUB
```

模型只负责真正需要语言理解的部分：

```text
读取一章 → 翻译一章 → 保存 → 下一章
```

文件解析、进度记录、结构校验和 EPUB 构建均由确定性脚本完成。

### 支持格式

输入支持：

* HTML / HTM
* EPUB
* TXT
* Markdown
* PDF（有限支持，仅适用于能够可靠提取文本层的 PDF，不默认执行 OCR）

默认输出为 EPUB。

对于 HTML、TXT 和 Markdown，Skill 会直接提取正文，不会为了翻译先将源文件转换成 EPUB。

### 翻译中间格式

所有输入都会被转换成轻量 Markdown：

```text
work/
├── units/
│   ├── chapter01.md
│   ├── chapter02.md
│   └── chapter03.md
├── translations/
│   ├── chapter01.md
│   ├── chapter02.md
│   └── chapter03.md
├── translation_profile.md
├── terminology.json
└── state.json
```

正文使用少量 `SEG` 标记保留结构定位：

```markdown
# Chapter 18

<!--SEG:c18-p001-->
He looked at *Ilya* and said, "Don't do that." He had been waiting all night.

<!--SEG:c18-p002-->
Ilya did not answer.
```

`SEG` 只是结构定位和校验标记，不是独立的翻译单元。正常情况下，Codex 会读取并翻译完整章节，而不是逐个 `SEG` 翻译。

### 章节优先

V6 默认采用 chapter-first 策略。

正常章节保持完整：

```text
chapter01.md → chapter01.zh
chapter02.md → chapter02.zh
chapter03.md → chapter03.zh
```

不会为了控制任务大小而预先把章节拆成大量 batch 或 JSON。

只有实际遇到上下文或输出长度限制时，才将超长章节按自然段边界拆成少量较大的部分，并保留上一部分的少量上下文。

### 试译

默认情况下，Skill 会先翻译第一篇具有实质内容的章节，并生成试读 EPUB。

流程为：

```text
准备源文件
→ 翻译第一章
→ 保存译文
→ 生成 Preview EPUB
→ 等待用户确认
```

确认翻译风格后，更新 `translation_profile.md`，Skill 即可继续后续章节。

如果不需要试译，也可以明确要求跳过 Preview。

### 翻译规则

通用规则保存在 Skill 中，而具体作品的翻译要求写入：

```text
translation_profile.md
```

例如：

```markdown
Target: Simplified Chinese

## Book-specific rules

- 人名保持英文原文。
- 俄语内容采用括号形式处理。
- 保留原文中的语言差异。
- 保留斜体表达。
```

这样无需为了某一本书修改整个 Skill。

术语表保存在：

```text
terminology.json
```

例如：

```json
{
  "The Other Side": "彼岸",
  "Black Forest": "黑森林"
}
```

术语库只用于需要跨章节保持一致的专有词汇，不需要记录普通词汇。

### Token 优化

V6 避免在翻译之外重复消耗模型上下文：

* 不把整本书一次性加载进模型。
* 不重复读取已经完成的章节。
* 不将正文转换成 JSON。
* 不生成 translated batch JSON。
* 不让模型负责章节拼接。
* HTML / TXT / MD 输入不会先生成中间 EPUB。
* 不对每一章执行额外的模型 QA。
* 不主动把普通章节切成多个小 batch。
* context compaction 后只恢复必要状态、翻译规则、少量上下文和下一章。

因此正文在正常生产流程中只需要经过模型一次。

### 最终流程

```text
HTML / EPUB / TXT / MD
          ↓
      prepare.py
          ↓
  chapter01.md
  chapter02.md
  chapter03.md
          ↓
       Codex
          ↓
translations/
  chapter01.md
  chapter02.md
  chapter03.md
          ↓
    build_epub.py
          ↓
      book.zh.epub
```

---

## English

### Overview

EPUB Translator V6 Lite is designed to make automated long-form translation behave as closely as possible to manual chapter-by-chapter translation.

Its core workflow is intentionally simple:

```text
Source
  ↓
Extract chapters
  ↓
Lightweight Markdown
  ↓
Translate one chapter
  ↓
Save
  ↓
Continue automatically
  ↓
Build EPUB
```

The language model handles only the work that actually requires language understanding:

```text
Read one chapter → Translate one chapter → Save → Next chapter
```

Extraction, progress tracking, structural validation, and EPUB construction are handled by deterministic scripts.

### Supported Inputs

Standard inputs:

* HTML / HTM
* EPUB
* TXT
* Markdown
* PDF with limitations; only text-layer PDFs are supported when text can be extracted reliably. OCR is not performed by default.

The standard output is EPUB.

HTML, TXT, and Markdown sources are parsed directly. They are not converted to an intermediate EPUB before translation.

### Translation Representation

All supported inputs are normalized into lightweight Markdown chapters:

```text
work/
├── units/
│   ├── chapter01.md
│   ├── chapter02.md
│   └── chapter03.md
├── translations/
│   ├── chapter01.md
│   ├── chapter02.md
│   └── chapter03.md
├── translation_profile.md
├── terminology.json
└── state.json
```

Minimal `SEG` anchors preserve structural references:

```markdown
# Chapter 18

<!--SEG:c18-p001-->
He looked at *Ilya* and said, "Don't do that." He had been waiting all night.

<!--SEG:c18-p002-->
Ilya did not answer.
```

A `SEG` marker is a reconstruction and validation anchor, not an independent translation request. Codex normally reads and translates the entire chapter in one context.

### Chapter-first Translation

V6 follows a chapter-first strategy.

Normal chapters remain intact rather than being proactively divided into small batches or JSON translation objects.

A chapter is split only when an actual context or output limitation makes whole-chapter translation impractical. When necessary, splitting occurs between natural paragraph boundaries and produces only a small number of large parts.

### Preview Workflow

By default, the skill first translates one substantial chapter and builds a preview EPUB:

```text
Prepare source
→ Translate first chapter
→ Save translation
→ Build preview EPUB
→ Wait for review
```

After the translation style is approved, book-specific requirements can be added to `translation_profile.md` and production translation continues automatically.

The preview step can also be explicitly skipped.

### Translation Profiles

General translation behavior belongs to the skill. Requirements specific to an individual book belong in:

```text
translation_profile.md
```

For example:

```markdown
Target: Simplified Chinese

## Book-specific rules

- Keep personal names in their original English form.
- Render Russian passages using parentheses.
- Preserve distinctions between languages in the source.
- Preserve meaningful italics.
```

This keeps the core skill general while allowing different books to use different translation strategies.

Selective terminology is stored in:

```text
terminology.json
```

For example:

```json
{
  "The Other Side": "彼岸",
  "Black Forest": "黑森林"
}
```

The terminology file is intended for recurring terms that require cross-chapter consistency, not ordinary vocabulary.

### Token Efficiency

V6 minimizes model work outside the translation itself:

* Never load the entire book into model context.
* Never reread completed chapters.
* Never store source or translated prose in JSON.
* Never create translated JSON batches.
* Never use the model to merge completed chapters.
* Never create an intermediate EPUB for HTML, TXT, or Markdown sources.
* Avoid model-based QA after every chapter.
* Do not proactively divide ordinary chapters into small batches.
* After context compaction, reload only essential state, translation rules, minimal continuity context, and the next chapter.

Under the normal production workflow, book prose should pass through the model only once.

### Final Pipeline

```text
HTML / EPUB / TXT / MD
          ↓
      prepare.py
          ↓
  chapter01.md
  chapter02.md
  chapter03.md
          ↓
       Codex
          ↓
translations/
  chapter01.md
  chapter02.md
  chapter03.md
          ↓
    build_epub.py
          ↓
      book.zh.epub
```

The design principle is deliberately minimal:

**one chapter, one translation pass, one checkpoint, then continue.**
