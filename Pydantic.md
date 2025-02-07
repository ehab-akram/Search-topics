# Pydantic Library

## Introduction

Pydantic is a Python library for data validation and settings management based on Python type annotations.

It ensures that input data adheres to predefined types, automatically converts types where possible, and provides detailed error messages when validation fails.

It is widely used in FastAPI, data parsing, and configuration management due to its speed and simplicity.

## Why Use Pydantic

In Python, variables are dynamically typed, meaning you don't have to explicitly declare their types. While this provides flexibility, it can also lead to issues.

For example, passing a string instead of an integer by mistake can cause unexpected errors.

This is where Pydantic comes in. Pydantic helps enforce data validation and type checking, ensuring that the values assigned to variables match their expected types.

```python
def process_age(age):
    return age + 5  # Expecting an integer

print(process_age("25"))  # This will raise an error at runtime
```

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int  # Pydantic enforces that this must be an integer
```

## Benefits of Pydantic

- Automatic Type Conversion
- Data Validation
- Detailed Error Messages
- JSON Serialization

## Versions of Pydantic & Differences

| Feature | Pydantic v1 | Pydantic v2 (Latest) |
|---------|------------|----------------------|
| Performance | Slower | 50% faster (Rust-based core) |
| Type Annotations | Optional validation | Stricter type enforcement |
| API Compatibility | Used BaseModel | Improved BaseModel methods |
| Data Parsing | Auto-coerces values | Stricter parsing rules |
| Core Library | Python & Cython | Rust-based (pydantic-core) |

## How to Use Pydantic

### Without Pydantic

This is how you check data validation using standard Python code:

```python
class User:
    def __init__(self, id, name='Jane Doe'):
        if not isinstance(id, int):
            raise TypeError(f'Expected id to be an int, got {type(id).__name__}')
        if not isinstance(name, str):
            raise TypeError(f'Expected name to be a str, got {type(name).__name__}')
        self.id = id
        self.name = name

try:
    user = User(id='123')
except TypeError as e:
    print(e)
```

### With Pydantic

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'Jane Doe'  # Sets 'Jane Doe' as a default value

# It will work without any error because it will convert '123' to int
user = User(id='123')
print(user.id)

user = User(id='123', name='Joe Doe')
print(user.model_fields_set)
print(user.model_dump())
print(user.model_dump_json())
print(user.model_json_schema())
```

#### Model Methods Explained

- **model_fields_set**: Returns a set of fields that were explicitly set when creating the model instance.
  Example output: `{'id', 'name'}`

- **model_dump**: Converts the Pydantic model into a Python dictionary.
  Example output: `{'id': 123, 'name': 'Joe Doe'}`

- **model_dump_json**: Converts the Pydantic model into a JSON string.
  Example output: `{"id": 123, "name": "Joe Doe"}`

- **model_json_schema**: Returns the JSON Schema representation of the model. Useful for documentation, API validation, and OpenAPI generation.
  Example output:
  ```json
  {
    "title": "User",
    "type": "object",
    "properties": {
      "id": {
        "title": "Id",
        "type": "integer"
      },
      "name": {
        "title": "Name",
        "type": "string"
      }
    },
    "required": ["id", "name"]
  }
  ```

### Nested Model

```python
from typing import List, Optional
from pydantic import BaseModel

class Food(BaseModel):
    name: str
    price: float
    ingredients: Optional[List[str]] = None  # Optional used to make None a valid value

class Restaurant(BaseModel):
    name: str
    location: str
    foods: List[Food]  # List references the upper pydantic class Food

restaurant_instance = Restaurant(
    name="Tasty Bites",
    location="123, Flavor Street",
    foods=[
        {"name": "Cheese Pizza", "price": 12.50, "ingredients": ["Cheese", "Tomato Sauce", "Dough"]},
        {"name": "Veggie Burger", "price": 8.99}
    ]
)

print(restaurant_instance)
print(restaurant_instance.model_dump())
```

### Special Types and Constraints

```python
from typing import List
from pydantic import BaseModel, EmailStr, PositiveInt, conlist, Field, HttpUrl

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Employee(BaseModel):
    name: str
    position: str
    email: EmailStr

class Owner(BaseModel):
    name: str
    email: EmailStr

class Restaurant(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9-' ]+$")
    owner: Owner
    address: Address
    employees: conlist(Employee, min_length=2)
    number_of_seats: PositiveInt
    delivery: bool
    website: HttpUrl
```

Special types explained:
- **EmailStr**: Ensures that the value is a valid email format (name@domain.com)
- **PositiveInt**: Ensures the number is strictly greater than 0 (no zero or negative numbers)
- **conlist**: Ensures the type of elements and enforces minimum and maximum length
- **HttpUrl**: Ensures the value is a valid URL (http:// or https://)

### Field

The `Field` class provides additional validation and metadata options:

```python
from uuid import uuid4
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(default_factory=lambda: uuid4().hex)
    
user = User()
print(user)
```

#### Field Aliases

Field aliases allow you to define alternative names for model fields:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., alias='username')

user = User(username='johndoe')  # Using alias as input
print(user)  # name='johndoe'
print(user.model_dump(by_alias=True))  # {'username': 'johndoe'}
```

#### Computed Fields

```python
from pydantic import BaseModel, computed_field
from datetime import datetime

class Person(BaseModel):
    name: str
    birth_year: int
    
    @computed_field
    @property
    def age(self) -> int:
        current_year = datetime.now().year
        return current_year - self.birth_year

print(Person(name="John Doe", birth_year=2000).model_dump())
```

### Validators

#### Field Validator

```python
from pydantic import BaseModel, EmailStr, field_validator

class Owner(BaseModel):
    name: str
    email: EmailStr

    @field_validator('name')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if ' ' not in v:
            raise ValueError('Owner name must contain a space')
        return v.title()

try:
    owner_instance = Owner(name="JohnDoe", email="john.doe@example.com")
except ValueError as e:
    print(e)
```

#### Model Validator

```python
from typing import Any
from pydantic import BaseModel, EmailStr, ValidationError, model_validator

class Owner(BaseModel):
    name: str
    email: EmailStr

    @model_validator(mode='before')
    @classmethod
    def check_sensitive_info_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'password' in data:
                raise ValueError('password should not be included')
            if 'card_number' in data:
                raise ValueError('card_number should not be included')
        return data

    @model_validator(mode='after')
    def check_name_contains_space(self) -> 'Owner':
        if ' ' not in self.name:
            raise ValueError('Owner name must contain a space')
        return self

print(Owner(name="John Doe", email="john.doe@example.com"))
```

Validator modes:
- Use `mode='before'` to sanitize or validate raw input data
- Use `mode='after'` to validate processed data or enforce rules on the final object

## Strict Mode

By default, Pydantic will attempt to coerce values to the desired type when possible. However, you can enforce strict type checking:

```python
from pydantic import BaseModel, ValidationError

class MyModel(BaseModel):
    x: int

print(MyModel.model_validate({'x': '123'}))  # Lax mode (Auto conversion)

try:
    MyModel.model_validate({'x': '123'}, strict=True)  # Strict mode
except ValidationError as exc:
    print(exc)
```

# Resources
- Official Documentation: [Pydantic Docs](https://docs.pydantic.dev/latest/)
- GitHub Repository: [Pydantic on GitHub](https://github.com/pydantic/pydantic)
