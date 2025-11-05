import re
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

DATE_RE = re.compile(r"\b\d{2}\.\d{2}\.\d{4}\b")
TIME_RE = re.compile(r"\b\d{1,2}:\d{2}\b")

#от " до "
NAME_RE = re.compile(r'"([^"]+)"')

#datetime
@dataclass
class Lesson:
    dt: datetime
    teacher: str


def parse_lesson_line(line: str) -> Lesson:
    text = line.strip()

    dm = DATE_RE.search(text)
    tm = TIME_RE.search(text)
    date_str = dm.group(0)
    time_str = tm.group(0)

    text = DATE_RE.sub("", text, 1)
    text = TIME_RE.sub("", text, 1)

    teacher = NAME_RE.search(text).group(1).strip()

    dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

    return Lesson(dt=dt, teacher=teacher)

def print_lessons(lessons: list[Lesson]):
    for l in lessons:
        print(f"{l.dt:%d.%m.%Y}\t{l.dt:%H:%M}\t{l.teacher}")

def main():
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "lessons.txt"

    lessons: list[Lesson] = [
        parse_lesson_line(line)
        for line in input_path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]

    lessons.sort(key=lambda l: l.dt)
    print_lessons(lessons)

    query = input("Введите фамилию/ФИО преподавателя: ").strip()
    if query:
        patt = re.compile(rf'(?i)\b{re.escape(query)}\b')
        filtered = [l for l in lessons if patt.search(l.teacher)]

        filtered.sort(key=lambda l: l.dt)

        print("\nЗанятия выбранного преподавателя:")
        print_lessons(filtered)
    else:
        print("\nФамилия не введена. Фильтр пропущен.")

if __name__ == "__main__":
    main()
