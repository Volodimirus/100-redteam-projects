from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from concurrent.futures import ThreadPoolExecutor
import logging
import argparse
from conf import BUFF_SIZE
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("UDPChatServer")


def handle_clinet_connection(
    server_socket: socket, client_addr: tuple, message: bytes, active_clients: list
):
    """
    Обработка подключения клиента и пересылка сообщений

    Args:
        server_socket: UDP сокет сервера
        client_addr: Адрес клиента (IP, port)
        message: Полученное сообщение
        active_clients: Список активных клиентов
    """

    try:
        # Попытка подключения нового клиента
        if message.strip() == b"CONNECT":
            if client_addr not in active_clients:
                active_clients.append(client_addr)
                logger.info(f"✅ New client connected: {client_addr}")
                server_socket.sendto(b"Auth successful! You can now chat.", client_addr)
            else:
                logger.info(f"ℹ️ Client already connected: {client_addr}")
                server_socket.sendto(b"You are already connected.", client_addr)
            return

        # Если клиент не авторизован
        if client_addr not in active_clients:
            logger.warning(f"⚠️ Unauthorized access from: {client_addr}")
            server_socket.sendto(
                b"Auth required. Send 'CONNECT' to join the chat.", client_addr
            )
            return

        # Пересылка сообщения всем клиентам
        logger.info(f"📤 Forwarding message from {client_addr}")
        for addr in active_clients:
            if addr == client_addr:
                continue  # Сообщение отправителю не будет пересылаться
            try:
                server_socket.sendto(message, addr)
            except (ConnectionResetError, OSError):
                logger.warning(f"Failed to send to {addr}, removing client")
                active_clients.remove(addr)

        #  Подтверждение отправки
        server_socket.sendto(b"Message delivered", client_addr)
    except Exception as e:
        logger.error(f"Eror handling client {client_addr}: {e}")


def run_udp_server(host: str, port: int):
    """
    Запускает и управляет UDP чат сервером

    Args:
        host: Хост для прослушки
        port: Порт для прослушки
    """

    active_clients = []

    try:
        with socket(AF_INET, SOCK_DGRAM) as server_socket:
            # Настройка сокета
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind((host, port))

            logger.info(f"🚀 UDP chat server started on {host}:{port}")
            logger.info(f"🟢 Ready to accept connections. Press Ctrl+C to stop")

            try:
                while True:
                    # Получает сообщение от клиента
                    message, client_addr = server_socket.recvfrom(BUFF_SIZE)
                    logger.debug(f"Received from {client_addr}: {message[:20]}...")

                    # Обработка сообщения
                    handle_clinet_connection(
                        server_socket, client_addr, message, active_clients
                    )
            except KeyboardInterrupt:
                logger.info("\n🛑 Server shutdown requested")
    except OSError as e:
        logger.critical(f"⛔ Socket error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"⛔ Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP chat server")
    parser.add_argument("host", type=str, help="Server hostname or IP address")
    parser.add_argument("port", type=int, help="Server port number")
    args = parser.parse_args()

    host = args.host
    port = args.port

    run_udp_server(host, port)
