def chatbot_response(message):
    message = message.lower()
    if "hello" in message:
        return "Hello! Welcome to the real-time chatbot."
    elif "time" in message:
        return "I respond in real time!"
    elif "bye" in message:
        return "Goodbye! Have a nice day!"
    else:
        return "Sorry, I didn’t understand that."
