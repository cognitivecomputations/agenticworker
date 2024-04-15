def scenario1():
    print("Running CrewAI scenario1")

def scenario2():
    print("Running CrewAI scenario2")

def run_crewai_scenario(scenario_name):
    if scenario_name == 'scenario1':
        scenario1()
    elif scenario_name == 'scenario2':
        scenario2()
    else:
        raise ValueError(f"Invalid scenario: crewai, {scenario_name}")