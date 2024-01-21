# This will provide a sample data in your database
import os
os.system('manage.py makemigrations')
os.system('manage.py migrate')
os.system('manage.py loaddata sample_data.json')
os.system('manage.py migrate')
print(' ------------------------\n  Succecfuly initialized \n ------------------------')