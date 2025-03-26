import re
import random

responses = {
    "i feel (.*)": ["Why do you feel {}?", "How long have you felt {}?", "Do you think feeling {} is normal?"],
    "why do you (.*)": ["Why does it concern you that I {}?", "What makes you ask that?"],
    "i'm (.*)": ["How does being {} make you feel?", "Do you enjoy being {}?"],
    "i (.*) you": ["Why do you {} me?", "What makes you think you {} me?"],
    "because (.*)": ["Is that the real reason?", "What other reasons might there be?",
                     "Does that reason explain everything?"],
    "yes": ["You seem quite sure.", "I understand."],
    "no": ["Why not?", "Can you explain why?"],
    "you are (.*)": ["What makes you think I am {}?", "Does it please you to think that I am {}?"],
    "i want (.*)": ["Why do you want {}?", "What would it mean if you got {}?"],
    "can you (.*)": ["Why do you ask?", "Perhaps you believe I can {}?"]
}

reflections = {
    "i am": "you are",
    "i'm": "you are",
    "i have": "you have",
    "i was": "you were",
    "i": "you",
    "me": "you",
    "my": "your",
    "you are": "I am",
    "you have": "I have",
    "you were": "I was"
}

default_responses = [
    "Tell me more.",
    "Why do you say that?",
    "How does that make you feel?",
    "Can you elaborate?",
    "That is very interesting."
]


def reflect(sentence):
    words = sentence.lower().split()
    return " ".join(reflections.get(word, word) for word in words)


def eliza_chat():
    print("Eliza: Hello, I'm Eliza. What's on your mind?")

    while True:
        input_text = input("You: ")
        if input_text.lower() in ["bye", "exit", "quit"]:
            print("Eliza: Goodbye! It was nice talking to you.")
            break

        matched = False
        for pattern, phrases in responses.items():
            match = re.match(pattern, input_text, re.IGNORECASE)
            if match:
                response = random.choice(phrases).format(*[reflect(g) for g in match.groups()])
                print("Eliza:", response)
                matched = True
                break

        if not matched:
            print("Eliza:", random.choice(default_responses))


eliza_chat()
