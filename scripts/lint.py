#!/usr/bin/env python3
"""
Простой нормализатор Markdown.

Что делает:
- Переносит длинные строки прозы под ширину 120 (proseWrap=always).
- В маркированных и нумерованных списках корректно обрабатывает многострочные пункты:
  continuation-строки получают отступ, равный длине маркера + 1 пробел.
- Нормализует отступы вложенных списков под prettier-стиль: каждый уровень вложенности
  получает отступ кратный 4 пробелам (0, 4, 8, ...). Содержимое пунктов после нормализации
  reflow-ается заново под текущий префикс.
- Выравнивает таблицы по содержимому колонок: ширина каждой колонки = максимальная
  длина ячейки в этой колонке (минимум 3 — для валидного разделителя). Разделитель —
  без пробелов вокруг тире (`|-----|`), ячейки данных — с одним пробелом по краям и
  padding-пробелами для выравнивания (`| value      |`). Поддерживается выравнивание
  через `:---`, `---:`, `:---:`.
- НЕ трогает: fenced code blocks (``` или ~~~), заголовки (#), горизонтальные
  разделители (---), HTML-блоки, blockquote-блоки.
- НЕ трогает YAML frontmatter: если файл начинается со строки `---` (точно с первой),
  всё до следующей `---` включительно проходит без изменений. Это критично для skill-файлов
  и других markdown с YAML-метаданными — иначе reflow склеит ключи в одну строку и сломает
  парсер.
- Гарантирует, что файл заканчивается ровно одним \\n.
- Схлопывает 3+ пустых строки до одной.

Использование:
    python3 lint.py <файл1.md> [<файл2.md> ...]
    python3 lint.py 02-introduction-basics/01-devops/*.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WIDTH = 120
INDENT_STEP = 4  # отступ на уровень вложенности списка (prettier-стиль)

LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
HEADER_RE = re.compile(r"^\s{0,3}#{1,6}\s")
HR_RE = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
TABLE_RE = re.compile(r"^\s*\|")
QUOTE_RE = re.compile(r"^(\s*(?:>\s?)+)(.*)$")
FENCE_RE = re.compile(r"^(\s*)(```|~~~)")
HTML_BLOCK_RE = re.compile(r"^\s*<[^>]+>\s*$")
TABLE_SEP_CELL_RE = re.compile(r"^:?-+:?$")


def reflow(text: str, prefix_first: str, prefix_rest: str, width: int = WIDTH) -> list[str]:
    """Перенос текста на строки шириной width с заданными префиксами."""
    words = text.split()
    if not words:
        return [prefix_first.rstrip()]

    lines: list[str] = []
    current = prefix_first + words[0]

    for word in words[1:]:
        candidate = current + " " + word
        if len(candidate) <= width:
            current = candidate
        else:
            lines.append(current)
            current = prefix_rest + word

    lines.append(current)
    return lines


def lint(content: str) -> str:
    """Основной линт: reflow прозы, списков, нормализация отступов вложенности."""
    lines = content.split("\n")
    out: list[str] = []
    i = 0
    in_fence = False
    fence_marker: str | None = None

    # YAML frontmatter: если файл начинается с `---` в первой строке,
    # пропускаем всё до следующей `---` включительно без изменений.
    # Это нужно для skill-файлов и другого markdown с YAML-метаданными.
    if lines and lines[0].strip() == "---":
        k = 1
        while k < len(lines) and lines[k].strip() != "---":
            k += 1
        if k < len(lines):  # нашли закрывающую `---`
            for j in range(0, k + 1):
                out.append(lines[j])
            i = k + 1

    # Стек активных уровней списка: [(orig_indent_len, level), ...]
    # Сбрасывается на любой нелистовой непустой блок (заголовок, абзац, таблица и т.п.).
    list_stack: list[tuple[int, int]] = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Fenced code blocks: pass through verbatim
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(2)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            out.append(line)
            i += 1
            list_stack.clear()
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue

        # Tables: pass through (форматируются в format_tables на пост-проходе)
        if TABLE_RE.match(line):
            out.append(line)
            i += 1
            list_stack.clear()
            continue

        # Headers, horizontal rules: pass through
        if HEADER_RE.match(line) or HR_RE.match(line):
            out.append(line)
            i += 1
            list_stack.clear()
            continue

        # HTML blocks: pass through (single line)
        if HTML_BLOCK_RE.match(line):
            out.append(line)
            i += 1
            list_stack.clear()
            continue

        # Empty line — стек НЕ сбрасываем (внутри списка пустая строка между пунктами легальна)
        if not stripped:
            out.append("")
            i += 1
            continue

        # List item — collect multi-line item, reflow content
        list_match = LIST_RE.match(line)
        if list_match:
            indent = list_match.group(1)
            marker = list_match.group(2)
            first_text = list_match.group(3)
            orig_indent_len = len(indent)

            # Определяем уровень вложенности через стек оригинальных отступов
            while list_stack and list_stack[-1][0] > orig_indent_len:
                list_stack.pop()

            if list_stack and list_stack[-1][0] == orig_indent_len:
                level = list_stack[-1][1]
            elif list_stack:
                level = list_stack[-1][1] + 1
                list_stack.append((orig_indent_len, level))
            else:
                level = 0
                list_stack.append((orig_indent_len, level))

            normalized_indent = " " * (level * INDENT_STEP)
            cont_indent = normalized_indent + " " * (len(marker) + 1)
            orig_cont_min = orig_indent_len + len(marker) + 1

            # Собираем продолжения текущего пункта (continuation-строки)
            j = i + 1
            collected = [first_text]
            while j < len(lines):
                nxt = lines[j]
                if not nxt.strip():
                    break
                if LIST_RE.match(nxt):
                    # Любой следующий list-маркер — это новый пункт (свой или вложенный),
                    # обработается в следующей итерации главного цикла
                    break
                if FENCE_RE.match(nxt) or TABLE_RE.match(nxt) or HEADER_RE.match(nxt) or HR_RE.match(nxt):
                    break
                # Continuation: отступ должен быть >= orig_cont_min
                # (или хотя бы >= orig_indent + 2 — для эвристического захвата)
                nxt_indent_len = len(nxt) - len(nxt.lstrip())
                if nxt_indent_len >= orig_cont_min or nxt_indent_len >= orig_indent_len + 2:
                    collected.append(nxt.strip())
                    j += 1
                else:
                    break

            full_text = " ".join(collected)
            prefix_first = normalized_indent + marker + " "
            prefix_rest = cont_indent
            for reflowed_line in reflow(full_text, prefix_first, prefix_rest):
                out.append(reflowed_line)
            i = j
            continue

        # Blockquote — НЕ переформатируем (внутри могут быть свои списки/абзацы)
        if QUOTE_RE.match(line):
            list_stack.clear()
            while i < len(lines) and (QUOTE_RE.match(lines[i]) or lines[i].strip().startswith(">")):
                out.append(lines[i].rstrip())
                i += 1
            continue

        # Обычный абзац — собрать все непустые подряд строки и reflow
        list_stack.clear()
        j = i
        collected = []
        while j < len(lines):
            nxt = lines[j]
            if not nxt.strip():
                break
            if (
                LIST_RE.match(nxt)
                or QUOTE_RE.match(nxt)
                or FENCE_RE.match(nxt)
                or TABLE_RE.match(nxt)
                or HEADER_RE.match(nxt)
                or HR_RE.match(nxt)
            ):
                break
            collected.append(nxt.strip())
            j += 1
        full_text = " ".join(collected)
        for reflowed_line in reflow(full_text, "", ""):
            out.append(reflowed_line)
        i = j

    # Схлопываем 3+ пустых строки до одной
    deduped: list[str] = []
    blank_run = 0
    for line in out:
        if not line.strip():
            blank_run += 1
            if blank_run <= 1:
                deduped.append("")
        else:
            blank_run = 0
            deduped.append(line.rstrip())

    # Гарантируем ровно один \n в конце
    while deduped and not deduped[-1].strip():
        deduped.pop()
    deduped.append("")

    return "\n".join(deduped)


def format_table_block(block: list[str]) -> list[str]:
    """Форматирует блок таблицы. Возвращает as-is, если блок не валидная GFM-таблица."""
    if len(block) < 2:
        return block

    def parse_row(line: str) -> list[str]:
        s = line.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        return [c.strip() for c in s.split("|")]

    rows = [parse_row(l) for l in block]

    sep_row = rows[1]
    if not sep_row or not all(TABLE_SEP_CELL_RE.match(c) for c in sep_row):
        return block

    n_cols = len(rows[0])
    for r in rows:
        while len(r) < n_cols:
            r.append("")
        del r[n_cols:]

    aligns: list[str] = []
    for cell in rows[1]:
        left = cell.startswith(":")
        right = cell.endswith(":")
        if left and right:
            aligns.append("center")
        elif right:
            aligns.append("right")
        else:
            aligns.append("left")

    # Ширина колонки = max длина текста среди header + data rows (разделитель не считаем)
    widths = [0] * n_cols
    data_rows = [rows[0]] + rows[2:]
    for r in data_rows:
        for ci, cell in enumerate(r):
            widths[ci] = max(widths[ci], len(cell))
    widths = [max(w, 3) for w in widths]  # минимум 3 — для валидного разделителя

    def fmt_cell(text: str, w: int, a: str) -> str:
        if a == "right":
            return text.rjust(w)
        if a == "center":
            pad = w - len(text)
            left = pad // 2
            right = pad - left
            return " " * left + text + " " * right
        return text.ljust(w)

    def fmt_data(row: list[str]) -> str:
        parts = [" " + fmt_cell(c, widths[ci], aligns[ci]) + " " for ci, c in enumerate(row)]
        return "|" + "|".join(parts) + "|"

    def fmt_sep() -> str:
        parts = []
        for ci, w in enumerate(widths):
            inner = w + 2  # столько же символов, сколько занимает ячейка данных между палочками
            a = aligns[ci]
            if a == "left":
                parts.append("-" * inner)
            elif a == "right":
                parts.append("-" * (inner - 1) + ":")
            else:  # center
                parts.append(":" + "-" * (inner - 2) + ":")
        return "|" + "|".join(parts) + "|"

    out = [fmt_data(rows[0]), fmt_sep()]
    for r in rows[2:]:
        out.append(fmt_data(r))
    return out


def format_tables(content: str) -> str:
    """Пост-обработка: форматирует таблицы по содержимому колонок."""
    lines = content.split("\n")
    out: list[str] = []
    i = 0
    in_fence = False
    fence_marker: str | None = None

    while i < len(lines):
        line = lines[i]

        fm = FENCE_RE.match(line)
        if fm:
            marker = fm.group(2)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue

        # Блок таблицы: 2+ подряд строк, начинающихся с |
        if line.strip().startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            block = lines[i:j]
            formatted = format_table_block(block)
            out.extend(formatted)
            i = j
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 1

    files: list[Path] = []
    for pattern in argv:
        p = Path(pattern)
        if p.is_dir():
            files.extend(p.rglob("*.md"))
        else:
            files.append(p)

    for f in files:
        if not f.exists() or not f.is_file():
            print(f"skip (not a file): {f}", file=sys.stderr)
            continue
        original = f.read_text(encoding="utf-8")
        linted = format_tables(lint(original))
        if linted != original:
            f.write_text(linted, encoding="utf-8")
            print(f"linted: {f}")
        else:
            print(f"unchanged: {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
