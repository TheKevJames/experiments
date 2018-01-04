#!/usr/bin/env python
import calendar
import datetime
import inspect
import time
import sys

if sys.version[0] == '2':
    import tzlocal
    import pytz


POSIX = int(time.time())
STRUCT_TIME_LOCAL = time.localtime()
STRUCT_TIME_UTC = time.gmtime()
if sys.version[0] == '2':
    AWARE_DATETIME = datetime.datetime.now(pytz.timezone('UTC'))
else:
    AWARE_DATETIME = datetime.datetime.now(datetime.timezone.utc)
AWARE_DATETIME = AWARE_DATETIME.replace(microsecond=0)
NAIVE_DATETIME_LOCAL = datetime.datetime.now()
NAIVE_DATETIME_LOCAL = NAIVE_DATETIME_LOCAL.replace(microsecond=0)
NAIVE_DATETIME_UTC = datetime.datetime.utcnow()
NAIVE_DATETIME_UTC = NAIVE_DATETIME_UTC.replace(microsecond=0)

TABLE = {
    'posix': {
        'posix': lambda x: x,
        'struct_time_local': lambda x: time.localtime(x),
        'struct_time_utc': lambda x: time.gmtime(x),
        'naive_datetime_local': lambda x: datetime.datetime.fromtimestamp(x),
        'naive_datetime_utc': lambda x: datetime.datetime.utcfromtimestamp(x),
        'aware_datetime_py2': lambda x: datetime.datetime.fromtimestamp(x, pytz.timezone('UTC')),
        'aware_datetime_py3': lambda x: datetime.datetime.fromtimestamp(x, datetime.timezone.utc),
    },
    'struct_time_local': {
        'posix': lambda x: time.mktime(x),
        'struct_time_local': lambda x: x,
        'naive_datetime_local': lambda x: datetime.datetime(*x[:6]),
    },
    'struct_time_utc': {
        'posix': lambda x: calendar.timegm(x),
        'struct_time_utc': lambda x: x,
        'naive_datetime_utc': lambda x: datetime.datetime(*x[:6]),
        'aware_datetime_py2': lambda x: datetime.datetime(*x[:6], tzinfo=pytz.timezone('UTC')),
        'aware_datetime_py3': lambda x: datetime.datetime(*x[:6], tzinfo=datetime.timezone.utc),
    },
    'naive_datetime_local': {
        'naive_datetime_local': lambda x: x,
        'aware_datetime_py2': lambda x: x.replace(tzinfo=tzlocal.get_localzone()),
        'aware_datetime_py3': lambda x: x.astimezone(),
    },
    'naive_datetime_utc': {
        'posix': lambda x: calendar.timegm(x.utctimetuple()),
        'struct_time_utc': lambda x: x.utctimetuple(),
        'naive_datetime_utc': lambda x: x,
        'aware_datetime_py2': lambda x: x.replace(tzinfo=pytz.timezone('UTC')),
        'aware_datetime_py3': lambda x: x.replace(tzinfo=datetime.timezone.utc),
    },
    'aware_datetime_py2': {
        'posix': lambda x: calendar.timegm(x.utctimetuple()),
        'struct_time_utc': lambda x: x.utctimetuple(),
        'naive_datetime_local': lambda x: x.astimezone(tzlocal.get_localzone()).replace(tzinfo=None),
        'naive_datetime_utc': lambda x: x.astimezone(pytz.timezone('UTC')).replace(tzinfo=None),
        'aware_datetime_py2': lambda x: x,
    },
    'aware_datetime_py3': {
        'posix': lambda x: calendar.timegm(x.utctimetuple()),
        'struct_time_utc': lambda x: x.utctimetuple(),
        'naive_datetime_local': lambda x: x.astimezone().replace(tzinfo=None),
        'naive_datetime_utc': lambda x: x.astimezone(datetime.timezone.utc).replace(tzinfo=None),
        'aware_datetime_py3': lambda x: x,
    },
}


def test(my_name, my_value):
    try:
        x = TABLE[my_name]['posix'](my_value)
        y = TABLE['posix'][my_name](x)
        assert x == POSIX, '{} != {}'.format(x, POSIX)
        assert y == my_value, '{} != {}'.format(y, my_value)
    except KeyError:
        print('unsupported: {} -> {}'.format(my_name, 'posix'))

    try:
        x = TABLE[my_name]['struct_time_local'](my_value)
        y = TABLE['struct_time_local'][my_name](x)
        assert x == STRUCT_TIME_LOCAL, '{} != {}'.format(x, STRUCT_TIME_LOCAL)
        assert y == my_value, '{} != {}'.format(y, my_value)
    except KeyError:
        print('unsupported: {} -> {}'.format(my_name, 'struct_time_local'))

    try:
        x = TABLE[my_name]['struct_time_utc'](my_value)
        y = TABLE['struct_time_utc'][my_name](x)
        assert x == STRUCT_TIME_UTC, '{} != {}'.format(x, STRUCT_TIME_UTC)
        assert y == my_value, '{} != {}'.format(y, my_value)
    except KeyError:
        print('unsupported: {} -> {}'.format(my_name, 'struct_time_utc'))

    try:
        x = TABLE[my_name]['naive_datetime_local'](my_value)
        y = TABLE['naive_datetime_local'][my_name](x)
        assert x == NAIVE_DATETIME_LOCAL, '{} != {}'.format(x, NAIVE_DATETIME_LOCAL)
        assert y == my_value, '{} != {}'.format(y, my_value)
    except KeyError:
        print('unsupported: {} -> {}'.format(my_name, 'naive_datetime_local'))

    try:
        x = TABLE[my_name]['naive_datetime_utc'](my_value)
        y = TABLE['naive_datetime_utc'][my_name](x)
        assert x == NAIVE_DATETIME_UTC, '{} != {}'.format(x, NAIVE_DATETIME_UTC)
        assert y == my_value, '{} != {}'.format(y, my_value)
    except KeyError:
        print('unsupported: {} -> {}'.format(my_name, 'naive_datetime_utc'))

    try:
        if sys.version[0] == '2':
            x = TABLE[my_name]['aware_datetime_py2'](my_value)
            y = TABLE['aware_datetime_py2'][my_name](x)
        else:
            x = TABLE[my_name]['aware_datetime_py3'](my_value)
            y = TABLE['aware_datetime_py3'][my_name](x)
        assert x == AWARE_DATETIME, '{} != {}'.format(x, AWARE_DATETIME)
        assert y == my_value, '{} != {}'.format(y, my_value)
    except KeyError:
        print('unsupported: {} -> {}'.format(my_name, 'aware_datetime'))


def test_all():
    test('posix', POSIX)
    test('struct_time_local', STRUCT_TIME_LOCAL)
    test('struct_time_utc', STRUCT_TIME_UTC)
    test('naive_datetime_local', NAIVE_DATETIME_LOCAL)
    test('naive_datetime_utc', NAIVE_DATETIME_UTC)
    if sys.version[0] == '2':
        test('aware_datetime_py2', AWARE_DATETIME)
    else:
        test('aware_datetime_py3', AWARE_DATETIME)


def print_table():
    ordered = ['posix', 'struct_time_local', 'struct_time_utc',
               'naive_datetime_local', 'naive_datetime_utc',
               'aware_datetime_py2', 'aware_datetime_py3']
    display_name = {
        'posix': '`POSIX`',
        'struct_time_local': '`struct_time` (local)',
        'struct_time_utc': '`struct_time` (UTC)',
        'naive_datetime_local': 'Naive `datetime` (local)',
        'naive_datetime_utc': 'Naive `datetime` (UTC)',
        'aware_datetime_py2': 'Aware `datetime` (Py2)',
        'aware_datetime_py3': 'Aware `datetime` (Py3)',
    }
    def display_code(lhs, rhs):
        if not TABLE[lhs].get(rhs):
            return '-'  # indirect
        src = inspect.getsource(TABLE[lhs][rhs]).strip(' ,\n')
        code = src.split('lambda x: ')[1]
        if code == 'x':
            return '-'
        return '`{}`'.format(code)

    print('| Row -> Col | {} |'.format(' | '.join(display_name[k] for k in ordered)))
    print('|----|{}|'.format('|'.join('-----' for _ in ordered)))
    for lhs in ordered:
        print('| {} | {} |'.format(display_name[lhs], ' | '.join(display_code(lhs, k) for k in ordered)))


test_all()
print_table()
