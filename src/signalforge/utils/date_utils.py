"""Date and time utilities module.

"""

import traceback
from datetime import datetime, timedelta, timezone

from signalforge.observability.log_config import get_logger

logger = get_logger(__name__)


def get_timestamp(include_timezone: bool = True) -> str:
    """(ISO )

    Args:
        include_timezone: 

    Returns:
        ISO 
    """
    if include_timezone:
        return datetime.now(timezone.utc).isoformat()
    else:
        return datetime.now().isoformat()


def parse_timestamp(timestamp_str: str) -> datetime | None:
    """ ISO 

    Args:
        timestamp_str: ISO 

    Returns:
        datetime , None
    """
    try:
        return datetime.fromisoformat(timestamp_str)
    except ValueError:
        logger.error(f"Invalid timestamp format: {timestamp_str}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        return None


def format_datetime(
    dt: datetime,
    format_str: str = "%Y-%m-%d %H:%M:%S",
) -> str:
    """ datetime 

    Args:
        dt: datetime 
        format_str: 

    Returns:
    """
    try:
        return dt.strftime(format_str)
    except Exception as e:
        logger.error(f"Failed to format datetime: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        return str(dt)


def parse_datetime(
    date_str: str,
    format_str: str = "%Y-%m-%d %H:%M:%S",
) -> datetime | None:
    """ datetime 

    Args:
        date_str: 
        format_str: 

    Returns:
        datetime , None
    """
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError as e:
        logger.error(f"Failed to parse datetime string '{date_str}': {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        return None


def get_current_date(
    format_str: str = "%Y-%m-%d",
    use_utc: bool = True,
) -> str:
    """

    Args:
        format_str: 
        use_utc:  UTC 

    Returns:
    """
    now = datetime.now(timezone.utc) if use_utc else datetime.now()
    return now.strftime(format_str)


def get_current_time(
    format_str: str = "%H:%M:%S",
    use_utc: bool = True,
) -> str:
    """

    Args:
        format_str: 
        use_utc:  UTC 

    Returns:
    """
    now = datetime.now(timezone.utc) if use_utc else datetime.now()
    return now.strftime(format_str)


def get_time_difference(
    dt1: datetime,
    dt2: datetime,
    unit: str = "seconds",
) -> float:
    """

    Args:
        dt1:  datetime 
        dt2:  datetime 
        unit:  (seconds, minutes, hours, days)

    Returns:
    """
    diff = abs((dt1 - dt2).total_seconds())

    if unit == "seconds":
        return diff
    elif unit == "minutes":
        return diff / 60
    elif unit == "hours":
        return diff / 3600
    elif unit == "days":
        return diff / 86400
    else:
        logger.warning(f"Unknown unit '{unit}', returning seconds")
        return diff


def is_weekend(dt: datetime | None = None) -> bool:
    """

    Args:
        dt: datetime ,

    Returns:
         True, False
    """
    if dt is None:
        dt = datetime.now()
    return dt.weekday() >= 5  # 5=Saturday, 6=Sunday


def humanize_timedelta(
    td: timedelta | float,
    precision: int = 2,
) -> str:
    """ timedelta 

    Args:
        td: timedelta 
        precision: 

    Returns:
    """
    if isinstance(td, int | float):
        td = timedelta(seconds=td)

    total_seconds = int(td.total_seconds())

    if total_seconds == 0:
        return "0 seconds"

    units = [
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    ]

    parts = []
    for unit_name, unit_seconds in units:
        if total_seconds >= unit_seconds:
            value = total_seconds // unit_seconds
            total_seconds %= unit_seconds
            unit_str = unit_name if value == 1 else f"{unit_name}s"
            parts.append(f"{value} {unit_str}")

            if len(parts) >= precision:
                break

    return ", ".join(parts)


def get_unix_timestamp(dt: datetime | None = None) -> int:
    """ Unix ()

    Args:
        dt: datetime ,

    Returns:
        Unix 
    """
    if dt is None:
        dt = datetime.now()

    return int(dt.timestamp())


def from_unix_timestamp(timestamp: int) -> datetime:
    """ Unix  datetime 

    Args:
        timestamp: Unix ()

    Returns:
        datetime 
    """
    return datetime.fromtimestamp(timestamp)


def add_days(dt: datetime, days: int) -> datetime:
    """ datetime 

    Args:
        dt: datetime 
        days: ()

    Returns:
         datetime 
    """
    return dt + timedelta(days=days)


def add_hours(dt: datetime, hours: int) -> datetime:
    """ datetime 

    Args:
        dt: datetime 
        hours: ()

    Returns:
         datetime 
    """
    return dt + timedelta(hours=hours)


def add_minutes(dt: datetime, minutes: int) -> datetime:
    """ datetime 

    Args:
        dt: datetime 
        minutes: ()

    Returns:
         datetime 
    """
    return dt + timedelta(minutes=minutes)


def get_week_start(dt: datetime | None = None) -> datetime:
    """(00:00:00)

    Args:
        dt: datetime ,

    Returns:
         datetime ( 00:00:00)
    """
    if dt is None:
        dt = datetime.now()
    # weekday()  0=Monday, 6=Sunday
    days_since_monday = dt.weekday()
    monday = dt - timedelta(days=days_since_monday)
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


def get_month_start(dt: datetime | None = None) -> datetime:
    """(00:00:00)

    Args:
        dt: datetime ,

    Returns:
         datetime ( 00:00:00)
    """
    if dt is None:
        dt = datetime.now()
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
