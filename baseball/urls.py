from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  # ログインページ
    path('logout/', LogoutView.as_view(), name='logout'),   # ログアウトページ
    path('', include('players.urls')),  # playersアプリのURL設定をインクルード
    # path('api/', include('api.urls')),  # 未使用でもコメントで残しておくと便利
]

# メディアファイルのURL設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)