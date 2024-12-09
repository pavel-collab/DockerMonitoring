import datetime

import psycopg as dbm

from flask import Blueprint, render_template, current_app

from utils.db import groupby_query_rows

general_bp = Blueprint('general_bp', __name__,
                       template_folder='templates')

@general_bp.route('/')
def main_page():
    with dbm.connect(current_app.config["DB_URI"]) as con:
        cur = con.cursor()
        # extracting data for tiles on mane page
        cur.execute("""SELECT 
                           COUNT(DISTINCT container_id), MAX(cpu_usage), 
                           MAX(memory_usage), MAX("time") 
                       FROM container_stats""")
        tile_data = cur.fetchone()
        if not tile_data[0]:
            tile_data = ('0', '-', '-', datetime.datetime.min)
        print(tile_data[-1].strftime("%Y-%m-%d %H:%M:%S"))
        # extracting data for plot on main page
        limit = 100
        cur.execute("""SELECT * FROM container_stats ORDER BY "time"
                       DESC LIMIT (%s)""", (limit,))
        rows = cur.fetchall()
        if rows:
            plot_data = groupby_query_rows(0, rows)
        else:
            plot_data = {'': [('', '', '', datetime.datetime.min)]}
    return render_template('general/index.html', tile_data=tile_data, plot_data=plot_data.items())