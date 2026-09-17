<a id="english"></a>
# E-Book Translator

A lightweight Codex skill for long-form book translation.

It translates books **chapter by chapter**, keeps model-facing text as simple as possible, and builds the completed translation into an EPUB.

**English** | [中文](#chinese)

---

## Overview

 E-Book Translator is designed for translating long-form fiction and other book-length texts with Codex while minimizing unnecessary model operations.

The core workflow is intentionally simple:

```text
HTML / EPUB / TXT / MD
        ↓
Extract chapters
        ↓
Lightweight Markdown + SEG markers
        ↓
Translate one chapter at a time
        ↓
Save translated chapters
        ↓
Build EPUB
````

The language model is used primarily for translation. File extraction, progress tracking, structural validation, and EPUB generation are handled by deterministic scripts.

## Features

* **Chapter-first translation**
  Normal chapters are translated as a whole so the model retains chapter-level context.

* **Low-overhead intermediate format**
  Book content is presented to the model as lightweight Markdown rather than raw HTML, XHTML, or JSON.

* **Minimal SEG markers**
  SEG markers preserve structural correspondence without turning paragraphs into independent translation tasks.

* **No prose-bearing JSON**
  JSON is used only for lightweight state and metadata. Source text and translations remain in Markdown.

* **Direct HTML input**
  HTML files are parsed directly. They are not converted to EPUB before translation.

* **Multiple input formats**
  Supports HTML, EPUB, TXT, and Markdown as standard inputs.

* **EPUB output**
  Completed translations are assembled into a standard EPUB.

* **Preview-first workflow**
  The first substantial chapter can be translated as a preview before the rest of the book is processed.

* **Resume support**
  Completed chapters are checkpointed so an interrupted translation can continue from the next unfinished chapter.

* **Book-specific translation profiles**
  Translation rules for a particular book can be stored separately without making the core skill increasingly complex.

* **Custom terminology**
  A small terminology file can be maintained for terms that require consistent treatment throughout the book.


## Supported Inputs

| Format     | Support | Processing                                                  |
| ---------- | ------- | ----------------------------------------------------------- |
| HTML / HTM | Yes     | Parsed directly into chapters                               |
| EPUB       | Yes     | Reads book XHTML content directly                           |
| TXT        | Yes     | Detects chapter-like headings when possible                 |
| Markdown   | Yes     | Preserves lightweight text structure                        |
| PDF        | Limited | Text-layer extraction only; OCR is not performed by default |

Regardless of the source format, translation uses the same chapter-based Markdown workflow.

## Installation

Download or clone this repository and install the `epub-translator` folder as a Codex skill.

The skill folder should contain:

```text
epub-translator/
├── SKILL.md
├── README.md
├── references/
│   ├── translation_profile.template.md
│   └── terminology.template.json
└── scripts/
    ├── prepare.py
    ├── next_chapter.py
    ├── save_translation.py
    ├── previous_context.py
    ├── approve_preview.py
    ├── build_epub.py
    ├── validate.py
    └── common.py
```

Start a new Codex session after installing or replacing the skill to avoid carrying an older translation workflow in the existing context.

## Usage

Provide Codex with a supported book file and ask it to translate the book using the skill.

For example:

```text
Use epub-translator to translate this book into Simplified Chinese.
Translate the first chapter as a preview and stop for my review.
```

The skill prepares the source into:

```text
work/
├── units/
│   ├── chapter01.md
│   ├── chapter02.md
│   └── ...
├── translations/
├── translation_profile.md
├── terminology.json
└── state.json
```

After the preview is approved, Codex can continue chapter by chapter until the book is complete.

The final EPUB is generated only after translation is complete, rather than repeatedly converting between HTML, EPUB, JSON, and Markdown during translation.

## Translation Profile

Book-specific translation requirements belong in:

```text
translation_profile.md
```

For example:

```markdown
# Translation profile

Target: Simplified Chinese

## Book-specific rules

- Keep personal names in their original English form.
- Preserve paragraph structure.
- Render Russian dialogue according to the convention defined for this book.
- Do not add translator notes unless explicitly requested.
```

This keeps special rules separate from the general-purpose skill.

## Terminology

Optional terminology can be stored in:

```text
terminology.json
```

For example:

```json
{
  "Black Sea": "黑海",
  "Federal Security Service": "联邦安全局"
}
```

The terminology file should remain selective. It is intended for terms whose translation must remain consistent, rather than ordinary vocabulary.

## Design Principle

The skill aims to keep automated book translation close to the simplest manual workflow:

```text
read one chapter
→ translate one chapter
→ save
→ continue
```

Formatting and file-management tasks are handled outside the model wherever possible.

---
<a id="chinese"></a>
# E-Book Translator

[English](#english) | **中文**

## 简介

 E-Book Translator 是一个面向 Codex 的轻量级长篇文本翻译 Skill。

它的主要目标是让自动翻译一本书的过程尽可能接近人工操作时最简单的“逐章翻译”方式，同时自动完成章节提取、进度记录、结构校验和 EPUB 生成。

核心流程为：

```text
HTML / EPUB / TXT / MD
        ↓
提取章节
        ↓
轻量 Markdown + SEG 标记
        ↓
逐章翻译
        ↓
保存译文章节
        ↓
生成 EPUB
```

大模型主要负责真正需要语言理解的翻译工作，其余格式转换和文件操作尽可能由确定性的脚本完成。

## 主要功能

* **整章优先翻译**
  正常长度的章节默认作为完整上下文交给模型翻译，以保留章节内部的语境、人物关系和叙事连续性。

* **轻量中间格式**
  模型读取的是接近纯文本的 Markdown，而不是包含大量标签的 HTML/XHTML 或 JSON。

* **轻量 SEG 标记**
  SEG 用于记录文本结构和位置，但不会把段落变成彼此独立的翻译任务。

* **正文不进入 JSON**
  JSON 只保存少量运行状态和元数据，不保存原文和译文正文。

* **HTML 直接处理**
  HTML 输入会直接提取章节，不会为了开始翻译而先转换成 EPUB。

* **支持多种输入格式**
  标准支持 HTML、EPUB、TXT 和 Markdown。

* **统一输出 EPUB**
  翻译完成后自动将各章节构建为 EPUB。

* **先试译再继续**
  默认可以先翻译第一篇有效章节作为试读，确认翻译风格和规则后再继续整本翻译。

* **支持断点续翻**
  已完成章节会被记录，中断后可以从下一篇未完成章节继续。

* **独立翻译 Profile**
  针对某一本书的特殊翻译要求保存在独立文件中，不需要不断修改通用 Skill。

* **自定义术语库**
  可以维护自己的术语文件，用于保证需要固定处理的词汇在全书中的一致性。

## 支持的输入格式

| 格式         | 支持情况 | 处理方式                    |
| ---------- | ---- | ----------------------- |
| HTML / HTM | 支持   | 直接解析并识别章节               |
| EPUB       | 支持   | 直接读取书籍中的 XHTML 内容       |
| TXT        | 支持   | 尽可能根据章节标题识别结构           |
| Markdown   | 支持   | 保留轻量文本结构                |
| PDF        | 有限支持 | 仅考虑已有文本层的 PDF，默认不执行 OCR |

无论原始文件是什么格式，进入翻译阶段后都会采用统一的章节 Markdown 工作流。

## 安装

下载或克隆本仓库，将 `epub-translator` 文件夹作为 Codex Skill 安装。

完整目录结构如下：

```text
epub-translator/
├── SKILL.md
├── README.md
├── references/
│   ├── translation_profile.template.md
│   └── terminology.template.json
└── scripts/
    ├── prepare.py
    ├── next_chapter.py
    ├── save_translation.py
    ├── previous_context.py
    ├── approve_preview.py
    ├── build_epub.py
    ├── validate.py
    └── common.py
```

如果刚刚替换过旧版本 Skill，建议新建一个 Codex Session 再开始新的翻译任务，避免当前上下文继续沿用旧版本的工作流程。

## 使用方法

向 Codex 提供需要翻译的书籍文件，并要求使用 `epub-translator`。

例如：

```text
使用 epub-translator 将这本书翻译成简体中文。
先翻译第一章作为试读，完成后停止，等我确认翻译规则。
```

Skill 会将原始文件整理为：

```text
work/
├── units/
│   ├── chapter01.md
│   ├── chapter02.md
│   └── ...
├── translations/
├── translation_profile.md
├── terminology.json
└── state.json
```

确认试译后，可以继续逐章翻译，直到整本书完成。

最终 EPUB 在翻译完成后统一生成，不需要在翻译过程中反复执行 HTML → EPUB → XHTML → Markdown 等转换。

## 翻译 Profile

针对某一本书的特殊规则写入：

```text
translation_profile.md
```

例如：

```markdown
# Translation profile

Target: Simplified Chinese

## Book-specific rules

- 人名保持英文原文。
- 保留原文段落结构。
- 俄语对白按照本书约定的方式处理。
- 除非明确要求，否则不添加译者注。
```

这样可以把“这一本书的特殊要求”和 Skill 本身的通用翻译流程分开。

换一本书时，只需要更换 Profile，而不需要修改整个 Skill。

## 自定义术语库

需要固定翻译的术语可以保存在：

```text
terminology.json
```

例如：

```json
{
  "Black Sea": "黑海",
  "Federal Security Service": "联邦安全局"
}
```

术语库不需要收录所有词汇。它主要用于保存那些需要在不同章节之间保持一致、容易产生歧义或具有特定译法的词。

## 设计原则

V6 Lite 尽量让自动翻译一本书接近最简单的人工逐章翻译：

```text
读取一章
→ 翻译一章
→ 保存
→ 下一章
```

能够由脚本完成的格式处理、文件管理和结构校验尽可能不交给大模型处理，从而让模型上下文主要用于真正的翻译工作。

