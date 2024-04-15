import os
from memgpt import create_client, configure

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

# Define the assistant's persona
persona = """
I am MemGPT Assistant, a friendly and intelligent AI assistant created by MemGPT.
My goal is to help users with a wide variety of tasks to the best of my abilities.
I have broad knowledge spanning many subjects, and I'm always eager to learn more.
I communicate in a warm, empathetic, and thoughtful manner.
I'm here to assist with things like writing, analysis, math, coding, creative projects, and answering questions.
Please let me know how I can help!
"""

# Create the MemGPT agent with the assistant persona
agent = client.create_agent(name="MemGPT Assistant", persona=persona)

print("Welcome to the MemGPT Personal Assistant demo!")
print("You are now chatting with an AI assistant. Type 'quit' to exit.\n")

while True:
    user_input = input("User: ")
    
    if user_input.lower() == "quit":
        print("\nThank you for chatting with the MemGPT Assistant. Goodbye!")
        break
    
    messages = client.user_message(agent_id=agent.id, message=user_input)
    
    for msg in messages:
        if "assistant_message" in msg:
            print(f"Assistant: {msg['assistant_message']}")
        elif "internal_monologue" in msg:
            print(f"Assistant's Thoughts: {msg['internal_monologue']}")