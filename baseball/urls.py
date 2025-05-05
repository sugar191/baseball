from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('home.urls')),  # playersアプリのURL設定をインクルード
    path('', include('players.urls')),  # playersアプリのURL設定をインクルード
    path('admin-tool/', include('admin_panel.urls')),
    # path('api/', include('api.urls')),  # 未使用でもコメントで残しておくと便利
]

# メディアファイルのURL設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)