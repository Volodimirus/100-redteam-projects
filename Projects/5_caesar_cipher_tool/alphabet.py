"""
Модуль для работы с алфавитами шифрования.
Предоставляет предопределенные алфавиты и функционал для создания пользовательских.
"""

# Предопределенные алфавиты
PREDEFINED_ALPHABETS = {
    "en": "abcdefghijklmnopqrstuvwxyz",
    "ru": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
}


class Alphabet:
    """
    Класс для представления алфавита шифрования.

    Атрибуты:
        chars (str): строка символов алфавита
        length (int): количество символов в алфавите
        char_to_index (dict): словарь (символ:индекс)
    """

    def __init__(self, chars: str):
        """
        Инициализирует алфавит из строки символов.

        Аргументы:
            chars (str): строка уникальных символов алфавита.
        """

        self.chars = chars
        self.length = len(chars)
        self.char_to_index = {char: idx for idx, char in enumerate(chars)}

    @classmethod
    def get_predefined(cls, lang: str) -> "Alphabet":
        """
        Возвращает предопределенный алфавит для языка.

        Аргументы:
            lang (str): идентификатор языка ('en', 'ru')

        Возвращает:
            Alphabet: экземпляр класса алфавита

        Исключения:
            ValueError: если язык не поддерживается
        """

        if lang not in PREDEFINED_ALPHABETS:
            raise ValueError(f"Неподдерживаемый язык: {lang}")
        return cls(PREDEFINED_ALPHABETS[lang])
