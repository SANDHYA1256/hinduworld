from django.db import models
import uuid
from django.core.validators import URLValidator, RegexValidator, MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import re
from ..models import *
from .district import District
from .category import Category
from .sub_category import SubCategory
from ..enums import status,GeoSite
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from .user import Register






class Organization(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    organization_name = models.CharField(max_length=200,)
    est_by = models.CharField(max_length=100)
    chairman = models.CharField(max_length=100)
    desc = models.TextField()
    est_date = models.CharField(max_length=50)
    reg_id = models.CharField(max_length=200)
    location = models.TextField()
    web_url = models.URLField()
    org_detail = models.TextField()
    mission = models.TextField()
    org_images = models.TextField()
    org_logo = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[(e.name, e.value) for e in status], default=status.PENDING.value)
    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.DISTRICT.value)
    object_id = models.ForeignKey(District, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='organization')
    organization_members = models.CharField(max_length=10000, null=True)
    sub_category_id = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, db_column='sub_category_id', null=True, blank=True)

    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, db_column='category_id', null=True, blank=True)
    govt_id_proof = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Register, on_delete=models.SET_NULL, related_name='Organization', null=True)


    class Meta:
        managed = False
        db_table = "organization"