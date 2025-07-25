# UDP Client-Server Application

Простое приложение для демонстрации работы с UDP-сокетами в Python. Позволяет отправлять текстовые сообщения между клиентом и сервером.

## 🎯 Назначение

Проект демонстрирует:
- Основы работы с UDP-протоколом
- Отправку и получение датаграмм
- Обработку сетевых ошибок
- Простую интерактивную коммуникацию

## ⚙️ Требования

- Python 3.6+
- Только стандартные библиотеки Python

## 🚀 Запуск приложения

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/udp-client-server.git
cd udp-client-server
```
2. Запустите сервер (в отдельном терминале):
```bash
python server.py
```
3. Запустите клиент (в другом терминале):
```bash
python client.py
```

## 🖥️ Использование

### Клиент

1. После запуска клиента подключитесь к серверу
2. Введите текст сообщения
3. Нажмите Enter для отправки
4. Сервер подтвердит получение
5. Для выхода введите exit

### Сервер
1. Автоматически принимает сообщения от клиентов
2. Логирует все входящие сообщения
3. Отправляет подтверждения клиентам
4. Для остановки нажмите Ctrl+C

## 📂 Структура файлов
- `client.py` - UDP-клиент
- `server.py` - UDP-сервер
- `conf.py` - общие настройки

## 🔧 Особенности реализации

1. **UDP-протокол:**
    - Быстрая доставка сообщений
    - Минимальные накладные расходы
    - Отсутствие гарантий доставки
2. **Обработка ошибок:**
    - Защита от неверного кодирования
    - Обработка разрыва соединения
    - Корректное завершение при Ctrl+C
3. **Логирование:**
    - Временные метки сообщений
    - Разные уровни логирования
    - Четкая визуализация событий
4. **Безопасность ресурсов:**
    - Контекстные менеджеры для сокетов
    - Гарантированное освобождение ресурсов
    - Защита от утечек памяти

## ⚠️ Ограничения

1. Нет шифрования сообщений
2. Нет аутентификации клиентов
3. Нет гарантии доставки сообщений
4. Работа только в локальной сети

## 📝 Пример работы

### Сервер:

```text
2023-10-15 14:30:22 - INFO - 🚀 UDP Server started on localhost:8888
2023-10-15 14:30:22 - INFO - 🟢 Ready to receive messages. Press Ctrl+C to stop
2023-10-15 14:30:25 - INFO - 📥 Received from 127.0.0.1: Hello world!
```

### Клиент:

```text
UDP Client connected to localhost:8888
Type 'exit' to quit

Enter message to send: Hello world!
✓ Sent: Hello world!
✓ Server response: Message received!
```
📜 Лицензия
MIT License