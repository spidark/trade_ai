def analyze_movement(percent_change):
    if percent_change > 2:
        return "buy"
    elif percent_change < -2:
        return "short"
    else:
        return "hold"
