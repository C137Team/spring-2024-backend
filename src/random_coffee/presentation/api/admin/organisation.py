from sqladmin import ModelView

from random_coffee.domain.core.models import (
    Organisation,
)


class OrganisationAdmin(ModelView, model=Organisation):
    column_list = [
        Organisation.id,
        Organisation.title,
        Organisation.email_domain,
    ]
