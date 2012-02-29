# -*- coding: UTF-8 -*-

from django.db import models

URL_CHOICE_TYPE = ( ( False, "No" ), ( True, "Yes" ), )

class MetaData(models.Model):
    """
    Model definition for following fields:
    1. path: holds
                  a) regular expression for the urls, same data has to be projected in title, keywords and description.
                  OR
                  b) complete path for which a specific data will be projected in title, keywords and description ( unique ).
    2. title, keywords, description: holds
                  a) data with view objects which get populated the way a template is rendered at run-time.
                     ** the data entries to be made for a particular view in mind must use save variable names as used in view,
                     ** example:: "This is title for {{ variable_name }}"
                  OR
                  b) holds static data for a specific-complete url.
    """
    regular_expression = models.BooleanField( choices= URL_CHOICE_TYPE, default=False )
    path = models.CharField(max_length=250, unique=True, help_text="Specify the path (URL) for this page (only if static data is to be displayed) or Specify the path's regular expression (only if same data is to be displayed for all regex matches)")
    title = models.CharField(max_length=250, default="", blank=True, help_text="This is the meta (page) title, that appears in the title bar.")
    keywords = models.TextField(default="", blank=True, help_text="Comma-separated keywords for search engines.")
    description = models.TextField(default="", blank=True, help_text="A short description, displayed in search results.")

    def __unicode__(self):
        return self.path

