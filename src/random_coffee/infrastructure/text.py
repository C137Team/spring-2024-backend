from typing import Literal

from transliterate import translit


EN_KB = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?!@#$%^&"""
RU_KB = """ёйцукенгшщзхъфывапролджэячсмитьбю.ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,!"№;%:?"""

EN_TO_RU = str.maketrans(EN_KB, RU_KB)
RU_TO_EN = str.maketrans(RU_KB, EN_KB)


def normalize_text(
        text: str,
        as_speech: bool = True,
        language: Literal['ru', 'en', 'any'] = 'any',
):
    if language == 'ru':
        text = text.translate(EN_TO_RU)
    elif language == 'en':
        text = text.translate(RU_TO_EN)
    elif language == 'any':
        pass
    else:
        raise TypeError(language)

    if as_speech:
        text = (text
                .lower()
                .strip())

    return text


def to_latin(text: str) -> str:
    result = translit(text, reversed=True)
    result = result.replace("'", '')
    return result


__all__ = [
    "normalize_text",
    "to_latin",
]
