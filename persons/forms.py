from django import forms
from .models import ReportedPerson, MissingPerson

#Form for missing persons

class MissingPersonCreateForm(forms.ModelForm):
	class Meta:
		model = MissingPerson
		exclude = ['status','matched_confidence','is_verified','face_encoding','is_matched_with_missing_person','found_location','found_time','reported_photo','is_contacted']

class MissingPersonUpdateForm(forms.ModelForm):
	class Meta:
		model = MissingPerson
		exclude = ['face_encoding', 'reported_photo','is_matched_with_missing_person','matched_confidence','is_verified', 'found_time','found_location','is_contacted']

class MissingPersonVerifyForm(forms.ModelForm):
	class Meta:
		model = MissingPerson
		fields =['is_verified']

#Forms for the reported suspected person in the db

class ReportedPersonCreateForm(forms.ModelForm):
	class Meta:
		model = ReportedPerson
		exclude = ['is_verified','face_encoding','is_matched_with_missing_person','matched_confidence','matched_face_encoding']

class ReportedPersonUpdateForm(forms.ModelForm):
	class Meta:
		model = ReportedPerson
		exclude =exclude = ['is_verified','face_encoding','is_matched_with_missing_person','matched_confidence','matched_face_encoding']

class ReportedPersonVerifyForm(forms.ModelForm):
	class Meta:
		model = ReportedPerson
		fields = ['is_verified']