from django.core.cache import cache
from django.shortcuts import render_to_response
from django.core import urlresolvers

def get_named_url_list(request):
    """
    Returns a pattern dictionary with key as name of the named urls and value as its
    corresponding regex.
    """
    if cache.get( 'pattern_list' ):
        pattern_list = eval(cache.get( "pattern_list" ))
    else:
        resolver = urlresolvers.get_resolver(None)
        pattern_list = [value[1] for key,value in resolver.reverse_dict.items() if isinstance(key,basestring)]
        cache.set( "pattern_list", repr(pattern_list), 30*24*60*60 )
    return render_to_response( 'get_named_url_list.html', locals() )   