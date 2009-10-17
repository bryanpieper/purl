

def short_url(request, url_token):
    """ 
    Lookup given url and redirect to new 
    location or homepage if not found.
    """
    from purl.models import ShortUrl
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    url_token = url_token.lower()
    redirect = reverse('homepage')
    try:
        surl = ShortUrl.objects.get(surl=url_token, active=True)
    except ShortUrl.DoesNotExist:
        pass
    else:
        from purl.models import SUrlHit
        redirect = surl.redirect_href
        
        # google analytics campaign data
        if surl.campaign_source or surl.campaign_medium or \
                surl.campaign_term or surl.campaign_content or \
                surl.campaign_name:
    
            from urlparse import urlparse
            redirect_parsed = urlparse(redirect)
            campaign_map = {
                'utm_source': surl.campaign_source,
                'utm_medium': surl.campaign_medium,
                'utm_term': surl.campaign_term,
                'utm_content': surl.campaign_content,
                'utm_campaign': surl.campaign_name,
            }
            campaign_str = ''
                        
            for c, v in campaign_map.items():
                if v:
                    campaign_str = '&'.join([campaign_str, '='.join([c, v])])
            
            if not redirect_parsed.query:
                if campaign_str and campaign_str[0] == '&': campaign_str = campaign_str[1:]
                redirect = '?'.join([redirect, campaign_str])
            else:
                redirect = ''.join([redirect, campaign_str])
        
        hit = SUrlHit(shorturl=surl)
        hit.ip_address = request.META['REMOTE_ADDR']
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            hit.ip_address = request.META['HTTP_X_FORWARDED_FOR'] 
        hit.user_agent = request.META.get('HTTP_USER_AGENT', '')
        hit.referer = request.META.get('HTTP_REFERER', '')
        hit.save()
    
    return HttpResponseRedirect(redirect)
   
