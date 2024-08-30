from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = request.form.get('filename', 'student_data.txt')
    data = []
    sorted_data = []
    
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = [line.strip().split(',') for line in file.readlines()]

    if request.method == 'POST':
        if 'submit' in request.form:
            roll_no = request.form['roll_no']
            name = request.form['name']
            student_class = request.form['class']
            avg_mark = request.form['avg_mark']
            remark = request.form['remark']
            filename = request.form['filename']

            details = f"{roll_no},{name},{student_class},{avg_mark},{remark}\n"
            
            with open(filename, "a") as file:
                file.write(details)
            
            return redirect(url_for('index'))

    return render_template('index.html', data=data, filename=filename, sorted_data=sorted_data)

@app.route('/sort', methods=['GET'])
def sort_data():
    sort_by = request.args.get('sort_by')
    filename = request.args.get('filename')
    sorted_filename = f"sorted_{filename}"

    if not os.path.exists(filename):
        return "File does not exist. Please enter data first."

    with open(filename, "r") as file:
        lines = file.readlines()

    sort_index = {
        "Roll No": 0,
        "Name": 1,
        "Class": 2,
        "Avg Mark": 3,
        "Remark": 4
    }[sort_by]

    def convert_key(line):
        parts = line.split(",")
        if sort_by in ["Roll No", "Avg Mark"]:
            return float(parts[sort_index]) if parts[sort_index].strip() else 0
        return parts[sort_index]

    sorted_lines = sorted(lines, key=convert_key)

    with open(sorted_filename, "w") as file:
        file.writelines(sorted_lines)

    with open(sorted_filename, 'r') as file:
        sorted_data = [line.strip().split(',') for line in file.readlines()]
    
    return render_template('index.html', sorted_data=sorted_data, filename=sorted_filename)

if __name__ == '__main__':
    app.run(debug=True)
