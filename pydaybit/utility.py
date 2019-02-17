import inspect
from decimal import Decimal


def optional(*optional_args):
    def args_deco(func):
        def decorated(*args, **kwargs):
            func_args = inspect.getfullargspec(func).args
            if not set(kwargs.keys()) - set(func_args) <= set(optional_args):
                keys = str(set(kwargs.keys()) - set(optional_args) - set(func_args))
                raise TypeError(
                    '{}() got unexpected keyword argument(s). {}'.format(func.__name__,
                                                                         keys[1:-1]))
            return func(*args, **kwargs)

        return decorated

    return args_deco


def to_str(d):
    if isinstance(d, Decimal):
        decimal_tuple = d.as_tuple()
        exponent = decimal_tuple.exponent

        if exponent < 0:
            formatter = f'%.{-exponent}f'
            return formatter % d
        return str(d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize())
    return str(d)
