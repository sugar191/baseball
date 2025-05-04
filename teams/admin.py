from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import League, Team, Organization

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

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

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)