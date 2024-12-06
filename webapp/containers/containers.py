import psycopg as dbm

from flask import Blueprint, render_template, current_app

containers_bp = Blueprint('containers_bp', __name__,
                       template_folder='templates')

@containers_bp.route('/')
def containers():
    with dbm.connect(current_app.config["DB_URI"]) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM dashboard_table")
    return render_template('containers/containers_table.html', rows=cur.fetchall())

@containers_bp.route('/<container_id>')
def container_page(container_id):
    with dbm.connect(current_app.config["DB_URI"]) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM container_stats WHERE container_id = (%s)", (container_id,))
    return render_template('containers/container_page.html', rows=cur.fetchall(), id=container_id)