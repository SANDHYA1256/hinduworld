import uuid
from django.db import models
from .state import State





class District(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45)  
    shortname = models.CharField(db_column='shortname', max_length=45)  
    headquarters = models.CharField(db_column='headquarters', max_length=45, blank=True, null=True)  
    desc = models.CharField(db_column='desc', max_length=250, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    cityname =models.CharField(max_length=200)
    created_at = models.CharField(max_length = 200)
    type=models.CharField(db_column='type', max_length=30, choices=[('DISTRICT','DISTRICT'),('CITY','CITY')],default='DISTRICT',blank=True)

    class Meta:
        managed = False
        db_table = 'district'
