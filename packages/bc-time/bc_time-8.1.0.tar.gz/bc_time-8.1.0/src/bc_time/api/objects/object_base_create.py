from bc_time.api.objects.base import Base
from bc_time.api.constants.api import Api as ApiConstants

class ObjectBaseCreate(Base):
    def create(self, payload: dict) -> dict:
        return self.api.create(
            content_type_id=self._content_type_id,
            payload=payload
        )

    def create_many(self, payloads: dict) -> dict:
        return self.api.create(
            content_type_id=self._content_type_id,
            payload=payloads,
            content_uid=ApiConstants.UID_POST_MANY
        )