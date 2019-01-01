from django.contrib import admin
from django.db.models.base import ModelBase
import knowledgequest.models

MODEL_CLASSES = [name for name, obj in vars(knowledgequest.models).items() if not name.startswith('_') and isinstance(obj, ModelBase)]


for ModelClass in MODEL_CLASSES:
    modeladmin_class_name = '{}Admin'.format(ModelClass.__name__)
    class CustomModelAdmin(admin.ModelAdmin):
        list_display = tuple([f.name for f in ModelClass._meta.get_fields()])
    locals()[modeladmin_class_name] = CustomModelAdmin
    ModelAdminClass = locals()[modeladmin_class_name]
    try:
        admin.site.register(ModelClass, ModelAdminClass)
    except admin.sites.AlreadyRegistered:
        print('{} is already registered'.format(ModelClass.__name__))
