import socket
import threading

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print(f"server listening on {self.host} : {self.port}")
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connected to {addr[0]} : {addr[1]}")
                # data = client_socket.recv(1024).decode('utf-8')
                # print(f"recieved: {data}")
                # response = f"you sent: {data}".encode('utf-8')
                # client_socket.sendall(response)
                # client_socket.close()
                self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()

        except socket.error as e:
            print(f"connection failed {e}")

        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode("utf-8")

                if not data:
                    break

                self.broadcast(data)

        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast(self, message):
        for client_socket in self.clients:
            try:
                client_socket.sendall(message.encode("utf-8"))
            except:
                self.clients.remove(client_socket)
                client_socket.close()


if __name__ == '__main__':
    server = Server('127.0.0.1', 6543)
    server.start()