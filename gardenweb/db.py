import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def create_bed(bed):
    db = get_db()
    db.execute(
        'INSERT INTO bed (top_left_x, top_left_y, x_length, y_length)'
        ' VALUES (?, ?, ?, ?)',
        (bed['top_left_x'], bed['top_left_y'], bed['x_length'], bed['y_length'])
    )
    db.commit()
    return None

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
        return None
    return bed

def update_bed(bed):
    db = get_db()
    db.execute(
        'UPDATE bed SET top_left_x = ?, top_left_y = ?, x_length = ?, y_length = ?'
        ' WHERE id = ?',
        (bed['top_left_x'], bed['top_left_y'], bed['x_length'], bed['y_length'], bed['id'])
    )
    db.commit()
    return None

def delete_bed(bed_id):
    db = get_db()
    db.execute('DELETE FROM bed WHERE id = ?', (bed_id,))
    db.commit()
    return None

def get_plantings(bed_id):
    plantings = get_db().execute(
        'SELECT id, bed_id, top_left_x, top_left_y, x_length, y_length, plant_type, date_planted, date_harvested'
        ' FROM planting'
        ' WHERE bed_id = ?',
        (bed_id,)
    ).fetchall()
    return plantings
