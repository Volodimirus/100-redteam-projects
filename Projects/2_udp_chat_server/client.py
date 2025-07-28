import argparse
from socket import socket
import logging
import sys
from socket import AF_INET, SOCK_DGRAM
from conf import BUFF_SIZE, MAX_WORKERS
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("UDPChatClient")


def receive_messages(client_socket: socket):
    """
    Принимает сообщения от сервера и выводит их

    Args:
        client_socket: Клиентский UDP сокет
    """

    try:
        while True:
            message, _ = client_socket.recvfrom(BUFF_SIZE)
            message_str = message.strip().decode()

            if message_str:
                print(f"\n💬 [Server]: {message_str}")
                print(f"👉 Your message: ", end="", flush=True)
    except OSError as e:
        logger.info(f"Connection closed: {e}")
    except Exception as e:
        logger.error(f"Error receiving messages: {e}")


def send_messages(client_socket: socket, server_addr: tuple):
    """
    Отправляет сообщения на сервер

    Args:
        client_socket: Клиентский UDP сокет
        server_addr: Адрес сервера (host, port)
    """

    try:
        # Аутентификация на сервере
        client_socket.sendto(b"CONNECT", server_addr)
        print("🔑 Sent authentication request. Waiting for confirmation...")

        while True:
            message = input("👉 Your message: ").strip()

            if not message:
                continue

            if message.lower() == "/exit":
                logger.info("Exiting chat...")
                sys.exit(0)

            try:
                client_socket.sendto(message.encode(), server_addr)
            except (ConnectionResetError, OSError):
                logger.error("Failed to send message to server")
    except KeyboardInterrupt:
        logger.info("\n👋 Exiting chat client")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error sending messages: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="UDP Chat Client")
    parser.add_argument("host", type=str, help="Server hostname or IP address")
    parser.add_argument("port", type=int, help="Server port number")
    args = parser.parse_args()

    host = args.host
    port = args.port

    try:
        # Создание UDP сокета
        with socket(AF_INET, SOCK_DGRAM) as client_socket:
            server_addr = (host, port)

            # Настройка таймаута для сокета
            client_socket.settimeout(60.0)

            # Запуск потока для приема сообщений
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                executor.submit(receive_messages, client_socket)

                logger.info(f"🔌 Connecting to chat server at {host}:{port}")
                logger.info("Type /exit to quit\n")

                # Основной цикл отправки сообщений
                send_messages(client_socket, server_addr)
    except ConnectionRefusedError:
        logger.error("❌ Server unavailable. Make sure server is running.")
    except Exception as e:
        logger.critical(f"⛔ Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
