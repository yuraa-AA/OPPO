from model import parse_lesson_line, parse_date_safe, Lesson

def load_lessons(filename: str) -> list[Lesson]:
    lessons = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                lessons.append(parse_lesson_line(line))
    return lessons


def sort_lessons(lessons: list[Lesson]) -> list[Lesson]:
    return sorted(
        lessons,
        key=lambda l: (
            parse_date_safe(l.date) is None,
            parse_date_safe(l.date)
        )
    )


def filter_by_teacher(lessons: list[Lesson], surname: str) -> list[Lesson]:
    surname = surname.lower()
    return [
        l for l in lessons
        if l.teacher and l.teacher.lower().startswith(surname)
    ]
