from enum import Enum


class DistanceUnits(Enum):
    """Supported distance units."""

    METERS = 1
    KILOMETERS = 1000
    MILES = 1609.34


class DateTimeParts(Enum):
    """Supported parts of a timestamp."""

    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    DAY_OF_WEEK = "day_of_week"
    HOUR = "hour"
    MINUTE = "minute"
    SECOND = "second"


class DaysOfWeek(Enum):
    """Supported days of the week."""

    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
