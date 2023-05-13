import os

from flask import Flask, render_template, g
import sqlite3
from werkzeug.exceptions import abort

from config import Config


class FlaskDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    def get(self):
        try:
            sql = ''' SELECT * FROM users'''
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Ошибка получения меню БД')

        return []

def get_db():
    '''соединение с БД, если оно еще не установленно'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

app = Flask(__name__ )
@app.teardown_appcontext
def close_db(error):
    ''' закрываем соединение с БД'''
    if hasattr(g, 'link_db'):
        g.link_db.close()



app.config.from_object(Config)
# print(*app.config.items(), sep='\n')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'bd_vk_post.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# гл стр
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/pass')
def pass1():
    return render_template('pass.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/post')
def subscribe():
    db = get_db()
    db = FlaskDataBase(db)

    return render_template('post.html', subs=db.get())

if __name__ == '__main__':
    app.run()
