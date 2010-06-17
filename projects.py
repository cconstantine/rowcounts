#!/usr/bin/env python
#

__author__ = 'Chris Constantine'

import datetime
import os
import random
import string
import sys
import wsgiref.handlers

from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
import logging

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

from BaseRequestHandler import BaseRequestHandler

  
class Project(db.Model):
  user = db.UserProperty(required=True)
  description = db.TextProperty()

  def get_id(self):
    return self.key().__str__()

class ProjectComponent(db.Model):
  user = db.UserProperty(required=True)
  description = db.TextProperty()
  row = db.IntegerProperty()

  in_project = db.ReferenceProperty(Project,
                                   collection_name='components')

  def get_id(self):
    return self.key().__str__()


class ProjectsPage(BaseRequestHandler):
  def get(self):
    current_user = users.get_current_user()
    self.response.headers['Content-Type'] = 'text/html'

    context = {}
    if (current_user):
      projects = Project.gql("WHERE user = :user",user=current_user);
      context['projects'] = projects.fetch(1000)

    self.generate('projects.html', context)
      

class ProjectPage(BaseRequestHandler):
  def get(self):
    project = self.request.get('id')

    if not project:
      self.redirect('/')

    user = users.get_current_user()
    

    projects = Project.gql("where user = :user_id and __key__ = :project_id ", user_id=user, project_id=db.Key(project));

    self.response.headers['Content-Type'] = 'text/html'
    self.generate('project.html', {
      'project': projects.fetch(1)[0],
    })


class CreateProjectAction(BaseRequestHandler):
  def post(self):    
    user = users.get_current_user()
    if user:
      desc = self.request.get('description')
      if desc and len(desc) > 0:
        newProject = Project(user = user, 
                             description=self.request.get('description'),
                             row=0)
        newProject.put()

        ProjectComponent(user = user, 
                         description="foo", 
                         row=0, 
                         in_project=newProject).save()

        ProjectComponent(user = user, 
                         description="bar", 
                         row=0, 
                         in_project=newProject).save()

    self.redirect('/')

class ModifyProjectAction(BaseRequestHandler):
  def post(self):
    button = self.request.get('action')
    row = int(self.request.get('row'))

    user = users.get_current_user()

    project = Project.gql("where user = :user_id and __key__ = :project_id",
                user_id=user, project_id=id).fetch(1)[0]
    
    if not project:
      self.redirect("/")

    if button == "Save":
      project.row = row
      project.put()

      self.redirect("/project?id=%s" % project.get_id())
    elif button == "Delete":
      project.delete()
      
      self.redirect("/")

class IncrementRowAction(BaseRequestHandler):
  def incRow(self, project):
    project.row += 1
    project.put()
    return project.row

  def post(self):
    id = db.Key(self.request.get('id'))
    rid = self.request.get('rid')

    user = users.get_current_user()
    project = Project.gql("where user = :user_id and __key__ = :project_id",
                          user_id=user, project_id=id).fetch(1)[0]

    if project:
      self.response.out.write(simplejson.dumps(
          {'row' : db.run_in_transaction_custom_retries(1000,self.incRow, project),
           'rid' : rid}))


def main():
  application = webapp.WSGIApplication([
    ('/', ProjectsPage),
    ('/project', ProjectPage),
    ('/actions/createProject.do', CreateProjectAction),
    ('/actions/modifyProject.do', ModifyProjectAction),
    ('/actions/IncrementRow.do', IncrementRowAction),
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
