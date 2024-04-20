from random_coffee.infrastructure.repo import BaseEntityRepo
from random_coffee.domain.telegram.models import Document


class AllDocuments(BaseEntityRepo[Document]):
    pass
