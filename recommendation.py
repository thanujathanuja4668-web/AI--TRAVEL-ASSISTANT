import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load travel dataset
def load_data():
    data = pd.read_csv("travel_data.csv")
    return data


# Recommend travel destinations
def recommend_places(budget, days, interest):

    data = load_data()

    # Filter destinations by budget, duration, and interest
    filtered_data = data[
        (data["budget_per_day"] <= budget) &
        (data["days"] <= days) &
        (data["interests"].str.contains(interest, case=False, na=False))
    ].copy()

    if filtered_data.empty:
        return "No matching destinations found. Try increasing your budget or trip duration."

    # Convert destination interests into numerical values
    vectorizer = TfidfVectorizer()

    interest_matrix = vectorizer.fit_transform(
        filtered_data["interests"].fillna("")
    )

    user_vector = vectorizer.transform([interest])

    # Calculate similarity
    similarity = cosine_similarity(
        user_vector, interest_matrix
    ).flatten()

    filtered_data["score"] = similarity

    # Sort destinations by similarity score
    recommendations = filtered_data.sort_values(
        by="score", ascending=False
    )

    # Remove duplicate destinations
    recommendations = recommendations.drop_duplicates(
        subset=["destination"]
    )

    # Return top 5 destinations
    return recommendations[
        ["destination", "budget_per_day", "days", "interests"]
    ].head(5)