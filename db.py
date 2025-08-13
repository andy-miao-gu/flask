import sqlite3 as sql


def create_table():
    connection = sql.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    connection.commit()
    connection.close()

def add_todo(task):
    connection = sql.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO todos (task) VALUES (?)', (task,))
    connection.commit()
    connection.close()

def get_all_todos():
    connection = sql.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = cursor.fetchall()
    connection.close()
    return todos
def complete_todo(todo_id):
    connection = sql.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE todos SET completed = 1 WHERE id = ?', (todo_id,))
    connection.commit()
    connection.close()

def delete_todo(todo_id):
    connection = sql.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    connection.commit()
    connection.close()