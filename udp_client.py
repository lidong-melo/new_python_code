from socket import *
import _thread
import json
import platform
import time
import message

# from collections import deque

# msg_list = deque([])

   
def send_msg(udp_msg):
    try:
        json_string = json.dumps(udp_msg)
        my_udp_socket.sendall(json_string.encode())
    except:
        print('send msg error. connection disappear when send msg')


   
def thread_udp_recv():
    while 1:
        try:
            recv_data = my_udp_socket.recv(1024)
            recv_str = recv_data.decode()
            recv_msg_dict = json.loads(recv_str)
            print('recv:',recv_msg_dict)
            parse_udp_msg(recv_msg_dict)
            recv_msg_dict.clear()
            
        except:
            pass
    my_udp_socket.close()

def parse_udp_msg(msg):
    message.udp_msg.push(msg)
    message.ui_msg.push(msg)
    #print(message.udp_msg)
    

if(platform.system() == "Linux"):
    server = {'IP':'10.0.5.1', 'PORT':61101}
else:
    server = {'IP':'127.0.0.1', 'PORT':61101}

    
## create UDP socket
while 1:
    try:
        my_udp_socket = socket(AF_INET,SOCK_DGRAM)
        my_udp_socket.connect((server['IP'],server['PORT']))
        break
    except:
        time.sleep(1)
        print('wait_for_pppd_service!!!!!!')
print('connect to', server)
_thread.start_new_thread(thread_udp_recv, ())
