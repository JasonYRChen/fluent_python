from functools import wraps


def wraps_(func_to_wrap):
    """ Self-made wraps to emulate functools.wraps """

    def deco(func_to_deco):
        func_to_deco.__doc__ = func_to_wrap.__doc__
        func_to_deco.__name__ = func_to_wrap.__name__
        return func_to_deco
    return deco


def deco(func):
    """ __doc__ of deco"""

    @wraps_(func) # swap 'wraps_' with 'wraps' and vice versa and see the result
    def inner(*args, **kwargs):
        """ __doc__ of inner"""
        print(f'-----Test of {func.__name__}-----')
        arg_list = [repr(arg) for arg in args]
        arg_list.extend(f'{k}={v}' for k, v in kwargs.items())
        arg_list = ' ,'.join(arg_list)
        print(f'{func.__name__}({arg_list}) = {func(*args, **kwargs)}')
        print(f'-----End of Test-----')
        return
    return inner


@deco
def add(a, b):
    """__doc__ of add"""
    return a + b


a = add
print(a.__name__)
print(a.__doc__)
a(3, 1)
