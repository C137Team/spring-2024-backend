from fastapi.security import OAuth2PasswordBearer


TOKEN_URL = '/v1/token'
SCOPES = {
}


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=TOKEN_URL,
    scopes=SCOPES,
)
