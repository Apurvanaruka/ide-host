# ide-host

'''
flask db init
'''
flask db migrate -m "Initial migration."
flask db upgrade
flask --app run run --reload