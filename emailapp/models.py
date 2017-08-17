from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from .utils import getKey



# Create your models here.
class Subscribers(models.Model):
	user_email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True)
	confirmKey = models.CharField(max_length=20, blank=True, null=True)
	confirmed = models.BooleanField(default=False)
	def __unicode__(self):
		return self.user_email

	def __str__(self):
		return self.user_email

	def save(self, *args, **kwargs):
		if self.confirmKey is None or self.confirmKey == "":
			self.confirmKey = getKey(self)
		super(Subscribers,self).save(*args,**kwargs)