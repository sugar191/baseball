from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Position, PositionCategory

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

# position
class PositionResource(resources.ModelResource):
    class Meta:
        model = Position

class PositionAdmin(BaseResourceAdmin):
    resource_class = PositionResource

# position_categories
class PositionCategoryResource(resources.ModelResource):
    class Meta:
        model = PositionCategory


class PositionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Position, PositionAdmin)
admin.site.register(PositionCategory, PositionCategoryAdmin)