import re
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class Lesson:
    date: str
    time: str
    teacher: str

# Дата/время
DATE_RE = re.compile(r"\b\d{2}\.\d{2}\.\d{4}\b")
TIME_RE = re.compile(r"\b\d{1,2}:\d{2}\b")

NAME_RE = re.compile(
    r"""
    (?P<fam>[А-ЯЁA-Z][а-яёa-z]+(?:-[А-ЯЁA-Z][а-яёa-z]+)?)
    (?:\s+
        (?:
            (?P<name>[А-ЯЁA-Z][а-яёa-z]+)
            (?:\s+(?P<patr>[А-ЯЁA-Z][а-яёa-z]+))?
          |
            (?P<i1>[А-ЯЁA-Z])\.\s*(?P<i2>[А-ЯЁA-Z])\.
        )
    )?
    """,
    re.VERBOSE,
)


def parse_lesson_line(line: str) -> Lesson:
    text = line.strip()

    date_match = DATE_RE.search(text)
    date_val = date_match.group(0) if date_match else ""
    if date_match:
        text = DATE_RE.sub("", text, count=1)

    time_match = TIME_RE.search(text)
    time_val = time_match.group(0) if time_match else ""
    if time_match:
        text = TIME_RE.sub("", text, count=1)

    # Ищем ФИО по регулярке среди оставшегося текста
    name_match = NAME_RE.search(text)
    if name_match:
        teacher_val = name_match.group(0).strip()
    else:
        # если ФИО не нашли, аккуратно очищаем хвост как fallback
        teacher_raw = re.sub(r"[,\t;]+", " ", text)
        teacher_raw = re.sub(r"\s+", " ", teacher_raw).strip()
        teacher_val = teacher_raw.strip(" .-")

    return Lesson(date=date_val, time=time_val, teacher=teacher_val)

def parse_date_safe(d: str):
    try:
        return datetime.strptime(d, "%d.%m.%Y")
    except Exception:
        return None

def print_lessons(lessons: list[Lesson]):
    for lesson in lessons:
        print(f"{lesson.date}\t{lesson.time}\t{lesson.teacher}")

def main():
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "lessons.txt"

    lessons: list[Lesson] = []
    with input_path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            if not line.strip():
                continue
            lesson = parse_lesson_line(line)
            lessons.append(lesson)

    # Сортировка по дате (непустые даты идут по возрастанию, пустые — в конце)
    lessons.sort(key=lambda l: (parse_date_safe(l.date) is None, parse_date_safe(l.date) or datetime.max))

    # Вывод всего расписания
    print_lessons(lessons)

    # Фильтр по фамилии (интерактивно)
    try:
        surname = input("Введите фамилию преподавателя: ").strip()
    except EOFError:
        surname = ""

    if surname:
        surname_lower = surname.lower()
        filtered = [
            l for l in lessons
            if l.teacher and l.teacher.split()[0].lower() == surname_lower
        ]
        # Повторная сортировка по дате для отфильтрованного списка
        filtered.sort(key=lambda l: (parse_date_safe(l.date) is None, parse_date_safe(l.date) or datetime.max))

        print("\nЗанятия выбранного преподавателя:")
        print_lessons(filtered)
    else:
        print("\nФамилия не введена. Фильтр пропущен.")

if __name__ == "__main__":
    main()

