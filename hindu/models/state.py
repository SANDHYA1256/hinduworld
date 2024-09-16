import uuid
from django.db import models

from .country import Country




class State(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    shortname = models.CharField(db_column='shortname', max_length=45)
    # capital = models.CharField(db_column='capital', max_length=45, blank=True, null=True)
    # language = models.CharField(db_column='languagge', max_length=45, blank=True, null=True)  
    desc = models.CharField(db_column='desc', max_length=250, blank=True, null=True) 
    country= models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    # country_id = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    type=models.CharField(db_column='type', max_length=30, choices=[('STATE','STATE')],default='STATE',blank=True)


    class Meta:
        managed = False
        db_table = 'state'