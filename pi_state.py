#import param
import time
import _thread
import udp
import clock
import message
import debug_input
import shake_hand


       
                
       

debug_input.main_ui()

meeting_clock = clock.my_clock()
udp_link = udp.class_client('127.0.0.1', 61101)

myshake = shake_hand.class_shake_hand()
    
def update_ui(msg):
    print ('update ui:', msg)

            

        
    
    

        



def new_pi_state():
    state = 'READY'
    SECOND = 50
    READY_TIMEOUT = 3
    START_TIMEOUT = 10
    STOP_TIMEOUT = 10
    SHAKE_TIMEOUT = 30
    timeout = READY_TIMEOUT*SECOND # 3s
    while 1:
        time.sleep(0.02) #20ms

        # for debug
        msg = udp_link.peek_msg()
        if msg == 'tx2_alive':
            udp_link.send_msg('pi_alive')
            msg = udp_link.get_msg()    
        elif msg == '?':
            print('state:',state)
            msg = udp_link.get_msg()
        # for debug end        
            
        if myshake.check(state, udp_link) == False:
            state = 'ERROR'
            message.err_msg.push('error:shake_hand')
            print(state)
        
                
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
            
            timeout-=1
            if timeout == 0:
                udp_link.send_msg('pi_ready')
                timeout = READY_TIMEOUT * SECOND
                
            # 清空ui_msg 队列    
            msg = message.ui_msg.clear()
            
            msg = udp_link.get_msg()
            if msg == 'tx2_idle':
                state = 'IDLE'
                update_ui('set_to_idle')
                udp_link.send_msg('pi_idle')
                print(state)
            elif msg.find('error') != -1:
                state = 'ERROR'
                message.err_msg.push('error:1')
                print(state)
            
                        
        #idle
        #wait for new meeting which is triggered by tx2 or user. response to volume button and wifi state.
        elif state == 'IDLE':
            msg = message.ui_msg.pop()
            if msg == 'volume_up':
                udp_link.send_msg('pi_vol_up')
                update_ui('set_to_vol_up')
            elif msg == 'volume_down':
                udp_link.send_msg('pi_vol_down')
                update_ui('set_to_vol_down')
            elif msg == 'wifi':
                update_ui('set_to_wifi')
            elif msg == 'start_meeting':
                state = 'START_LOADING'
                udp_link.send_msg('pi_start_meeting')
                update_ui('set_to_start_loading')
                timeout = START_TIMEOUT * SECOND # 3s
                print(state)

            msg = udp_link.get_msg()
            if msg.find("error") != -1:
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
                
            # 清空ui_msg 队列        
            msg = message.ui_msg.clear()
            
            msg = udp_link.get_msg()
            if msg == 'tx2_recording': # tx2 ack ok
                state = 'RECORDING'
                udp_link.send_msg('pi_recording')
                update_ui('set_to_recording')
                meeting_clock.start()
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
                udp_link.send_msg('pi_mute')
                update_ui('set_to_mute')
            elif msg == 'unmute':
                udp_link.send_msg('pi_unmute')
                update_ui('set_to_unmute')
            elif msg == 'volume_up':
                udp_link.send_msg('pi_vol_up')
                update_ui('set_to_vol_up')
            elif msg == 'volume_down':
                udp_link.send_msg('pi_vol_down')
                update_ui('set_to_vol_down')
            elif msg == 'wifi':
                update_ui('set_to_wifi')
                
            elif msg == 'pause':
                state = 'PAUSE'
                update_ui('set_to_pause')
                udp_link.send_msg('pi_pause')
                meeting_clock.pause()
                print(state)
            elif msg == 'stop_meeting': #ui click stop
                state = 'STOP_LOADING'
                update_ui('set_to_stop_meeting')
                udp_link.send_msg('pi_stop')
                meeting_clock.stop()
                timeout = STOP_TIMEOUT * SECOND
                print(state)
            
            msg = udp_link.get_msg()
            if  msg == 'tx2_idle': # tx2 stop meeting
                state = 'IDLE'
                update_ui('set_to_idle')
                udp_link.send_msg('pi_idle')
                meeting_clock.reset()
                print(state)
                #应该做一下记录
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
                udp_link.send_msg('pi_mute')
            elif msg == 'unmute':
                update_ui('set_to_unmute')
                udp_link.send_msg('pi_unmute')
            elif msg == 'volume_up':
                update_ui('set_to_vol_up')
                udp_link.send_msg('pi_vol_up')
            elif msg == 'volume_down':
                update_ui('set_to_vol_down')
                udp_link.send_msg('pi_vol_down')
            elif msg == 'wifi':
                update_ui('set_to_wifi')
                
            elif msg == 'resume':
                state = 'RECORDING'
                update_ui('set_to_resume')
                udp_link.send_msg('pi_resume')
                meeting_clock.resume()
                print(state)
            elif msg == 'stop_meeting':# ui click stop
                state = 'STOP_LOADING'
                update_ui('set_to_stop_meeting')
                udp_link.send_msg('pi_stop')
                meeting_clock.stop()
                timeout = STOP_TIMEOUT * SECOND
                print(state)
            
            msg = udp_link.get_msg()
            if  msg == 'tx2_idle': # tx2 stop meeting
                state = 'IDLE'
                update_ui('set_to_idle')
                udp_link.send_msg('pi_idle')
                meeting_clock.reset()
                print(state)
                #应该做一下记录
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
            
            # 清空ui_msg 队列                
            msg = message.ui_msg.clear()         
            msg = udp_link.get_msg()
            if msg == 'tx2_idle':
                state = 'IDLE'
                update_ui('set_to_idle')
                udp_link.send_msg('pi_idle')
                meeting_clock.reset()
                print(state)
            elif msg.find("error") != -1:
                state = 'ERROR'
                message.err_msg.push('error:7')
                print(state)

                
                

_thread.start_new_thread(new_pi_state(),())