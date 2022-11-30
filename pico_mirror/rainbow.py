import machine
import time
def ledpin(pin_id):
    return machine.Pin(pin_id, machine.Pin.OUT)
class dummy_button(object):
    def is_pressed(null):
        return False

red = ledpin(3)
orange = ledpin(4)
yellow = ledpin(5)
green = ledpin(6)
blue = ledpin(7)
violet = ledpin(8)
button = dummy_button()

def rainbow(repeats=10, delay=0.2):
    def pause():
        time.sleep(delay)
    for repeat in range(repeats):
        red.on(); pause()
        orange.on(); pause()
        yellow.on(); pause()
        green.on(); pause()
        blue.on(); pause()
        violet.on(); pause()
        red.off(); pause()
        orange.off(); pause()
        yellow.off(); pause()
        green.off(); pause()
        blue.off(); pause()
        violet.off(); pause()

class blinker(object):
    def __init__(self, led, on_duration_ms, off_duration_ms, timeout_s, blocking=False):
        self.led = led
        self.on_duration_ms = on_duration_ms
        self.off_duration_ms = off_duration_ms
        if blocking:
                self.loops = int(timeout_s * 1000 / (self.on_duration_ms + self.off_duration_ms))
        else:
                self.loops = int(1000 / (self.on_duration_ms + self.off_duration_ms))
        self.timeout_s = timeout_s
        self.time_start = None
    def respond(self, time_since=None):
        if time_since is None:
            if self.time_start is None:
                self.time_start = time.time()
            time_since = time.time() - self.time_start
        if time_since < self.timeout_s:
            for i in range(self.loops):
                self.led.on()
                time.sleep_ms(self.on_duration_ms)
                self.led.off()
                time.sleep_ms(self.off_duration_ms)
        else:
            self.led.off()
    def reset(self):
        self.time_start = None
        self.led.off()

class steady(object):
    def __init__(self, led):
        self.led = led
    def respond(self, time_since=None):
        self.led.on()
    def reset(self):
        self.led.off()

#rainbow(repeats=10, delay=0.2)



