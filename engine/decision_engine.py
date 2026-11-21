def make_decision(contract_result: dict, context_result: dict, impact_result: dict) -> dict:
    """
    Combines all stages to make a final deterministic decision.
    Priority: BLOCK > HUMAN REVIEW > ALLOW
    """
    # 1. Mandatory Restriction -> BLOCK (Risk score never overrides)
    if contract_result["decision"] == "BLOCK":
        return {
            "decision": "BLOCK",
            "explanation": contract_result["reason"]
        }

    # 2. High Impact or Unclear Context -> HUMAN REVIEW
    if impact_result["impact_level"] == "HIGH" or context_result["context_risk"] == "HIGH":
        return {
            "decision": "HUMAN REVIEW",
            "explanation": f"Action is permitted but flagged for review. Impact: {impact_result['reason']} Context: {context_result['reason']}"
        }

    # 3. Low Risk -> ALLOW
    return {
        "decision": "ALLOW",
        "explanation": "Action passed all checks: Contract valid, context safe, impact low."
    }