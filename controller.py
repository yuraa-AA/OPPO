"""загрузка, сортировка и фильтрация занятий"""
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
        key=lambda lesson: (
            parse_date_safe(lesson.date) is None,
            parse_date_safe(lesson.date),
        ),
    )


def filter_by_teacher(lessons: list[Lesson], surname: str) -> list[Lesson]:
    surname = surname.lower()
    return [
        lesson for lesson in lessons
        if lesson.teacher and lesson.teacher.lower().startswith(surname)
    ]
