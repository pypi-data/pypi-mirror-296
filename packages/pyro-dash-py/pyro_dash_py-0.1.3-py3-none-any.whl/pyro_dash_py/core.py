from enum import Enum
from functools import wraps
from typing import Callable, TypeVar, Any


POST = "POST"
GET = "GET"
PUT = "PUT"
DEL = "DELETE"


class PyroJobTypes(Enum):
    WILDEST = "wildest"
    FSIM = "fsim"
    FUELSCAPE = "fuelscape"
    LIABILITY_RISK = "liability_risk"


# TODO: implement PyroApiError ?
class ResourceNotAvailableError(Exception):
    pass


T = TypeVar("T", bound=Callable[..., Any])


def require_resource(func: T) -> T:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._resource is None:
            raise ResourceNotAvailableError(
                "_resource property must be set to perform this operation"
            )
        return func(self, *args, **kwargs)

    return wrapper  # pyright: ignore
