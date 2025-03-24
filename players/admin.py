from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Place, Currency, ExchangeRate, PositionCategory, Player, League, Team, HandThrowing, HandBatting, PlayerCommonRecord

# places
class PlaceResource(resources.ModelResource):
    class Meta:
        model = Place

class PlaceAdmin(ImportExportModelAdmin):
    resource_class = PlaceResource

# currency
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code','name',)

# exchange_rates
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('year','currency',)

# position_categories
class PositionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# players
class PlayerResource(resources.ModelResource):
    class Meta:
        model = Player

class PlayerAdmin(ImportExportModelAdmin):
    resource_class = PlayerResource

# hands_throwing
class HandThrowingAdmin(admin.ModelAdmin):
    list_display = ('name',)

# hands_batting
class HandBattingAdmin(admin.ModelAdmin):
    list_display = ('name',)

# leagues
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order')  # sort_orderも表示
    list_editable = ('sort_order',)  # 管理画面でsort_orderを編集可能にする

# teams
class TeamResource(resources.ModelResource):
    class Meta:
        model = Team

class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource

# player_common_records
class PlayerCommonRecordResource(resources.ModelResource):
    class Meta:
        model = PlayerCommonRecord

class PlayerCommonRecordAdmin(ImportExportModelAdmin):
    resource_class = PlayerCommonRecordResource

admin.site.register(Place, PlaceAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(PositionCategory, PositionCategoryAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(HandThrowing, HandThrowingAdmin)
admin.site.register(HandBatting, HandBattingAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(PlayerCommonRecord, PlayerCommonRecordAdmin)
