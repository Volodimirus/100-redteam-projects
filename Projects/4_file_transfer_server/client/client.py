from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import argparse
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y:%m:%d %H:%M:%S",
)
logger = logging.getLogger("FileTransferClient")

BUFFER_SIZE = 4096  # Размер буфера для передачи данных


def send_file(filename: str, host: str, port: int):
    """Отправляет файл на сервер"""

    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        file_size = os.path.getsize(filename)
        logger.info(f"Preparing to send {filename} ({file_size} bytes)")

        with socket(AF_INET, SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))

            # Проверка готовности сервера
            response = client_socket.recv(1024).decode()
            if response != "READY":
                raise ConnectionError("Server not ready")

            # Отправка имени файла
            client_socket.sendall(
                f"{os.path.basename(filename)}:FILENAME_END:".encode()
            )

            # Отправка размера файла
            client_socket.sendall(f"{file_size}:SIZE_END:".encode())

            # Ожидание подтверждения
            response = client_socket.recv(1024).decode()

            if response != "START_TRANSFER":
                raise ConnectionError("Transfer not approved")

            # Отправка содержимого файла
            sent_bytes = 0

            with open(filename, "rb") as f:
                while sent_bytes < file_size:
                    chunk = f.read(BUFFER_SIZE)

                    if not chunk:
                        break

                    client_socket.sendall(chunk)
                    sent_bytes += len(chunk)

            # Получение результата
            response = client_socket.recv(1024).decode()
            if response.startswith("SUCCESS"):
                logger.info(f"File transfer sucessful: {response.split(":")[1]}")
            else:
                raise Exception(f"Transfer failed: {response}")
    except Exception as e:
        logger.error(f"File transfer error {e}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="File transfer client")
    parser.add_argument(
        "--host", type=str, required=True, help="Server hostname or IP address"
    )
    parser.add_argument("--port", type=int, required=True, help="Server port number")
    parser.add_argument(
        "--file", type=str, required=True, help="Path to file for transfer"
    )
    args = parser.parse_args()

    send_file(args.file, args.host, args.port)


if __name__ == "__main__":
    main()
