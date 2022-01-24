from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired


class SelectDateForm(FlaskForm):
    select_date = DateField('Выбор даты',
                            validators=[DataRequired()], format='%Y-%m-%d',
                            render_kw={"class": "datepicker"})
    update = SubmitField('Обновить', render_kw={"class": "btn btn-primary"})
