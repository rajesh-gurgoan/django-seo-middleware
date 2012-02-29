from django.core import urlresolvers
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from seo.models import MetaData
from django.core.cache import cache

DEFUALT_META_DATA = {'title': 'HTCampus','description':'HTCampus','keywords':'HTCampus'}

def get_url_name_pattern():
    """
    Returns a pattern dictionary with key as name of the named urls and value as its
    corresponding regex.
    """
    if cache.get( 'pattern_dict' ):
        pattern_dict = eval(cache.get( "pattern_dict" ))
    else:
        resolver = urlresolvers.get_resolver(None)
        pattern_dict = dict([(key,value[1]) for key,value in resolver.reverse_dict.items() if isinstance(key,basestring)])
        cache.set( "pattern_dict", repr(pattern_dict), 30*24*60*60 )
    return pattern_dict


def get_meta_info( path, SEO_CONTENT_DICT ):
    """
    Returns a dictionary which will render the html to be displayed in head for meta tags.
    Either returns a default dictionary or a dictionary computed by MetaData obj in-case a positive regex match is found.
    ** url_name gives the name of the named url, current path belongs to.
    """
    url_name = urlresolvers.resolve(path).url_name
    pattern_dict = get_url_name_pattern()
    url_regex = pattern_dict[url_name]
    try:
        meta_obj = MetaData.objects.get( path = url_regex )
    except:
        return DEFUALT_META_DATA
    else:
        SEO_CONTENT_DICT['title'], SEO_CONTENT_DICT['keywords'], SEO_CONTENT_DICT['description'] = meta_obj.title, meta_obj.keywords, meta_obj.description

    return SEO_CONTENT_DICT

class MetaDataMiddleware(object):
    """
    Middleware for adding meta-data for each page.
    Add 'seo.middleware.MetaDataMiddleware' to MIDDLEWARE_CLASSES
    """
    def process_template_response(self, request, response):

        path = request.path
        view_data_dict = response.context_data
        SEO_CONTENT_DICT = {}
        try:
            meta_obj = MetaData.objects.get( path = path )
        except:
            SEO_CONTENT_DICT = get_meta_info( path, SEO_CONTENT_DICT )
        else:
            SEO_CONTENT_DICT['title'], SEO_CONTENT_DICT['keywords'], SEO_CONTENT_DICT['description'] = meta_obj.title, meta_obj.keywords, meta_obj.description

        spl_char_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '}', '{',
                         ']','[', ':', '?', '~', '|',"'","`","~",'.',';','\\']

        r_t_s = render_to_string('seo_data.html', SEO_CONTENT_DICT)
        t1 = Template(r_t_s)
        c = Context(view_data_dict)
        seo_content = t1.render(c)
        actual_seo_content = ''.join( [ c for c in seo_content if c not in spl_char_list ] )
        response.context_data['seo_meta_data'] = mark_safe(actual_seo_content)
        return response
