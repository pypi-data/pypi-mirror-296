import socket


class socketChat:
    def __init__(self, host: str, port: int):
        self.adress = (host, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STEAM)

    def startChat(self):
        self.server.bind(self.adress)
        
        while True:
            self.server.listen()
            client, addr = self.server.accept()
            msg = client.recv(1024).decode("utf-8")
            if msg == "stop":
                client.close()
            else:
                print(msg)
            
            client.sendall(input('Msg: ').encode("utf-8"))