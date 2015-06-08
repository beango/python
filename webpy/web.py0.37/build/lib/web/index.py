#!/usr/bin/python
# -*- coding: utf-8 -*-

import web

reload(sys)
sys.setdefaultencoding('utf-8')

urls = (
  '/', 'index',
  '/add', 'Add',
  '/edit/(\d+)', 'Edit',
  '/del/(\d+)', 'Del',
  '/view/(\d+)', 'View',
  '/register', 'Register',
  '/login', 'Login',
  '/logout', 'Logout',
  '/user/(\d+)', 'Profile',
  '/account/(\w+)', 'Account',
  '/password', 'Password',
  '/about', 'About')

class Index:
    def GET(self):
        i = web.input(page='1')
        page = int(i.page)
        page_posts, page_count = model.Post().list(page)
        return titled_render().list(page_posts, page_count, page)
        
if __name__ == "__main__":
    app.run()