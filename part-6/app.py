from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

TASKS = [
    {'id': 1, 'title': 'Learn Flask', 'status': 'Completed', 'priority': 'High'},
    {'id': 2, 'title': 'Build To-Do App', 'status': 'In Progress', 'priority': 'Medium'},
    {'id': 3, 'title': 'Push to GitHub', 'status': 'Pending', 'priority': 'Low'},
]


# HOME – LIST TASKS (WITH PRIORITY FILTER)
@app.route('/')
def home():
    priority = request.args.get('priority')
    if priority:
        filtered = [t for t in TASKS if t['priority'] == priority]
    else:
        filtered = TASKS
    return render_template('index.html', tasks=filtered)


# ADD TASK
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        new_task = {
            'id': len(TASKS) + 1,
            'title': request.form['title'],
            'status': request.form['status'],
            'priority': request.form['priority']
        }
        TASKS.append(new_task)
        return redirect(url_for('home'))
    return render_template('add.html')


# VIEW TASK
@app.route('/task/<int:id>')
def task_detail(id):
    task = next((t for t in TASKS if t['id'] == id), None)
    return render_template('task.html', task=task)


# EDIT TASK
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = next((t for t in TASKS if t['id'] == id), None)
    if request.method == 'POST':
        task['title'] = request.form['title']
        task['status'] = request.form['status']
        task['priority'] = request.form['priority']
        return redirect(url_for('home'))
    return render_template('edit.html', task=task)


# DELETE TASK
@app.route('/delete/<int:id>')
def delete_task(id):
    global TASKS
    TASKS = [t for t in TASKS if t['id'] != id]
    return redirect(url_for('home'))


# DASHBOARD
@app.route('/dashboard')
def dashboard():
    total = len(TASKS)
    completed = len([t for t in TASKS if t['status'] == 'Completed'])
    pending = len([t for t in TASKS if t['status'] == 'Pending'])
    progress = len([t for t in TASKS if t['status'] == 'In Progress'])

    return render_template(
        'dashboard.html',
        total=total,
        completed=completed,
        pending=pending,
        progress=progress
    )


# ABOUT
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
