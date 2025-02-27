from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/digital_footprints')
def digital_footprints():
    return render_template('digital_footprints.html')

# Function to get subjects from SQLite
def get_subjects(branch, semester):
    conn = sqlite3.connect('lms_portal.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access
    cursor = conn.cursor()
    cursor.execute("SELECT name, resources FROM subjects WHERE branch = ? AND semester = ?", (branch, semester))
    subjects = cursor.fetchall()
    conn.close()
    return subjects

@app.route('/core_skills', methods=['GET', 'POST'])
def core_skills():
    subjects = []
    if request.method == 'POST':
        branch = request.form.get('branch')
        semester = request.form.get('semester')
        if branch and semester:
            subjects = get_subjects(branch, semester)
    return render_template('core_skills.html', subjects=subjects)

@app.route('/process-management')
def process_management():
    return render_template('process_management.html')

@app.route('/communication-skills')
def communication_skills():
    # Placeholder for recommending YouTube videos
    videos = [
        {"title": "How to Improve Communication Skills", "url": "https://www.youtube.com/watch?v=1z5f1x1CzxI"},
        {"title": "Effective Communication for Professionals", "url": "https://www.youtube.com/watch?v=2pHXzWjOY7U"},
        {"title": "Mastering Workplace Communication", "url": "https://www.youtube.com/watch?v=3HYf5cK6fU"}
    ]
    return render_template('communication_skills.html', videos=videos)

@app.route('/core-skills/subjects-and-courses', methods=['GET', 'POST'])
def subjects_and_courses():
    departments = ["Computer Science", "Mechanical", "Electrical", "Civil"]
    years = ["First Year", "Second Year", "Third Year", "Final Year"]
    subjects = {}
    courses = {}

    if request.method == 'POST':
        selected_department = request.form.get('department')
        selected_year = request.form.get('year')

        # Populate subjects and courses dynamically based on the department and year
        subjects = {
            "First Year": ["Mathematics", "Physics", "Basic Programming"],
            "Second Year": ["Data Structures", "Thermodynamics", "Circuit Theory"],
            "Third Year": ["Algorithms", "Fluid Mechanics", "Control Systems"],
            "Final Year": ["Machine Learning", "Project Management", "Power Systems"]
        }
        courses = {
            "First Year": ["Introduction to Python", "Engineering Drawing"],
            "Second Year": ["Object-Oriented Programming", "Strength of Materials"],
            "Third Year": ["Advanced Algorithms", "Robotics"],
            "Final Year": ["Deep Learning", "Entrepreneurship"]
        }

        return render_template('subjects_courses.html',
                               department=selected_department,
                               year=selected_year,
                               subjects=subjects.get(selected_year, []),
                               courses=courses.get(selected_year, []))

    return render_template('subjects_courses.html', departments=departments, years=years)

if __name__ == '__main__':
    app.run(debug=True, port=5001)