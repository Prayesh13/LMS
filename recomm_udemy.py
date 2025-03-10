import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process  # For fuzzy matching

# Step 1: Define the get_data() function to load data
def get_data(file_path="data/udemy_cleaned.csv"):
    """
    This function loads the CSV file containing Udemy courses data.
    :param file_path: Path to the CSV file.
    :return: A pandas DataFrame with the course data.
    """
    df = pd.read_csv(file_path)
    
    # Convert categorical text columns to lowercase for consistency
    df['subject'] = df['subject'].str.lower()
    df['level'] = df['level'].str.lower()
    df['course_title'] = df['course_title'].str.lower()
    
    # Select relevant features
    df_filtered = df[['course_id', 'course_title', 'is_paid', 'num_subscribers', 'num_reviews', 'subject', 'level', 'content_duration', 'price', 'url']].copy()
    
    return df_filtered

from sklearn.metrics.pairwise import cosine_similarity

# Step 2: Content-Based Filtering (CBF) Logic
def content_based_filtering(course_title, df_filtered, content_similarity, top_n=5):
    # Function for matching course titles (partial matching)
    def find_similar_course_title(user_input):
        # Direct substring match
        matching_courses = df_filtered[df_filtered['course_title'].str.contains(user_input.lower(), regex=True, na=False)]

        if not matching_courses.empty:
            return matching_courses.iloc[0]['course_title']

        # If no exact match, use fuzzy matching
        closest_match, score = process.extractOne(user_input, df_filtered['course_title'])

        if score > 60:  # Acceptable similarity threshold
            return closest_match

        return None  # No similar course found
    
    # calculating similarity
    def calculate_content_similarity(df_filtered):
        # Assuming we are using 'course_title' as the feature for similarity calculation
        # Convert text data into a suitable form (e.g., TF-IDF or embeddings)
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(df_filtered['course_title'])
        
        # Calculate cosine similarity
        content_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
        return content_similarity

    matched_course_title = find_similar_course_title(course_title)
    content_similarity = calculate_content_similarity(df_filtered)
    
    if not matched_course_title:
        print(f"Warning: No similar course found for '{course_title}'.")
        return []

    course_idx = df_filtered[df_filtered['course_title'] == matched_course_title].index[0]
    similarity_scores = list(enumerate(content_similarity[course_idx]))
    sorted_courses = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    return [df_filtered.iloc[i[0]]['course_title'] for i in sorted_courses]

# Step 3: Hybrid Recommendation Logic (CBF + CF)
def hybrid_recommendation(subject=None, level=None, course_title=None, content_similarity=None, top_n=5):
    df_filtered = get_data()
    if course_title and not subject and not level:
        # Only `course_title` given → Return Content-Based Filtering results
        return content_based_filtering(course_title.lower(), df_filtered, content_similarity, top_n=top_n)

    elif subject and level and not course_title:
        # Only `subject` and `level` given → Return Collaborative Filtering results
        cf_courses = df_filtered[
            df_filtered['subject'].str.contains(subject.lower(), case=False, na=False) &
            df_filtered['level'].str.contains(level.lower(), case=False, na=False)
        ]
        
        # Sort by number of subscribers and return top N
        cf_courses = cf_courses.sort_values(by='num_subscribers', ascending=False).head(top_n)
        
        # Return relevant columns
        return cf_courses[['course_id', 'course_title', 'subject', 'level', 'num_subscribers', 'price']]

    elif subject and level and course_title:
        # All three are given → Return Hybrid Recommendations
        cbf_courses = content_based_filtering(course_title.lower(), df_filtered, content_similarity, top_n=top_n)

        # Ensure `cbf_courses` is a DataFrame
        if isinstance(cbf_courses, list):
            cbf_courses = df_filtered[df_filtered['course_title'].isin(cbf_courses)]

        # Collaborative filtering recommendations
        cf_courses = df_filtered[(df_filtered['subject'] == subject.lower()) & 
                                 (df_filtered['level'] == level.lower())]
        cf_courses = cf_courses.sort_values(by='num_subscribers', ascending=False).head(top_n)

        # Combine both approaches
        hybrid_recommendations_index = pd.concat([cbf_courses, cf_courses], ignore_index=True).drop_duplicates().head(top_n).index
        return df_filtered.loc[hybrid_recommendations_index, ['course_id', 'course_title', 'subject', 'level', 'num_subscribers', 'price', 'url']]

    else:
        return "Error: Please provide at least a `course_title` or (`subject` and `level`)."
