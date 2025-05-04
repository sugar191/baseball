from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Player, HandThrowing, HandBatting

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

# players
class PlayerResource(resources.ModelResource):
    class Meta:
        model = Player

class PlayerAdmin(BaseResourceAdmin):
    resource_class = PlayerResource

# hands_throwing
class HandThrowingResource(resources.ModelResource):
    class Meta:
        model = HandThrowing


class HandThrowingAdmin(admin.ModelAdmin):
    list_display = ('name',)

# hands_batting
class HandBattingResource(resources.ModelResource):
    class Meta:
        model = HandBatting


class HandBattingAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Player, PlayerAdmin)
admin.site.register(HandThrowing, HandThrowingAdmin)
admin.site.register(HandBatting, HandBattingAdmin)