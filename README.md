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
    ollama pull llama3.2
    ollama pull msc802/xiaobu-embedding-v2
    ```
    *(You can change these models in `app.py` (constants `LLM_MODEL_NAME`, `EMBEDDING_MODEL_NAME`) if you prefer others, but make sure they are supported by Ollama and compatible with Langchain.)*

## Setup & Installation

1.  **Create a Project Directory:**
    Create a directory for your project (e.g., `local_doc_qa_flask`) and place all the provided files (`app.py`, `requirements.txt`, `README.md`, and the `templates` folder with `index.html` inside it) into this directory.

2.  **Create a Virtual Environment (Recommended):**
    Open your terminal, navigate to your project directory, and run:
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On Windows: `.\venv\Scripts\activate`
    *   On macOS/Linux: `source venv/bin/activate`

3.  **Install Dependencies:**
    With your virtual environment activated, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Ensure Ollama is running** with the necessary models pulled (see Prerequisites).
2.  **Start the Flask Application:**
    In your terminal, from the project's root directory (e.g., `local_doc_qa_flask/`), run:
    ```bash
    python app.py
    ```
3.  **Access the Web Interface:**
    Open your web browser and go to: `http://127.0.0.1:5000/` (or `http://localhost:5000/`)

    If you see output like `* Running on http://0.0.0.0:5000/`, it means the app is accessible on your local network via your machine's IP address on port 5000.

## How to Use

1.  **Upload a Document:**
    *   Click on "Choose File".
    *   Select a `.txt`, `.pdf`, or `.csv` file from your computer.
    *   Click "Upload & Process Document".
    *   Wait for the confirmation message (e.g., "Document 'yourfile.pdf' processed successfully.") indicating the AI is ready. If there are errors, they will be displayed.

2.  **Ask a Question:**
    *   Once a document is processed successfully, the "Ask Your Question" input field will be enabled.
    *   Type your question related to the content of the uploaded document.
    *   Click "Ask AI".

3.  **View the Answer:**
    *   The AI's response will appear below the question form. The answer is generated solely from the information present in the uploaded document.

## Project Structure

```
local_rag_ollama/
├── app.py # Main Flask application logic
├── requirements.txt # Python dependencies
├── templates/ # HTML templates for the web interface
│ └── index.html # Main page layout
├── uploads/ # Temporary storage for uploaded files (created by app)
├── chroma_db_flask/ # Stores the vector database for the last processed document (created by app)
├── .gitignore # Specifies intentionally untracked files that Git should ignore
└── README.md # This file
```

      
## Customization

*   **AI Models:** You can change the LLM and embedding models by modifying the `LLM_MODEL_NAME` and `EMBEDDING_MODEL_NAME` constants at the top of `app.py`. Remember to `ollama pull` any new models you specify.
*   **Retriever:** The number of retrieved chunks (`search_kwargs={"k": 4}`) can be adjusted in `app.py` inside the `initialize_rag_components_for_document` function.
*   **Prompt Template:** The system prompt guiding the LLM's behavior can be modified in the `prompt_template_str` variable within the `ask_question_route` function in `app.py`.
*   **Styling:** Modify the HTML and CSS in the `templates/index.html` file to change the appearance.

## Troubleshooting

*   **"Ollama server not running" / Connection Errors / Model Initialization Errors:** Ensure the Ollama application is running on your system *before* starting the Flask app. Check the console output when starting `app.py` for messages about model initialization.
*   **Model Not Found Errors (in Ollama or app):** Double-check that you have pulled the specified models using `ollama pull <model_name>`. Verify the model names in `app.py` match exactly what Ollama expects.
*   **Permissions Issues:** If the app can't create `uploads/` or `chroma_db_flask/` directories, ensure it has write permissions in the project directory.
*   **Slow Processing/Responses:** Local AI models, especially larger ones, can be resource-intensive. Performance depends on your CPU/GPU and the size of the models/documents.
*   **Encoding Issues (CSV/TXT):** The app attempts UTF-8 encoding for TXT and autodetects for CSV. If you encounter issues with specific files, you might need to ensure they are UTF-8 encoded or adjust loader parameters in `app.py`.
*   **File Upload Issues:** Check for flash messages in the UI. Ensure the file type is one of the allowed extensions (TXT, PDF, CSV).

## Contributing
This project is created by [AhmedMostafaAttiaaa](https://github.com/AhmedMostafaAttiaaa).
If you'd like to contribute, please fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

---
## Contact the Author

This application was developed by **Ahmed Mostafa Attia**.

*   **Email**: `ahmed.mostafa.attiaaa@gmail.com`
*   **LinkedIn**: [Ahmed Mostafa Attia](https://www.linkedin.com/in/ahmedmostafaattiaaa/)
*   **GitHub**: [AhmedMostafaAttiaaa](https://github.com/AhmedMostafaAttiaaa)
*   **Portfolio**: (A link to his portfolio is available on his full CV, as indicated by the portfolio icon)

    