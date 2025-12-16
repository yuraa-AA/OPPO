"""вывод занятий и ввод текста пользователем"""
from model import Lesson


def show_lessons(lessons: list[Lesson], title: str = ""):
    if title:
        print(title)
    for lesson in lessons:
        print(f"{lesson.date}\t{lesson.time}\t{lesson.teacher}")


def ask_text(msg: str) -> str:
    try:
        return input(msg).strip()
    except EOFError:
        return ""
