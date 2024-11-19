import os
from memgpt_scenarios import create_client, configure

# Configure MemGPT
configure(
    model_endpoint_type="openai",
    model_endpoint="https://api.openai.com/v1",  # Replace with your OpenAI endpoint
    openai_key=os.environ["OPENAI_API_KEY"],  # Set your OpenAI API key as an environment variable
    storage_backend="local",
    db_uri="sqlite:///:memory:",  # Use an in-memory SQLite database
)

# Create a MemGPT client
client = create_client()

# Define the historical figure's name and background information file path
historical_figure_name = "Albert Einstein"
background_file_path = "path/to/albert_einstein_background.txt"  # Replace with the path to the background file

# Create a data source and load the background information into it
source = client.create_source(name=f"{historical_figure_name} Background")
client.load_file_into_source(filename=background_file_path, source_id=source.id)

# Define the historical figure's persona
persona = f"""
I am {historical_figure_name}, the famous historical figure.
I will engage in conversation with users, drawing upon my life experiences, views, and accomplishments.
I aim to provide authentic and insightful responses based on the knowledge provided about me.
Users can ask me about my life, debate ideas with me, and get my perspective on various topics.
"""

# Create the MemGPT agent with the historical figure's persona
agent = client.create_agent(name=historical_figure_name, persona=persona)

# Attach the background information data source to the agent's memory
client.attach_source_to_agent(source_name=f"{historical_figure_name} Background", agent_id=agent.id)

print(f"Welcome to the MemGPT Historical Figure Roleplaying Chatbot demo!")
print(f"You are now chatting with {historical_figure_name}.")
print(f"Ask about their life, debate ideas, and get their perspective on various topics.")
print("Type 'quit' to exit.\n")

while True:
    user_input = input("User: ")
    
    if user_input.lower() == "quit":
        print(f"\nThank you for chatting with {historical_figure_name}. Goodbye!")
        break
    
    messages = client.user_message(agent_id=agent.id, message=user_input)
    
    for msg in messages:
        if "assistant_message" in msg:
            print(f"{historical_figure_name}: {msg['assistant_message']}")
        elif "internal_monologue" in msg:
            print(f"{historical_figure_name}'s Thoughts: {msg['internal_monologue']}")