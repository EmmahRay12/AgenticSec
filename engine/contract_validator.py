import json
from pathlib import Path

CONTRACTS_DIR = Path(__file__).parent.parent / "contracts"

def load_contracts() -> dict:
    contracts = {}
    for path in CONTRACTS_DIR.glob("*.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            contracts[data["agent_id"]] = data
    return contracts

def validate_action(contract, action, resource):
    if contract is None:
        return {"decision": "BLOCK", "reason": "No contract found.", "stage": "contract"}
    for r in contract.get("restrictions", []):
        if r["action"] == action and (r["resource"] == resource or r["resource"] == "*"):
            return {"decision": "BLOCK", "reason": r["reason"], "stage": "contract"}
    for p in contract.get("permissions", []):
        if p["action"] == action and (p["resource"] == resource or p["resource"] == "*"):
            return {"decision": "ALLOW", "reason": "Permitted by contract.", "stage": "contract"}
    return {"decision": "BLOCK", "reason": "Default deny.", "stage": "contract"}