from flask import render_template, request, redirect, Blueprint
from ..data.mongoDb import mongo
from flask_pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId
from ..data.Todo import Todo
import pprint

main = Blueprint('app', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/todos')
def list_todos():
    todos = mongo.db.todos.find({})
    print(f'Number of items: {todos.collection.count()}')
    return render_template('todos.html', list=todos.sort('dueDate', ASCENDING))

@main.route('/todos/create', methods=["GET","POST"])
def create_todo():
    if request.method == "POST":
        try:
            print(f"Saved {request.form['title']}")  
            todo = Todo.mapFromInput(request.form)
            mongo.db.todos.insert_one({'title': todo.title, 'description': todo.description, 'dueDate': todo.dueDate })
        except Exception as err:
            return f'Error processing the request. {err}'
        return redirect("/todos")
    else:
        return render_template('create.html')

@main.route('/todos/delete/<string:todo_id>')
def delete_todo(todo_id):
    print(f'Deleting {todo_id}')
    mongo.db.todos.find_one_and_delete({'_id': ObjectId(todo_id)})
    return redirect("/todos")

@main.route('/todos/edit/<string:todo_id>')
def find(todo_id):
    todo = mongo.db.todos.find_one({'_id': ObjectId(todo_id)})
    return render_template("edit.html", todo=Todo.mapFromDbModel(todo))