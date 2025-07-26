from socket import socket, AF_INET, SOCK_STREAM
from conf import BUFF_SIZE
import argparse
import logging
import sys
from concurrent.futures import ThreadPoolExecutor

# Конфиг логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("TCPChatClient")

def receive_messages(client_socket: socket):
    """
        Принимает и отображает входящие сообщения

        Args:
            client_socket: Сокет подключения к клиенту
    """
    try:
        while True:
            message_bytes = client_socket.recv(BUFF_SIZE).strip()

            if not message_bytes:
                logger.info("Server closed connection")
                break

            message = message_bytes.decode()
            
            if message:
                if message.startswith("Enter your nickname:"):
                    nickname = input("👉 Enter your nickname: ")

            if message:
                if message.startswith("Enter your nickname:"):
                    nickname = input("👉 Enter your nickname: ").strip()

                    if nickname:
                        client_socket.sendall(nickname.encode())
                else:
                    print(f"\n💬 Companion: {message}")
                    print("👉 Your message: ", end="", flush=True)
    except (ConnectionResetError, BrokenPipeError):
        logger.error("Connection to server lost")
    except Exception as e:
        logger.error(f"Message receiving error: {e}")


def send_messages(client_socket: socket):
    """
    Отправка сообщения на сервер

    Args:
        client_socket: Сокет подключения к серверу
    """
    try:
        while True:
            message = input("👉 Your message: ").strip()

            if message.lower() == "/exit":
                logger.info("Exiting chat...")
                sys.exit(0)

            if message:
                client_socket.sendall(message.encode())
    except (ConnectionResetError, BrokenPipeError):
        logger.error("Connection to server lost")
    except Exception as e:
        logger.error(f"Message sending error: {str(e)}")



def main():
    parser = argparse.ArgumentParser(description="Start server")
    parser.add_argument("host", type=str, help="Host (localhost)")
    parser.add_argument("port", type=int, help="Port (8888)")

    args = parser.parse_args()

    HOST = args.host
    PORT = args.port

    try:
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            # Подключение к серверу
            client_socket.connect((HOST, PORT))
            logger.info(f"🔌 Connected to chat server at {HOST}:{PORT}")
            logger.info("Type /exit to quit\n")

            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(receive_messages, client_socket)
                executor.submit(send_messages, client_socket)

                while True:
                    pass
    except ConnectionRefusedError:
        logger.error("❌ Server unavailable. Make sure server is running.")
    except KeyboardInterrupt:
        logger.info("\n👋 Exiting chat client")
    except Exception as e:
        logger.critical(f"⛔ Critical client error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
