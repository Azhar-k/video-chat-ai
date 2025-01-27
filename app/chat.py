from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

class ChatBot:
    def __init__(self, transcript: str):
        # Split transcript into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(transcript)

        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings()
        self.vectorstore = FAISS.from_texts(chunks, embeddings)

        # Initialize conversation chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0.7),
            retriever=self.vectorstore.as_retriever(),
            memory=ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        )

    def get_response(self, question: str) -> str:
        """
        Get response from the chatbot
        
        Args:
            question (str): User's question
            
        Returns:
            str: Chatbot's response
        """
        response = self.chain({"question": question})
        return response['answer'] 