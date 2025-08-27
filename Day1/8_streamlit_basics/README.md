# Streamlit Basics

## What is Streamlit?

Streamlit is a Python library that makes it easy to create web applications. It's perfect for building AI interfaces, data dashboards, and interactive tools.

## Why Use Streamlit?

- **Simple to use** - Write Python code, get a web app
- **Fast development** - No HTML/CSS/JavaScript needed
- **Interactive** - Built-in widgets and real-time updates
- **Perfect for AI** - Great for building chat interfaces and AI tools

## Files

### streamlit_basics.py
Basic Streamlit concepts and widgets. Shows how to create simple web applications.

### streamlit_chat_app.py
Complete chat application built with Streamlit. Demonstrates real-world usage.

## What Each File Shows

### streamlit_basics.py
```python
# Basic widgets
user_name = st.text_input("Enter your name:", "Guest")
age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
favorite_color = st.selectbox("Choose your favorite color:", ["Red", "Blue", "Green"])

# Layout features
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Column 1")
```
**Learning**: Basic Streamlit widgets and layout concepts

### streamlit_chat_app.py
```python
# Chat interface
if prompt := st.chat_input("What would you like to chat about?"):
    add_message("user", prompt)
    response = simple_ai_response(prompt)
    add_message("assistant", response)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
```
**Learning**: Building complete applications with Streamlit

## Key Concepts

### 1. Widgets
- **Input widgets** - Text input, number input, selectbox, slider
- **Display widgets** - Write, markdown, dataframe, charts
- **Action widgets** - Button, checkbox, file uploader

### 2. Layout
- **Columns** - Organize content side by side
- **Sidebar** - Navigation and settings
- **Expander** - Collapsible content sections

### 3. Session State
- **Persistent data** - Store information between interactions
- **Chat history** - Remember conversation context
- **User preferences** - Save user settings

### 4. Real-time Updates
- **Automatic refresh** - App updates as you interact
- **Live data** - Show changing information
- **Interactive charts** - Respond to user input

## How to Run

1. **Install Streamlit**: `pip install streamlit`
2. **Run basics demo**: `streamlit run streamlit_basics.py`
3. **Run chat app**: `streamlit run streamlit_chat_app.py`

## Learning Progression

1. **Start with streamlit_basics.py** - Understand basic widgets and layout
2. **Try streamlit_chat_app.py** - See how to build complete applications
3. **Customize the chat app** - Add your own features
4. **Connect to AI models** - Integrate with LangChain/LangGraph

## What This Enables

- **Web interfaces** - Turn Python scripts into web apps
- **AI applications** - Build chat interfaces for your agents
- **Data dashboards** - Visualize and interact with data
- **User tools** - Create applications others can use
- **Prototyping** - Quickly test ideas with real users

## Next Steps

- **Connect to AI** - Integrate Streamlit with your LangGraph agents
- **Add databases** - Store chat history and user data
- **Deploy online** - Share your app with others
- **Build end-to-end app** - Complete AI application

## Note

Streamlit makes web development simple. Focus on Python logic, and Streamlit handles the web interface. Perfect for AI applications and data tools.



### Streaming responses - Real-time text generation
Since the core functionality is working, you could add:
Streaming responses - Real-time text generation
Chat export - Save conversations as files
AI personality settings - Different assistant behaviors
Tool integration - Connect to GitHub, filesystem, etc.
Chat search - Find specific conversations