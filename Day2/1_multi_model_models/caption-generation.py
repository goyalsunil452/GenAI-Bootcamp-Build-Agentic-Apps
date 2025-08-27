import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO


load_dotenv()


client = genai.Client()


st.title("AI Image Caption Generator")


uploaded_image = st.file_uploader(
    "Upload an image for caption generation", type=["png", "jpg", "jpeg"]
)


if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image")

    if st.button("Generate Caption"):
        try:
            with st.spinner("Generating caption..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash", contents=["What is this image?", image]
                )
                st.subheader("Generated Caption:")
                st.write(response.text)
        except Exception as e:
            st.error("Error generating caption")
