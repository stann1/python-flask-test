import datetime

class Todo:
    def __init__(self, title, description, due_date, _id=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self._id = _id
    
    @staticmethod
    def mapFromDbModel(model):
        _id = str(model['_id'])
        title = model['title']
        description = model['description']
        due_date = datetime.datetime.date(model['dueDate'])

        return Todo(title, description, due_date, _id)
    
    @staticmethod
    def mapFromInput(form):
        title = form['title']
        description = form['description']
        due_date_str = form['due_date']
        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None

        return Todo(title, description, due_date)
