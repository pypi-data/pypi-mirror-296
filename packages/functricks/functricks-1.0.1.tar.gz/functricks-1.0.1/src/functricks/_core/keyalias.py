import functools

from .tofunc import tofunc

__all__ = ["keyalias"]


def keyalias(**kwargs):
    return functools.partial(decorator, **kwargs)


def propertyget(self, /, *, key):
    return self[key]


def propertyset(self, value, /, *, key):
    self[key] = value


def propertydel(self, /, *, key):
    del self[key]


def decorator(cls, /, **kwargs):
    raws = [propertyget, propertyset, propertydel]
    for alias, key in kwargs.items():
        bindings = list()
        for raw in raws:
            b = functools.partial(raw, key=key)
            b = tofunc(b)
            bindings.append(b)
        pro = property(*bindings)
        setattr(cls, alias, pro)
    return cls
