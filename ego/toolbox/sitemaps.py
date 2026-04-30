from django.contrib import sitemaps
from django.urls import reverse
from toolbox.views.core.pages import get_blog_posts
from toolbox.views.core.catalog import get_tool_catalog

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # 这里的名字对应 toolbox/urls.py 中的 name
        return ['toolbox:index', 'toolbox:about', 'toolbox:privacy', 'toolbox:terms', 'toolbox:blog_list']

    def location(self, item):
        return reverse(item)

class ToolSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # 只包含有有效 URL 的工具
        return [tool for tool in get_tool_catalog() if tool.get('url')]

    def location(self, item):
        return item['url']

class BlogSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return get_blog_posts()

    def location(self, item):
        return reverse('toolbox:blog_detail', kwargs={'post_id': item['id']})

    def lastmod(self, item):
        from datetime import datetime
        return datetime.strptime(item['date'], '%Y-%m-%d')
