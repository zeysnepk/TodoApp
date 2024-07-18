from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # Create a new Flask application instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/zeynepkaplan/Desktop/Projects/TodoApp/todo.db' # Set the database URI
db = SQLAlchemy(app) # Initialize SQLAlchemy

class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key=True) # Unique ID for each todo
    task = db.Column(db.String(100), nullable=False) # Title of the todo
    is_complete = db.Column(db.Boolean, default=False) # Whether the todo is completed or not
   
with app.app_context(): # Ensure the application context is running when creating tables in a Flask extension
    db.create_all() # Create the database tables if they don't exist yet
    
@app.route('/') # Define the route for the main page
def index():
    todos = Todo.query.all() # Get all the todo items from the database
    return render_template('index.html',todos=todos) # Render the index.html template with the todo items

@app.route("/add", methods=['POST']) # Define the route for adding a new todo item
def add():
    task = request.form.get("task") # Get the task from the form submission
    newTask = Todo(task=task) # Create a new Todo object with the task from the form submission
    db.session.add(newTask) # Add the new todo to the database session
    db.session.commit() # Commit the changes to the database
    return redirect(url_for('index'))

@app.route("/complete/<string:id>") # Define the route for marking a todo item as completed or not
def complete(id):
    todo = Todo.query.filter_by(id=id).first() # Get the todo item with the specified ID from the database
    if todo.is_complete:
        todo.is_complete = False # Mark the todo as not completed
    else:
        todo.is_complete = True # Mark the todo as completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<string:id>") # Define the route for deleting a todo item
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo) # Delete the todo from the database session
    db.session.commit()
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True) # Run the Flask application
    