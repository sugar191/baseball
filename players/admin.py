from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Place, Currency, ExchangeRate, Position, PositionCategory, Player, League, Team, HandThrowing, HandBatting, PlayerCommonRecord, PlayerPitchingRecord, PlayerBattingRecord, PlayerFieldingRecord, Organization, CareerCategory, Career, PlayerCareer, CareerVersion, Title, PlayerTitle, DraftCategory, Draft, PlayerDraft

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

# position
class PositionResource(resources.ModelResource):
    class Meta:
        model = Position

class PositionAdmin(ImportExportModelAdmin):
    resource_class = PositionResource

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

# organizations
class OrganizationResource(resources.ModelResource):
    class Meta:
        model = Organization

class OrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationResource

# leagues
class LeagueResource(resources.ModelResource):
    class Meta:
        model = League

class LeagueAdmin(ImportExportModelAdmin):
    list_display = ('name', 'sort_order')  # sort_orderも表示
    list_editable = ('sort_order',)  # 管理画面でsort_orderを編集可能にする
    resource_class = LeagueResource

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

# player_pitching_records
class PlayerPitchingRecordResource(resources.ModelResource):
    class Meta:
        model = PlayerPitchingRecord

class PlayerPitchingRecordAdmin(ImportExportModelAdmin):
    resource_class = PlayerPitchingRecordResource

# player_batting_records
class PlayerBattingRecordResource(resources.ModelResource):
    class Meta:
        model = PlayerBattingRecord

class PlayerBattingRecordAdmin(ImportExportModelAdmin):
    resource_class = PlayerBattingRecordResource

# player_fielding_records
class PlayerFieldingRecordResource(resources.ModelResource):
    class Meta:
        model = PlayerFieldingRecord

class PlayerFieldingRecordAdmin(ImportExportModelAdmin):
    resource_class = PlayerFieldingRecordResource

# career_category
class CareerCategoryResource(resources.ModelResource):
    class Meta:
        model = CareerCategory

class CareerCategoryAdmin(ImportExportModelAdmin):
    resource_class = CareerCategoryResource

# career
class CareerResource(resources.ModelResource):
    class Meta:
        model = Career

class CareerAdmin(ImportExportModelAdmin):
    resource_class = CareerResource

# career
class CareerVersionResource(resources.ModelResource):
    class Meta:
        model = CareerVersion

class CareerVersionAdmin(ImportExportModelAdmin):
    resource_class = CareerVersionResource

# player_career
class PlayerCareerResource(resources.ModelResource):
    class Meta:
        model = PlayerCareer

class PlayerCareerAdmin(ImportExportModelAdmin):
    resource_class = PlayerCareerResource

# title
class TitleResource(resources.ModelResource):
    class Meta:
        model = Title

class TitleAdmin(ImportExportModelAdmin):
    resource_class = TitleResource

# player_title
class PlayerTitleResource(resources.ModelResource):
    class Meta:
        model = PlayerTitle

class PlayerTitleAdmin(ImportExportModelAdmin):
    resource_class = PlayerTitleResource

# draft_category
class DraftCategoryResource(resources.ModelResource):
    class Meta:
        model = DraftCategory

class DraftCategoryAdmin(ImportExportModelAdmin):
    resource_class = DraftCategoryResource

# draft
class DraftResource(resources.ModelResource):
    class Meta:
        model = Draft

class DraftAdmin(ImportExportModelAdmin):
    resource_class = DraftResource

# player_draft
class PlayerDraftResource(resources.ModelResource):
    class Meta:
        model = PlayerDraft

class PlayerDraftAdmin(ImportExportModelAdmin):
    resource_class = PlayerDraftResource

admin.site.register(Place, PlaceAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(PositionCategory, PositionCategoryAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(HandThrowing, HandThrowingAdmin)
admin.site.register(HandBatting, HandBattingAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(PlayerCommonRecord, PlayerCommonRecordAdmin)
admin.site.register(PlayerPitchingRecord, PlayerPitchingRecordAdmin)
admin.site.register(PlayerBattingRecord, PlayerBattingRecordAdmin)
admin.site.register(PlayerFieldingRecord, PlayerFieldingRecordAdmin)
admin.site.register(CareerCategory, CareerCategoryAdmin)
admin.site.register(Career, CareerAdmin)
admin.site.register(CareerVersion, CareerVersionAdmin)
admin.site.register(PlayerCareer, PlayerCareerAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(PlayerTitle, PlayerTitleAdmin)
admin.site.register(DraftCategory, DraftCategoryAdmin)
admin.site.register(Draft, DraftAdmin)
admin.site.register(PlayerDraft, PlayerDraftAdmin)
