from django.contrib import admin
from .models import Customer
from .models import Illustration
from .models import IlluPic

admin.site.register(Customer)
# Register your models here.
admin.site.register(Illustration)
admin.site.register(IlluPic)