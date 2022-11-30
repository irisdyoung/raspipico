# raspipico
Simple timekeeping and mqtt functionality for a Raspberry Pi Pico with wireless and LEDs.

You will need:

- Raspberry Pi Pico with wireless capabilities
- Connected to 6 LEDs (pins 3-8 on my device; edit `rainbow.py` to select different ones)
- umqtt.simple library on the pico
- paho_mqtt on your laptop or other device capable of full-featured python
- Google API and authentication APIs (google-api-python-client and google-auth-oauthlib) on your laptop or other device -- see https://github.com/googleapis/google-api-python-client/tree/main/docs for reference
- A Google calendar and Gmail account to connect to
- Custom filters set up to label the emails you want to monitor for

The authentication process will ask for read-only permissions to the calendar and gmail account you want to monitor. If you don't want to grant these permissions, you can remove credentials.py and anything that imports it -- this will kill about half the functionality here. Or substitute something of your own design. 

You could also consider creating a new account with Google just for this interface. It could only receive the emails from your computing cluster and only have read access to calendar(s) you share with it for events you want to be notified for. I haven't yet looked into setting this up for non-Google emails and calendars.

This repo will allow you to:

- Control 6 LEDs to have them each reflect something they are monitoring. Specifically:
- **RED:** Is the server down? You can modify check_perlmutter_status.py to check some other server or webpage of your choosing.
- **ORANGE:** Notify me when a batch job completes, and let me know if it exited or completed normally. For this you will need to set up both mail notification on job completion (on slurm, use `--mail-type=END,FAIL` and `--mail-user=your.email@address`) and a filter in Gmail to label these incoming messages.
- **YELLOW:** Notify me when an interactive session I've requested is ready for me. For this you will again need to set up notifications from your cluster, this time with `--mail-type=ALL`, and matching filters in Gmail.
- **GREEN:** Let me know when I've put in 8 hours of work. This is completely internal to the pico. 
- **BLUE:** Notify me when I have a meeting coming up (steady light for a 10 minute warning, and flashing for a 1 minute warning). This one depends on being able to query your Google calendar.
- **VIOLET:** Let me know when I've been working for a half hour and should take a stretch break. This one is also completely internal to the pico. At some later point I will add functionality for a button to reset this light; right now it's a dummy button because I don't have the physical button to test with yet.

More details soon -- I have pages of notes on the process of setting this up and all the wrong turns I made. In the meantime, please reach out to me at @irisvirus@fediscience.org (on mastodon) or irisdyoung@gmail.com with any communications.
