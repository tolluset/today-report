import os
import dotenv

from googleapiclient.discovery import build

dotenv.load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

service = build(
    "calendar",
    "v3",
    developerKey=key,
)


calendar = service.calendars().get(calendarId="primary").execute()

print(f"🚀 : calendar.py:9: calendar={calendar}")


service.close()


def calendar_list():
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:
            print(calendar_list_entry["summary"])
        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break


def event_list():
    page_token = None
    while True:
        events = (
            service.events().list(calendarId="primary", pageToken=page_token).execute()
        )
        for event in events["items"]:
            print(event["summary"])
        page_token = events.get("nextPageToken")
        if not page_token:
            break
