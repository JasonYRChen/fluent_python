class Field:
    """
        A descriptor for field management, compatible with __slots__.
        'managed_name' is the name of managed attribute in managed object,
        which may or may not be same as 'field_name' depending on the
        application: with __slots__ they should be different, otherwise
        it's up to user's decision. 'constructor' should be the class
        of managed attribute. If instance is passed instead, it will 
        automatically transform into its class.

        Arguments:
            field_name: str, the name to call by user
            managed_name: str, the name of managed name in managed object
            constructor: obj, used to form new value, i.e. int, str, list..
    """

    def __init__(self, field_name, managed_name, constructor):
        self._field_name = field_name
        self._managed_name = managed_name
        self._constructor = constructor if type(constructor) is type else type(constructor)

    def __set__(self, instance, value):
        name, constructor = self._managed_name, self._constructor
        try:
            value = constructor() if value is ... else constructor(value)
        except (TypeError, ValueError) as error:
            msg = f"'{constructor.__name__}' is not compatible with '{value}'"
            raise TypeError(msg) from error
        setattr(instance, name, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._managed_name)


class MetaChecked(type):
    """
        Unlike a simpler context of metaclass in fluent python (2nd), I
        do it on purpose to build both '__init__' and '__repr__' in 
        metaclass instead of in the class using this metaclass. The reason
        is that both methods need the data in 'cls_attr'. If those methods
        were built in the normal class, each method needs to search some-
        thing like 'cls_attr', respectively. The total searching time is
        triple than my version.
    """

    def __new__(cls_meta, cls_name, bases, cls_dict):
        # collect all attributes from annotations and expressions
        cls_attr = {k: v for k, v in cls_dict.items() 
                    if not k.startswith('__') and not k.endswith('__')}
        cls_attr.update(cls_dict.get('__annotations__', {}))

        def __init__(self, **kwargs):
            for key, value in cls_attr.items():
                value = ... if type(value) is type else value
                setattr(self, key, kwargs.pop(key, value))
            if kwargs: # unmatched attributes
                wrong_args = '(' + ', '.join(kwargs) + ')'
                right_args = '(' + ', '.join(cls_attr) + ')'
                cls_name = type(self).__name__
                msg = f"'{cls_name}' has no attribute {wrong_args}. " + \
                      f"Supported attribute: {right_args}."
                raise AttributeError(msg)

        def __repr__(self):
            cls_name = type(self).__name__
            attributes = (f"{k}={getattr(self, k)}" for k in cls_attr)
            attributes = ', '.join(attributes)
            return f"{cls_name}({attributes})"

        slots = [] # container to __slots__
        for key, attr in cls_attr.items():
            slots.append('_' + key)
            cls_dict[key] = Field(key, '_' + key, attr) # attributes protected by descriptor
                
        # methods to add to class
        additional_dict = {'__slots__': slots,
                           '__init__': __init__,
                           '__repr__': __repr__
                          }
        for name, method in additional_dict.items():
            if name in cls_dict:
                msg = f'Method conflict: cannot build {name}'
                raise AttributeError(f'{msg}')
            cls_dict[name] = method

        return super().__new__(cls_meta, cls_name, bases, cls_dict)


class Checked(metaclass=MetaChecked):
    pass
    #def __init__(self, **kwargs):
    #    pass

        


class Test(Checked):
    name = 'John Doe'
    age: int
    height = float
    address = ''


t = Test()
print(t)
t.age = 100
print(t)
