from datetime import datetime
from sensors_DS18B20 import Sensors_DS18B20
import time as _time
from webapp import create_app
from webapp.db import db
from webapp.trends.models import Trends


DATA_MAX_COUNT = 10000


app = create_app()


def control_base_max_size(max_size=DATA_MAX_COUNT):
    row_count = Trends.query.count()
    if row_count > max_size:
        first_trends = Trends.query.order_by(Trends.id.asc()).first()
        db.session.delete(first_trends)
        print('deleted {}'.format(first_trends))


def add_reccord_in_base(time, temp_in_house=None,
                        temp_outdoor=None,
                        temp_heating_collector=None,
                        pressure_water_collector=None,
                        value_electricity_meter=None):
    trends = Trends(time=time,
                    temp_in_house=temp_in_house,
                    temp_outdoor=temp_outdoor,
                    temp_heating_collector=temp_heating_collector,
                    pressure_water_collector=pressure_water_collector,
                    value_electricity_meter=value_electricity_meter)
    db.session.add(trends)
    control_base_max_size()
    db.session.commit()
    print('Added {}'.format(trends))


def read_values():
    sensors = Sensors_DS18B20()
    return {'time': datetime.now(),
            'temp_in_house': sensors.read_temp('28-8a201681c3ff'),
            'temp_outdoor': sensors.read_temp('28-20320c3f4fd9'),
            'temp_heating_collector': sensors.read_temp('28-8a201653deff')
            }


if __name__ == '__main__':
    with app.app_context():
        while True:
            values = read_values()
            if values:
                add_reccord_in_base(time=values['time'],
                                    temp_in_house=values['temp_in_house'],
                                    temp_outdoor=values['temp_outdoor'],
                                    temp_heating_collector=values['temp_heating_collector'])
            _time.sleep(10)
