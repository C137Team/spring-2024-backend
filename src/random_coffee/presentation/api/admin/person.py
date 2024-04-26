from sqladmin import ModelView

from random_coffee.domain.core.models.person.person import Person


class PersonAdmin(ModelView, model=Person):
    column_list = [
        Person.id,
        Person.full_name,
        Person.account_id,
        Person.telegram_account_id,
    ]
