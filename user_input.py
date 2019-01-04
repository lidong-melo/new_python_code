import udp
import _thread


def auto_recv(udp):
    while 1:
        msg = myhost.get_msg()
        if msg != 'NONE':
            print(msg)
        pass       

myhost = udp.class_host('127.0.0.1', 61101)

_thread.start_new_thread(auto_recv, (myhost,))



while 1:
    msg= input("input msg:")
    myhost.send_msg(msg)
    

    
