import streamlit as st
import pandas as pd

from chatbot import get_travel_response
from recommendation import recommend_places


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
    layout="wide"
)


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>

.stApp {
    background-color: #eaf5e9;
}

h1, h2, h3 {
    color: #174d32;
}

.stButton > button {
    background-color: #176b45;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #104d31;
    color: white;
}

.destination-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #c5dfc8;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- MAIN TITLE ----------------

st.title("✈️ AI Travel Assistant")
st.subheader("Your personal AI-powered travel planner")

st.write(
    "Plan your trips, explore destinations and "
    "discover places according to your budget and interests."
)


# ---------------- NAVIGATION ----------------

page = st.sidebar.radio(
    "Choose a Service",
    [
        "🏠 Home",
        "🤖 AI Travel Chatbot",
        "🌍 Destination Recommendation"
    ]
)


# ---------------- HOME PAGE ----------------

if page == "🏠 Home":

    st.header("Welcome to AI Travel Assistant!")

    st.write("""
    This application helps travellers plan their trips
    easily using Artificial Intelligence and Machine Learning.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="destination-card">
        <h3>🤖 AI Travel Chatbot</h3>
        <p>Ask questions about destinations, hotels,
        transportation, food and travel budgets.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="destination-card">
        <h3>🌍 Destination Recommendation</h3>
        <p>Discover destinations based on your budget,
        trip duration and travel interests.</p>
        </div>
        """, unsafe_allow_html=True)

    st.success("Start exploring your next travel destination!")


# ---------------- AI CHATBOT PAGE ----------------

elif page == "🤖 AI Travel Chatbot":

    st.header("🤖 AI Travel Chatbot")

    st.write(
        "Ask me anything about your travel plans!"
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_message = st.chat_input(
        "Example: Suggest a 2-day Mysore trip within ₹5000"
    )

    if user_message:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        with st.chat_message("user"):
            st.markdown(user_message)

        with st.chat_message("assistant"):

            with st.spinner("Planning your trip..."):

                response = get_travel_response(user_message)

            st.markdown(response)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })


# ---------------- DESTINATION RECOMMENDATION ----------------

elif page == "🌍 Destination Recommendation":

    st.header("🌍 Find Your Perfect Travel Destination")

    st.write(
        "Find destinations based on your budget, "
        "trip duration and interests."
    )

    st.markdown("### Enter Your Travel Preferences")

    budget = st.number_input(
        "💰 Budget per day (₹)",
        min_value=500,
        max_value=50000,
        value=2000,
        step=500
    )

    days = st.number_input(
        "📅 Trip Duration (Days)",
        min_value=1,
        max_value=30,
        value=2,
        step=1
    )

    interest = st.selectbox(
        "❤️ Choose Your Interest",
        [
            "Nature",
            "Heritage",
            "Adventure",
            "Beach",
            "Trekking",
            "Sightseeing"
        ]
    )

    if st.button("🔍 Recommend Destination"):

        with st.spinner("Finding the best destinations for you..."):

            try:

                results = recommend_places(
                    budget,
                    days,
                    interest
                )

                if isinstance(results, str):

                    st.warning(results)

                elif isinstance(results, pd.DataFrame) and not results.empty:

                    st.success("Your Recommended Destinations")

                    columns = st.columns(2)

                    for index, (_, place) in enumerate(
                        results.iterrows()
                    ):

                        with columns[index % 2]:

                            st.markdown(
                                f"""
                                <div class="destination-card">
                                <h3>📍 {place['destination']}</h3>
                                <p>💰 Budget per day:
                                ₹{place['budget_per_day']}</p>
                                <p>📅 Suggested duration:
                                {place['days']} days</p>
                                <p>❤️ Interests:
                                {place['interests']}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                else:

                    st.warning(
                        "No matching destinations found. "
                        "Try changing your budget or interests."
                    )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "AI Travel Assistant | BCA Final Year Project | "
    "Python, Streamlit, Gemini API and Machine Learning"
)