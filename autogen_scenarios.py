def scenario1():
    print("Running AutoGen scenario1")

def scenario2():
    print("Running AutoGen scenario2")

def run_autogen_scenario(scenario_name):
    if scenario_name == 'scenario1':
        scenario1()
    elif scenario_name == 'scenario2':
        scenario2()
    else:
        raise ValueError(f"Invalid scenario: autogen, {scenario_name}")