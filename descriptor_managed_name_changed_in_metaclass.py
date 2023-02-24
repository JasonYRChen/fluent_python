class NameProperty:
    def __init__(self):
        self._managed_name = None

    def __set__(self, instance, value):
        if not value.strip():
            raise ValueError(f"'{self._managed_name}' cannot be empty")
        instance.__dict__[self._managed_name] = value

class NameMeta(type):
    def __new__(cls_meta, cls_name, bases, dicts):
        for name, attr in dicts.items():
            if isinstance(attr, NameProperty):
                #print(f'{attr._managed_name}')
                attr._managed_name = name
        return super().__new__(cls_meta, cls_name, bases, dicts)


class NameBase(metaclass=NameMeta):
    pass


class Name(NameBase):
    first_name = NameProperty()
    last_name = NameProperty()

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        cls_name = type(self).__name__
        name = f"first={self.first_name}, last={self.last_name}"
        return f"{cls_name}({name})"


person = Name('j', 'c')
#person = Name('j', '')
print(person)
person.first_name = 'ian'
#person.first_name = ''
#person.last_name = ''
print(person)
