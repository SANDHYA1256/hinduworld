
from django.db import models
from ..enums.user_status_enum import UserStatus
from ..enums import MemberStatus
import uuid
from django.utils import timezone
from ..utils import send_email, generate_otp, validate_email, send_sms
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from ..enums.user_type_enum import UserType
from ..enums import TrainingType


class Register(AbstractUser):
    id = models.CharField(db_column='id', primary_key=True, max_length=45,default=uuid.uuid1, editable=False)
    full_name = models.CharField(db_column='full_name', max_length=200)
    # name = models.CharField(db_column='name', max_length=200)
    dob = models.DateField(null=True,blank=True)
    contact_number = models.CharField(db_column='contact_number', max_length=10, null=True, blank=True)
    father_name = models.CharField(db_column='father_name', max_length=200, null=True, blank=True)
    profile_pic = models.TextField(db_column='profile_pic', null=True, blank=True)
    is_member = models.CharField(db_column='is_member', max_length=50, choices=[(e.name, e.value) for e in MemberStatus], default=MemberStatus.FALSE.value)
    verification_otp = models.CharField(db_column='verification_otp', max_length=6, null=True, blank=True)
    verification_otp_created_time = models.DateTimeField(db_column='verification_otp_created_time', null=True)
    verification_otp_resend_count = models.IntegerField(default=0, db_column='verification_otp_resend_count')
    status = models.CharField(db_column='status', max_length=50, choices=[(e.name, e.value) for e in UserStatus], default=UserStatus.CREATED.value)
    training_type = models.CharField(db_column='training_type',max_length=10,choices=[(e.value, e.value) for e in TrainingType],default=TrainingType.OFFLINE.value)  
    # image = models.TextField(db_column='image',null=True)
    # video = models.TextField(db_column='video',null=True)
    certificate = models.TextField(db_column='certificate',null=True)
    # map_location = models.TextField(db_column='map_location',null=True)
    experience = models.CharField(db_column='experience', max_length=50,null=True)
    achievements = models.CharField(db_column='achievements',max_length=500,null=True,blank=True)
    email = models.EmailField(db_column='email',max_length=50,null=True,blank=True)
    user_type = models.CharField(db_column='user_type',max_length=45, choices=[(e.name, e.value)for e in UserType], default=UserType.MEMBER.value)
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='custom_user_groups',
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     verbose_name='groups',
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='custom_user_permissions',
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions',
    # )
    class Meta:
        db_table = "user"
    def __str__(self):
        return self.username