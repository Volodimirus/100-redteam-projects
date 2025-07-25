from socket import socket, AF_INET, SOCK_STREAM

HOST = "localhost" # Адрес сервера
PORT = 8887 # Порт сервера
BUFFER_SIZE = 1024 # Размер буфера для приема данных


def main():
    """Основная функция клиента"""
    # Создание TCP-сокета
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        try:
            # Соединение с сервером
            client_socket.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")

            # Получение сообщения от пользователя
            prompt = input("Type your message for the server: ").strip()

            # Отправка сообщения на сервер
            client_socket.sendall(prompt.encode())
            print("Message sent to server")

            # Получение подтверждения от сервера
            response = client_socket.recv(BUFFER_SIZE)
            print(f"Server response: {response.decode().strip()}")
        except ConnectionRefusedError:
            print("Error: Server is not available")
        except (ConnectionResetError, BrokenPipeError):
            print("Error: connection lost")
        except OSError as e:
            print(f"Network error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()