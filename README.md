# LinkedIn Post Scraper and Doppelganger

## Project Overview

This project automates the process of scraping LinkedIn posts, performing web research, and generating new LinkedIn posts that emulate the writing style of a specific profile. The system is designed using a combination of web scraping tools, AI agents, and language models to achieve this functionality.

## Components

### Libraries and Tools Used

- **BeautifulSoup**: For parsing HTML content.
- **Selenium**: For web scraping and automation.
- **CrewAI**: For defining and managing agents and tasks.
- **LangChain**: For integrating with various language models.
- **dotenv**: For managing environment variables.

### Language Models

- **ChatGoogleGenerativeAI**: Utilized as the primary LLM (Large Language Model) with the `gemini-pro` model.
- **ChatMistralAI**: Used for generating LinkedIn posts, with the `mistral-large-latest` model.

### Agents

1. **LinkedIn Scraper Agent**
   - **Role**: Scrapes LinkedIn posts.
   - **Goal**: Scrape LinkedIn.
   - **Backstory**: Expert in web scraping.

2. **Web Searcher Agent**
   - **Role**: Searches for topics on the web.
   - **Goal**: Search for a topic on the web.
   - **Backstory**: Expert in web scraping and research.

3. **Doppelganger Agent**
   - **Role**: Creates LinkedIn posts.
   - **Goal**: Create a LinkedIn post comparing Llama 2 and Llama 3.
   - **Backstory**: Expert in emulating LinkedIn influencer writing styles.

### Tasks

1. **Scrape LinkedIn Task**
   - **Description**: Scrape a LinkedIn profile to get some relevant posts.
   - **Expected Output**: A list of LinkedIn posts obtained from a LinkedIn profile.
   - **Agent**: LinkedIn Scraper Agent.

2. **Web Research Task**
   - **Description**: Gather high-quality information about the comparison between Llama 2 and Llama 3.
   - **Expected Output**: High-quality information about the comparison between Llama 2 and Llama 3.
   - **Agent**: Web Searcher Agent.

3. **Create LinkedIn Post Task**
   - **Description**: Create a LinkedIn post comparing Llama 2 and Llama 3 following the writing style expressed in the scraped LinkedIn posts.
   - **Expected Output**: A high-quality and engaging LinkedIn post comparing Llama 2 and Llama 3, emulating the writing style of the scraped LinkedIn posts.
   - **Agent**: Doppelganger Agent.
   - **Context**: Uses output from Scrape LinkedIn Task and Web Research Task.

### Project Workflow

1. **Setup**: Load environment variables using `dotenv` and initialize the language models.
2. **Define Agents**: Create agents for scraping LinkedIn posts, performing web research, and generating new LinkedIn posts.
3. **Define Tasks**: Create tasks that describe the scraping, research, and post-creation processes.
4. **Assemble Crew**: Combine agents and tasks into a `Crew`.
5. **Execute**: Kick off the `Crew` to perform the tasks and achieve the project goals.
6. **Scraping Function**: Use Selenium and BeautifulSoup to scrape LinkedIn posts.
7. **Run Tasks**: Execute each task in sequence, using the results of previous tasks as context for subsequent ones.

### Example Execution

```python
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

from crewai import Crew 
from dotenv import load_dotenv
from agents import linkedin_scraper_agent,web_search_agent,doppelganger_agent

from tasks import scrape_linkedin_task,create_linkedin_post_task,web_research_task

load_dotenv()

crew = Crew(
    agents=[
        linkedin_scraper_agent,
        web_search_agent,
        doppelganger_agent
    ],
    tasks=[
        scrape_linkedin_task,
        web_research_task,
        create_linkedin_post_task
    ]
)

result = crew.kickoff()

print("Here is the result: ")
print(result)

from tools import scrape_linkedin_posts_fn

print(scrape_linkedin_posts_fn())

from crewai import Task
from textwrap import dedent 
from agents import web_search_agent,doppelganger_agent,linkedin_scraper_agent

scrape_linkedin_task = Task(
    description=dedent(
        "Scrape a LinkedIn profile to get some relevant posts"),
    expected_output=dedent("A list of LinkedIn posts obtained from a LinkedIn profile"),
    agent=linkedin_scraper_agent,
)

web_research_task = Task(
    description=dedent(
        "Get valuable and high quality web information about the comparison between Llama 2 and Llama 3"),
    expected_output=dedent("Your task is to gather high quality information about the comparison"
                           " between Llama 2 and Llama 3"),
    agent=web_search_agent,
)

create_linkedin_post_task = Task(
    description=dedent(
        "Create a LinkedIn post comparing Llama 2 and Llama 3 following the writing-style "
        "expressed in the scraped LinkedIn posts."
    ),
    expected_output=dedent("A high-quality and engaging LinkedIn post comparing Llama 2 and Llama 3."
                           " The LinkedIn post must follow"
                           " the same writing-style as the one expressed in the scraped LinkedIn posts"),
    agent=doppelganger_agent,
)

create_linkedin_post_task.context = [scrape_linkedin_task, web_research_task]

```
LINKEDIN_EMAIL=<your-linkedin-email>
LINKEDIN_PASSWORD=<your-linkedin-password>
GOOGLE_API_KEY=<your-google-api-key>
MISTRAL_API_KEY=<your-mistral-api-key>

## Output
The output will include:

Scraped LinkedIn posts.
Research information about Llama 2 and Llama 3.
Generated LinkedIn post comparing Llama 2 and Llama 3 in the writing style of the scraped LinkedIn posts.


## Sample Output 
![Screenshot (289)](https://github.com/Idk507/Linkedin_Automation_Crew_Gemini/assets/93417785/5a94af46-1077-44c4-af7a-81b359baf487)

