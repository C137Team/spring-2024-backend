import enum
from datetime import datetime

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped

from random_coffee.infrastructure.models import BuiltinSubtypeMixin
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class IdentificationSessionStatusEnum(enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    EXPIRED = 'EXPIRED'  # currently not supports


class IdentificationRequestId(int, BuiltinSubtypeMixin):
    pass


class IdentificationSession(BaseRelationalEntity):
    __tablename__ = 'identification_session'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"))
    confirmation_code_hash: Mapped[str] = mapped_column()
    status: Mapped[IdentificationSessionStatusEnum] = mapped_column(
        Enum(IdentificationSessionStatusEnum),
        default=IdentificationSessionStatusEnum.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
