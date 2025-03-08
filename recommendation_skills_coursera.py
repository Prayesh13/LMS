from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_data():
    df_cleaned = pd.read_csv("data/Coursera_cleaned.csv")
    return df_cleaned

# Step 1: Preprocessing the user input skills
def preprocess_user_skills(user_skills):
    # the input is a string
    return " ".join(user_skills) if isinstance(user_skills, set) else user_skills

# Step 2: Vectorize skills using TF-IDF
def vectorize_skills(df):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    skills_matrix = tfidf_vectorizer.fit_transform(df['Skills'])
    return tfidf_vectorizer, skills_matrix

# Step 3: Calculate cosine similarity between user skills and course skills
def calculate_cosine_similarity(user_skills_vector, skills_matrix):
    return cosine_similarity(user_skills_vector, skills_matrix)

# Step 4: Filter and rank courses based on similarity and rating
def filter_and_rank_courses(df, sim_scores, rating_threshold=4, top_n=5):
    # Sort the courses based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:top_n]  # Get top N similar courses

    # Extract course indices
    course_indices = [i[0] for i in sim_scores]
    
    # Get the courses corresponding to the indices
    recommended_courses = df.iloc[course_indices]
    
    # Apply rating threshold (filter courses with ratings below the threshold)
    recommended_courses = recommended_courses[recommended_courses['Rating'] >= rating_threshold]
    
    # Sort by rating (descending)
    recommended_courses = recommended_courses.sort_values(by='Rating', ascending=False)
    
    return recommended_courses[['Name', 'University', 'Difficulty Level', 'Rating', 'URL','Description', 'Skills']]

# Step 5: Combine all steps into a pipeline
def recommend_courses_pipeline(user_skills, top_n=5, rating_threshold=4):
    try:
        # get the data
        df = get_data()
        # Preprocess the user input skills
        user_skills = preprocess_user_skills(user_skills)

        # Vectorize skills and calculate similarity
        tfidf_vectorizer, skills_matrix = vectorize_skills(df)
        user_skills_vector = tfidf_vectorizer.transform([user_skills])  # Convert user skills to vector
        cosine_sim = calculate_cosine_similarity(user_skills_vector, skills_matrix)

        # Get the top N recommended courses based on skills similarity and rating
        recommended_courses = filter_and_rank_courses(df, list(enumerate(cosine_sim[0])), rating_threshold, top_n)
        
        return recommended_courses
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# # enter user skills
# user_skills = "communication"

# recommended_courses = recommend_courses_pipeline(user_skills=user_skills, top_n=5, rating_threshold=4)

# print(recommended_courses)