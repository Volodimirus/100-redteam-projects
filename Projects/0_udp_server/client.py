from socket import socket, AF_INET, SOCK_DGRAM
from conf import HOST, PORT, BUFFER_SIZE
import sys


def main():
    """Основная функция UDP-клиента"""
    try:
        # Создание UDP-сокета
        with socket(AF_INET, SOCK_DGRAM) as client_socket:
            print(f"UDP client connected to {HOST}:{PORT}")
            print("Type 'exit' to quit\n")

            while True:
                try:
                    # Получение ввода пользователя
                    message = input("Enter message to send: ").strip()

                    # Проверка на выход

                    if message.lower() == "exit":
                        print("\nClosing connection...")
                        break

                    # Отправка сообщения на сервер
                    client_socket.sendto(message.encode(), (HOST, PORT))
                    print(f"✓ Sent: {message}")

                    # Получение ответа от сервера
                    response, _ = client_socket.recvfrom(BUFFER_SIZE)
                    print(f"✓ Server response: {response.decode().strip()}\n")
                except KeyboardInterrupt:
                    print("\nOpeartion cancelled by user")
                    break
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    continue
    except Exception as e:
        print(f"⛔ Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
