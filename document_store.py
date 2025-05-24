from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import pickle

class DocumentStore:
    def __init__(self, docs_dir="docs", store_directory="vector_store"):
        self.docs_dir = docs_dir
        self.store_directory = store_directory
        self.index_file = os.path.join(store_directory, "faiss_index")
        self.store_file = os.path.join(store_directory, "faiss_store.pkl")
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cuda'}  # Use GPU if available
        )
        self.vector_store = None
        
    def load_documents(self):
        """Load documents from the docs directory."""
        # Try to load existing vector store
        if os.path.exists(self.index_file) and os.path.exists(self.store_file):
            try:
                with open(self.store_file, 'rb') as f:
                    store_dict = pickle.load(f)
                self.vector_store = FAISS.load_local(
                    self.store_directory,
                    self.embeddings,
                    store_dict
                )
                return
            except Exception as e:
                print(f"Error loading existing store: {e}")
        
        # If loading fails or store doesn't exist, create new one
        documents = []
        
        # Create docs directory if it doesn't exist
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
            
        # Load all .txt files from the docs directory
        for file in os.listdir(self.docs_dir):
            if file.endswith(".txt"):
                loader = TextLoader(os.path.join(self.docs_dir, file))
                documents.extend(loader.load())
                
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        split_docs = text_splitter.split_documents(documents)
        
        # Create vector store
        if not os.path.exists(self.store_directory):
            os.makedirs(self.store_directory)
            
        self.vector_store = FAISS.from_documents(
            split_docs,
            self.embeddings
        )
        
        # Save the vector store
        self.vector_store.save_local(self.store_directory)
        store_dict = self.vector_store.docstore._dict
        with open(self.store_file, 'wb') as f:
            pickle.dump(store_dict, f)
            
    def similarity_search(self, query: str, k: int = 3):
        """Search for similar documents."""
        if not self.vector_store:
            self.load_documents()
        return self.vector_store.similarity_search(query, k=k)
    
    def clear_store(self):
        """Clear the vector store."""
        if os.path.exists(self.store_directory):
            import shutil
            shutil.rmtree(self.store_directory)
        self.vector_store = None 