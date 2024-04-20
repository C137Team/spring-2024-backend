import math
from typing import Iterable


def get_by_id(collection: Iterable, id_: int):
    return get_by_field(collection, "id", id_)


def get_by_field(collection: Iterable, field: str, value):
    for i in collection:
        if getattr(i, field) == value:
            return i
    return None


async def get_all_by_field(collection: set, field: str, value):
    result = []
    for i in collection:
        if getattr(i, field) == value:
            result.append(i)
    return result


def evaluate_kpi(base: int, product: int) -> float:
    if not base or not product:
        return 0.
    return product * 100 / base
