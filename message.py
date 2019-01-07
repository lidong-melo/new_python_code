from collections import deque

class class_msg:

    def __init__(self):
        self.msg_list = deque([])
        pass
    
    def push(self, msg):
        self.msg_list.append(msg)
    def pop(self):
        try:
            msg = self.msg_list.popleft()
            #print('pop msg:',msg)
        except:
            msg = 'NONE'
        return msg
    def peek(self):
        try:
            msg = self.msg_list[0]
            #print('pop msg:',msg)
        except:
            msg = 'NONE'
        return msg
    
    def clear(self):
        self.msg_list = deque([])
        
        
# udp_msg = class_msg()
ui_msg = class_msg()
err_msg = class_msg()  

        

# Raspi - UI:

# mute

# unmute

# volume_up

# volume_down

# pause

# resume

# stop_meeting

# start_meeting




# Raspi - recv UDP:

# tx2_alive

# tx2_ready

# tx2_idle

# tx2_recording

# tx2_pause

# tx2_error:10111

# wifi:-35


# Raspi - send UDP:

# pi_alive

# pi_ready

# pi_idle

# pi_vol_up

# pi_vol_down

# pi_mute

# pi_unmute

# pi_start_meeting

# pi_recording

# pi_pause

# pi_resume

# pi_stop_meeting

# pi_error:10022


