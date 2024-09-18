from abc import ABC
from typing import Self

from griff.domain.common_types import Entity
from griff.infra.repository.repository import Repository
from griff.services.date.fake_date_service import FakeDateService
from griff.services.uniqid.generator.fake_uniqid_generator import FakeUniqIdGenerator
from griff.services.uniqid.uniqid_service import UniqIdService


class DataTestFactory(ABC):
    def __init__(self, start_id=1):
        self.uniqid_service = UniqIdService(FakeUniqIdGenerator(start_id))
        self.date_service = FakeDateService()

    async def persist(
        self, repository: Repository, data: list[Entity] | Entity
    ) -> Self:
        if isinstance(data, list) is False:
            await repository.save(data)
            return self

        for a in data:
            await repository.save(a)
        return self
