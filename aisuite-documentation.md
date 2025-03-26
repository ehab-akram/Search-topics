# Introduction

AISuite is a powerful library designed to simplify the use of **multiple Large Language Models** (LLMs) through a **standardized interface**. 

It provides developers with an intuitive, **OpenAI-like interface** that makes it easy to interact with popular LLMs and compare their outputs seamlessly.

AISuite acts as a thin wrapper around various Python client libraries, allowing users to effortlessly switch between different LLM providers **without modifying their code.**

# Code Example

## 1. Import necessary libraries
```python
import aisuite as ai
from dotenv import load_dotenv
import os
import time
```

## 2. Load the API keys
```python
# Load environment variables from the .env file
load_dotenv(dotenv_path=r"D:\@Projects\aisuite\.env")

# Retrieve API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
```

## 3. Initiate instance and add the models
```python
client = ai.Client()

models = [
    "openai:gpt-4o",
    "anthropic:claude-3-5-sonnet-20240620",
    "groq:llama-3.3-70b-versatile",
    "groq:deepseek-r1-distill-qwen-32b",
    "huggingface:mistralai/Mistral-7B-Instruct-v0.3",
    "ollama:llama3.1:8b-instruct-q6_K"
]
```

Note: Each item contains "provider_name:model_name"

## 4. Create your prompt message
```python
messages = [
    {"role": "system", "content": "Respond in Pirate English."},
    {"role": "user", "content": "Tell me a joke."},
]
```

## 5. Loop over each model and print the result
```python
for model in models:
    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.75
    )
    end_time = time.time()
    execution_time = end_time - start_time
    print(model, "\n", execution_time, "\n", response.choices[0].message.content)
    print("#" * 30)
```

## Output

```
openai:gpt-4o
execution_time: 1.3258731365203857
Why did the pirate go to school?

To improve his "arrrr-ticulation!" Har har har!
##############################
anthropic:claude-3-5-sonnet-20240620
execution_time: 3.0504684448242188
Arrr, ye be wantin' a joke, do ye? Well, shiver me timbers! Here be one fer ye, ye scurvy dog:

Why couldn't the pirate play cards?

Because he was sittin' on the deck!

Har har har! That be a knee-slapper, ain't it? If ye didn't find it funny, I'll make ye walk the plank, ye landlubber! Now, where be me rum?
##############################
groq:llama-3.3-70b-versatile
execution_time: 0.6751089096069336
Here's one:

What do you call a fake noodle?

An impasta!

I hope that made you laugh! Do you want to hear another one?
##############################
groq:deepseek-r1-distill-qwen-32b
execution_time: 2.2043683528900146
The joke "Why don't skeletons fight each other? They don't have the guts!" is humorous due to its clever use of wordplay. The key elements are:

1. **Double Entendre**: The word "guts" serves a dual purpose. Literally, it refers to internal organs, which skeletons lack. Figuratively, it means courage, implying that skeletons are too cowardly to fight.

2. **Unexpected Twist**: The joke subverts expectations by shifting from the literal (lack of organs) to the figurative (lack of courage), creating a humorous surprise.

3. **Cultural Familiarity**: The effectiveness of the joke relies on the audience's knowledge of both the literal and slang meanings of "guts," making it relatable.

4. **Self-Contained Structure**: The joke is concise and self-explanatory, making it easy to deliver and remember.

In essence, the joke's humor stems from the unexpected double meaning of "guts," combining a literal truth with a figurative twist.
##############################
huggingface:mistralai/Mistral-7B-Instruct-v0.3
execution_time: 0.9055664539337158
Sure, here's a classic math joke for you:

Why was the math book sad?

Because it had too many problems.

Now, don't worry, we're here to solve your problems, not create them! How can I assist you today?
##############################
ollama:llama3.1:8b-instruct-q6_K
execution_time: 3.149134397506714
Here's one:

What do you call a fake noodle?

An impasta.
##############################
```

# Resources

- https://github.com/andrewyng/aisuite
