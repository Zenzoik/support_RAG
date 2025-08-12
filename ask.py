import chromadb
from dotenv import load_dotenv
from llm_client.openai_client import generate_answer
import os
load_dotenv()

# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = os.getenv("CHROMA_PATH")

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="Today.ua")


async def handle_message(user_query: str) -> str:
    results = collection.query(
        query_texts=[user_query],
        n_results=1
    )
    print(results['documents'])
    prompt = (
        "Відповідай лише з CONTEXT. Якщо точної відповіді немає — напиши стандартну фразу.\n"
        f"CONTEXT:\n{results['documents']}\n\nQUESTION:\n{user_query}"
    )
    response = generate_answer(prompt)
    return response

#print(results['metadatas'])
