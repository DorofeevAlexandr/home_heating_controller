from datetime import timedelta
import os


basedir = os.path.abspath(os.path.dirname(__file__))

WEATHER_DEFAULT_CITY = "Saransk,Russia"
WEATHER_API_KEY = "908e2a6d72af42c396b123736210812"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..',
                                                      'webapp.db')

SECRET_KEY = 'jhgyttyunhuytfr4567987697gftyhgffvjcfu'

REMEMBER_COOKIE_DURATION = timedelta(days=5)
SQLALCHEMY_TRACK_MODIFICATIONS = False
