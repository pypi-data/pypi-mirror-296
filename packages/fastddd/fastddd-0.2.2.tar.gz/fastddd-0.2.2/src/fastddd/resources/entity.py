import string
from datetime import datetime, timezone
import secrets
from uuid import uuid4
from pydantic import BaseModel, ConfigDict


class Entity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    __id_field: str = "id"

    def set_id_field(self, id_field: str):
        self.__id_field = id_field

        return self

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Entity):
            return False
        return getattr(self, self.__id_field) == getattr(value, self.__id_field)

    @classmethod
    def generate_id(cls):
        return str(uuid4())

    @classmethod
    def generate_secret(cls, size: int = 12, include_punctuation=False):
        pool = string.ascii_letters + string.digits
        if include_punctuation:
            pool += string.punctuation
        secret = "".join([secrets.choice(pool) for _ in range(size)])
        return secret

    @classmethod
    def now(cls) -> datetime:
        return datetime.now(timezone.utc)
