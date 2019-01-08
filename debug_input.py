import udp
import _thread
import message

def auto_recv(udp):
    while 1:
        time.sleep(0.1)
        msg = my_udphost.get_msg()
        if msg != 'NONE':
            print(msg)
        pass       

def main_udp():
    my_udphost = udp.class_host('127.0.0.1', 61101)

    _thread.start_new_thread(auto_recv, (my_udphost,))
    _thread.start_new_thread(input_udp, ())

def input_udp():
    while 1:
        msg= input("input msg:")
        my_udphost.send_msg(msg)
        


def main_ui():
    _thread.start_new_thread(input_ui, ())

def input_ui():
    while 1:
        msg= input("input msg:")
        message.ui_msg.push(msg)
    