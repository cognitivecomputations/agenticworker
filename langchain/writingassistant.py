import os
from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Grammar/spelling checker tool
def grammar_checker(text):
    prompt = f"""Please correct the grammar and spelling in the following text: 
    
    Text: {text}
    
    Corrected text:"""
    chain = LLMChain(llm=OpenAI(temperature=0), prompt=PromptTemplate.from_template(prompt))
    return chain.predict(text=text)

# Summarizer tool
def summarizer(text):
    prompt = f"""Please provide a concise summary of the following text:
    
    Text: {text}
    
    Summary:"""
    chain = LLMChain(llm=OpenAI(temperature=0), prompt=PromptTemplate.from_template(prompt))
    return chain.predict(text=text)

# Tone analyzer tool
def tone_analyzer(text):
    prompt = f"""Analyze the tone of the following text and suggest ways to improve it:
    
    Text: {text}
    
    Tone analysis and suggestions:"""
    chain = LLMChain(llm=OpenAI(temperature=0), prompt=PromptTemplate.from_template(prompt))
    return chain.predict(text=text)

# Thesaurus tool
def thesaurus(word):
    prompt = f"""Please provide synonyms for the word '{word}':"""
    chain = LLMChain(llm=OpenAI(temperature=0), prompt=PromptTemplate.from_template(prompt))
    return chain.predict(word=word)

# Create tools list
tools = [
    Tool(name="Grammar Checker", func=grammar_checker, description="Useful for correcting grammar and spelling."),
    Tool(name="Summarizer", func=summarizer, description="Useful for summarizing text."),
    Tool(name="Tone Analyzer", func=tone_analyzer, description="Useful for analyzing and improving the tone of text."),
    Tool(name="Thesaurus", func=thesaurus, description="Useful for finding synonyms.")
]

# Initialize agent
agent = initialize_agent(tools, OpenAI(temperature=0), agent="zero-shot-react-description", verbose=True)

# Main loop
while True:
    print("\nWelcome to the Writing Assistant Agent!")
    user_input = input("Please enter your text or type 'exit' to quit: ")
    
    if user_input.lower() == "exit":
        print("Thank you for using the Writing Assistant Agent. Goodbye!")
        break
    
    result = agent.run(user_input)
    print(f"\nResult: {result}")