class Field:
    def __init__(self, name, constructor):
        if not callable(constructor) or constructor is type(None):
            raise TypeError(f'{constructor!r} is not a callable')
        self._name = name
        self._constructor = constructor

    def __set__(self, instance, value):
        # using 'isinstance' is another type testing method
        # but 'callable(value)' forces to copy original data
        # and transforms them into callable type
        name, constructor = self._name, self._constructor
        try:
            instance.__dict__[name] = constructor() if value is ... else \
                                      constructor(value)
        except (TypeError, ValueError):
            raise ValueError(f"'{value}' is not compatible with {constructor.__name__}")


class Checked:
    def __init_subclass__(subclass):
        # automatically implement descriptor
        super().__init_subclass__()
        for name, constructor in subclass.get_fields().items():
            setattr(subclass, name, Field(name, constructor))

    def __init__(self, **kwargs):
        for field in self.get_fields():
            value = kwargs.pop(field, ...)
            setattr(self, field, value)
        if kwargs:
            self.wrong_fields(AttributeError, kwargs.keys())

    def __setattr__(self, key, value):
        if key not in self.get_fields():
            self.wrong_fields(AttributeError, (key, ))
        cls = type(self)
        cls.__dict__[key].__set__(self, value)

    def __repr__(self):
        cls_name = type(self).__name__
        fields = (f'{key}={self.__dict__[key]}' for key in self.get_fields())
        fields = ', '.join(fields)
        return f'{cls_name}({fields})'

    @classmethod
    def get_fields(cls):
        return cls.__annotations__

    def wrong_fields(self, error_type, extra_fields):
        cls_name = type(self).__name__
        extra_s = '' if len(extra_fields) == 1 else 's'
        self_s = '' if len(self.get_fields()) == 1 else 's'
        extra_fields = ', '.join(extra_fields)
        self_fields = ', '.join(self.get_fields().keys())
        msg = f"'{cls_name}' has no attribute{extra_s} '{extra_fields}'. " +\
              f"{cls_name}'s attribute{self_s}: {self_fields}"
        raise error_type(msg)


class Test(Checked):
    name: str
    age: int
    height: float
    address: str


t = Test(name='jason')
print(t)
t.age = 45
print(t)
t.height = 'aa'
print(t)
