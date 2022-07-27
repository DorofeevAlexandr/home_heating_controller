from datetime import datetime, timedelta
from webapp import create_app
from webapp.db import db
from webapp.trends.models import Trends

app = create_app()


def add_reccord_in_base(time):
    trends = Trends(time=time,
                    temp_in_house=time.second,
                    temp_outdoor=time.second/2,
                    temp_heating_collector=time.minute,
                    pressure_water_collector=time.hour/10,
                    value_electricity_meter=time.hour*3600+time.minute*60+time.second)
    db.session.add(trends)
    print('Added {}'.format(trends))


def control_base_max_size(max_size):
    row_count = Trends.query.count()
    if row_count > max_size:
        first_trends = Trends.query.order_by(Trends.id.asc()).first()
        db.session.delete(first_trends)
        print('deleted {}'.format(first_trends))


if __name__ == '__main__':
    # Временно добавим в базу данные для тестирования отображения трендов
    DATA_MAX_COUNT = 10
    with app.app_context():
        time = datetime.now() - timedelta(hours=48)
        delta = timedelta(minutes=1, seconds=1)
        for _ in range(DATA_MAX_COUNT):
            time += delta
            add_reccord_in_base(time)
            control_base_max_size(max_size=DATA_MAX_COUNT)
        db.session.commit()
