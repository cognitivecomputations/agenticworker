import os
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

# Configure the LLM
config_list = [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]

# Create a local command line code executor
code_executor = LocalCommandLineCodeExecutor(work_dir="./workspace")

# Code Writer Agent
code_writer = AssistantAgent(
    name="CodeWriter",
    description="Writes code based on user's task description",
    system_message="You are a coding assistant. Write code based on the user's task description.",
    llm_config={"config_list": config_list},
)

# Code Reviewer Agent
code_reviewer = AssistantAgent(
    name="CodeReviewer",
    description="Reviews code and provides feedback and suggestions",
    system_message="You are a code reviewer. Analyze the given code, provide feedback and suggestions for improvements.",
    llm_config={"config_list": config_list},
)

# User Proxy Agent
user_proxy = UserProxyAgent(
    name="UserProxy",
    code_execution_config={
        "last_n_messages": 2,  # Only pass last 2 messages to code executor
        "executor": code_executor,
    },
    human_input_mode="TERMINATE",  # Allow user input until 'exit' is typed
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

def review_code(task_description):
    code_writer.initiate_chat(
        user_proxy, message=f"Write code to: {task_description}"
    )
    
    for _ in range(3):  # 3 rounds of code review
        code_reviewer.initiate_chat(
            code_writer, message="Please review the code and provide feedback."
        )
        code_writer.initiate_chat(
            code_reviewer, message="Please update the code based on the feedback."
        )

# Example usage
review_code("Create a function that takes a list of integers and returns the sum of all even numbers in the list.")