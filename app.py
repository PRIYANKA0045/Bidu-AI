import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# API KEY AND MODEL SETUP (IMPORTANT!)
load_dotenv()

# Retrieve the key from the environment variables
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

# Initialize the Gemini Client
try:
    if not API_KEY:
        st.error("Ruk jaao, shehzaade! API Key missing hai. Please insert your key at the top of the script.")
        # Prevent further execution if key is missing
        st.stop()
    
    # Initialize client once
    gemini_client = genai.Client(api_key=API_KEY)

except Exception as e:
    st.error(f"Client initialization mein gadbad (Error): {e}")
    st.stop()


# HELPER FUNCTION: Defines the AI Persona
def create_prompt(topic: str) -> str:
    """Creates the detailed instruction set for the model's Bollywood persona."""
    return f"""
System Instruction: 
You are an AI specifically designed to answer technical questions related to AI, ML, IoT, cybersecurity, blockchain, etc., 
in a simple and easy-to-understand manner. You MUST respond in a dramatic Bollywood style, using Romanized Hindi (Hindi written using English alphabets), 
movie references, iconic dialogues, and dramatic expressions.

Your response MUST follow these rules:
1. Provide a clear and concise explanation of the core concepts of the question's topic.
2. Include at least two paragraphs of detailed explanation, using Bollywood-style dramatization.
3. Use Bollywood references, movie references, and Hindi language to make it engaging and memorable.
4. If the question is NOT technical, simply reply with the Hindi dialogue: "Mai sirf technical sawalon ke jawab deta hoon."
5. When the user's input is a simple greeting (like 'hello' or 'namaste'), reply with: "Mai Bidu AI Naam toh suna hoga."
6. When the user's input is a simple farewell (like 'bye' or 'alvida'), respond with: "Alvida."
7. If foul language is detected in the user's 'Question', you MUST respond with the Hindi dialogue: "Krupaya tameez se baat kijiye."

Question: {topic}

Bollywood Style Answer in Romanized Hindi:
"""

# STREAMLIT UI SETUP

st.set_page_config(page_title="🎬 Bolly Chat Bot", layout="centered")

st.markdown("""
<style>
.st-emotion-cache-p5m94y {
    background-color: #fce8a6; /* Light yellow background for the whole page */
    padding: 20px;
    border-radius: 10px;
}
h1 {
    color: #E91E63; /* Deep pink title */
    text-align: center;
    text-shadow: 2px 2px 4px #000000;
}
.stButton>button {
    background-color: #FF9800; /* Orange button */
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    transition: background-color 0.3s;
}
.stButton>button:hover {
    background-color: #F57C00; /* Darker orange on hover */
}
.st-emotion-cache-1cyn8z {
    border: 3px solid #E91E63; /* Pink border for text area */
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Bolly Chat Bot - Tech Ka Sultan!")
st.write("Janaab, koi bhi **technical sawal** puchiye (AI, ML, Cybersecurity). Jawab milega, woh bhi poora **Bollywood style** mein! 🍿✨")

# User input
user_input = st.text_area(
    "Enter your question (Topic for Bidu AI):", 
    height=150, 
    placeholder="Example: Explain the concept of Quantum Computing."
)

if st.button(" Generate Bollywood Response (Awaaz Do!)"):
    topic = user_input.strip()
    if not topic:
        st.warning("Arre yaar! Pehle kuch likho toh sahi. Sawal ke bina jawab kaisa?")
    else:
        with st.spinner("Bidu AI soch raha hai... Kisi film ki kahani se kam nahi hoga jawab! 🎬"):
            try:
                # 1. Generate the detailed prompt including all instructions
                prompt = create_prompt(topic)
                
                # 2. Call the native Gemini API
                response = gemini_client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                )
                answer = response.text.strip()
                
                # Check for model safety blocks 
                if not answer and response.prompt_feedback.block_reason:
                    answer = f"**Model Blocked:** (Yeh sawal thoda khatarnak tha!) Reason: {response.prompt_feedback.block_reason.name}"
                
                # 3. Display the answer
                st.markdown("###  Bollywood Style Answer")
                st.success(answer)

            except Exception as e:
                # General error handling
                st.error(f"Bidu AI ko gussa aa gaya (Unexpected Error). Details: {str(e)}")
                print(f"General Error Details: {e}")

