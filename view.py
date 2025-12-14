from model import Lesson

def show_lessons(lessons: list[Lesson], title: str = ""):
    if title:
        print(title)
    for l in lessons:
        print(f"{l.date}\t{l.time}\t{l.teacher}")


def ask_text(msg: str) -> str:
    try:
        return input(msg).strip()
    except EOFError:
        return ""
