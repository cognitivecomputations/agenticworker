def scenario1():
    print("Running MemGPT scenario1")

def scenario2():
    print("Running MemGPT scenario2")

def run_memgpt_scenario(scenario_name):
    if scenario_name == 'scenario1':
        scenario1()
    elif scenario_name == 'scenario2':
        scenario2()
    else:
        raise ValueError(f"Invalid scenario: memgpt, {scenario_name}")