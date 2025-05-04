from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Place

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

# place
class PlaceResource(resources.ModelResource):
    class Meta:
        model = Place

class PlaceAdmin(BaseResourceAdmin):
    resource_class = PlaceResource

admin.site.register(Place, PlaceAdmin)