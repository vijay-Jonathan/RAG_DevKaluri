# RAG-QA-Self 🤖

A Retrieval-Augmented Generation (RAG) based chatbot application that answers questions about Dev using personal data from PDF documents.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://langchain.com)

## 📖 About

This AI-powered chatbot uses advanced natural language processing to answer questions about Dev based on PDF documents containing personal information. The application leverages state-of-the-art technologies to provide accurate, contextual responses.

**Read the full article:** [How I Built a RAG-based AI Chatbot from My Personal Data](https://medium.com/keeping-up-with-ai/how-i-built-a-rag-based-ai-chatbot-from-my-personal-data-88eec0d3483c)

## 🛠️ Technology Stack

- **Framework:** LangChain for RAG pipeline orchestration
- **Embeddings:** GPT4All (all-MiniLM-L6-v2) for document vectorization
- **LLM:** Google Gemini 1.5 Flash for response generation
- **Vector Database:** ChromaDB for efficient similarity search
- **UI:** Streamlit for interactive web interface
- **State Management:** LangGraph for conversation flow
- **Document Processing:** PyPDF for PDF parsing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google AI Studio API key (free tier available)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rag-qa-self
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/)
   - Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Create the vector database:**
   ```bash
   python create_db.py
   ```

6. **Launch the application:**
   ```bash
   streamlit run main.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
rag-qa-self/
├── main.py                 # Streamlit web application
├── langchain_helper.py     # RAG pipeline and LangGraph workflow
├── create_db.py           # Vector database creation script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── data_sources/          # PDF documents for knowledge base
│   └── Dev_Kaluri_WL.pdf # Personal data document
└── chroma/               # ChromaDB vector database (auto-generated)
```

## 🔧 Configuration

### Customizing the Knowledge Base

1. Add your PDF documents to the `data_sources/` directory
2. Run `python create_db.py` to rebuild the vector database
3. The system will automatically process and index your documents

### Adjusting Text Chunking

In `create_db.py`, modify the text splitter parameters:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,        # Size of each text chunk
    chunk_overlap=100,     # Overlap between chunks
    length_function=len,
    add_start_index=True,
)
```

### Changing the LLM Model

In `langchain_helper.py`, you can switch to different Gemini models:
```python
llm = GoogleGenerativeAI(
    model="gemini-1.5-pro",  # or "gemini-1.5-flash"
    google_api_key=os.environ['GEMINI_API_KEY']
)
```

## 🐛 Troubleshooting

### Common Installation Issues

**Issue: `pysqlite3` build error on Windows**
- **Solution:** The project uses `pysqlite3-binary` which provides pre-compiled wheels
- Make sure you don't have `import pysqlite3` in your code (use standard `sqlite3` instead)

**Issue: Missing API key error**
- **Solution:** Ensure your `.env` file contains `GEMINI_API_KEY=your_actual_key`

**Issue: No documents found**
- **Solution:** Make sure PDF files are in the `data_sources/` directory and run `create_db.py`

### Performance Tips

- For faster responses, use `gemini-1.5-flash` instead of `gemini-1.5-pro`
- Adjust `chunk_size` in `create_db.py` based on your document complexity
- Consider using a local embedding model for privacy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) for the RAG framework
- [Google AI](https://ai.google.dev) for the Gemini API
- [Streamlit](https://streamlit.io) for the web framework
- [ChromaDB](https://www.trychroma.com) for vector storage
