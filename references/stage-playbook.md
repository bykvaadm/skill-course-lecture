# Per-stage playbook

What good vs. mediocre work looks like at each stage. What to push back on. Common pitfalls. Read this before drafting
each stage; it captures lessons from real production runs.

## Stage 1 — `01-skeleton.md`

### What it produces

- Full section list with timecodes and word budgets.
- 3–4 thesis points per section (one line each).
- Per-section discharge plan (story / meme / quote / cycle of attention).
- Optional: narrative-frame hooks and Sec-hooks per section.

### What good looks like

- The skeleton fits the timing target (default 28–35 minutes, ≈4200 words).
- Every section has a clear job — no section is "filler" or "context for context".
- Discharges are spaced 5–7 minutes apart. The audience needs micro-rests.
- The closing section explicitly hands off to whatever comes next (next part of the module, next module).

### Common pitfalls

- **Front-loading.** First three sections taking 60% of the time, last three squashed. Distribute more evenly.
- **Missing discharges.** Pure thesis content for 30 minutes loses the audience around minute 12.
- **Sections without a takeaway.** Every section should have one main thought; if you can't formulate it on this stage,
  the section's purpose is unclear.
- **Generic openings.** "Today we'll discuss DevOps" is dead before it starts. The opening should be a hook — story,
  number, contradiction.

### Push-back signals

- Section titles longer than 5–6 words: probably trying to fit two ideas into one section.
- Word budget that exceeds 35-min target by more than 10%: cut earlier, easier than at stage 3.
- No connecting tissue between sections: the audience needs to feel the through-line.

## Stage 2 — `02-content-plan.md`

### What it produces

For each section in the skeleton:

- **Ключевая мысль** — one sentence summarizing the section's main idea.
- **Обязательные тезисы** — bullet list of points that must appear in the narration.
- **Источники** — with `⚠️ FACT-CHECK` markers for uncertain claims.
- **Аналогии и метафоры** — choose 1–2 dominant ones; flag the runners-up.
- **Анти-тезисы** — what NOT to say (saves redrafts in stage 3).
- **Черновик слайдов** — list of slides with one-line description each.

### What good looks like

- The content plan can be skim-read in 10 minutes and the reader understands the entire lecture's content.
- Every concrete claim has a source. `⚠️ FACT-CHECK` markers are explicit.
- Анти-тезисы catch the formulations that the user has previously rejected ("not пафосно", "no proselytizing", etc.).
- Slide drafts are paired with content — main thought slides, hook slides, discharge slides are all already planned.

### Common pitfalls

- **Skipping anti-thesis section.** Saves time at stage 2, costs 3× at stage 3 when the user rejects formulations.
- **Vague sources.** "By many studies" with no citation. Either find a citation or rephrase the claim.
- **No simplification flags.** When you cut nuance for lecture format, mark it. Hidden simplifications come back to bite
  during fact-check.
- **Slides as decoration.** Slides should carry the main thought, the hook, the visual anchor. Not decorative wallpaper.

### Push-back signals

- A section without a main-thought sentence: the section's purpose is unclear; rewrite the skeleton entry first.
- More than 6 mandatory thesis points per section: probably bloated; the audience won't retain.
- Anti-thesis section is empty: either the writer is the audience (rare) or the writer hasn't internalized the
  audience's pain points.

### Структура антипаттерн-карточки

Когда секция содержит антипаттерн (типичная ошибка внедрения, «как не надо делать»), оформляй его в `02-content-plan.md`
четырёхслойной карточкой:

1. **Образ / маркер.** Короткая запоминающаяся формулировка-якорь. «Обмазаться DevOps-инструментарием». «Купить тулсет».
   «Переехать в облако = стать DevOps».
2. **Описание соблазна.** Почему люди в это попадают — обычно потому что это **единственное**, что можно сделать
   решением сверху. «Нанять консультанта, выписать ордер, поставить — и отрапортовать».
3. **Последствие.** Что получают вместо обещанного. «Дорогой carcass без эффекта: технология стоит, под капотом всё то
   же самое — каждая команда деплоит по-своему, релиз ручной по пятницам, продакшен лежит без плана восстановления».
4. **Переформулировка.** Чем это **на самом деле** является. «Это не плохое облако и не плохой Kubernetes — это попытка
   решить организационную проблему технической закупкой».

Четыре слоя дают слушателю полный круг: что → почему → что вышло → как правильно думать. Без любого слоя карточка
проседает: без образа не запоминается, без описания соблазна звучит как поучение, без последствия абстрактна, без
переформулировки слушатель уходит с «не делай так», но не понимает почему.

## Stage 3 — `03-script.md`

### What it produces

The full narration ready for voice-over. Each section opens with `## Секция N — Название`, contains slide markers `###
Слайд X.Y — *описание*`, and is written as natural spoken prose with `[P]` inline pauses where the speaker should hold
for emphasis.

### What good looks like

- Reads cleanly aloud on first try. No "wait, how does this sentence end".
- Numbers as digits. Foreign terms italicized on first use only.
- Bold sparingly — one or two emphasized words per paragraph at most.
- Slide changes feel natural in the flow, not abrupt.
- Main-thought beats land — the slide is up and the formulation is sharp.
- Discharges feel like exhale — short, witty, returning to the topic.

### Common pitfalls

- **Fragmented sentences.** 3–4-word punches that read clipped when voiced. Reflow into natural connective syntax.
- **Over-instructed lecturer hints.** `[темп замедляется]`, `[тон ироничный]`. The lecturer decides; you provide text.
- **Pauses as separate lines.** Empty paragraph break already signals a pause. Don't write `[Пауза]` on a line of its
  own.
- **Drifting from the content plan.** The content plan got reviewed; if the script invents new claims, they bypass
  fact-check.
- **Excessive bolding.** One bold word per sentence loses all emphasis. Pick the climactic word.

### Push-back signals

- Sentences shorter than 5 words on average: too telegraphic for spoken delivery.
- More than 2 `[P]` pauses per section: overload — speaker won't honor them all.
- Slide marker without prior planning in `02-content-plan.md`: probably a script-time invention; check whether the slide
  is needed.

### Editing the user's edits

The user reviews and inserts their own changes. Common patterns to support, not undo:

- `<!-- BYKVA: ... -->` HTML comments → leave in place; they signal points the user wants to revisit.
- Inline replacements that change formulation but keep meaning → leave; they're closer to the user's voice.
- New sentences inserted by the user → leave; they're audience-targeted refinements.

If the user asks you to apply their edits (e.g. "fix this comment"), do that surgically — change only what the comment
requests.

### Замена примера / аналогии / инструмента-символа — синхронно через все артефакты

Когда лектор на вычитке просит заменить пример («не нравится мне эта аналогия», «инструмент устарел», «придумай другой
символ антипаттерна»), правка **не точечная в одном файле**. Один и тот же пример обычно живёт в:

- `01-skeleton.md` — короткий тезис («Главный антипаттерн: купить X»).
- `02-content-plan.md` — карточка антипаттерна (4 слоя) и черновик слайда.
- `03-script.md` — центральный абзац в речитативе и описание слайда в italics.
- `context.md` — главная мысль секции, если пример в неё попал.

Любая из 5–10 точек упоминания, оставшаяся со старым именем, даёт **дрейф между этапами**: слайд показывает один символ,
лектор читает про другой, content plan ссылается на третий. Это плохо ловится глазами и всплывает только на этапе 5
(финальная сборка).

**Процедура замены:**

1. `grep` по всем `.md` подмодуля — найди все вхождения старого имени и связанных формулировок.
2. Раздели на два списка:
    - **Перечисления и нейтральные упоминания** (например, «Jenkins, GitLab, Kubernetes — это технологии») — заменять
      аккуратно, проверяя, не появится ли дубль («GitLab, GitLab, Kubernetes»). Иногда лучше заменить на третий
      инструмент или вообще оставить как есть.
    - **Антипаттерн-маркеры** (например, «купить X», «X стоит, никто не пользуется», «любой X бесполезен») — заменять
      все одновременно на новый символ. Здесь дрейф вреднее всего.
3. Переформулируй центральный абзац в `03-script.md` (там обычно нужна не только замена слова, а перестройка фразы под
   новый образ).
4. Синхронизируй описание слайда в italics в `03-script.md` и карточку слайда в таблице `02-content-plan.md`.
5. Если меняется главная мысль секции — обновляй её и в `03-script.md`, и в `02-content-plan.md`, и в `context.md`.
6. Прогон линтера.

После такой замены проверяй конечный результат `grep`'ом: старое имя должно остаться только в нейтральных контекстах
(перечисления, конкретные исторические факты).

## Stage 4 — `04-slides-outline.md`

### What it produces

For each `### Слайд X.Y`:

- Layout (single-column / two-column / centered / etc.)
- Title and body content
- Visuals (icon / image / diagram / chart) with brief description
- Accents (which words are bold, what's a callout, what's color-coded)
- Notes for the designer (style / mood / brand consistency)

### What good looks like

- The deck reads as a parallel narrative to the script — open the deck, the audience can roughly follow the lecture.
- Main-thought slides are visually distinct (dark background, large text, no decorations).
- Hook / opening slide signals the lecture's tone.
- Closing slide ties to the narrative-frame closure if applicable.

### Common pitfalls

- **Walls of text.** Slides are visual anchors, not handouts. 5–8 lines of text per slide max; usually less.
- **Wrong slide count.** Too few — the script outpaces the deck. Too many — the lecturer is constantly clicking.
- **Generic stock imagery.** Photos that don't actually relate to the content. Either find specific imagery or use
  type-driven design.

### Шаблон антипаттерн-слайда: «коллаж vs список»

Для слайдов антипаттернов хорошо работает устойчивая композиция:

- **Левая половина — образный коллаж** того, что «накупили» в антипаттерн. 3–5 крупных иконок/изображений
  символов-маркеров (например: стакан смузи, табличка «BARBERSHOP», логотипы Kubernetes/облака/Copilot). Сами по себе
  они визуально лёгкие и узнаваемые.
- **Правая половина — аккуратный вертикальный список** того, чего реально не хватает — короткие пункты с галочками или
  иконками («документация», «унификация», «отказоустойчивость», «DRP»). Это серьёзная часть.
- **Между половинами — стрелка** с короткой подписью, направляющей внимание справа налево: «то, чего реально не
  хватает», «что действительно решает проблему», «без чего всё остальное бесполезно».

Композиция работает за лектора: визуальный гэг слева задаёт ритм и держит внимание, серьёзная конкретика справа
возвращает фокус на тезис. Если в речитативе соответствующий абзац построен на иронии-разрядке (см. style-guide
«Ирония-разрядка ставится в сухие места»), слайд и текст начинают работать в паре — это и есть «двойное назначение
разрядки».

Шаблон применим к большинству антипаттернов вида «X купили, а реально нужно Y»: технологическая закупка vs процессы,
hero culture vs blameless culture, security review в конце vs security gates в pipeline.

## Stage 5 — `final/*.pptx` and `final/*.docx`

### What it produces

- `*.pptx` — production-ready slide deck.
- `*-script.docx` — narration formatted for the lecturer's reading view (large text, page breaks at section boundaries,
  slide markers as headings).
- Optional: `*-handout.docx` — student handout with key takeaways and references.

### What good looks like

- `.pptx` matches `04-slides-outline.md` 1:1.
- `.docx` script reads comfortably on a tablet at arm's length.
- File names are descriptive: `01-devops-script.docx`, not `script.docx`.

### Process notes

- Use the `pptx` and `docx` skills (Anthropic-bundled) for the file generation. They handle the production-grade details
  (template adherence, font embedding, etc.).
- Render an example slide and check it before mass-producing 30 slides.

## Cross-cutting: when to push back vs. when to comply

**Push back when:**

- A request would break the format (interactive elements in a non-interactive recording).
- A claim lacks a source and is presented as fact.
- The user is committing to scope that won't fit the timing target.
- Style violations are repeated (anti-thesis from `context.md`).

**Comply when:**

- The user changes formulation for voice / personal style. They're going to read it; let them.
- The user inserts comments / edits without explanation. Trust their instinct; the lecturer hears it differently.
- The user explicitly disagrees with a convention from `context.md` for this section. Update `context.md` (so the
  agreement persists) and apply.

The user has the final say. The skill's job is to make the consequences of choices visible.
