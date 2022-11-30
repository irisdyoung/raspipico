import time
from rainbow import blinker, steady, green, violet, button#, yellow

class Timer(object):
    def __init__(self, duration_s, led_responder, trigger_reset_lambda):
        self.now = time.time()
        self.duration = int(duration_s)
        self.end = self.now + self.duration
        self.led = led_responder
        self.trigger_reset = trigger_reset_lambda # e.g. record button press
        self.led.reset()
    def update(self):
        self.now = time.time()
        if self.now >= self.end:
            self.led.respond(self.now - self.end) # this might be complex, like flashing at some frequency or fading out
            # and we're assuming this only gets to update momentarily within a loop of several other things happening
        if self.trigger_reset():
            self.reset()
    def reset(self):
        self.now = time.time()
        self.end = self.now + self.duration
        self.led.reset()
        print('Reset timer.')
        self.report_status()
    def report_status(self):
        print('Time until alarm: {}'.format(self.end - self.now))

class Timekeeper(object):
    timers = {}
    def init_timer(self, name, duration_min, led_responder, trigger_reset_lambda):
        self.timers[name] = Timer(duration_min * 60, led_responder, trigger_reset_lambda)
    def update(self):
        for timer in self.timers:
            self.timers[timer].update()

class WorkdayTimekeeper(Timekeeper):
    def __init__(self):
        self.init_timer('breaks', 30, steady(violet), button.is_pressed)
        self.init_timer('workday', 8*60, steady(green), button.is_pressed)


