from di.dependent import Injectable

from .interface import Notifier as _NonInjectableNotifier
from .builder import build_notifier


class Notifier(_NonInjectableNotifier, Injectable, call=build_notifier, scope='request'):
    pass
