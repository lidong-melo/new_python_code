#import param
import time
import _thread
import udp_host

import message



# udp_msg = message.udp_msg()
# ui_msg = message.ui_msg()
# err_msg = message.err_msg()  
        
    
def send_udp_msg(msg):
    udp_client.send_msg(msg)
    print ('send_udp_msg:', msg)
    
def update_ui(msg):
    print ('update ui:', msg)
    
    



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
        msg = message.udp_msg.peek()
        if msg == 'tx2_alive':
            send_udp_msg('pi_alive')
            msg = message.udp_msg.pop()    
        elif msg == '?':
            print('state:',state)
            msg = message.udp_msg.pop()
        # for debug end
            
        #ready
        #wait 3s for ack, send msg to pi
        if state == 'READY':
            
            timeout-=1
            if timeout == 0:
                send_udp_msg('tx2_ready')
                timeout = READY_TIMEOUT * SECOND
            msg = message.ui_msg.pop()
            msg = message.udp_msg.pop()
            if msg == 'pi_ready':
                state = 'IDLE'
                send_udp_msg('tx2_idle')
                print(state)
            elif msg.find('error') != -1:
                state = 'ERROR'
                message.err_msg.push('error:1')
                print(state)
        
        #error
        #log error msg
        elif state == 'ERROR':
            while 1:
                msg = message.err_msg.pop()
                if msg != 'NONE':
                    print('err_msg =', msg)
                else:
                    break
            state = 'READY'    
            print(state)
            
            
                
            
        #idle
        #wait for new meeting which is triggered by tx2 or user. response to volume button and wifi state.
        elif state == 'IDLE':
            msg = message.ui_msg.pop()
            if msg == 'volume_up':
                send_udp_msg('pi_vol_up')
                update_ui('set_to_vol_up')
            elif msg == 'volume_down':
                send_udp_msg('pi_vol_down')
                update_ui('set_to_vol_down')
            elif msg == 'wifi':
                update_ui('set_to_wifi')
            elif msg == 'start_meeting':
                state = 'START_LOADING'
                send_udp_msg('pi_start_meeting')
                update_ui('set_to_start_loading')
                timeout = START_TIMEOUT * SECOND # 3s
                print(state)

            # tx2端启动会议，应该直接进入recording模式
            msg = message.udp_msg.pop()
            if msg == 'tx2_recording': # tx2 ack ok
                state = 'RECORDING'
                send_udp_msg('pi_recording')
                update_ui('set_to_recording')
                print(state)
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:2')
                print(state)

        #start loading
        #wait 3s for ack, otherwise set to error
        elif state == 'START_LOADING':
            timeout-=1
            if timeout == 0: # 3s timeout
                message.err_msg.push('error:3')
                state = 'ERROR'
                print(state)
            msg = message.ui_msg.pop()
            
            msg = message.udp_msg.pop()
            if msg == 'tx2_recording': # tx2 ack ok
                state = 'RECORDING'
                send_udp_msg('pi_recording')
                update_ui('set_to_recording')
                print(state)
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:4')
                print(state)

        #recording
        #wait for pause and stop which is triggered by tx2 or user. response to volume/mute button and wifi state.
        elif state == 'RECORDING':
            msg = message.ui_msg.pop()
            if msg == 'mute':
                send_udp_msg('pi_mute')
                update_ui('set_to_mute')
            elif msg == 'unmute':
                send_udp_msg('pi_unmute')
                update_ui('set_to_unmute')
            elif msg == 'volume_up':
                send_udp_msg('pi_vol_up')
                update_ui('set_to_vol_up')
            elif msg == 'volume_down':
                send_udp_msg('pi_vol_down')
                update_ui('set_to_vol_down')
            elif msg == 'wifi':
                update_ui('set_to_wifi')
                
            elif msg == 'pause':
                state = 'PAUSE'
                update_ui('set_to_pause')
                send_udp_msg('pi_pause')
                print(state)
            elif msg == 'stop_meeting': #ui click stop
                state = 'STOP_LOADING'
                update_ui('set_to_stop_meeting')
                send_udp_msg('pi_stop')
                timeout = STOP_TIMEOUT * SECOND
                print(state)
            
            msg = message.udp_msg.pop()
            if  msg == 'tx2_stop_meeting': # tx2 stop meeting
                state = 'STOP_LOADING'
                update_ui('set_to_stop_meeting')
                send_udp_msg('pi_stop')
                timeout = STOP_TIMEOUT * SECOND
                print(state)
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:5')
                print(state)
        
                
                
        #pause
        #wait for resume and stop which is triggered by tx2 or user. response to volume/mute button and wifi state.
        elif state == 'PAUSE':
            msg = message.ui_msg.pop()
            if msg == 'mute':
                update_ui('set_to_mute')
                send_udp_msg('pi_mute')
            elif msg == 'unmute':
                update_ui('set_to_unmute')
                send_udp_msg('pi_unmute')
            elif msg == 'volume_up':
                update_ui('set_to_vol_up')
                send_udp_msg('pi_vol_up')
            elif msg == 'volume_down':
                update_ui('set_to_vol_down')
                send_udp_msg('pi_vol_down')
            elif msg == 'wifi':
                update_ui('set_to_wifi')
                
            elif msg == 'resume':
                state = 'RECORDING'
                update_ui('set_to_resume')
                send_udp_msg('pi_resume')
                print(state)
            elif msg == 'stop_meeting':# ui click stop
                state = 'STOP_LOADING'
                update_ui('set_to_stop_meeting')
                send_udp_msg('pi_stop')
                timeout = STOP_TIMEOUT * SECOND
                print(state)
            
            msg = message.udp_msg.pop() 
            if msg == 'tx2_stop_meeting': # tx2 stop meeting
                state = 'STOP_LOADING'
                update_ui('set_to_stop_meeting')
                send_udp_msg('pi_stop')
                timeout = STOP_TIMEOUT * SECOND
                print(state)
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:6')
                print(state)
                
                
        #stop meeting
        #wait 3s for ack. otherwise set to error
        elif state == 'STOP_LOADING':
            timeout-=1
            if timeout == 0:
                state = 'ERROR'
                message.err_msg.push('error:7')
                print(state)
                
            msg = message.ui_msg.pop()
            msg = message.udp_msg.pop()
            if msg == 'tx2_idle':
                state = 'IDLE'
                update_ui('set_to_idle')
                send_udp_msg('pi_idle')
                print(state)
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:7')
                print(state)

                
                

_thread.start_new_thread(new_tx2_state(),())