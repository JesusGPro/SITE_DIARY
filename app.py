from flask import Flask, render_template, url_for, request, flash, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key'

try:
    connection = sqlite3.connect("messages.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE Messages_Register(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TITLE VARCHAR(50) NOT NULL,
                    CONTENT VARCHAR(250) UNIQUE NOT NULL,
                    DATE_TIME) """)

    connection.close()


except sqlite3.OperationalError:
    connection = sqlite3.connect("messages.db")
    cursor = connection.cursor()

    messages = cursor.execute("SELECT * FROM Messages_Register").fetchall()

    messages_view = []

    for user in messages:
        messages_view.append({'id': user[0], 'title': user[1], 'content': user[2]})

    connection.close()

@app.route('/')
def index():
    return render_template("index.html", messages=messages_view)

@app.route('/refresh/', methods=('GET', 'POST'))
def refresh():
    connection = sqlite3.connect("messages.db")
    cursor = connection.cursor()

    messages = cursor.execute("SELECT * FROM Messages_Register").fetchall()

    messages_view_2 = []

    for user in messages:
        messages_view_2.append({'id': user[0], 'title': user[1], 'content': user[2]})

    connection.close()

    return render_template("refresh.html", messages=messages_view_2)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    global cursor
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        today = datetime.now()
        data = [title, content, today]


        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            connection = sqlite3.connect("messages.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Messages_Register ('TITLE', 'CONTENT', 'DATE_TIME') VALUES (?, ?, ?)", (data))
            connection.commit()

            flash("The massage has been successfully saved")

            connection.close()

    return render_template('create.html')


@app.route('/read/', methods=('GET', 'POST'))
def read():
    if request.method == 'POST':
        id_search = request.form['id']

        if not id_search:
            flash('Id is required!')

        # conectamos con la base de datos
        connection = sqlite3.connect("messages.db")
        cursor = connection.cursor()

        messages_search = cursor.execute("SELECT * FROM Messages_Register WHERE ID= ?", (id_search,)).fetchall()

        if messages_search == []:
            flash("The id was not found in the Data Base")
            return redirect(url_for('read'))

        else:
            for user in messages_search:
                global search
                search = [{'title_search': user[1], 'content_search': user[2]}]

            return redirect(url_for('show'))

    return render_template('read_input.html')

@app.route('/show/')
def show():
    return render_template('read.html', we_search=search)


@app.route('/delete/', methods=('GET', 'POST'))
def delete():
    if request.method == 'POST':
        id_search = request.form.get('id')

        if not id_search:
            flash('Id is required!')

        connection = sqlite3.connect("messages.db")
        cursor = connection.cursor()
        messages_search = cursor.execute("SELECT * FROM Messages_Register WHERE ID= ?", (id_search,)).fetchall()
        connection.close()

        if messages_search == []:
            flash("The id was not found in the Data Base")
            return redirect(url_for('delete'))


        else:
            # conectamos con la base de datos
            connection = sqlite3.connect("messages.db")
            cursor = connection.cursor()

            cursor.execute("DELETE FROM Messages_Register WHERE ID= ?", (id_search,)).fetchall()

            connection.commit()  # confirmar cambios
            connection.close()  # cerrar conexion

            flash("Field deleted successfully")

    return render_template('delete_input.html')

@app.route('/update/', methods=('GET', 'POST'))
def update():
    if request.method == 'POST':

        id_search = request.form['id']

        if not id_search:
            flash('Id is required!')

        title = request.form['title']
        content = request.form['content']
        today = datetime.now()
        data = [title, content, today, id_search]
        print(data)

        connection = sqlite3.connect("messages.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE Messages_Register SET TITLE=?, CONTENT=?, DATE_TIME=? WHERE ID= ?",
                       (title, content, today, id_search,))
        connection.commit()

        flash("Report updated")

    return render_template('update.html')

if __name__ == '__main__':
    app.run(debug=True)


