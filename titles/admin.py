from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Title, PlayerTitle

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

# title
class TitleResource(resources.ModelResource):
    class Meta:
        model = Title

class TitleAdmin(BaseResourceAdmin):
    resource_class = TitleResource

# player_title
class PlayerTitleResource(resources.ModelResource):
    class Meta:
        model = PlayerTitle

class PlayerTitleAdmin(BaseResourceAdmin):
    list_display = ('player', 'title')
    resource_class = PlayerTitleResource

admin.site.register(Title, TitleAdmin)
admin.site.register(PlayerTitle, PlayerTitleAdmin)
