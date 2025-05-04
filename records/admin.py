from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Currency, ExchangeRate, PlayerCommonRecord, PlayerPitchingRecord, PlayerBattingRecord, PlayerFieldingRecord

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

# currency
class CurrencyResource(resources.ModelResource):
    class Meta:
        model = Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code','name',)

# exchange_rates
class ExchangeRateResource(resources.ModelResource):
    class Meta:
        model = ExchangeRate

class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('year','currency',)

# player_common_records
class PlayerCommonRecordResource(resources.ModelResource):
    class Meta:
        model = PlayerCommonRecord

class PlayerCommonRecordAdmin(BaseResourceAdmin):
    resource_class = PlayerCommonRecordResource

# player_pitching_records
class PlayerPitchingRecordResource(resources.ModelResource):
    class Meta:
        model = PlayerPitchingRecord

class PlayerPitchingRecordAdmin(BaseResourceAdmin):
    resource_class = PlayerPitchingRecordResource

# player_batting_records
class PlayerBattingRecordResource(resources.ModelResource):
    class Meta:
        model = PlayerBattingRecord

class PlayerBattingRecordAdmin(BaseResourceAdmin):
    resource_class = PlayerBattingRecordResource

# player_fielding_records
class PlayerFieldingRecordResource(resources.ModelResource):
    class Meta:
        model = PlayerFieldingRecord

class PlayerFieldingRecordAdmin(BaseResourceAdmin):
    resource_class = PlayerFieldingRecordResource

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(PlayerCommonRecord, PlayerCommonRecordAdmin)
admin.site.register(PlayerPitchingRecord, PlayerPitchingRecordAdmin)
admin.site.register(PlayerBattingRecord, PlayerBattingRecordAdmin)
admin.site.register(PlayerFieldingRecord, PlayerFieldingRecordAdmin)