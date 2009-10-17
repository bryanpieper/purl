"""
Short Url data container, tracking and methods.
 
Copyright (c) 2009 Bryan Pieper, http://www.thepiepers.net/
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
 
"""

from django.db import models
import hashlib, time


class ShortUrl(models.Model):
    """ 
    Short Url. Stores short aliases, urls and campaign data. Used for
    url shortening.
    """
    surl = models.CharField(max_length=30, db_index=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    redirect_href = models.URLField()
    description = models.CharField(max_length=255, blank=True)
    campaign_source = models.CharField(max_length=255, null=True, blank=True)
    campaign_medium = models.CharField(max_length=255, null=True, blank=True)
    campaign_content = models.CharField(max_length=255, null=True, blank=True)
    campaign_name = models.CharField(max_length=255, null=True, blank=True)
    campaign_term = models.CharField(max_length=255, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, token_len=5):
        """ 
        Saves the url. If insert, generate surl unique token (alias)
        """
        if (not self.id):
            url_token = None
            while 1:
                url_token = self.gen_token(token_len)
                try:
                    ShortUrl.objects.get(surl=url_token)
                except ShortUrl.DoesNotExist:
                    break
            self.surl = url_token
            
        super(ShortUrl, self).save(force_insert, force_update) 


    def gen_token(self, token_len=5):
        """
        Generates a random token based on redirect_href 
        """
        h = hashlib.new('ripemd160')
        h.update(self.redirect_href)
        h.update(str(time.time()))
        token = h.hexdigest()
        token_start = 0
        for i, c in enumerate(token):
            if c.isdigit():
               token_start = i + 1
            else:
                break        
        return token[token_start:(token_len + token_start)]
    
    def __unicode__(self):
        return ', '.join([self.surl, self.redirect_href])
    
    @models.permalink
    def get_absolute_url(self):
        return ('url-redirect', (), {'url_token': self.surl})

    
    
class SUrlHit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)
    shorturl = models.ForeignKey('ShortUrl')
    referer = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        ordering = ['-created']
        

def get_shorturl(alias):
    """
    Get the short url by alias
    """
    try:
        surl = ShortUrl.objects.get(surl=alias, active=True)
    except ShortUrl.DoesNotExist:
        pass
    else:
        return surl
