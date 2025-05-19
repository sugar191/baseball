from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Season


# Register your models here.
# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass


class SeasonResource(resources.ModelResource):
    class Meta:
        model = Season


class SeasonAdmin(BaseResourceAdmin):
    resource_class = SeasonResource


admin.site.register(Season, SeasonAdmin)
