from langchain.vectorstores import FAISS
from langchain.llms import GooglePalm
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory  import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()

def create_vector_db():
    loader = CSVLoader(file_path='College_Data.csv', source_column="query")
    data = loader.load()

    embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-large")
    vectordb_file_path = "faiss_index"

    vectordb = FAISS.from_documents(documents=data, embedding=embeddings)
    vectordb.save_local(vectordb_file_path)

def get_qa_chain():
    vectordb_file_path = "faiss_index"
    embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-large")
    vectordb = FAISS.load_local(vectordb_file_path, embeddings)
    retriever = vectordb.as_retriever(score_threshold=0.7)

    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I'm sorry, I don't have that information." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(llm=GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.5),
                                        chain_type="stuff",
                                        retriever=retriever,
                                        input_key="query",
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt": PROMPT})

    return chain

def chat(qa_chain, memory):
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response, _ = qa_chain.generate_answer({"query": user_input}, memory=memory)
        print("Chatbot:", response)

if __name__ == "__main__":
    create_vector_db()
    qa_chain = get_qa_chain()
    memory = ConversationBufferMemory()  # Initialize conversation memory
    chat(qa_chain, memory)