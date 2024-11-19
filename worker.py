import argparse
import logging
from autogen_scenarios import run_autogen_scenario
from memgpt_scenarios import run_memgpt_scenario
from langchain_scenarios import run_langchain_scenario
from crewai_scenarios import run_crewai_scenario

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        parser = argparse.ArgumentParser(description='Worker Node')
        parser.add_argument('framework', choices=['autogen', 'memgpt', 'langchain', 'crewai'], help='The framework to use')
        parser.add_argument('scenario', help='The scenario to run')
        args = parser.parse_args()

        scenario_runner = {
            'autogen': run_autogen_scenario,
            'memgpt': run_memgpt_scenario,
            'langchain': run_langchain_scenario,
            'crewai': run_crewai_scenario
        }
        scenario_runner[args.framework](args.scenario)
    except KeyError:
        logger.error(f"Invalid framework: {args.framework}")
        raise
    except Exception as e:
        logger.error(f"Error running scenario: {e}")
        raise

if __name__ == '__main__':
    main()