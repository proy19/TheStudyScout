from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
import pdfplumber
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv
import gradio as gr

def load_pdfs(folder):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            with pdfplumber.open(os.path.join(folder, filename)) as pdf:
                text = "\n".join([
                    page.extract_text() for page in pdf.pages
                    if page.extract_text()
                ])
            docs.append(Document(
                page_content=text,
                metadata={"source": filename}
            ))
    print(f"Loaded {len(docs)} PDF documents")
    return docs

pdf_docs = load_pdfs("./pdfs")

def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=40,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks from {len(docs)} documents")
    return chunks

chunks = chunk_docs(pdf_docs)

for i, chunk in enumerate(chunks):
    print(f"\n{'='*50}")
    print(f"Chunk {i+1} | Source: {chunk.metadata.get('source', 'unknown')}")
    print(f"Length: {len(chunk.page_content)} chars")
    print(f"{'-'*50}")
    print(chunk.page_content)

print(f"\nTotal chunks: {len(chunks)}")

def embed_chunks(chunks):
    model      = SentenceTransformer("all-MiniLM-L6-v2")
    texts      = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    print(f"Embedded {len(embeddings)} chunks")
    return model, texts, embeddings

def store_embeddings(texts, embeddings, chunks):
    client     = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("study_spots")

    collection.add(
        documents  = texts,
        embeddings = embeddings.tolist(),
        metadatas  = [chunk.metadata for chunk in chunks],
        ids        = [f"chunk_{i}" for i in range(len(texts))]
    )
    print(f"Stored {len(texts)} chunks in Chroma")
    return collection

model, texts, embeddings = embed_chunks(chunks)

collection               = store_embeddings(texts, embeddings, chunks)

def retrieve(query, collection, model, k=5):
    query_embedding = model.encode([query]).tolist()
    results         = collection.query(
        query_embeddings = query_embedding,
        n_results        = k
    )

    docs = []
    for i in range(len(results["documents"][0])):
        docs.append({
            "text":   results["documents"][0][i],
            "source": results["metadatas"][0][i].get("source", "unknown")
        })
    return docs

# test retrieval
query   = "quiet spot with outlets open late"
results = retrieve(query, collection, model)

for r in results:
    print(f"\nSource: {r['source']}")
    print(r["text"])
    print("---")

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate(query, k=5):
    results = retrieve(query, collection, model, k)
    context = "\n".join([r["text"] for r in results])
    sources = list(set([r["source"] for r in results]))

    response = client.chat.completions.create(
        model    = "meta-llama/llama-4-scout-17b-16e-instruct",
        messages = [
            {
                "role":    "system",
                "content": "You are a helpful assistant that recommends study spots to students. Only answer using the context provided."
            },
            {
                "role":    "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ]
    )

    answer  = response.choices[0].message.content
    src_str = "\n".join([f"- {s}" for s in sources])

    return answer, src_str

def ask(query):
    answer, sources = generate(query)
    return answer, sources

with gr.Blocks(title="Study Spots Finder") as app:
    gr.Markdown("## Study Spots Finder")
    gr.Markdown("Ask anything about study spots on campus.")

    with gr.Row():
        query_box = gr.Textbox(
            label       = "Your question",
            placeholder = "What is the best study spot that serves coffee?",
            scale       = 4
        )
        submit_btn = gr.Button("Ask", variant="primary", scale=1)

    with gr.Row():
        answer_box = gr.Textbox(label="Answer", lines=6)

    with gr.Row():
        sources_box = gr.Textbox(label="Sources", lines=3)

    submit_btn.click(
        fn      = ask,
        inputs  = [query_box],
        outputs = [answer_box, sources_box]
    )

    query_box.submit(
        fn      = ask,
        inputs  = [query_box],
        outputs = [answer_box, sources_box]
    )

app.launch()
