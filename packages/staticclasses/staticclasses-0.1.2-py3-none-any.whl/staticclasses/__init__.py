class staticmeta(type):
    def __call__(cls, *args, **kwargs):
        e = "Cannot instantiate static class %r!"
        e %= cls.__name__
        raise TypeError(e)


class staticclass(metaclass=staticmeta): ...
