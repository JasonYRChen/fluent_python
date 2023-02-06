"""
    This package imitates contextlib.contextmanager behavior. The point is making
    a closure to accept generator to be used as context manager and arguments of
    that generator. Then initiate an instance with __enter__ and __exit__ methods.
"""


def wrap_(func_origin):
    def wrap(func_to_replace):
        func_to_replace.__name__ = func_origin.__name__
        func_to_replace.__doc__ = func_origin.__doc__
        return func_to_replace
    return wrap


def context_manager(func):
    @wrap_(func)
    def inner(*args, **kwargs):
        return ContextManager(func, args, kwargs)
    return inner


class ContextManager:
    def __init__(self, func, args, kwargs):
        self._gen = func(*args, **kwargs)

    def __enter__(self):
        return self._gen.send(None)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            next(self._gen)
        except StopIteration:
            pass


@context_manager
def basenumber(number):
    yield number
    print('---End of generator-type context---')


if __name__ == '__main__':
    with basenumber(5) as num:
        print(num * 2)

    with basenumber(203) as num:
        print(num - 3)
