from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = 1.0

    def items(self):
        return ['/', '/blog/']

    def location(self, obj):
        return obj
