from flask import Blueprint, render_template, current_app
from webapp.trends.models import Trends
from webapp.weather import weather_by_city
from datetime import datetime, timedelta, time

blueprint = Blueprint('trends', '__name__')

