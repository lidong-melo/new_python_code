#coding:utf-8
import platform
from socket import *
import _thread
import json
import time
from collections import deque


address_list = ['10.0.5.2', 10000]

msg_list = deque([])

def tx2_udp_send(msg_dict):
    json_string = json.dumps(msg_dict)
    address_tuple = tuple(address_list)
    try:
        s.sendto(json_string.encode(), address_tuple)
        print('send', address_tuple, json_string)
    except:
        print(address_tuple)
        print('disconnect')  
        
def thread_udp_recv():
    while 1:
        try:
            recv_data,address_recv = s.recvfrom(1024)
            
            # update client ip -->
            address_list.clear()
            address_list_temp = list(address_recv)
            address_list.append(address_list_temp[0])
            address_list.append(address_list_temp[1])
            #print('recv',address_list,recv_data)
            # <-- update client ip
            
            # parse recv msg
            recv_str = recv_data.decode()
            recv_msg_dict = json.loads(recv_str)
            parse_udp_msg(recv_msg_dict)
            recv_msg_dict.clear()
        except:
            pass
    my_udp_socket.close()


def parse_udp_msg(msg):
    msg_list.append(msg)
    pass
            
    
#udp inits
if platform.node().find('DESKTOP') != -1:
    server = {'IP':'127.0.0.1', 'PORT':61101}
else:
    server = {'IP':'10.0.5.1', 'PORT':61101}
print(server)
    
    
#udp init
while 1:
    try:
        s = socket(AF_INET,SOCK_DGRAM)  
        s.bind((server['IP'], server['PORT']))
        print('setup host ok!')
        break
    except:
        time.sleep(1)
        print('wait_for_pppd_service!!!!!!')
        
        
_thread.start_new_thread(thread_udp_recv, ())    
