from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import TransferType, Transfer, PlayerTransfer


# 共通のベース管理クラス
class BaseResourceAdmin(ImportExportModelAdmin):
    pass


class TransferTypeResource(resources.ModelResource):
    class Meta:
        model = TransferType


class TransferTypeAdmin(BaseResourceAdmin):
    resource_class = TransferTypeResource


class TransferResource(resources.ModelResource):
    class Meta:
        model = Transfer


class TransferAdmin(admin.ModelAdmin):
    resource_class = TransferResource


class PlayerTransferResource(resources.ModelResource):
    class Meta:
        model = PlayerTransfer


class PlayerTransferAdmin(admin.ModelAdmin):
    resource_class = PlayerTransferResource


admin.site.register(TransferType, TransferTypeAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(PlayerTransfer, PlayerTransferAdmin)
