import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendar:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        print (os.getcwd())
        self._authenticate()

    def _authenticate(self):
        # Check if the token file exists
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        # If no valid credentials are available, go through the OAuth flow
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for future use
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

    def _get_calendar_ids(self):
        try:
            service = build('calendar', 'v3', credentials=self.creds)
            calendar_list = service.calendarList().list().execute()
            calendars = []
            for calendar in calendar_list.get('items', []):
                calendars.append({
                    'id': calendar['id'],
                    'summary': calendar.get('summary', 'No Summary')
                })
            return [cal['id'] for cal in calendars]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def add_event(self, title, start_time, end_time, description=None):
        try:
            service = build('calendar', 'v3', credentials=self.creds)
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'UTC',  # Adjust time zone as needed
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'UTC',  # Adjust time zone as needed
                },
            }
            event_result = service.events().insert(calendarId='primary', body=event).execute()
            print (f'Event added: {event_result}')
            return event_result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_availability(self, calendar_ids, time_min, time_max,
                         event_duration_minutes=60):
        """
        Get the availability of the specified calendars within a time range.

        :param calendar_ids: List of calendar IDs to check.
        :param time_min: ISO formatted start time for the availability query.
        :param time_max: ISO formatted end time for the availability query.
        :param event_duration_minutes: Duration of the event in minutes.
        :return: Dictionary with calendar IDs and a list of free time slots.
        """
        service = build('calendar', 'v3', credentials=self.creds)

        try:
            cal_events = []
            for calendar_id in calendar_ids:
                # Set up the query parameters for the events list
                events_result = service.events().list(
                    calendarId=calendar_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()

                events = events_result.get('items', [])

                # Check if there are any events
                if not events:
                    continue

                # List to store event details
                calendar_events = []

                print(f"Events scheduled in calendar '{calendar_id}':")
                for event in events:
                    start = event['start'].get('dateTime',
                                               event['start'].get('date'))
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    summary = event.get('summary', 'No Title')

                    # Print event details
                    print(f"- {summary}: {start} to {end}")

                    # Add to list of events
                    calendar_events.append({
                        'summary': summary,
                        'start': start,
                        'end': end,
                        'id': event['id']
                    })

                cal_events.append({calendar_id: calendar_events})
            return cal_events

        except Exception as e:
            print(f"An error occurred: {e}")
            return []
