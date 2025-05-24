from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from games.models import GameStatus, Game


# Register your models here.
# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass


class GameStatusResource(resources.ModelResource):
    class Meta:
        model = GameStatus


class GameStatusAdmin(BaseResourceAdmin):
    resource_class = GameStatusResource


class GameResource(resources.ModelResource):
    class Meta:
        model = Game


class GameAdmin(BaseResourceAdmin):
    resource_class = GameResource


admin.site.register(GameStatus, GameStatusAdmin)
admin.site.register(Game, GameAdmin)
