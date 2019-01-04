from socket import *
import _thread
import json
import platform
import time
import message



class class_client:
    def __init__(self, ip, port):
        self.connection = False
        self.recv_msg = message.class_msg()
        
        while 1:
            try:
                self.socket = socket(AF_INET,SOCK_DGRAM)
                self.socket.connect((ip,port))
                self.connection = True
                #print('connection ok!')
                _thread.start_new_thread(thread_client_recv, (self,))
                
                break
            except:
                time.sleep(1)
                print('wait_for_pppd_service!!!!!!')
        
    def send_msg(self, udp_msg):
        try:
            json_string = json.dumps(udp_msg)
            self.socket.sendall(json_string.encode())
            print('send msg:',json_string)
        except:
            print('send msg error. connection disappear when send msg')
    
    def get_msg(self):
        msg = self.recv_msg.pop()
        return msg
        
    def peek_msg(self):
        msg = self.recv_msg.peek()
        return msg
        
    def __del__(self):
        self.connection = False
        self.socket.close()

            
def thread_client_recv(insta):
    print('wait for msg...')
    while insta.connection == True:
        try:
            recv_data = insta.socket.recv(1024)
            recv_str = recv_data.decode()
            recv_msg_dict = json.loads(recv_str)
            #print('recv:', recv_msg_dict)
            insta.recv_msg.push(recv_msg_dict)
            message.ui_msg.push(recv_msg_dict)# only for debug           
            recv_msg_dict.clear()
            
        except:
            time.sleep(0.1)
            print('wait_for_host...')

            
# def thread_host_recv(insta):
    # while insta.connection == True:
        # try:
            # print('recv...')
            # # update client ip -->
            # recv_data,address_recv = insta.socket.recvfrom(1024)
            # insta.client_list.clear()
            # client_list_temp = list(address_recv)
            # insta.client_list.append(client_list_temp[0])
            # insta.client_list.append(client_list_temp[1])
            # print('recv',insta.client_list,recv_data)
            # # <-- update client ip
            
            
            # recv_str = recv_data.decode()
            # recv_msg_dict = json.loads(recv_str)
            # insta.recv_msg.push(recv_msg_dict)
            # recv_msg_dict.clear()
            
        # except:
            # pass

            
            
#for client test
# myudp = client('127.0.0.1', 61101)
# myudp.send_msg('hi')
# while 1:
    # msg = myudp.get_msg()
    # if msg != 'NONE':
        # print(msg)
    # pass
