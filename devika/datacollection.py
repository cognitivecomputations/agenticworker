from devika import Devika

def automate_scenario_3():
    # Initialize Devika
    devika = Devika(base_model='claude-3-haiku-20240307', search_engine='google')

    # User prompt
    user_prompt = "Devika, I need to collect data on all 500 companies in the Fortune 500 - their revenues, # of employees, headquarters location, and main industry. Can you collect this data for me and compile it into a spreadsheet?"

    # Create a new project
    project_name = "Fortune 500 Data Collection"
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

    # Extract the spreadsheet URL from the latest message
    spreadsheet_url = extract_url_from_message(latest_message['message'])

    # Print the spreadsheet URL
    print(f"Fortune 500 data collected successfully! Spreadsheet URL: {spreadsheet_url}")

def extract_url_from_message(message):
    # Extract the URL from the message using regular expressions or string manipulation
    # This function should be implemented based on the expected format of the URL in the message
    # For simplicity, let's assume the URL is the last word in the message
    return message.split()[-1]

# Run the automation
automate_scenario_3()