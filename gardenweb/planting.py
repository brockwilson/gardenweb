from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from gardenweb.db import create_planting, get_planting, get_plantings, update_planting, delete_planting, get_bed
from gardenweb.drawing import make_beds_svg, make_bed_svg, make_planting_svg

bp = Blueprint('planting', __name__)

@bp.route('/bed/<int:bed_id>/planting/create/', methods=('GET', 'POST'))
def create(bed_id):
    if request.method == 'POST':
        planting = {}
        planting['top_left_x'] = request.form['top_left_x']
        planting['top_left_y'] = request.form['top_left_y']
        planting['x_length'] = request.form['x_length']
        planting['y_length'] = request.form['y_length']
        planting['plant_type'] = request.form['plant_type']
        planting['date_planted'] = request.form['date_planted']
        planting['date_harvested'] = request.form['date_harvested']
        planting['bed_id'] = bed_id
        create_planting(planting)
        make_beds_svg()
        # should probably have a make_bed_svg in here
        return redirect(url_for('bed.view', id = bed_id))
    else:
        return render_template('planting/create.html')
    
@bp.route('/bed/<int:bed_id>/planting/<int:planting_id>/')
def view(bed_id, planting_id):
    planting = get_planting(planting_id)
    make_planting_svg(planting)
    return render_template('planting/view.html', planting=planting)

@bp.route('/bed/<int:bed_id>/planting/<int:planting_id>/update/', methods=('GET', 'POST'))
def update(bed_id, planting_id):
    if request.method == 'POST':
        planting = {}
        planting['top_left_x'] = request.form['top_left_x']
        planting['top_left_y'] = request.form['top_left_y']
        planting['x_length'] = request.form['x_length']
        planting['y_length'] = request.form['y_length']
        planting['plant_type'] = request.form['plant_type']
        planting['date_planted'] = request.form['date_planted']
        planting['date_harvested'] = request.form['date_harvested']
        planting['id'] = planting_id
        update_planting(planting)
        make_beds_svg()
        bed = get_bed(bed_id)
        make_bed_svg(bed)
        plantings = get_plantings(bed_id)
        # would be better to show the planting here, but I haven't figured that out yet.
        return render_template('bed/view.html', bed=bed, plantings=plantings)
        
    
    else:
        planting = get_planting(planting_id)
        return render_template('planting/update.html', planting=planting)
    return None
    
@bp.route('/planting/<int:id>/delete', methods=('POST',))
def delete(id):
    planting = get_planting(id)
    delete_planting(id)
    return redirect(url_for('bed.view', id=planting['bed_id']))
