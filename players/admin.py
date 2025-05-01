from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Place, Currency, ExchangeRate, Position, PositionCategory, Player, League, Team, HandThrowing, HandBatting, PlayerCommonRecord, PlayerPitchingRecord, PlayerBattingRecord, PlayerFieldingRecord, Organization, CareerCategory, Career, PlayerCareer, CareerVersion, Title, PlayerTitle, DraftCategory, Draft, PlayerDraft

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

# place
class PlaceResource(resources.ModelResource):
    class Meta:
        model = Place

class PlaceAdmin(BaseResourceAdmin):
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

class PositionAdmin(BaseResourceAdmin):
    resource_class = PositionResource

# position_categories
class PositionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# players
class PlayerResource(resources.ModelResource):
    class Meta:
        model = Player

class PlayerAdmin(BaseResourceAdmin):
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

class OrganizationAdmin(BaseResourceAdmin):
    resource_class = OrganizationResource

# leagues
class LeagueResource(resources.ModelResource):
    class Meta:
        model = League

class LeagueAdmin(BaseResourceAdmin):
    list_display = ('name', 'sort_order')
    list_editable = ('sort_order',)
    resource_class = LeagueResource

# teams
class TeamResource(resources.ModelResource):
    class Meta:
        model = Team

class TeamAdmin(BaseResourceAdmin):
    resource_class = TeamResource

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

# draft_category
class DraftCategoryResource(resources.ModelResource):
    class Meta:
        model = DraftCategory

class DraftCategoryAdmin(BaseResourceAdmin):
    resource_class = DraftCategoryResource

# draft
class DraftResource(resources.ModelResource):
    class Meta:
        model = Draft

class DraftAdmin(BaseResourceAdmin):
    list_display = ('year', 'draft_category')
    resource_class = DraftResource

# player_draft
class PlayerDraftResource(resources.ModelResource):
    class Meta:
        model = PlayerDraft

class PlayerDraftAdmin(BaseResourceAdmin):
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
