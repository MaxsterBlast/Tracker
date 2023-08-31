from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

papers = []

def save_data():
    with open('data.json', 'w') as f:
        json.dump(papers, f)

def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    sorted_by_date = sorted(papers, key=lambda x: x['due_date'])
    sorted_by_difficulty = sorted(papers, key=lambda x: x['difficulty'])

    return render_template('index.html', papers=sorted_by_date, papers_by_difficulty=sorted_by_difficulty)

@app.route('/submit', methods=['POST'])
def submit():
    paper = {
        'subject': request.form['subject'],
        'due_date': request.form['due_date'],
        'style': request.form['style'],
        'difficulty': request.form['difficulty'],
        'completed': False
    }
    papers.append(paper)
    save_data()
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    papers.pop(index)
    save_data()
    return redirect('/')

if __name__ == '__main__':
    papers = load_data()
    app.run(debug=True, host='0.0.0.0',port=5000)
