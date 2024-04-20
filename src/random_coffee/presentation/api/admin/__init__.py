from sqladmin import Admin

from .person import PersonAdmin
from .notification_destination import NotificationDestinationAdmin


def include_admin_views(admin_app: Admin):
    admin_app.add_view(PersonAdmin)
    admin_app.add_view(NotificationDestinationAdmin)
