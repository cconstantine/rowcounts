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

    user = users.get_current_user()

    if (not project) or (not user):
      return self.redirect('/')
    
    projects = Project.gql("where user = :user_id and __key__ = :project_id ", user_id=user, project_id=db.Key(project)).fetch(1);
    
    if len(projects) == 0:
      return self.redirect('/')

    self.response.headers['Content-Type'] = 'text/html'
    self.generate('project.html', {
      'project': projects[0],
    })


class CreateProjectAction(BaseRequestHandler):
  def post(self):    
    try:
      user = users.get_current_user()
      if user:
        desc = self.request.get('description')
        if desc and len(desc) > 0:
          newProject = Project(user = user, 
                               description=self.request.get('description'),
                               row=0)
          newProject.save()

          component = ProjectComponent(user=user,
                                       description="Start",
                                       row=1,
                                       in_project=newProject).save()
    except:
      pass;

    self.redirect('/')


class CreateComponentAction(BaseRequestHandler):
  def post(self):
    project_id = db.Key(self.request.get('project_id'))
    desc = self.request.get('desc')
    user = users.get_current_user()

    if desc == "":
      self.redirect("/project?id=%s" % project_id)
    project = Project.gql("where user = :user_id and __key__ = :project_id",
                          user_id=user, project_id=project_id).fetch(1)[0]

    component = ProjectComponent(user=user,
                               description=desc,
                               row=1,
                               in_project=project).save()
    
    self.redirect("/project?id=%s" % project.get_id())


class DeleteComponentAction(BaseRequestHandler):
  def post(self):
    project_id = self.request.get('project_id')
    component_id = db.Key(self.request.get('component_id'))

    user = users.get_current_user()
    component = ProjectComponent.gql(
      "where user = :user_id and __key__ = :component_id",
      user_id=user, component_id=component_id).fetch(1)[0]

    if component:
      component.delete()
    
    self.redirect("/project?id=%s" % project_id)


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
  def incRow(self, component):
    component.row += 1
    component.put()
    return component.row

  def post(self):
    id = db.Key(self.request.get('id'))
    rid = self.request.get('rid')

    user = users.get_current_user()
    component = ProjectComponent.gql(
      "where user = :user_id and __key__ = :component_id",
      user_id=user, component_id=id).fetch(1)[0]

    if component:
      self.response.out.write(simplejson.dumps(
          {'row' : db.run_in_transaction_custom_retries(1000,self.incRow, component),
           'rid' : rid,
           'id' : self.request.get('id')}))

class GetRowCount(webapp.RequestHandler):
  def get(self):
    id = db.Key(self.request.get('id'))
    user = users.get_current_user()

    component = ProjectComponent.gql(
      "where user = :user_id and __key__ = :component_id",
      user_id=user, component_id=id).fetch(1)

    if component:
      self.response.out.write(component[0].row)
    
def main():
  application = webapp.WSGIApplication([
    ('/', ProjectsPage),
    ('/project', ProjectPage),
    ('/actions/createProject.do', CreateProjectAction),
    ('/actions/createComponent.do', CreateComponentAction),
    ('/actions/deleteComponent.do', DeleteComponentAction),
    ('/actions/modifyProject.do', ModifyProjectAction),
    ('/actions/IncrementRow.do', IncrementRowAction),
    ('/row', GetRowCount),
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
