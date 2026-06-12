def evaluate(param_value, condition, expected=None):
    """Evaluate a condition against a parameter value.
    Returns True if the element matches the rule (= needs highlighting)."""

    if param_value is None:
        param_value = ""

    param_value = str(param_value)

    if condition == "is_empty":
        return param_value.strip() == ""

    if condition == "is_not_empty":
        return param_value.strip() != ""

    if condition == "equals":
        return param_value == expected

    if condition == "not_equals":
        return param_value != expected

    if condition == "contains":
        return expected in param_value

    if condition == "not_contains":
        return expected not in param_value

    if condition == "greater_than":
        try:
            return float(param_value) > float(expected)
        except (ValueError, TypeError):
            return False

    if condition == "less_than":
        try:
            return float(param_value) < float(expected)
        except (ValueError, TypeError):
            return False

    return False
