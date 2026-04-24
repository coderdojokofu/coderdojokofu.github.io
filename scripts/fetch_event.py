#!/usr/bin/env python3
"""Fetch the next upcoming CoderDojo甲府 event from Connpass and write event.json."""

import json
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

SERIES_ID = 4255
API_URL = f"https://connpass.com/api/v1/event/?series_id={SERIES_ID}&order=2&count=5"
JST = timezone(timedelta(hours=9))


def fetch_events():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())["events"]


def main():
    try:
        events = fetch_events()
    except Exception as e:
        print(f"Failed to fetch events: {e}", file=sys.stderr)
        sys.exit(0)

    now = datetime.now(JST)
    upcoming = [e for e in events if datetime.fromisoformat(e["started_at"]) > now]

    if not upcoming:
        print("No upcoming events found.", file=sys.stderr)
        sys.exit(0)

    event = upcoming[0]
    started = datetime.fromisoformat(event["started_at"])

    result = {
        "title": event["title"],
        "started_at": event["started_at"],
        "month": f"{started.month}月",
        "day": str(started.day),
        "place": event.get("place", ""),
        "url": event["event_url"],
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    with open("event.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Next event: {result['title']} on {result['started_at']}")


if __name__ == "__main__":
    main()
