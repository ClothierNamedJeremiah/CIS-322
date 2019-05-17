import arrow
import timeblocks
def get_all_busy(service,calendars,begin_date,end_date,begin_time,end_time):
    """
    @brief      creates a list of busy times using events from a set of given calendars

    @param      service: Google 'service' object
    @param      calendars (dict): a list of calendars
    @param      begin_date (str): beginning of busy times date range. ISO formated date EX. 2017-11-15T00:00:00-08:00
    @param      end_date (str): end of busy times date range. ISO formated date EX. 2017-11-21T00:00:00-08:00
    @param      begin_time (str): beginning of busy times time range. Format HH:mm EX. 08:00
    @param      end_time (str): end of busy times time range. Format HH:mm EX. 17:00

    @return     a list of events (event_description,start_str,end_str) marked as busy for all calendars

    """
    all_busy_times = [] # List of lists, each list holds busy times for ONE calendar
    begin_hr, begin_min = list(map(int,begin_time.strip().split(":")))
    end_hr, end_min = list(map(int,end_time.strip().split(":")))
    begin_date = arrow.get(begin_date)
    begin_date = begin_date.shift(hours=+begin_hr,minutes=+begin_min)
    end_date = arrow.get(end_date)
    end_date = end_date.shift(hours=+end_hr,minutes=+end_min)

    for calendar in calendars:
        all_busy_times += get_busy(service,calendar["id"],begin_date,end_date,None) # Add additional busy times to list of all busy times

    # all_busy_times contains a list of TimeBlocks
    all_busy_times.sort(key=lambda x:x.get_start_time()) # sorts in place by starting dates of calendar events
    return all_busy_times

def get_busy(service,calendar_id,begin_date,end_date,unique_id = None):
    """
    @brief      creates a list of busy times using events for ONE Google Calendar

    @param      service: Google 'service' object
    @param      calendar_id: a specific Google calendar's id
    @param      begin_date (arrow): beginning of busy times date range
    @param      end_date (arrow): end of busy times date range
    @param      unique_id: specific id of a recurring Google calendar event

    @return     a list of events from a calendar(event_description,start_str,end_str) that which a person is marked "busy"

    """
    busy_events = []
    page_token = None
    i = 0
    while True:
        # Events: list (https://developers.google.com/google-apps/calendar/v3/reference/events/list#examples)
        if unique_id:
            events = service.events().instances(calendarId=calendar_id, eventId=unique_id,pageToken=page_token).execute()
        else:
            events = service.events().list(calendarId=calendar_id,pageToken=page_token).execute()
        for event in events['items']:
            event_description = None
            # the 'transparency' key will only be present for calendar events marked: Show me as Available
            # Thus the condition below with result true when an event is marked
            # Show me as: Busy
            if "transparency" in event:
                continue
            # The "recurrence" key will be present in events that repeat multiple times (i.e. once a week). We must individually
            # loop thorugh each of these events by their unique_id in order to get the appropriate times and dates
            if "recurrence" in event:
                busy_events += get_busy(service,calendar_id,begin_date,end_date,event["id"])
                continue
            # Get a text field that describes the event
            try:
                event_description = event["summary"]
                # the 'date' field will only be present for events that last a whole day.
                # Otherwise a 'datetime' will be present
                if "date" in event['start']:
                    start = event['start']['date'] # Date format is YYYY-DD-MM
                    end = event['start']['date'] # Date format is YYYY-DD-MM
                else:
                    start = event['start']['dateTime'] # dateTime format is YYYY-MM-DD HH:mm:ss ZZ
                    end = event['end']['dateTime'] # dateTime format is YYYY-MM-DD HH:mm:ss ZZ
                # Create arrow objects for event start, end and the daterange
                event_start = arrow.get(start)
                event_end = arrow.get(end)
                window = timeblocks.TimeBlock(begin_date,end_date)
                event = timeblocks.TimeBlock(event_start,event_end,event_description)
                if event.is_within(window):
                    busy_events.append(event.get_overlap(window))
            except KeyError:
                print("Key Error")
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return busy_events

def list_checked(calendars,request):
    """
    @brief      creates a list of check marked calendars

    @param      calendars: A list of calendars (Google Calendars)
    @param      request: The HTTP POST request from /setcalendars

    @return     a list of calendars (Google Calendars) that were checked when the "choose calendar" button was clicked
    """
    checked_calendar_names = get_checked_calendars(calendars,request) # set of calendar names that were checked when "choose calendar" button is clicked
    list_of_checked_calendars = []
    for calendar in calendars:
        current_name = calendar["summary"] # Name of the current calendar we're looking at
        if current_name in checked_calendar_names:
            list_of_checked_calendars.append(calendar)

    return list_of_checked_calendars

def get_checked_calendars(calendars,request):
    """
    @brief      creates a list of names of all the selected calenders from our web application

    @param      calendars: A list of calendars (Google Calendars)
    @param      request: The HTTP POST request from /setcalendars

    @return     Number of displayed calendars.
    """
    num_of_calendars = count_displayed_calendars(calendars)
    checked = set()
    for i in range(1,num_of_calendars+1):
        try:
            calendar = request.form["check{}".format(i)]
            checked.add(calendar)
        # Calling requst.form["check{}"] on a checkbox that has not been "checked" will raise an error
        # If that is the case, then we can simply "skip" the current checkbox and move to check the rest [i...N+1]
        except:
            pass
    return checked

def count_displayed_calendars(calendars):
    """
    @brief      counts the number of displayed calendars

    @param      calendars: A list of calendars (Google Calendars)

    @return     Number of displayed calendars.

                For example, the user may have 7 separate calendars linked
                to their account, but only 5 are displayed on the webpage.
    """
    count = 0
    for calendar in calendars:
        if calendar['selected']:
            count += 1
    return count

    page_token = None