def delete_todo_user(username, todo_id, data):
    """Deletes a todo for the given user."""
    if username not in data or todo_id >= len(data[username]['todos']):
        return False, data  # User does not exist or todo_id is invalid
    del data[username]['todos'][todo_id]
    return True, data
def make_new_user(username,password,data):
    """
    Creates a new user with the given username and password.
    """
    if username in data:
        return False,data  # User already exists
    data[username] = {'password': password, 'todos': []}
    return True, data
    


def get_all_todos_user(username, data):
    """
    Returns all todos for the given user.
    """
    if username not in data:
        return []
    return data[username]['todos']

def add_todo_user(username, task, data):
    """
    Adds a todo for the given user.
    """
    if username not in data:
        return False, data  # User does not exist
    todo = {'task': task, 'completed': False}
    data[username]['todos'].append(todo)
    return True, data
def complete_todo_user(username, todo_id, data):
    """Completes a todo for the given user.
    """
    if username not in data or todo_id >= len(data[username]['todos']):
        return False, data  # User does not exist or todo_id is invalid
    data[username]['todos'][todo_id]['completed'] = True
    return True, data