from flask import render_template, request, redirect, Blueprint, current_app
from flask_pymongo import ASCENDING
from bson.objectid import ObjectId
from ..data.mongoDb import mongo
from ..data.Todo import Todo
#import pprint

main = Blueprint('app', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/todos')
def list_todos():
    todos = mongo.db.todos.find({})
    current_app.logger.debug(f'Number of items: {todos.collection.count()}')
    return render_template('todos.html', list=map(Todo.mapFromDbModel, todos.sort('dueDate', ASCENDING)))

@main.route('/todos/create', methods=["GET", "POST"])
def create_todo():
    if request.method == "POST":
        try:
            current_app.logger.debug(f"Saved {request.form['title']}")  
            todo = Todo.mapFromInput(request.form)
            mongo.db.todos.insert_one({
                'title': todo.title,
                'description': todo.description,
                'dueDate': todo.due_date})
        except Exception as err:
            print(f'Error processing the request. {err}')
            raise err
        return redirect("/todos")
    
    return render_template('create.html')

@main.route('/todos/delete/<string:todo_id>')
def delete_todo(todo_id):
    current_app.logger.debug(f'Deleting {todo_id}')
    mongo.db.todos.find_one_and_delete({'_id': ObjectId(todo_id)})
    return redirect("/todos")

@main.route('/todos/edit/<string:todo_id>', methods=["GET", "POST"])
def edit(todo_id):
    if request.method == "GET":
        todo = mongo.db.todos.find_one({'_id': ObjectId(todo_id)})
        return render_template("edit.html", todo=Todo.mapFromDbModel(todo))
    if request.method == "POST":
        edited_todo = Todo.mapFromInput(request.form)
        mongo.db.todos.find_one_and_update({'_id': ObjectId(todo_id)}, 
                {'$set': {
                    'title': edited_todo.title,
                    'description': edited_todo.description,
                    'dueDate': edited_todo.due_date
                }})
        return redirect("/todos")
    
    raise NotImplementedError 