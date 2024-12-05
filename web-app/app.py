#!/usr/bin/env python3

import psycopg as dbm
#import psycopg_pool

from flask import Flask, render_template, request, redirect, url_for, jsonify

DB_NAME = 'postgres'
#DB_CONN_STR = "dbname='postgres'"
app = Flask(__name__)
#pool = psycopg_pool.ConnectionPool(DB_CONN_STR)

@app.route('/')
def main_page():
    with dbm.connect(dbname=DB_NAME) as con:
        cur = con.cursor()
        cur.execute("""SELECT 
                           COUNT(DISTINCT container_id), MAX(cpu_usage), 
                           MAX(memory_usage), MAX("time") 
                       FROM container_stats""")
    return render_template('index.html', data=cur.fetchone())

@app.route('/containers')
def containers():
    with dbm.connect(dbname=DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM dashboard_table")
    return render_template('containers_table.html', rows=cur.fetchall())

@app.route('/containers/<container_id>')
def container_page(container_id):
    with dbm.connect(dbname=DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM container_stats WHERE container_id = (%s)", (container_id,))
    return render_template('container_page.html', rows=cur.fetchall(), id=container_id)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5010, debug=True)