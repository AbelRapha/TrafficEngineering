from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
load_dotenv()

pc = Pinecone(api_key= os.getenv('PINECONE_API_KEY'))

pc.create_index(
    name="trafficengineering",
    dimension=768, # Replace with your model dimensions
    metric="euclidean", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)