import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# ========================== SETUP ==========================

# ✅ Replace with your real Gemini API key here
MODEL_NAME = "gemini-1.5-flash"

# Check API key is set
if not API_KEY:
    raise ValueError("API_KEY must be provided.")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# ========================== CLIENT SETUP ==========================

# Create a Gemini client with desired config
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={"temperature": 0.7},
)

# ========================== STREAMLIT UI ==========================

st.set_page_config(page_title="Image Caption Generator", layout="centered")
st.title("🖼️ Image Caption Generator with Gemini 1.5")
st.markdown("Upload an image and generate a smart caption using Google's Gemini AI.")

# Image uploader
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="✅ Image Preview", use_column_width=True)

    if st.button("📝 Generate Caption"):
        with st.spinner("Thinking..."):
            try:
                # Prompt for captioning
                prompt = (
                    "Provide a natural, concise caption for this image. "
                    "Mention key elements like scenery, objects, people, signs, or artistic style if applicable."
                )

                # Send request to Gemini with image
                response = model.generate_content([prompt, image])
                caption = response.text.strip()

                st.success("Caption Generated:")
                st.markdown(f"**{caption}**")
            except Exception as e:
                st.error(f"❌ Error generating caption: {e}")

