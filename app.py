from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'tasks.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.id} {self.title}>"

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/task/new', methods=['GET','POST'])
def new_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description','')
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_task.html')

@app.route('/task/<int:task_id>/edit', methods=['GET','POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description','')
        task.done = 'done' in request.form
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # ensure DB exists
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
