from django.shortcuts import render
from django.http import HttpResponse
from pipes import Template
from django.template import loader
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
from PIL import Image, ImageDraw
import face_recognition
from persons.models import MissingPerson, ReportedPerson
from .forms import *
from scipy.spatial import distance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.conf import settings
import numpy as np
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

class IndexView(TemplateView):
	template_name = "index.html"

##MISSING PERSONS
#view to list all missing persons
class MissingPersonListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	model = MissingPerson
	context_object_name = 'missing_persons'
	template_name = 'persons/missing_person_list.html'
 
#view list missing persons that need to be approved
class MissingPersonToBeApprovedListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	template_name = 'persons/missing_person_list.html'
	queryset = MissingPerson.objects.filter(is_verified=False)
	context_object_name = 'missing_persons'

#view to list all missing persons with status as leads(a possible match with a reported person) 	
class MissingPersonWithLeadsListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	template_name = 'persons/missing_person_list.html'
	queryset = MissingPerson.objects.filter(status='Leads')
	context_object_name = 'missing_persons'

#view to display all missing persons who have been found
class MissingPersonFoundListView(LoginRequiredMixin,ListView):
	login_url= reverse_lazy('index')
	logout_url = reverse_lazy('index')	
	template_name = 'persons/missing_person_list.html'
	queryset = MissingPerson.objects.filter(status='Found')
	context_object_name = 'missing_persons'

#a view to create a missing person
class MissingPersonCreateView(CreateView):
	model = MissingPerson
	form_class = MissingPersonCreateForm
	template_name = 'persons/create_update_form.html'
	success_url =reverse_lazy('missing_person_form_success')
	

# view to verify a missing person (if background check is done)
class MissingPersonVerifyView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('index')
    logout_url = reverse_lazy('index')
    model = MissingPerson
    form_class = MissingPersonVerifyForm
    template_name = 'persons/create_update_form.html'
    success_url = reverse_lazy ('missing_person_face')

    def post(self,request,**kwargs):
    	print("Catching Update Function")
    	form = self.form_class(request.POST)
    	if form.is_valid():
    		
    			self.object = self.get_object()
    			uploaded_file_url=self.object.photo.url
    			print("image URL is",self.object.photo.url)
    			print("face ID is",self.object.face_encoding)
    			#if the person is verified and does not already have a face id, we generate
    			if not self.object.face_encoding:
    				print("Calling Face Encoding Generation")
    				#generating face encoding to database
    				missing_persons=face_recognition.load_image_file(uploaded_file_url[1:])
    				face_encodings = face_recognition.face_encodings(missing_persons)
    				#missing_persons_face_encodings=face_encodings
    				#print("Detected face encoding is",face_encodings)
    				#saving the generated face into database
    				self.object.face_encoding = face_encodings
    				self.object.save()
    				#return face_encodings
    	return super().post(request,**kwargs)
# to update a missing person
class MissingPersonUpdateView(LoginRequiredMixin, UpdateView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	model = MissingPerson
	form_class = MissingPersonUpdateForm
	template_name = 'persons/create_update_form.html'
	success_url = reverse_lazy('list_missing_person')

# view to deletea missing person
class MissingPersonDeleteView(LoginRequiredMixin, DeleteView):
	login_url = reverse_lazy('index')
	logout_url=reverse_lazy('index')
	model = MissingPerson
	template_name ='persons/delete_form.html'
	success_url = reverse_lazy('list_missing_person')

	#REPORTED PERSONS
#View to list all reported persons
class ReportedPersonListView(LoginRequiredMixin,ListView):
	logout_url =reverse_lazy('index')
	login_url = reverse_lazy('index')
	model = ReportedPerson
	template_name = 'persons/all_reported_persons.html'
	context_object_name = "reported_persons"
#to view list of all reported persons who need to be approved
class ReportedPersonToBeApprovedListView(LoginRequiredMixin,ListView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	template_name = 'persons/reported_person_process_face.html'
	context_object_name = 'reported_persons'
	queryset = ReportedPerson.objects.filter(is_verified=False)
# see a list of all reported persons who have been matched with a missing person
class ReportedPersonMatchedListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	template_name = 'persons/reported_person_list.html'
	context_object_name = 'reported_persons'
	queryset = MissingPerson.objects.all().filter(is_matched_with_missing_person=True)
# see a list of reported persons who have not been matched
class ReportedPersonNotMatchedListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	template_name = 'persons/reported_person_list.html'
	context_object_name = 'reported_persons'
	queryset = ReportedPerson.objects.filter(is_matched_with_missing_person=False, is_verified=True)

# view to create reported person
class ReportedPersonCreateView(CreateView):
	model = ReportedPerson
	form_class = ReportedPersonCreateForm
	template_name = 'persons/reported_create_update_form.html'
	success_url = reverse_lazy('reported_person_form_success')

#view to update persons reported

class ReportedPersonUpdateView(LoginRequiredMixin,UpdateView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	model = ReportedPerson
	form_class = ReportedPersonUpdateForm
	template_name = 'persons/update_reported_person.html'
	success_url = reverse_lazy('list_reported_person')
#view to verify reported person

class ReportedPersonVerifyView(LoginRequiredMixin,UpdateView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	model = ReportedPerson
	form_class = ReportedPersonVerifyForm
	template_name = 'persons/reported_create_update_form.html'
	success_url = reverse_lazy('list_reported_person')

	def post(self, request, **kwargs):
		print("Catching update Function")

		form = self.form_class(request.POST)
		if form.is_valid():
			if form.cleaned_data['is_verified']:
				self.object = self.get_object()
				uploaded_file_url=self.object.photo.url
				print("Image URL is", self.object.photo.url)
				print("Image Path is",self.object.photo.path)

				print("face ID is",self.object.face_encoding)
				#to get a list of all face encodings of missing persons
				# = list(MissingPerson.objects.filter(face_encoding__isnull=False).values_list('face_encoding', flat=True))
				files = []
				first_name = []
				last_name= []
				images=[]
				encodings=[]
				missing_person = MissingPerson.objects.all()
				for prsn  in missing_person:
					first_name.append(prsn.first_name)
					last_name.append(prsn.last_name)
					files.append(prsn.photo)
					images.append(prsn.last_name + ' '+  prsn.first_name)
					encodings.append(prsn.first_name)
				for i in range(0, len(images)):
					images[i] = face_recognition.load_image_file(files[i])
					encodings[i]=face_recognition.face_encodings(images[i])[0]
					#array of known face encoding and names
					known_face_encodings = encodings
					known_face_names = first_name
					known_last_names = last_name




				#missing_face_encodings= np.asarray(missing_face_encoding)
				#print("face ID from database is",missing_face_encodings)
						# person is verified and does not already have a face id, we generate
				if not self.object.face_encoding:
					print("Calling Face ID Generation")
					#generating face id
					reported_persons=face_recognition.load_image_file(uploaded_file_url[1:])
					face_locations = face_recognition.face_locations(reported_persons)
					reported_face_encodings =face_recognition.face_encodings(reported_persons,face_locations)
					self.object.face_encoding = reported_face_encodings
					self.object.save()

					pil_image = Image.fromarray(reported_persons)
					# Create a Pillow ImageDraw Draw instance to draw with
					draw = ImageDraw.Draw(pil_image)

					#loop through each face found in the unknown face
					for (top, right, bottom, left) , face_encoding in zip (face_locations, reported_face_encodings):
						#see if the face is a match
						matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
						name = "Unknown person"
						last_names ="Uknown"


					#reported_encodings = np.asarray(reported_face_encodings)
					#print("REPORT:Detected Face ID is",reported_face_encodings)

					face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
					best_match_index = np.argmin(face_distances)
					if matches[best_match_index]:
						name = known_face_names[best_match_index]
						last_names = known_last_names[best_match_index]
						for i, face_distance in enumerate(face_distances):
							if(face_distance < 0.6):
								#if MissingPerson.objects.filter(face_encoding=results[0]).exists():
								print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
								print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
								print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
								print("The names are:",name,last_names)
								
								print()
								if MissingPerson.objects.filter(first_name=name).exists():
									print("Match found with face distance of {:.2} ".format(face_distance))
									#get the matched missing person
									found_person =MissingPerson.objects.get(first_name=name)
									found_person.status = "Leads"
									found_person.is_matched_with_missing_person=True
									found_person.reported_photo = self.object.photo
									found_person.matched_confidence="This is " + found_person.first_name + " lost at " + found_person.last_seen + " reported by "+ found_person.contact_person +  " having confidence rate of " + str(face_distance*100) +"%."
									found_person.found_location = self.object.reported_location
									found_person.found_time = self.object.created_date
									found_person.save()
									
									#update the details to the database
									self.object.matched_face_encoding =face_encoding 
									self.object.is_matched_with_missing_person= True
									self.object.matched_confidence = "This is " + found_person.first_name + " lost at " + found_person.last_seen + " reported by "+ found_person.contact_person +  " having confidence rate of " + str(face_distance*100) +"%." 
									self.object.save()	
								else:
									print("no match found")
												
								
					
					
		return super().post(request,**kwargs)

#view to delete reported person
class ReportedPersonDeleteView(LoginRequiredMixin,DeleteView):
	login_url = reverse_lazy('index')
	logout_url = reverse_lazy('index')
	model = ReportedPerson
	template_name = 'persons/delete_form.html'
	success_url = reverse_lazy('list_reported_person')

#view to show matched/found person details
class FoundPersonDetailView(LoginRequiredMixin,DetailView):
	def get(self, request, *args, **kwargs):
		found_person_details = get_object_or_404(MissingPerson,pk=kwargs['pk'])
		context = {'found_person_details': found_person_details}
		return render(request, 'persons/found_person_details.html', context)
		

	#def get_context_data(self,**kwargs):
		#context = super().get_context_data(**kwargs)
		#context['reported_person_details'] = ReportedPerson.objects.all().filter(is_matched_with_missing_person=True)
		#context['found_person_details'] = MissingPerson.objects.all().filter(is_contacted=False)
		#return context

#def FoundPerson(request,id):
	#found_person_details=MissingPerson.objects.get(id=id)
	
	#context={
	 #'found_person_details':found_person_details
	 #}
	#return render(request,'persons/found_person_details.html',context)


#view to display missing person has been successfully registered
class MissingPersonFormSuccessView(TemplateView):
	template_name = 'persons/missing_person_form_success.html'

#view to display reported persons has been successfully registered
class ReportedPersonFormSuccessView(TemplateView):
	template_name = 'persons/reported_person_form_success.html'
#view to display reported persons has been successfully registered
class MissingPersonFaceFormSuccessView(TemplateView):
	template_name = 'persons/missing_person_face.html'

#send email to contact person
def SendEmailToContact(object):
	subject = f'We have found {object.first_name}!'
	message = f'Hi {object.contact_person},{object.first_name} {object.last_name} was reported to be found at {object.found_location} on {object.found_time}.'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [object.contact_email,]
	send_mail(subject, message, email_from, recipient_list)
#function to set status as found and send email to the cntact person
def missing_person_update_status(request, pk):
	object = get_object_or_404(MissingPerson, pk=pk)
	object.status = "Found"
	#contact the relative
	SendEmailToContact(object)
	object.is_contacted = True
	object.save()
	print("Email sent!")
	context = {'missing_person_object' : object}
	return render(request, "persons/missing_person_matched.html", context)











		



