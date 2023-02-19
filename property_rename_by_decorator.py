import abc

NAME_TEMPLATE = 'qualified#'


class Qualification(abc.ABC):
    instance_count = 0

    def __init__(self):
        cls = type(self)
        self.name = NAME_TEMPLATE + str(cls.instance_count)
        cls.instance_count += 1

    @abc.abstractmethod
    def __set__(self, instance, value):
        """ Implement criteria for value"""


class Age(Qualification):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Age should not smaller than 0')
        instance.__dict__[self.name] = value


class Name(Qualification):
    def __set__(self, instance, value):
        if not value.strip():
            raise ValueError('Name should not be blank')
        instance.__dict__[self.name] = value


def property_rename(base_class=Qualification, attr='name'):
    def inner(cls):
        for name, descriptor in cls.__dict__.items():
            if isinstance(descriptor, base_class):
                descriptor.__dict__[attr] = name
        return cls
    return inner


@property_rename() # hashtag this line and see the effect of the decorator
class People:
    age = Age()
    age2 = Age()
    name = Name()
    name2 = Name()

    def __init__(self, name, name2, age, age2):
        self.age = age
        self.age2 = age2
        self.name = name
        self.name2 = name2

    def __repr__(self):
        cls_name = type(self).__name__
        attrs = (f'{k}={v}' for k, v in self.__dict__.items())
        attrs = ', '.join(attrs)
        return f'{cls_name}({attrs})'


print(People.age.name, People.age2.name, People.name.name, People.name2.name)
p = People('j', 'c', 34, 12)
print(p)
