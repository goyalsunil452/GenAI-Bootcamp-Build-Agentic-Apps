"""
Streamlit Basics - Simple Web App Framework

This file demonstrates basic Streamlit concepts for building web applications.
"""

import streamlit as st


def basic_streamlit_demo():
    """
    Basic Streamlit elements and concepts
    """
    st.title("Streamlit Basics Demo")
    st.write("Welcome to Streamlit! This is a simple web app framework.")

    # Headers and text
    st.header("Headers and Text")
    st.subheader("This is a subheader")
    st.write("This is regular text using st.write()")
    st.markdown("**This is bold text** using markdown")

    # Input widgets
    st.header("Input Widgets")

    # Text input
    user_name = st.text_input("Enter your name:", "Guest")
    st.write(f"Hello, {user_name}!")

    # Number input
    age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
    st.write(f"You are {age} years old.")

    # Selectbox
    favorite_color = st.selectbox(
        "Choose your favorite color:", ["Red", "Blue", "Green", "Yellow", "Purple"]
    )
    st.write(f"Your favorite color is {favorite_color}.")

    # Slider
    temperature = st.slider("Select temperature:", 0, 100, 20)
    st.write(f"Temperature: {temperature}°C")

    # Checkbox
    if st.checkbox("Show additional info"):
        st.write("This is additional information!")

    # Button
    if st.button("Click me!"):
        st.write("Button was clicked!")

    # File uploader
    st.header("File Handling")
    uploaded_file = st.file_uploader("Choose a file:")
    if uploaded_file is not None:
        st.write(f"File uploaded: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")


def layout_demo():
    """
    Demonstrate Streamlit layout features
    """
    st.header("Layout Features")

    # Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Column 1")
        st.button("Button 1")

    with col2:
        st.write("Column 2")
        st.button("Button 2")

    with col3:
        st.write("Column 3")
        st.button("Button 3")

    # Sidebar
    st.sidebar.header("Sidebar")
    sidebar_option = st.sidebar.selectbox(
        "Choose option:", ["Option 1", "Option 2", "Option 3"]
    )
    st.sidebar.write(f"Selected: {sidebar_option}")

    # Expander
    with st.expander("Click to expand"):
        st.write("This content is hidden by default.")
        st.write("Click the expander to see it!")


def data_display_demo():
    """
    Show how to display data in Streamlit
    """
    st.header("Data Display")

    # Sample data
    import pandas as pd
    import numpy as np

    # Create sample dataframe
    data = {
        "Name": ["Alice", "Bob", "Charlie", "Diana"],
        "Age": [25, 30, 35, 28],
        "City": ["New York", "London", "Paris", "Tokyo"],
    }
    df = pd.DataFrame(data)

    st.write("Sample Data:")
    st.dataframe(df)

    # Charts
    st.header("Charts")

    # Line chart
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
    st.line_chart(chart_data)

    # Bar chart
    st.bar_chart(chart_data)


def main():
    """
    Main function to run the Streamlit demo
    """
    st.set_page_config(page_title="Streamlit Basics", page_icon="📊", layout="wide")

    # Navigation
    page = st.sidebar.selectbox(
        "Choose a page:", ["Basic Demo", "Layout Demo", "Data Display"]
    )

    if page == "Basic Demo":
        basic_streamlit_demo()
    elif page == "Layout Demo":
        layout_demo()
    elif page == "Data Display":
        data_display_demo()


if __name__ == "__main__":
    main()
