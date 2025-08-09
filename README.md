[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vgbm4cZ0)

AI Corporate Agent for ADGM Compliance
This repository contains the source code for an AI-powered legal assistant designed to review, validate, and help prepare documentation for business incorporation and compliance within the Abu Dhabi Global Market (ADGM) jurisdiction.

The agent leverages a Retrieval-Augmented Generation (RAG) architecture, using LangChain, Google Gemini, and a FAISS vector store to ensure its analysis is grounded in a specific knowledge base of legal documents.

Features
Intelligent Document Analysis: Reviews uploaded .docx files for legal red flags, inconsistencies, and missing clauses.

RAG-Powered Accuracy: Uses a local FAISS vector store built from your own legal templates (.docx and .pdf) to provide contextually relevant and accurate analysis.

Automated Document Checklist: Verifies if all mandatory documents are present for specific legal processes (e.g., Company Incorporation).

Inline Highlighting & Commenting: Automatically generates a new .docx file with problematic text highlighted in red and detailed comments added to the relevant paragraphs.

Structured Reporting: Outputs a detailed JSON report summarizing all findings, including document names, issue descriptions, severity, and actionable suggestions.

Secure API Key Management: Uses a .env file to keep your Google API key secure and off version control.

Simple Web Interface: Built with Gradio for easy document uploading and interaction.

How It Works
Knowledge Base Creation: The create_vector_store.py script reads all .docx and .pdf files from the templates_for_db folder, splits them into chunks, and stores their vector embeddings in a local FAISS database. This only needs to be done once or whenever the knowledge base is updated.

Document Upload: The user uploads one or more .docx files via the Gradio web interface.

Checklist Verification: The system first checks if all required documents for a given process are present.

RAG-Powered Analysis: For each document, the system:

Retrieves the most relevant text chunks from the FAISS vector store.

Sends the document's content along with the retrieved context to the Gemini LLM.

Prompts the LLM to identify issues and return a structured JSON object.

Output Generation: The application generates a downloadable, reviewed .docx file with highlights and comments, alongside a comprehensive JSON report of the findings.

Setup and Installation
Follow these steps to set up and run the project on your local machine.

Step 1: Clone the Repository
git clone <your-repository-url>
cd <repository-folder>

Step 2: Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies
Install all the required packages from the requirements.txt file.

pip install -r requirements.txt

Step 4: Create the Environment File (Crucial!)
This project uses a .env file to manage the Google API Key. This file is not included in the repository and must be created manually.

Create a new file named .env in the root of the project directory.

Add your Google API key to this file as follows:

# .env
GOOGLE_API_KEY="PASTE_YOUR_GOOGLE_API_KEY_HERE"

Step 5: Create and Populate the Knowledge Base Folder
The agent's "knowledge" comes from the documents you provide. This folder is not included in the repository and must be created manually.

In the root of the project directory, create a new folder named templates_for_db.

Copy all your reference ADGM documents (.docx and .pdf files) into this templates_for_db folder. The quality and relevance of these documents will directly impact the performance of the AI agent.

Step 6: Build the Vector Store
Before running the main application, you must process your knowledge base files into a FAISS vector store.

Run the create_vector_store.py script from your terminal:

python create_vector_store.py

This will create a faiss_index folder in your project directory. You only need to re-run this script if you add, remove, or change the files in the templates_for_db folder.

Step 7: Run the Application
Once the vector store is created, you can launch the Gradio web application.

python app.py

Open your web browser and navigate to the local URL provided by Gradio (usually http://127.0.0.1:7860) to start using the Corporate Agent.
