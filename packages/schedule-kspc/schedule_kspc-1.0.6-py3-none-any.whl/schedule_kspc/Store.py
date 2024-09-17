import enum


class Parser(enum.Enum):
    COLUMN = 0
    ROW = 1
    VALUE = 2


class Lesson(enum.Enum):
    LESSON_NAME = 0
    TEACHER = 1
    CABINET = 2
    GROUP = 3


WEEKDAYS: tuple = (
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
)

LESSONS: tuple = (
    '1 Пара',
    '2 Пара',
    '3 Пара',
    '4 Пара',
    '5 Пара',
    '6 Пара',
    '7 Пара',
    '8 Пара',
    '9 Пара',
    '10 Пара',
)

# Site urls
URL: dict = {
    'site': 'https://kg-college.ru/studentam/raspisanie/',
    'file': 'https://kg-college.ru/files/studentam/raspisanie/',
}

# Pattern find all
URL_FILE_PATTERN: str = r'\/files\/studentam\/raspisanie\/' \
                    r'((schedule(\d+)\.xlsx)\?(\d{2}\.\d{2}\.\d{2})-(\d{2}\.\d{2}\.\d{4}))'

DATETIME_PATTERN: str = '%d.%m.%Y_%H.%M.%S'
