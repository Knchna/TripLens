"""
TripLens - Novelty & Visited Destination Scoring Engine
Calculates destination novelty and penalizes previously visited places unless
explicitly requested by the user.
"""

def compute_novelty_score(package_destinations: str, visited_destinations: list) -> tuple[float, dict | None]:
    if not visited_destinations or not package_destinations:
        return 1.0, {"text": "Fresh destination you haven't visited before", "positive": True}

    dest_str = package_destinations.lower()
    matches = [v for v in visited_destinations if v.lower() in dest_str or dest_str in v.lower()]

    if matches:
        return 0.2, {
            "text": f"You previously visited {', '.join(matches)}",
            "positive": False
        }

    return 1.0, {
        "text": "New destination consistent with your travel style",
        "positive": True
    }
