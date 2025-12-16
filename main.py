from controller import load_lessons, sort_lessons, filter_by_teacher
from view import show_lessons, ask_text


def main():
    lessons = load_lessons("lessons.txt")
    lessons = sort_lessons(lessons)

    show_lessons(lessons, "Все занятия:")

    surname = ask_text("\nВведите фамилию преподавателя: ")
    if surname:
        filtered = filter_by_teacher(lessons, surname)
        show_lessons(filtered, "\nЗанятия выбранного преподавателя:")


if __name__ == "__main__":
    main()
