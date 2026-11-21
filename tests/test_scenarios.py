"""
Appendix A — 7 initial test cases from the hackathon plan.
Run with:  pytest tests/test_scenarios.py -v
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.contract_validator import load_contracts, validate_action

CONTRACTS = load_contracts()

CASES = [
    ("cloud_management_agent", "list_servers",          "cloud_inventory",    "ALLOW"),
    ("cloud_management_agent", "delete_server",         "backup_server",      "BLOCK"),
    ("cloud_management_agent", "delete_server",         "noncritical_server", "ALLOW"),
    ("research_agent",         "read_public_report",    "public_reports",     "ALLOW"),
    ("research_agent",         "read_internal_records", "internal_database",  "BLOCK"),
    ("data_management_agent",  "clean_dataset",         "approved_dataset",   "ALLOW"),
    ("data_management_agent",  "delete_dataset",        "source_dataset",     "BLOCK"),
]

def test_appendix_a_cases():
    failures = []
    for agent_id, action, resource, expected in CASES:
        result = validate_action(CONTRACTS.get(agent_id), action, resource)
        if result["decision"] != expected:
            failures.append(f"FAIL: {agent_id}.{action} expected {expected}, got {result['decision']}")
    assert not failures, "\n".join(failures)