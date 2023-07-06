import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server {self.host}:{self.port}")
            threading.Thread(target=self.receive_messages).start()

            while True:
                message = input("user2")
                self.send_message(message)

        except socket.error as e:
            print(f"Connection error: {e}")

        finally:
            self.client_socket.close()

    def receive_messages(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode("utf-8")
                print(data)

        except socket.error as e:
            print(f"Error receiving messages: {e}")

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode("utf-8"))

        except socket.error as e:
            print(f"Error sending message: {e}")


if __name__ == '__main__':
    client = Client('127.0.0.1', 6543)
    client.connect()
