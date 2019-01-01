from django.contrib import admin
from django.db.models.base import ModelBase
import knowledgequest.models

MODEL_CLASSES = [obj for name, obj in vars(knowledgequest.models).items() if not name.startswith('_') and isinstance(obj, ModelBase)]


for ModelClass in MODEL_CLASSES:
    print(ModelClass)
    modeladmin_class_name = '{}Admin'.format(ModelClass.__name__)
    field_names = tuple([f.name for f in ModelClass._meta.get_fields()])
    print(field_names)
    class CustomModelAdmin(admin.ModelAdmin):
        list_display = field_names
    globals()[modeladmin_class_name] = globals().pop('CustomModelAdmin')
    locals()[modeladmin_class_name] = globals()[modeladmin_class_name]
    globals()[modeladmin_class_name].__name__ = modeladmin_class_name
    locals()[modeladmin_class_name].__name__ = modeladmin_class_name
    print(locals()[modeladmin_class_name])
    ModelAdminClass = locals()[modeladmin_class_name]
    try:
        admin.site.register(ModelClass, ModelAdminClass)
    except admin.sites.AlreadyRegistered:
        print('{} is already registered'.format(ModelClass.__name__))
