from django.contrib import admin

from .models import Property
from .models import Inquiry
from .models import PropertyImage
from .models import Profile
from .models import PropertyVisit

admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(Profile)
admin.site.register(PropertyVisit)
