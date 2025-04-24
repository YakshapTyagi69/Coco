from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load existing reports
if os.path.exists('reports.json'):
    with open('reports.json', 'r') as f:
        reports = json.load(f)
else:
    reports = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    desc = request.form['description']
    loc = request.form['location']
    rtype = request.form['type']
    file = request.files['image']

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    report = {
        'description': desc,
        'location': loc,
        'type': rtype,
        'image': filename,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    reports.append(report)

    with open('reports.json', 'w') as f:
        json.dump(reports, f, indent=2)

    return redirect(url_for('index'))

@app.route('/reports')
def view_reports():
    return render_template('reports.html', reports=reports)

if __name__ == '__main__':
    app.run(debug=True)
