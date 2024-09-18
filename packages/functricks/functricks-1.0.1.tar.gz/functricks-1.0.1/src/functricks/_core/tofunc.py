import functools

__all__ = ["tofunc"]


def tofunc(old, /):
    def new(*args, **kwargs):
        return old(*args, **kwargs)

    try:
        new = functools.wraps(old)(new)
    except:
        pass
    return new
