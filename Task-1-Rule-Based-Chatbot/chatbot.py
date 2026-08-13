"""CodSoft AI Internship - Task 1
Rule-Based Chatbot

A simple chatbot that responds to user input using predefined rules.
"""


def get_response(user_input: str) -> str:
    """Return a predefined response based on the user's input."""
    message = user_input.lower().strip()

    if message in {"hello", "hi", "hey", "good morning", "good afternoon", "good evening"}:
        return "Hello! How can I help you today?"
    elif "your name" in message or "who are you" in message:
        return "I am a simple rule-based AI chatbot created for the CodSoft internship."
    elif "artificial intelligence" in message or "what is ai" in message:
        return "Artificial Intelligence (AI) is the field of creating systems that can perform tasks that normally require human intelligence."
    elif "machine learning" in message or "what is ml" in message:
        return "Machine Learning is a branch of AI that enables computers to learn patterns from data and make predictions or decisions."
    elif "how does ai work" in message or "how ai works" in message:
        return "AI systems learn patterns from data and use algorithms and models to make predictions, decisions, or generate useful outputs."
    elif "how are you" in message:
        return "I'm doing great! Thanks for asking. How can I help you?"
    elif "what can you do" in message or "what do you do" in message:
        return "I can answer a small set of predefined questions about myself and basic AI concepts."
    elif message in {"thanks", "thank you", "thankyou"}:
        return "You're welcome!"
    elif "help" in message:
        return "You can ask me about AI, machine learning, my name, or what I can do."
    elif "who created you" in message or "who made you" in message:
        return "I was created as a CodSoft Artificial Intelligence internship project."
    elif message in {"bye", "goodbye", "exit", "quit"}:
        return "Goodbye! Have a great day."
    else:
        return "I'm sorry, I don't understand that yet. Please try asking something else."


def main() -> None:
    """Run the chatbot in the terminal."""
    print("=" * 55)
    print("       CODSOFT - RULE-BASED AI CHATBOT")
    print("=" * 55)
    print("Type 'bye' or 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        response = get_response(user_input)
        print(f"Bot: {response}\n")

        if user_input.lower().strip() in {"bye", "goodbye", "exit", "quit"}:
            break


if __name__ == "__main__":
    main()
