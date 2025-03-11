import pandas as pd

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
    
    # Select relevant features
    df_filtered = df[['course_id', 'course_title', 'is_paid', 'num_subscribers', 'num_reviews', 'subject', 'level', 'content_duration', 'price', 'url']].copy()
    
    return df_filtered

# Step 2: Collaborative Filtering (CF) Logic
def collaborative_filtering(subject, level, top_n=5):
    df_filtered = get_data()
    
    # Filter courses based on subject and level
    cf_courses = df_filtered[
        (df_filtered['subject'].str.contains(subject.lower(), case=False, na=False)) &
        (df_filtered['level'].str.contains(level.lower(), case=False, na=False))
    ]
    
    # Sort by number of subscribers and return top N
    cf_courses = cf_courses.sort_values(by='num_subscribers', ascending=False).head(top_n)
    
    # Return relevant columns
    return cf_courses[['course_id', 'course_title', 'subject', 'level', 'num_subscribers', 'price', 'url']]

# Step 3: Recommendation Function
def get_recommendations(subject=None, level=None, top_n=5):
    if subject and level:
        return collaborative_filtering(subject, level, top_n)
    else:
        return "Error: Please provide both `subject` and `level`."
