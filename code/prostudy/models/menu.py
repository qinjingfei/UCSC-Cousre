# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('ProStudy'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="#",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

#navigation bar
response.menu = [
    (T('Home'), False, URL('default', 'BG'), []) #Create a new link on the navigation bar
]

response.menu += [
    (T('APP'), False, URL('default', 'index'), []) #Add a new a link
]

response.menu += [
    (T('Help'), False, URL('default', 'help'), [])
]

response.menu += [
    (T('Feedback'), False, URL('default', 'list_posts'), [])
]

#Created by Daniel F Martinez



if "auth" in locals():
    auth.wikimenu()
