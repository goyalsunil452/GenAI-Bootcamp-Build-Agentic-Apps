# Structured Output with Pydantic

## What is Pydantic?

Pydantic is a Python library for data validation and serialization. It helps ensure that data follows a specific structure and format.
Documentation: https://docs.pydantic.dev/latest/concepts/models/

## Why Use Structured Outputs?

- **Predictable responses** - AI always returns data in the same format
- **Easy to parse** - No need to extract information from text
- **Data validation** - Ensures all required fields are present
- **Better integration** - Works seamlessly with other systems

## Files

### simple_pydantic.py
Basic Pydantic model definition and usage. Shows how to create models and work with data.

### structured_agent.py
How to use Pydantic models with AI agents to get structured responses.

### main-agent.py
Advanced example with memory and checkpoints.

## What Each File Shows

### simple_pydantic.py
```python
class Person(BaseModel):
    name: str
    age: int
    city: str

person = Person(name="John", age=30, city="New York")
```
**Learning**: Basic Pydantic model creation and data handling

### structured_agent.py
```python
agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",
    response_format=TaskPlan,  # This enforces structured output
)
```
**Learning**: How to make AI agents return structured data

## Key Concepts

### 1. BaseModel
Inherit from `BaseModel` to create data models with validation.

### 2. Type Annotations
Use Python type hints to define what data each field should contain.

### 3. response_format
Tell the AI agent exactly what structure to return.

### 4. structured_response
Access the validated, structured data from the agent's response.

## How to Run

1. Install: `pip install -r requirements.txt`
2. Set up `.env` file with GROQ_API_KEY
3. Run examples:
   - `python simple_pydantic.py`
   - `python structured_agent.py`
   - `python main-agent.py`

## Learning Progression

1. **Start with simple_pydantic.py** - Understand Pydantic basics
2. **Try structured_agent.py** - See AI with structured outputs
3. **Move to main-agent.py** - Advanced features with memory

## What This Enables

- **Consistent AI responses** - Same format every time
- **Easy data processing** - No text parsing needed
- **Better applications** - Structured data for databases, APIs, etc.
- **Professional outputs** - Predictable, reliable responses
