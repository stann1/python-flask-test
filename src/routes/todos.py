from flask import render_template, request, redirect, Blueprint, current_app
from flask_pymongo import ASCENDING
from bson.objectid import ObjectId
from ..data.mongoDb import mongo
from ..data.Todo import Todo
#import pprint

todos_router = Blueprint('todos', __name__, url_prefix='/todos')

@todos_router.route('/')
def list_todos():
    todos = mongo.db.todos.find({})
    current_app.logger.debug(f'Number of items: {todos.collection.count()}')
    items_list = map(Todo.mapFromDbModel, todos.sort('dueDate', ASCENDING))
    return render_template('todos/list.html', list=items_list)

@todos_router.route('/create', methods=["GET", "POST"])
def create_todo():
    if request.method == "POST":
        try:
            current_app.logger.debug(f"Saved {request.form['title']}")  
            try:
                todo = Todo.mapFromInput(request.form)
            except AttributeError as err:
                return render_template('todos/create.html', error=err)

            mongo.db.todos.insert_one({
                'title': todo.title,
                'description': todo.description,
                'dueDate': todo.due_date})
        except Exception as err:
            print(f'Error processing the request. {err}')
            raise err
        
        return redirect("/todos")
    
    return render_template('todos/create.html')

@todos_router.route('/delete/<string:todo_id>')
def delete_todo(todo_id):
    current_app.logger.debug(f'Deleting {todo_id}')
    mongo.db.todos.find_one_and_delete({'_id': ObjectId(todo_id)})
    return redirect("/todos")

@todos_router.route('/edit/<string:todo_id>', methods=["GET", "POST"])
def edit(todo_id):
    if request.method == "GET":
        todo = mongo.db.todos.find_one({'_id': ObjectId(todo_id)})
        return render_template("todos/edit.html", todo=Todo.mapFromDbModel(todo))
    if request.method == "POST":
        edited_todo = Todo.mapFromInput(request.form)
        mongo.db.todos.find_one_and_update({'_id': ObjectId(todo_id)}, {
            '$set': {
                'title': edited_todo.title,
                'description': edited_todo.description,
                'dueDate': edited_todo.due_date
            }
        })
        return redirect("/todos")
    
    raise NotImplementedError 