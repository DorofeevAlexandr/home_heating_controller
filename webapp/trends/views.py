from datetime import datetime, timedelta
from flask import Blueprint, current_app, render_template
from webapp.trends.forms import SelectDateForm
from webapp.trends.models import Trends
from webapp.weather import weather_by_city

blueprint = Blueprint('trends', '__name__')


@blueprint.route('/monitor', methods=['GET', 'POST'])
def monitor():
    form = SelectDateForm()
    if form.select_date.data:
        select_date = form.select_date.data
    else:
        select_date = datetime.today()
        form.select_date.data = select_date
    # if form.validate_on_submit():
    #     s_begin_time = form.select_date.data
    #     return redirect(url_for('trends.monitor'))
    title = "Мониторинг системы отопления"
    chart_data = ChartData()
    chart_data.read_data_in_base(select_date)
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    last_value = read_last_data_in_base()
    return render_template('trends/index.html',
                           page_title=title, form=form,
                           values=[chart_data.temperatures_in_house,
                                   chart_data.temperatures_outdoor,
                                   chart_data.temperatures_heating_collector],
                           labels=chart_data.times,
                           legends=chart_data.legends,
                           select_date=chart_data.st_select_date,
                           weather=weather,
                           current_value=last_value)


class ChartData():
    def __init__(self) -> None:
        self.times = []
        self.temperatures_in_house = []
        self.temperatures_outdoor = []
        self.temperatures_heating_collector = []
        self.legends = ['Температура в доме, °C',
                        'Темп. на улице, °C',
                        'Темп. коллектора отопления, °C']
        self.st_select_date = ''

    def read_data_in_base(self, select_date):
        # begin_time = select_date.replace(hour=0, minute=0, second=0)
        begin_time = datetime.combine(select_date, datetime.min.time())
        end_time = begin_time + timedelta(hours=23, minutes=59, seconds=59)
        self.st_select_date = begin_time.strftime('%d.%m.%Y')

        trend_data = Trends.query.filter((Trends.time > begin_time) & (Trends.time < end_time)).all()
        for point in trend_data:
            self.times.append(point.time.strftime('%H:%M:%S'))
            if point.temp_in_house:
                self.temperatures_in_house.append(point.temp_in_house)
            else:
                self.temperatures_in_house.append(0)
            if point.temp_outdoor:
                self.temperatures_outdoor.append(point.temp_outdoor)
            else:
                self.temperatures_outdoor.append(0)
            if point.temp_heating_collector:
                self.temperatures_heating_collector.append(point.temp_heating_collector)
            else:
                self.temperatures_heating_collector.append(0)


def read_last_data_in_base():
    last_data_trends = Trends.query.order_by(Trends.id.desc()).first()
    return {'time': last_data_trends.time.strftime('%Y.%m.%d %H:%M:%S'),
            'temp_in_house': last_data_trends.temp_in_house,
            'temp_outdoor': last_data_trends.temp_outdoor,
            'temp_heating_collector': last_data_trends.temp_heating_collector,
            }
