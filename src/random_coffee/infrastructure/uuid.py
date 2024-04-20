from uuid import UUID


def is_valid_uuid(text: str, version: int = 4):
    try:
        UUID(text, version=version)
    except ValueError:
        return False
    else:
        return True
