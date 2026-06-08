---
name: course-lecture
description: >-
  Production of narration-style lectures for online courses, paired with slide decks. Supports two formats:
  non-interactive pre-recorded video (default) and interactive live online lectures (with built-in quizzes between
  blocks). Use this skill whenever the user is creating educational content — writing a narration script for a lecture,
  designing slides to accompany spoken narration, structuring a course module, or planning the iterative production of
  course materials. Triggers include phrases like "лекция", "курс", "модуль курса", "запишем лекцию", "скрипт для
  лекции", "презентация к лекции", "образовательный модуль", "narration script", "course lecture", "lecture module", or
  any request to produce structured spoken text paired with synchronized slides. Make sure to apply this skill even
  when the user doesn't explicitly name it — recognize the intent from context (work on a multi-part course, talk about
  recording a lecture, asking for slides for a course, etc.). The format (interactive vs non-interactive) must be
  confirmed with the user at the start, not assumed. Do NOT use this skill for: generic blog posts, programming
  tutorials whose primary artifact is annotated code, or single-page reference docs.
---

# Course Lecture

A 5-stage process for producing a video lecture with synchronized slides. The end product is a slide deck (`.pptx`) and
a narration script (`.docx` or `.md`) ready for voice-over recording or live online delivery. Per-stage files accumulate
in one folder per "part" of a module.

**Two formats supported, ask the user which one at the start:**

- **Non-interactive (pre-recorded video).** Default for pure narration content. Length: 28–35 минут. Разрядки строятся в
  текст как короткие истории, цитаты, мемы. Без квизов, без вопросов в зал.
- **Interactive (live online lecture).** Длительность задаётся реальным слотом занятия — обычно 90–150 минут чистого
  речитатива (без учёта орг-вопросов и перерыва). Между главами и большими блоками — **квизы** (4–7 вопросов, 5–10 минут
  на квиз), которые служат механизмом закрепления. Квизы по умолчанию частично заменяют разрядки.

**Не угадывай формат.** Всегда спрашивай при старте через AskUserQuestion. Если пользователь выбрал interactive — по
умолчанию **предлагай квизы** между главами и крупными блоками главы 4, и уточняй стиль вопросов (multiple choice / open
discussion / mix). Подробнее в разделе «Interactive format conventions» ниже.

## Why this skill exists (don't skip stages)

Recorded narration-style lectures have constraints that generic "write a script" prompts miss:

- **Timing matters and depends on format.**
    - Non-interactive video: target ≈ 30 minutes (range 28–35). At 140 wpm that's ≈ 4200 слов. Going to 45 минут теряет
      внимание; ниже 25 — материал поверхностный.
    - Interactive live: длительность определяется слотом занятия. Уточняй у пользователя «реальный слот минус
      орг-вопросы минус перерыв». 135 минут чистого речитатива — типовой кейс для трёхчасового live-занятия.
- **Format dictates pacing.** Non-interactive — нет вопросов в зал, нет квизов, разрядки строятся в текст. Interactive —
  квизы после каждой главы и после крупных блоков, 4–7 вопросов, 5–10 минут на квиз. Квизы — это не «вода», это механизм
  закрепления материала в реальном времени и точка естественной паузы.
- **Spoken voice ≠ written prose.** Sentences must be long and natural; numbers as digits; minimal lecturer hints.
- **Slides and narration co-designed.** Slides aren't decoration after the fact — they're an axis of attention, carrying
  main thoughts and acting as memory anchors.
- **Educational outcomes are explicit.** Every section maps to a learning outcome (`ОР`); every section has one
  outcome-shaped "main thought" that becomes a takeaway.

Skipping any stage produces material that's hard to record and hard to follow. The 5 stages are a debt repayment
schedule for these constraints.

## The 5 stages and their files

Each stage produces one Markdown file. The user reviews each file before moving on. Don't jump ahead — drafts written
without an approved skeleton tend to need full rewrites.

| #   | File                   | What's in it                                                                                                      |
|-----|------------------------|-------------------------------------------------------------------------------------------------------------------|
| 1   | `01-skeleton.md`       | Section structure, timecodes, 3–4 thesis points per section, discharge points                                     |
| 2   | `02-content-plan.md`   | Per section: key idea, mandatory thesis, sources (with `⚠️ FACT-CHECK`), analogies, anti-thesis, draft slide list |
| 3   | `03-script.md`         | Full narration ready to read aloud, with slide markers and `[P]` inline pauses                                    |
| 4   | `04-slides-outline.md` | Per-slide layout, content, visuals, accents — design-ready specs                                                  |
| 5   | `final/`               | `.pptx` slides, `.docx` script, optional `.docx` handout                                                          |

Plus one shared file at the part root:

- `context.md` — single source of truth for agreements (audience, tone, narrative frame, learning outcomes, timing,
  style). All decisions live here, not in chat.

## Workflow on first contact

The user will say something like "let's write part N of module X" or "make a lecture on topic Y". Steps:

1. **Read the course map first if it exists.** Look for `<course-root>/course-structure.md`. This file lists all
   sections, all submodules, and how they relate. Without it, you can't reason correctly about what comes before/after,
   what's a forward reference vs. a callback, or where Sec-hooks should point. **If the file doesn't exist — ask the
   user to provide the full course structure before doing anything else.** Don't proceed without it: a lecture written
   in isolation usually misplaces hooks (anchors a "Sec-hook" to the next submodule when it should anchor to a section
   four modules later, or pretends to be the audience's first encounter with the topic when it's actually the third).
   Также: цель раздела/модуля ≠ ОР отдельной части — модуль может обещать больше, чем покрывает одна лекция. Не ссылайся
   на соседние части, не убедившись, что они есть в карте (не анонсируй «об этом в следующей части», если такой части
   нет).
2. **Locate the part folder.** Convention: `<course-root>/<NN-section>/<NN-part-name>/`, e.g.
   `devsecops/02-introduction-basics/01-devops/`.
3. **Read `context.md` if it exists.** Confirm the agreements before drafting anything. If something's missing, propose
   additions and ask the user to confirm before editing the file.
4. **If `context.md` doesn't exist**, copy from `references/context-template.md` and run a short interview to fill it
   (see "Setup interview" below). For new parts of an existing module, copy the previous part's `context.md` and adapt
   the part-specific sections (structure, narrative frame, learning outcomes) — the rest is inherited.
5. **Once `context.md` is approved**, start stage 1 (skeleton) and proceed sequentially.

The agent doesn't pick the audience, tone, or narrative frame on its own — these are user decisions. The agent proposes
options and asks.

## Setup interview (when creating a new `context.md`)

Use the AskUserQuestion tool when available. Cover at minimum:

- **Full course structure** (this is critical): all sections, all submodules, what comes before/after the current one.
  Without this you can't reason about Sec-hooks, callbacks, what the audience already knows, or where forward references
  should point. If the course has a `course-structure.md`, read it. If not, ask the user to provide the whole list
  before any other questions. Update or create `course-structure.md` as the result.
- **Audience**: beginners / experienced engineers / managers / mixed.
- **What audience already knows by this point**: explicitly. If the audience has gone through three previous modules,
  they know the terms and pain points from those — don't reintroduce them.
- **Tone**: academic / conversational with stories / provocative / mix.
- **Sec / cross-module connections** (if the course is multi-module): which other sections does this one connect to, and
  where does each connection point — to the next submodule, to a later module, or both? (E.g. in DevSecOps course,
  Sec-hooks in module 2 typically point to module 4, not to the next submodule.)
- **Language**: Russian with anglicisms / Russian with calques / English / bilingual glossary.
- **Narrative frame**: any sustained metaphor across parts? (e.g. "tutorial boss" — gameplay arc with a falling giant).
- **Format** (**обязательный явный вопрос, не угадывай**): non-interactive video / interactive live online. От формата
  зависит структура скрипта (есть квизы или нет), хронометраж и пропорции содержательных блоков. Если пользователь
  сказал «лекция» без уточнения — спрашивай через AskUserQuestion с двумя опциями плюс пояснениями.
- **Timing target**:
    - non-interactive video — default 30 минут (range 28–35);
    - interactive live — спрашивай реальный слот: «общая длительность занятия минус орг-вопросы минус перерыв = целевые
      минуты речитатива». Не подставляй 30 минут по умолчанию.
- **Если формат interactive** — задавай ещё пару вопросов:
    - **Квизы между блоками** (по умолчанию: да). Это базовый механизм закрепления для live-формата. Если пользователь
      явно говорит «без квизов» — используй вместо них longer narrative разрядки и in-zone questions.
    - **Стиль вопросов**: multiple choice (4 варианта, голосование в чате) / open discussion (без фиксированного ответа,
      лектор разбирает) / mix. По умолчанию — multiple choice как основной плюс одна open-discussion на блок.

Don't proceed past stage 1 without these answers locked in `context.md`.

## Style and conventions (mandatory)

Full reference: `references/style-guide.md`. Highlights that affect every stage:

- **Long natural sentences in narration.** Don't fragment into 3–4-word punches — that ritmically falls apart when read
  aloud. Use natural Russian (or target-language) connective syntax.
- **Numbers as digits in narration.** "1 августа 2012", "11.7 секунд", "440 миллионов долларов" — not "первое августа
  две тысячи двенадцатого года".
- **Minimal lecturer hints.** No `[темп замедляется]` / `[тон серьёзный]`. The lecturer decides at recording time. Only
  two markers are kept inline:
    - `### Слайд X.Y — *описание*` — slide change, with a one-line description in italics on the same line.
    - `[P]` — short inline pause for emphasis. Used sparingly, only at climactic moments.
- **Empty line between paragraphs = pause.** Don't write `[Пауза]` as a separate line.
- **Bold** for words to emphasize vocally. One or two per paragraph, not whole sentences.
- **Parallel enumerations: repeat the subject in each item.** "DevOps это не должность... DevOps это не отдел... DevOps
  это не «купить инструмент»" reads better aloud than "Не должность... Не отдел... Не «купить инструмент»". Pair with a
  `[P]` per item for rhythm.
- **Idiomatic Russian, not calques.** «In a loop» → «по кругу», not «в петле»; «на Toyota» → «в Toyota». If a phrase
  reads as if translated from English — rewrite.
- **Concrete metrics with their accepted abbreviations** (Lead Time, TTM, MTTR, MTBF, uptime, change failure rate,
  deploy frequency) instead of vague "speed" or "stability". For an engineering audience these are professional
  language, not jargon.
- **Metaphors only when explanatory.** A metaphor must help comprehension (ship-with-cargo for delivery / deployment /
  release does this). Decorative metaphors («получили вторую жизнь») are noise — the lecturer adds intonation, the text
  doesn't need flowery language.
- **No unresolved forward references — but only the metaphor kind.** Don't introduce a metaphor or image in section N
  that's only explained in section N+2 — the listener gets stuck on the unexplained picture and loses the thread.
  Neutral topic announcements are fine: "the third part of the process, which we'll cover in the next section" works
  because "part of the process" is self-explanatory; "the third leg of the stool we'll discuss later" doesn't, because
  "stool" is an image not yet introduced.
- **Russian typography**: «ёлочки» for quotes, "лапки" only inside or in English; long em-dash —, not hyphen; letter ё
  always (not е).
- **Stop-words in vague claims**: avoid «является», «имеется», «считается» when the claim is fuzzy ("считается, что …"
  needs a source). In precise statements they're fine.
- **English-term gloss on first use per file.** `pipeline (конвейер сборки)`, `SAST (Static Application Security Testing
  — статический анализ исходного кода на уязвимости)`. Subsequent uses go without gloss.
- **Fact-check discipline.** Any concrete fact (date, number, name, quote) carries a source in `02-content-plan.md`. If
  the formulation is uncertain, tag with `⚠️ FACT-CHECK` and note exactly what to verify. Before recording — a dedicated
  pass over all `⚠️ FACT-CHECK` markers, hitting first sources.

## Interactive format conventions

Применяется только если на этапе setup interview пользователь выбрал **interactive live** формат.

### Где ставить квизы

- **После каждой главы** уровня 1 (главы основной структуры лекции). Это естественные точки паузы.
- **После каждого крупного блока внутри главы**, если глава длинная (например, в Nginx-лекции глава 4 разбита на блоки
  4.1, 4.2, 4.3 — после каждого блока свой квиз).
- **Не ставь** квизы внутри коротких секций (1–3 минуты) — это разрывает поток.

### Структура квиз-блока

```markdown
### Слайд КN.1 — *QUIZ-слайд, заголовок «Квиз N. Название»*

**Квиз N. Название (X минут)**

Y вопросов. Голосуйте в чате — букву варианта.

**Вопрос 1.** Текст вопроса?

- A) Вариант A.
- B) Вариант B.
- C) Вариант C.
- D) Вариант D.

(**Правильный — B.** Краткое объяснение почему — 1–2 предложения для лектора.)

**Вопрос 2.** ...
```

### Сколько вопросов в квизе

- **Глава из 15–20 минут** — 4–5 вопросов, 5–7 минут на квиз.
- **Большой блок главы 4 из 25–30 минут** — 6–7 вопросов, 8–10 минут на квиз.
- **Финальный квиз** — 4 вопроса с акцентом на главные мысли всей лекции, 5 минут.

### Что должен делать каждый вопрос

- **Закреплять конкретный тезис** из только что разобранного блока. Не общие знания, а именно то, что было сказано.
- **Иметь чёткий правильный ответ** (для multiple choice). Без двусмысленностей.
- **В неправильных вариантах** — типичные заблуждения, чтобы разбор был содержательным. Не бессмысленные дистракторы.
- **Объяснение** в скобках — 1–2 предложения, помогающие лектору быстро рассказать почему. Не зачитывается дословно.

### Анти-паттерны для квизов

- **Вопросы на запоминание имён собственных** — года релизов, точные имена авторов, номера версий. Это проверяет
  внимание, а не понимание. Исключение: ключевые факты, которые специально подчёркивались в речитативе.
- **Trick questions** с двумя правильными вариантами по разным интерпретациям. Слушатель отвечает «правильно», но
  чувствует, что его обманули.
- **«Очевидно неправильные» дистракторы** в стиле «А) сжечь сервер». Не педагогично.
- **Вопросы длиннее, чем варианты ответов** — теряется внимание ещё до выбора.

## Narrative frame (optional but powerful)

If the course has a sustained metaphor across parts, document it in `context.md` under a "Нарративная рамка модуля"
section. Recurring conventions:

- The frame works **structurally**, not by being named in the script. If you mention "tutorial boss" out loud, the
  illusion breaks. The audience should feel the rhythm, not hear the trick's name.
- The frame supplies recurring hooks (e.g., one-sentence callbacks at the end of each section) and a closing reveal in
  the final section.
- The frame doesn't replace the educational content — it amplifies retention.

## Hronometraj rule

Don't force sections into pre-allocated time slots in stage 3. If a section's content needs +30 sec — give it. If it
turned out thin — compress. Final timing is the **sum of what got dense**, not a pre-allocated grid.

## Linter

`scripts/lint.py` is a zero-dependency Markdown normalizer. Run after each save and at the end of each stage:

```bash
python3 scripts/lint.py <part-folder>/*.md
```

What it does:

- Reflows prose and list items to width 120 (proseWrap=always).
- Normalizes nested list indentation prettier-style (4 spaces per level).
- Aligns Markdown tables by column content.
- Leaves untouched: fenced code blocks, headings, horizontal rules, blockquotes, HTML blocks.
- Collapses 3+ blank lines to one. Ensures exactly one trailing `\n`.

Canonical-источник линтера — `scripts/lint.py` в этой папке skill. Не дублируй файл в корень каждого курса: дубли будут
разъезжаться. Если пользователю нужен короткий вызов из корня курса, ставим **символическую ссылку** или используем
alias / Makefile-цель, ссылающиеся на canonical. Прямой запуск: `python3 ~/.claude/skills/course-lecture/scripts/lint.py
<part-folder>/*.md`.

## What this skill is NOT

- Not for written-LMS-style lessons (1200–1500 words с квизами и tutorial-step'ами). Другой формат, другие constraints.
- Not for pure code walkthroughs where the artifact is annotated code rather than narration.
- Not for blog posts, marketing pages, or one-page explainers.

**Поддерживается** (через interactive-формат): live online лекции с квизами и точками паузы. См. раздел «Interactive
format conventions» выше.

## Reference: a complete worked example

The Knight-Capital-themed DevOps lecture (in `references/example-devops-lecture/`) is a complete reference for the style
and process: `context.md`, all 5 stage files, and the final outputs. When uncertain about voice, density, or formatting
— read its `03-script.md`.

## Stage-by-stage hints

For per-stage tactics (what good vs. mediocre work looks like at each stage, common pitfalls, what to push back on), see
`references/stage-playbook.md`.
