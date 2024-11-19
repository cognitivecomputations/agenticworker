def scenario1():
    print("Running LangChain scenario1")

def scenario2():
    print("Running LangChain scenario2")

def run_langchain_scenario(scenario_name):
    if scenario_name == 'scenario1':
        scenario1()
    elif scenario_name == 'scenario2':
        scenario2()
    else:
        raise ValueError(f"Invalid scenario: langchain, {scenario_name}")