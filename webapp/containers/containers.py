import psycopg as dbm

from flask import Blueprint, render_template, current_app
from utils.cache import cache

containers_bp = Blueprint('containers_bp', __name__,
                       template_folder='templates')

@containers_bp.route('/')
@cache.cached(timeout=5)
def containers():
    # cache data in case of problems with database
    containers_table = cache.get(__name__ + "containers_table")
    if containers_table is None:
        containers_table = ['-'] * 4 # 4 columns in containers table
        cache.set(__name__ + "containers_table", containers_table)

    try:
        with dbm.connect(current_app.config["DB_URI"]) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM dashboard_table")
            rows = cur.fetchall()
        if rows is not None:
            containers_table = rows
            cache.set(__name__ + "containers_table", containers_table)
    except Exception:
        current_app.logger.error('Error occured while connecting to the database. Using cached data for render.')
    return render_template('containers/containers_table.html', rows=cur.fetchall())

@containers_bp.route('/<container_id>')
@cache.cached(timeout=5)
def container_page(container_id):
    # cache data in case of problems with database
    container_table = cache.get(__name__ + "container_table")
    if container_table is None:
        container_table = ['-'] * 4 # 4 columns in container table
        cache.set(__name__ + "container_table", container_table)

    try:
        with dbm.connect(current_app.config["DB_URI"]) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM container_stats WHERE container_id = (%s)", (container_id,))
            rows = cur.fetchall()
        if rows is not None:
            container_table = rows
            cache.set(__name__ + "container_table", container_table)
    except Exception:
        current_app.logger.error('Error occured while connecting to the database. Using cached data for render.')

    return render_template('containers/container_page.html', rows=container_table, id=container_id)