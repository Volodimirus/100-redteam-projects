"""
Функционал обработки сообщений и применения шифра.
"""

from enum import Enum
from alphabet import Alphabet, PREDEFINED_ALPHABETS


class CipherMode(Enum):
    """Режимы работы шифра."""

    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"


def normalize_message(message: str) -> str:
    """
    Нормализует сообщение для обработки:
    - Приводит к нижнему регистру
    - Удаляет начальные/конечные пробелы

    Аргументы:
        message (str): исходное сообщение

    Возвращает:
        str: форматированное сообщение
    """

    normalized = message.strip().lower()

    if not normalized:
        print("Предупреждение: получено пустое сообщение")

    return normalized


def apply_caesar_cipher(
    message: str,
    offset: int,
    mode: CipherMode,
    lang: str = "en",
    custom_alphabet: str = None,
) -> str:
    """
    Применяет шифр Цезаря к сообщению.

    Аргументы:
        message (str): текст для обработки
        offset (int): величина сдвига
        mode (CipherMode): режим (ширфование/дешифрование)
        lang (str): язык для стандартного алфавита ('en', 'ru')
        custom_alphabet (str): кастомный алфавит

    Возвращает:
        str: обработанный текст

    Исключения:
        ValueError: при некорректных параметрах
    """

    message = normalize_message(message)

    # Получение объекта алфавита
    if custom_alphabet:
        alphabet = Alphabet(custom_alphabet)
    elif lang in PREDEFINED_ALPHABETS:
        alphabet = Alphabet.get_predefined(lang)
    else:
        raise ValueError(f"Неподдерживаемый язык: {lang}")

    # Определение направления сдвига
    shift = offset if mode == CipherMode.ENCRYPT else -offset
    effective_shift = shift % alphabet.length

    result = []
    for char in message:
        # Пропуск символов не из алфавита
        if char not in alphabet.char_to_index:
            result.append(char)
            continue

        # Вычисление нового индекса
        current_idx = alphabet.char_to_index[char]
        new_idx = (current_idx + effective_shift) % alphabet.length
        result.append(alphabet.chars[new_idx])

    return "".join(result)
