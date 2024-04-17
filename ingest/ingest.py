from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

loader = TextLoader("ingest/docs/doc.md")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

index_name = "trafficengineering"

PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)



