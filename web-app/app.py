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
    return render_template('index.html')

@app.route('/containers')
def containers():
    with dbm.connect(dbname=DB_NAME) as con:
        cur = con.cursor()
        cur.execute(
            """SELECT
                container_id,
                AVG(cpu_usage) AS avg_cpu_usage,
                AVG(memory_usage) AS avg_memory_usage,
                MAX("time") AS last_update_time
            FROM container_stats
            GROUP BY container_id"""
        )
    return render_template('containers.html', rows=cur.fetchall())


if __name__ == '__main__':
    app.run('0.0.0.0', port=5010, debug=True)