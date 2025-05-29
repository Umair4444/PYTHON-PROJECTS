from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from document import documents
from uuid import uuid4
from dotenv import load_dotenv
import os

load_dotenv()

pinecone_api_key = os.getenv('PINECONE_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')

if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY is not set in .env file")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file")

# print("Gemini Key:", gemini_api_key)
# print("Pinecone Key:", pinecone_api_key)

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index_name = "testing-rag"

# The Gemini embedding model returns vectors of dimension 1536
embedding_dimension = 768

# Create index if it doesn't exist
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=embedding_dimension,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Connect to index
index = pc.Index(index_name)

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model='models/text-embedding-004',
    google_api_key=gemini_api_key
)

# Test embedding
vector = embeddings.embed_query("hello world")
# print(vector[:5])
print(len(vector))
print("-------------------------------------------------------------------------------------")

try:
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    # print("Vector Store Initialized:", vector_store)

    # Create unique IDs for each document
    uuids = [str(uuid4()) for _ in range(len(documents))]
    # print("UUIDs:", uuids)
    # print("Documents:", documents)

    # Add documents to vector store
    vector_store.add_documents(documents=documents, ids=uuids)
    print("Documents added successfully")

except Exception as e:
    print(f"Error occurred: {e}")

else:
    print("Successfully completed!")

vector_result = vector_store.similarity_search(
    """Langchain provide abs to make work with llm easy""",
    k=4,
    filter={'source' : "tweet"}
)

for res in vector_result:
    print(f"* {res.page_content} ==> {res.metadata}")
