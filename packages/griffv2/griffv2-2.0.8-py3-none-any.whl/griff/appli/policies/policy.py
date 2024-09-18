from abc import ABC, abstractmethod
from typing import TypeVar, List, Any, Generic

from griff.utils.errors import BaseError

S = TypeVar("S", bound=Any)
E = TypeVar("E", bound=BaseError)


class BasePolicyResult(Generic[S, E], ABC):
    @property
    @abstractmethod
    def is_success(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_failure(self) -> bool:
        ...

    @property
    @abstractmethod
    def result(self) -> S:
        ...

    @property
    @abstractmethod
    def error(self) -> E:
        ...


class PolicyResultSuccess(BasePolicyResult[S, E]):
    def __init__(self, result: S):
        self._result = result

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def result(self) -> S:
        return self._result

    @property
    def error(self) -> E:
        raise RuntimeError("result is success, get result instead")


class PolicyResultFailure(BasePolicyResult[S, E]):
    def __init__(self, result: E):
        self._result = result

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True

    @property
    def result(self) -> S:
        raise RuntimeError("result has failed, get error instead")

    @property
    def error(self) -> E:
        return self._result


PolicyResult = PolicyResultSuccess[S, E] | PolicyResultFailure[S, E]


class Policy(ABC):
    @abstractmethod
    async def verify(self, data: Any) -> PolicyResult:
        ...


async def verify_policies(data: Any, policies: List[Policy]) -> PolicyResult:
    # todofsc: faire des tests
    if not policies:
        return PolicyResultSuccess(data)

    result = data
    for policy in policies:
        result = await policy.verify(data)
        if result.is_failure:
            return result
        data = result.result
    return result
