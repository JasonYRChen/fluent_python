"""
    Here 'delegate' and 'delegate2' are acting pipelines. Each of which can do
    distinct works independent of the other. The common point is to pass data
    back and forth.
"""

def average():
    total = 0
    avg = 0
    count = 0
    while True:
        avg = yield avg
        if avg is StopIteration:
            break
        total += avg
        count += 1
        avg = total / count
    return avg, count


def delegate():
    result = yield from delegate2()
    print(f'---in delegate: {result}---')
    return result


def delegate2():
    result = yield from average()
    print(f'---in delegate2: {result}---')
    return result


d = delegate()
for i in [None, 1, 3, 5, StopIteration]:
    try:
        current_avg = d.send(i)
    except StopIteration as si:
        print(f'final: {si.value}')
    else:
        print(f'current average: {current_avg}')
