from flask import Flask, render_template, request
from recommendation_skills_coursera import recommend_courses_pipeline

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/digital_footprints')
def digital_footprints():
    return render_template('digital_footprints.html')

@app.route('/course-recommendation', methods=['GET', 'POST'])
def course_recommendation():
    recommended_courses = None
    user_skills = ""
    
    if request.method == 'POST':
        user_skills = request.form.get('skills')  # Get user input from form
        if user_skills:
            recommended_courses = recommend_courses_pipeline(user_skills, top_n=6, rating_threshold=4)
    
    return render_template('course_recommendation.html', courses=recommended_courses, user_skills=user_skills)


@app.route('/communication-skills')
def communication_skills():
    # Placeholder for recommending YouTube videos
    videos = [
        {"title": "How to Improve Communication Skills", "url": "https://www.youtube.com/watch?v=1z5f1x1CzxI"},
        {"title": "Effective Communication for Professionals", "url": "https://www.youtube.com/watch?v=2pHXzWjOY7U"},
        {"title": "Mastering Workplace Communication", "url": "https://www.youtube.com/watch?v=3HYf5cK6fU"}
    ]
    return render_template('communication_skills.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True, port=5001)