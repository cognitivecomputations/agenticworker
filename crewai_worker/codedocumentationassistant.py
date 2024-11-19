import os
from crewai_scenarios import Crew, Agent, Task
from crewai_tools import CodeDocsSearchTool, GithubSearchTool, tool

# Set up the necessary environment variables
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

def agent_step_callback(step: dict):
    print(f"Step: {step['step']}, Action: {step['action']}, Observation: {step['observation']}")

@tool("Code Snippet Extractor")
def extract_code_snippet(docs_url: str) -> str:
    # Implementation of code snippet extraction logic
    # This is a placeholder and should be replaced with the actual implementation
    return "Extracted code snippet"

# Create the code documentation assistant agent
code_assistant = Agent(
    role="Code Documentation Assistant",
    goal="Help developers find relevant information within code documentation",
    backstory="An AI-powered assistant specializing in code documentation search and retrieval.",
    tools=[
        CodeDocsSearchTool(),
        GithubSearchTool(content_types=["code", "issue"]),
        extract_code_snippet,
    ],
    verbose=True,
    max_iter=5,
    step_callback=agent_step_callback,
)

# Define the code documentation search task
search_task = Task(
    description="Search code documentation for information on 'Python list comprehension'",
    expected_output="Relevant information and code examples related to Python list comprehension.",
    agent=code_assistant,
)

# Create the crew
documentation_crew = Crew(
    agents=[code_assistant],
    tasks=[search_task],
)

# Kick off the crew
result = documentation_crew.kickoff()
print(result)