import argparse
from autogen import run_autogen_scenario
from memgpt import run_memgpt_scenario
from langchain import run_langchain_scenario
from crewai import run_crewai_scenario

def main():
    parser = argparse.ArgumentParser(description='Worker Node')
    parser.add_argument('framework', choices=['autogen', 'memgpt', 'langchain', 'crewai'], help='The framework to use')
    parser.add_argument('scenario', help='The scenario to run')
    args = parser.parse_args()

    if args.framework == 'autogen':
        run_autogen_scenario(args.scenario)
    elif args.framework == 'memgpt':
        run_memgpt_scenario(args.scenario)
    elif args.framework == 'langchain':
        run_langchain_scenario(args.scenario)
    elif args.framework == 'crewai':
        run_crewai_scenario(args.scenario)
    else:
        raise ValueError(f"Invalid framework: {args.framework}")

if __name__ == '__main__':
    main()