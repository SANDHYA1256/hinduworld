    
import uuid
from django.db import models


class EventCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45)
    desc = models.CharField(db_column='desc', blank=True, null=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    pic = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'Event_category'

