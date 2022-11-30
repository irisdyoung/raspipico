# This code should be run by a laptop, not the raspberry pi pico
from paho_mqtt.mqtt_client import Communicator
from check_perlmutter_status import check_perlmutter_status
from check_for_job_completed import GmailReader
from check_for_event import CalendarReader
from credentials import get_credentials
import time

class PicoHelper(object):
    def __init__(self):
        self.creds = get_credentials()
        self.comm = Communicator()
        self.gmail_reader = GmailReader(creds=self.creds)
        self.gcal_reader = CalendarReader(creds=self.creds)
        self.topic = 'rpipico'
        self.perl_status = None
        self.interactive_ready = False
        self.batch_status = None
        self.events_status = False
    def check_perl(self):
        status = check_perlmutter_status()
        if status != self.perl_status:
            print(status)
            self.comm.send_message('{}/perl_status'.format(self.topic), status, retain=True)
            self.perl_status = status
    def check_jobs(self):
        status = self.gmail_reader.check_interactive_jobs()
        if status != self.interactive_ready:
            print(status)
            self.comm.send_message('{}/interactive'.format(self.topic), status, retain=True)
            self.interactive_ready = status
        status = self.gmail_reader.check_batch_jobs()
        if status != self.batch_status:
            print(status)
            self.comm.send_message('{}/batch'.format(self.topic), status, retain=True)
            self.batch_status = status
    def check_calendar(self):
        status = self.gcal_reader.check_calendar()
        if status != self.events_status:
            print(status)
            self.comm.send_message('{}/calendar'.format(self.topic), status, retain=True)
            self.events_status = status
    def loop(self):
        while True:
            start_time = time.time()
            self.check_perl()
            self.check_jobs()
            self.check_calendar()
            delta_time = time.time() - start_time
            if delta_time < 10:
                time.sleep(10 - delta_time)

def run_helper_on_loop():
    helper = PicoHelper()
    helper.loop()

if __name__ == "__main__":
    run_helper_on_loop()
