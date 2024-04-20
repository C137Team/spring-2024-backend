from base64 import urlsafe_b64encode, urlsafe_b64decode

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    def model_dump_base64url(self, by_alias: bool = True):
        json = self.model_dump_json(by_alias=by_alias, exclude_none=True)
        blob = json.encode('ascii')
        return urlsafe_b64encode(blob)

    @classmethod
    def model_validate_base64url(cls, string: str):
        return cls.model_validate_json(urlsafe_b64decode(string).decode('ascii'))
