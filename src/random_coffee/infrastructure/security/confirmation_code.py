import random

from passlib.context import CryptContext


ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_confirmation_code():
    return str(random.randint(100_000, 999_999))


def get_confirmation_code_hash(code):
    return pwd_context.hash(code)


def verify_confirmation_code(plain_code, hashed_code) -> bool:
    return pwd_context.verify(plain_code, hashed_code)
