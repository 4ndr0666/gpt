import argparse
import json
from pathlib import Path

def get_config(company, root=Path("/mnt/data")):
    default_config_dir = root / "Default"
    company_config_dir = root / "CompanyConfig" / company if company else None

    config_files = {
        "chat_chain": "ChatChainConfig.json",
        "phase": "PhaseConfig.json",
        "role": "RoleConfig.json"
    }

    config_paths = {}
    for key, filename in config_files.items():
        if company_config_dir and (company_config_dir / filename).exists():
            config_paths[key] = company_config_dir / filename
        else:
            config_paths[key] = default_config_dir / filename

    return config_paths

def read_json_config(path):
    try:
        with path.open('r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuration file not found: {path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {path}")
    except Exception as e:
        print(f"Unexpected error reading {path}: {e}")
    return None  # Consider raising an exception for critical errors

# Set up argparse for command-line arguments
parser = argparse.ArgumentParser(description="Load configurations for ChatChain.")
parser.add_argument("--company", help="Specify the company name to load its configurations.", required=True)
parser.add_argument("--task", help="Specify the task prompt.", required=False)
parser.add_argument("--name", help="Specify the project name.", required=False)
parser.add_argument("--org", help="Specify the organization name.", required=False)
parser.add_argument("--path", help="Specify the code path.", required=False)

args = parser.parse_args()

# Load configuration paths
config_paths = get_config(args.company)

# Load the configurations
chat_chain_config = read_json_config(config_paths["chat_chain"])
phase_config = read_json_config(config_paths["phase"])
role_config = read_json_config(config_paths["role"])

# Check if all configurations are loaded successfully
if not all([chat_chain_config, phase_config, role_config]):
    print("Failed to load one or more configuration files.")
    exit(1)

# Import ChatChain class after configurations are successfully loaded
from chat_chain import ChatChain

# Initialize ChatChain with loaded configurations and additional parameters
chat_chain = ChatChain(
    chat_chain_config=chat_chain_config,  # Loaded chat chain configuration data
    phase_config=phase_config,  # Loaded phase configuration data
    role_config=role_config,  # Loaded role configuration data
    task_prompt=args.task,  # Additional parameters, if any
    project_name=args.name,
    org_name=args.org,
    code_path=args.path
)

# Execute ChatChain operations
chat_chain.pre_processing()
chat_chain.make_recruitment()
chat_chain.execute_chain()
chat_chain.post_processing()
