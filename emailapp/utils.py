import random
import string

def code_generator():
	chars=string.ascii_lowercase + string.digits
	return ''.join(random.choice(chars) for _ in range(20))

def getKey(instance):
	new_code = code_generator()
	qs = instance.__class__
	qs_exists = qs.objects.filter(confirmKey=new_code).exists()
	while qs_exists:
		new_code = code_generator()
		qs_exists = qs.objects.filter(confirmKey=new_code).exists()	
	return new_code