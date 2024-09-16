from django.db import models
from .category import Category
import uuid

class SubCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    desc=models.CharField(db_column='desc',max_length=10000)
    category_id = models.ForeignKey(Category,on_delete=models.SET_NULL,db_column='category_id', null=True, blank=True)

    



    class Meta:
        managed=False
        db_table = 'organization_sub_category'