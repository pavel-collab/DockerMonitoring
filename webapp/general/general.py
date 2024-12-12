import datetime

import psycopg as dbm

from flask import Blueprint, render_template, current_app

from utils.db import groupby_query_rows
from utils.cache import cache

general_bp = Blueprint('general_bp', __name__,
                       template_folder='templates')

@general_bp.route('/')
@cache.cached(timeout=5)
def main_page():
    # cache data in case of problems with database
    plot_data = cache.get(__name__ + ".plot_data")
    if plot_data is None:
        plot_data = {'': [('', '', '', datetime.datetime.min)]}
        cache.set(__name__ + ".plot_data", plot_data)

    tile_data = cache.get(__name__ + ".tile_data")
    if tile_data is None:
        tile_data = ('0', '-', '-', datetime.datetime.min)
        cache.set(__name__ + ".tile_data", tile_data)
    
    try:
        with dbm.connect(current_app.config["DB_URI"]) as con:
            cur = con.cursor()
            # extracting data for tiles on mane page
            cur.execute("""SELECT 
                            COUNT(DISTINCT container_id), MAX(cpu_usage), 
                            MAX(memory_usage), MAX("time") 
                        FROM container_stats""")
            query = cur.fetchone()
            if query[0] != 0:
                tile_data = query
                cache.set(__name__ + ".plot_data", tile_data)

            # extracting data for plot on main page
            limit = 100
            cur.execute("""SELECT * FROM container_stats ORDER BY "time"
                        DESC LIMIT (%s)""", (limit,))
            rows = cur.fetchall()
            if rows is not None:
                plot_data = groupby_query_rows(0, rows)
                cache.set(__name__ + ".plot_data", plot_data)
    except Exception:
        current_app.logger.error('Error occured while connecting to the database. Using cached data for render.')
            
    return render_template('general/index.html', tile_data=tile_data, plot_data=plot_data.items())