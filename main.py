# import libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# create flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

# connect to database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# configure a database table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return self.text


# home route shows the app page
@app.route("/")
def home():

    todo_list = Todo.query.all()
    return render_template("index.html", todos=todo_list)


# endpoint for creating and storing a new todo_item
@app.route("/add", methods=["POST"])
def add():

    if request.method == "POST":

        data = request.form
        task_name = data["title"]

        new_todo = Todo(
            text=task_name,
            complete=False
        )
        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for("home"))


# endpoint to check off a completed todo_item
@app.route("/update/<int:todo_id>")
def update(todo_id):

    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for("home"))


# endpoint for deleting a todo_item
@app.route("/delete/<int:todo_id>")
def delete(todo_id):

    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("home"))


# run Flask app in debug mode
if __name__ == "__main__":
    db.create_all()  # initialize and create the database
    app.run(debug=True)
