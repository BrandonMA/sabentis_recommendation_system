import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import spacy

# Ensure you have installed the spaCy Spanish model using:
# python -m spacy download es_core_news_sm

nlp = spacy.load("es_core_news_sm")

file_paths = {
    "Auditorias": "txt/MANUAL AUDITORIAS_ESP (2).txt",
    "Ausentismo": "txt/MANUAL DE AUSENTISMO_ESP (2).txt",
    "Estructura Organizativa": "txt/MANUAL ESTRUCTURA ORGANIZATIVA_ESP (2).txt",
    "Riesgos": "txt/MANUAL IDENTIFICACION Y EVALUACION DE RIESGOS IER_ESP (1).txt",
    "Información": "txt/MANUAL INFORMACIÓN DOCUMENTADA_ESP (2).txt",
    "Emergencia": "txt/MANUAL PLANES DE EMERGENCIA_ESP (2).txt"
}

def load_documents():
    documents = {}
    for name, path in file_paths.items():
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            doc = Document(page_content=content)
            documents[name] = doc
    return documents

def split_text(documents: dict[str, Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=60,
        length_function=len,
        add_start_index=True,
    )
    split_chunks = {}
    for name in documents.keys():
        split_chunks[name] = []
        text = documents[name]
        doc_chunks = text_splitter.split_documents([text])
        doc_chunks = [chunk.page_content.replace('\n', ' ') for chunk in doc_chunks]
        split_chunks[name].extend(doc_chunks)
    return split_chunks

def process_text(text: str):
    doc = nlp(text)
    processed_text = ' '.join([token.lemma_ for token in doc if not token.is_stop])
    return processed_text

def process_and_save_chunks(manual_chunks: dict[str, list[str]], folder_name: str):
    for name, chunks in manual_chunks.items():
        processed_chunks = [process_text(chunk) for chunk in chunks]
        file_path = f"{folder_name}/{name.lower()}.txt"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n\n'.join(processed_chunks))

documents = load_documents()
manual_chunks = split_text(documents)

# Save original chunks
for name, chunks in manual_chunks.items():
    file_path = f"chunks/{name.lower()}.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(chunks))

# Process and save chunks with lemmatization and stop word removal
process_and_save_chunks(manual_chunks, "processed_chunks")
