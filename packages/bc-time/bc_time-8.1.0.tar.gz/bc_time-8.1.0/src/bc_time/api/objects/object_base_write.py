from bc_time.api.objects.object_base_create import ObjectBaseCreate
from bc_time.api.objects.object_base_update import ObjectBaseUpdate

class ObjectBaseWrite(ObjectBaseCreate, ObjectBaseUpdate):
    pass