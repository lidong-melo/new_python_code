import datetime

class my_clock:        
    def reset(self):
        # self.start_time = time.datetime.now()
        # self.stop_time = time.datetime.now()
        # self.pause_start =  time.datetime.now()
        # self.pause_stop =  time.datetime.now()
        # self.pause_time = 0
        # print (self.start_time)
        # print (self.stop_time)
        self.pause_time = []
        print('clock reset')
        
    def start(self):
        self.start_time = datetime.datetime.now()
        self.pause_time = []
        print('clock start')
        
    def pause(self):
        self.pause_start =  datetime.datetime.now()
        print('clock pause')
        
    def resume(self):
        self.pause_stop =  datetime.datetime.now()
        self.pause_time.insert(0, self.pause_stop - self.pause_start)
        print('pause_time=',self.pause_stop,' - ',self.pause_start,' = ', self.pause_time[0])
        
        print('clock resume')
        
    def stop(self):
        self.stop_time = datetime.datetime.now()
        # calculate all pause time
        pause_total = datetime.timedelta(seconds = 0)
        for pause in self.pause_time:
            pause_total += pause
        
        self.total_time = self.stop_time - self.start_time - pause_total
        print('total_time=',self.stop_time,' - ',self.start_time,' - ',pause_total, ' = ', self.total_time)
        print('clock stop') 
        
# debug code        
# myclock = my_clock()

# msg= input("input msg:")

# myclock.start()

# msg= input("input msg:")
# myclock.pause()

# msg= input("input msg:")
# myclock.resume()

# msg= input("input msg:")
# myclock.pause()

# msg= input("input msg:")
# myclock.resume()


# msg= input("input msg:")
# myclock.stop()
