import os
from crewai_scenarios import Crew, Agent, Task, Process
from crewai_tools import WebsiteSearchTool, CSVSearchTool, DirectoryReadTool, FileReadTool

# Set up the necessary environment variables
os.environ["SERPER_API_KEY"] = "your_serper_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Create the researcher agent
researcher = Agent(
    role="Researcher",
    goal="Gather information on the topic: The Future of Artificial Intelligence",
    backstory="A skilled researcher with a background in AI and technology.",
    tools=[WebsiteSearchTool(), CSVSearchTool()],
    memory=True,
    verbose=True,
)

# Create the writer agent
writer = Agent(
    role="Writer",
    goal="Generate a well-structured and engaging blog post based on the researcher's findings",
    backstory="An experienced writer with a knack for creating captivating content.",
    tools=[DirectoryReadTool(directory="previous_blog_posts"), FileReadTool()],
    memory=True,
    verbose=True,
)

# Define the researcher's task
research_task = Task(
    description="Gather information on the topic: The Future of Artificial Intelligence",
    expected_output="A collection of relevant information and key points about the future of AI.",
    agent=researcher,
)

# Define the writer's task
writing_task = Task(
    description="Generate a blog post based on the researcher's findings",
    expected_output="A well-structured and engaging blog post about the future of AI.",
    agent=writer,
    output_file="generated_blog_post.md",
)

# Create the crew
blog_post_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
)

# Kick off the crew
result = blog_post_crew.kickoff()
print(result)