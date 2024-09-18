from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

from griff.appli.event.event_handler import EventHandler
from griff.infra.persistence.dict_domain_persistence import DictDomainPersistence
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase

CH = TypeVar("CH", bound=EventHandler)


class EventHandlerTestCase(Generic[CH], RuntimeTestMixin, TestCase, ABC):
    handler: CH

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().event_test_handler()

    def setup_method(self):
        super().setup_method()
        self.handler = self.get_injected(self.handler_class)

    @staticmethod
    async def prepare_success_resultset(persistence: DictDomainPersistence):
        return {"persistence": await persistence.run_query("list_all")}

    @property
    @abstractmethod
    def handler_class(self) -> Type[CH]:
        pass
