import os
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# --- CONFIGURATION ---
load_dotenv()

# Check if the API key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please set it.")

# Directory containing the knowledge base files
DATA_SOURCE_DIR = './templates_for_db/'

# --- SCRIPT LOGIC ---
def create_vector_store():
    """
    Loads .docx and .pdf files from a directory, splits them into chunks, 
    creates embeddings, and saves them to a FAISS vector store.
    """
    print("🚀 Starting to create the vector store...")

    # 1. Load documents using the appropriate loader for each file type
    all_docs = []
    print(f"Reading documents from '{DATA_SOURCE_DIR}'...")
    
    # Get a list of all files in the directory
    try:
        files = os.listdir(DATA_SOURCE_DIR)
        if not files:
            print(f"⚠️ No files found in the '{DATA_SOURCE_DIR}' directory.")
            print("Please add your ADGM template files (.docx or .pdf) and try again.")
            return
    except FileNotFoundError:
        print(f"❌ Error: The directory '{DATA_SOURCE_DIR}' was not found.")
        print("Please create it and add your knowledge base files.")
        return

    for file_name in files:
        file_path = os.path.join(DATA_SOURCE_DIR, file_name)
        
        try:
            if file_name.lower().endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                print(f"   - Loading PDF: {file_name}")
                all_docs.extend(loader.load())
            elif file_name.lower().endswith(".docx"):
                loader = Docx2txtLoader(file_path)
                print(f"   - Loading DOCX: {file_name}")
                all_docs.extend(loader.load())
            else:
                print(f"   - Skipping non-supported file: {file_name}")
        except Exception as e:
            print(f"   - ❌ Error loading {file_name}: {e}")

    if not all_docs:
        print("\n⚠️ No processable documents were loaded. Halting script.")
        return
    print(f"\n✅ Successfully loaded content from {len(all_docs)} document pages/sections.")

    # 2. Split documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    split_docs = text_splitter.split_documents(all_docs)
    print(f"Split documents into {len(split_docs)} chunks.")

    # 3. Create embeddings using Google's model
    print("Initializing Google Generative AI Embeddings...")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    except Exception as e:
        print(f"❌ Error initializing embeddings model: {e}")
        print("Please ensure your GOOGLE_API_KEY is correct and has access.")
        return

    # 4. Create the FAISS vector store
    print("Creating FAISS vector store... (This might take a few minutes)")
    try:
        db = FAISS.from_documents(split_docs, embeddings)
    except Exception as e:
        print(f"❌ An error occurred during FAISS index creation: {e}")
        return

    # 5. Save the vector store locally
    db.save_local("faiss_index")
    print("\n----------------------------------------------------")
    print("✅ Vector store created and saved successfully!")
    print("You can now run the main application using 'app.py'.")
    print("----------------------------------------------------")


if __name__ == "__main__":
    create_vector_store()
