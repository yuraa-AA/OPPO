import pytest

from model import Lesson, parse_lesson_line, parse_date_safe
from controller import sort_lessons, filter_by_teacher

# python -m pytest -q


class TestModelParsing:

    def test_parse_correct_line(self):
        line = '12.09.2025 "Иванов" 10:30'
        lesson = parse_lesson_line(line)

        assert lesson.date == "12.09.2025"
        assert lesson.time == "10:30"
        assert "Иванов" in lesson.teacher

    def test_parse_different_order(self):
        line = '10:30 "Петров" 12.09.2025'
        lesson = parse_lesson_line(line)

        assert lesson.date == "12.09.2025"
        assert lesson.time == "10:30"
        assert "Петров" in lesson.teacher

    def test_parse_with_garbage(self):
        line = '10:30 "Иванов Иван Иванович"\\\\ 12.09.2025 \\\\ мусор'
        lesson = parse_lesson_line(line)

        assert lesson.date == "12.09.2025"
        assert lesson.time == "10:30"
        assert "Иванов" in lesson.teacher

    def test_parse_without_teacher(self):
        line = "12.09.2025 10:30"
        lesson = parse_lesson_line(line)

        assert lesson.date == "12.09.2025"
        assert lesson.time == "10:30"
        assert lesson.teacher == ""

    def test_parse_bad_line(self):
        line = "какая-то хрень"
        lesson = parse_lesson_line(line)

        assert lesson.date == ""
        assert lesson.time == ""
        assert lesson.teacher == ""

    def test_parse_empty_or_spaces_line(self):
        assert parse_lesson_line("") == Lesson("", "", "")
        assert parse_lesson_line("   \t\n") == Lesson("", "", "")

    def test_lesson_creation(self):
        lesson = Lesson("12.09.2025", "10:30", "Иванов")
        assert lesson.date == "12.09.2025"
        assert lesson.time == "10:30"
        assert lesson.teacher == "Иванов"


class TestBoundaries:

    @pytest.mark.parametrize(
        "date_str, expected_valid",
        [
            ("01.01.2025", True),
            ("31.12.1999", True),
            ("29.02.2024", True),
            ("29.02.2023", False),
            ("31.04.2025", False),
            ("00.12.2025", False),
            ("12.00.2025", False),
            ("12.13.2025", False),
            ("", False),
        ],
    )
    def test_parse_date_safe_boundaries(self, date_str, expected_valid): # граничные значения
        dt = parse_date_safe(date_str)
        assert (dt is not None) == expected_valid

    @pytest.mark.parametrize(
        "line, exp_date, exp_time",
        [
            ("01.01.2025 Иванов 0:00", "01.01.2025", "0:00"),
            ("01.01.2025 Иванов 23:59", "01.01.2025", "23:59"),
            ("01.01.2025 Иванов 24:00", "01.01.2025", "24:00"),
            ("01.01.2025 Иванов 9:5", "01.01.2025", ""),
            ("1.1.2025 Иванов 10:30", "", "10:30"),
        ],
    )
    def test_parse_lesson_line_time_date_edges(self, line, exp_date, exp_time): # граничные значения
        lesson = parse_lesson_line(line)
        assert lesson.date == exp_date
        assert lesson.time == exp_time


class TestSortingAndFiltering:

    def test_sort_lessons_by_date_only_valid_first(self): # сортировка
        lessons = [
            Lesson("12.09.2025", "10:30", "Иванов"),
            Lesson("11.09.2025", "09:00", "Петров"),
            Lesson("99.99.9999", "12:00", "BadDate"),
            Lesson("", "08:00", "NoDate"),
        ]

        res = sort_lessons(lessons)

        assert [lesson.date for lesson in res[:2]] == [
                 "11.09.2025",
                 "12.09.2025",
                ]
        assert [lesson.teacher for lesson in res[2:]] == ["BadDate", "NoDate"]

    def test_sort_is_stable_for_same_date(self): # сортировка
        lessons = [
            Lesson("12.09.2025", "12:00", "A"),
            Lesson("12.09.2025", "09:00", "B"),
            Lesson("12.09.2025", "10:00", "C"),
        ]
        res = sort_lessons(lessons)
        assert [lesson.teacher for lesson in res] == ["A", "B", "C"]

    def test_filter_by_teacher_startswith_case_insensitive(self): # фильтрация
        lessons = [
            Lesson("12.09.2025", "10:30", "Иванов"),
            Lesson("13.09.2025", "11:00", "иванович"),
            Lesson("14.09.2025", "12:00", "Петров"),
            Lesson("15.09.2025", "13:00", ""),
        ]

        res = filter_by_teacher(lessons, "ИВА")
        assert [lesson.teacher for lesson in res] == ["Иванов", "иванович"]

    def test_filter_by_teacher_empty_surname(self): # фильтрация
        lessons = [
            Lesson("12.09.2025", "10:30", "Иванов"),
            Lesson("13.09.2025", "11:00", "Петров"),
            Lesson("14.09.2025", "12:00", ""),
        ]
        res = filter_by_teacher(lessons, "")
        assert [lesson.teacher for lesson in res] == ["Иванов", "Петров"]
