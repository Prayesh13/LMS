from flask import Flask, render_template, request
from recommendation_skills_coursera import recommend_courses_pipeline
from recomm_udemy import hybrid_recommendation

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
        {"title": "Communication Skills - The 6 Keys Of Powerful Communication", "url": "https://youtu.be/XCc6-qr0Gww?si=GaGwLr_o_R7QZ-hf","Channel": "Actualized.org"},
        {"title": "Communication Skills SIMPLIFIED: A Step-by-Step Roadmap for Success", "url": "https://youtu.be/X3Fz_Gu5WUE?si=Id0rhYkGljNQzUPY","Channel": "Simerjeet Singh"},
        {"title": "TOP 3 Tips To Improve Your Communication Skills!", "url": "https://youtu.be/LsyfrGnBL4c?si=sF5Zii9h4nTBy_ai","Channel": "Vanessa Van Edwards"},
        {"title": "Effective Communication Skills", "url": "https://youtu.be/6pYSbdGiDYw?si=_rxUHf3Jdz5y7ESf","Channel": "Communication Coach Alexander Lyon"}
    ]
    return render_template('communication_skills.html', videos=videos)


@app.route('/udemy-recommendation', methods=['GET', 'POST'])
def udemy_recommendation():
    recommended_courses = None
    user_query = ""
    user_subject = ""
    user_level = ""

    if request.method == 'POST':
        # Get user inputs from form
        user_query = request.form.get('course_title')  
        user_subject = request.form.get('subject')
        user_level = request.form.get('level')
        
        if user_query and user_subject and user_level:
            # Assuming `recommend_udemy_courses` is a function that returns recommended courses based on the input
            recommended_courses = hybrid_recommendation(user_query, user_subject, user_level, top_n=6)
    
    return render_template('udemy_recommendation.html', 
                           courses=recommended_courses, 
                           user_query=user_query, 
                           user_subject=user_subject, 
                           user_level=user_level)

if __name__ == '__main__':
    app.run(debug=True, port=5001)