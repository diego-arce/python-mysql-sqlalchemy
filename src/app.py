from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuariomariadb:clavemariadb@localhost/basemariadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(100))
    author = db.Column(db.String(20))
    date = db.Column(db.Date)
    
    def __init__(self, title, description, author, date):
        self.title = title
        self.description = description
        self.author = author
        self.date = date

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'author', 'date')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']
    date = request.json['date']

    new_task = Task(title, description, author, date)
    db.session.add(new_task)
    db.session.commit()

    print(request.json)
    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']
    author = request.json['author']
    date = request.json['date']

    task.title = title
    task.description = description
    task.author = author
    task.date = date

    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': "Welcome to my API"})
    
if __name__ == "__main__":
    app.run(debug=True)