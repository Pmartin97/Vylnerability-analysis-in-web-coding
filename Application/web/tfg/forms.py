from django import forms
from django.core import validators
from .models import Archivo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

FRAMEWORK_CHOICE = (
    ('unknown', 'Unknown'),('html', "HTML"), ('nodejs', 'Nodejs'), ("react", "React")
)
def validate_string(value):
	reg = "([^A-Za-z0-9\-\_\.]+)"
	search = re.search(reg, str(value))
	print("validating: "+str(value))
	if search:
		raise ValidationError(
			_('Only letters, numbers, dash, underscore or point are allowed.'),
			params={'value': value},
		)


class UploadFileForm(forms.Form):

	file = forms.FileField()
	framework = forms.ChoiceField(choices = FRAMEWORK_CHOICE, initial='unknown', widget=forms.Select(), required=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
		
		Row(
			Column('file', css_class='form-group col-md-12 mb-0'),
			css_class='form-row'
			),
		Row(
			Column('framework', css_class='form-group col-md-12 mb-0'),
			css_class='form-row'
			),
		Submit('submit', 'Save')
		)
	
class ChangeFileForm(forms.Form):
	new_title = forms.CharField(max_length=50, validators=[validate_string])
	titulo_archivo = forms.CharField(max_length=50, widget=forms.HiddenInput())
	framework = forms.ChoiceField(choices = FRAMEWORK_CHOICE, initial='unknown', widget=forms.Select(), required=True)
	text = forms.CharField(widget=forms.Textarea)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
		
		Row(
			Column('titulo_archivo', css_class='hidden'),
			Column('new_title', css_class='form-group col-md-4 mb-0'),
			css_class='form-row'
			),
		Row(
			Column('framework', css_class='form-group col-md-12 mb-0'),
			css_class='form-row'
			),
		Row(
			Column('text', css_class='form-group col-md-12 mb-0'),
			css_class='form-row'
			),
		
		Submit('submit', 'Save changes', css_class="btn btn-success btn-lg")
		)

	

class NewPost(forms.Form):
	title = forms.CharField(max_length=50, validators=[validate_string])
	description = forms.CharField(widget=forms.Textarea)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
		
		Row(
			Column('title', css_class='form-group col-md-4 mb-0'),
			css_class='form-row'
			),
		Row(
			Column('description', css_class='form-group col-md-12 mb-0'),
			css_class='form-row'
			),
		
		Submit('submit', 'Create New Post', css_class="btn btn-success btn-lg ")
		)
class NewVulnerability(forms.Form):
	cve = forms.CharField(max_length=50, validators=[validate_string])
	description = forms.CharField(widget=forms.Textarea)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
		
		Row(
			Column('cve', css_class='form-group col-md-4 mb-0'),
			css_class='form-row'
			),
		Row(
			Column('description', css_class='form-group col-md-12 mb-0'),
			css_class='form-row'
			),
		
		Submit('submit', 'Send vulnerability request', css_class="btn btn-success btn-lg ")
		)


class NewMessage(forms.Form):
	message = forms.CharField(widget=forms.Textarea)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
		
		
		Row(
			Column('message', css_class='form-group col-md-12 mb-0'),
			css_class='form-row'
			),
		
		Submit('submit', 'Response', css_class="btn btn-success btn-lg ")
		)


class ChangeUserForm(forms.Form):
	user = forms.CharField(max_length=30, validators=[validators.validate_slug])
	first_name = forms.CharField(max_length=30, validators=[validators.validate_slug])
	last_name = forms.CharField(max_length=30, validators=[validators.validate_slug])


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
		
		Row(
			Column('user', css_class='form-group col-md-4 mb-0'),
			css_class='form-row'
			),
		Row(
			Column('first_name', css_class='form-group col-md-4 mb-0'),
			css_class='form-row'),
		Row(
			Column('last_name', css_class='form-group col-md-4 mb-0'),
			css_class='form-row'),
		
		Submit('submit', 'Save changes', css_class="btn btn-success btn-lg")
		)


