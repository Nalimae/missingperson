from django.db import models
import PIL.Image
import face_recognition
from phonenumber_field.modelfields import PhoneNumberField
from django.core import validators


# Create your models here.
#Model for reporting missing persons

class MissingPerson(models.Model):

	GENDER_CAT_CHOICES=(
		("Male","Male"),
		("Female","Female"),
		("Other","Other"),
		)
	RELATIONSHIP_CAT_CHOICES=(
		("Mother","Mother"),
		("Brother","Brother"),
		("Sister","Sister"),
		("Father","Father"),
		("Husband","Husband"),
		("Wife","Wife"),
		("Relative","Relative"),
		("Friend","Friend"),
		("Other","Other"),
		)
	CURRENT_STATUS_CHOICES = (
		("New","New"),
		("Leads","Leads"),
		("Found","Found"),
		("Closed","Closed"),
		)
	#other fields for the missing person model
	
	first_name = models.CharField(verbose_name="Enter First Name", max_length=200, blank=False,null=False)
	last_name = models.CharField(verbose_name="Enter Last Name",max_length=200, blank=False,null=False)
	age= models.CharField(verbose_name="Enter Age of Missing Person", max_length=200,blank=False,null=False)
	gender = models.CharField(verbose_name="Select Gender of Missing Person", choices=GENDER_CAT_CHOICES, max_length=200,blank=False, null=False)
	last_seen = models.CharField(verbose_name="The Last Seen Location", max_length=200, blank=False,null=False)
	description = models.TextField(verbose_name="Provide Any Relevant Details", max_length=1000,blank=True,null=True)
	photo = models.ImageField(verbose_name="Upload Photo of Missing Person",upload_to="missingpersons/", blank=False, null=False)
	reported_photo = models.ImageField(verbose_name="Reported Photo of Missing Person found",upload_to="reportedfoundpersons/", blank=False, null=False)
	matched_confidence = models.CharField(verbose_name="Details of the Match", max_length=200,blank=True,null=True)
	
	#Information of person to be contacted in case the missing person is found
	
	contact_person = models.CharField(verbose_name="Person to be Contacted", max_length=200,blank=False,null=False)
	contact_relationship=models.CharField(verbose_name="Select Relationship with the Missing Person", choices=RELATIONSHIP_CAT_CHOICES, max_length=200, blank=False, null=False)
	contact_email = models.EmailField(verbose_name="Contact Email Address",max_length=254,blank=False,null=False,validators=[validators.EmailValidator(message="Invalid Email")])
	phone = PhoneNumberField(verbose_name="Mobile Number", null=False,blank=False)
	
	#Current situation of the case
	status = models.CharField(verbose_name="Current Status",choices=CURRENT_STATUS_CHOICES,max_length=200,null=False,blank=False)

	#fields used in face recognition algorithm
	is_verified = models.BooleanField(verbose_name="Process Face encoding",default=False)
	face_encoding =models.CharField(verbose_name="Face Encoding of Missing Person", max_length=250,blank=True,null=True)
	is_matched_with_missing_person = models.BooleanField(verbose_name="Has the Match been Found?", default=False)
	#if found, location from where it was reported 
	found_location = models.CharField(verbose_name="Found Location",max_length=200,blank=True,null=True)
	found_time = models.DateTimeField(blank=True,null=True)
	is_contacted = models.BooleanField(verbose_name="Has Contact Person Been Informed?", default=False)

	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now_add=True)

	#def get_encodings(self):


	class Meta:
		verbose_name ='Missing Person'
		verbose_name_plural = 'Missing People'
		ordering = ('first_name',)

	def __str__(self):
		return str(self.first_name)+ "" + str(self.last_name) + "" + str(self.face_encoding)

class ReportedPerson(models.Model):
	reported_location = models.CharField(verbose_name="Found Location",max_length=200,blank=False,null=False)
	description = models.TextField(verbose_name="Any Other Relevant Details", max_length=1000,blank=True,null=True)
	photo = models.ImageField(verbose_name="Upload Photo of Reported Person",upload_to="reportedpersons/", null=False,blank=False)

	#Fields in Face Recognition deep learning
	is_verified= models.BooleanField(verbose_name="Process Face encoding to match?", default=False)
	face_encoding = models.CharField(verbose_name="Face Encoding of Reported Person", max_length=250,blank=True,null=True)
	is_matched_with_missing_person = models.BooleanField(verbose_name="Has the Match been Found?", default=False)
	matched_confidence = models.CharField(verbose_name="Details of the Match", max_length=200,blank=True,null=True)
	matched_face_encoding = models.CharField(verbose_name="Face Encoding of Matched Person", max_length=200,blank=True,null=True)

	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Reported Person'
		verbose_name_plural = 'Reported Persons'
		ordering = ('created_date',)
	def __str__(self):
		return str(self.created_date)







    









		