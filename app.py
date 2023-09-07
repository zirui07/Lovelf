import sqlite3
from sqlite3 import Error
import os
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def create_db():
    if not os.path.exists('data.db'):
        conn = sqlite3.connect('data.db')
        conn.execute('''CREATE Table Journal(
                  ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  Title TEXT NOT NULL,
                  Date TEXT NOT NULL,
                  Day TEXT NOT NULL,
                  Content TEXT NOT NULL,
                  Mood TEXT NOT NULL)   
  ''')


def connect_db(db):
    try:
        conn = sqlite3.connect(db)
        print('Database connected')
        return (conn)
    except Error as e:
        return (e)


def new_journal(conn, title, date, day, content, mood):
    sql = 'INSERT INTO Journal(Title, Date, Day, Content, Mood) VALUES(?,?,?,?,?)'
    try:
        conn.execute(sql, (title, date, day, content, mood))
        conn.commit()
        return ('Updated successfully')
    except Error as e:
        return (e)


def get_last3journal(conn):
    sql = 'SELECT * FROM Journal ORDER BY ID DESC LIMIT 3'
    try:
        cur = conn.execute(sql)
        last3_lst = cur.fetchall()  #[(id title, date, day content mood) *3]
        return (last3_lst)
    except Error as e:
        return (e)


@app.route('/treehole/')
def treehole():
    create_db()
    conn = connect_db('data.db')
    last3_lst = get_last3journal(conn)
    conn.close()  #use jinja in html to loop through
    return render_template('journal.html', last3_lst=last3_lst)


@app.route('/update/')
def update():
    conn = connect_db('data.db')
    title = request.args['title']
    date = request.args['date']
    day = request.args['day']
    content = request.args['content']
    mood = request.args['mood']
    new_journal(conn, title, date, day, content, mood)
    conn.close()
    return render_template('upd_journal.html')


@app.route('/self-care practices/')
def self_care_practices():

    return render_template('self-care.html')


@app.route('/helpline/')
def helpline():

    return render_template('helpline.html')


if __name__ == '__app__':
    app.run(debug=True, port=6000)
