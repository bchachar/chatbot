from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from document_store import DocumentStore


class Chatbot:
    def __init__(self, model_name="llama3"):
        # Initialize the language model using Ollama
        self.llm = Ollama(
            model=model_name,
            temperature=0.7,
            base_url="http://localhost:11434"  # Default Ollama URL
        )
        
        # Initialize document store
        self.doc_store = DocumentStore()
        self.doc_store.load_documents()
        
        # Define the conversation prompt template with document context
        template = """The following is a friendly conversation between a Human and an AI assistant.
        The AI assistant is helpful, creative, clever, and very friendly.
        
        Context information from relevant documents:
        {context}
        
        Human: {user_input}
        AI Assistant:"""
        
        self.prompt = PromptTemplate(
            input_variables=["user_input", "context"],
            template=template
        )
        
        # Create the conversation chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=True
        )
    
    def get_response(self, user_input: str) -> str:
        """
        Get a response from the chatbot based on user input.
        
        Args:
            user_input (str): The user's message
            
        Returns:
            str: The chatbot's response
        """
        try:
            # Search for relevant documents
            relevant_docs = self.doc_store.similarity_search(user_input)
            context = "\n".join([doc.page_content for doc in relevant_docs])
            
            # Get response with document context
            response = self.chain.run(
                user_input=user_input,
                context=context
            )
            return response.strip()
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def clear_memory(self):
        """Clear the document store."""
        self.doc_store.clear_store() 