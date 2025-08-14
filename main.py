import flask
from flask import Flask, render_template
from db import create_table, add_todo, get_all_todos, complete_todo, delete_todo
app = Flask(__name__)

create_table()

@app.route('/')
def home():
    todos = get_all_todos()
    # make a dictionary 
    for i in range(len(todos)):
        todos[i] = {
            'id': todos[i][0],
            'task': todos[i][1],
            'completed': todos[i][2]
        }
    return render_template('home.html', todos=todos)
    

@app.route('/add_todo', methods=['POST'])
def add_todo_route():
    task = flask.request.form.get('task')
    if task:
        add_todo(task)
    return flask.redirect(flask.url_for('home'))


@app.route('/complete_todo/<int:todo_id>', methods=['POST'])
def complete_todo_route(todo_id):
    complete_todo(todo_id)
    return flask.redirect(flask.url_for('home'))

@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo_route(todo_id):
    delete_todo(todo_id)
    return flask.redirect(flask.url_for('home'))


if __name__=="__main__":
    app.run(debug=True)