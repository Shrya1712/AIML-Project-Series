import random
import pyjokes
import nltk
from nltk.tokenize import word_tokenize

class Chatbot:
    def __init__(self) -> None:
        self.context = []
        self.questions = [
            "What's your name?",
            "How was your day?",
            "What's your favorite hobby?"
        ]
        self.answers = []

    def greet(self):
        return "Hello, how can I assist you today?"
    
    def respond_to_question(self, question):
        if question.lower() in ["hi", "hello", "hey"]:
            return "Hey, how can I help you today?"
        elif question.lower() == "how are you?":
            return "I am just a Chatbot, but I am doing well."
        elif question.lower() in ["how can you help", "what can you do"]:
            return "I can help you with various tasks and answer your questions."
        elif question.lower() == "tell me a joke":
            return pyjokes.get_joke()
        elif question.lower() == "how old are you?":
            return "I'm just a computer program, so I don't have an age."
        elif question.lower() in ["what did i ask before", "can you tell me what i asked before", "what have i asked before"]:
            return self.recall_context()
        else:
            return self.handle_unknown_input()

    def farewell(self):
        return "Goodbye! Have a great day!"
    
    def add_to_context(self, user_input, bot_response):
        self.context.append((user_input, bot_response))

    def recall_context(self):
        if not self.context:
            return "You haven't asked me anything yet."
        previous_questions = "Here are the things you've asked me so far:\n"
        for i, (user_input, response) in enumerate(self.context, 1):
            previous_questions += f"{i}. You asked: '{user_input}' and I responded: '{response}'\n"
        return previous_questions.strip()
    
    def handle_unknown_input(self):
        return "I'm sorry, I didn't understand that. Could you please rephrase or ask something else?"

    
    def ask_questions(self):
        for question in self.questions:
            print("Chatbot:", question)
            user_response = input("You: ")
            self.answers.append(user_response)
            response = self.react_to_answers(question, user_response)
            print("Chatbot:", response)

    def react_to_answers(self, question, answer):
        tokens = word_tokenize(answer.lower())
        if "name" in question.lower():
            return f"Nice to meet you, {answer}!"
        elif "day" in question.lower():
            if "good" in tokens or "great" in tokens or "fine" in tokens:
                return "I'm glad to hear you had a good day!"
            elif "bad" in tokens or "not" in tokens:
                return "I'm sorry to hear that. I hope it gets better!"
            else:
                return "That sounds interesting!"
        elif "hobby" in question.lower():
            hobbies = ["reading", "sports", "music", "traveling", "gaming"]
            for hobby in hobbies:
                if hobby in tokens:
                    return f"{hobby.capitalize()} is a great hobby!"
            return "That sounds like a fun hobby!"
        return "Thanks for sharing!"

chatbot = Chatbot()
print(chatbot.greet())
# Start the conversation loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "goodbye", "see you later", "exit"]:
        print(chatbot.farewell())
        break
    elif user_input.lower() in ["ask me questions", "ask me something"]:
        chatbot.ask_questions()
    else:
        response = chatbot.respond_to_question(user_input)
        chatbot.add_to_context(user_input, response)
        print("Chatbot:", response)
