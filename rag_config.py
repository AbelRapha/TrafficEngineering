from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI , GoogleGenerativeAIEmbeddings
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Config Vector DB and retriver

index_name = "trafficengineering"

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

docsearch = PineconeVectorStore(embedding = embeddings, index_name=index_name)

retriever = docsearch.as_retriever(search_type="mmr")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Prompt Template

llm_prompt_template = """Você agora é um assistente que responderá perguntas sobre o capítulo de um livro relacionado a engenharia de tráfego.
Sendo assim, apenas utilize do contexto para se basear e criar uma resposta coesa. 
Sempre responda no idioma Portguês do Brasil.
Caso você não encontre a resposta diga: 'Desculpe, tente refazer a sua pergunta'.\n
Contexto: {context} \nPergunta: {question} \nResposta:"""

llm_prompt = PromptTemplate.from_template(llm_prompt_template)

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5, top_p=1)
    
rag_chain = (
    {"context": retriever | format_docs ,"question": RunnablePassthrough()}
    | llm_prompt
    | llm
    | StrOutputParser()
)

def invoke_chain(query):
    return rag_chain.stream(query)
