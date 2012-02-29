What it does:
    This app is useful when:
    1. You want to put the static seo content on the specific page.
    2. You want to put the customized ( based on the regular expressioned url) seo content on the page.

Advantage: You can directly call the view variables while configuring the seo content to display the seo content.

Requirements for this app:
    1. This app works for Django 1.3 and above.
    2. This app works only when each view within various apps of the project
       returns a TemplateResponse( not render_to_response ) which is a SimpleTemplateResponse object
       for more info read : https://docs.djangoproject.com/en/dev/ref/template-response/

To use this app:
    1. Install the seo directory somewhere in your python path
    2. Add 'seo' to INSTALLED_APPS in settings.py
    3. Add 'seo.middleware.MetaDataMiddleware' to MIDDLEWARE_CLASSES in settings.py
	4. Include url(r'^seo/', include('seo.urls')), into your urls.py.
    5. Add reference {{ seo_meta_data }} in your (eg base) template
	  
Model Definition:
    1. regular_expression: a boolean field choices a) static_url, b) dynamic_url
    2. path: url path of the page or the regular expression of the page
    3. title : a char field.
    4. keywords: a text field.
    5. description: a text field.

Admin Outlook:
    regular_expression:
    If selected NO: the path remains a char field and user may enter complete url
                             for the page he wants a static seo data to be displayed.

    If selected YES: the path field gets populated with list (select-field drop-down) of regex-es for which the
                              administrator wants to display a logical data on all regex matches.



Middleware definition for seo app.

    MetaDataMiddleware

    This middleware function is called for all the views returning a SimpleTemplateResponse object( TemplateResponse ).
        **Unlike render_to_response when a view returns a TemplateResponse the template is not rendered until all the middleware
          checks are complete. This gives us a handle of the context data in process_template_response, which can be changed, overriden or
          added here.

        **Here process_template_response processes various factors based on following steps to compute meta data for a particular url
          ::Checks for complete current path in MetaData table.
            If found:
                a) The corresponding title, keywords and description is computed and set for display as meta tags.
            If Not found:
                b) It does a regex match for the current url and if found a match in MetaData table, the following steps take place:
                    >> (definition get_meta_info() is responsible for this)- It checks for corresponding entry for title, keywords and description
                       and renders it with the context data returned by the current view in process.
                    >> If no match is found get_meta_info() returns a default text for the respective meta tags ( DEFUALT_META_DATA )