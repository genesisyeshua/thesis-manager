import webapp2
from google.appengine.ext import ndb
#from google.appengine.ext import db
import jinja2
import os
import urllib
import logging


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# STUDENT_CREATE_HTML_FORM = """\
# <html>
#     <body bgcolor="pink">
#     <form action="/student" method="post">
#       <div><font face="Curlz MT"> <b>First Name</b> <input type="text" name= "first_name" > </text></div>
#     <div><b>Last Name</b> <input type="text" name= "last_name" > </text></div>
#     <div> <b>Age</b> <input type="text" name= "age" > </text></div><br/>
#     <div> <input type="submit" value= "Create" > </text></div>
#     </form>
#   </body>
# </html>"""

class Student(ndb.Model):
	first_name= ndb.StringProperty(indexed=True)
	last_name= ndb.StringProperty(indexed=True)
	age= ndb.IntegerProperty()
	date= ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<h1>Hello, World!</h1>')

        
class studentcreate(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


    def post(self):
        student= Student()
        student.first_name=self.request.get('first_name')
        student.last_name= self.request.get('last_name')
        student.age= int(self.request.get('age'))
        student.put()
        self.redirect('/success')

class successpage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Success! <a href="/student/list">view students</a>')

class studentlist(webapp2.RequestHandler):
    def get(self):
        students = Student.query().order(-Student.date).fetch()
        logging.info(students)
        template_data = {
            'student_list': students
        }
        template = JINJA_ENVIRONMENT.get_template('student_list_page.html')
        self.response.write(template.render(template_data))

class studentedit(webapp2.RequestHandler):
    def get(self,student_id):
        stud = Student.get_by_id(int(student_id))
        template_data = {
            'student': stud
        }
        template = JINJA_ENVIRONMENT.get_template('student_edit.html')
        self.response.write(template.render(template_data))

    def post(self,student_id):
        student = Student.get_by_id(int(student_id))
        student.first_name=self.request.get('first_name')
        student.last_name= self.request.get('last_name')
        student.age= int(self.request.get('age'))
        student.put()
        self.redirect('/success')

class studentdel(webapp2.RequestHandler):
    def get(self,student_id):
        stud_del = Student.get_by_id(int(student_id))
        stud_del.key.delete()
        self.response.write('Success! <a href="/student/list">view students</a>')
       
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/student/create', studentcreate),
    ('/success', successpage),
    ('/student/list', studentlist),
    ('/student/edit/(.*)', studentedit),
    ('/student/del/(.*)', studentdel)  
], debug=True)
