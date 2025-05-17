# Local Document Q&A with AI 📄🤖

This Flask web application allows you to upload documents (TXT, PDF, or CSV files) and ask questions about their content using a locally running AI model. Your data remains private as all processing, including AI inference, happens on your machine.

Powered by [Langchain](https://www.langchain.com/) and [Ollama](https://ollama.ai/).

## Features

*   **Supports Multiple File Types:** Upload `.txt`, `.pdf`, and `.csv` files.
*   **Local AI Processing:** Utilizes Ollama to run large language models (LLMs) and embedding models locally.
*   **Contextual Q&A:** The AI answers questions based *only* on the content of the uploaded document.
*   **Privacy Focused:** Your documents and queries are not sent to any third-party services.
*   **Simple Web Interface:** Easy-to-use interface for uploading documents and asking questions.

## Prerequisites

1.  **Python 3.8+**
2.  **Ollama Installed and Running:**
    *   Download and install Ollama from [ollama.ai](https://ollama.ai/).
    *   Ensure the Ollama application/server is running in the background.
3.  **Required Ollama Models:**
    You need to pull the LLM and embedding models that the application will use. Open your terminal and run:
    ```bash
    ollama pull llama3.2  # Or your preferred general-purpose LLM
    ollama pull msc802/xiaobu-embedding-v2 # Or your preferred embedding model
    ```
    *(You can change these models in `app.py` if you prefer others, but make sure they are supported by Ollama and compatible with Langchain.)*

## Setup & Installation

1.  **Clone the Repository (or download the files):**
    ```bash
    # If you host this on GitHub:
    # git clone https://github.com/AhmedMostafaAttiaaa/your-repo-name.git
    # cd your-repo-name
    ```
    If you're just using the files I provided, create a directory (e.g., `local_doc_qa_app`) and place all the files (`app.py`, `requirements.txt`, `templates/`, etc.) inside it.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On Windows: `.\venv\Scripts\activate`
    *   On macOS/Linux: `source venv/bin/activate`

3.  **Install Dependencies:**
    Navigate to the project directory in your terminal (where `requirements.txt` is located) and run:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Ensure Ollama is running** with the necessary models pulled (see Prerequisites).
2.  **Start the Flask Application:**
    In your terminal, from the project's root directory (e.g., `local_doc_qa_app/`), run:
    ```bash
    python app.py
    ```
3.  **Access the Web Interface:**
    Open your web browser and go to: `http://127.0.0.1:5000/` (or `http://localhost:5000/`)

    If you see output like `* Running on http://0.0.0.0:5000/`, it means the app is accessible on your local network via your machine's IP address on port 5000.

## How to Use

1.  **Upload a Document:**
    *   Click on "Choose File" or the file input area.
    *   Select a `.txt`, `.pdf`, or `.csv` file from your computer.
    *   Click "Upload & Process Document".
    *   Wait for the confirmation message indicating the AI is ready.

2.  **Ask a Question:**
    *   Once a document is processed, the "Ask Your Question" input field will be enabled.
    *   Type your question related to the content of the uploaded document.
    *   Click "Ask AI".

3.  **View the Answer:**
    *   The AI's response will appear below the question form. The answer is generated solely from the information present in the uploaded document.

## Project Structure

```
local_doc_qa_app/
├── app.py               # Main Flask application logic
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates for the web interface
│   ├── index.html       # Main page layout
│   └── ai_response.html # Template for displaying AI's answer
├── uploads/             # Temporary storage for uploaded files (created by app)
├── .gitignore           # Specifies intentionally untracked files that Git should ignore
└── README.md            # This file
```
*(The `chrome_langchain_db/` directory will also be created by the app to store the vector database.)*

## Customization

*   **AI Models:** You can change the LLM and embedding models used by modifying the `model` parameters in `OllamaLLM(...)` and `OllamaEmbeddings(...)` calls within `app.py` (in the `initialize_langchain_components` function). Remember to `ollama pull` any new models you specify.
*   **Retriever:** The number of retrieved chunks (`search_kwargs={"k": 4}`) can be adjusted in `app.py` inside the `setup_new_document_context` function.
*   **Prompt Template:** The system prompt guiding the LLM's behavior can be modified in the `template` variable within `setup_new_document_context` in `app.py`.
*   **Styling:** Modify the HTML and CSS in the `templates/index.html` and `templates/ai_response.html` files to change the appearance.

## Troubleshooting

*   **"Ollama server not running" / Connection Errors:** Ensure the Ollama application is running on your system before starting the Flask app.
*   **Model Not Found Errors:** Double-check that you have pulled the specified models using `ollama pull <model_name>`.
*   **Permissions Issues:** If the app can't create `uploads/` or `chrome_langchain_db/` directories, ensure it has write permissions in the project directory.
*   **Slow Processing/Responses:** Local AI models, especially larger ones, can be resource-intensive. Performance depends on your CPU/GPU and the size of the models/documents.
*   **Encoding Issues (CSV/TXT):** The app attempts UTF-8 encoding and autodetects for CSV. If you encounter issues with specific files, you might need to ensure they are UTF-8 encoded or adjust loader parameters in `app.py`.

## Contributing
This project is created by [AhmedMostafaAttiaaa](https://github.com/AhmedMostafaAttiaaa).
If you'd like to contribute, please fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
