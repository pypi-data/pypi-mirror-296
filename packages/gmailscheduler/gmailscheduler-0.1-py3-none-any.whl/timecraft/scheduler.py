from datetime import datetime, timedelta, tzinfo, timezone
import pytz
from .google_calendar import GoogleCalendar
from logging import getLogger
from .participant import Participant

log = getLogger('__name__')


class Scheduler:
    def __init__(self):
        self.participants = []
        self.google_calendar = GoogleCalendar()

    def add_participant(self, participant):
        self.participants.append(participant)

    def make_offset_aware(self, dt):
        if dt.tzinfo is None:  # Check if datetime is naive
            return dt.replace(
                tzinfo=timezone.utc)  # Assume UTC for naive datetime
        return dt

    def find_best_slot(self, calendar_data, start_time, end_time,
                       event_duration_minutes=60):
        # Parse the start and end time to datetime objects
        time_min_dt = self.make_offset_aware(start_time)
        time_max_dt = self.make_offset_aware(end_time)

        # Collect all busy times
        all_busy_times = []

        for calendar in calendar_data:
            for calendar_id, events in calendar.items():
                for event in events:
                    busy_start = datetime.fromisoformat(event['start'])
                    busy_end = datetime.fromisoformat(event['end'])
                    all_busy_times.append(
                        {'start': self.make_offset_aware(busy_start), 'end': self.make_offset_aware(busy_end)})

        # Sort the busy times by start time
        all_busy_times.sort(key=lambda x: x['start'])

        # Initialize the current time to the start of the search window
        current_time = time_min_dt
        best_slot = None
        # Iterate through the sorted busy periods to find free slots
        for busy_period in all_busy_times:
            busy_start = busy_period['start']
            busy_end = busy_period['end']

            # Check if there is a free slot before this busy period
            if current_time < busy_start:
                free_end = busy_start
                if free_end - current_time >= timedelta(
                        minutes=event_duration_minutes):
                    # This is a potential free slot
                    free_slot = (current_time, free_end)

                    # Select the earliest available slot
                    if best_slot is None or free_slot[0] < best_slot[0]:
                        best_slot = free_slot

            # Move current time forward to the end of this busy period if it overlaps
            if current_time < busy_end:
                current_time = busy_end

        # Check for a free slot after the last busy period until the end of the search window
        if current_time < time_max_dt:
            if time_max_dt - current_time >= timedelta(
                    minutes=event_duration_minutes):
                free_slot = (current_time, time_max_dt)
                if best_slot is None or free_slot[0] < best_slot[0]:
                    best_slot = free_slot

        # Output the best available slot
        if best_slot:
            print(f"Best available slot: {best_slot[0]} to {best_slot[1]}")
        else:
            print("No available slots found.")

        return best_slot

    def schedule_event(self, title, duration=60, constraints=None,
                       priority_list=None):
        # Define the time range for checking availability (e.g., next 7 days)
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(days=7)
        time_min = start_time.isoformat() + 'Z'
        time_max = end_time.isoformat() + 'Z'

        # Get calendar IDs and check availability
        calendar_ids = self.google_calendar._get_calendar_ids()
        availability = self.google_calendar.get_availability(calendar_ids,
                                                             time_min, time_max)
        # Find the best available slot considering constraints and priorities        best_start, best_end = self._find_best_slot(availability, duration)

        best_slot =self.find_best_slot(calendar_data=availability, start_time=start_time, end_time=end_time)
        if not best_slot:
            print("No suitable slots found.")
            return None

        best_start,best_end = best_slot[0], best_slot[1]


        # Add the event to Google Calendar
        event_result = self.google_calendar.add_event(title, best_start.isoformat(),end_time=(best_start+timedelta(minutes=30)).isoformat(),
                                                      description="Scheduled by timecraft")

        return best_start if event_result else None

    def __repr__(self):
        return f"Scheduler(participants={self.participants})"

