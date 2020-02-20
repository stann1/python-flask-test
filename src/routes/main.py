from flask import render_template, Blueprint

main = Blueprint('app', __name__)

@main.route('/')
def index():
    return render_template('index.html')