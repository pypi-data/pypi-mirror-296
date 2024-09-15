import http.server as server
import socketserver as socket
import os


class httpServer:
    def __init__(self, host: str, port: int, path="./"):
        self.host = host
        self.port = port
        self.path = path
        adress = (self.host, self.port)

        os.chdir(path)


        self.handler = server.SimpleHTTPRequestHandler
        self.httpd = socket.TCPServer(adress, self.handler)

    def startServerHTTP(self):
        menu = f"""
        Le serveur est en ligne 

        info :
            host : {self.host}
            port : {self.port}
            path : {self.path}

        """

        print(menu)

        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("Serveur arrêté !")
            self.httpd.shutdown()