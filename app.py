from flask import Flask, render_template
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__ )




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
    connect = sqlite3.connect('bd_vk_post.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM users')
    subs = cursor.fetchall()
    return render_template('post.html', subs=subs)

if __name__ == '__main__':
    app.run()
