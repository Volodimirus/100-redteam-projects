from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from concurrent.futures import ThreadPoolExecutor
import logging
from conf import HOST, PORT, BUFFER_SIZE, MAX_WORKERS

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("TCPServer")


def client_connection_handler(client_socket: socket, client_addr):
    """
    Обрабатывает соединение с клиентом

    Args:
        client_socket: Сокет клиентского соединения
        client_addr: Адрес клиента (IP, порт)
    """
    try:
        logger.info(f"Client connected: {client_addr}")

        while True:
            # Принимаем данные от клиента
            client_data = client_socket.recv(BUFFER_SIZE)
            if not client_data:
                logger.info(f"Client {client_addr} disconnected")
                break

            # Декодируем и обрабатываем сообщение
            client_data_str = client_data.decode().strip()
            logger.info(f"Received from {client_addr}: {client_data_str}")

            # Отправляем подтверждение клиенту
            try:
                client_socket.sendall(b"Message received!\n")
            except (ConnectionResetError, BrokenPipeError):
                logger.warning(f"Send failed to {client_addr}")
                break
    except (ConnectionResetError, BrokenPipeError):
        logger.warning(f"Client {client_addr} connection reset")
    except OSError as e:
        logger.error(f"Socket error with {client_addr}: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error with {client_addr}")
    finally:
        # Гарантированное закрытие соединения
        client_socket.close()
        logger.info(f"Connection closed for {client_addr}")

def main():
    """Основная функция сервера"""
    # Создание TCP-сокета
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        try:
            # Настройка сокета
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen(MAX_WORKERS)

            logger.info(f"Server started on {HOST}:{PORT}. Waiting for connections...")

            # Настройка пула потоков для обработки соединений
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                while True:
                    try:
                        # Получение нового соединения
                        client_socket, client_addr = server_socket.accept()
                        logger.debug(f"New connection from {client_addr}")

                        # Запуск обработчика клиента в отдельном потоке
                        executor.submit(
                            client_connection_handler,
                            client_socket, client_addr
                        )
                    except OSError as e:
                        logger.error(f"Accept error: {e}")
        except KeyboardInterrupt:
            logger.info("Server stopped by administrator")
        except Exception as e:
            logger.exception("Fatal server error")

if __name__ == "__main__":
    main()
