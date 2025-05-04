from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import CareerCategory, Career, CareerVersion, PlayerCareer

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

# career_category
class CareerCategoryResource(resources.ModelResource):
    class Meta:
        model = CareerCategory

class CareerCategoryAdmin(BaseResourceAdmin):
    resource_class = CareerCategoryResource

# career
class CareerResource(resources.ModelResource):
    class Meta:
        model = Career

class CareerAdmin(BaseResourceAdmin):
    resource_class = CareerResource

# career_version
class CareerVersionResource(resources.ModelResource):
    class Meta:
        model = CareerVersion

class CareerVersionAdmin(BaseResourceAdmin):
    resource_class = CareerVersionResource

# player_career
class PlayerCareerResource(resources.ModelResource):
    class Meta:
        model = PlayerCareer

class PlayerCareerAdmin(BaseResourceAdmin):
    resource_class = PlayerCareerResource

admin.site.register(CareerCategory, CareerCategoryAdmin)
admin.site.register(Career, CareerAdmin)
admin.site.register(CareerVersion, CareerVersionAdmin)
admin.site.register(PlayerCareer, PlayerCareerAdmin)