from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf.urls.static import static
from blog.sitemaps import PostSitemap
from portal.sitemaps import StaticSitemap

sitemaps = {
    'post': PostSitemap,
    'static': StaticSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('markdownx/', include('markdownx.urls')),
    path('blog/', include('blog.urls')),
    path('', include('portal.urls')),
]

# 開発環境でのメディアファイルの配信設定
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
