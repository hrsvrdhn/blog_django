from django import forms
from .models import Subscribers
from .validators import validateemail

class EmailPostForm(forms.Form):
	user_email = forms.EmailField(
			label = '',
			# validators = [validateemail],
			widget = forms.TextInput(
					attrs = {
						"placeholder" : "Your Email",
						"class" : "form-control",
					}
				)
			)