from flask import Flask, render_template, request, redirect
from data.mongoInit import initDB
from flask_pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId
from data.Todo import Todo


app = Flask(__name__)
mongo = initDB(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todos')
def list_todos():
    todos = mongo.db.todos.find({})
    print(todos.collection.count())
    return render_template('todos.html', list=todos.sort('dueDate', ASCENDING))

@app.route('/todos/create', methods=["GET","POST"])
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

@app.route('/todos/delete/<string:todo_id>')
def delete_todo(todo_id):
    print(f'Deleting {todo_id}')
    mongo.db.todos.find_one_and_delete({'_id': ObjectId(todo_id)})
    return redirect("/todos")


if(__name__ == "__main__"):
    app.run(debug=True) 