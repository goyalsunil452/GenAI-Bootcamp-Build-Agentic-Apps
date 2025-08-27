import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO


load_dotenv()


client = genai.Client()


st.title("AI Video Caption Generator")
file_uri = st.text_input("provide youtube video url")

if st.button("Generate Caption"):
    if not file_uri:
        st.warning("Please enter the prompt!")
    else:
        try:
            with st.spinner("Generating caption..."):
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash",
                    contents=types.Content(
                        parts=[
                            types.Part(file_data=types.FileData(file_uri=file_uri)),
                            types.Part(
                                text="Please summarize the video in 3 sentences."
                            ),
                        ]
                    ),
                )
            st.subheader("Video Summary")
            st.write(response.text)

        except Exception as e:
            st.error("Error generating caption")
