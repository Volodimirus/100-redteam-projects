from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import argparse
import logging
import os
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y:%m:%d %H:%M:%S",
)
logger = logging.getLogger("FileTransferServer")

BUFFER_SIZE = 4096  # Размер буфера для передачи данных
MAX_FILENAME_LENGTH = 255  # Максимальная длина имени файла
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB максимальный размер файла


def recv_until(socket: socket, delimiter: str) -> bytes:
    """Получает данные из сокета до встречи разделителя"""
    data = b""

    while True:
        chunk = socket.recv(1)

        if not chunk:
            raise ConnectionError("Connection closed prematurely")

        data += chunk

        if data.endswith(delimiter):
            return data[: -len(delimiter)]


def handle_client(client_socket: socket, client_addr: tuple):
    """Обрабатывает подключение одного клиента"""

    try:
        logger.info(f"Client {client_addr} connected")
        client_socket.sendall(b"READY")  # Готовность принять файл

        # Получение имени файла
        try:
            filename = recv_until(client_socket, b":FILENAME_END:").decode()
            if not filename or len(filename) > MAX_FILENAME_LENGTH:
                raise ValueError("Invalid filename")
        except Exception as e:
            logger.error(f"Filename error: {e}")
            client_socket.sendall(b"ERROR: Invalid filename format")
            return

        # Получение размера файла
        try:
            file_size = int(recv_until(client_socket, b":SIZE_END:"))
            if file_size <= 0 or file_size > MAX_FILE_SIZE:
                raise ValueError("Invalid file size")
        except Exception as e:
            logger.error(f"Filesize error: {e}")
            client_socket.sendall(b"ERROR: Invalid file size")
            return

        # Подтверждение готовности принять файл
        client_socket.sendall(b"START_TRANSFER")

        # Получение данных файла
        received = 0
        file_data = b""

        while received < file_size:
            chunk = client_socket.recv(min(BUFFER_SIZE, file_size - received))
            if not chunk:
                raise ConnectionError("Incomplete file transfer")
            file_data += chunk
            received += len(chunk)

        # Сохранение файла
        try:
            safe_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(filename)}"

            with open(safe_filename, "wb") as f:
                f.write(file_data)

            logger.info(f"File saved as {safe_filename} ({file_size} bytes)")
            client_socket.sendall(f"SUCCESS:{safe_filename}".encode())
        except Exception as e:
            logger.error(f"File save error: {e}")
            client_socket.sendall(f"ERROR: file save failed".encode())
    except Exception as e:
        logger.exception(f"Client handling error: {e}")
        try:
            client_socket.sendall(f"ERROR: {e}".encode())
        except:
            pass
    finally:
        client_socket.close()
        logger.info(f"Client {client_addr} disconnected")


def main():
    parser = argparse.ArgumentParser(description="File transfer server")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Server hostname or IP address"
    )
    parser.add_argument("--port", type=int, default=8888, help="Server port number")
    args = parser.parse_args()

    try:
        with socket(AF_INET, SOCK_STREAM) as server_socket:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind((args.host, args.port))
            server_socket.listen(5)
            logger.info(f"Server started on {args.host}:{args.port}")

            while True:
                client_socket, client_addr = server_socket.accept()
                handle_client(client_socket, client_addr)
    except KeyboardInterrupt:
        logger.info("Server stopped by admin")
    except Exception as e:
        logger.exception(f"Server error: {e}")


if __name__ == "__main__":
    main()
