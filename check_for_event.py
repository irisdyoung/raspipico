from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from credentials import get_credentials
import datetime

class CalendarReader(object):
    def __init__(self, creds=None):
        if creds is None:
            creds = get_credentials()
        self.service = build('calendar', 'v3', credentials=creds)
    def check_calendar(self):
        try:
            for minutes in [1,10,60]:
                now = datetime.datetime.utcnow()
                later = now + datetime.timedelta(minutes=minutes)
                now_iso = now.isoformat() + 'Z'  # 'Z' indicates UTC time
                later_iso = later.isoformat() + 'Z'
                events = []
                for cal_id in ['primary']: # add more calendars by name if you wish
                        events_result = self.service.events().list(
                                calendarId=cal_id, timeMin=now_iso,
                                timeMax=later_iso, singleEvents=True).execute()
                        events.extend(events_result.get('items', []))
                events = [e for e in events if 'dateTime' in e['start']] # filter out all-day events
                if events:
                    if minutes == 1:
                        return 'Meeting starting in 1 minute.'
                    elif minutes == 10:
                        return 'Meeting starting in <10 minutes.'
                    else:
                        return 'There is a meeting starting within the hour.'
            return 'No events in the next hour.'
        except HttpError as error:
            print('An error occurred: %s' % error)
            return 'Could not check calendar.'


if __name__ == '__main__':
    reader = CalendarReader()
    print(reader.check_calendar())
