from sqladmin import ModelView

from random_coffee.domain.core.models import NotificationDestination


class NotificationDestinationAdmin(ModelView, model=NotificationDestination):
    column_list = [
        NotificationDestination.id,
        NotificationDestination.notifier_backend,
        NotificationDestination.internal_identifier,
    ]
