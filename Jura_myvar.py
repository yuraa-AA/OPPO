import re
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class Lesson:
    date: str
    time: str
    teacher: str

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

    name_match = NAME_RE.search(text)
    if name_match:
        teacher_val = name_match.group(0).strip()
    else:
        teacher_val = re.sub(r"\s+", " ", text).strip(" .-")

    return Lesson(date=date_val, time=time_val, teacher=teacher_val)

def print_lessons(lessons: list[Lesson]):
    for lesson in lessons:
        print(f"{lesson.date}\t{lesson.time}\t{lesson.teacher}")

def main():
    base_dir = Path(file).resolve().parent
    input_path = base_dir / "lessons.txt"

    lessons: list[Lesson] = []
    with input_path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            if not line.strip():
                continue
            lessons.append(parse_lesson_line(line))

    lessons.sort(key=lambda l: datetime.strptime(l.date, "%d.%m.%Y"))
    print_lessons(lessons)

    surname = input("Введите фамилию преподавателя: ").strip()
    filtered = [l for l in lessons if l.teacher.split()[0].lower() == surname.lower()]
    filtered.sort(key=lambda l: datetime.strptime(l.date, "%d.%m.%Y"))
    print("\nЗанятия выбранного преподавателя:")
    print_lessons(filtered)

    add_q = input("\nДобавить занятие? (да/нет): ").strip().lower()
    if add_q in ("да", "д", "y", "yes"):
        date_in = input("Дата (ДД.ММ.ГГГГ): ").strip()
        time_in = input("Время (ЧЧ:ММ): ").strip()
        teacher_in = input("Фамилия преподавателя: ").strip()

        with input_path.open("a", encoding="utf-8") as f:
            f.write(f"{date_in} {time_in} {teacher_in}\n")

        lessons.append(Lesson(date=date_in, time=time_in, teacher=teacher_in))
        lessons.sort(key=lambda l: datetime.strptime(l.date, "%d.%m.%Y"))

        print("\nОбновлённое расписание:")
        print_lessons(lessons)

if name == "main":
    main()