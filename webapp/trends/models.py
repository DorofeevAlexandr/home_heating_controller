from webapp.db import db


class Trends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    temp_in_house = db.Column(db.Float, nullable=True)
    temp_outdoor = db.Column(db.Float, nullable=True)
    temp_heating_collector = db.Column(db.Float, nullable=True)
    pressure_water_collector = db.Column(db.Float, nullable=True)
    value_electricity_meter = db.Column(db.Float, nullable=True)

    def __repr__(self):
        result = f'{self.id} time = {self.time}, '
        result += f'{self.temp_in_house}, '
        result += f'{self.temp_outdoor}, '
        result += f'{self.temp_heating_collector}, '
        result += f'{self.pressure_water_collector}, '
        result += f'{self.value_electricity_meter}'
        return result
