import os
from autogen_scenarios import RetrieveAssistantAgent, RetrieveUserProxyAgent
from autogen.retrievechat import ChromaRetriever

# Configure the LLM
config_list = [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]

# Set up the vector database and index the research papers
papers_folder = "./research_papers"  # Folder containing research papers
chroma_retriever = ChromaRetriever(
    docs_path=papers_folder,
    chunk_token_size=200,
    embedding_model="all-mpnet-base-v2",
)

# Chatbot Assistant Agent
chatbot = RetrieveAssistantAgent(
    name="Chatbot",
    system_message="You are a helpful assistant who answers questions based on the provided research papers.",
    llm_config={"config_list": config_list},
)

# User Proxy Agent
user_proxy = RetrieveUserProxyAgent(
    name="UserProxy",
    retrieve_config={
        "retriever": chroma_retriever,
        "search_kwargs": {"k": 3},  # Retrieve top 3 relevant chunks
    },
    human_input_mode="TERMINATE",  # Allow user input until 'exit' is typed
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

def ask_question(question):
    user_proxy.initiate_chat(chatbot, message=question)

# Example usage
ask_question("What are the main challenges in developing robust language models?")