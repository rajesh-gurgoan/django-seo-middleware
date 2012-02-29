from django.conf.urls.defaults import url, patterns
urlpatterns = patterns( 'seo.views',
                        url( r'^get_named_url_list/$', 'get_named_url_list', name = 'get_named_url_list' ),
                    )