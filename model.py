"""структуры данных и функции парсинга строк"""
import re
from dataclasses import dataclass
from datetime import datetime

DATE_RE = re.compile(r"\b\d{2}\.\d{2}\.\d{4}\b")
TIME_RE = re.compile(r"\b\d{1,2}:\d{2}\b")

NAME_RE = re.compile(
    r"[А-ЯЁA-Z][а-яёa-z]+(?:\s+[А-ЯЁA-Z][а-яёa-z]+)?"
)


@dataclass
class Lesson:
    date: str
    time: str
    teacher: str


def parse_lesson_line(line: str) -> Lesson:
    """Парсит строку расписания и возвращает объект Lesson"""
    text = line.strip()

    date = DATE_RE.search(text)
    time = TIME_RE.search(text)
    name = NAME_RE.search(text)

    date_val = date.group(0) if date else ""
    time_val = time.group(0) if time else ""
    teacher_val = name.group(0) if name else ""

    return Lesson(date_val, time_val, teacher_val)


def parse_date_safe(d: str):
    """преобразует строку dd.mm.yyyy в datetime. Возвращает None при ошибке"""
    try:
        return datetime.strptime(d, "%d.%m.%Y")
    except ValueError:
        return None
