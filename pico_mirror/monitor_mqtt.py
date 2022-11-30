from subscribe_mqtt import Communicator
from secrets import secrets
from rainbow import red, orange, yellow, blue, button, blinker, steady

topic = secrets['mqtt_main_topic']
perl_status_topic = topic + '/perl_status'
calendar_status_topic = topic + '/calendar'
interactive_status_topic = topic + '/interactive'
batch_status_topic = topic + '/batch'

class Responder(object):
    def __init__(self, led_responder, respond_message, reset_message,
                 alt_responder=None, alt_message=None):
        self.led = led_responder
        self.alt_led = alt_responder
        self.respond_message = respond_message
        self.alt_message = alt_message
        self.reset_message = reset_message
    def update(self, message):
        if message == self.respond_message:
            self.led.respond()
        elif message == self.alt_message:
            self.alt_led.respond()
        elif message == self.reset_message:
            self.reset()
    def reset(self):
        self.time_since = None
        self.led.reset()

class Monitor(object):
    def __init__(self):
        self.comm = Communicator()
        self.monitors = {}
        self.monitors[perl_status_topic] = Responder(
            steady(red),
            'Perlmutter is down or degraded.',
            'Perlmutter is OK.')
        self.monitors[calendar_status_topic] = Responder(
            steady(blue),
            'Meeting starting in <10 minutes.',
            'No events in the next hour.',
            alt_responder = blinker(blue, 100, 100, 60*11, blocking=False),
            alt_message = 'Meeting starting in 1 minute.')
        self.monitors[interactive_status_topic] = Responder(
            blinker(yellow, 100, 100, 3*60, blocking=False),
            'Interactive job is ready!!!!',
            'No interactive jobs active.')
        self.monitors[batch_status_topic] = Responder(
            steady(orange),
            'Slurm job completed.',
            'No jobs to report.',
            alt_responder = blinker(orange, 100, 100, 60, blocking=False),
            alt_message = 'Slurm job exited.')
    def update(self, force=False):
        self.comm.update(force=force)
        for topic in self.comm.messages:
            message = self.comm.messages[topic]
            self.monitors[topic].update(message)


