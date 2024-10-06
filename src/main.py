#!/usr/bin/env python3
import logging
from datetime import datetime

from dateutil import parser
from dateutil.tz import gettz
from requests_cache import CachedSession

from config import read_config
from ptv import sign_url

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def main():
    config = read_config()
    url = sign_url(
        config,
        "/v3/departures/route_type/{0}/stop/{1}?direction_id={2}".format(
            config.route_type, config.stop_id, config.direction_id
        ),
    )
    session = CachedSession(
        "DepartureBoard", backend="filesystem", use_cache_dir=True, expire_after=3600
    )
    response = session.get(url)
    data = response.json()

    now = datetime.now(gettz(config.timezone))

    seen_departures = {}

    print("Departures")
    for d in data["departures"]:
        departure_time_utc = parser.parse(
            d["estimated_departure_utc"] or d["scheduled_departure_utc"]
        )
        departure_time = departure_time_utc.astimezone(gettz(config.timezone))

        if departure_time > now and departure_time not in seen_departures:
            seen_departures[departure_time] = d
            departure_time_str = departure_time.strftime("%H:%M")
            minutes_left = int((departure_time - now).total_seconds() / 60)
            print(f"{departure_time_str} ({minutes_left} minutes)")
            logger.debug(f"{departure_time_str}: {d}")

        if len(seen_departures) >= 2:
            break


if __name__ == "__main__":
    main()
