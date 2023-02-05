from dataclasses import dataclass


def class_deco(cls):
    fields = cls.__annotations__.keys()

    class inner_class(cls):
        def __init__(self, *args):
            for field, arg in zip(fields, args):
                self.__dict__[field] = arg

        def __repr__(self):
            items = {k: self.__dict__[k] for k in fields}
            return f'{cls.__name__}({items})'

    inner_class.__name__ = cls.__name__
    return inner_class


@class_deco
class test:
    value: int
    name: str


t = test(2, 'a')
print(t)
print(t.__class__.__name__)
