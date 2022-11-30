from monitor_mqtt import Monitor
from timekeeping import WorkdayTimekeeper
from rainbow import rainbow
import time

timekeeper = WorkdayTimekeeper()
monitor = Monitor()

def monitor_input():
    pass

def main_loop(delay_s=1):
    rainbow(repeats=2)
    while True:
        start_time = time.time()
        timekeeper.update()
        monitor.update()
        monitor_input()
        delta = time.time() - start_time
        if delta < delay_s:
            time.sleep(delay_s - delta)

main_loop()

