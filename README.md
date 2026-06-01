# AI PDF Chatbot & Medical Report Analyzer

An AI-powered PDF Chatbot built using LangChain, FAISS, Google Gemini, and Streamlit.

The application allows users to upload PDF documents, ask questions, generate summaries, extract important information, and create doctor-friendly medical report insights using Retrieval Augmented Generation (RAG).

---

## Features

### General PDF Analysis

* Upload PDF documents
* Ask questions from uploaded PDFs
* Generate document summaries
* Retrieve relevant source chunks
* Page-level source attribution

### Medical Report Analysis

* Extract patient details
* Highlight abnormal laboratory values
* Generate clinical summaries
* Provide doctor-friendly insights
* Display key test values and reference ranges

---

## Tech Stack

### Frontend

* Streamlit

### AI & RAG

* LangChain
* Google Gemini
* FAISS Vector Database

### Document Processing

* PyPDF
* RecursiveCharacterTextSplitter

### Embeddings

* Google Generative AI Embeddings

---

## Architecture

User Uploads PDF

↓

PyPDF Text Extraction

↓

Text Chunking

↓

Gemini Embeddings

↓

FAISS Vector Database

↓

Similarity Search

↓

Gemini LLM

↓

Answer Generation with Source Citations

---

## Example Use Cases

### General PDF Queries

* Summarize this document
* Explain the key concepts
* What is velocity?
* What are the main conclusions?

### Medical Reports

* Summarize this report
* Extract patient details
* Show abnormal findings
* Provide doctor insights
* Generate clinical impression

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Gautams1990/AI-PDF-Chatbot-RAG.git
cd AI-PDF-Chatbot-RAG
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create .env File

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

### Run Application

```bash
streamlit run app.py
```

---

## Screenshots

### Home Page

(Add Screenshot Here)

### PDF Upload

(Add Screenshot Here)

### Medical Report Summary

(Add Screenshot Here)

### Retrieved Source Chunks

(Add Screenshot Here)

---

## Project Highlights

* Retrieval Augmented Generation (RAG)
* Semantic Search using FAISS
* Gemini-powered Question Answering
* Medical Report Understanding
* Source-Based Answers
* Live Streamlit Deployment

---

## Future Improvements

* Chat Memory
* Multi-document comparison
* PDF export of summaries
* Advanced medical risk scoring
* Doctor dashboard
* OCR support for scanned PDFs

---

## Author

Gautam Sharma

Mechanical Engineering Graduate | Physics Educator | Aspiring AI Engineer

GitHub:
https://github.com/Gautams1990
