from datetime import datetime
import requests
import pprint


def get_events():
    """
    Returns: The list of event object to be inserted in the calender.
    """
    try:
        r = requests.get('http://codeforces.com/api/contest.list')
        events = r.json()["result"]
        # Events to be added in the calender.
        new_events = []

        for event in events:
            if event["phase"] == "BEFORE":
                event_duration = event["durationSeconds"]
                event_start = event["startTimeSeconds"]
                event_name = event["name"]
                event_description = "This round will be " + event["type"] + " kind of event."
                event_begins = datetime.utcfromtimestamp(int(event_start)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
                event_ends = datetime.utcfromtimestamp(int(event_start) + int(event_duration)).strftime('%Y-%m-%dT%H:%M:%S+00:00')

                new_event = {
                  'summary': event_name,
                  'location': 'Raipur, India',
                  'description': event_description,
                  'start': {
                    'dateTime': event_begins,
                    'timeZone': 'Asia/Kolkata'
                  },
                  'end': {
                    'dateTime': event_ends,
                    'timeZone': 'Asia/Kolkata'
                  },
                  'reminders': {
                    'useDefault': False,
                    'overrides': [
                      {'method': 'popup', 'minutes': 15},
                    ],
                  },
                }
                new_events.append(new_event)
            else:
                # print("Event is Over! No need to add to calender!")
                continue

        if new_events:
            print("Total CodeForces Events Found are: " + str(len(new_events)))
            return new_events
        else:
            return None
    except ConnectionError:
        print("The API URL is not Valid")
    except:
        print("An unexpected error occurred!")
