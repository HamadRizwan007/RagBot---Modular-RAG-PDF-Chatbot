import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(vectorstore):
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY, 
        model="llama-3.1-8b-instant"
    )
    
    # 2. Remove the trailing comma at the end of this line
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    return RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )