import os, sys 
#sys.stdout = sys.stderr 
from os.path import abspath, dirname, join 
#from site import addsitedir 
#from django.core.handlers.wsgi import WSGIHandler 
#sys.path.append('/usr/local/lib/python2.7/site-packages/django')
#sys.path.append('/var/www/html/sbu_pdt')
#sys.path.insert(0, '/var/www/html')
#sys.path.insert(0, '/home/tester/tools/python/python_project/sbu_pdt')
sys.path.insert(0, '/home/tester/tools/python/python_project')
#sys.path.insert(0, abspath(join(dirname(__file__), "../"))) 
#sys.path.insert(0, abspath(join(dirname(__file__), ". . /. . /"))) 
os.environ['DJANGO_SETTINGS_MODULE'] = 'sbu_pdt.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'
#application = WSGIHandler()
#apache_configuration= os.path.dirname(__file__)
#project = os.path.dirname(apache_configuration)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mdash.settings'
#os.environ['PYTHON_EGG_CACHE'] = '/tmp'   

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
#print>>sys.stderr,sys.path

