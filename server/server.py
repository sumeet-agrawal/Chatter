from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# Global Constants
HOST = 'localhost'
PORT = 5500
BUFSIZ = 512
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10

# Gloal Variables
persons = []

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def broadcast(msg, name):
    """
    send new message to all clients 
    :param msg: bytes[utf8]
    :param name: string
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8")+msg)
        except Exception as e:
            print(e)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param client: socket
    :return: None
    """
    client = person.client
    
    # first message is name of client
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat", "utf8")
    broadcast(msg, "") #broadcast welcome message

    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name+": ")
                print(f"{name}: ", msg.decode("utf8"))
        except Exception as e:
            print("[EXCEPTION]", e)
            break


def wait_for_connection():
    """
    Wait for connection from new client, start new thread once connected
    :param SERVER: socket
    :return: None
    """
    while True:
        try:
            client, addr = SERVER.accept()  # accept new client connection
            person = Person(addr, client)
            persons.append(person)
            print(f"[CONNECTED] {addr} connected to server at {time.time()}")
            Thread(target = client_communication, args=(person, )).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break
    
    print("[STOPPED] Server Crashed")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # open server to listen for connections
    print("[STARTED] Waiting for connection...")
    connection = Thread(target=wait_for_connection)
    connection.start()
    connection.join()
    SERVER.close()