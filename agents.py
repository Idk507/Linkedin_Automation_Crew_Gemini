import os 
from textwrap import dedent 
from crewai import Agent 
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import DuckDuckGoSearchRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
# Set up Gemini Pro as the LLM
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.5,
    google_api_key=""
)

mistral_llm = ChatMistralAI(
    model="mistral-large-latest",
    verbose=True,
    temperature=0.5,
    mistral_api_key= ""
)

scrape_website_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()

linkedin_scraper_agent = Agent(
    role = "Linkedin Scraper",
    goal = "Scrape Linkedin",
    backstory = """
    You are a programmzise expertise and perform good at web scraping""",
    verbose = True,
    tools = [scrape_website_tool,search_tool],
    llm = gemini_llm,
  
)

web_search_agent = Agent(
    role = "Web Searcher",
    goal = "Search for a topic on the web",
    backstory = """
    You are a programmzise expertise and perform good at web scraping""",
    verbose = True,
    tools = [search_tool],
    llm = gemini_llm,

)

doppelganger_agent = Agent(
    role="LinkedIn Post Creator",
    goal="You will create a LinkedIn post comparing Llama 2 and Llama 3 following the writing style "
         "observed in the LinkedIn posts scraped by the LinkedIn Post Scraper.",
    backstory=dedent(
        """
        You are an expert in writing LinkedIn posts replicating any influencer style
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=mistral_llm
)