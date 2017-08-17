from django.core.exceptions import ValidationError
from .models import Subscribers

def validateemail(value):
	qs = Subscribers.objects.filter(user_email__iexact=value)
	if qs.exists():
		raise ValidationError("You are already with us :)")
	return value