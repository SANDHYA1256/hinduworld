# from django.db import models
# import uuid
# from django.core.validators import URLValidator, RegexValidator, MaxLengthValidator, MinLengthValidator
# from django.core.exceptions import ValidationError
# import re




# class continents(models.Model):
#     _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
#     name = models.CharField(db_column='name', max_length=45) 
#     # capital = models.CharField(db_column='capital', max_length=45, blank=True, null=True) 
#     alternativename = models.CharField(db_column='alternativename', max_length=45, blank=True, null=True) 
#     desc = models.CharField(db_column='desc', max_length=250, blank=True, null=True) 
#     type=models.CharField(db_column='type', max_length=30)
#     created_at = models.DateTimeField(db_column='created_at',auto_now_add=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         managed=False
#         db_table = 'continent'







# class Country(models.Model):
#     _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
#     name = models.CharField(db_column='name', max_length=45) 
#     capital = models.CharField(db_column='capital', max_length=45, blank=True, null=True) 
#     alternativename = models.CharField(db_column='alternativename', max_length=45, blank=True, null=True) 
#     desc = models.CharField(db_column='desc', max_length=250, blank=True, null=True) 
#     type=models.CharField(db_column='type', max_length=30, choices=[('COUNTRY','COUNTRY')],default='COUNTRY',blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     continent=models.ForeignKey(continents,on_delete=models.CASCADE,related_name='continent')

#     def __str__(self):
#         return self.name

#     class Meta:
#         managed=False
#         db_table = 'country'




# # class organization(models.Model):
# #     _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
# #     organization_name = models.CharField(max_length=200)
# #     est_by = models.CharField(max_length=100)
# #     chairman = models.CharField(max_length=100,db_column='chairman')
# #     desc = models.TextField(db_column='desc',blank=True, null=True)
# #     est_date = models.CharField(max_length=200,blank=True, null=True)
# #     reg_id = models.CharField(max_length=200)
# #     location = models.TextField()
# #     wed_url = models.URLField()
# #     org_detail= models.CharField(max_length=200)
# #     mission = models.TextField()
# #     org_images= models.TextField(null=True)
# #     country=models.ForeignKey(Country,on_delete=models.CASCADE,blank=True, null=True,related_name='country')

# #     class Meta:
# #         db_table = 'organization'




# class organization(models.Model):
#     _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
#     organization_name = models.CharField(
#         max_length=200,
#         validators=[
#             MaxLengthValidator(200),
#             MinLengthValidator(2, "Organization name cannot be empty")
#         ]
#     )
#     est_by = models.CharField(
#         max_length=100,
#         validators=[
#             MaxLengthValidator(100),
#             MinLengthValidator(1, "Establisher name cannot be empty")
#         ]
#     )
#     chairman = models.CharField(
#         max_length=100,
#         validators=[
#             MaxLengthValidator(100),
#             MinLengthValidator(1, "Chairman name cannot be empty")
#         ]
#     )
#     desc = models.TextField(
#         validators=[
#             MinLengthValidator(1, "Description cannot be empty")
#         ]
#     )
#     est_date = models.CharField(
#         max_length=50,
#         validators=[
#             MaxLengthValidator(50),
#             MinLengthValidator(1, "Establishment date cannot be empty"),
#             RegexValidator(
#                 regex=r'^\d{4}-\d{2}-\d{2}$',
#                 message="Date must be in YYYY-MM-DD format"
#             )
#         ]
#     )
#     reg_id = models.CharField(
#         max_length=200,
#         validators=[
#             MaxLengthValidator(200),
#             MinLengthValidator(1, "Registration ID cannot be empty")
#         ]
#     )
#     location = models.TextField(
#         validators=[
#             MinLengthValidator(1, "Location cannot be empty")
#         ]
#     )
#     web_url = models.URLField(
#         validators=[
#             URLValidator(message="Invalid URL format")
#         ]
#     )
#     org_detail = models.CharField(
#         max_length=200,
#         validators=[
#             MaxLengthValidator(200),
#             MinLengthValidator(1, "Organization detail cannot be empty")
#         ]
#     )
#     mission = models.TextField(
#         validators=[
#             MinLengthValidator(1, "Mission cannot be empty")
#         ]
#     )
#     org_images = models.TextField(
#         validators=[
#             MinLengthValidator(1, "Organization images cannot be empty")
#         ]
#     )

#     country=models.ForeignKey(Country,on_delete=models.CASCADE,related_name='country',db_column="country")
#     # def clean(self):
#     #     super().clean()
#     #     if not re.match(r'^\d{4}-\d{2}-\d{2}$', self.est_date):
#     #         raise ValidationError({'est_date': "Date must be in YYYY-MM-DD format"})

#     #     # Add any other custom validations here

#     # def save(self, *args, **kwargs):
#     #     self.full_clean()  # This will call clean() and run all the validations
#     #     super().save(*args, **kwargs)


#     class Meta:
#         db_table = "organization"

