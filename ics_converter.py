from ics import Calendar, Event
import json
from pathlib import Path


def convert_to_24h(time: str, am_pm: str):
    if am_pm == "AM":
        return f"{time}:00"
    elif am_pm == "PM":
        hour, minute = time.split(":")
        return f"{int(hour)+12}:{minute}:00"
    else:
        raise ValueError(f"am_pm must be AM or PM")


def format_datetime(date: str, time: str) -> tuple[str, str]:
    d, m, y = date.split(" - ")[0].split('/')
    t0, t1 = time.split(" - ")
    
    t0 = convert_to_24h(*t0.split(" "))
    t1 = convert_to_24h(*t1.split(" "))

    return f"{y}-{m}-{d} {t0}", f"{y}-{m}-{d} {t1}"


if __name__ == '__main__':
    with open(Path(__file__).parent.joinpath("museum_events.json"), 'r') as json_file:
        museum_events = json.load(json_file)

        calendar = Calendar()

        for event in museum_events:
            calendar_event = Event()
            calendar_event.name = event['name']
            calendar_event.begin, calendar_event.end = format_datetime(event['date'],
                                                                       event['time'])
            calendar_event.description = (f"{event['description']}\n"
                                          f"{event['booking_details']}\n"
                                          f"{event['event_page']}\n")
            calendar_event.location = event['location']
            calendar.events.add(calendar_event)

        with open(Path(__file__).parent.joinpath("museum_events.ics"), 'w') as ics_file:
            ics_file.writelines(calendar.serialize_iter())
