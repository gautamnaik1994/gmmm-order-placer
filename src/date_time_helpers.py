from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

holiday_list = [
    # '2022-01-26',
    # '2022-03-01',
    # '2022-03-18',
    # '2022-04-14',
    # '2022-04-15',
    # '2022-05-03',
    # '2022-08-09',
    # '2022-08-15',
    # '2022-08-31',
    # '2022-10-05',
    # '2022-10-24',
    # '2022-10-26',
    # '2022-11-08',
    # '2023-01-26',
    # '2023-03-07',
    # '2023-03-30',
    # '2023-04-04',
    # '2023-04-07',
    # '2023-04-14',
    # '2023-05-01',
    # '2023-06-29',
    # '2023-08-15',
    # '2023-09-19',
    # '2023-10-02',
    # '2023-10-24',
    # '2023-11-14',
    # '2023-11-27',
    # '2023-12-25',
    # '2024-01-26',
    # '2024-02-19',
    # '2024-03-08',
    # '2024-03-25',
    # '2024-03-29',
    # '2024-04-09',
    # '2024-04-11',
    # '2024-04-17',
    # '2024-05-01'
    # '2024-05-20',
    # '2024-06-17',
    # '2024-07-17',
    # '2024-08-15',
    # '2024-10-02',
    # '2024-11-01',
    # '2024-11-15',
    # '2024-12-25',
    '2025-01-26',
    "2025-02-26",
    "2025-03-14",
    "2025-03-31",
    "2025-04-10",
    "2025-04-14",
    "2025-04-18",
    "2025-05-01",
    "2025-08-15",
    "2025-08-27",
    "2025-10-02",
    "2025-10-21",
    "2025-10-22",
    "2025-11-05",
    "2025-12-25",
    '2026-01-26',
    '2026-03-03',
    '2026-03-26',
    '2026-03-31',
    '2026-04-03',
    '2026-04-14',
    '2026-05-01',
    '2026-05-28',
    '2026-06-26',
    '2026-09-14',
    '2026-10-02',
    '2026-10-20',
    '2026-11-10',
    '2026-11-24',
    '2026-12-25'
]

muhurat_trading = '2024-11-01'


def check_if_holiday(date):
    date = date.strftime("%Y-%m-%d")
    if date in holiday_list:
        return True
    return False


def check_if_today_holiday():
    return check_if_holiday(get_converted_datetime())


def check_if_weekend(date):
    if date.weekday() == 5 or date.weekday() == 6:
        return True
    return False


def get_converted_datetime():
    database_time = datetime.utcnow()
    utctime = database_time.replace(tzinfo=ZoneInfo('UTC'))
    localtime = utctime.astimezone(ZoneInfo('Asia/Kolkata'))
    return localtime


def get_current_date():
    return get_converted_datetime().strftime("%Y-%m-%d")


def get_current_date_obj():
    return get_converted_datetime()


def get_current_year_month():
    return get_converted_datetime().strftime("%Y-%m")


def get_current_day():
    return get_converted_datetime().strftime("%d")


def get_current_year():
    return get_converted_datetime().strftime("%Y")


def get_current_month():
    return get_converted_datetime().strftime("%m")


def get_current_time():
    return get_converted_datetime().strftime("%H:%M:%S")


def get_current_date_time():
    return get_converted_datetime().strftime("%Y-%m-%d %H:%M:%S")


def get_next_tradable_date(formatted=True):
    current_date = get_converted_datetime()
    # current_date = datetime.strptime('13-04-2022', "%Y-%m-%d")
    found_date = False
    next_tradable_date = current_date
    while not found_date:
        next_tradable_date = next_tradable_date + timedelta(days=1)
        if check_if_weekend(next_tradable_date):
            continue
        if check_if_holiday(next_tradable_date):
            continue
        found_date = True
    if not formatted:
        return next_tradable_date
    return next_tradable_date.strftime("%Y-%m-%d")


def get_prev_tradable_date(formatted=True):
    current_date = get_converted_datetime()
    # current_date = datetime.strptime('2022-03-21', "%Y-%m-%d")
    found_date = False
    prev_tradable_date = current_date
    while not found_date:
        prev_tradable_date = prev_tradable_date + timedelta(days=-1)
        if check_if_weekend(prev_tradable_date):
            continue
        if check_if_holiday(prev_tradable_date):
            continue
        found_date = True
    if not formatted:
        return prev_tradable_date
    return prev_tradable_date.strftime("%Y-%m-%d")


# print(get_current_year())
