import streamlit as st
from google import genai
from google.genai import errors
import time
import os


def get_travel_response(user_message):

    try:
        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY") or
            st.secrets["GEMINI_API_KEY"]
        )

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=f"""
                    You are a helpful AI Travel Assistant.

                    Help users with:
                    1. Tourist destinations
                    2. Travel itineraries
                    3. Trip budgets
                    4. Hotel suggestions
                    5. Food recommendations
                    6. Travel tips

                    Give clear and simple answers.

                    User question: {user_message}
                    """
                )

                return response.text

            except errors.APIError as e:

                if e.code in [429, 500, 502, 503, 504]:
                    if attempt < 2:
                        time.sleep(3 * (attempt + 1))
                        continue

                    return (
                        "Gemini is currently experiencing high demand. "
                        "Please wait a little and try again."
                    )

                return f"Gemini API error: {e}"

    except Exception as e:
        return f"Something went wrong: {e}"

    return "Please try again later."
