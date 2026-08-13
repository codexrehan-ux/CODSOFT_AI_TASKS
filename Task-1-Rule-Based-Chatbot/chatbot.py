"""CodSoft AI Internship - Task 1
Rule-Based Chatbot

A simple chatbot that responds to user input using predefined rules.
"""


def get_response(user_input: str) -> str:
    """Return a predefined response based on the user's input."""
    message = user_input.lower().strip()

    if message in {"hello", "hi", "hey", "good morning", "good afternoon"}:
        return "Hello! How can I help you today?"
    elif "your name" in message or "who are you" in message:
        return "I am a simple rule-based AI chatbot created for the CodSoft internship."
    elif "artificial intelligence" in message or message == "what is ai" or "what is ai" in message:
        return "Artificial Intelligence (AI) is the field of creating systems that can perform tasks that normally require human intelligence."
    elif "how are you" in message:
        return "I'm doing great! Thanks for asking. How can I help you?"
    elif "help" in message:
        return "You can ask me about AI, my name, or simply say hello or goodbye."
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
