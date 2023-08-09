from client import Client
import time
from threading import Thread

c1 = Client("Sumeet")
c2 = Client("Sheetal")

def update_messages():
    msgs = []
    while True:
        time.sleep(0.1)
        new_msgs = c1.get_messages()
        msgs.extend(new_msgs)
        for msg in new_msgs:
            print(msg)
            if(msg == "{quit}"):
                break

Thread(target=update_messages).start()

c1.send_message("hello")
time.sleep(2)
c2.send_message("hello")
time.sleep(2)
c1.send_message("whats up")
time.sleep(2)
c2.send_message("nothing much")
time.sleep(2)

c1.disconnect()
c2.disconnect()