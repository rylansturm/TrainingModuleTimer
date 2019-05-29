import datetime


def countdown_format(seconds: int):
    """ takes int (seconds) and returns str (":SS", "MM:SS", or "HH:MM:SS") """
    sign = -1 if seconds < 0 else 1
    seconds = seconds * sign
    sign_label = '-' if sign < 0 else ''
    hours, minutes = divmod(seconds, 3600)
    minutes, seconds = divmod(minutes, 60)
    hour_label = '%sh:%02d' % (hours, minutes)
    minute_label = '%s:%02d' % (minutes, seconds)
    second_label = sign_label + ':%02d' % seconds
    return seconds if hours < 0 else hour_label if hours else minute_label if minutes else second_label


def now():
    """ shorthand for the current datetime object """
    return datetime.datetime.now()
