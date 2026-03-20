
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
response = tavily_client.crawl("https://docs.tavily.com", instructions="Find all pages on the Python SDK")

# print(response)

response = tavily_client.search("Who is Leo Messi?")

# print(response)

response = tavily_client.extract("https://en.wikipedia.org/wiki/Artificial_intelligence")

# print(response)

response = tavily_client.map("https://docs.tavily.com")

print(response)
