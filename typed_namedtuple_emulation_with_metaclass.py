"""
    Most of the tricks in 'MetaNamedTuple' can be done without metaclass,
    except for '__slots__'. This is why metaclass is the only choice for 
    the case.
"""


class MetaNamedTuple(type):
    def __new__(cls_meta, cls_name, bases, cls_dict):
        attributes = {}

        def __init__(self, **kwargs):
            for key, value in attributes.items():
                setattr(self, key, kwargs.pop(key, value))
            if kwargs:
                keys = ', '.join(k for k in kwargs)
                cls_name = type(self).__name__
                msg = f'{cls_name} does not have attribute {keys}.'
                raise AttributeError(f'{msg}')

        def __repr__(self):
            attrs = ', '.join(f'{k}={getattr(self, k)}' for k in self.__slots__)
            cls_name = type(self).__name__
            return f'{cls_name}({attrs})'

        new_cls_dict = {'__slots__': [], 
                         '__init__': __init__, 
                         '__repr__': __repr__}
        for key, attr in cls_dict.items():
            if key in new_cls_dict:
                msg = f'Method conflict: cannot build {key}'
                raise AttributeError(f'{msg}')
            if key.startswith('__') and key.endswith('__'):
                if key == '__annotations__':
                    for key, constructor in attr.items():
                        attributes[key] = constructor()
                        new_cls_dict['__slots__'].append(key)
                else:
                    new_cls_dict[key] = attr
            else:
                attributes[key] = attr
                new_cls_dict['__slots__'].append(key)

        return super().__new__(cls_meta, cls_name, bases, new_cls_dict)


class Test(metaclass=MetaNamedTuple):
    name: str
    age: int
    address = None

    def __set__(self):
        pass


t = Test(name='j')
print(t)
