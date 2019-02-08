import os
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE = os.getenv('DATABASE', default='database/example.db')
