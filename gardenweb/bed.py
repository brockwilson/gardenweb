from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from gardenweb.db import get_db
from gardenweb.drawing import make_bed_svg, make_bed_svg_inline

bp = Blueprint('bed', __name__)

@bp.route('/')
def index():
    db = get_db()
    beds = get_beds()
    make_bed_svg()
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
            return redirect(url_for('bed.index'))
    return render_template('bed/update.html', bed=bed)
        
@bp.route('/bed/<int:id>/delete', methods=('POST',))
def delete(id):
    get_bed(id)
    db = get_db()
    db.execute('DELETE FROM bed WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('bed.index'))
