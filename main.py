'''
Blog Engine
Copyright (C) 2019  Franco Minucci

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import cherrypy
import os
from mako.template import Template
from manage_db import query,insert,query_by_year
from cherrypy.lib import auth_basic
import time

def load_posts(id,year):
    if year != '':
        g = query_by_year('blog_post',year)
        content = ''
        for row in g:
            content += '<H1>'+row[1]+'</H1>'+row[3]+'<p>'+row[2]+'</p>\n'
        return content

    if int(id) == -1:
        c = query('blog_post')
        c.reverse()
        content = ''
        n = 0
        for row in c:
            if n ==3:
                break
            content += '<H1>'+row[1]+'</H1>'+row[3]+'<p>'+row[2]+'</p>\n'
            n+=1
        
        content+= '<a href="?id=-2">[all]</a>'

    elif int(id) == -2:
        c = query('blog_post')
        c.reverse()
        content = ''
        for row in c:
            content += '<H1>'+row[1]+'</H1>'+row[3]+'<p>'+row[2]+'</p>\n'

    elif int(id) >= 0:
        c = query('blog_post',id)
        c.reverse()
        content = ''
        for row in c:
            content += '<H1>'+row[1]+'</H1>'+row[3]+'<p>'+row[2]+'</p>'+'\n'
    return content

class Website:

    @cherrypy.expose
    def index(self,id=-1,year=''):
        home = Template(filename='./templates/page.html')
        
        return home.render(title="Home page",
            content=load_posts(id,year))
        

    @cherrypy.expose
    def about(self):
        about = Template(filename='./templates/page.html')
        return about.render(title="About me",content="about me")

    @cherrypy.expose
    def contact(self):
        contact = Template(filename='./templates/page.html')
        return contact.render(title="Contact me directly",content='E-mail: <a href="mailto:ir.fminucci@gmail.com">ir.fminucci@gmail.com</a>')

    @cherrypy.expose
    def _admin(self, title="", content=""):
        if title=="" or content=="":
            ad = Template(filename='./templates/admin.html')
            return ad.render()
            
        else:
            posts = query('blog_post')
            posts.sort()
            id = posts[-1][0]+1
            dt = time.strftime("%d-%m-%Y")
            string = str(id)+',"'+title+'","'+content+'","'+dt+'"'
            insert('blog_post',[string])
            
            return '''
            <html>
            <head>
            <meta http-equiv="Refresh" content="5" URL=_admin">
            <title>Success</title>
            </head>
            <body>
            <h3> Post submitted!</h3>
            You are being redirected to the admin page
            </body>
            </html>
            '''


def validate_password(realm, username, password):
    check_admin = query('admins')
    for a in check_admin:
        if a[0] == username and a[1]==password:
            return True
    return False

conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './templates'
        },
        '/_admin': {
         'tools.auth_basic.on': True,
         'tools.auth_basic.realm': 'localhost',
         'tools.auth_basic.checkpassword': validate_password,
         'tools.auth_basic.accept_charset': 'UTF-8',
        }
    }

website = Website()
cherrypy.quickstart(website,'/',conf)


