

from django.contrib import admin
from purl.models import ShortUrl, SUrlHit

class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ('surl', 'redirect_href', 'description', 'created', 'modified', 'active',)
    
class SUrlHitAdmin(admin.ModelAdmin):
    list_display = ('shorturl', 'created', 'ip_address', 'user_agent', 'referer', )
    list_per_page = 50
    ordering = ['-created']
 
admin.site.register(ShortUrl, ShortUrlAdmin)
admin.site.register(SUrlHit, SUrlHitAdmin)
