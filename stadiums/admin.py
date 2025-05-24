from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from stadiums.models import Stadium


# Register your models here.
# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass


class StadiumResource(resources.ModelResource):
    class Meta:
        model = Stadium


class StadiumAdmin(BaseResourceAdmin):
    resource_class = StadiumResource


admin.site.register(Stadium, StadiumAdmin)
