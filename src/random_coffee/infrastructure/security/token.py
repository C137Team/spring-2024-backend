from typing import Optional, Union, AbstractSet

from datetime import timedelta, datetime

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, root_validator, ValidationError, validator

from random_coffee.infrastructure.config import environment
from random_coffee.infrastructure.security.scopes import AccessScopeEnum


ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class Sub(BaseModel):
    # serialized format. example: key:value
    # note that this argument is first
    sub: Optional[str] = None

    # at the rest goes application-specific aliases
    login: Optional[str] = None

    @classmethod
    def _build_from_sub(cls, sub_string):
        items = sub_string.split(':')

        if len(items) != 2:
            raise ValueError("Sub string must contain two values, separated by colon")

        key, value = items

        if key == "sub":
            raise ValueError("Identifier can't be named as `sub`")

        return {key: value}

    @root_validator(skip_on_failure=True)
    def check_identifier(cls, data):
        if data.get("sub") is not None:
            return cls._build_from_sub(data.get("sub"))

        identifiers_count = sum([i is None for i in data.values()])

        if identifiers_count == 0:
            raise ValueError("JWT Subject must have at leas one identifier")
        elif identifiers_count == 1:
            pass
        else:
            raise ValueError("JWT Subject support only single identifier")

        return data

    def as_string(self):
        key, value = next(iter(self.dict(exclude_none=True).items()))
        return f'{key}:{value}'


class CreateTokenData(BaseModel):
    sub: Union[Sub, str]
    scopes: list[str] = []

    @validator("sub")
    def check_sub(cls, value):
        if isinstance(value, str):
            return Sub(sub=value)
        else:
            return value

    @property
    def access_scopes(self) -> AbstractSet[AccessScopeEnum]:
        return set(map(AccessScopeEnum, self.scopes))


class TokenData(CreateTokenData):
    exp: datetime


class PreparedTokenData(BaseModel):
    sub: str
    exp: datetime
    scopes: list[str]


class InvalidCredentialsError(Exception):
    pass


def create_access_token(create_payload: CreateTokenData, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=environment.jwt_expire_minutes)

    expire = datetime.utcnow() + expires_delta
    payload = TokenData(
        sub=create_payload.sub,
        exp=expire,
        scopes=create_payload.scopes,
    )
    prepared_payload = PreparedTokenData(
        sub=payload.sub.as_string(),
        exp=payload.exp,
        scopes=payload.scopes,
    )
    to_encode = prepared_payload.dict()
    encoded_jwt = jwt.encode(to_encode, environment.jwt_secret, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    try:
        raw_payload = jwt.decode(token, environment.jwt_secret, algorithms=[ALGORITHM])
    except JWTError:
        raise InvalidCredentialsError()

    try:
        payload = TokenData.model_validate(raw_payload)
    except ValidationError:
        raise InvalidCredentialsError()

    return payload
