from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from gardenweb.db import create_bed, get_beds, get_bed, update_bed, delete_bed, get_plantings
from gardenweb.drawing import make_beds_svg, make_bed_svg

bp = Blueprint('bed', __name__)

@bp.route('/')
def index():
    beds = get_beds()
    return render_template('bed/index.html', beds=beds)

@bp.route('/bed/create', methods=('GET', 'POST'))
def create():
    bed = {}
    if request.method == 'POST':
        bed['top_left_x'] = request.form['top_left_x']
        bed['top_left_y'] = request.form['top_left_y']
        bed['x_length'] = request.form['x_length']
        bed['y_length'] = request.form['y_length']
        create_bed(bed)
        make_beds_svg()
        return redirect(url_for('bed.index'))
    else:
        return render_template('bed/create.html')

    
@bp.route('/bed/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        bed = {}
        bed['top_left_x'] = request.form['top_left_x']
        bed['top_left_y'] = request.form['top_left_y']
        bed['x_length'] = request.form['x_length']
        bed['y_length'] = request.form['y_length']
        bed['id'] = id
        update_bed(bed)
        make_beds_svg()
        return redirect(url_for('bed.index'))
    else:
        bed = get_bed(id)
        return render_template('bed/update.html', bed=bed)

@bp.route('/bed/<int:id>/')
def view(id):
    bed = get_bed(id)
    make_bed_svg(bed)
    plantings = get_plantings(id)
    return render_template('bed/view.html', bed=bed, plantings=plantings)

@bp.route('/bed/<int:id>/delete', methods=('POST',))
def delete(id):
    delete_bed(id)
    make_beds_svg()
    return redirect(url_for('bed.index'))
