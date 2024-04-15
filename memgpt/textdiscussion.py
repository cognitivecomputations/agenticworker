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

# Define the file path for the book/article
file_path = "path/to/your/book_or_article.txt"  # Replace with the path to your book or article file

# Create a data source and load the book/article into it
source = client.create_source(name="Book/Article")
client.load_file_into_source(filename=file_path, source_id=source.id)

# Define the discussion partner's persona
persona = """
I am an AI book/article discussion partner created by MemGPT.
My role is to engage in in-depth discussions about the content of the book or article provided to me.
I can answer questions, share my perspective, and relate ideas to other concepts I've learned.
I aim to provide thoughtful and insightful responses to help the user better understand and analyze the material.
"""

# Create the MemGPT agent with the discussion partner persona
agent = client.create_agent(name="MemGPT Discussion Partner", persona=persona)

# Attach the book/article data source to the agent's memory
client.attach_source_to_agent(source_name="Book/Article", agent_id=agent.id)

print("Welcome to the MemGPT Book/Article Discussion Partner demo!")
print("You are now chatting with an AI that has read the provided book/article.")
print("Ask questions, share your thoughts, and engage in a discussion about the content.")
print("Type 'quit' to exit.\n")

while True:
    user_input = input("User: ")
    
    if user_input.lower() == "quit":
        print("\nThank you for discussing the book/article with the MemGPT Discussion Partner. Goodbye!")
        break
    
    messages = client.user_message(agent_id=agent.id, message=user_input)
    
    for msg in messages:
        if "assistant_message" in msg:
            print(f"Assistant: {msg['assistant_message']}")
        elif "internal_monologue" in msg:
            print(f"Assistant's Thoughts: {msg['internal_monologue']}")