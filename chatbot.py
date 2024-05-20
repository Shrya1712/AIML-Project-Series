import os
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.memory import ConversationBufferMemory
from secret_key import gemini_key

# Set your OpenAI API kedidy
os.environ['GOOGLE_API_KEY'] = gemini_key
llm = ChatGoogleGenerativeAI(model="gemini-pro")

memory = ConversationBufferMemory()

# Create a conversation chain that uses the LLM and the conversation buffer memory
conversation_chain = ConversationChain(llm=llm, memory=memory)

class Chatbot:
    def __init__(self):
        self.conversation_chain = conversation_chain


    def greet(self):
        return "Hello! How can I assist you today?"

    def respond_to_question(self, question):
        # Generate response using conversation chain
        response = self.conversation_chain.predict(input=question)
        return response
    def handle_unknown_input(self):
        return "I'm sorry, I didn't understand that. Could you please rephrase or ask something else?"
    
if __name__ == "__main__":
    chatbot = Chatbot()
    print(chatbot.greet())

    # Start the conversation loop
    while True:
        question = input("You: ")
        if question.lower() in ["bye", "goodbye", "exit"]:
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = chatbot.respond_to_question(question)
        print("Chatbot:", response)