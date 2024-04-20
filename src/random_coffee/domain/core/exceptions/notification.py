from .base import DomainError


class NotificationError(DomainError):
    pass


class PersonHasNoNotificationDestinations(NotificationError):
    def __init__(self, person_id):
        self.person_id = person_id


class CantReportInternalError(NotificationError):
    pass
