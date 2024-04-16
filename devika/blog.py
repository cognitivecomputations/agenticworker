from devika import Devika

def automate_scenario_1():
    # Initialize Devika
    devika = Devika(base_model='claude-3-haiku-20240307', search_engine='google')

    # User prompt
    user_prompt = "Devika, I'd like to create a personal blog website. It should have a modern design, an about me page, and the ability for me to easily write and publish blog posts. Can you build this for me?"

    # Create a new project
    project_name = "Personal Blog Website"
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

    # Extract the blog URL from the latest message
    blog_url = extract_url_from_message(latest_message['message'])

    # Print the blog URL
    print(f"Personal blog website created successfully! URL: {blog_url}")

def extract_url_from_message(message):
    # Extract the URL from the message using regular expressions or string manipulation
    # This function should be implemented based on the expected format of the URL in the message
    # For simplicity, let's assume the URL is the last word in the message
    return message.split()[-1]

# Run the automation
automate_scenario_1()