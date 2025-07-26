from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from conf import BUFF_SIZE, MAX_WORKERS
from concurrent.futures import ThreadPoolExecutor
import argparse
import logging
import sys

# Конфигурация логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("TCPChatServer")


def authenticate_client(client_socket: socket) -> dict:
    """
    Аутентификация клиента, запрос и получение его никнейма

    Args:
        client_socket: Сокет клиента

    Returns:
        Словарь с данными клиента: {
            'nickname': str,
            'address': tuple
        }
    """

    try:
        # Запрос ника
        client_socket.sendall(b"Enter your nickname: ")
        nickname_bytes = client_socket.recv(BUFF_SIZE).strip()

        if not nickname_bytes:
            raise ValueError("Empty nickname received")
        
        nickname = nickname_bytes.decode()
        address = client_socket.getpeername()
        
        return {
            "nickname": nickname,
            "address": address
        }
    except (ConnectionResetError, BrokenPipeError):
        logger.error("Connection lost during authentication")
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise

def handle_client_messages(source_socket: socket, target_socket: socket):
    """
    Пересылает сообщения от исходного клиента к целевому

    Args:
        source_socket: Сокет клиента отправителя
        target_socket: Сокет клиента получателя
    """

    try:
        while True:
            message_bytes = source_socket.recv(BUFF_SIZE)
            if not message_bytes:
                logger.info("Client disconnected")
                break

            try:
                target_socket.sendall(message_bytes)
            except (ConnectionResetError, BrokenPipeError):
                logger.warning("Failed to send message to companion")
                break
    except Exception as e:
        logger.error(f"Message handling error: {e}")
    finally:
        source_socket.close()
        target_socket.close()

def main():
    parser = argparse.ArgumentParser(description="TCP chat server")
    parser.add_argument("host", type=str, help="Server hostname or IP address")
    parser.add_argument("port", type=int, help="Server port number")
    args = parser.parse_args()

    HOST = args.host
    PORT = args.port

    try:
        with socket(AF_INET, SOCK_STREAM) as server_socket:
            # Настройка сокета
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen(2)

            logger.info(f"Chat server started on {HOST}:{PORT}")
            logger.info("🟢 Waiting for 2 clients to connect...")

            # Ожидание подключения двух клиентов
            client1_socket, client1_addr = server_socket.accept()
            logger.info(f"🔵 Client #1 connected from {client1_addr}")

            client2_socket, client2_addr = server_socket.accept()
            logger.info(f"🟣 Client #2 connected from {client2_addr}")

            # Аутентификация клиентов
            client1_data = authenticate_client(client1_socket)
            client2_data = authenticate_client(client2_socket)

            client1_nickname = client1_data["nickname"]
            client1_address = client1_data["address"]
            client2_nickname = client2_data["nickname"]
            client2_address = client2_data["address"]

            logger.info(f"👤 Client #1 nickname: {client1_nickname}")
            logger.info(f"👤 Client #2 nickname: {client2_nickname}")
            logger.info("💬 Chat session started")

            # Уведомление клиентов о начале чата
            client1_socket.sendall(f"Connected to {client2_nickname}".encode())
            client2_socket.sendall(f"Connected to {client2_nickname}".encode())

            # Запуск обработчиков сообщений
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                executor.submit(handle_client_messages, client1_socket, client2_socket)
                executor.submit(handle_client_messages, client2_socket, client1_socket)

                while True:
                    pass
    except KeyboardInterrupt:
        logger.info("\n🛑 Server stopped by admin")
    except Exception as e:
        logger.critical(f"⛔ Critical server error: {e}")
        sys.exit(1)

