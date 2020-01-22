from flask import Flask, render_template, request, redirect
from data.mongoInit import initDB
from flask_pymongo import ASCENDING, DESCENDING
import datetime
from bson.objectid import ObjectId


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
            title = request.form['title']
            description = request.form['description']
            dueDateStr = request.form['dueDate']
            dueDate = datetime.datetime.strptime(dueDateStr, "%Y-%m-%d")
            mongo.db.todos.insert_one({'title': title, 'description': description, 'dueDate': dueDate })
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