#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2012 Makoto Siraisi

import os
import urllib2
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from django.utils import simplejson

APP_ID = "9797AC36778F8D869B3E4CF8073A024E3B5A2CCC"
base_url = "http://api.search.live.net/json.aspx?"

class MainPage(webapp.RequestHandler):
  def get(self):
    template_values = {
      'title': 'Quark Search',
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    html = template.render(path, template_values)
    self.response.out.write(html)

class SearchPages(webapp.RequestHandler):
  def get(self):
    keyword = self.request.get('keyword')
    url = "%sAppid=%s&query=%s&sources=web&Web.Count=50" % (base_url, APP_ID,
            keyword)
    output = urlfetch.fetch(url)
    data = simplejson.loads(output.content)
    urls = []
    titles = []
    descriptions = []
    times = []
    try:
      for i in range(50):
        titles.append(data['SearchResponse']['Web']['Results'][i]['Title'])
        urls.append(data['SearchResponse']['Web']['Results'][i]['Url'])
        descriptions.append(data['SearchResponse']['Web']['Results'][i]['Description'])
        times.append(data['SearchResponse']['Web']['Results'][i]['DateTime'])
    except:
      pass
    total = data['SearchResponse']['Web']['Total']
    datas = [titles, urls, descriptions, times]
    template_values = {
      'title': keyword,
      'titles': titles,
      'urls': urls,
      'descriptions': descriptions,
      'times': times,
      'total': total,
      'datas': datas,
    }
    path = os.path.join(os.path.dirname(__file__), 'search.html')
    html = template.render(path, template_values)
    self.response.out.write(html)

class UnderDev(webapp.RequestHandler):
  def get(self):
    template_values = {
            'title': 'Coming Soon!',
            }
    path = os.path.join(os.path.dirname(__file__), 'underdev.html')
    html = template.render(path, template_values)
    self.response.out.write(html)

def main():
    application = webapp.WSGIApplication([('/', MainPage),
        ('/search', SearchPages),
        ('/underdev', UnderDev)],
                                         debug=False)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
