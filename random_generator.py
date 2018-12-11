import random
import time
from lorem.text import TextLorem


def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end):
    return str_time_prop(start, end, '%Y-%m-%d', random.random())


def random_book_name():
    with open('data/words.txt', 'r') as words:
        words_list = words.read().split()

    return random.choice(words_list)


def random_text():
    with open('data/words.txt', 'r') as words:
        words_list = words.read().split()
    lorem = TextLorem(wsep=' ', srange=(4, 7), words=words_list)
    return lorem.sentence()


def random_number():
    return random.randint()


def random_name():
    with open('data/first-names.txt', 'r') as first_names:
        first = first_names.read().split()
    with open('data/middle-names.txt', 'r') as middle_names:
        middle = middle_names.read().split()

    return random.choice(first) + ' ' + random.choice(middle)