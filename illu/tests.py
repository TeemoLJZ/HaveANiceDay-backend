from django.test import TestCase
from ..common.models import IlluPic
# Create your tests here.

IlluPic.objects.delete(picid = {4,5,6})