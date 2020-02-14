import datetime

class Todo:
    id = None
    title = None
    description = None
    dueDate = None

    def __init__(self, title, description, dueDate, id=None):
        self.title = title
        self.description = description
        self.dueDate = dueDate
        self.id = id
    
    @staticmethod
    def mapFromDbModel(model):
        id = str(model['_id'])
        title = model['title']
        description = model['description']
        dueDate = datetime.datetime.date(model['dueDate'])

        return Todo(title, description, dueDate, id)
    
    @staticmethod
    def mapFromInput(form):
        title = form['title']
        description = form['description']
        dueDateStr = form['dueDate']
        dueDate = datetime.datetime.strptime(dueDateStr, "%Y-%m-%d") if dueDateStr else None

        return Todo(title, description, dueDate)