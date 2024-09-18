from bc_time.api.objects.base import Base
from bc_time.api.constants.api import Api as ApiConstants

class ObjectBaseUpdate(Base):
    def update(self, content_uid, payload: dict) -> dict:
        return self.api.update(
            content_type_id=self._content_type_id,
            content_uid=content_uid,
            payload=payload
        )

    def update_many(self, payloads: dict) -> dict:
        return self.api.update(
            content_type_id=self._content_type_id,
            content_uid=ApiConstants.UID_POST_MANY,
            payload=payloads
        )