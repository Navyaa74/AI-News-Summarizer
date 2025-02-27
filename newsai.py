import streamlit as st
import google.generativeai as genai
import newspaper
from newspaper import Article
import os
from dotenv import load_dotenv 

#Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def fetch_news(url):
    #extracts article text from a news URL
    article=Article(url)
    article.download()
    article.parse()
    return article.text
def summarize_news(text):
    #uses gemini api to summarixe the extraxted news text
    model= genai.GenerativeModel("gemini-pro")
    response =model.generate_content(text)
    return response.text.strip()

# Streamlit UI
st.set_page_config(page_title="AI News Summarizer", page_icon="📰", layout="centered")
st.title("📜 AI Quick News")
st.write("Kindly Enter news article link for summarization.")
# CSS Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #5cffd3, #16a881);
        color: white;
    }
    h1 {
        text-align: center;
        color: white;
    }
    div.stButton > button {
        background-color: #f5f5ae !important;
        color: black !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        border: 2px solid #ffaa00 !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #5effda !important;
        color: white !important;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)


# User input
url = st.text_input("Enter news article URL:", "")

if st.button("brief news"):
    if url:
        with st.spinner("Fetching and summarizing the article..."):
            news_text = fetch_news(url)
            if news_text.startswith("Error"):
                st.error("Failed to fetch article. Check the URL.")
            else:
                st.subheader("Original Article (Preview):")
                st.write(news_text[:500] + "...")
                
                summary = summarize_news(news_text)
                st.subheader("Summarized Article:")
                st.write(summary)
    else:
        st.warning("Please enter a valid URL.")


