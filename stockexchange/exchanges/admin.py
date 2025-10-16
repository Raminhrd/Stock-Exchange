from django.contrib import admin
from exchanges.models import *


admin.site.register(Company)
admin.site.register(Portfolio)
admin.site.register(Order)
admin.site.register(Trade)