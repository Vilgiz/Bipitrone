import socket

class Robot:

    def __init__(self):
        self.host = '192.168.0.21'
        self.port = 48569

    def open_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        print(f"Сервер слушает на {self.host}:{self.port}")
        self.server_socket.listen(1)  # Добавлен вызов listen для установки максимального количества ожидающих соединений
        self.client_socket, client_address = self.server_socket.accept()
        print(f"Подключен клиент {client_address}")

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

    def cast_message(self, command, cX, cY, angle=None):
        self.message = f"{command};{cX};{cY}"

    def close_socket(self):
        self.client_socket.close()
        self.server_socket.close()

if __name__ == "__main__":
    robot = Robot()
    try:
        robot.open_socket()
        robot.cast_message("move;", "100;", "150;")
        robot.send_message(robot.message)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        robot.close_socket()
