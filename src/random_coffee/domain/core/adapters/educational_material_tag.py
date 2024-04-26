from typing import Iterable

from numpy import select

from random_coffee.domain.core.models.education.educational_material import EducationalMaterial
from random_coffee.domain.core.models.education.educational_material_tag import EducationalMaterialTag
from random_coffee.domain.core.models.education.tag import Tag
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllEducationalMaterialTag(BaseEntityRepo[EducationalMaterialTag]):
    async def create_link(
            self,
            edm: EducationalMaterial,
            tag: Tag
    ):
        obj = EducationalMaterialTag(
            educational_material_id=edm.id,
            tag_id=tag.id
        )
        await self.save(obj)
        return obj
