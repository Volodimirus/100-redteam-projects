"""
Дешифрование сообщений с помощью шифра Цезаря.
Использование: decrypt.py [-h] -m MESSAGE [-o OFFSET] [-l LANG] [-a ALPHABET]
"""

import argparse
from utils import apply_caesar_cipher, CipherMode


def decrypt_message(
    message: str, offset: int, lang: str = "en", custom_alphabet: str = None
) -> str:
    """
    Дешифрует сообщение шифром Цезаря.

    Аргументы:
        message (str): текст для шифрования
        offset (int): величина сдвига
        lang (str): язык стандартного алфавита
        custom_alphabet (str): пользовательский алфавит

    Возвращает:
        str: Дешифрованное сообщение
    """

    return apply_caesar_cipher(
        message=message,
        offset=offset,
        mode=CipherMode.DECRYPT,
        lang=lang,
        custom_alphabet=custom_alphabet,
    )


def main():
    """Обработка аргументов командной строки и запуск дешифрования"""

    parser = argparse.ArgumentParser(description="Дешифрование сообщения шифром Цезаря")
    parser.add_argument(
        "-o", "--offset", type=int, default=3, help="Величина сдвига (по умолчанию: 3)"
    )
    parser.add_argument(
        "-m", "--message", type=str, required=True, help="Сообщение для дешифрования"
    )
    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        default="en",
        help="Язык алфавита (en/ru, по умолчанию: en)",
    )
    parser.add_argument(
        "-a", "--alphabet", type=str, help="Пользовательский алфавит (опционально)"
    )

    args = parser.parse_args()

    decrypted_message = decrypt_message(
        message=args.message,
        offset=args.offset,
        lang=args.lang,
        custom_alphabet=args.alphabet,
    )

    print(f"Расшифрованное сообщение: {decrypted_message}")


if __name__ == "__main__":
    main()
