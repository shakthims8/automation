from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

app = Flask(__name__)
redis = Redis(host='localhost', port=8080)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/edit')
def home1():
    todo_list = Todo.query.all()
    return render_template('base.html',todo_list=todo_list)

@app.route('/')
def list1():
    todo_list = Todo.query.all()
    hits = redis.incr('hits')
    return render_template('list.html',todo_list=todo_list)


@app.route('/add',methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home1"))    


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home1"))    


@app.route('/update/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home1"))


@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)     
    
