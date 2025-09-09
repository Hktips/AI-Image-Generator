import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
st.title("AI Image Generator")
user_prompt = st.text_input("What do you want to generate image for?")
if st.button("Generate Image:"):
    if not user_prompt:
        st.warning("Please enter the prompt")
    else:
        try:
            with st.spinner("Generating image..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['Text', 'Image']
                    )
                )
                st.subheader("Image Generator")
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        st.write(part.text)
                    elif part.inline_data is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        st.image(image)
        except Exception as e:
            st.error(f"Image getting error: {e}")
            