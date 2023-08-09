from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock

class Client:

    # Global Constants
    HOST = "localhost"
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name) -> None:
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()

        self.send_message(name)
        self.lock = Lock()

    def receive_message(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[Exception]", e)
                break
    
    def send_message(self, msg):
        """
        Send messages to server
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
        

    
    def get_messages(self) -> []:
        """
        :return list of messages
        """
        messages_copy = self.messages[:]
        
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy
    

    def disconnect(self):
        self.send_message("{quit}")