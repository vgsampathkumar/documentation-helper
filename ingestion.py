import asyncio
import os
import ssl
from typing import Any, Dict ,List
import certifi
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_tavily  import TavilyCrawl,TavilyExtract,TavilyMap

from logger import (Colors, log_info, log_success, log_error, log_warning, log_header)

load_dotenv()

# Configure SSL context to use certifi's Certificate Authority bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


embeddings = OpenAIEmbeddings(model="text-embedding-3-small",show_progress_bar=True, chunk_size=50,retry_min_seconds=10)

#chroma=Chroma(collection_name="langchain-docs", embedding_function=embeddings, persist_directory="./chroma_db") 

vectorstore=PineconeVectorStore(
    index_name=os.getenv("INDEX_NAME"),
    embedding=embeddings,
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)
    
tavily_extract=TavilyExtract()
tavily_map=TavilyMap(max_depth=3,max_breadth=20, max_pages=1000)
tavily_crawl=TavilyCrawl()


async def main():
    print("Excited to start the web crawl!")
    log_header("Starting Web Crawl with Tavily")
    log_header("Documentation Ingestion Pipeline")
    log_info(" TavilyCrawl Starting to crawl docuemntation from https://python.langchain.com",Colors.PURPLE)
    #Crawl the documentation
    res=tavily_crawl.invoke({"url":"https://python.langchain.com",
                             "max_depth":1,
                             "extract_depth":"advanced"})

    all_docs=res["results"]
    log_success(f"Successfully crawled {len(all_docs)} documents from the website.")
    log_info(f"the contents {all_docs}")

if __name__ == "__main__":
    asyncio.run(main())