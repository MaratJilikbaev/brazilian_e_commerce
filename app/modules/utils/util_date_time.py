import datetime
import pytz


def dt_from_string(dt: str, format='%Y-%m-%d'):
    return datetime.datetime.strptime(dt, format)


def dt_to_string(dt: datetime.datetime, format='%Y-%m-%d'):
    return dt.strftime(format)


def string_utc_to_seconds_since_epoch(dt_string, format='%Y-%m-%d %H:%M:%S'):
    local = pytz.timezone("UTC")
    naive = datetime.datetime.strptime(dt_string, format)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    secs = int(utc_dt.timestamp())
    return secs


if __name__ == '__main__':
    secs1 = string_utc_to_seconds_since_epoch('2001-01-01 00:00:00')
    secs2 = string_utc_to_seconds_since_epoch('2019-12-31 19:20:21')
    assert secs1 == 978307200
    assert secs2 == 1577820021
    print(f'secs1={secs1}')
    print(f'secs2={secs2}')

    d1 = dt_from_string('2022-01-01', format='%Y-%m-%d')
    d2 = dt_from_string('2022-07-05', format='%Y-%m-%d')
    delta = d2 - d1
    print(f'days={delta.days} between d1={d1} and d2={d2}')
    pass