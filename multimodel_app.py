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
st.title("AI Image Caption Generator")
uploaded_image=st.file_uploader("Upload an image for caption generation", type=["png","jpg"])
if uploaded_image:
    image=Image.open(uploaded_image)  
    st.image(image,caption="Uploaded Image")

    if st.button("Generate Caption"):
        try:
            with st.spinner("Generating Caption..."):
                response=client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["what is this image?",image]
            )
                st.subheader("Generated Caption:")
                st.write(response.text)

        except Exception as e:
            st.error("Error generating Caption")

st.title("AI YouTube Video SUmmarizer")
youtube_url=st.text_input(" Enter youtube video url")
if st.button("Summrized youtube video"):
    if not youtube_url:
        st.warning("No YouTube Url Present")
    else:
        try:
            with st.spinner("Summirizing YouTube Video"):
                response = client.models.generate_content(
                    model='models/gemini-2.5-flash',
                    contents=types.Content(
                        parts=[
                            types.Part(
                                file_data=types.FileData(file_uri=youtube_url),
                                video_metadata=types.VideoMetadata(
                                    start_offset='1250s',
                                    end_offset='1570s'
                                )
                            ),
                            types.Part(text='Please summarize the video in 3 sentences.')
                        ]
                    )
                )
                st.subheader("Summaring video")
                st.write(response.text)
        except Exception as e:
              st.error("Error generating summary")
