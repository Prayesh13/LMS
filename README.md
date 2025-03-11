# LMS Recommendation System

This is a course recommendation system built with Flask. The project uses datasets containing information about online education courses from Udemy and Coursera to recommend courses to users based on their skills and preferences.

## Features
- **Udemy Course Recommendations**: Provides personalized course suggestions from Udemy based on user interests and skills.
- **Coursera Course Recommendations**: Recommends courses from Coursera tailored to users' profiles and skills.
- **Skills Matrix**: Maps and suggests courses based on the skills that the user wants to learn.
- **Web Interface**: A user-friendly web interface built with HTML, CSS, and Flask, with Bootstrap for easy navigation and interaction.

## Dataset
The project uses the following dataset files:
1. **Coursera.csv**: Contains raw data about Coursera courses, including course title, category, and other metadata.
2. **Coursera_cleaned.csv**: Cleaned dataset for Coursera courses, preprocessed for recommendation.
3. **Udemy_cleaned.csv**: Cleaned dataset for Udemy courses, preprocessed for recommendation.
4. **udemy_online_education_courses_dataset.csv**: Raw dataset containing information about Udemy online education courses.

## How It Works
The recommendation system uses a combination of skills-based filtering and metadata-based filtering to suggest courses. It processes the user's input about their skills or interests, then finds the most relevant courses from the datasets. 

### Steps:
1. The user selects or enters their skill preferences.
2. The system matches the user’s input with relevant courses in the Coursera and Udemy datasets.
3. The system recommends courses from both platforms based on the input data, using pre-trained models such as `skills_matrix.pkl` and `tfidf_vectorizer.pkl`.

### Files & Modules:
- **app.py**: The main Flask application that runs the web service and integrates with the recommendation logic.
- **recomm_udemy.py**: Contains the recommendation logic for Udemy courses.
- **recommendation_skills_coursera.py**: Contains the recommendation logic for Coursera courses.
- **models/skills_matrix.pkl**: Pre-trained model for skill-based course recommendations.
- **models/tfidf_vectorizer.pkl**: TF-IDF vectorizer used to process course descriptions and titles.
- **notebooks**: Contains Jupyter notebooks for exploring and developing the recommendation models.
  
## Live Demo
You can try the LMS Recommendation System live at [https://student-partner.onrender.com/](https://student-partner.onrender.com/).

## Requirements
To run the project locally, make sure you have the following dependencies installed:
- Flask
- Pandas
- Scikit-learn
- Pickle
- Jupyter (for notebooks)

You can install the necessary dependencies by running:

```
pip install -r requirements.txt
```
