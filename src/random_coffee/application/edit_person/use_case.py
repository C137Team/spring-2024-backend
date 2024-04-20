from random_coffee.domain.core.services import AuthenticationService

from random_coffee.infrastructure.bases.use_case import UseCase
from random_coffee.infrastructure.security.token import create_access_token, CreateTokenData, Sub

from .dto import EditPersonDTO, EditPersonResponseDTO
from ..common.dto import PersonDTO
from ...domain.core.adapters import AllPersons


class EditPerson(UseCase[EditPersonDTO, EditPersonResponseDTO]):
    # noinspection PyProtocol
    def __init__(
            self,
            authentication_service: AuthenticationService,
            all_persons: AllPersons,
    ):
        self.all_persons = all_persons
        self.authentication_service = authentication_service

    async def __call__(self, payload: EditPersonDTO) -> EditPersonResponseDTO:
        person = await self.all_persons.with_id(payload.person_id)
        if payload.set_age is not None:
            person.age = payload.set_age
        if payload.set_post is not None:
            person.post = payload.set_post
        if payload.set_description is not None:
            person.description = payload.set_description
        if payload.set_full_name is not None:
            person.full_name = payload.set_full_name
        await self.all_persons.save(person)

        return EditPersonResponseDTO(
            entity=await PersonDTO.from_model(person),
        )
