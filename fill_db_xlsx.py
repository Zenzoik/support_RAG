import os
import pandas as pd
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from dotenv import load_dotenv
load_dotenv()

# === Путь к файлу Excel ===
DATA_PATH = "data/Today.ua_qa_pairs.xlsx"  # <-- сюда впишите реальный путь

# === Путь к ChromaDB ===
CHROMA_PATH = os.getenv("CHROMA_PATH")

# === Подключение к ChromaDB ===
os.makedirs(CHROMA_PATH, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name="Today.ua"
)

# === Загружаем все листы Excel в память ===
excel_data = pd.read_excel(DATA_PATH, sheet_name=None)

# Преобразуем в список Document
raw_documents = []
for sheet_name, df in excel_data.items():
    # превращаем в текст (CSV в виде строки)
    text = f"Лист: {sheet_name}\n" + df.to_csv(index=False)
    raw_documents.append(Document(page_content=text, metadata={"sheet": sheet_name}))

# === Разрезаем на чанки ===
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(raw_documents)

# === Заливаем в ChromaDB ===
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[f"doc_{i}"],
        documents=[chunk.page_content],
        metadatas=[chunk.metadata]
    )

print(f"Загружено {len(chunks)} чанков в ChromaDB")
