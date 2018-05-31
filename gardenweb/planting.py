from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from gardenweb.db import get_db
from gardenweb.drawing import make_beds_svg, make_bed_svg

bp = Blueprint('planting', __name__)

@bp.route('/bed/<int:bed_id>/planting/create/', methods=('GET', 'POST'))
def create(bed_id):
    if request.method == 'POST':
        top_left_x = request.form['top_left_x']
        top_left_y = request.form['top_left_y']
        x_length = request.form['x_length']
        y_length = request.form['y_length']
        plant_type = request.form['plant_type']
        date_planted = request.form['date_planted']
        date_harvested = request.form['date_harvested']
        
        db = get_db()
        db.execute(
            'INSERT INTO planting (bed_id, top_left_x, top_left_y, x_length, y_length, plant_type, date_planted, date_harvested)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (bed_id, top_left_x, top_left_y, x_length, y_length, plant_type, date_planted, date_harvested)
        )
        db.commit()
        make_beds_svg()
        return redirect(url_for('bed.view', id = bed_id))
    else:
        g.bed_id = bed_id
        return render_template('planting/create.html')

def get_planting(planting_id):
    planting = get_db().execute(
        'SELECT id, bed_id, top_left_x, top_left_y, x_length, y_length, plant_type, date_planted, date_harvested'
        ' FROM planting'
        ' WHERE id = ?',
        (planting_id,)
    ).fetchone()
    return planting
    
@bp.route('/planting/<int:id>/delete', methods=('POST',))
def delete(id):
    planting = get_planting(id)
    db = get_db()
    db.execute('DELETE FROM planting WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('bed.view', id=planting['bed_id']))
