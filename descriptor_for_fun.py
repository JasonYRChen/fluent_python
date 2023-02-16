class Fun:
    def __init__(self):
        self._sum = 0

    def __set__(self, instance, args):
        cls = type(instance)
        original_repr = cls.__repr__
        name = original_repr(instance)
        self._sum = sum(args)
        cls.__repr__ = lambda x: f'{name} now has a sum of {self._sum}.'
        print(instance)
        cls.__repr__ = original_repr

    def __get__(self, instance, owner):
        print(f'{instance} has sum of {self._sum} for now')
        return self._sum


class Test:
    fun = Fun()

    def __repr__(self):
        return 'Test obj'


t = Test()
r = t.fun
print(r)
t.fun = (1, 2, 3, 4, 5)
print(t)
print(t.fun)
