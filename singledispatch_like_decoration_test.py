from pprint import pprint
from collections import abc


class Deco:
    def __init__(self, func):
        self._func = func
        self._name = func.__name__
        self._funcs = {self._name: func} 

    def speak(self):
        print('-----It works-----')

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError('key should be a string')
        return self._funcs[key]

    def __repr__(self):
        return f'{self._name}({self._funcs})'

    def register(self, func):
        self._funcs[func.__name__] = func


@Deco
def add(x, y):
    return x + y


@add.register
def sub(x, y):
    return x - y


t = add
print(t)
print()
pprint(locals())
