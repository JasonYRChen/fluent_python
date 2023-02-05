from collections import namedtuple
from random import randrange, choice
from time import sleep, time


RANDRANGESTART = 1
RANDRANGEEND = 9


event = namedtuple('Event', 'time taxi status')


def prime(gen):
    def inner(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g
    return inner


@prime
def schedule(taxi, laps):
    time = yield
    time = yield event(time, taxi, 'leave garage')
    for _ in range(laps):
        time = yield event(time, taxi, 'pick up passenger')
        time = yield event(time, taxi, 'drop off passenger')
    yield event(time, taxi, 'back to garage')


def print_status(event):
    time = event.time
    taxi = event.taxi
    status = event.status
    print(f'time{time:>4}: {" "*4*taxi}taxi {taxi} {status}')


taxis = [schedule(0, 3), schedule(1, 2), schedule(2, 3)]
time_lap = 0
while taxis:
    number = randrange(len(taxis))
    taxi = taxis[number]
    try:
        status = taxi.send(time_lap)
    except StopIteration:
        del taxis[number] # find a good way to handle taxi drop-off
    else:
        print_status(status)
    time_lap += randrange(RANDRANGESTART, RANDRANGEEND)
print('---End of simulation---')
