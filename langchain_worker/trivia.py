import os
from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import WikipediaLoader

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Load Wikipedia data
doc_path = "path_to_your_wikipedia_data"
loader = WikipediaLoader(doc_path)
docs = loader.load()

# Create embeddings and vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# Wikipedia search tool
def wikipedia_search(query):
    docs = vectorstore.similarity_search(query)
    return "\n".join([doc.page_content for doc in docs][:3])

# Multiple choice tool
def multiple_choice(query, choices):
    prompt = f"""Given the following question and choices, select the most appropriate answer:

    Question: {query}
    Choices: {choices}

    Answer:"""
    chain = LLMChain(llm=OpenAI(temperature=0), prompt=PromptTemplate.from_template(prompt))
    return chain.predict(query=query, choices=choices)

# Create tools list
tools = [
    Tool(name="Wikipedia Search", func=wikipedia_search, description="Useful for searching Wikipedia for relevant information."),
    Tool(name="Multiple Choice", func=multiple_choice, description="Useful for selecting the most appropriate answer from given choices.")
]

# Initialize agent
agent = initialize_agent(tools, OpenAI(temperature=0), agent="zero-shot-react-description", verbose=True)

# Main loop
while True:
    print("\nWelcome to the Trivia Game Agent!")
    question = input("Please enter your trivia question or type 'exit' to quit: ")
    
    if question.lower() == "exit":
        print("Thank you for playing the Trivia Game Agent. Goodbye!")
        break
    
    choices_input = input("Please enter the answer choices separated by commas: ")
    choices = [choice.strip() for choice in choices_input.split(",")]
    
    result = agent.run(f"Question: {question}\nChoices: {', '.join(choices)}")
    print(f"\nResult: {result}")