from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import DraftCategory, Draft, PlayerDraft

# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass

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

admin.site.register(DraftCategory, DraftCategoryAdmin)
admin.site.register(Draft, DraftAdmin)
admin.site.register(PlayerDraft, PlayerDraftAdmin)