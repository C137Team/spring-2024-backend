import secrets

from starlette.requests import Request
from starlette.responses import Response

from sqladmin.authentication import AuthenticationBackend

from random_coffee.infrastructure.config import environment


class SQLAdminAuth(AuthenticationBackend):
    def _validate_credentials(self, username: str, password: str):
        is_username_correct = secrets.compare_digest(
            username.encode(),
            environment.admin_username.encode()
        )
        is_password_correct = secrets.compare_digest(
            password.encode(),
            environment.admin_password.encode()
        )
        return is_username_correct and is_password_correct

    async def login(self, request: Request) -> bool:
        form = await request.form()
        is_authorized = self._validate_credentials(
            username=form.get("username"),
            password=form.get("password"),
        )
        if is_authorized:
            request.session["authorized"] = True
        return is_authorized

    async def authenticate(self, request: Request) -> Response | bool:
        return request.session.get("authorized", False)

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
