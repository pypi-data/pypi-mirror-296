from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

from griff.appli.command.command_handler import CommandHandler, CommandResponse
from griff.infra.repository.repository import Repository
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase

CH = TypeVar("CH", bound=CommandHandler)


class CommandHandlerTestCase(Generic[CH], RuntimeTestMixin, TestCase, ABC):
    handler: CH

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().command_test_handler()

    def setup_method(self):
        super().setup_method()
        self.handler = self.get_injected(self.handler_class)

    @staticmethod
    async def prepare_success_resultset(
        response: CommandResponse, repository: Repository
    ):
        results = await repository._persistence.run_query("list_all")
        persistence = (
            [repository._convert_to_hydratation_dict(r) for r in results if r]
            if results
            else None
        )
        return {"response": response.model_dump(), "persistence": persistence}

    @property
    @abstractmethod
    def handler_class(self) -> Type[CH]:
        pass
