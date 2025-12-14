from model import Lesson, parse_lesson_line

#python -m pytest -q
#для запуска

class TestModel:

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
        line = '12.09.2025 10:30'
        lesson = parse_lesson_line(line)

        assert lesson.date == "12.09.2025"
        assert lesson.time == "10:30"
        assert lesson.teacher == ""

    def test_parse_bad_line(self):
        line = 'какая-то хрень'
        lesson = parse_lesson_line(line)

        assert lesson.date == ""
        assert lesson.time == ""

    def test_lesson_creation(self):
        lesson = Lesson("12.09.2025", "10:30", "Иванов")
        assert lesson.date == "12.09.2025"
        assert lesson.time == "10:30"
        assert lesson.teacher == "Иванов"
