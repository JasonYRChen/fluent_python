"""
    This is a built-in property class emulation. This only demonstrates
    getter and setter and leave out the rests in the original property.
    One bizarre behavior in original property is that when the name of 
    getter and setter are different, the property of the getter cannot
    include setter. Instead, the setter build a new property in name of
    the setter's name. In my version Property, I correct this problem.
"""


class Property:
    def __init__(self, getter=None, setter=None):
        self._getter = getter
        self._setter = setter
        self._name = getter.__name__

    def __get__(self, instance, owner):
        if self._getter is None:
            raise AttributeError(f'Property of {owner} object has no getter')
        return self._getter(instance)

    def __set__(self, instance, value):
        if self._setter is None:
            raise AttributeError(f"Property '{self._name}' of '{type(instance).__name__}' object has no setter")
        self._setter(instance, value)

    def setter(self, method):
        self._setter = method
        return self


class Test:
    def __init__(self):
        self._value = 13

    @Property
    def value(self):
        return self._value

    @value.setter
    def value_setter(self, value):
        self._value = value


t = Test()
print(Test.__dict__)
print(t.value)
print(Test.__dict__)
t.value = 100
print(t.value)
print(Test.__dict__)
