from datetime import datetime
from flask import Blueprint, render_template
from webapp.trends.forms import SelectDateForm


blueprint = Blueprint('trends', '__name__')


@blueprint.route('/monitor', methods=['GET', 'POST'])
def chart():
    form = SelectDateForm()
    if form.select_date.data:
        select_date = form.select_date.data
    else:
        select_date = datetime.today()
        form.select_date.data = select_date
    # if form.validate_on_submit():
    #     s_begin_time = form.select_date.data
    #     return redirect(url_for('trends.monitor'))
    title = "Архив температуры"
    return render_template('trends/index.html',
                           page_title=title, form=form)
