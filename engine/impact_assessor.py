def assess_impact(action: str, resource: str) -> dict:
    """
    Estimates severity, reversibility, scope, and uncertainty.
    """
    # Destructive actions
    if "delete" in action or "drop" in action or "format" in action:
        return {
            "impact_level": "HIGH",
            "reversible": False,
            "reason": "Destructive action detected. Impact is potentially irreversible."
        }
    
    # Read-only actions
    if action.startswith("read") or action.startswith("list"):
        return {
            "impact_level": "LOW",
            "reversible": True,
            "reason": "Read-only action. Low impact."
        }
        
    return {
        "impact_level": "MEDIUM",
        "reversible": True,
        "reason": "Standard action with moderate impact."
    }