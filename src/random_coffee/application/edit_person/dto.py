from dataclasses import dataclass

from random_coffee.application.common.dto import PersonDTO


@dataclass
class EditPersonDTO:
    entity_id: int | None = None
    set_full_name: str | None = None
    set_age: int | None = None
    set_post: str | None = None
    set_description: str | None = None


@dataclass
class EditPersonResponseDTO:
    entity: PersonDTO
