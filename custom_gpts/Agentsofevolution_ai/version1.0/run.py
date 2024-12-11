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
>>>>>>>>>>>>>>>>>>>>
    config_paths = []
>>>>>>>>>>>>>>>>>>>>>>

    for config_file in config_files:
        config_path = (company_config_dir / config_file) if company_config_dir and (company_config_dir / config_file).exists() else (default_config_dir / config_file)
        config_paths.append(config_path)

    return tuple(config_paths)

import json

def read_json_config(path):
    try:
        with path.open('r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {path}")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {path}")
    except Exception as e:
        logging.error(f"Unexpected error reading {path}: {e}")
    return None  # Return None or consider raising an exception

import argparse

parser = argparse.ArgumentParser(description="Load configurations for ChatChain.")
parser.add_argument("--company", help="Specify the company name to load its configurations.", required=True)
args = parser.parse_args()

# Assuming the get_config and read_json_config functions are defined above

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

# Start AgentsOfEvolution AI

# ----------------------------------------
#          Init ChatChain
# ----------------------------------------

# Initialize ChatChain with the paths returned by get_config
# Convert Path objects to strings if necessary (depending on ChatChain's implementation)
chat_chain = ChatChain(
    config_path=str(config_path),  # Convert Path to string if necessary
    config_phase_path=str(config_phase_path),  # Convert Path to string if necessary
    config_role_path=str(config_role_path),  # Convert Path to string if necessary
    task_prompt=args.task,
    project_name=args.name,
    org_name=args.org,
    code_path=args.path
)

# Proceed with the rest of the operations
chat_chain.pre_processing()
chat_chain.make_recruitment()
chat_chain.execute_chain()
chat_chain.post_processing()
