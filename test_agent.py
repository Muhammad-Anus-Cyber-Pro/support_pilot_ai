from app.agent import ask_agent

questions = [
    "What is your return policy?",
    "Do you have wireless headphones under $50?",
    "Where is my order #1025?",
    "I received the wrong product and want compensation.",
]

for q in questions:
    print(f"\nCUSTOMER: {q}")
    result = ask_agent(q)
    print(f"AGENT: {result['response']}")
    print(f"HANDOFF: {result['handoff']}")