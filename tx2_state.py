#import param
import time
import _thread
import udp

import message

debug = [1]


class class_meeting:
    def start(self):
        print('meeting start')
    def stop(self):
        print('meeting stop')
    def pause(self):
        print('meeting pause')
    def resume(self):
        print('meeting resume')  
        
def find_app(state):
    if debug[0] == 1:
        if state == 'STOP_LOADING':
            return False
        else:
            return True
        
        
meeting = class_meeting()
udp_link = udp.class_host('127.0.0.1', 61101)

      

def sound_control(msg):
    print ('sound_control:', msg)
        



def new_tx2_state():
    state = 'READY'
    SECOND = 50
    READY_TIMEOUT = 3
    START_TIMEOUT = 10
    STOP_TIMEOUT = 10
    timeout = READY_TIMEOUT*SECOND # 3s
    while 1:
        time.sleep(0.02) #20ms

        # for debug
        msg = udp_link.peek_msg()
        if msg == 'pi_alive':
            udp_link.send_msg('tx2_alive')
            msg = udp_link.get_msg()    
        elif msg == '?':
            print('state:',state)
            msg = udp_link.get_msg()
        # for debug end        
            
            
        
                
        #error
        #log error msg
        if state == 'ERROR':
            msg = message.err_msg.pop()
            print('err_msg =', msg)
            timeout = READY_TIMEOUT*SECOND # 3s
            state = 'READY'
            print(state)
            
            
        #ready
        #wait 3s for ack, send msg to tx2
        elif state == 'READY':
            
            # timeout-=1
            # if timeout == 0:
                # udp_link.send_msg('tx2_ready')
                # timeout = READY_TIMEOUT * SECOND
                
            # 清空ui_msg 队列    
            msg = message.ui_msg.clear()
            
            msg = udp_link.get_msg()
            if msg == 'pi_ready':
                state = 'IDLE'
                udp_link.send_msg('tx2_idle')
                print(state)
            elif msg.find('error') != -1:
                state = 'ERROR'
                message.err_msg.push('error:1')
                print(state)
            
                        
        #idle
        #wait for new meeting which is triggered by tx2 or user. response to volume button and wifi state.
        elif state == 'IDLE':
            msg = udp_link.get_msg()
            if msg == 'pi_vol_up':
                sound_control('vol_up')
            elif msg == 'pi_vol_down':
                sound_control('vol_down')
            elif msg == 'pi_start_meeting':
                state = 'START_LOADING'
                meeting.start()
                timeout = START_TIMEOUT * SECOND
                print(state)
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:2')
                print(state)

                
        #start loading
        #wait 3s for ack, otherwise set to error
        elif state == 'START_LOADING':
            timeout-=1
            if timeout == 0:
                message.err_msg.push('error:3')
                state = 'ERROR'
                print(state)
            
            msg = udp_link.get_msg()
            if msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:4')
                print(state)
                
            if find_app(state) == True:
                state = 'RECORDING'
                udp_link.send_msg('tx2_recording')
                print(state)


        #recording
        #wait for pause and stop which is triggered by tx2 or user. response to volume/mute button and wifi state.
        elif state == 'RECORDING':
            if find_app(state) == False:
                state = 'IDLE'
                print(state)
                #应该做记录
                
            msg = udp_link.get_msg()
            if msg == 'pi_mute':
                sound_control('mute')
            elif msg == 'pi_unmute':
                sound_control('unmute')
            elif msg == 'pi_vol_up':
                sound_control('vol_up')
            elif msg == 'pi_vol_down':
                sound_control('vol_down')
                
            elif msg == 'pi_pause':
                state = 'PAUSE'
                meeting.pause()
                print(state)
            elif msg == 'pi_stop':
                state = 'STOP_LOADING'
                meeting.stop()
                timeout = STOP_TIMEOUT * SECOND
                print(state)
                
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:5')
                print(state)
                

        
                
                
        #pause
        #wait for resume and stop which is triggered by tx2 or user. response to volume/mute button and wifi state.
        elif state == 'PAUSE':
            msg = udp_link.get_msg()
            if msg == 'pi_mute':
                sound_control('mute')
            elif msg == 'pi_unmute':
                sound_control('unmute')
            elif msg == 'pi_vol_up':
                sound_control('vol_up')
            elif msg == 'pi_vol_down':
                sound_control('vol_down')
                
            elif msg == 'pi_resume':
                state = 'RECORDING'
                meeting.resume()
                print(state)
            elif msg == 'pi_stop':# ui click stop
                state = 'STOP_LOADING'
                meeting.stop()
                timeout = STOP_TIMEOUT * SECOND
                print(state)
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:6')
                print(state)
                
                
        #stop meeting
        #wait 3s for ack. otherwise set to error
        elif state == 'STOP_LOADING':
            # timeout-=1
            # if timeout == 0:
                # state = 'ERROR'
                # message.err_msg.push('error:7')
                # print(state)
            
            msg = udp_link.get_msg()
            # if msg.find("error") != -1:
                # state = 'ERROR'
                # message.err_msg.push('error:7')
                # print(state)
            if find_app(state) == False:
                state = 'IDLE'
                udp_link.send_msg('tx2_idle')
                print(state)
                
                

_thread.start_new_thread(new_tx2_state(),())