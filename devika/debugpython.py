from devika import Devika

def automate_scenario_2():
    # Initialize Devika
    devika = Devika(base_model='claude-3-haiku-20240307', search_engine='google')

    # Sample Python code with errors
    code_with_errors = '''
def analyze_sales_data(data):
    total_sales = 0
    for sale in data
        total_sales += sale['amount']
    average_sales = total_sales / len(data)
    print("Total Sales:", total_sale)
    print("Average Sales:", average_sales)

data = [
    {'id': 1, 'amount': 1000},
    {'id': 2, 'amount': 1500},
    {'id': 3, 'amount': 2000},
    {'id': 4, 'amount': 1200}
]

analyze_sales_data(data)
'''

    # User prompt
    user_prompt = f"Hi Devika, I'm working on this Python script to analyze some sales data but I'm getting errors when I run it. Here's my code:\n\n{code_with_errors}\n\nCan you debug this and get it working?"

    # Create a new project
    project_name = "Sales Data Analysis"
    devika.project_manager.create_project(project_name)

    # Add user message
    devika.project_manager.add_message_from_user(project_name, user_prompt)

    # Execute Devika
    devika.execute(user_prompt, project_name)

    # Wait for Devika to complete the task
    while not devika.agent_state.is_agent_completed(project_name):
        pass

    # Get the latest message from Devika
    latest_message = devika.project_manager.get_latest_message_from_devika(project_name)

    # Extract the debugged code from the latest message
    debugged_code = extract_code_from_message(latest_message['message'])

    # Print the debugged code
    print("Debugged Code:")
    print(debugged_code)

def extract_code_from_message(message):
    # Extract the code block from the message using string manipulation
    # Assuming the code block is enclosed in triple backticks (```)
    start_index = message.find("```python") + len("```python")
    end_index = message.find("```", start_index)
    code_block = message[start_index:end_index].strip()
    return code_block

# Run the automation
automate_scenario_2()