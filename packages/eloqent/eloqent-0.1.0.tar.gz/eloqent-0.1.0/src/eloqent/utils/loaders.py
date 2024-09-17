import os

import yaml


def load_assistant_config(assistant_path):
    domain_path = os.path.join(assistant_path, "domain.yaml")
    flows_path = os.path.join(assistant_path, "flows.yaml")

    with open(domain_path, "r", encoding="utf-8") as f:
        domain = yaml.safe_load(f)

    with open(flows_path, "r", encoding="utf-8") as f:
        flows = yaml.safe_load(f)

    # merge flows into domain
    domain |= flows
    return domain
