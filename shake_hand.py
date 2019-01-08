
class class_shake_hand:
    def __init__(self):
        SECOND = 50
        self.send_period = SECOND
        self.send_count = 0
        self.noshake_timeout= 5 * SECOND # no shakehand
        self.noshake_count = 0
        self.wrongstate_timeout = 5 * SECOND # wrong state
        self.wrongstate_count = 0
        
    def check(self, state, link):        
        self.send_count += 1
        if self.send_count == self.send_period:
            self.send_count = 0 # period = 1s
            temp = 'shake_hand:' + state
            msg = link.send_msg(temp)
            
        msg = link.peek_msg()
        # if msg != 'NONE':
            # print('print for shake hand:', msg)
        if msg.find('shake_hand:') == -1: # not a shake_hand
            self.noshake_count += 1
            if self.noshake_count > self.noshake_timeout: # no shake_hand within N1 seconds
                self.noshake_count = 0
                print('no shake_hand 5s')
                return False
            else:
                return True
        else: # is a shake_hand, then check state
            self.noshake_count = 0
            temp = msg[20:]
            if temp != state:
                self.wrongstate_count += 1
                if self.wrongstate_count > self.wrongstate_timeout:  # shake hand but wrong state >N2
                    self.wrongstate_count = 0
                    print('wrong state 5s')
                    return False
                else:
                    return True
            else:
                self.wrongstate_count = 0
                return True 