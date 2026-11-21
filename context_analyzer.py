def analyze_context(action: str, resource: str) -> dict:
    """
    Checks if the action aligns with the known scenario facts.
    """
    # Scenario facts: certain resources are considered highly sensitive
    sensitive_resources = ["internal_database", "backup_server", "source_dataset"]
    
    if resource in sensitive_resources:
        return {
            "context_risk": "HIGH",
            "reason": f"Resource '{resource}' is marked as highly sensitive in the current context."
        }
    
    return {
        "context_risk": "LOW",
        "reason": "Context appears normal for this action."
    }