from django.contrib import admin
from knowledgequest.models import Address, Email

for m in [Address, Email]:
    print(m)
    print(m.__class__)

class AddressAdmin(admin.ModelAdmin):
    pass

class EmailAdmin(admin.ModelAdmin):
    pass

admin.site.register(Address, AddressAdmin)
admin.site.register(Email, EmailAdmin)
