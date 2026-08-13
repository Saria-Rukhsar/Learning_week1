import os
from doc_loader import chunk_text, load_document
from dotenv import load_dotenv
from google import genai
from q_a import QAEngine
from vec_store import SimpleVectorStore

# .env file se API Key load karna
load_dotenv()


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. \nSet your API key in the .env file.")
        return

    client = genai.Client(api_key=api_key)
    vector_store = SimpleVectorStore(client)
    qa_engine = QAEngine(client)

    print("==========================================")
    print("      CLI Document Q&A Assistant          ")
    print("==========================================")

    while True:
        file_path = input("\nEnter document path (PDF, TXT, DOCX): ").strip()
        file_path = file_path.strip("'\"")

        try:
            print("Reading Document...")
            raw_text = load_document(file_path)

            print("Chunking Document...")
            chunks = chunk_text(raw_text)
            print(f"Total {len(chunks)} chunks are created.")

            vector_store.add_chunks(chunks)
            break
        except Exception as e:
            print(f"Error: {e}.\n Give file again.")

    print("\n------------------------------------------")
    print("Document ready! Sawaal poochen (exit/quit likhein band krne k liye):")
    print("------------------------------------------\n")

    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() in ["exit", "quit"]:
            print("Good Bye!")
            break

        relevant_chunks = vector_store.search(query, top_k=3)
        answer = qa_engine.generate_answer(query, relevant_chunks)
        print(f"\nBot: {answer}\n")

if __name__ == "__main__":
    main()