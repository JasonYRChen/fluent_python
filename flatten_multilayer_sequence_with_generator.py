"""
    This is a generator to flatten a sequence (or to be specific, an iteranble)
    with muliple layers, i.e. sequences inside sequences. The sequence is actually
    check against abc.Iterable instead of abc.Sequence, since abc.Iterable implements
    __subclasshook__ method with '__iter__' structural type check, but abc.Sequence
    does not implement the counterpart with only registered objects.

    As a result, this generator will fail on object without implementing '__iter__'
    method but still being an iterable, which can be iterated in loops with only
    '__getitem__' method exists. 
"""

from collections.abc import Iterable


def deepgen(obj):
    if isinstance(obj, Iterable):
        for sub_obj in obj:
            yield from deepgen(sub_obj)
    else:
        yield obj


a = [[[0, 1], [2, [3, 4]],5], [6, [7, [8, [9]]]]]
for i in deepgen(a):
    print(i)
