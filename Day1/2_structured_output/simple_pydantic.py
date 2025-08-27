from pydantic import BaseModel


# Simple Pydantic model
class Person(BaseModel):
    name: str
    age: int
    city: str


# Create an instance
person = Person(name="John", age=30, city="New York")
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"City: {person.city}")

# Convert to dictionary
person_dict = person.model_dump()
print(f"Dictionary: {person_dict}")

# Convert from dictionary
new_person = Person(**person_dict)
print(f"New person: {new_person}")
