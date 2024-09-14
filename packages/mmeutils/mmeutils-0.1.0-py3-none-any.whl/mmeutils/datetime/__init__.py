"""Date & Time Manipulation"""


import time

from typing import Tuple


def get_time_format() -> int:
    """Detects and returns 12 vs 24 hour time format usage.
    
    :return: 12 or 24
    :rtype: int
    """
    return 12 if ('AM' in time.strftime('%X') or 'PM' in time.strftime('%X')) else 24


def get_timezone_offset() -> Tuple[int, int]:
    """Returns the local timezone offset from UTC.
    
    :return: A tuple (`diff_from_utc`, `hours_in_seconds`)
    :rtype: Tuple[int, int]
    """
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone

    diff_from_utc = int(offset / 60 / 60 * -1)
    hours_in_seconds = diff_from_utc * 3600 * -1

    return diff_from_utc, hours_in_seconds


def get_adjusted_datetime(
            epoch_timestamp: int,
            format_string: str="%Y-%m-%dT%H:%M"
        ) -> str:
    """Converts an epoch timestamp to the time of the
    local computers' timezone.

    :param epoch_timestamp: An UNIX epoch timestamp.
    :type epoch_timestamp: int

    :param format_string: The `strftime()`-compatible date-time format string.
    :type format_string: str

    :return: A formatted date-time string.
    :rtype: str
    """
    diff_from_utc, hours_in_seconds = get_timezone_offset()

    adjusted_timestamp = epoch_timestamp + diff_from_utc * 3600
    adjusted_timestamp += hours_in_seconds

    return time.strftime(format_string, time.localtime(adjusted_timestamp))
