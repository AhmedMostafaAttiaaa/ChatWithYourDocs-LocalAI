import os
import shutil
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
CHROMA_PERSIST_DIRECTORY = 'chroma_db_flask'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv'}
LLM_MODEL_NAME = "llama3.2"
EMBEDDING_MODEL_NAME = "msc802/xiaobu-embedding-v2" # Ensure this model is pulled in Ollama

# --- Flask App Setup ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_super_secret_key_for_flash_messages' # Change this in production

# Create upload and chroma directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHROMA_PERSIST_DIRECTORY, exist_ok=True)

# --- Langchain Components ---
# Initialize models (can be done once, with error handling)
llm = None
embeddings_model = None
try:
    llm = OllamaLLM(model=LLM_MODEL_NAME)
    embeddings_model = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
    print(f"Successfully initialized Ollama LLM ('{LLM_MODEL_NAME}') and Embeddings ('{EMBEDDING_MODEL_NAME}').")
except Exception as e:
    print(f"ERROR: Could not initialize Ollama models: {e}")
    print(f"Please ensure Ollama is running and you have pulled the necessary models:")
    print(f"  ollama pull {LLM_MODEL_NAME}")
    print(f"  ollama pull {EMBEDDING_MODEL_NAME}")
    # The app will still run, but functionality will be impaired. Flashing messages will alert the user.

# Global variable to hold the retriever for the current document
current_retriever = None
current_document_filename = None

# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def initialize_rag_components_for_document(file_path, file_extension):
    """
    Processes the uploaded document and sets up the RAG retriever.
    Returns True if successful, False otherwise.
    """
    global current_retriever, embeddings_model, llm # Access global instances

    if not embeddings_model or not llm:
        flash(f"Ollama models ('{LLM_MODEL_NAME}', '{EMBEDDING_MODEL_NAME}') not initialized. Please check Ollama setup and ensure models are pulled.", "error")
        return False

    try:
        # 1. Load Document
        if file_extension == 'pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension == 'txt':
            loader = TextLoader(file_path, encoding='utf-8')
        elif file_extension == 'csv':
            loader = CSVLoader(file_path, encoding='utf-8', autodetect_encoding=True)
        else:
            flash(f"Unsupported file type: {file_extension}", "error")
            return False
        
        documents = loader.load()

        if not documents:
            flash("Could not load any content from the document. It might be empty or in an unsupported format.", "error")
            return False

        # 2. Split Document
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)

        if not splits:
            flash("Could not split the document into manageable chunks. It might be too small or structured in a way that prevents splitting.", "error")
            return False

        # 3. Create Vector Store and Retriever
        # Clear previous ChromaDB contents to start fresh for the new document
        if os.path.exists(CHROMA_PERSIST_DIRECTORY):
            shutil.rmtree(CHROMA_PERSIST_DIRECTORY)
        os.makedirs(CHROMA_PERSIST_DIRECTORY, exist_ok=True)

        print(f"Creating vector store with {len(splits)} document splits.")
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embeddings_model,
            persist_directory=CHROMA_PERSIST_DIRECTORY
        )
        
        current_retriever = vector_store.as_retriever(search_kwargs={"k": 4}) # Retrieve top 4 chunks
        
        flash(f"Document '{os.path.basename(file_path)}' processed successfully. Ready to answer questions.", "success")
        print(f"Document '{os.path.basename(file_path)}' processed. Retriever is ready.")
        return True

    except Exception as e:
        error_message = f"Error processing document: {str(e)}"
        print(f"ERROR: {error_message}")
        flash(error_message, "error")
        current_retriever = None # Reset retriever on failure
        return False

# --- Flask Routes ---
@app.route('/', methods=['GET'])
def index():
    # Pass status to the template
    return render_template('index.html',
                           document_ready=(current_retriever is not None),
                           processed_filename=current_document_filename,
                           answer=request.args.get('answer'),
                           question_asked=request.args.get('question_asked'))

@app.route('/upload', methods=['POST'])
def upload_file_route(): # Renamed to avoid conflict with any potential 'upload_file' helper
    global current_retriever, current_document_filename # To modify global state
    
    if not llm or not embeddings_model:
        flash(f"Cannot process document: Ollama models ('{LLM_MODEL_NAME}', '{EMBEDDING_MODEL_NAME}') are not initialized. Check console and Ollama setup.", "error")
        return redirect(url_for('index'))

    if 'document' not in request.files:
        flash('No file part in the request.', 'error')
        return redirect(url_for('index'))
    
    file = request.files['document']
    if file.filename == '':
        flash('No selected file.', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            # Reset retriever and filename before processing new doc
            current_retriever = None
            current_document_filename = None 
            print(f"Attempting to process uploaded file: {filename}")

            if initialize_rag_components_for_document(file_path, file_extension):
                current_document_filename = filename # Set only on successful processing
            else:
                # Error message already flashed by initialize_rag_components_for_document
                if os.path.exists(file_path): # Clean up failed upload file
                    os.remove(file_path)
            
            return redirect(url_for('index'))

        except Exception as e:
            error_msg = f"An error occurred during file upload or processing: {str(e)}"
            print(f"ERROR: {error_msg}")
            flash(error_msg, "error")
            current_retriever = None # Ensure state is reset
            current_document_filename = None
            if 'file_path' in locals() and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass 
            return redirect(url_for('index'))
    else:
        flash(f"File type not allowed. Please upload {', '.join(ALLOWED_EXTENSIONS)}.", 'error')
        return redirect(url_for('index'))

@app.route('/ask', methods=['POST'])
def ask_question_route(): # Renamed to avoid conflict
    global current_retriever, llm # Access global instances
    
    question = request.form.get('question')
    if not question:
        flash('Please enter a question.', 'warning')
        return redirect(url_for('index', 
                                document_ready=(current_retriever is not None), 
                                processed_filename=current_document_filename))

    if not current_retriever:
        flash('No document processed yet, or processing failed. Please upload a document first.', 'error')
        return redirect(url_for('index', question_asked=question))
    
    if not llm:
        flash(f"LLM ('{LLM_MODEL_NAME}') not available. Cannot answer questions. Check Ollama setup.", "error")
        return redirect(url_for('index', 
                                document_ready=(current_retriever is not None), 
                                processed_filename=current_document_filename, 
                                question_asked=question))

    try:
        print(f"Received question: '{question}' for document '{current_document_filename}'")
        retrieved_docs = current_retriever.invoke(question)
        
        context_docs_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

        prompt_template_str = """
        You are an AI assistant. Answer the question based ONLY on the following context.
        If the context does not contain the answer, state that "The document does not provide an answer to this question."
        Do not use any information outside of the provided context.

        Context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(prompt_template_str)
        
        chain = prompt | llm | StrOutputParser()
        
        print("Invoking LLM chain...")
        answer = chain.invoke({"context": context_docs_text, "question": question})
        print(f"LLM Answer: {answer}")
        
        return redirect(url_for('index', 
                                document_ready=True, 
                                processed_filename=current_document_filename,
                                answer=answer, 
                                question_asked=question))
    except Exception as e:
        error_msg = f"Error getting answer from AI: {str(e)}"
        print(f"ERROR: {error_msg}")
        flash(error_msg, "error")
        return redirect(url_for('index', 
                                document_ready=(current_retriever is not None),
                                processed_filename=current_document_filename,
                                question_asked=question))

# --- Main Execution ---
if __name__ == '__main__':
    if not llm or not embeddings_model:
        print("WARNING: Ollama models (LLM or Embeddings) not initialized at startup.")
        print("The application will run, but document processing and Q&A will likely fail until Ollama is correctly set up and models are available.")
    
    print(f"Flask app starting. Access at http://127.0.0.1:5000 or http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)