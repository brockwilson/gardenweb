from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from gardenweb.db import get_db
from gardenweb.drawing import make_beds_svg, make_bed_svg

bp = Blueprint('bed', __name__)

@bp.route('/')
def index():
    beds = get_beds()
    return render_template('bed/index.html', beds=beds)

@bp.route('/bed/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        top_left_x = request.form['top_left_x']
        top_left_y = request.form['top_left_y']
        x_length = request.form['x_length']
        y_length = request.form['y_length']
        
        db = get_db()
        db.execute(
            'INSERT INTO bed (top_left_x, top_left_y, x_length, y_length)'
            ' VALUES (?, ?, ?, ?)',
            (top_left_x, top_left_y, x_length, y_length)
        )
        db.commit()
        make_beds_svg()
        return redirect(url_for('bed.index'))
    else:
        return render_template('bed/create.html')

def get_beds():
    db = get_db()
    beds = db.execute(
        'SELECT id, top_left_x, top_left_y, x_length, y_length'
        ' FROM bed'
    ).fetchall()
    return beds
    
def get_bed(id):
    bed = get_db().execute(
        'SELECT id, top_left_x, top_left_y, x_length, y_length'
        ' FROM bed'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if bed is None:
        abort(404, "Bed id {0} doesn't exist.".format(id))

    return bed

def get_plantings(bed_id):
    plantings = get_db().execute(
        'SELECT id, bed_id, top_left_x, top_left_y, x_length, y_length, plant_type, date_planted, date_harvested'
        ' FROM planting'
        ' WHERE bed_id = ?',
        (bed_id,)
    ).fetchall()
    return plantings


@bp.route('/bed/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    bed = get_bed(id)

    if request.method == 'POST':
        top_left_x = request.form['top_left_x']
        top_left_y = request.form['top_left_y']
        x_length = request.form['x_length']
        y_length = request.form['y_length']
        error = None

        if not top_left_x:
            error = 'Top left x is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE bed SET top_left_x = ?, top_left_y = ?, x_length = ?, y_length = ?'
                ' WHERE id = ?',
                (top_left_x, top_left_y, x_length, y_length, id)
            )
            db.commit()
            make_beds_svg()
            return redirect(url_for('bed.index'))
    return render_template('bed/update.html', bed=bed)

@bp.route('/bed/<int:id>/')
def view(id):
    bed = get_bed(id)
    make_bed_svg(bed)
    plantings = get_plantings(id)
    return render_template('bed/view.html', bed=bed, plantings=plantings)

@bp.route('/bed/<int:id>/delete', methods=('POST',))
def delete(id):
    get_bed(id)
    db = get_db()
    db.execute('DELETE FROM bed WHERE id = ?', (id,))
    db.commit()
    make_beds_svg()
    return redirect(url_for('bed.index'))
