from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import os

class ChatBot:
    def __init__(self, transcript: str):
        try:
            # Split transcript into chunks
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(transcript)

            # Create embeddings and vector store
            embeddings = GoogleGenerativeAIEmbeddings(
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                model="models/embedding-001"
            )
            self.vectorstore = FAISS.from_texts(chunks, embeddings)

            # Initialize the QA chain
            self.chain = self.create_chain()

        except Exception as e:
            if "Developer instruction is not enabled" in str(e):
                raise Exception("Please enable the Gemini API in your Google Cloud Console") from e
            raise

    def create_chain(self):
        """
        Create and return a question-answering chain using ChatGoogleGenerativeAI and a custom prompt.
        """
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an AI assistant tasked with answering questions about a video transcript. 
            The following text is the relevant content extracted from the transcript:

            {context}

            Using the above context, please answer the following question. If the question asks for a summary, 
            provide a comprehensive summary of the main points in the transcript. If you can't find the answer 
            in the context, simply state that you don't have enough information to answer the question.

            Question: {question}

            Answer:"""
        )
        
        chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
        return chain

    def get_response(self, question: str) -> str:
        """
        Get response from the chatbot
        
        Args:
            question (str): User's question
            
        Returns:
            str: Chatbot's response
        """
        # Retrieve relevant context from the vector store
        context = self.vectorstore.similarity_search(question, k=3)
        context_text = " ".join(doc.page_content for doc in context) if context else "No relevant context found."

        # Convert the context to a Document
        doc = Document(page_content=context_text, metadata={})

        # Use the QA chain to generate a response
        response = self.chain.invoke({
            "input_documents": [doc],
            "question": question
        })
        
        # Extract the output text from the response
        return response["output_text"] 