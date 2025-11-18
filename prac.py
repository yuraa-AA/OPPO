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