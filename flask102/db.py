import click
from flask import current_app, g
from flask.cli import with_appcontext
import cryptography

import pymysql


def get_db():
    g.db=pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='!QA2ws3ed',
        db='testo'
    ).cursor()
    return g.db

def db_fetch(db):
    print(db.fetchall())

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def execute_multiline_sql(f,db):
    query = [i.strip() for i in ' '.join(f.read().decode('utf8').split()).split(';') if i != '']
    for q in query:
        db.execute(q)

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        execute_multiline_sql(f,db)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('        Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
