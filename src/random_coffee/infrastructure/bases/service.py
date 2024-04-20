from di.dependent import Injectable


class BaseService(Injectable):
    def __init_subclass__(cls, **kwargs):
        kwargs.setdefault('scope', 'request')
        return super().__init_subclass__(**kwargs)
