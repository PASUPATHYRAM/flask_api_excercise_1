import os

base_dir=os.path.abspath(os.path.dirname(__file__))
sql_config='sqlite:///'+os.path.join(base_dir,'task.db')

