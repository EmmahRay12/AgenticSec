import json
from pathlib import Path
from datetime import datetime

AUDIT_FILE = Path(__file__).parent.parent / "audit_log.json"

def log_decision(agent_id: str, action: str, resource: str, decision: str, explanation: str):
    """Saves the evaluation result to a JSON file."""
    record = {
        "timestamp": datetime.now().isoformat(),
        "agent_id": agent_id,
        "action": action,
        "resource": resource,
        "decision": decision,
        "explanation": explanation
    }
    
    # Load existing logs
    logs = []
    if AUDIT_FILE.exists():
        try:
            with open(AUDIT_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
            
    # Append new log
    logs.append(record)
    
    # Save back to file
    with open(AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

def get_all_logs():
    """Returns all saved audit logs."""
    if not AUDIT_FILE.exists():
        return []
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []