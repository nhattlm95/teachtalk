import sys

 
sys.path.insert(0, '/var/www/teachtalk')

activate_this = '/home/nlt26/.local/share/virtualenvs/teachtalk-dWXd8pQP/bin/activate_this.py'
with open(activate_this) as file_:
	exec(file_.read(), dict(__file__=activate_this))

from app import app as application
