# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import time
from datetime import timedelta

d3 = 0


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    # response.flash = T("Welcome")
    # Welcome is annoying
    return dict()


# the following is written by Weikai Wu

def empty_form():
    response.flash = T("Please enter a task!")
    return 'empty form'


def dup_task():
    response.flash = T("Task exist!")
    return  'duplicate task'


def no_record():
    response.flash = T("No Record!")
    return 'no record'


def add_conflict():
    response.flash = T("Can't add task while counting down")
    return 'councting down'


def del_conflict():
    response.flash = T("Can't delete task while counting down")
    return 'councting down'


def no_task_to_start():
    response.flash = T("Please select a task to start")
    return 'no task to start'


# the above is written by Weikai Wu


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def home():

    return locals()

def BG(): return dict(message="hello from BG.py")

def help(): return dict(message="hello")

POST_PER_PAGE=10 #There can be at most 10 posts in the list_posts page

def list_posts():
    page=request.args(0, cast=int, default=0) # Request the current page
    start=page*POST_PER_PAGE # Start counting at page*_PER_PAGE
    stop=start+POST_PER_PAGE #Stop at POST_PER_PAGE
    rows=db(db.post).select(orderby=~db.post.created_on, limitby=(start,stop)) #Post 10 posts in the given range
    return locals()

@auth.requires_login() #it means the user must be logged in to see the page
def edit_post():
    id=request.args(0,cast=int) # Request the id of the post that will be edited
    page=request.args(1,cast=int,default=0)
    form=SQLFORM(db.post,id).process(next=URL('view_post',args=(id,page))) #Create an SQLFORM and process it. When done, go to the edited post 
    return locals()

@auth.requires_login()
def create_post():
    form=SQLFORM(db.post).process(next=URL('list_posts')) # Create an SQLFORM to make a post. Once done, go to the current list of posts
    return locals()

@auth.requires_login()
def view_post():
    id=request.args(0,cast=int) #Request the id of the post that the user wants to see
    page=request.args(1,cast=int, default=1)
    post=db.post(id) or redirect(URL('index')) #If the id doesn't exist, redirect to the main page
    field_var_created_by=post.created_by #Stores in a variable who created the post. This variable is later used in the editing feature
    db.comm.post.default=id #set the reference variable of comment to post equals to id. This is used for choosing the right comments
    form=SQLFORM(db.comm).process() #Create a new SQLFORM to process comments
    comment=db(db.comm.post==post.id).select(orderby=~db.comm.created_on) #Select the comments which reference variable equals post.id
    number_of_comments=db(db.comm.post==post.id).count() #Count the number of comments to display pagination buttons
    return locals()
