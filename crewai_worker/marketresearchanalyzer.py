import os
from crewai_scenarios import Crew, Agent, Task, Process
from crewai_tools import CSVSearchTool, WebsiteSearchTool, tool
from langchain_openai import ChatOpenAI

# Set up the necessary environment variables
os.environ["SERPER_API_KEY"] = "your_serper_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

@tool("Market Research API")
def market_research_api(query: str) -> str:
    # Implementation of the market research API access logic
    # This is a placeholder and should be replaced with the actual implementation
    return "Market research data"

# Create the data collector agent
data_collector = Agent(
    role="Data Collector",
    goal="Gather market research data on the topic: Smartphone Market Trends",
    backstory="An efficient data collector with expertise in market research.",
    tools=[CSVSearchTool(), WebsiteSearchTool(), market_research_api],
    memory=True,
    verbose=True,
    cache=True,
)

# Create the analyst agent
analyst = Agent(
    role="Analyst",
    goal="Analyze the collected market research data to identify trends, patterns, and insights",
    backstory="A skilled analyst with a keen eye for data interpretation.",
    memory=True,
    verbose=True,
    cache=True,
)

# Create the report generator agent
report_generator = Agent(
    role="Report Generator",
    goal="Create a comprehensive market research report based on the analyst's findings",
    backstory="An experienced report writer with a talent for creating compelling market research reports.",
    memory=True,
    verbose=True,
    cache=True,
)

# Define the data collection task
data_collection_task = Task(
    description="Gather market research data on the topic: Smartphone Market Trends",
    expected_output="A collection of relevant market research data on smartphone market trends.",
    agent=data_collector,
)

# Define the data analysis task
data_analysis_task = Task(
    description="Analyze the collected market research data to identify trends, patterns, and insights",
    expected_output="A summary of key trends, patterns, and insights from the market research data.",
    agent=analyst,
)

# Define the report generation task
report_generation_task = Task(
    description="Create a comprehensive market research report based on the analyst's findings",
    expected_output="A well-structured and informative market research report on smartphone market trends.",
    agent=report_generator,
    output_file="market_research_report.md",
)

# Create the crew
market_research_crew = Crew(
    agents=[data_collector, analyst, report_generator],
    tasks=[data_collection_task, data_analysis_task, report_generation_task],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),
)

# Kick off the crew
result = market_research_crew.kickoff()
print(result)