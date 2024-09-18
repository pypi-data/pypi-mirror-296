from ulid import ULID

from griff.services.uniqid.generator.uniqid_generator import (
    UniqIdGenerator,
)


class UlidUniqIdGenerator(UniqIdGenerator):
    def next_id(self) -> str:
        return str(ULID())
