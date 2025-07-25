from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
import logging
from conf import HOST, PORT, BUFFER_SIZE

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("UDPServer")


def run_udp_server():
    """Запуск и управление UDP-сервером"""
    try:
        # Создаем и настраиваем UDP-сокет
        with socket(AF_INET, SOCK_DGRAM) as server_socket:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))

            logger.info(f"🚀 UDP Server started on {HOST}:{PORT}")
            logger.info(f"🟢 Ready to receive messages. Press Ctrl+C to stop\n")

            try:
                while True:
                    try:
                        # Прием сообщения от клиента
                        data, addr = server_socket.recvfrom(BUFFER_SIZE)
                        client_ip = addr[0]

                        # Decode и логирование сообщения
                        message = data.decode().strip()
                        logger.info(f"📥 Received from {client_ip}: {message}")

                        # Отправка подтверждения
                        ack_msg = (
                            f"Message '{message[:20]}...' received!"
                            if len(message) > 20
                            else f"Message received!"
                        )
                        server_socket.sendto(ack_msg.encode(), addr)
                    except UnicodeDecodeError:
                        logger.warning(f"⚠️ Invalid encoding from {client_ip}")
                    except Exception as e:
                        logger.error(f"❌ Processing error: {e}")
            except KeyboardInterrupt:
                logger.info("\n🛑 Server shutdown requested")
    except OSError as e:
        logger.critical(f"⛔ Socket error: {e}")
    except Exception as e:
        logger.critical(f"⛔ Critical error: {e}")


if __name__ == "__main__":
    run_udp_server()
