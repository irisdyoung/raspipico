# code from https://picockpit.com/raspberry-pi/everything-about-the-raspberry-pi-pico-w/#Connecting_to_WiFi
from secrets import secrets
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(secrets['wifi_ssid'], secrets['wifi_pw'])

def light_onboard_led():
    led = machine.Pin('LED', machine.Pin.OUT)
    led.on();

timeout = 10
while timeout > 0:
    if wlan.status() >= 3:
        #light_onboard_led()
        print('Connected.')
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)
   
wlan_status = wlan.status()

